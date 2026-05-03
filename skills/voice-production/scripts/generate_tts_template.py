"""
TTS 생성 템플릿 — vp-voice-engineer가 프로젝트에 맞게 수정하여 사용
사용법: 이 파일을 <project>/generate_tts.py로 복사 후 경로를 수정하여 실행

핵심: dummy-suffix + auto-trim
  Qwen3-TTS는 학습 데이터(silence-trimmed)의 영향으로 문장 끝 모음이
  완전 감쇠하기 전에 EOS 토큰을 예측한다 → 마지막 음절이 cliff로 잘림.
  해결: narration 뒤에 " 네." 더미를 붙여 EOS를 뒤로 밀고,
  envelope 역스캔으로 더미 앞 silence gap을 찾아 거기서 trim.
"""
import struct
import sys
import json
import os
import shutil
import wave

import numpy as np
import soundfile as sf
import torch

# === 설정 (프로젝트에 맞게 수정) ===
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SCENE_PLAN_PATH = os.path.join(PROJECT_DIR, "_workspace/scene_plan.json")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "_workspace/tts")
RAW_DIR = os.path.join(OUTPUT_DIR, "_raw")  # trim 전 raw wav 보관(재검증용)
REF_AUDIO = os.path.expanduser("~/.claude/skills/voice-production/reference/yoojh_voice_ref.wav")
REF_TEXT = "안녕하세요 저는 AWS Technical Account Manager 유재혁 입니다"
MODEL_PATH = os.path.expanduser("~/models/Qwen3-TTS-Base")

# === Auto-trim 파라미터 (2026-05-03 개정: 중간 pause 오탐 방지) ===
DUMMY_SUFFIX = " 네."         # EOS를 뒤로 밀어 본문 tail 자연 감쇠 확보
SILENCE_THR = 200             # peak < 200 = silence (int16 기준)
LOUD_THR = SILENCE_THR * 3    # peak > LOUD_THR = 발화 중
TAIL_MARGIN_SEC = 0.10        # silence 시작 이후 이만큼 여유 두고 trim
FALLBACK_MARGIN_SEC = 0.15    # silence gap 탐지 실패 시 dummy_end에서 이만큼 앞
MIN_DUMMY_GAP_SEC = 0.08      # dummy와 본문 사이 silence gap 최소 길이
MIN_KEEP_RATIO = 0.5          # Gate A: trim 결과가 raw의 이 비율 미만이면 거부

# === 검증 가드 파라미터 ===
# Gate B: 씬별 char/sec 비율이 이 값 미만이면 재생성(음절당 너무 짧음)
MIN_CHAR_PER_SEC = 3.0        # 한국어 평균 12~15, 극단 하한을 3으로 두어 명백한 이탈만 잡음
MAX_CHAR_PER_SEC = 25.0       # 극단 상한 (평균 대비 2배)
MAX_RETRIES = 2               # Gate B 위반 시 재생성 횟수


def save_wav(out_path: str, wav, sr: int) -> None:
    arr = np.asarray(wav, dtype=np.float32)
    if arr.ndim > 1:
        arr = arr.mean(axis=-1)
    peak = float(np.max(np.abs(arr))) if arr.size else 0.0
    if peak > 1.0:
        arr = arr / peak
    sf.write(out_path, arr, sr, subtype="PCM_16")


def measure(path: str) -> float:
    with wave.open(path, "rb") as wf:
        return wf.getnframes() / float(wf.getframerate())


def find_trim_point(wav_path: str):
    """Dummy suffix가 붙은 raw wav에서 trim 지점을 찾는다.

    전략 (2026-05-03 개정: 본문 내부 pause 오탐 방지):
      1. 끝에서 역방향으로 마지막 loud 블록 = dummy_end
      2. dummy_end에서 역방향으로 peak < SILENCE_THR 로 처음 떨어지는 블록
         = dummy_silence_end (더미 발화 바로 앞 silence 진입점)
      3. 그 silence run의 시작까지 walk → silence_start (본문 tail 끝)
      4. silence gap 길이 >= MIN_DUMMY_GAP_SEC 이면 trim = silence_start + margin
         아니면 fallback: dummy_end - FALLBACK_MARGIN_SEC
      5. 본문 중간 pause(쉼표/말줄임)는 전혀 scan하지 않음 → 오탐 불가

    구버전은 MIN_SILENCE_SEC(0.25s)짜리 silence를 본문 안쪽에서 찾는 방식이라
    한국어 쉼표/말줄임/열거의 중간 pause에 오탐해 뒤쪽 음성을 통째로 잘랐음.

    리턴: (trim_frame: int|None, peaks: list[int], rate: int)
    """
    with wave.open(wav_path, "rb") as w:
        rate = w.getframerate()
        ch = w.getnchannels()
        n = w.getnframes()
        raw = w.readframes(n)

    if ch == 2:
        samples = struct.unpack(f"<{n*2}h", raw)
        mono = [max(abs(samples[k*2]), abs(samples[k*2+1])) for k in range(n)]
    else:
        samples = struct.unpack(f"<{n}h", raw)
        mono = [abs(s) for s in samples]

    block_size = int(rate * 0.02)  # 20ms block
    nblocks = n // block_size
    peaks = [max(mono[k*block_size:(k+1)*block_size]) for k in range(nblocks)]

    # 1. dummy "네"의 끝 블록 (마지막 loud 블록)
    dummy_end = None
    for i in range(nblocks - 1, -1, -1):
        if peaks[i] > LOUD_THR:
            dummy_end = i
            break
    if dummy_end is None:
        return None, peaks, rate

    # 2. dummy 발화 바로 앞 silence 진입점
    dummy_silence_end = None
    for i in range(dummy_end, -1, -1):
        if peaks[i] < SILENCE_THR:
            dummy_silence_end = i
            break
    if dummy_silence_end is None:
        trim_block = max(0, dummy_end - int(FALLBACK_MARGIN_SEC / 0.02))
        return trim_block * block_size, peaks, rate

    # 3. silence run의 시작점까지 walk
    silence_start = dummy_silence_end
    while silence_start > 0 and peaks[silence_start - 1] < SILENCE_THR:
        silence_start -= 1

    # 4. gap 길이 검증
    gap_sec = (dummy_silence_end - silence_start + 1) * 0.02
    if gap_sec < MIN_DUMMY_GAP_SEC:
        trim_block = max(0, dummy_end - int(FALLBACK_MARGIN_SEC / 0.02))
        return trim_block * block_size, peaks, rate

    trim_block = silence_start + int(TAIL_MARGIN_SEC / 0.02)
    trim_frame = trim_block * block_size
    return trim_frame, peaks, rate


def trim_and_save(raw_path: str, out_path: str):
    """raw wav에서 trim 지점을 찾아 잘라 out_path로 저장. 리턴: (ok, trim_sec, new_dur).

    Gate A: trim 결과가 raw의 MIN_KEEP_RATIO(기본 50%) 미만이면 trim 거부 →
           과잉 trim 방어 (알고리즘이 본문 내부에서 잘못된 경계를 찾는 경우 대비).
    """
    trim_frame, peaks, rate = find_trim_point(raw_path)
    if trim_frame is None:
        shutil.copyfile(raw_path, out_path)
        return False, None, measure(out_path)

    with wave.open(raw_path, "rb") as w:
        params = w.getparams()
        frames = w.readframes(w.getnframes())
        raw_dur = w.getnframes() / float(rate)

    trim_sec = trim_frame / rate
    # Gate A: 과잉 trim 방어
    if trim_sec < raw_dur * MIN_KEEP_RATIO:
        shutil.copyfile(raw_path, out_path)
        return False, trim_sec, measure(out_path)

    cut_bytes = trim_frame * params.sampwidth * params.nchannels
    trimmed = frames[:cut_bytes]

    with wave.open(out_path, "wb") as w:
        w.setparams(params)
        w.writeframes(trimmed)
    return True, trim_sec, measure(out_path)


def generate_one(model, text: str, raw_path: str) -> bool:
    """본문 뒤 DUMMY_SUFFIX 붙여 생성하고 raw_path에 저장. 1회 재시도 포함."""
    text_with_dummy = text + DUMMY_SUFFIX
    for attempt in (1, 2):
        try:
            wavs, sr = model.generate_voice_clone(
                text=text_with_dummy, ref_audio=REF_AUDIO, ref_text=REF_TEXT
            )
            save_wav(raw_path, wavs[0], int(sr))
            return True
        except Exception as e:
            print(f"       attempt {attempt} 실패: {type(e).__name__}: {e}",
                  file=sys.stderr, flush=True)
            if os.path.exists(raw_path):
                os.remove(raw_path)
    return False


def main() -> int:
    if not os.path.isdir(MODEL_PATH):
        print(f"FATAL: ~/models/Qwen3-TTS-Base가 없습니다: {MODEL_PATH}", file=sys.stderr)
        return 2
    if not os.path.exists(REF_AUDIO):
        print(f"FATAL: 레퍼런스 음성 없음: {REF_AUDIO}", file=sys.stderr)
        return 2

    with open(SCENE_PLAN_PATH, encoding="utf-8") as f:
        scenes = json.load(f)["scenes"]

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    print(f"[INFO] 씬 {len(scenes)}개, 레퍼런스: {REF_AUDIO}")
    print("[INFO] Qwen3-TTS-Base 로딩 (bfloat16)...")
    kwargs = {"dtype": torch.bfloat16}
    if torch.cuda.is_available():
        kwargs["device_map"] = "cuda:0"
    from qwen_tts import Qwen3TTSModel
    model = Qwen3TTSModel.from_pretrained(MODEL_PATH, **kwargs)
    print("[INFO] 모델 로드 완료\n")

    failures = []
    trim_fallbacks = []
    gate_b_violations = []
    for scene in scenes:
        sid = scene["id"]
        text = (scene.get("narration_tts") or scene.get("narration") or "").strip()
        out_path = os.path.join(OUTPUT_DIR, f"seg_{sid:02d}.wav")
        raw_path = os.path.join(RAW_DIR, f"seg_{sid:02d}_raw.wav")

        if not text:
            print(f"  [{sid:02d}] 내레이션 없음 — 스킵")
            continue

        print(f"  [{sid:02d}] chars={len(text)}  {text[:55]}...", flush=True)

        # Gate B 재시도 루프: char/sec 이탈 시 최대 MAX_RETRIES까지 재생성
        final_dur = None
        trim_sec = None
        trim_ok = False
        for attempt in range(MAX_RETRIES + 1):
            if not generate_one(model, text, raw_path):
                silence = np.zeros(24000 * 5, dtype=np.float32)
                save_wav(out_path, silence, 24000)
                print(f"       [FALLBACK] 5초 무음 생성", flush=True)
                failures.append(sid)
                final_dur = 5.0
                break

            trim_ok, trim_sec, final_dur = trim_and_save(raw_path, out_path)
            if not trim_ok:
                print(f"       [WARN] trim 거부 또는 탐지 실패 — raw 사용 ({final_dur:.2f}s)",
                      flush=True)
                trim_fallbacks.append(sid)

            # Gate B: char/sec 검증
            cps = len(text) / final_dur if final_dur > 0 else 0
            if MIN_CHAR_PER_SEC <= cps <= MAX_CHAR_PER_SEC:
                print(f"       → trim @ {trim_sec if trim_sec else 'N/A'}, final {final_dur:.2f}s, cps={cps:.1f}",
                      flush=True)
                break
            # Gate B 위반 — 재시도
            print(f"       [GATE-B] cps={cps:.1f} out of [{MIN_CHAR_PER_SEC},{MAX_CHAR_PER_SEC}] → 재시도 {attempt+1}/{MAX_RETRIES}",
                  flush=True)
            if attempt == MAX_RETRIES:
                gate_b_violations.append((sid, cps, final_dur, len(text)))
                print(f"       [GATE-B FAIL] 재시도 소진 — 최종 cps={cps:.1f}, 수동 확인 필요",
                      flush=True)

        if final_dur is not None:
            if final_dur < 0.5:
                print(f"       [WARN] {final_dur:.2f}s — 너무 짧음")
            if final_dur > 30.0:
                print(f"       [WARN] {final_dur:.2f}s — 너무 김 (분할 검토)")

    print()
    if failures:
        print(f"[WARN] TTS 실패(무음 대체) 씬: {failures}")
    if trim_fallbacks:
        print(f"[WARN] trim 거부/탐지 실패(raw 사용) 씬: {trim_fallbacks}")
    if gate_b_violations:
        print(f"[FATAL] Gate B 위반 (char/sec 이탈) 씬: {gate_b_violations}")
        print("        → 해당 씬은 수동 청취 확인 필요")
    if not failures and not trim_fallbacks and not gate_b_violations:
        print("[DONE] 전 씬 TTS 생성 + Gate A/B 통과")
    # Gate B 위반은 fatal로 취급 (exit code 1)
    return 0 if not failures and not gate_b_violations else 1


if __name__ == "__main__":
    sys.exit(main())

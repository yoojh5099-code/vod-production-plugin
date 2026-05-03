"""
문장별 TTS 생성 + 씬 wav concat + subtitle_timings.json 수학적 재계산.

사용법: 이 파일을 <project>/generate_tts.py로 복사 후 경로를 수정하여 실행.
(per-sentence 방식. 씬 단위 방식은 generate_tts_template.py 사용)

전략:
  1) 각 씬의 narration(자막용)과 narration_tts(TTS 입력)를 문장 단위로 분할
     - 정규식: (?<=[.?!。])(?!\\S)\\s*  (TimedSubtitle.tsx와 동일)
  2) 각 문장을 개별 Qwen3-TTS 호출로 생성 + dummy-suffix/auto-trim 적용
  3) 문장 사이 250ms silence 패딩을 둔 상태로 씬 wav concat
  4) 문장 wav 길이의 누적으로 subtitleStartsSec 수학적 계산

검증 Gate:
  - Gate A (MIN_KEEP_RATIO): trim 결과가 raw의 50% 미만이면 거부하고 raw 유지
  - Gate B (char/sec): 씬 전체 오디오 길이 대비 char/sec 검증, 위반 시 fatal
"""
from __future__ import annotations

import json
import os
import re
import shutil
import struct
import sys
import wave

import numpy as np
import soundfile as sf
import torch


# === 설정 (프로젝트에 맞게 수정) ===
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SCENE_PLAN_PATH = os.path.join(PROJECT_DIR, "_workspace/scene_plan.json")
SENT_DIR = os.path.join(PROJECT_DIR, "_workspace/tts_sentences")
SCENE_DIR = os.path.join(PROJECT_DIR, "_workspace/tts")
RAW_DIR = os.path.join(SENT_DIR, "_raw")
REF_AUDIO = os.path.join(PROJECT_DIR, "voice/voice_ref.wav")
REF_TEXT = "안녕하세요 저는 AWS Technical Account Manager 유재혁 입니다"
MODEL_PATH = os.path.expanduser("~/models/Qwen3-TTS-Base")
SUB_TIMINGS_PATH = os.path.join(PROJECT_DIR, "_workspace/subtitle_timings.json")

# === Auto-trim 파라미터 (2026-05-03 개정) ===
DUMMY_SUFFIX = " 네."
SILENCE_THR = 200
LOUD_THR = SILENCE_THR * 3
TAIL_MARGIN_SEC = 0.10
FALLBACK_MARGIN_SEC = 0.15
MIN_DUMMY_GAP_SEC = 0.08
MIN_KEEP_RATIO = 0.5

# === Gate B 파라미터 ===
MIN_CHAR_PER_SEC = 3.0
MAX_CHAR_PER_SEC = 25.0

# Inter-sentence silence padding
INTER_SENTENCE_PAD_MS = 250

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.?!。])(?!\S)\s*")


def split_sentences(text: str) -> list[str]:
    if not text:
        return []
    parts = SENTENCE_SPLIT_RE.split(text.strip())
    return [p.strip() for p in parts if p and p.strip()]


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
    """더미 " 네." 발화 구간의 시작 경계 바로 앞 silence만 본문 tail로 인정.
    본문 중간 pause(쉼표/말줄임)는 무시 → 과잉 trim 방지.
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

    block_size = int(rate * 0.02)
    nblocks = n // block_size
    peaks = [max(mono[k*block_size:(k+1)*block_size]) for k in range(nblocks)]

    dummy_end = None
    for i in range(nblocks - 1, -1, -1):
        if peaks[i] > LOUD_THR:
            dummy_end = i
            break
    if dummy_end is None:
        return None, peaks, rate

    dummy_silence_end = None
    for i in range(dummy_end, -1, -1):
        if peaks[i] < SILENCE_THR:
            dummy_silence_end = i
            break
    if dummy_silence_end is None:
        trim_block = max(0, dummy_end - int(FALLBACK_MARGIN_SEC / 0.02))
        return trim_block * block_size, peaks, rate

    silence_start = dummy_silence_end
    while silence_start > 0 and peaks[silence_start - 1] < SILENCE_THR:
        silence_start -= 1

    gap_sec = (dummy_silence_end - silence_start + 1) * 0.02
    if gap_sec < MIN_DUMMY_GAP_SEC:
        trim_block = max(0, dummy_end - int(FALLBACK_MARGIN_SEC / 0.02))
        return trim_block * block_size, peaks, rate

    trim_block = silence_start + int(TAIL_MARGIN_SEC / 0.02)
    trim_frame = trim_block * block_size
    return trim_frame, peaks, rate


def trim_and_save(raw_path: str, out_path: str):
    """Gate A: trim 결과가 raw의 MIN_KEEP_RATIO 미만이면 raw 유지."""
    trim_frame, peaks, rate = find_trim_point(raw_path)
    if trim_frame is None:
        shutil.copyfile(raw_path, out_path)
        return False, None, measure(out_path)

    with wave.open(raw_path, "rb") as w:
        params = w.getparams()
        frames = w.readframes(w.getnframes())
        raw_dur = w.getnframes() / float(rate)

    trim_sec = trim_frame / rate
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


def read_wav_samples(path: str):
    with wave.open(path, "rb") as w:
        p = w.getparams()
        frames = w.readframes(w.getnframes())
    return frames, p


def concat_scene(sentence_paths: list[str], out_path: str, pad_ms: int):
    all_frames = b""
    common_params = None
    for i, p in enumerate(sentence_paths):
        frames, params = read_wav_samples(p)
        if common_params is None:
            common_params = params
        all_frames += frames
        if i != len(sentence_paths) - 1:
            pad_samples = int(common_params.framerate * pad_ms / 1000)
            silence_bytes = b"\x00\x00" * pad_samples * common_params.nchannels
            all_frames += silence_bytes

    with wave.open(out_path, "wb") as w:
        w.setparams(common_params)
        w.writeframes(all_frames)


def main() -> int:
    if not os.path.isdir(MODEL_PATH):
        print(f"FATAL: ~/models/Qwen3-TTS-Base가 없습니다: {MODEL_PATH}", file=sys.stderr)
        return 2
    if not os.path.exists(REF_AUDIO):
        print(f"FATAL: 레퍼런스 음성 없음: {REF_AUDIO}", file=sys.stderr)
        return 2

    with open(SCENE_PLAN_PATH, encoding="utf-8") as f:
        scenes = json.load(f)["scenes"]

    os.makedirs(SENT_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(SCENE_DIR, exist_ok=True)

    scene_sentences = []
    for sc in scenes:
        disp = split_sentences(sc.get("narration", ""))
        tts_text = sc.get("narration_tts") or sc.get("narration", "")
        tts_list = split_sentences(tts_text)
        if len(disp) != len(tts_list):
            print(f"[WARN] 씬 {sc['id']}: display({len(disp)}) != tts({len(tts_list)}) — narration만 사용")
            tts_list = disp
        scene_sentences.append((sc["id"], disp, tts_list, tts_text))

    total_sentences = sum(len(s[1]) for s in scene_sentences)
    print(f"[INFO] 씬 {len(scenes)}개, 총 문장 {total_sentences}개")

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
    subtitle_timings: dict[str, dict] = {}

    for sid, disp_list, tts_list, scene_tts_text in scene_sentences:
        print(f"[Scene {sid:02d}] {len(tts_list)}개 문장")
        sentence_paths: list[str] = []
        durations: list[float] = []

        for i, (sent_disp, sent_tts) in enumerate(zip(disp_list, tts_list)):
            raw_path = os.path.join(RAW_DIR, f"seg_{sid:02d}_sent_{i:02d}_raw.wav")
            sent_path = os.path.join(SENT_DIR, f"seg_{sid:02d}_sent_{i:02d}.wav")
            text = sent_tts.strip()
            if not text:
                continue
            print(f"  [{sid:02d}.{i:02d}] chars={len(text)}  {text[:55]}...", flush=True)

            if not generate_one(model, text, raw_path):
                silence = np.zeros(24000 * 3, dtype=np.float32)
                save_wav(sent_path, silence, 24000)
                failures.append((sid, i))
                print("       [FALLBACK] 3초 무음 생성", flush=True)
            else:
                ok, trim_sec, new_dur = trim_and_save(raw_path, sent_path)
                if not ok:
                    trim_fallbacks.append((sid, i))
                    print(f"       [WARN] trim 실패/거부 — raw 사용 ({new_dur:.2f}s)", flush=True)
                else:
                    print(f"       → trim @ {trim_sec:.2f}s, final {new_dur:.2f}s", flush=True)
            sentence_paths.append(sent_path)
            durations.append(measure(sent_path))

        # concat 씬 wav
        scene_wav = os.path.join(SCENE_DIR, f"seg_{sid:02d}.wav")
        concat_scene(sentence_paths, scene_wav, INTER_SENTENCE_PAD_MS)
        scene_dur = measure(scene_wav)

        # Gate B: 씬 전체 char/sec 검증
        scene_chars = len(scene_tts_text.strip())
        cps = scene_chars / scene_dur if scene_dur > 0 else 0
        if not (MIN_CHAR_PER_SEC <= cps <= MAX_CHAR_PER_SEC):
            gate_b_violations.append((sid, cps, scene_dur, scene_chars))
            print(f"       [GATE-B FAIL] 씬 {sid:02d} cps={cps:.1f} out of [{MIN_CHAR_PER_SEC},{MAX_CHAR_PER_SEC}]", flush=True)

        # subtitleStartsSec 수학 계산 (pad 포함)
        starts: list[float] = []
        cursor = 0.0
        for i, d in enumerate(durations):
            starts.append(round(cursor, 3))
            cursor += d
            if i != len(durations) - 1:
                cursor += INTER_SENTENCE_PAD_MS / 1000.0

        expected = sum(durations) + (len(durations) - 1) * INTER_SENTENCE_PAD_MS / 1000.0
        diff = abs(scene_dur - expected)
        print(f"       scene dur={scene_dur:.3f}s cps={cps:.1f} (expected {expected:.3f}s, diff {diff*1000:.1f}ms)")

        subtitle_timings[str(sid)] = {
            "subtitleStartsSec": starts,
            "audioDuration": round(scene_dur, 3),
            "sentences": disp_list,
        }

    with open(SUB_TIMINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(subtitle_timings, f, ensure_ascii=False, indent=2)

    print()
    if failures:
        print(f"[WARN] TTS 실패 문장: {failures}")
    if trim_fallbacks:
        print(f"[WARN] trim 거부/탐지 실패 문장(raw 사용): {trim_fallbacks}")
    if gate_b_violations:
        print(f"[FATAL] Gate B 위반 씬: {gate_b_violations}")
        print("        → 해당 씬은 수동 청취 확인 필요")
    if not failures and not trim_fallbacks and not gate_b_violations:
        print("[DONE] 전 문장 TTS 생성 + Gate A/B 통과 + 씬 concat 완료")
    print(f"[DONE] subtitle_timings → {SUB_TIMINGS_PATH}")
    return 0 if not failures and not gate_b_violations else 1


if __name__ == "__main__":
    sys.exit(main())

"""
타이밍 측정 템플릿 — vp-voice-engineer가 프로젝트에 맞게 수정하여 사용
사용법: 이 파일을 <project>/generate_timing.py로 복사 후 경로를 수정하여 실행
"""
import wave
import json
import os
import sys

# === 설정 (프로젝트에 맞게 수정) ===
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SCENE_PLAN_PATH = os.path.join(PROJECT_DIR, "_workspace/scene_plan.json")
TTS_DIR = os.path.join(PROJECT_DIR, "_workspace/tts")
OUTPUT_PATH = os.path.join(PROJECT_DIR, "_workspace/timing.json")
PADDING_SEC = 0.6       # 씬 간 여유 패딩 (전환 시 목소리 끊김 방지)
LAST_SCENE_PAD = 0.3    # 마지막 씬은 꼬리 공백 줄이기 위해 짧게

def get_wav_duration(wav_path):
    """WAV 파일의 실제 오디오 길이(초)를 반환한다."""
    with wave.open(wav_path, 'r') as w:
        frames = w.getnframes()
        rate = w.getframerate()
        return frames / rate

def main():
    # 씬 플랜 로드
    with open(SCENE_PLAN_PATH, "r", encoding="utf-8") as f:
        scene_plan = json.load(f)

    scenes = scene_plan["scenes"]
    timing = []
    current_sec = 0.0
    long_segments = []  # 10초 초과 세그먼트 추적

    print(f"총 {len(scenes)}개 씬 타이밍 측정 시작")

    for i, scene in enumerate(scenes):
        seg_id = scene["id"]
        is_last = (i == len(scenes) - 1)
        pad = LAST_SCENE_PAD if is_last else PADDING_SEC
        wav_path = os.path.join(TTS_DIR, f"seg_{seg_id:02d}.wav")

        if not os.path.exists(wav_path):
            print(f"  [WARN] seg_{seg_id:02d}.wav 없음 — 5초 기본값 사용", file=sys.stderr)
            audio_duration = 5.0
        else:
            audio_duration = get_wav_duration(wav_path)

        # 검증
        if audio_duration < 0.5:
            print(f"  [WARN] seg_{seg_id:02d} 너무 짧음: {audio_duration:.2f}초", file=sys.stderr)
        if audio_duration > 30:
            print(f"  [WARN] seg_{seg_id:02d} 너무 김: {audio_duration:.2f}초", file=sys.stderr)

        duration_with_padding = audio_duration + pad

        # 10초 초과 세그먼트 추적
        if audio_duration > 10:
            long_segments.append({"id": seg_id, "duration": round(audio_duration, 2)})

        timing.append({
            "id": seg_id,
            "startSec": round(current_sec, 3),
            "durationSec": round(duration_with_padding, 3),
            "audioDuration": round(audio_duration, 3),
            "subtitle": scene.get("subtitle", ""),
            "narration": scene.get("narration", ""),
            "visual_desc": scene.get("visual_note", "")
        })

        current_sec += duration_with_padding
        print(f"  [{seg_id:02d}] {audio_duration:.2f}초 (시작: {timing[-1]['startSec']}초)")

    # timing.json 저장
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(timing, f, ensure_ascii=False, indent=2)

    total_duration = round(current_sec, 2)
    print(f"\n타이밍 측정 완료")
    print(f"  총 세그먼트: {len(timing)}개")
    print(f"  총 길이: {total_duration}초 ({total_duration//60:.0f}분 {total_duration%60:.0f}초)")
    print(f"  저장: {OUTPUT_PATH}")

    if long_segments:
        print(f"\n  ⚠ 10초 초과 세그먼트 ({len(long_segments)}개):")
        for seg in long_segments:
            print(f"    - 씬 {seg['id']}: {seg['duration']}초 → 이미지 추가 필요")

if __name__ == "__main__":
    main()

"""
사용자 직접 녹음 워크플로 전용 타이밍 측정 스크립트.

입력:  <project>/_workspace/scene_plan.json (cp-scene-architect 산출)
       <project>/_workspace/tts/seg_NN.wav (normalize_recordings.sh 산출)
출력:  <project>/_workspace/timing.json

사용법: python3 generate_timing.py [<project_root>]
       기본 project_root는 현재 디렉터리.

PADDING_SEC=0.3 디폴트는 사람 직접 녹음 + narration only 영상에 맞춤.
TTS 합성보다 씬간 톤·볼륨 편차가 약간 있어 0.6초 무음이 답답하게 들린다는
사용자 피드백 누적 결과 (claude-vs-codex 프로젝트 §10.4).

답답하면 PADDING_SEC=0.4, 너무 빠르면 PADDING_SEC=0.2로 미세 조정 후 재실행.
"""
import wave
import json
import os
import sys

# === 사람 직접 녹음 + narration only 표준값 ===
PADDING_SEC = 0.3       # 씬 간 여유 패딩
LAST_SCENE_PAD = 0.3    # 마지막 씬도 동일 (TTS 워크플로는 0.3이지만 사람은 균일이 자연)


def get_wav_duration(wav_path):
    with wave.open(wav_path, "r") as w:
        return w.getnframes() / w.getframerate()


def main():
    project_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    scene_plan_path = os.path.join(project_root, "_workspace/scene_plan.json")
    tts_dir = os.path.join(project_root, "_workspace/tts")
    output_path = os.path.join(project_root, "_workspace/timing.json")

    if not os.path.exists(scene_plan_path):
        print(f"[FATAL] scene_plan.json 없음: {scene_plan_path}", file=sys.stderr)
        sys.exit(1)

    with open(scene_plan_path, "r", encoding="utf-8") as f:
        scene_plan = json.load(f)

    scenes = scene_plan["scenes"]
    timing = []
    current_sec = 0.0
    long_segments = []
    missing_wavs = []

    print(f"[timing] 총 {len(scenes)}개 씬 측정 (PADDING_SEC={PADDING_SEC})")

    for i, scene in enumerate(scenes):
        seg_id = scene["id"]
        is_last = i == len(scenes) - 1
        pad = LAST_SCENE_PAD if is_last else PADDING_SEC
        wav_path = os.path.join(tts_dir, f"seg_{seg_id:02d}.wav")

        if not os.path.exists(wav_path):
            print(f"  [WARN] seg_{seg_id:02d}.wav 없음 — 5초 기본값 사용", file=sys.stderr)
            audio_duration = 5.0
            missing_wavs.append(seg_id)
        else:
            audio_duration = get_wav_duration(wav_path)

        if audio_duration < 0.5:
            print(f"  [WARN] seg_{seg_id:02d} 너무 짧음: {audio_duration:.2f}초", file=sys.stderr)
        if audio_duration > 30:
            print(f"  [WARN] seg_{seg_id:02d} 너무 김: {audio_duration:.2f}초", file=sys.stderr)

        duration_with_padding = audio_duration + pad

        if audio_duration > 10:
            long_segments.append({"id": seg_id, "duration": round(audio_duration, 2)})

        timing.append({
            "id": seg_id,
            "startSec": round(current_sec, 3),
            "durationSec": round(duration_with_padding, 3),
            "audioDuration": round(audio_duration, 3),
            "subtitle": scene.get("subtitle", ""),
            "narration": scene.get("narration", ""),
            "visual_desc": scene.get("visual_note", ""),
        })
        current_sec += duration_with_padding
        print(f"  [{seg_id:02d}] {audio_duration:.2f}s (start {timing[-1]['startSec']}s)")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(timing, f, ensure_ascii=False, indent=2)

    total_duration = round(current_sec, 2)
    minutes = int(total_duration // 60)
    seconds = int(total_duration % 60)
    print(f"\n[timing] 완료")
    print(f"  총 세그먼트: {len(timing)}개")
    print(f"  총 길이: {total_duration}s ({minutes}분 {seconds}초)")
    print(f"  저장: {output_path}")

    if long_segments:
        print(f"\n  ⚠ 10초 초과 세그먼트 ({len(long_segments)}개):")
        for seg in long_segments:
            print(f"    - 씬 {seg['id']}: {seg['duration']}초 → stage reveal 분리 검토")

    if missing_wavs:
        print(f"\n[FATAL] {len(missing_wavs)}개 wav 누락: {missing_wavs}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

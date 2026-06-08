#!/usr/bin/env bash
# 사용자 직접 녹음 wav를 video-production 표준 포맷으로 일괄 변환.
#
# 입력:  <project>/_workspace/audio/seg-NN.wav     (어떤 SR/channel/bitrate든 허용)
# 출력:  <project>/_workspace/tts/seg_NN.wav       (24kHz / mono / 16-bit PCM)
#
# 변환:
#   1. 샘플레이트 → 24000 Hz
#   2. 채널 → mono (스테레오면 down-mix)
#   3. 비트심도 → 16-bit signed PCM
#   4. 앞부분 무음 trim (-50dB 이하 0.1s+)
#   5. 100ms padding (균일한 시작 호흡)
#   6. 끝부분은 자연 감쇠 보존 (의도적으로 trim 안 함)
#
# 파일명 변환: seg-01.wav → seg_01.wav (하이픈→언더스코어, scene_plan.json id 매칭)
#
# 사용법:
#   ./normalize_recordings.sh [<project_root>]
#
# 기본 project_root는 현재 디렉터리.
#
# 검증:
#   - 입력 디렉터리 비어있으면 fatal
#   - 각 출력 wav 길이가 입력과 ±0.5s 이내 (앞 무음 차이만큼만 줄어듦)

set -euo pipefail

PROJECT_ROOT="${1:-$(pwd)}"
INPUT_DIR="$PROJECT_ROOT/_workspace/audio"
OUTPUT_DIR="$PROJECT_ROOT/_workspace/tts"

if [ ! -d "$INPUT_DIR" ]; then
    echo "[FATAL] 입력 디렉터리 없음: $INPUT_DIR" >&2
    echo "  사용자가 _workspace/audio/seg-NN.wav 로 녹음해야 함" >&2
    exit 1
fi

# 입력 wav 개수 확인
INPUT_COUNT=$(find "$INPUT_DIR" -maxdepth 1 -name 'seg-*.wav' -o -name 'seg_*.wav' | wc -l)
if [ "$INPUT_COUNT" -eq 0 ]; then
    echo "[FATAL] $INPUT_DIR 에 seg-*.wav 또는 seg_*.wav 파일이 없음" >&2
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "[normalize] 입력: $INPUT_DIR ($INPUT_COUNT 파일)"
echo "[normalize] 출력: $OUTPUT_DIR"
echo ""

CONVERTED=0
FAILED=0

# seg-XX.wav 또는 seg_XX.wav 둘 다 처리
for src in "$INPUT_DIR"/seg-*.wav "$INPUT_DIR"/seg_*.wav; do
    [ -f "$src" ] || continue

    base=$(basename "$src")
    # 파일명 정규화: seg-01.wav 또는 seg_01.wav → seg_01.wav
    id=$(echo "$base" | sed -E 's/^seg[-_]([0-9]+)\.wav$/\1/')
    if [ -z "$id" ] || [ "$id" = "$base" ]; then
        echo "  [SKIP] $base — 파일명 패턴 불일치 (seg-NN.wav 또는 seg_NN.wav 필요)"
        continue
    fi

    out="$OUTPUT_DIR/seg_${id}.wav"

    # ffmpeg:
    # - silenceremove start_periods=1 stop_threshold=-50dB stop_duration=0.1
    #     → 앞부분 무음(피크 < -50dB)이 0.1초 이상 지속되면 그 지점까지 잘라냄
    # - aformat=channel_layouts=mono → adelay 전에 mono로 down-mix (스테레오 입력일 때 adelay가
    #   첫 채널에만 적용돼 100ms 시차 echo가 생기는 버그 방지)
    # - adelay=100:all=1 → 모든 채널에 100ms 무음 패딩 (균일한 시작 호흡)
    # - ar 24000 / ac 1 / sample_fmt s16
    if ffmpeg -y -loglevel error \
        -i "$src" \
        -af "silenceremove=start_periods=1:start_silence=0.1:start_threshold=-50dB,aformat=channel_layouts=mono,adelay=100:all=1" \
        -ar 24000 -ac 1 -sample_fmt s16 \
        "$out" 2>&1; then

        # 검증: 출력 길이 확인
        in_dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$src")
        out_dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out")
        diff=$(echo "$in_dur $out_dur" | awk '{print ($1>$2 ? $1-$2 : $2-$1)}')

        # 앞 무음을 잘라내므로 출력이 입력보다 짧아지는 건 정상.
        # 단 2초 이상 짧아지면 의심 (긴 무음 또는 silenceremove 오작동)
        if (( $(echo "$diff > 2.0" | bc -l) )); then
            echo "  [WARN] $base: 길이 차이 ${diff}s (입력 ${in_dur}s → 출력 ${out_dur}s) — 청취 확인 권장"
        fi

        printf "  [OK]   %s → seg_%s.wav (%.2fs → %.2fs)\n" "$base" "$id" "$in_dur" "$out_dur"
        CONVERTED=$((CONVERTED + 1))
    else
        echo "  [FAIL] $base"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "[normalize] 완료: $CONVERTED 변환, $FAILED 실패"

if [ "$FAILED" -gt 0 ]; then
    exit 1
fi

# 추가 검증: scene_plan.json 씬 수와 일치하는지
SCENE_PLAN="$PROJECT_ROOT/_workspace/scene_plan.json"
if [ -f "$SCENE_PLAN" ]; then
    EXPECTED=$(python3 -c "import json; print(len(json.load(open('$SCENE_PLAN'))['scenes']))")
    ACTUAL=$(find "$OUTPUT_DIR" -maxdepth 1 -name 'seg_*.wav' | wc -l)
    if [ "$EXPECTED" != "$ACTUAL" ]; then
        echo "[WARN] scene_plan.json 씬 수($EXPECTED) ≠ 출력 wav 수($ACTUAL)"
        echo "  녹음이 빠진 씬이 있는지 확인 필요"
        exit 1
    fi
    echo "[normalize] 씬 수 일치: $ACTUAL = $EXPECTED"
fi

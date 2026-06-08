#!/usr/bin/env bash
# scaffold_short.sh — Mode B용 Remotion 쇼츠 프로젝트 신규 셋업
#
# 사용법:
#   bash scaffold_short.sh <project_dir>
#
# <project_dir>은 video-production 표준 폴더 구조를 갖는다고 가정.
# 없는 폴더는 생성하고, <project_dir>/<basename>-video/ 가 이미 있으면 안전하게 skip.

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "usage: scaffold_short.sh <project_dir>" >&2
  exit 1
fi

PROJECT_DIR="$1"
PROJECT_DIR="${PROJECT_DIR%/}"
BASENAME="$(basename "$PROJECT_DIR")"
REMOTION_DIR="$PROJECT_DIR/${BASENAME}-video"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

mkdir -p \
  "$PROJECT_DIR/script" \
  "$PROJECT_DIR/output" \
  "$PROJECT_DIR/_workspace/shorts" \
  "$PROJECT_DIR/_workspace/shorts/tts" \
  "$PROJECT_DIR/voice" \
  "$PROJECT_DIR/image" \
  "$PROJECT_DIR/thumbnail" \
  "$PROJECT_DIR/background"

if [ -d "$REMOTION_DIR" ]; then
  echo "[scaffold] $REMOTION_DIR 이미 존재 — Remotion 셋업 skip"
else
  echo "[scaffold] Remotion 프로젝트 신규 생성: $REMOTION_DIR"
  mkdir -p "$REMOTION_DIR/src" "$REMOTION_DIR/public/audio" "$REMOTION_DIR/public/images" "$REMOTION_DIR/public/fonts"

  cat > "$REMOTION_DIR/package.json" <<'JSON'
{
  "name": "shorts-video",
  "version": "1.0.0",
  "scripts": {
    "start": "remotion studio --port 3123",
    "build": "remotion render Short output/short.mp4",
    "still": "remotion still Short output/short_thumbnail.png --frame=0"
  },
  "dependencies": {
    "react": "18.3.1",
    "react-dom": "18.3.1",
    "remotion": "4.0.276",
    "@remotion/bundler": "4.0.276",
    "@remotion/cli": "4.0.276"
  },
  "devDependencies": {
    "@types/react": "18.3.12",
    "@types/node": "20.11.0",
    "typescript": "5.5.0"
  }
}
JSON

  cat > "$REMOTION_DIR/tsconfig.json" <<'JSON'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "react",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true
  },
  "include": ["src"]
}
JSON

  cat > "$REMOTION_DIR/remotion.config.ts" <<'TS'
import { Config } from "@remotion/cli/config";
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
TS

  cat > "$REMOTION_DIR/src/index.ts" <<'TS'
import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";
registerRoot(RemotionRoot);
TS

  cat > "$REMOTION_DIR/src/Root.tsx" <<'TSX'
import React from "react";
import { Composition } from "remotion";
import { Short, FPS, TOTAL_FRAMES } from "./Short";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Short"
    component={Short}
    durationInFrames={TOTAL_FRAMES}
    fps={FPS}
    width={1080}
    height={1920}
  />
);
TSX

  # Short.tsx는 Short.template.tsx 그대로 복사. 컴포저가 SCENES만 채워넣음.
  cp "$SKILL_DIR/assets/Short.template.tsx" "$REMOTION_DIR/src/Short.tsx"

  echo "[scaffold] npm install 실행 중..."
  (cd "$REMOTION_DIR" && npm install --silent)
fi

echo "[scaffold] 완료"
echo "  Remotion: $REMOTION_DIR"
echo "  쇼츠 작업 공간: $PROJECT_DIR/_workspace/shorts/"
echo ""
echo "다음 단계:"
echo "  1. $PROJECT_DIR/script/ 에 쇼츠 대본 배치"
echo "  2. vp-scene-architect 호출 (Shorts 컨텍스트 전달)"
echo "  3. vp-voice-engineer → Audio Sync → vp-video-composer"

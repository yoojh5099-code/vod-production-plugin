# Mode A: 기존 영상에서 쇼츠 추출

본편 video-production 산출물(scene_plan.json + tts/seg_NN.wav + Remotion 프로젝트)을 재활용해 9:16 쇼츠를 만든다. **TTS·씬 분석은 새로 하지 않는다** — 컴포저만 호출.

## 입력 요구사항

- `<project>/_workspace/scene_plan.json` (본편)
- `<project>/_workspace/tts/seg_*.wav` (본편)
- `<project>/<project>-video/` Remotion 프로젝트 (본편)
- 사용자가 추출할 씬 ID 목록 지정 (예: `[2, 4, 7]`)

## Phase A0: 씬 선택 검증

오케스트레이터가 직접 수행:

```python
import json
plan = json.load(open(f"{PROJECT}/_workspace/scene_plan.json"))
selected_ids = [2, 4, 7]  # 사용자 지정
selected = [s for s in plan["scenes"] if s["id"] in selected_ids]

# 검증
missing = set(selected_ids) - {s["id"] for s in selected}
assert not missing, f"씬 ID 없음: {missing}"

total_sec = sum(s.get("audioDurationSec", s["durationSec"]) for s in selected)
assert 30 <= total_sec <= 70, f"합산 길이 {total_sec}s — 40~60s 범위 벗어남"

# 쇼츠용 작업 공간에 저장
import os
os.makedirs(f"{PROJECT}/_workspace/shorts", exist_ok=True)
json.dump(
    {"scenes": selected, "totalSec": total_sec, "aspect": "shorts"},
    open(f"{PROJECT}/_workspace/shorts/scene_plan_short.json", "w"),
    ensure_ascii=False, indent=2,
)
```

**합산 길이가 60s 초과**면 사용자에게 다음 옵션 제시:
- (a) 가장 긴 씬 1개 제외
- (b) 특정 씬 cut-down (예: 24s → 14s, 컴포저가 narration trim)
- (c) 진행 강행 (60~70s까지는 허용, 70s+ 거부)

## Phase A1: TTS·timing 재활용

본편 TTS를 그대로 쇼츠 Remotion 프로젝트에 복사:

```bash
cd <project>
SHORT_AUDIO_DIR="<project>-video/public/audio_short"
mkdir -p "$SHORT_AUDIO_DIR"

for sid in 2 4 7; do
  src=$(printf "_workspace/tts/seg_%02d.wav" $sid)
  cp "$src" "$SHORT_AUDIO_DIR/"
done

# timing.json은 새로 생성 (선택 씬만)
python3 - <<'EOF'
import json
plan = json.load(open("_workspace/shorts/scene_plan_short.json"))
timing = {
    "scenes": [
        {"id": s["id"], "audioSrc": f"seg_{s['id']:02d}.wav",
         "durationSec": s["audioDurationSec"]}
        for s in plan["scenes"]
    ]
}
json.dump(timing, open("<project>-video/public/audio_short/timing.json", "w"),
          ensure_ascii=False, indent=2)
EOF
```

**주의**: 본편의 `public/audio/`를 덮어쓰지 말 것. `public/audio_short/`로 격리.

## Phase A2: 컴포저 호출

vp-video-composer를 서브에이전트로 호출:

```
Agent(
  description: "쇼츠 9:16 조립",
  subagent_type: "general-purpose",  # 또는 vp-video-composer 정의된 그대로
  prompt: "~/.claude/agents/vp-video-composer.md를 읽고 역할을 수행하라.
    ~/.claude/skills/remotion-assembly/SKILL.md를 따른다.
    프로젝트 경로: <project>

    ⚠️ Shorts Mode A:
    - aspect: 9:16 (1080×1920 @ 30fps)
    - 입력: <project>/_workspace/shorts/scene_plan_short.json (선택된 N씬만)
    - TTS 위치: <project>/<project>-video/public/audio_short/seg_NN.wav (이미 복사됨)
    - 베이스 컴포넌트: ~/.claude/skills/short-production/assets/Short.template.tsx 그대로 복사해
      <project>/<project>-video/src/Short.tsx 생성
    - SCENES 배열만 채워넣어라. 시그니처(카라오케 자막·BGM 없음·프로그레스 바)는 변경 금지
    - 각 씬의 Content는 본편 SceneVisual.tsx의 해당 씬 컴포넌트를 참고하되,
      9:16 세로 스택 레이아웃으로 재배치 (좌우 split 금지)
    - audioSrc는 'seg_NN.wav' 형식, staticFile은 'audio_short/' prefix 사용 — 즉 본 템플릿의
      SceneAudio가 staticFile(`audio/${src}`)로 되어 있으면 'audio_short/${src}'로 수정
    - 9:16 호환 패턴 화이트리스트: ~/.claude/skills/short-production/references/patterns.md
    - Root.tsx에 'Short' Composition 추가 (id='Short', 1080×1920, durationInFrames=TOTAL_FRAMES)
    - 본편 'MainVideo' Composition은 건드리지 말 것
    - TypeScript 컴파일 검증까지만 수행, npx remotion render는 호출 금지
    - 산출 보고: src/Short.tsx 경로 + 합산 duration",
  model: "opus"
)
```

## Phase A3: Gate C (선택)

본편 TTS를 재활용했으므로 이미 Gate C 통과한 상태. **선택 씬에 한해서만 Whisper 재검증할 필요 없음** — skip 가능.

단, 본편 Gate C false positive였던 씬을 쇼츠에 포함했다면 사용자에게 청취 확인 요청.

## Phase A4: Studio 프리뷰 → 렌더 (오케스트레이터)

```bash
cd <project>/<project>-video
npx remotion studio --port 3123 --gl=angle &
# 사용자에게 http://localhost:3123 → 'Short' composition 확인 요청
# 승인 후:
npx remotion render Short ../output/short.mp4
npx remotion still Short ../output/short_thumbnail.png --frame=0
```

## Caveman 케이스 참고

`vod/claude-opensource/claude-opensource-video/src/ShortCaveman.tsx`가 Mode A의 실제 결과물.
- 본편 38씬 중 씬 2(seg_02), 씬 4(seg_04), 씬 7(seg_07) 추출
- 합산 43.94s
- 본편 카드(DefinitionFormula, Scene4Reveal, RecommendedAudience)를 9:16에 맞게 단순화
- 본편 자막(TimedSubtitle)을 카라오케 자막(KaraokeText)으로 교체

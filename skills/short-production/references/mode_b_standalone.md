# Mode B: 단독 쇼츠 제작

본편 없이 쇼츠 전용 짧은 대본 하나로 9:16 영상을 만든다. video-production의 5 Phase를 그대로 따르되 9:16 컨텍스트로 분기.

## 입력 요구사항

- `<project>/script/short.md` (또는 `short_*.md`) — 40~60s 분량 대본
- `<project>/voice/` voice reference (선택, 없으면 default)

## Phase B0: 스캐폴딩

```bash
bash ~/.claude/skills/short-production/assets/scaffold_short.sh <project>
```

이 스크립트가:
- 폴더 구조 생성: `script/`, `output/`, `_workspace/shorts/`, `_workspace/shorts/tts/`, `voice/`, `image/` 등
- `<project>/<project>-video/` Remotion 프로젝트 신규 셋업 (이미 있으면 skip)
- `Short.tsx`를 `Short.template.tsx`로 초기화
- `Root.tsx`에 `Short` Composition 등록 (1080×1920 @ 30fps)
- `npm install`

## Phase B1: 씬 분석 (vp-scene-architect)

```
Agent(
  description: "쇼츠 씬 분석",
  prompt: "~/.claude/agents/vp-scene-architect.md를 읽고 역할을 수행하라.
    ~/.claude/skills/scene-analysis/SKILL.md를 따른다.
    프로젝트 경로: <project>
    대본: <project>/script/short.md

    ⚠️ Shorts Mode B:
    - aspect: 9:16 (1080×1920)
    - target_duration: 40~60s (총합)
    - 권장 막 구성: 3~4막. 도구 소개면 WHAT/HOW/WHO 3막 고정 권장
    - 9:16 호환 패턴만 사용 — ~/.claude/skills/short-production/references/patterns.md 화이트리스트
    - iPad 템플릿 금지, 좌우 split 금지, QuadrantMatrix·LethalTriangle·HorseHarness 금지
    - 다이버시티 예산은 쇼츠 길이에 맞게 축소: signature 1회·special 1회·generic 2회 이하
    - BGM은 사용하지 않음 (scene_plan에 bgm 필드 비울 것)

    산출물:
      1. <project>/_workspace/shorts/scene_plan.json (visual + visual_category + visual_tier 포함)
      2. <project>/_workspace/shorts/visual_allocation_audit.md
    
    합산 duration이 60s 초과 추정이면 narration 압축 시도.
    압축 실패 시 사용자에게 보고하고 중단.",
  model: "opus"
)
```

**검증**:
- `_workspace/shorts/scene_plan.json` 존재
- 모든 씬의 `visual`이 화이트리스트에 포함
- 합산 추정 duration이 40~70s 범위

## Phase B2: TTS 생성 (vp-voice-engineer)

```
Agent(
  description: "쇼츠 TTS 생성",
  prompt: "~/.claude/agents/vp-voice-engineer.md를 읽고 역할을 수행하라.
    ~/.claude/skills/voice-production/SKILL.md를 따른다.
    프로젝트 경로: <project>
    
    ⚠️ Shorts 작업 공간:
    - scene_plan: <project>/_workspace/shorts/scene_plan.json
    - 출력: <project>/_workspace/shorts/tts/seg_NN.wav + <project>/_workspace/shorts/timing.json
    - 영문→한글 발음 치환 동일 적용 (narration_tts 필드)
    - Gate A/B 동일 적용",
  model: "opus"
)
```

**검증**: 본편과 동일 (Gate A/B 통과, exit code 0).

## Phase B2.1: Audio Sync (오케스트레이터 직접)

```bash
cd <project>
REMOTION_DIR=$(ls -d *-video 2>/dev/null | head -1)
mkdir -p "$REMOTION_DIR/public/audio"
cp _workspace/shorts/tts/seg_*.wav "$REMOTION_DIR/public/audio/"
cp _workspace/shorts/timing.json "$REMOTION_DIR/public/audio/timing.json"
```

Mode B는 본편 audio 디렉터리와 충돌 없음 (본편이 없으므로). 그냥 `public/audio/` 사용.

## Phase B3: 영상 조립 (vp-video-composer)

```
Agent(
  description: "쇼츠 9:16 조립",
  prompt: "~/.claude/agents/vp-video-composer.md를 읽고 역할을 수행하라.
    ~/.claude/skills/remotion-assembly/SKILL.md를 따른다.
    프로젝트 경로: <project>

    ⚠️ Shorts Mode B:
    - aspect: 9:16 (1080×1920 @ 30fps)
    - scene_plan: <project>/_workspace/shorts/scene_plan.json
    - 베이스 컴포넌트: <project>/<project>-video/src/Short.tsx (이미 scaffold로 초기화됨)
    - SCENES 배열만 채워넣어라. 각 씬의 Content는 화이트리스트 패턴으로 구현
    - 시그니처 컴포넌트(KaraokeText, ProgressBar, SectionLabelOverlay)는 변경 금지
    - 9:16 호환 패턴: ~/.claude/skills/short-production/references/patterns.md
    - 브랜드 로고 자동 매칭은 동일 적용
      (~/.claude/skills/remotion-assembly/references/brand-logos/manifest.yml)
    - TypeScript 컴파일 검증까지만, npx remotion render 호출 금지

    산출 보고: src/Short.tsx 경로 + 합산 duration",
  model: "opus"
)
```

## Phase B3.5: Gate C (Whisper)

본편과 동일. `<project>-video/public/audio/` 기준으로 Whisper 전사 → narration_tts 마지막 15자 검증.

video-production SKILL.md의 Gate C 스크립트를 그대로 사용.

## Phase B4: Studio → 렌더 (오케스트레이터)

```bash
cd <project>/<project>-video
npx remotion studio --port 3123 --gl=angle &
# 사용자 승인 대기
npx remotion render Short ../output/short.mp4
npx remotion still Short ../output/short_thumbnail.png --frame=0
```

## Phase B5: 완료 보고

```
✅ 쇼츠 제작 완료
- 영상: <project>/output/short.mp4
- 썸네일: <project>/output/short_thumbnail.png
- Remotion: <project>/<project>-video/
- 씬 수: N개, 길이: M초
```

## 모드 B 사용 시점

- 본편을 만들 계획 없음 (쇼츠만 단발성)
- 본편 대본의 일부가 아니라 쇼츠 전용 hook + payoff 구조의 짧은 대본
- 기존 본편이 있더라도 "쇼츠는 완전히 다른 톤·구조로 새로 짜고 싶다"는 경우

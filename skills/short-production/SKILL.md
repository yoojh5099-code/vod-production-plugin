---
name: short-production
description: |
  9:16 세로 YouTube Shorts(40~60초)를 자동 제작하는 오케스트레이터 스킬. video-production의
  vp-scene-architect / vp-voice-engineer / vp-video-composer 팀을 그대로 재사용하되, 9:16 1080×1920
  포맷·쇼츠 전용 컴포넌트·짧은 페이싱으로 분기 실행한다.
  "쇼츠 만들어줘", "유튜브 쇼츠 제작", "Shorts production", "9:16 영상", "세로 영상 제작",
  "기존 영상에서 쇼츠 뽑아줘", "대본으로 쇼츠 만들어줘" 요청 시 이 스킬을 사용한다.
  16:9 본편이 필요하면 video-production 스킬을 사용할 것.
---

# YouTube Shorts 제작 오케스트레이터

video-production의 4팀 파이프라인을 9:16 쇼츠로 분기시킨 스킬. 두 가지 입력 모드를 지원한다.

## 두 가지 모드

| 모드 | 입력 | 사용 시점 |
|------|------|----------|
| **Mode A — 추출** | 기존 video-production 프로젝트 (Remotion 디렉터리 + scene_plan.json + tts/) | 본편이 이미 있고 핵심 씬 N개를 쇼츠로 뽑을 때 |
| **Mode B — 단독** | 쇼츠 전용 짧은 대본 (40~60초 분량) | 처음부터 쇼츠만 제작할 때 |

상세는 `references/mode_a_reuse.md`, `references/mode_b_standalone.md`.

## 시그니처 요소 (강제 기본값)

쇼츠 모든 산출물은 아래 3개를 무조건 포함한다. 사용자가 명시적으로 끄지 않는 한 변경 금지.

1. **카라오케 자막** — 44px CookieRun, 글자별 흰→노랑(`#fbbf24`) 글로우, lead=0.04
2. **BGM 없음** — 자동재생 무음 시청 대응 + 점수 하락 회피
3. **상단 프로그레스 바** — 6px 높이, 막대형, 좌→우 진행. 시청 이탈 방지

`assets/Short.template.tsx`에 위 3개가 베이스로 박혀 있다. 컴포저는 이 템플릿을 변형하지 말고 콘텐츠만 채워 넣는다.

## 포맷

- **Composition**: 1080×1920 @ 30fps
- **총 길이**: 40~60초 (target). 60초 초과 시 vp-scene-architect가 강제 압축
- **막 구성**: 권장 3막(WHAT/HOW/WHO) — 도구 소개 장르 기준. 다른 장르(스토리·튜토리얼)면 자유 변형 가능
- **레이아웃**: 세로 스택 전용. 좌우 split 금지 (가독성 저하)
- **iPad 템플릿**: 사용 금지 (16:9 전용 프레임)
- **배경**: 다크 그라디언트 `linear-gradient(180deg, #0b1120 0%, #1e293b 50%, #0b1120 100%)` + 상단 라디얼 액센트

## 9:16 호환 패턴 화이트리스트

기존 `~/.claude/skills/remotion-assembly/references/component-patterns.md` 카탈로그에서 **세로 비율에 맞는 패턴만** 사용한다. 상세는 `references/patterns.md`.

**허용**: BigTitle, GlassCard, BulletList, BarChart(세로형), CodeBlock, ParticleConfetti, BrandLogo, KaraokeText, ProgressBar, SectionLabel, LevelBar

**금지**: QuadrantMatrix(2×2), LethalTriangle, HorseHarness, ReactLoop, TimelineCards(가로), iPadTemplate

vp-scene-architect는 이 화이트리스트만 본다. 카탈로그에 있어도 금지 목록은 자동 제외.

## 출력 파일명 컨벤션

| 산출물 | 경로 |
|--------|------|
| 쇼츠 영상 | `<project>/output/short.mp4` |
| 쇼츠 썸네일 (첫 프레임) | `<project>/output/short_thumbnail.png` |

`<project>/output/output.mp4`(본편)과 공존 가능. 같은 프로젝트에서 본편+쇼츠 모두 산출.

## 워크플로우

### Phase 0: 모드 판별

```
1. 사용자 입력 확인:
   - "기존 영상", "본편에서 추출", Remotion 디렉터리 경로 → Mode A
   - "쇼츠 대본", "처음부터", script/short_*.md → Mode B
   - 모호하면 사용자에게 질문
2. 프로젝트 경로 확정. 폴더 구조 검증:
   <project>/
   ├── script/        ← Mode B 필수, Mode A는 선택
   ├── output/
   ├── _workspace/
   │   └── shorts/    ← 쇼츠 전용 작업 공간 (본편과 격리)
   └── <project>-video/   ← Remotion 프로젝트 (Mode A는 기존, Mode B는 신규)
3. _workspace/shorts/ 디렉터리 없으면 생성
```

### Mode A: 기존 레퍼토리 추출

상세 워크플로우는 `references/mode_a_reuse.md` 참조. 핵심 흐름:

1. 사용자에게 사용할 씬 ID 목록 확인 (예: "씬 2, 4, 7로 쇼츠")
2. 본편 `_workspace/scene_plan.json`에서 해당 씬만 추출 → `_workspace/shorts/scene_plan_short.json`
3. `_workspace/tts/seg_NN.wav` 그대로 재활용 (TTS 재생성 안 함)
4. **vp-video-composer만 호출** — 9:16 컴포지션 + 카라오케 자막 + 프로그레스 바 추가
5. Phase 4 (Studio 프리뷰 → 렌더)

### Mode B: 단독 쇼츠 제작

상세 워크플로우는 `references/mode_b_standalone.md` 참조. 핵심 흐름:

1. `assets/scaffold_short.sh <project>` 실행 — Remotion 프로젝트 신규 셋업
2. **vp-scene-architect** 호출 — 쇼츠 화이트리스트 + `aspect: shorts` + `target_duration: 40-60` 컨텍스트 전달
3. **vp-voice-engineer** 호출 — TTS 생성 (Gate A/B는 그대로 유지)
4. Audio Sync (Phase 2.1) — 본편과 동일
5. **vp-video-composer** 호출 — 9:16 1080×1920 + `assets/Short.template.tsx` 사용
6. Gate C (Whisper) — 본편과 동일
7. Phase 4 (Studio 프리뷰 → 렌더)

## 서브에이전트 호출 시 9:16 컨텍스트 (공통)

쇼츠 분기를 위해 모든 서브에이전트 prompt에 다음 컨텍스트를 추가한다:

```
⚠️ Shorts 모드:
- aspect: 9:16 (1080×1920)
- target_duration: 40~60s
- BGM 금지, 카라오케 자막 강제, 상단 프로그레스 바 강제
- 9:16 호환 패턴 화이트리스트만 사용 (상세: ~/.claude/skills/short-production/references/patterns.md)
- iPad 템플릿 금지
- 작업 공간: <project>/_workspace/shorts/ (본편 _workspace와 격리)
- 컴포넌트 베이스: ~/.claude/skills/short-production/assets/Short.template.tsx
- 출력: output/short.mp4 + output/short_thumbnail.png
```

## Phase 4: 프리뷰 + 렌더 (오케스트레이터 직접)

video-production과 동일 규칙. 서브에이전트는 Studio도 안 띄우고 render도 안 한다.

```bash
cd <project>/<project>-video
npx remotion studio --port 3123 --gl=angle  # 백그라운드
# 사용자 승인 대기
npx remotion render Short output/short.mp4
npx remotion still Short output/short_thumbnail.png --frame=0
```

Composition id는 **`Short`** 로 고정. 여러 쇼츠를 만들 땐 `ShortCaveman`, `ShortGraphify` 등 suffix 부여하고 Phase 4 명령에서 id 교체.

## 데이터 흐름

```
Mode A:
  본편 <project>/_workspace/scene_plan.json
       + tts/seg_NN.wav
       ↓ (사용자가 씬 ID 지정)
  _workspace/shorts/scene_plan_short.json (선택된 씬만)
       ↓
  [vp-video-composer] 9:16 + 카라오케 자막 + 프로그레스 바
       ↓
  output/short.mp4 + output/short_thumbnail.png

Mode B:
  script/short_*.md
       ↓
  scaffold_short.sh → <project>-video/ (신규)
       ↓
  [vp-scene-architect] 화이트리스트 + 40~60s 컨텍스트
       ↓
  _workspace/shorts/scene_plan.json
       ↓
  [vp-voice-engineer] TTS + Gate A/B
       ↓
  _workspace/shorts/tts/ + timing.json
       ↓
  [오케스트레이터] Audio Sync
       ↓
  [vp-video-composer] 9:16 + Short.template.tsx
       ↓
  [오케스트레이터] Gate C (Whisper)
       ↓
  [오케스트레이터] Studio → 사용자 승인 → 렌더
       ↓
  output/short.mp4 + output/short_thumbnail.png
```

## 에러 핸들링

| Phase | 에러 | 대응 |
|-------|------|------|
| 0 | 모드 판별 불가 | 사용자에게 입력 시나리오 질문 |
| Mode A | 지정 씬 ID가 scene_plan.json에 없음 | 사용 가능한 씬 ID 리스트 보고 |
| Mode A | 합산 길이가 60s 초과 | 사용자에게 씬 제외 또는 cut-down 선택 요청 |
| Mode B | 대본이 60s 초과 추정 | vp-scene-architect가 압축 시도 → 실패 시 사용자 협의 |
| 1~3 | 본편과 동일 | video-production SKILL.md 참조 |

## 테스트 시나리오

### Mode A 정상 흐름
- 입력: `vod/claude-opensource/` (본편 38씬 완성됨), "씬 2/4/7로 쇼츠"
- 기대: `output/short.mp4`(약 44s) + `short_thumbnail.png`. ShortCaveman.tsx와 유사 구조.

### Mode B 정상 흐름
- 입력: `vod/test-short/script/short.md` (40~60s 분량 대본)
- 기대: scaffold → 씬 분석 → TTS → 조립 → Studio → 렌더. 총 5~10분.

# vod-production-plugin

YouTube 콘텐츠 기획부터 영상 제작까지 에이전트 팀 기반 엔드투엔드 파이프라인.

## 구성

**오케스트레이터 스킬 2개**

| 스킬 | 역할 |
|---|---|
| `content-production` | 트렌드 리서치 → 스크립트 작성 → SEO + 썸네일 기획을 팀으로 조율 |
| `video-production` | 씬 분석 → TTS → Remotion 조립 → 렌더링을 팀으로 조율 |

**서브 스킬 9개**

| 스킬 | 용도 |
|---|---|
| `trend-research` | cp-trend-researcher용 |
| `script-writing` | cp-script-writer용 |
| `seo-optimization` | cp-seo-optimizer용 |
| `thumbnail-planning` | cp-thumbnail-planner용 |
| `scene-analysis` | cp-scene-architect / vp-scene-architect용 — 씬 구조화 (scene_plan.json) |
| `voice-production` | vp-voice-engineer용 — Qwen3-TTS (short-production 등 외부 워크플로 전용, 본편은 사용자 직접 녹음) |
| `remotion-assembly` | vp-video-composer / vp-motion-designer용 — Remotion 조립 |
| `content-qa` | content-production / video-production 산출물 9종 sync 검증 + 자동 복구 |
| `short-production` | 9:16 세로 YouTube Shorts(40~60초) 자동 제작 오케스트레이터 |

**에이전트 10개**: cp-* 6개(기획팀, scene-architect 포함) + vp-* 4개(제작팀)

## 설치

Claude Code 세션에서:

```
/plugin marketplace add yoojh5099-code/vod-production-plugin
/plugin install vod-production-plugin@vod-production
```

> 마켓플레이스 이름은 `vod-production` (repo 루트의 `.claude-plugin/marketplace.json`에 정의), 플러그인 이름은 `vod-production-plugin` 입니다.

로컬 개발용으로 테스트하려면:

```
claude --plugin-dir /path/to/vod-production-plugin
```

## 사용

설치 후 슬래시 명령으로 호출 (네임스페이스 `vod-production-plugin` 프리픽스가 붙을 수 있음):

```
/content-production     # 기획 (트렌드→스크립트→SEO→썸네일→씬 분할→녹음 가이드)
/video-production       # 제작 (사용자 직접 녹음 wav → 정규화→timing→Remotion→렌더)
/short-production       # 9:16 쇼츠 제작 (40~60초)
/content-qa             # 산출물 9종 sync 검증 + 자동 복구
```

기본 흐름: `content-production` 산출물(스크립트 + scene_plan + 녹음 가이드) → 사용자가 Audacity로 녹음 → `video-production`이 wav를 받아 영상 조립.

스크립트를 수정했거나 sync가 의심되면 `content-qa`로 9종 산출물(script/scene_plan/timing/audio 등) 정합성을 검증·복구.

## 주의 — 내부 경로 참조

각 스킬 문서에 `~/.claude/skills/<skill>/...` 형태의 절대 경로 참조가 포함돼 있음. 이는 플러그인 이전 구조의 유산이며, 플러그인만 설치해서 쓸 경우 Claude가 문맥으로 올바른 파일을 찾도록 의도됨. 원본(`~/.claude/skills/`)을 제거하려면 각 스킬 내부 참조를 플러그인 상대 경로로 정리하는 후속 작업이 필요.

## 워크플로 변경 (2026-05-26)

본편 `video-production`은 사용자가 Audacity로 직접 녹음한 wav를 정규화하는 방식으로 전환됐으며, TTS 기반 `voice-production`은 더 이상 본편 파이프라인에 사용되지 않음 (deprecated). `voice-production`은 이제 빠른 드래프트 또는 `short-production` 같은 외부 워크플로에서만 사용.

쇼츠는 길이가 짧아 TTS 자동 생성을 그대로 유지 — `short-production`은 9:16 1080×1920 포맷으로 분기 실행.

## content-qa — 산출물 sync 검증

`content-production` / `video-production` 파이프라인은 9종 산출물을 만들어내는데(script, scene_plan, timing, audio 등), 어느 한 단계에서 수정이 일어나면 후속 산출물과 어긋날 수 있음. `content-qa`가 정합성을 검증하고 깨진 sync는 자동 복구.

호출 시점: 스크립트 수정 직후, 사용자 녹음 후, video-production 진입 전, Studio 프리뷰가 어색할 때.

## 라이선스

MIT

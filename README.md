# vod-production-plugin

YouTube 콘텐츠 기획부터 영상 제작까지 에이전트 팀 기반 엔드투엔드 파이프라인.

## 구성

**오케스트레이터 스킬 2개**

| 스킬 | 역할 |
|---|---|
| `content-production` | 트렌드 리서치 → 스크립트 작성 → SEO + 썸네일 기획을 팀으로 조율 |
| `video-production` | 씬 분석 → TTS → Remotion 조립 → 렌더링을 팀으로 조율 |

**서브 스킬 7개**

| 스킬 | 용도 |
|---|---|
| `trend-research` | cp-trend-researcher용 |
| `script-writing` | cp-script-writer용 |
| `seo-optimization` | cp-seo-optimizer용 |
| `thumbnail-planning` | cp-thumbnail-planner용 |
| `scene-analysis` | vp-scene-architect용 — 씬 구조화 (scene_plan.json) |
| `voice-production` | vp-voice-engineer용 — Qwen3-TTS + Gate A/B/C 검증 |
| `remotion-assembly` | vp-video-composer / vp-motion-designer용 — Remotion 조립 |

**에이전트 9개**: cp-* 5개(기획팀) + vp-* 4개(제작팀)

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
/content-production     # 기획 (트렌드→스크립트→SEO→썸네일)
/video-production       # 제작 (씬→TTS→Remotion→렌더)
```

두 파이프라인을 연속 실행할 때는 기획 산출물(`script/script.json`)이 제작의 입력이 됨.

## 주의 — 내부 경로 참조

각 스킬 문서에 `~/.claude/skills/<skill>/...` 형태의 절대 경로 참조가 포함돼 있음. 이는 플러그인 이전 구조의 유산이며, 플러그인만 설치해서 쓸 경우 Claude가 문맥으로 올바른 파일을 찾도록 의도됨. 원본(`~/.claude/skills/`)을 제거하려면 각 스킬 내부 참조를 플러그인 상대 경로로 정리하는 후속 작업이 필요.

## 핵심 품질 가드 (voice-production)

TTS 자동 생성의 신뢰성 확보를 위한 3중 게이트:

- **Gate A** `MIN_KEEP_RATIO=0.5` — trim 결과가 raw의 50% 미만이면 거부
- **Gate B** `char/sec ∈ [3, 25]` — 씬별 발화 속도 이탈 시 최대 2회 자동 재생성
- **Gate C** Whisper 전사로 `narration_tts` 마지막 15자 포함 여부 검증 (렌더 직전)

video-production 오케스트레이터는 추가로:

- **Phase 2.1 Audio Sync** — `_workspace/tts/*.wav` → `<project>-video/public/audio/` 멱등 동기화

## 라이선스

MIT

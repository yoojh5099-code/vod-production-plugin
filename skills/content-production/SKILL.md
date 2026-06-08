---
name: content-production
description: |
  YouTube 콘텐츠 기획 팀 오케스트레이터. 트렌드 리서치 → 스크립트 작성 → SEO 최적화 + 썸네일 기획 → 씬 분할 → 녹음 가이드 산출까지 팀으로 조율하여 사용자가 Audacity로 녹음만 시작하면 되는 상태를 만들어준다.
  '유튜브 콘텐츠 기획', 'YouTube content plan', '영상 기획', '유튜브 팀 실행', '콘텐츠 기획 시작', '영상 주제부터 썸네일까지', '유튜브 기획 전체 프로세스' 등의 요청 시 반드시 이 스킬을 사용할 것.
  단순 스크립트 작성만 요청하는 경우에는 script-writing 스킬을 대신 사용.
---

# YouTube Content Harness — Orchestrator

YouTube 콘텐츠 기획 팀을 조율하는 오케스트레이터. 6명의 전문 에이전트를 감독자 패턴으로 운영하여, 사용자가 직접 녹음을 시작할 수 있는 상태(`recording_guide.md`)까지 만들어준다.

## 팀 구성

| 에이전트 | 역할 | 스킬 |
|---------|------|------|
| cp-supervisor | 팀 감독, 통합 검토 | (직접 조율) |
| cp-trend-researcher | 트렌드 리서치 | trend-research |
| cp-script-writer | 스크립트 작성 | script-writing |
| cp-seo-optimizer | SEO 최적화 | seo-optimization |
| cp-thumbnail-planner | 썸네일 컨셉 | thumbnail-planning |
| cp-scene-architect | 씬 분할, Visual 매핑 | scene-analysis |

## 실행 모드

**에이전트 팀** (감독자 패턴, 사람 직접 녹음 워크플로 기본)

## 워크플로우 개요

```
[사용자 요청]
    ↓
Phase 1: 준비 (00_brief.md)
    ↓
Phase 2: 트렌드 리서치 (cp-trend-researcher)
    ↓ 주제 선정
Phase 3: 스크립트 작성 (cp-script-writer)
    ↓
Phase 4: SEO + 썸네일 (병렬)
    ↓
Phase 5: 통합 검토 (cp-supervisor)
    ↓
Phase 6: 씬 분할 (cp-scene-architect)        ← 신규
    ↓
Phase 7: 녹음 가이드 산출                      ← 신규
    ↓
[사용자 Audacity 녹음 → _workspace/audio/seg-NN.wav]
    ↓
[/video-production 으로 핸드오프]
```

## Phase 1: 준비

1. 사용자 요청에서 다음을 파악한다:
   - 채널 정보 (니치, 구독자 규모, 스타일)
   - 타겟 오디언스
   - 특정 주제 요청 여부
   - 선호/제외 조건
2. 프로젝트 폴더 구조 확인/생성:
   ```
   <project>/
   ├── script/
   ├── thumbnail/
   ├── _workspace/
   └── _workspace/audio/   ← 사용자 녹음 wav 저장 위치 (Phase 7 이후)
   ```
3. 입력 정보를 `_workspace/00_brief.md`에 정리한다

## Phase 2: 트렌드 리서치

1. `cp-trend-researcher` 에이전트를 실행한다
   - 에이전트 정의: `~/.claude/agents/cp-trend-researcher.md`
   - 스킬: `trend-research`
   - 입력: `_workspace/00_brief.md`
   - 출력: `_workspace/01_researcher_trend_report.md`
2. 트렌드 보고서를 검토하고 주제를 선정한다
   - 사용자가 특정 주제를 지정한 경우 이 Phase는 생략하고 해당 주제로 진행

## Phase 3: 스크립트 작성

1. `cp-script-writer` 에이전트를 실행한다
   - 에이전트 정의: `~/.claude/agents/cp-script-writer.md`
   - 스킬: `script-writing`
   - 입력: 선정 주제 + 트렌드 데이터 + 채널 톤
   - 출력: `script/02_writer_script.md`
2. 스크립트를 검토한다
   - 후킹이 충분히 강력한가
   - 분량이 타겟 길이에 맞는가
   - 채널 톤과 일치하는가
   - **CTA 규칙 준수 확인 (아래 참조)**
   - **출처/크레딧 노출 규칙 준수 확인 (아래 참조)**

### 출처/크레딧 처리 규칙

참고자료의 원문 작성자·출처는 **영상 낭독(본문·후킹·CTA) 어디에도 기본적으로 언급하지 않는다.** 사용자가 참고자료를 제공했더라도 마찬가지다.

- **금지:** "○○님 블로그에 따르면", "이 영상은 ○○ 기사 기반으로…", "원문 크레딧: …" 같은 낭독 문장
- **허용 (영상 외부):** 영상 설명란(Description)에 "참고자료" 섹션으로 링크·작성자 표기 — SEO 에이전트가 설명문에 포함하도록 한다
- **예외 (영상 내 언급 허용):**
  - 사용자가 "출처를 영상 안에서 밝혀달라"고 명시한 경우
  - 연구·논문·공식 통계의 신뢰성을 영상 내에서 담보해야 하는 경우
  - 인터뷰/협업 콘텐츠처럼 크레딧 자체가 콘텐츠 본질인 경우
- **이유:** 크레딧 문장은 시청자 몰입을 끊고, 정보성 콘텐츠를 "남의 글 소개"로 톤다운시킨다. 출처 투명성은 영상 설명란에서 충분히 확보된다.

Supervisor는 Phase 5 교차 검토에서 스크립트에 크레딧 문장이 남아있지 않은지, 출처 링크가 설명문(03_seo_optimization.md)에 포함됐는지 둘 다 확인한다.

### CTA 작성 규칙 (엄격)

스크립트 마지막 CTA는 다음 규칙을 따른다. 사용자가 명시적으로 다른 지시를 한 경우에만 예외를 허용한다.

- **금지:** "구독·좋아요·알림설정" 같은 상투적 요청 문구 일괄 제외 — 채널 톤을 하입처럼 만들고 시청자 피로를 유발
- **허용:** 짧은 마무리 한 문장 + "추가로 궁금한 점/자신의 경험은 댓글에 남겨달라" 정도의 가벼운 유도
- **선택적 허용:** 다음 영상 예고(시리즈인 경우), 영상 요약 한 줄
- **톤:** 담백하고 간결하게. 과장·느낌표 연발 금지

예시(권장):
> "오늘 내용 한 줄로 요약하면 [X]입니다. 여러분은 어떻게 쓰고 계신지, 궁금한 점이나 본인 경험이 있으면 댓글에 남겨주세요. 그럼 다음 영상에서 뵐게요."

예시(지양):
> ~~"구독과 좋아요, 알림설정까지 꼭 눌러주시고 다음 영상도 기대해주세요!"~~

## Phase 4: SEO + 썸네일 (병렬)

스크립트 완료 후 두 에이전트를 **병렬로** 실행한다 (단일 메시지에 두 Agent 호출):

**4-A. SEO 최적화** (`cp-seo-optimizer`)
- 에이전트 정의: `~/.claude/agents/cp-seo-optimizer.md`
- 스킬: `seo-optimization`
- 입력: 스크립트 + 주제 + 채널 정보
- 출력: `_workspace/03_seo_optimization.md`

**4-B. 썸네일 기획** (`cp-thumbnail-planner`)
- 에이전트 정의: `~/.claude/agents/cp-thumbnail-planner.md`
- 스킬: `thumbnail-planning`
- 입력: 스크립트 + 채널 정보
- 출력: `_workspace/04_thumbnail_concepts.md`

SEO Optimizer는 제목 후보를 파일에 먼저 저장하고, Thumbnail Planner는 해당 파일을 참조하여 제목-썸네일 일관성을 확보한다.

## Phase 5: 통합 검토 (cp-supervisor)

Supervisor가 모든 산출물을 교차 검토한다:

1. **일관성 검증**
   - 스크립트 톤 ↔ 제목 톤 일치 여부
   - SEO 키워드 ↔ 스크립트 내 키워드 반영 여부
   - 썸네일 컨셉 ↔ 제목/스크립트 메시지 일관성
   - 스크립트에 원문 크레딧 문장이 남아있지 않은지 (예외 조건 해당 시 제외)
   - 출처·원문 링크가 설명문(`03_seo_optimization.md`)에 "참고자료" 섹션으로 포함됐는지
2. **품질 검증**
   - 각 산출물이 기대 수준을 충족하는지
   - 불일치나 누락이 없는지
3. **통합 기획서 작성**
   - `_workspace/final_content_plan.md`에 최종 산출물 통합

## Phase 6: 씬 분할 (cp-scene-architect)

스크립트가 확정되면 `cp-scene-architect`를 실행한다. 이 단계는 video-production이 아니라 콘텐츠 팀이 담당한다 — 사용자 직접 녹음 워크플로에서 녹음 가이드를 산출하려면 씬 정보가 먼저 필요하기 때문이다.

```
Agent(
  description: "씬 분석",
  prompt: "~/.claude/agents/cp-scene-architect.md를 읽고 역할을 수행하라.
    ~/.claude/skills/scene-analysis/SKILL.md의 워크플로우를 따른다.
    Visual 선택은 반드시 ~/.claude/skills/remotion-assembly/references/pattern-catalog.md의
    카테고리 매핑과 다이버시티 예산 규칙을 따른다 (component-patterns.md는 읽지 말 것).

    입력: <project>/script/02_writer_script.md
    참고: <project>/_workspace/03_seo_optimization.md (키워드 일관성)
          <project>/thumbnail/ (썸네일 방향)

    중요: 사용자 직접 녹음 워크플로이므로 narration_tts 필드는 생성하지 말 것.
    영문 브랜드 발음 가이드는 Phase 7 recording_guide.md에서 별도 처리.

    산출물 2개:
      1. <project>/_workspace/scene_plan.json (visual + visual_category + visual_tier 포함)
      2. <project>/_workspace/visual_allocation_audit.md (예산 검증 리포트)",
  model: "opus"
)
```

**검증**:
- `_workspace/scene_plan.json` 존재 + 유효한 JSON
- `_workspace/visual_allocation_audit.md` 존재 + 예산 위반 없음 확인
- 각 씬에 `visual_category`, `visual_tier`, `estimated_duration_sec` 필드 존재
- 모든 씬에 `narration` 존재 (`narration_tts`는 없어야 함)

### 다이버시티 예산 (요약)

| tier | 개수 | 예산/영상 |
|------|------|----------|
| signature | 7 | 1회씩 |
| special | 3 | 2회 이하 |
| generic | 14 | 3회 이하 |

추가 규칙: 인접 씬 동일 visual 금지 · 3씬 이내 동일 visual 최대 2회 · 의도 카테고리 7 중 최소 5종 사용.

## Phase 7: 녹음 가이드 산출

scene_plan.json을 입력으로 `recording_guide.md`를 자동 생성한다. 사용자가 Audacity를 켜고 바로 녹음을 시작할 수 있는 모든 정보를 담는다.

```bash
python3 ~/.claude/skills/content-production/scripts/generate_recording_guide.py <project>
```

**산출물**: `<project>/_workspace/recording_guide.md`

포함 내용:
- wav 파일 사양 (24kHz/mono/16-bit 권장, 그러나 어떤 입력도 video-production이 자동 정규화)
- Audacity 셋업 가이드
- 톤 가이드 (담백, 1인칭, 분당 350~400자)
- **이 영상에 등장하는 영문 브랜드만 추려낸 발음 표** (전체 카탈로그 아님)
- 씬별 대본 (id → 파일명 → 추정 길이 → 자막 → narration 본문)
- 녹음 후 검증 체크리스트
- 다음 단계 안내 (`/video-production` 호출)

**검증**:
- `_workspace/recording_guide.md` 존재
- 씬 수 일치 (scene_plan.json의 scenes 배열 길이와 동일)

## 최종 산출물

콘텐츠 팀의 책임은 다음 9개 파일로 마무리된다:

```
<project>/
├── script/02_writer_script.md            ← Phase 3
├── _workspace/
│   ├── 00_brief.md                       ← Phase 1
│   ├── 01_researcher_trend_report.md     ← Phase 2 (선택)
│   ├── 03_seo_optimization.md            ← Phase 4-A
│   ├── 04_thumbnail_concepts.md          ← Phase 4-B
│   ├── final_content_plan.md             ← Phase 5
│   ├── scene_plan.json                   ← Phase 6
│   ├── visual_allocation_audit.md        ← Phase 6
│   └── recording_guide.md                ← Phase 7
```

## 사용자에게 핸드오프

Phase 7 완료 후 사용자에게 다음 메시지를 전달한다:

```
✅ 콘텐츠 기획 완료

📋 산출물:
- 통합 기획서: _workspace/final_content_plan.md
- 스크립트: script/02_writer_script.md
- 씬 분할: _workspace/scene_plan.json (N씬, 추정 M분 S초)
- 녹음 가이드: _workspace/recording_guide.md

🎙️ 다음 단계: Audacity로 녹음
1. recording_guide.md를 열어 §5 씬별 대본을 보면서 녹음
2. _workspace/audio/seg-01.wav ~ seg-NN.wav 로 저장
3. 녹음이 끝나면 다음 메시지로 진행:
   > "녹음 끝났어. /video-production 돌려줘"

video-production이 자동으로 wav 정규화 → timing 측정 → Remotion 조립 →
Studio 프리뷰 → 사용자 승인 → 최종 렌더까지 처리합니다.
```

## 데이터 흐름

```
[사용자 요청]
    ↓
[00_brief.md] ← 입력 정리
    ↓
[cp-trend-researcher] → [01_researcher_trend_report.md]
    ↓ (주제 선정)
[cp-script-writer] → [script/02_writer_script.md]
    ↓ (병렬)
[cp-seo-optimizer] → [03_seo_optimization.md]
[cp-thumbnail-planner] → [04_thumbnail_concepts.md]
    ↓
[Supervisor 통합 검토] → [final_content_plan.md]
    ↓
[cp-scene-architect] → [scene_plan.json + visual_allocation_audit.md]
    ↓
[generate_recording_guide.py] → [recording_guide.md]
    ↓
[사용자 Audacity 녹음] → [_workspace/audio/seg-NN.wav]
    ↓
[/video-production]
```

## 에이전트 실행 방법

각 에이전트는 `Agent` 도구로 실행한다. 반드시 `model: "opus"`를 지정한다.

```
Agent(
  description: "[에이전트 역할 요약]",
  prompt: "[에이전트 정의 파일 경로]를 읽고 역할을 수행하라. [스킬 파일 경로]의 워크플로우를 따른다. 입력: [파일 경로]. 출력: [파일 경로]에 저장.",
  model: "opus"
)
```

병렬 실행이 가능한 Phase 4에서는 두 Agent 호출을 동일 메시지에서 병렬로 실행한다.

## 산출물 수정 시 sync 보장

사용자가 `script/02_writer_script.md` 또는 `_workspace/scene_plan.json` 등을 직접 수정하면 9개 산출물이 어긋날 수 있다. 다음 시점마다 `/content-qa` (content-qa 스킬) 호출 권장:

- 스크립트 다듬은 직후 (Layer 1, 4)
- 수동으로 scene_plan.json 편집 후 (Layer 1, 3, 5)
- 새 영상 제작 진입 전 (전체 9 layer)

호출:
```bash
python3 ~/.claude/skills/content-qa/scripts/check_sync.py <project>          # dry-run
python3 ~/.claude/skills/content-qa/scripts/check_sync.py <project> --apply  # 자동 복구
```

상세는 `~/.claude/skills/content-qa/SKILL.md` 참조.

## 에러 핸들링

| 상황 | 대응 |
|------|------|
| 트렌드 리서치 실패 | 사용자 주제로 직접 진행. 보고서에 "트렌드 데이터 없음" 명시 |
| 스크립트 품질 미달 | 구체적 피드백 후 1회 재작업 요청 |
| SEO/썸네일 불일치 | Supervisor가 직접 조정하여 일관성 확보 |
| 에이전트 응답 없음 | 해당 파트를 Supervisor가 직접 수행 |
| Phase 6 예산 위반 | cp-scene-architect가 자동 리밸런싱 (같은 카테고리 내 generic 대체). 그래도 위반이면 audit.md에 경고 기록 후 진행 |
| Phase 7 scene_plan.json 누락 | Phase 6 미완료 — 사용자에게 보고 후 중단 |

## 테스트 시나리오

### 정상 흐름
- 입력: "IT/기술 채널, 구독자 5만, 20~30대 개발자 타겟, 10분 영상"
- 기대: 7개 Phase 순차 실행, 최종 산출물에 기획서/스크립트/SEO/썸네일/씬분할/녹음가이드 모두 포함

### 특정 주제 지정
- 입력: "Claude Code 신기능 소개 영상 기획해줘"
- 기대: Phase 2(트렌드 리서치) 생략, 지정 주제로 Phase 3부터 진행

### 에러 흐름 — 채널 정보 없음
- 입력: "영상 기획해줘"
- 기대: Supervisor가 합리적 추정으로 진행하되, 추정 사항을 기획서에 명시

### 자동 연결 모드
- 입력: "이 주제로 기획부터 영상까지 한번에 해줘"
- 기대: content-production 7개 Phase 완료 → 사용자 녹음 대기 → "녹음 끝났어" 응답 후 video-production 자동 실행

# Pattern Catalog — Visual 선택 가이드

**목적**: scene_plan.json의 각 씬에 `visual` 타입을 할당할 때 사용하는 얇은 선택 레이어.
**구현 참조는 `component-patterns.md`** (이 파일은 선택용. 구현 코드는 필요할 때만 Grep으로 lazy load).

---

## 다이버시티 예산 규칙 (MANDATORY)

영상 전체에서 다음 규칙을 **반드시** 지킨다. vp-scene-architect는 초안 생성 후 검증·리밸런싱한다.

| 규칙 | 한도 | 위반 시 |
|------|------|---------|
| 시그니처 패턴 1개당 최대 사용 횟수 | **1회** | 같은 의도 카테고리 내 다른 시그니처/제네릭으로 교체 |
| 제네릭 패턴 1개당 최대 사용 횟수 | **3회** | 같은 의도 카테고리 내 다른 제네릭으로 교체 |
| 스페셜 패턴 1개당 최대 사용 횟수 | **2회** | 같은 카테고리 내 대체 |
| 인접 씬(N, N+1) 동일 visual | **금지** | 둘 중 하나를 교체 |
| 3씬 이내 동일 visual 반복 | **최대 2회** | 간격 확장 |
| 의도 카테고리 커버리지 (7종 중) | **≥5종 사용** | 미사용 카테고리에서 후보 선택 |

**리밸런싱 원칙**: 교체할 때는 **같은 의도 카테고리** 내에서 선택. 카테고리를 넘어가면 내러티브가 흐트러진다.

---

## 의도 카테고리 (7종)

각 카테고리는 씬이 전달하려는 **의미 기능**으로 분류. 패턴은 카테고리 내 **알파벳 순**으로 나열 (선호 편향 방지).

### 1. Comparison — 비교/대조

두 대상의 차이를 병치. Before/After, A vs B, 경쟁사 비교.

| visual 타입 | 컴포넌트 | 사용 상황 | tier |
|------------|---------|----------|------|
| `code-split` | CodeEditorSplit | 코드 Before/After, 정책 변경, 경고 강조 | signature |
| `comparison-cards` | ComparisonCards | 제품/기능/플랜 2개 비교, VS 구도 | generic |

### 2. Timeline — 시간순/단계

시간 축 또는 순서가 있는 진행. 로드맵, 히스토리, 단계.

| visual 타입 | 컴포넌트 | 사용 상황 | tier |
|------------|---------|----------|------|
| `svg-path-draw` | SVGPathDraw | 곡선 따라 드로잉되는 단계 연결 | generic |
| `timeline-cards` | TimelineCards | 시간순 단계 카드 (vertical/horizontal) | generic |

### 3. Data-viz — 수치/지표 시각화

숫자가 주인공인 씬. 성장, 비율, 달성률.

| visual 타입 | 컴포넌트 | 사용 상황 | tier |
|------------|---------|----------|------|
| `animated-pie` | AnimatedPieChart | 구성 비율, 점유율, 분해 | special |
| `count-up` | CountUpNumber | 단일/다중 숫자 강조 (2~3개 나열) | generic |
| `progress-ring` | ProgressRing | 퍼센트 게이지, 성능 점수 | generic |
| `rocket-trajectory` | RocketTrajectory | 성장 곡선, KPI 궤적, 채택 속도 | signature |

### 4. Quotation — 인용/권위

외부 발언, 트윗, 선언문. 권위자 증거·명언.

| visual 타입 | 컴포넌트 | 사용 상황 | tier |
|------------|---------|----------|------|
| `definition-formula` | DefinitionFormula | "X = A + B" 공식 레이아웃. 타이틀 박스 → 정의 캡션(단어별 reveal) → 공식 라인(=, 요소, +, 요소) 3-stage 순차 reveal | generic |
| `glass-card` | GlassCard + BigTitle | 일반 선언 카드, 제목 강조 | generic |
| `tweet-card` | TweetCard | 트위터/X 인용, 소셜 증거 | signature |
| `word-by-word` | WordByWordText | 핵심 문장 단어별 reveal | generic |

### 5. Warning — 경고/위험

주의 환기, 금기, 리스크 시각화.

| visual 타입 | 컴포넌트 | 사용 상황 | tier |
|------------|---------|----------|------|
| `checklist` | GlassCard + ListItems (dangerMode) | 위험 항목 체크리스트 | generic |
| `lethal-triangle` | LethalTriangle | 3요소 위험 (Lethal Trifecta) | signature |
| `terminal-bg` | TerminalBlock | 에러 로그, 경고 코드 블록 | generic |

### 6. Process — 프로세스/구조

시스템 흐름, 루프, 관계 다이어그램.

| visual 타입 | 컴포넌트 | 사용 상황 | tier |
|------------|---------|----------|------|
| `horse-harness` | HorseHarnessDiagram | 모델+하네스 은유 다이어그램 | signature |
| `pipeline-flow` | PipelineFlow | 단계 파이프라인 (loopBack 지원) | generic |
| `quadrant-matrix` | QuadrantMatrix | 2×2 분면 (BCG, 위험/영향) | signature |
| `react-loop` | ReActLoopDiagram | 순환 루프 + 후손 파생 | signature |
| `staggered-cards` | StaggeredCards | 병렬 요소 그리드 (3~6개) | generic |

### 7. Emphasis — 강조/전환

축하, 인트로, 임팩트 전환, 모핑.

| visual 타입 | 컴포넌트 | 사용 상황 | tier |
|------------|---------|----------|------|
| `flip-cards` | FlipCardGrid | 키워드→상세 공개, 퀴즈 | generic |
| `logo-meet` | BigTitle + StepBadge | 인트로 타이틀, 섹션 시작 | generic |
| `morphing-shape` | MorphingShape | 도형 변환 (원→육각→별) | special |
| `particle-confetti` | ParticleConfetti | 축하, outro, 성공 | generic |

---

## Tier 분류 요약

| tier | 개수 | 예산 | 의도 |
|------|------|------|------|
| signature | 7 | 1회/영상 | 강한 시그니처 — 특정 씬의 유일한 비주얼 |
| special | 2 | 2회/영상 | 특수 시각화 — 데이터/구조 전용 |
| generic | 15 | 3회/영상 | 범용 — 같은 타입 내에서 variant/이징으로 변주 |

**총 24종 visual 타입.** (default-scene은 매핑 실패 시 fallback으로 별도)
**2026-05-03 변경**: `concentric-rings` 제거(실제 쓸 일이 적고 morphing/word-by-word/definition-formula로 충분) + `definition-formula` 추가 ("A = B + C" 공식 정의 패턴).

---

## 선택 알고리즘 (vp-scene-architect용)

```
INPUT: scenes[] (내레이션 + 컨텍스트), budget_state (초기값 = tier별 최대치)

for scene in scenes:
    1. 내레이션 분석 → 의도 카테고리 1개 결정 (7종 중)
    2. 카테고리 내 후보 패턴 나열 (signature → special → generic 순)
    3. 다음을 모두 만족하는 첫 패턴 선택:
       - 현재 사용 횟수 < tier 예산
       - 직전 씬(N-1)과 다름
       - 지난 2씬(N-2, N-1)에서 3회 미만 출현
    4. 모두 소진 시 → 같은 카테고리 내 generic 재사용 OR 인접 카테고리 대안
    5. 그래도 없으면 → default-scene

OUTPUT: scene_plan.json 초안

POST-CHECK (감사 단계):
    - 시그니처 사용 횟수 체크 (각 ≤1)
    - 스페셜 사용 횟수 체크 (각 ≤2)
    - 제네릭 사용 횟수 체크 (각 ≤3)
    - 카테고리 커버리지 체크 (≥5)
    - 인접 중복 스캔
    - 위반 발견 시 → 교체 후보 제시 및 적용
    - 최종 결과를 visual_allocation_audit.md로 출력
```

---

## Scene Plan 스키마 확장

각 씬에 **`visual_category`**, **`visual_tier`** 필드를 추가한다 (감사/추적용):

```json
{
  "id": 0,
  "visual": "tweet-card",
  "visual_category": "quotation",
  "visual_tier": "signature",
  "narration": "...",
  "subtitle": "..."
}
```

기존 vp-video-composer는 `visual` 필드만 사용하므로 새 필드는 무시된다 (하위호환).

---

## 감사 리포트 (visual_allocation_audit.md)

scene-architect는 scene_plan.json과 함께 `_workspace/visual_allocation_audit.md`를 작성한다:

```markdown
# Visual Allocation Audit

## Summary
- Total scenes: 26
- Unique visual types: 17 / 24
- Unique categories: 7 / 7 ✓
- Signature usage: 6 / 7 (horse-harness 미사용)
- Max single-pattern usage: 2 (glass-card)
- Adjacent duplicates: 0 ✓

## Distribution
| visual | category | tier | count | budget | status |
|--------|----------|------|-------|--------|--------|
| tweet-card | quotation | signature | 1 | 1 | ✓ |
| glass-card | quotation | generic | 2 | 3 | ✓ |
| ...

## Budget Violations
(none)

## Coverage Gaps
- horse-harness (signature, process) — 미사용
- morphing-shape (special, emphasis) — 미사용

## Rebalancing Log
- scene 14: staggered-cards (4회째) → flip-cards 교체 (process → emphasis 카테고리 이동)
```

---

## 참고 링크

- **구현 코드**: `component-patterns.md`의 해당 섹션 (Grep으로 lazy load)
- **Studio 프리뷰**: `http://localhost:3123` → `Patterns` 폴더 → 각 패턴 6초 미리보기
- **이징 변주**: 같은 visual이 2씬 연속될 경우 `component-patterns.md`의 "이징 변주 가이드" 참조

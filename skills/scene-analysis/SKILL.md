---
name: scene-analysis
description: |
  YouTube 영상 대본을 분석하여 정규화된 씬 구조(scene_plan.json)를 생성하는 스킬.
  vp-scene-architect 에이전트가 사용한다. 직접 트리거되지 않으며, video-production 오케스트레이터를 통해 실행된다.
---

# 씬 분석 스킬

대본 파일을 읽고 모든 하류 에이전트(이미지, 음성, 영상)가 사용할 정규화된 씬 구조를 생성한다.

## 워크플로우

### 1. 대본 파일 탐색

`<project>/script/` 폴더에서 대본 파일을 찾는다. 우선순위:
1. `script.json` — JSON 형식 (가장 구조화됨)
2. `*.md` — 마크다운 형식
3. `*.xlsx` — 엑셀 형식 (openpyxl로 파싱)

### 2. 대본 파싱

**JSON 형식:**
```json
[
  {"id": 0, "start": 0, "end": 5, "text": "내레이션", "visual_note": "비주얼 설명"}
]
```

**마크다운 형식:**
씬 구분은 `## Scene N` 또는 `### N.` 또는 번호 리스트로 판단한다.
각 씬에서 내레이션 텍스트와 비주얼 노트를 추출한다.

**엑셀 형식:**
| 시간 | 화면구성 | 자막 | 내레이션 |
첫 행은 헤더로 판단하고, 이후 행을 씬으로 변환한다.

### 3. 씬 카테고리 분류

씬의 위치와 내용으로 카테고리를 자동 부여한다:

| 위치/내용 | category |
|-----------|----------|
| 첫 1~2개 씬 | intro |
| "왜", "이유", "문제" 키워드 | why |
| "준비", "설치", "설정" 키워드 | prep |
| 대부분의 본론 씬 | step |
| "데모", "실행", "결과" 키워드 | demo |
| 마지막 1~2개 씬 | outro |

> 배경은 iPad 템플릿(background.png) 고정. AuroraBackground variant는 사용하지 않는다.

### 4. Visual 타입 부여 (의도 카테고리 기반 + 다이버시티 예산)

**권위 있는 선택 소스**: `~/.claude/skills/remotion-assembly/references/pattern-catalog.md` (24종 visual, 7 의도 카테고리, tier별 예산).
이 스킬은 **구현 코드 레퍼런스(`component-patterns.md`)를 읽지 않는다** — 선택에만 집중.

#### 4-1. 카테고리 분류

각 씬의 내레이션을 읽고 **7 의도 카테고리** 중 1개를 먼저 결정한다:

| 카테고리 | 키워드/시그널 | 예시 |
|---------|--------------|------|
| Comparison | "vs", "Before/After", "차이", "비교", "대신" | Copilot vs Cursor |
| Timeline | "단계", "순서", "로드맵", "역사", "진화" | 3세대 Software 진화 |
| Data-viz | 숫자/퍼센트/지표 (88%, 2천만, 1.7배) | 생산성 88% 향상 |
| Quotation | 인용문, "라고 말했다", 트윗/X, 권위자 이름 | Karpathy 인용 |
| Warning | "위험", "경고", "주의", "금지", "실패", "에러" | Lethal Trifecta |
| Process | "흐름", "파이프라인", "루프", "구조", "아키텍처" | ReAct Loop |
| Emphasis | 후킹, 인트로, outro, 강조 문장, 축하 | 오프닝 타이틀 |

#### 4-2. 카테고리 내 패턴 선택

pattern-catalog.md에서 해당 카테고리의 후보 패턴을 나열한 뒤, 다음 순서로 후보를 고른다:

1. signature tier 우선 (영상당 1회씩만)
2. special tier (영상당 2회까지)
3. generic tier (영상당 3회까지)

**예산/인접성 제약**을 모두 만족하는 첫 패턴을 선택한다:
- 현재 사용 횟수 < tier 예산
- 직전 씬(N-1)과 `visual` 다름
- 최근 3씬 내 동일 `visual` ≤ 2회

#### 4-3. 각 씬에 카테고리/tier 기록

scene_plan.json의 각 씬에 추가 필드를 기록한다 (하위호환 유지):
- `visual_category`: 7 카테고리 중 1개
- `visual_tier`: "signature" | "special" | "generic"

### 4-bis. 감사(Audit) 단계 — 초안 생성 후 필수

초안 scene_plan.json을 만든 후 **반드시 검증 및 리밸런싱**을 수행한다:

1. **예산 검증**
   - 시그니처 패턴 각 사용 횟수 ≤ 1
   - 스페셜 패턴 각 사용 횟수 ≤ 2
   - 제네릭 패턴 각 사용 횟수 ≤ 3
2. **인접 중복 스캔**: `scenes[N].visual === scenes[N+1].visual` 발견 시 둘 중 하나 교체
3. **카테고리 커버리지**: 사용된 카테고리 수 ≥ 5 (7 중). 부족하면 미사용 카테고리에서 대체 후보 추천
4. **리밸런싱**: 초과 사용 패턴을 **같은 카테고리 내 다른 후보**로 교체 (카테고리 이동 최소화)
5. **리포트 생성**: `_workspace/visual_allocation_audit.md`에 분포표/위반/갭/리밸런싱 이력 기록

감사 리포트 포맷은 `pattern-catalog.md`의 "감사 리포트" 섹션 참조.

### 5. 배경 템플릿

기본 배경 템플릿은 **iPad**로 고정한다: `"background_template": "ipad"`

### 6. 썸네일 방향

`<project>/thumbnail/` 폴더를 확인한다:
- 썸네일 컨셉 문서가 있으면 핵심 방향을 `meta.thumbnail_concept`에 요약
- 없으면 영상 제목과 주제 기반으로 기본 방향 제시

### 7. 출력

`<project>/_workspace/scene_plan.json`에 최종 결과를 저장한다. 스키마는 에이전트 정의(`vp-scene-architect.md`)에 명시된 형식을 따른다.

## 검증 체크리스트

- [ ] 모든 씬에 id, category, visual, narration, subtitle이 있는가
- [ ] 모든 씬에 **visual_category, visual_tier**가 있는가
- [ ] scene_plan.json이 유효한 JSON인가
- [ ] meta.total_scenes와 실제 scenes 배열 길이가 일치하는가
- [ ] **시그니처 패턴이 각각 최대 1회만 사용되었는가**
- [ ] **스페셜 패턴이 각각 최대 2회 이하인가**
- [ ] **제네릭 패턴이 각각 최대 3회 이하인가**
- [ ] **인접 씬(N, N+1)에 동일 visual이 없는가**
- [ ] **의도 카테고리 커버리지가 7 중 5 이상인가**
- [ ] **`_workspace/visual_allocation_audit.md`가 생성되었는가**

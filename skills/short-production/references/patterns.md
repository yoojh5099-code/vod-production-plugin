# 9:16 Shorts 호환 패턴 화이트리스트

`~/.claude/skills/remotion-assembly/references/component-patterns.md`의 25종 카탈로그 중 **세로 비율(1080×1920)에서 가독성·임팩트가 유지되는 패턴만** 사용한다.

## 허용 패턴

| 패턴 | 카테고리 | 9:16 적용 노트 |
|------|----------|---------------|
| BigTitle | hero | 폰트 96~128px. 화면 중앙 또는 상단 1/3 |
| GlassCard | container | maxWidth 900, 세로 스택 내부 |
| BulletList | enumeration | 최대 3개. 각 항목 fontSize 36~48 |
| BarChart (vertical) | comparison | 가로형이 아닌 **세로 누적/병렬 막대** 권장. LevelBar처럼 가로 막대도 OK |
| LevelBar | comparison | ShortCaveman의 caveman/light/ultra 패턴. 세로 스택으로 3~4개까지 |
| CodeBlock / TerminalBox | code | maxWidth 900, 폰트 24~28px (가로폭 80자 미만) |
| ParticleConfetti | accent | 배경 효과로만 |
| BrandLogo | logo | 200~260px 크기. 단독 배치 |
| SectionLabel (chip) | label | 시그니처. 매 씬 상단에 색상 칩 |
| FormulaCard | reveal | "X → Y" 수식. ShortCaveman의 "Claude Code 응답 ↓ 원시인처럼 짧게" |
| AudienceBullet | bullet | 아이콘 + 텍스트 한 줄. 추천 대상 표현에 최적 |
| ResultCard | stat | 큰 숫자/문구 + 출처 메타. 마지막 막에 임팩트 |

## 금지 패턴

| 패턴 | 금지 사유 |
|------|----------|
| QuadrantMatrix (2×2) | 가로폭에 4분할 — 세로에서 셀 너무 작음 |
| LethalTriangle | 가로 정삼각형 배치 |
| HorseHarness | 가로 다이어그램 |
| ReactLoop | 가로 사이클 다이어그램 |
| TimelineCards (가로) | 좌→우 시간축 — 세로에선 부적합 (세로 타임라인은 OK) |
| iPadTemplate | 16:9 가로 프레임 — 9:16에 비율 어긋남 |
| FlipCardGrid (3+ 카드) | 가로폭에 3카드 병렬 — 세로 1080px엔 협소 |
| SpectrumAxis (가로축) | 가로 축이 본질 |
| ConcentricRings (큰 사이즈) | 1000px+ 원은 세로에서 잘림 — 600px 이하면 허용 |

## 예외 처리

화이트리스트에 없지만 사용하고 싶은 패턴이 있다면:

1. **세로 스택으로 재배치 가능한가?** — 좌우 split → 상하 split. 가능하면 OK
2. **세로 1920 안에 들어가는가?** — visual + 자막(bottom 400) + 프로그레스 바(top 40) 빼고 `1920 - 90(label) - 400(subtitle) - 80 = 약 1350px`가 콘텐츠 영역
3. 위 두 조건 충족이면 ad hoc 허용. 단 카탈로그 추가는 별도 PR.

## 다이버시티 예산 (쇼츠용)

본편 카탈로그 예산을 쇼츠 길이(40~60s, 3~5씬)에 맞게 축소:

| tier | 본편 예산 | 쇼츠 예산 |
|------|----------|----------|
| signature | 1회씩 | **1회 이하** (쇼츠 전체에서 최대 1개) |
| special | 2회 이하 | **1회 이하** |
| generic | 3회 이하 | **2회 이하** |

추가 규칙:
- 인접 씬 동일 visual 금지 (본편과 동일)
- 카테고리 7 중 최소 3종 사용 (본편은 5종, 쇼츠는 짧으니 완화)

## 시그니처 컴포넌트 (변경 금지)

`assets/Short.template.tsx`에 박혀 있는 다음 3개는 **컴포저가 절대 수정하지 않는다**:

1. **KaraokeText** — 글자별 흰→노랑 전환, 44px CookieRun, lead=0.04
2. **ProgressBar** — 상단 6px, 좌→우 진행
3. **SectionLabelOverlay** — 매 씬 상단 색상 칩

이들의 위치·색상·폰트·애니메이션 파라미터를 바꾸지 말 것. 사용자가 명시적으로 수정 요청한 경우만 예외.

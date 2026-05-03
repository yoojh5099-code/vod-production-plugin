# vp-video-composer — 비디오 컴포저

## 핵심 역할

Phase 1-2에서 생성된 에셋(씬 구조, 음성, 타이밍)을 조합하여 Remotion 프로젝트를 만든다.
scene_plan.json에서 직접 컴포넌트를 매핑하고 narration에서 props를 추출하여 Remotion 코드를 생성한다.
프리뷰 후 최종 영상을 렌더링한다.

## 작업 원칙

### 1단계: 프로젝트 셋업
1. Remotion 프로젝트 생성: `npx create-video@latest --template blank`
2. 의존성 설치: `@remotion/google-fonts`, `@remotion/media-utils`, `@remotion/transitions`
3. 폰트 복사: `~/.claude/skills/remotion-assembly/references/font/*.otf` → `public/fonts/`
4. 오디오 복사: `_workspace/tts/seg_*.wav` → `public/audio/`
5. BGM 복사: `music/*.mp3` → `public/audio/bgm.mp3`
6. 이미지 복사 (프로젝트 커스텀 우선): `image/*.{png,svg}` → `public/images/` (있는 경우)
7. 필수 에셋 복사 (반드시 references/ 폴더에서만 복사. 프로젝트의 background/ 폴더 사용 금지):
   - `cp ~/.claude/skills/remotion-assembly/references/background.png public/images/background.png`
   - `cp ~/.claude/skills/remotion-assembly/references/mascot.png public/images/mascot.png`
8. **브랜드 로고 매칭 (필수)** — `~/.claude/skills/remotion-assembly/references/brand-logos/manifest.yml`을 로드하고 scene_plan.json의 각 씬 narration+subtitle+visual_note를 스캔. `logos[*].aliases`와 매칭되는 브랜드의 SVG를 `public/images/`로 복사하고, 씬에 `matched_logos` 목록을 첨부한다. 절차·포맷은 remotion-assembly SKILL.md의 "브랜드 로고 자동 매칭" 섹션 참조. 결과를 `<project>/_workspace/logo_matches.md`에 기록
9. `remotion.config.ts` 설정 (angle GL 렌더러)

### 2단계: 코드 생성
1. `src/data/scenes.ts` — `_workspace/timing.json` + `_workspace/scene_plan.json` 기반. `SceneData`에 **`audioDurationSec` 필드(wav 실측값, 패딩 제외) 필수** — MainVideo의 씬별 오디오 fade in/out 계산 기준. timing.json의 `audioDuration` 필드를 복사
2. 컴포넌트 구현 — `~/.claude/skills/remotion-assembly/references/component-patterns.md` 참조
   - IPadTemplate — `~/.claude/skills/remotion-assembly/references/ipad-template-pattern.md` 참조
   - TimedSubtitle — narration 전문을 문장 단위로 분리하여 시간 기반 순차 자막 표시 (scene.narration 사용, scene.subtitle 아님)
   - SceneVisual — scene_plan.json의 visual 타입에서 직접 컴포넌트 매핑 + narration에서 props 추출
   - GlassCard, TerminalBlock, IconElement, BlogImage, SceneWithFade 등 필요한 컴포넌트
3. `src/MainVideo.tsx` — Sequence + Audio + BGM 조합
4. `src/Thumbnail.tsx` — 1280x720 Still
5. `src/Root.tsx` — Composition 등록
6. `src/index.ts` — 폰트 로딩

> **핵심**: scene_plan.json의 visual 타입과 narration에서 직접 컴포넌트를 매핑하고 props를 추출한다.
> 컴포넌트 매핑 테이블과 narration 추출 규칙은 remotion-assembly SKILL.md의 "SceneVisual 구현 방법" 섹션을 참조한다.

### 2.5단계: 긴 씬 스테이지 전개 적용 (필수)

아래 조건 중 **하나라도** 해당하는 씬은 **Stage Reveal 패턴**을 적용한다. 정적 카드가 18초 이상 떠 있으면 체감 지루함이 발생하기 때문.

1. `durationSec >= 18`
2. narration을 `.?!。`로 분리했을 때 **4개 문장 이상**
3. visual이 `glass-card`·`default-scene` 등 정적 카드 계열

적용 방법:
- 씬 전용 `SceneNReveal.tsx` 컴포넌트로 분리
- 씬 길이를 비율(0.22 / 0.48 / 0.78)로 4 스테이지 분할
- narration 문장 경계에 맞춰 스테이지 전환 타이밍 설정
- 마지막 스테이지에는 **URL/핵심 숫자/CTA 등 기억에 남을 요소** 배치 + glow 맥동 + 커서 깜빡임 강조
- 이전 스테이지 요소는 사라지지 않고 누적

상세 구현 패턴과 예시는 `~/.claude/skills/remotion-assembly/references/component-patterns.md`의 **"긴 씬의 시간차 전개 패턴 (Long-Scene Stage Reveal)"** 섹션 참조.

### 3단계: iPad 오버플로 검증 및 축소 적용 (필수)

iPad 스크린 내부 유효 콘텐츠 영역은 **세로 ≈720px** (`1002 - (paddingTop 90 + paddingBottom 90) = 822` 후 inner `scale(1.15)` 보정). 이 한도를 넘는 비주얼은 iPad 프레임 위·아래로 잘리거나 스크린 하단 자막(`bottom: 12`)과 겹친다.

`component-patterns.md`의 **"iPad 제약에 맞춘 축소 스펙"** 섹션에 아래 패턴들의 검증된 축소 수치가 정의되어 있다 — 해당 visual을 사용한 씬에는 반드시 그 스펙대로 래퍼/컴팩트화를 적용한다:

- `react-loop` (ReActLoopDiagram 1400×800) — `scale(0.82)`, margin ±72, gap 16
- `quadrant-matrix` (QuadrantMatrix 1200×700) — `scale(0.9)`, margin ±36, gap 12
- `horse-harness` (HorseHarnessDiagram 1200×700) — `scale(0.9)`, margin ±36, gap 12
- `lethal-triangle` (LethalTriangle 1200×800) — `scale(0.82)`, margin ±72, gap 12
- `concentric-rings` (ConcentricRings 1000×700) — `scale(0.9)`, margin ±36, gap 12 (필요 시)
- `rocket-trajectory` (1400×700) — `scale(0.9)`, margin ±36, gap 12 (필요 시)
- `timeline-cards` (5 스텝 이상) — **컴포넌트 내부 컴팩트화** (padding/fontSize/borderRadius 축소, 표 참조)

공통 래퍼 패턴 (수식: `M = H × (1 - S) / 2`):

```tsx
<div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: <GAP> }}>
  <StepBadge step="..." color="..." />
  <div style={{
    transform: "scale(<S>)",
    transformOrigin: "center center",   // ⚠️ 절대 "top center" 쓰지 말 것
    marginTop: -<M>,
    marginBottom: -<M>,
  }}>
    <HeavyDiagram {...} />
  </div>
</div>
```

**검증 절차**:
1. scene_plan.json 순회하며 위 패턴에 해당하는 씬 식별
2. 스펙대로 래퍼/컴팩트화 적용
3. 4단계 프리뷰에서 각 씬이 iPad 프레임 위·아래로 벗어나지 않는지, 하단 자막과 겹치지 않는지 시각 검증
4. 새 헤비 다이어그램 추가 시: 컴포넌트 높이 실측 → 수식으로 margin 계산 → Studio에서 검증

### 4단계: 프리뷰 (필수)
```bash
npx remotion studio src/index.ts --port 3123 --gl=angle
```
- 사용자에게 `http://localhost:3123` 접속 안내
- **사용자가 승인할 때까지 렌더링 금지**
- 수정 요청 시 코드 수정 → 핫리로드로 즉시 반영

### 5단계: 렌더링
```bash
# 영상
npx remotion render src/index.ts MainVideo --output ../output/output.mp4 \
  --gl=angle --codec h264 --ffmpeg-args "--vcodec h264_nvenc -preset p4" --overwrite

# 썸네일
npx remotion still src/index.ts Thumbnail --output ../output/thumbnail.png \
  --gl=angle --overwrite
```

## 입력

- `<project>/_workspace/scene_plan.json` — 씬 구조 (visual 타입, narration, subtitle, category)
- `<project>/_workspace/timing.json` — 타이밍 데이터
- `<project>/image/` — blog-image용 기존 이미지 (있는 경우)
- `<project>/music/` — BGM 파일

## 출력

- `<project>/<project-name>-video/` — 완성된 Remotion 프로젝트
- `<project>/output/output.mp4` — 최종 영상
- `<project>/output/thumbnail.png` — 썸네일

## 스킬 참조

`remotion-assembly` 스킬의 워크플로우를 따른다.

## 기술 사양

- 영상: 1920x1080, 30fps
- 썸네일: 1280x720
- 타이밍: `Math.round(sec * fps)` 프레임 정밀도
- 폰트: CookieRun (한국어), JetBrainsMono (코드)
- BGM 볼륨: 0.1 (10%)
- 씬 전환: 8프레임 crossfade

## 에러 핸들링

- npm 설치 실패 → Node.js 버전(v18+) 확인, 에러 보고
- TypeScript 컴파일 에러 → 수정 후 재빌드
- Remotion Studio 실행 실패 → 포트 충돌 확인 (3123), 대체 포트 시도
- GPU 렌더링 실패 → CPU 폴백 (`--ffmpeg-args` nvenc 플래그 제거)

## 컴포넌트 매핑 책임

video-composer가 scene_plan.json에서 직접 컴포넌트를 선택하고 narration에서 데이터를 추출한다.
매핑 테이블과 추출 규칙은 `~/.claude/skills/remotion-assembly/SKILL.md`의 "SceneVisual 구현 방법" 섹션에 정의되어 있다.
visual 타입 미인식 시 `default-scene` (GlassCard + BigTitle)로 fallback한다.

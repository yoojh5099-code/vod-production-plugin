---
name: remotion-assembly
description: |
  Remotion(React) 기반 YouTube 영상을 조립하는 스킬. 씬 데이터, 이미지, 음성, BGM을 조합하여 완성된 Remotion 프로젝트를 만들고 렌더링한다.
  vp-video-composer 에이전트가 사용한다. 직접 트리거되지 않으며, video-production 오케스트레이터를 통해 실행된다.
---

# Remotion 조립 스킬

씬 데이터, 이미지, 음성, BGM을 Remotion 프로젝트로 조립하여 YouTube 영상을 완성한다.

## 기술 사양

| 항목 | 값 |
|------|-----|
| 영상 해상도 | 1920x1080, 30fps |
| 썸네일 해상도 | 1280x720 |
| 타이밍 정밀도 | `Math.round(sec * fps)` |
| 폰트 (한국어) | CookieRun (Regular/Bold/Black) |
| 폰트 (코드) | JetBrains Mono (Google Fonts) |
| BGM 볼륨 | 0.1 (10%) |
| 씬 전환 | 8프레임 crossfade |
| GL 렌더러 | angle |
| 비디오 코덱 | h264_nvenc (GPU) |

## 프로젝트 셋업

### 디렉토리 구조 생성

```bash
cd <project>
npx create-video@latest --template blank <project-name>-video 2>/dev/null || true
cd <project-name>-video
npm install @remotion/google-fonts @remotion/media-utils @remotion/transitions
```

### 에셋 복사

```bash
# 폰트 (파일명에 공백 금지 — 공백 있으면 렌더링 시 404)
mkdir -p public/fonts
for f in ~/.claude/skills/remotion-assembly/references/font/*.otf; do
  cp "$f" "public/fonts/$(basename "$f" | tr -d ' ')"
done

# 오디오
mkdir -p public/audio
cp ../_workspace/tts/seg_*.wav public/audio/
cp ../music/*.mp3 public/audio/bgm.mp3 2>/dev/null || true
cp ../_workspace/timing.json public/audio/

# 이미지 (프로젝트 커스텀 — 우선)
mkdir -p public/images
cp ../image/*.png public/images/ 2>/dev/null || true
cp ../image/*.svg public/images/ 2>/dev/null || true

# ⚠️ 필수 에셋: 반드시 references/ 폴더에서만 복사할 것
# 프로젝트의 background/ 폴더나 다른 경로의 파일을 사용하지 않는다.
cp ~/.claude/skills/remotion-assembly/references/background.png public/images/background.png
cp ~/.claude/skills/remotion-assembly/references/mascot.png public/images/mascot.png

# 브랜드 로고 라이브러리 매칭 — 아래 "브랜드 로고 자동 매칭" 섹션 참조
# (narration 스캔 후 manifest.yml과 매칭되는 로고만 선택적으로 복사)
```

> **중요**: 모든 에셋 경로는 코드에서 `staticFile()` 사용 필수. `/images/xxx.png` 형태로 직접 참조하면 렌더링 시 404 에러 발생.

### remotion.config.ts

```typescript
import {Config} from '@remotion/cli/config';
Config.setVideoImageFormat('png');  // 투명도 지원 필수 — jpeg는 마스코트 배경이 흰색으로 됨
Config.setOverwriteOutput(true);
Config.setChromiumOpenGlRenderer('angle');
```

### 폰트 로딩 (`src/index.ts`)

CookieRun 폰트를 `@font-face`로 등록하고, 코드용 JetBrains Mono는 `@remotion/google-fonts`에서 로드한다.

**⚠️ 중요: 로컬 폰트는 반드시 `staticFile()`로 참조해야 한다. 절대 경로(`url('/fonts/...')`)를 사용하면 Remotion 렌더링 시 404 NetworkError가 발생한다.**

```typescript
import {registerRoot, staticFile} from 'remotion';
import {RemotionRoot} from './Root';
import {loadFont} from '@remotion/google-fonts/JetBrainsMono';

// JetBrains Mono (코드/터미널용)
loadFont('normal', {ignoreTooManyRequestsWarning: true});

// CookieRun (한국어 메인 폰트) — 반드시 staticFile() 사용
const cookieRunFonts = [
  {weight: '400', file: 'CookieRunRegular.otf'},
  {weight: '700', file: 'CookieRunBold.otf'},
  {weight: '900', file: 'CookieRunBlack.otf'},
];

for (const {weight, file} of cookieRunFonts) {
  const fontFace = new FontFace('CookieRun', `url('${staticFile(`fonts/${file}`)}')`, {
    weight,
    style: 'normal',
  });
  fontFace.load().then((loaded) => document.fonts.add(loaded));
}

registerRoot(RemotionRoot);
```

컴포넌트에서 사용 시:
```typescript
// 한국어 텍스트
style={{ fontFamily: 'CookieRun', fontWeight: 700 }}

// 코드/터미널
style={{ fontFamily: 'JetBrains Mono', fontWeight: 400 }}
```

## 씬 데이터 생성

`_workspace/timing.json` + `_workspace/scene_plan.json`을 조합하여 `src/data/scenes.ts`를 생성한다.
scene_plan.json의 visual 타입과 narration을 그대로 포함하여, SceneVisual에서 직접 컴포넌트 매핑 + props 추출에 사용한다.

```typescript
export type SceneCategory = 'intro' | 'why' | 'prep' | 'step' | 'demo' | 'outro';

export interface SceneData {
  id: number;
  startSec: number;
  durationSec: number;
  visual: string;       // scene_plan.json의 visual 타입 (컴포넌트 매핑에 사용)
  subtitle: string;     // scene_plan.json의 subtitle
  narration: string;    // scene_plan.json의 narration (props 추출 + 자막에 사용)
  category: SceneCategory;
  images: string[];     // blog-image용 기존 이미지 (있는 경우)
}

export const scenes: SceneData[] = [/* timing.json + scene_plan.json 기반 */];
// ⚠️ narration 필드는 scene_plan.json의 전체 원문을 그대로 사용할 것. 축약/요약 금지.
// TimedSubtitle 컴포넌트가 narration을 문장 단위로 분리하여 자막으로 표시한다.
export const FPS = 30;
export const TOTAL_DURATION_SEC = scenes.reduce((sum, s) => Math.max(sum, s.startSec + s.durationSec), 0);
export const TOTAL_DURATION_FRAMES = Math.round(TOTAL_DURATION_SEC * FPS);
```

### 배경 템플릿

배경은 **iPad 템플릿(background.png)** 고정. AuroraBackground는 사용하지 않는다.
iPad 화면은 투명 배경(흰색)이며, 모든 컨텐츠는 라이트 테마 색상을 사용한다.

> **⚠️ 필수 규칙 4가지:**
> 1. **iPad 프레임은 반드시 `background.png` 이미지를 `<Img>` 태그로 사용한다.** CSS gradient/SVG로 iPad를 그리지 않는다.
> 2. **마스코트는 모든 씬에서 표시가 기본이다.** intro/outro에서만 표시하는 것은 안티패턴. `showBear={i === 0 || i === scenes.length - 1}` 패턴 사용 금지.
> 3. **로컬 폰트는 반드시 `staticFile()`로 참조한다.** `url('/fonts/...')` 절대경로 사용 시 렌더링 404 에러 발생.
> 4. **자막은 TimedSubtitle 컴포넌트를 사용한다.** scene_plan.json의 narration 전문(축약/요약 금지)을 scenes.ts에 그대로 넣고, `<TimedSubtitle narration={scene.narration} durationInFrames={durationFrames} />`로 렌더링한다. subtitle 필드가 아닌 narration 필드를 자막으로 사용한다.

## 컴포넌트 구현

21개 컴포넌트 패턴의 상세 구현은 다음 참조 파일에 있다:

- **컴포넌트 패턴**: `~/.claude/skills/remotion-assembly/references/component-patterns.md`
  - 라이트 테마 색상 가이드 (iPad 흰 배경용)
  - visual 타입 → 컴포넌트 매핑 테이블
  - 기본 7종: TimedSubtitle, GlassCard, TerminalBlock, IconElement, BlogImage, SceneWithFade, AuroraBackground
  - 유틸 4종: BigTitle, StepBadge, ListItems, PipelineFlow
  - 고급 모션 6종: WordByWordText, SVGPathDraw, CountUpNumber, ProgressRing, MorphingShape, ParticleConfetti
  - PPT 카드 4종: StaggeredCards, ComparisonCards, FlipCard/FlipCardGrid, TimelineCards
  - 이징 가이드: Easing 6종 사용법
- **iPad 템플릿**: `~/.claude/skills/remotion-assembly/references/ipad-template-pattern.md`
  - IPadTemplate — `background.png` 이미지를 배경으로 사용 (CSS로 iPad 그리지 않음)
  - iPad 화면은 투명 배경 (`screenTint` 없음) — 흰색 화면 위에 라이트 테마 컨텐츠
  - 마스코트는 `TalkingMascot` 컴포넌트로 최상단 별도 레이어 (z-index 100)
  - 마스코트 입 애니메이션: 3개 sin파 합성으로 말하는 효과

### 브랜드 로고 자동 매칭 (references/brand-logos/)

공용 브랜드 로고 라이브러리 위치: `~/.claude/skills/remotion-assembly/references/brand-logos/`

- `manifest.yml` — 로고별 파일명 + aliases(검색어) + usage_note
- `*.svg` — 실제 로고 파일들 (공식 프레스킷 기반)

#### 사용 절차 (vp-video-composer가 Phase 3에서 수행)

```
1. manifest.yml 로드
2. scene_plan.json의 각 씬에 대해:
     - narration + subtitle + visual_note를 하나의 텍스트로 합침
     - logos[*].aliases 배열과 case-insensitive 부분 일치 검사
     - 매칭된 브랜드 키 목록을 scene에 첨부 (예: scene.matched_logos = ["datadog"])
3. 매칭된 모든 브랜드의 SVG 파일을
     ~/.claude/skills/remotion-assembly/references/brand-logos/{file}
     → <project>/<project-name>-video/public/images/{file}
     로 복사 (프로젝트 image/의 동명 파일이 있으면 덮어쓰지 않음 — 프로젝트 우선)
4. SceneVisual.tsx의 해당 씬에 BrandLogo 또는 컴포넌트별 logoSrc prop 주입:
     - StepBadge와 함께 쓰는 씬: <BrandLogo src="images/{file}" size={44} /> 좌측 정렬
     - QuadrantMatrix: quadrants[i].logoSrc = "images/{file}"
     - GlassCard 내부 타이틀: <BrandLogo src="..." size={72} /> 상단
     - 타이틀 카드(logo-meet): <BrandLogo src="..." size={100} label="by {Brand}" />
5. 매칭 리포트를 <project>/_workspace/logo_matches.md에 기록
     - 씬별 매칭 결과, 미매칭 브랜드 언급(사용자가 나중에 로고 추가하도록 안내)
```

#### BrandLogo 컴포넌트

로고 표시 전용 컴포넌트. `staticFile()`로 SVG/PNG 참조 + spring 입장 애니메이션.

```tsx
import React from "react";
import { Img, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

export const BrandLogo: React.FC<{
  src: string;          // 예: "images/datadog.svg"
  size?: number;        // 기본 120px
  delay?: number;       // 초 단위
  label?: string;       // 선택 라벨 (예: "by Anthropic")
  labelColor?: string;
}> = ({ src, size = 120, delay = 0, label, labelColor = "#475569" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enterProg = spring({
    frame: frame - Math.round(delay * fps),
    fps,
    config: { damping: 14, stiffness: 110, mass: 0.7 },
  });
  const opacity = interpolate(frame, [delay * fps, (delay + 0.3) * fps], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const scale = interpolate(enterProg, [0, 1], [0.85, 1]);
  return (
    <div style={{ display: "inline-flex", flexDirection: "column", alignItems: "center", gap: 8, opacity, transform: `scale(${scale})` }}>
      <Img src={staticFile(src)} style={{ width: size, height: size, objectFit: "contain" }} />
      {label && (
        <span style={{ fontSize: 18, fontWeight: 700, color: labelColor, fontFamily: "'CookieRun', sans-serif" }}>
          {label}
        </span>
      )}
    </div>
  );
};
```

#### 라이브러리 확장 규칙

새 로고가 필요해지면 (영상 제작 중 vp-video-composer가 발견한 미매칭 브랜드 포함):
1. 공식 프레스킷에서 SVG 다운 → `~/.claude/skills/remotion-assembly/references/brand-logos/{slug}.svg`
2. `manifest.yml`의 `logos` 섹션에 `slug: {file, aliases, usage_note}` 추가
3. `aliases`는 한국어·영어·대소문자 변형 모두 포함 (예: `[figma, FIGMA, 피그마]`)

#### 저작권 주의

- 대부분 nominative fair use(회사·제품 지칭 맥락)에서 허용되나 **최종 책임은 업로더**
- 로고 변형·왜곡·부정적 맥락 사용 금지
- `manifest.yml`의 `usage_note` 필드를 제작 전 확인할 것

### SceneVisual 구현 방법

`scene_plan.json`의 `visual` 타입과 `narration`에서 직접 컴포넌트를 매핑하고 props를 추출한다.

#### 컴포넌트 매핑 테이블

| visual 타입 | 컴포넌트 | 데이터 추출 방법 |
|------------|---------|----------------|
| `glass-card` | GlassCard + BigTitle | subtitle → emoji + title + description |
| `terminal-bg` | TerminalBlock | narration → 코드/명령어 라인 배열 추출 |
| `checklist` | GlassCard + ListItems | narration → 체크리스트 항목 배열 추출 |
| `pipeline-flow` | StepBadge + PipelineFlow | narration → 단계명 배열 추출 |
| `word-by-word` | WordByWordText | subtitle → 텍스트 그대로 |
| `count-up` | CountUpNumber (2~3개) | narration → 숫자 + 라벨 + suffix 추출 |
| `progress-ring` | ProgressRing (2~3개) | narration → % 수치 + 라벨 추출 |
| `svg-path-draw` | SVGPathDraw | narration → 노드 라벨 배열 추출 |
| `particle-confetti` | ParticleConfetti + WordByWordText | subtitle → 축하 텍스트 |
| `staggered-cards` | StaggeredCards | narration → icon + title + description 배열 추출 |
| `comparison-cards` | ComparisonCards | narration → left(title, items) + right(title, items) 추출 |
| `flip-cards` | FlipCardGrid | narration → front(icon, title) + back(title, description) 배열 추출 |
| `timeline-cards` | TimelineCards | narration → number + title + description 배열 추출 |
| `blog-image` | BlogImage | 프로젝트 `image/` 폴더의 기존 이미지 참조 |
| `logo-meet` | BigTitle + StepBadge | subtitle → 제목 + 뱃지 텍스트 |
| `default-scene` | GlassCard + BigTitle | subtitle → 제목 |

#### Narration 데이터 추출 규칙

각 visual 타입에 맞게 narration 텍스트를 파싱하여 컴포넌트 props로 변환한다:

- **checklist / staggered-cards**: 번호 리스트, 불릿 리스트, "첫째/둘째" 패턴에서 항목 추출
- **terminal-bg**: 백틱 코드 블록, `$` 시작 명령어, 인덴트된 코드 추출
- **comparison-cards**: "전/후", "Before/After", "vs" 구분자로 좌우 분리
- **count-up / progress-ring**: 숫자 + 단위(%, 배, 초, 개 등) 패턴 매칭
- **timeline-cards**: "1단계", "Step 1", 시간순 패턴에서 순서 추출
- **flip-cards**: 키워드 → 설명 쌍 추출 (콜론, 대시, 괄호 패턴)
- **pipeline-flow / svg-path-draw**: 화살표(→), 순서 패턴에서 단계명 추출

#### 레이아웃 규칙

모든 씬의 기본 구조:

```
SceneWithFade
  └─ IPadTemplate (screenTint 설정)
  │    └─ SceneVisual (매핑된 컴포넌트)
  ├─ Mascot (IPadTemplate 바깥, 모든 씬에서 표시)
  └─ TimedSubtitle (IPadTemplate 바깥, 하단)
```

**screenTint**: `terminal-bg`만 `"rgba(13,17,23,0.95)"`, 나머지 `"transparent"`

#### SceneVisual 코드 패턴

```typescript
// SceneVisual.tsx — scene_plan.json의 visual 타입에서 직접 컴포넌트 매핑
const SceneVisual: React.FC<{scene: SceneData}> = ({scene}) => {
  // narration에서 데이터를 추출하여 컴포넌트 props를 구성
  switch (scene.visual) {
    case 'word-by-word':
      return <WordByWordText text={scene.subtitle} fontSize={52} staggerFrames={4} />;
    case 'staggered-cards':
      return <StaggeredCards columns={2} cards={extractCards(scene.narration)} />;
    case 'comparison-cards':
      return <ComparisonCards {...extractComparison(scene.narration)} />;
    case 'terminal-bg':
      return <TerminalBlock lines={extractCodeLines(scene.narration)} />;
    case 'count-up':
      return <>{extractNumbers(scene.narration).map((n, i) => <CountUpNumber key={i} {...n} />)}</>;
    case 'timeline-cards':
      return <TimelineCards steps={extractSteps(scene.narration)} />;
    // ... 기타 visual 타입 (매핑 테이블 참조)
    default:
      return <GlassCard><BigTitle text={scene.subtitle} /></GlassCard>;
  }
};
```

> **핵심**: video-composer가 scene_plan.json에서 직접 컴포넌트를 매핑하고 narration에서 props를 추출한다.
> 중간 산출물(visual_spec.json) 없이 씬 구조에서 바로 Remotion 코드를 생성한다.

### 애니메이션 원칙

- `spring()`: 입장 애니메이션 (damping: 10-12, stiffness: 100-150, mass: 0.5-0.8)
- `interpolate()`: opacity, Ken Burns, 연속 모션
- 입장 후에도 동적 효과 유지 (플로팅, 스캔, 펄스) — 정적 화면 방지

### blog-image 씬 처리

`scene_plan.json`에서 `blog-image` 타입 씬을 확인하고 `<project>/image/` 폴더의 기존 이미지를 BlogImage 컴포넌트로 표시한다.
이미지가 없으면 `glass-card`로 fallback한다.

## MainVideo.tsx 패턴

```typescript
export const MainVideo: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {scenes.map((scene, i) => {
        const startFrame = Math.round(scene.startSec * fps);
        const durationFrames = Math.round(scene.durationSec * fps);
        return (
          <Sequence key={scene.id} from={startFrame} durationInFrames={durationFrames}>
            <SceneWithFade durationInFrames={durationFrames} isFirst={i === 0} isLast={i === scenes.length - 1}>
              <IPadTemplate>
                <SceneVisual sceneId={scene.id} visual={scene.visual} subtitle={scene.subtitle}
                  category={scene.category} images={scene.images} />
              </IPadTemplate>
              <Mascot size={260} />
              <TimedSubtitle narration={scene.narration} durationInFrames={durationFrames} />
            </SceneWithFade>
            {/* 씬별 오디오 100ms fade in/out — 씬 경계 체감 끊김 방지.
                반드시 scene.audioDurationSec(wav 실측, 패딩 제외) 기준으로 계산한다.
                durationFrames(패딩 포함)로 계산하면 음성 끝 전에 감쇠가 시작되어 말꼬리가 잘린다. */}
            <Audio
              src={staticFile(`audio/seg_${String(scene.id).padStart(2, '0')}.wav`)}
              volume={(f) => {
                const fadeFrames = Math.round(0.1 * fps);
                const audioFrames = Math.round(scene.audioDurationSec * fps);
                if (f < fadeFrames) return f / fadeFrames;
                if (f > audioFrames - fadeFrames)
                  return Math.max(0, (audioFrames - f) / fadeFrames);
                return 1;
              }}
            />
          </Sequence>
        );
      })}
      <Audio src={staticFile("audio/bgm.mp3")} volume={0.1} loop />
    </AbsoluteFill>
  );
};
```

### 씬 경계 오디오 체감 개선 — 필수 조합

씬 전환 시 "목소리가 중간에 잘리는 듯한 느낌"을 피하려면 아래 **두 가지를 함께** 적용해야 한다. 하나만 해서는 효과가 부족하다:

1. **씬 간 패딩 0.6초** (voice-production의 `generate_timing.py`에서 `PADDING_SEC = 0.6`) — wav 뒤에 호흡 공간 확보. 마지막 씬은 0.3초로 단축 (꼬리 공백 방지)
2. **씬별 오디오 100ms fade in/out** (위 MainVideo 코드) — 경계에서 선형 감쇠. wav 실측값(`audioDurationSec`) 기준이어야 페이드가 실제 음성 끝에 맞는다

### scenes.ts에 `audioDurationSec` 필드 필수

오디오 fade 계산의 기준이 되므로 `src/data/scenes.ts`의 `SceneData` 인터페이스에 반드시 포함한다:

```typescript
export interface SceneData {
  id: number;
  startSec: number;
  durationSec: number;        // 패딩 포함 (Sequence 길이 기준)
  audioDurationSec: number;   // wav 실측값 (패딩 제외, fade 기준)
  visual: string;
  subtitle: string;
  narration: string;
  category: SceneCategory;
  images: string[];
}
```

값은 `_workspace/timing.json`의 각 씬 `audioDuration` 필드를 그대로 복사한다.

기본 배경 템플릿은 **IPadTemplate**이다. `references/background.png` 이미지를 배경으로 사용한다.
CSS로 iPad 프레임을 그리지 않는다. background.png에는 iPad + 그라데이션만 포함되어 있다 (마스코트 미포함).
마스코트는 `references/mascot.png`를 별도 Mascot 컴포넌트로 렌더링한다.
상세 구현: `~/.claude/skills/remotion-assembly/references/ipad-template-pattern.md` 참조.

> **⚠️ background.png, mascot.png는 반드시 `~/.claude/skills/remotion-assembly/references/`에서만 복사한다.**
> 프로젝트의 `background/` 폴더나 다른 경로의 파일로 덮어쓰지 않는다.

## 프리뷰 (필수)

**전체 렌더링 전에 반드시 Remotion Studio에서 확인한다.**

```bash
cd <project-name>-video
npx remotion studio src/index.ts --port 3123 --gl=angle
```

사용자에게 `http://localhost:3123` 접속을 안내한다.

**확인 항목:**
- 씬 전환, 애니메이션 동작
- 이미지 크기/레이아웃
- 자막 싱크, 가독성
- BGM 재생 (끝까지 반복되는지)
- 전체 흐름 타임라인 확인

수정 요청 시 코드 수정 → 핫리로드 → 재확인. **사용자 승인 후에만 렌더링.**

## 렌더링

```bash
# 영상
npx remotion render src/index.ts MainVideo --output ../output/output.mp4 \
  --gl=angle --codec h264 --ffmpeg-args "--vcodec h264_nvenc -preset p4" --overwrite

# 썸네일
npx remotion still src/index.ts Thumbnail --output ../output/thumbnail.png \
  --gl=angle --overwrite
```

GPU 렌더링 실패 시 CPU 폴백:
```bash
npx remotion render src/index.ts MainVideo --output ../output/output.mp4 \
  --gl=angle --codec h264 --overwrite
```

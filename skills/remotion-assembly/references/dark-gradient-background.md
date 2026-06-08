# Dark Gradient Background — 표준 배경 (2026-05-19 확정)

iPad 템플릿/마스코트 폐지 이후의 새 배경 표준. 1920×1080 풀스크린 다크 그라디언트 + 상단 amber radial 액센트만 사용한다.

> **변경 배경**: 이전에는 `references/background.png`(iPad 프레임 + 그라디언트) + `references/mascot.png`(북극곰)를 모든 씬에 깔았다. codex-mobile 프로젝트(2026-05-17~18)에서 풀스크린 다크 그라디언트로 전환한 결과 — 콘텐츠 가독성, 텍스트 대비, 모션 프리뷰 모두에서 더 나았기에 이를 새 표준으로 채택한다.

## 핵심 원칙

> **1.** 풀스크린 1920×1080. iPad 프레임/노치/홈 인디케이터 같은 디바이스 mockup을 배경에 그리지 않는다.
> **2.** 마스코트 캐릭터는 사용하지 않는다. `Mascot` 컴포넌트와 `mascot.png` 모두 더 이상 import/복사하지 않는다.
> **3.** 배경은 CSS로 직접 그린다 — `background.png` 같은 비트맵 의존 없음.
> **4.** 콘텐츠는 다크 톤에 맞춘 밝은 텍스트(slate-100~300)와 액센트 컬러(amber/cyan/emerald/rose/violet)를 사용한다.
> **5.** 모든 에셋 경로는 `staticFile()` 사용 (폰트, 오디오, 브랜드 로고 등 — 단 배경은 CSS이므로 해당 없음).

## 표준 배경 사양

```css
/* MainVideo.tsx의 최외곽 AbsoluteFill에 적용 */
background:
  radial-gradient(ellipse at top, rgba(245, 158, 11, 0.12) 0%, transparent 55%),
  linear-gradient(180deg, #0b1120 0%, #1e293b 50%, #0b1120 100%);
```

| 레이어 | 값 | 역할 |
|---|---|---|
| 베이스 그라디언트 | `linear-gradient(180deg, #0b1120 0%, #1e293b 50%, #0b1120 100%)` | 위·아래 진네이비, 중앙 살짝 밝아짐 — 시선이 가운데로 모임 |
| 상단 액센트 | `radial-gradient(ellipse at top, rgba(245,158,11,0.12) 0%, transparent 55%)` | amber radial이 상단에서 살짝 발광 — 따뜻한 질감 |

> 두 그라디언트는 **콤마로 결합**한다 (radial을 위에 쌓아야 액센트가 얹힘). React 인라인 스타일에서는 `background: "radial-gradient(...), linear-gradient(...)"` 한 줄로 작성.

## 컬러 팔레트 (다크 캔버스 기준)

> **이전(iPad 흰 배경)**: 텍스트는 slate-800/600, 카드 배경은 인디고 틴트.
> **현재(다크 그라디언트)**: 텍스트는 slate-100/200/300, 카드 배경은 진네이비 + 액센트 보더 + glow.

### 텍스트

| 용도 | 색상 | 코드 |
|------|------|------|
| 제목 (강조) | slate-50 | `#f8fafc` |
| 제목 (기본) | slate-100 | `#f1f5f9` |
| 본문 | slate-200 | `#e2e8f0` |
| 보조/캡션 | slate-300 | `#cbd5e1` |
| 비활성/메타 | slate-400 | `#94a3b8` |
| 미지정 라벨 | slate-500 | `#64748b` (점선/축 등 비활성 요소만) |

### 액센트 (의도별)

| 의도 | 색상 | 코드 |
|---|---|---|
| 메인 강조 (warm) | amber-500 | `#f59e0b` |
| 정보/링크 (cool) | cyan-400 | `#22d3ee` |
| 성공/긍정 | emerald-500 | `#10b981` |
| 위험/경고 | rose-500 | `#f43f5e` |
| 보조 (보라) | violet-400 | `#a78bfa` |

> 액센트 5종을 한 영상에서 모두 쓰지 말 것 — 영상당 **메인 1 + 보조 1~2개** 권장. 의도가 흐려진다.

### 카드 / 컨테이너

| 용도 | 코드 |
|---|---|
| 카드 배경 (기본) | `linear-gradient(180deg, rgba(15,23,42,0.85), rgba(11,17,32,0.95))` |
| 카드 보더 | `1px solid rgba(245,158,11,0.25)` (메인 액센트 0.25 알파) |
| 카드 glow | `box-shadow: 0 0 32px rgba(245,158,11,0.18), inset 0 1px 0 rgba(255,255,255,0.04)` |
| 비활성 카드 배경 | `rgba(51,65,85,0.92)` (slate-700, 암색 묻힘 방지) |
| 비활성 카드 보더 | `1px solid rgba(148,163,184,0.25)` |

### 점선/축/구분선 (slate-700/800 금지)

다크 배경에 slate-700(`#334155`) 이하 톤은 거의 보이지 않는다. 구분선·점선은 **slate-400(`#94a3b8`) 또는 slate-500(`#64748b`)** 사용.

| 요소 | 권장 색 |
|---|---|
| 점선 축 (Quadrant 등) | `#64748b` |
| 비활성 화살표/노드 | `#94a3b8` |
| 미체크 박스 보더 | `#94a3b8` |

## MainVideo.tsx 패턴 (표준)

```tsx
import { AbsoluteFill, Sequence, Audio, staticFile, useVideoConfig } from "remotion";
import { scenes } from "./data/scenes";
import { SceneVisual } from "./components/SceneVisual";
import { TimedSubtitle } from "./components/TimedSubtitle";
import { SceneWithFade } from "./components/SceneWithFade";

export const MainVideo: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(ellipse at top, rgba(245,158,11,0.12) 0%, transparent 55%), " +
          "linear-gradient(180deg, #0b1120 0%, #1e293b 50%, #0b1120 100%)",
      }}
    >
      {scenes.map((scene, i) => {
        const startFrame = Math.round(scene.startSec * fps);
        const durationFrames = Math.round(scene.durationSec * fps);
        const audioFrames = Math.round(scene.audioDurationSec * fps);
        const fadeFrames = Math.round(0.1 * fps);
        const isFirst = i === 0;
        const isLast = i === scenes.length - 1;

        return (
          <Sequence key={scene.id} from={startFrame} durationInFrames={durationFrames}>
            <SceneWithFade
              durationInFrames={durationFrames}
              isFirst={isFirst}
              isLast={isLast}
            >
              <AbsoluteFill
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  padding: "80px 120px 200px", // 하단 200px = 자막 safe area
                }}
              >
                <SceneVisual scene={scene} />
              </AbsoluteFill>
              <TimedSubtitle
                narration={scene.narration}
                durationInFrames={audioFrames}
              />
            </SceneWithFade>
            <Audio
              src={staticFile(`audio/seg_${String(scene.id).padStart(2, "0")}.wav`)}
              volume={(f) => {
                if (f < fadeFrames) return f / fadeFrames;
                if (f > audioFrames - fadeFrames)
                  return Math.max(0, (audioFrames - f) / fadeFrames);
                return 1;
              }}
            />
          </Sequence>
        );
      })}
      {/* BGM (있는 경우) */}
      {/* <Audio src={staticFile("audio/bgm.mp3")} volume={0.08} loop /> */}
    </AbsoluteFill>
  );
};
```

### 레이아웃 표준 (1920×1080)

| 항목 | 값 | 비고 |
|---|---|---|
| 캔버스 | 1920 × 1080 | 풀스크린, iPad 프레임 없음 |
| 콘텐츠 패딩 | `80px 120px 200px` | 좌·우 120, 상 80, 하 200(자막 영역) |
| 자막 위치 | 캔버스 하단(=200px safe area 내) | TimedSubtitle 표준은 `bottom: 80~120` 사이에서 가독성 우선 |
| 콘텐츠 가용 영역 | 1680 × 800 | 패딩 적용 후 — 이전 iPad 720px보다 80px 더 여유 |

> **iPad 시절 축소 스펙은 더 이상 필수가 아니다.** 콘텐츠 가용 높이가 720→800px로 늘어났기 때문에 react-loop·quadrant-matrix·timeline-cards 등 헤비 다이어그램은 원본 크기 그대로 들어가는 경우가 많다. 다만 1080 캔버스를 넘어가는 다이어그램(예: 900px 이상)은 여전히 scale 0.85~0.9 권장.

## 자막 (TimedSubtitle) 표준

자막은 캔버스 좌표 기준 — 더 이상 iPad 스크린 로컬 좌표를 쓰지 않는다.

```tsx
<div
  style={{
    position: "absolute",
    bottom: 96,                    // 200px safe area 내 중간 — 가독성 우선
    left: "50%",
    transform: "translateX(-50%)",
    maxWidth: 1600,
    width: "max-content",
    zIndex: 50,
    pointerEvents: "none",
  }}
>
  <div
    style={{
      background: "rgba(11, 17, 32, 0.78)",
      backdropFilter: "blur(10px)",
      borderRadius: 14,
      padding: "16px 38px",
      border: "1px solid rgba(245, 158, 11, 0.18)",
    }}
  >
    <span
      style={{
        color: "#f1f5f9",
        fontSize: 36,
        fontFamily: "'CookieRun', sans-serif",
        fontWeight: 500,
        lineHeight: 1.4,
      }}
    >
      {currentText}
    </span>
  </div>
</div>
```

> **변경점 vs 이전 iPad 자막**: 배경 alpha를 0.78로 유지하되 색은 `#000` → `#0b1120`(베이스 그라디언트와 동일)로. 보더 색을 amber 0.18 알파로 줘서 메인 액센트와 호응.

## 마스코트 — 사용하지 않음

- `Mascot.tsx`, `references/mascot.png`, `IPadTemplate`의 `overlay` prop 등 **모든 마스코트 관련 코드는 신규 프로젝트에서 제거**한다.
- 기존 프로젝트의 마스코트는 호환을 위해 그대로 두되, 새 영상에는 도입하지 않는다.
- 후킹 영상(`OffthreadVideo` 인서트)이 있는 경우 마스코트 위치를 참고할 필요 없음 — 후킹은 캔버스를 풀스크린으로 채운다.

## 후킹 비디오 인서트 (선택)

오프닝에 외부 데모 영상(예: 제품 공식 데모)을 인서트할 때:

```tsx
import { OffthreadVideo, staticFile } from "remotion";

// SceneVisual.tsx 내 'intro-clip' 케이스
<AbsoluteFill style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
  <OffthreadVideo
    src={staticFile("video/intro_clip.mp4")}
    style={{
      width: "100%",
      height: "100%",
      objectFit: "cover",
    }}
  />
</AbsoluteFill>
```

> 부모 `AbsoluteFill`은 padding과 무관하게 padding box(=1920×1080 캔버스)를 채우므로 별도 음수 마진 보정이 필요 없다. 후킹 영상은 정중앙 자동 정렬된다.

## 폰트

| 폰트 | 용도 | 로딩 |
|---|---|---|
| CookieRun (Regular/Bold/Black) | 한국어 본문·자막 | `staticFile("fonts/CookieRun{Regular|Bold|Black}.otf")` 로컬 |
| JetBrains Mono | 코드/터미널/URL | `@remotion/google-fonts/JetBrainsMono` |

> 로컬 폰트 파일명에 공백 금지(`CookieRun Bold.otf` ❌). `staticFile()` 사용 필수 (`/fonts/...` 절대 경로 ❌).

## 에셋 복사 (프로젝트 셋업 시)

```bash
# 폰트 — 공백 제거 필수
mkdir -p public/fonts
for f in ~/.claude/skills/remotion-assembly/references/font/*.otf; do
  cp "$f" "public/fonts/$(basename "$f" | tr -d ' ')"
done

# 오디오
mkdir -p public/audio
cp ../_workspace/tts/seg_*.wav public/audio/
cp ../music/*.mp3 public/audio/bgm.mp3 2>/dev/null || true
cp ../_workspace/timing.json public/audio/

# 이미지 (프로젝트 커스텀 + 브랜드 로고 매칭 결과만)
mkdir -p public/images
cp ../image/*.png public/images/ 2>/dev/null || true
cp ../image/*.svg public/images/ 2>/dev/null || true

# ❌ 더 이상 복사하지 않는 파일:
#   ~/.claude/skills/remotion-assembly/references/background.png  (iPad 프레임 — 폐지)
#   ~/.claude/skills/remotion-assembly/references/mascot.png      (북극곰 — 폐지)

# 브랜드 로고는 manifest.yml 매칭 결과만 선택적 복사 (component-patterns.md 참조)
```

## 마이그레이션 체크리스트 (구 프로젝트 → 신 표준)

기존 iPad 기반 프로젝트를 다크 그라디언트 표준으로 이전할 때:

1. `MainVideo.tsx` 최외곽 `AbsoluteFill`의 `backgroundColor: "#000"` → 위 표준 그라디언트 두 줄로 교체
2. `IPadTemplate` 사용처 모두 제거 — 직접 `<AbsoluteFill style={{ display:"flex", alignItems:"center", justifyContent:"center", padding: "80px 120px 200px" }}>` 로 감쌈
3. `<Mascot />` 컴포넌트 사용처 전부 삭제. `Mascot.tsx` 파일은 보관(다른 프로젝트 호환), import만 제거
4. `TimedSubtitle` 위치를 iPad 스크린 로컬(`bottom: 12`)에서 캔버스 글로벌(`bottom: 96`)로 변경. 색·보더는 위 자막 코드 참조
5. `SceneVisual.tsx`의 텍스트 색을 라이트 테마(`#1e293b` 등)에서 다크 테마(`#f1f5f9` 등)로 일괄 치환
6. 점선/축/비활성 요소: `#475569` → `#94a3b8` 또는 `#64748b`로 상향
7. `screenTint` prop과 `terminal-bg`의 다크 오버레이는 **그대로 유지** — 다크 그라디언트와 자연스럽게 합쳐짐
8. 헤비 다이어그램(react-loop, quadrant-matrix 등)의 scale·margin 래퍼는 **선택적**으로 유지. 1920×1080·콘텐츠 800px 영역에 들어가면 원본 그대로 사용 가능

## 안티패턴

- `background.png`를 `<Img>`로 깔고 그 위에 그라디언트를 오버레이 — 비트맵을 굳이 쓸 이유가 없다. CSS 그라디언트가 렌더 비용 0
- iPad 베젤/노치를 SVG로 다시 그림 — 새 표준은 풀스크린이다
- 캐릭터/마스코트를 우하단에 고정 — 정보 밀도를 떨어뜨리고 채널 의존성을 만든다
- 다크 배경에 slate-700/800 톤의 텍스트·구분선 — 거의 보이지 않음. slate-300 이상 또는 slate-400~500 사용
- 액센트 컬러 5종을 한 씬에 동시 사용 — 의도 분산. 메인 1 + 보조 1~2개 원칙

## 참고 프로젝트

`vod/codex-mobile/codex-mobile-video/` — 본 표준의 레퍼런스 구현. 16개 다크톤 패턴 컴포넌트 + 30씬 (hook 포함) 9분 영상.

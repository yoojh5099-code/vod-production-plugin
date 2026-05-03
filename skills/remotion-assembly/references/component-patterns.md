# Remotion 컴포넌트 패턴 레퍼런스

YouTube 영상 제작 시 사용하는 핵심 컴포넌트들의 구현 패턴.
이 파일의 코드를 그대로 복사하여 프로젝트에 사용할 수 있다.

## 라이트 테마 색상 가이드 (iPad 배경용)

> **중요**: iPad 배경(background.png)은 흰색 화면이므로, 모든 텍스트/UI 요소는 **라이트 테마** 색상을 사용한다.
> TerminalBlock만 예외로 다크 테마를 유지한다.

| 용도 | 색상 | 코드 |
|------|------|------|
| 제목 텍스트 | slate-800 | `#1e293b` |
| 본문 텍스트 | slate-600 | `#475569` |
| 서브/라벨 텍스트 | slate-500 | `#64748b` |
| SVG 라벨 | slate-700 | `#334155` |
| GlassCard 배경 | 인디고 틴트 | `rgba(99,102,241,0.12)` |
| GlassCard 테두리 | 인디고 | `rgba(99,102,241,0.3)` |
| ListItem 배경 | 인디고 틴트 | `rgba(99,102,241,0.06)` |
| ListItem 활성 배경 | 그린 틴트 | `rgba(16,185,129,0.12)` |
| ListItem 체크박스 기본 | 인디고 | `#6366f1` |
| ListItem 체크박스 활성 | 에메랄드 | `#10b981` |
| ListItem 활성 텍스트 | 에메랄드 진 | `#059669` |
| Pipeline 기본 텍스트 | slate-700 | `#334155` |
| Pipeline 활성 텍스트 | 에메랄드 진 | `#059669` |
| Subtitle 배경 | 인디고 | `rgba(99,102,241,0.9)` |
| Subtitle 텍스트 | 흰색 | `#ffffff` |
| TerminalBlock 배경 | 다크 (유일한 예외) | `rgba(13,17,23,0.95)` |
| TerminalBlock 텍스트 | 밝은 회색 | `#e2e8f0` |

### visual 타입 → 컴포넌트 매핑

scene_plan.json의 `visual` 필드에 따라 아래 컴포넌트를 사용한다:

| visual 타입 | 컴포넌트 | 데이터 소스 |
|------------|---------|------------|
| `glass-card` | GlassCard + 이모지/제목/설명 | subtitle, narration |
| `terminal-bg` | TerminalBlock | narration에서 코드 추출 |
| `checklist` | GlassCard + ListItems | narration에서 항목 추출 |
| `pipeline-flow` | StepBadge + PipelineFlow | narration에서 단계 추출 |
| `word-by-word` | WordByWordText | subtitle 텍스트 |
| `count-up` | CountUpNumber (2~3개 나열) | narration에서 숫자 추출 |
| `progress-ring` | ProgressRing (2~3개 나열) | narration에서 % 추출 |
| `svg-path-draw` | SVGPathDraw (커스텀 노드) | narration에서 단계 추출 |
| `particle-confetti` | ParticleConfetti + WordByWordText | subtitle |
| `staggered-cards` | StaggeredCards | narration에서 항목 추출 (icon+title+desc) |
| `comparison-cards` | ComparisonCards | narration에서 좌/우 항목 추출 |
| `flip-cards` | FlipCardGrid | narration에서 키워드→상세 추출 |
| `timeline-cards` | TimelineCards | narration에서 단계별 추출 |
| `tweet-card` | TweetCard | 인용 트윗 (author/handle/text/accentWords) |
| `code-split` | CodeEditorSplit | 좌/우 코드 비교 (leftLines/rightLines/warningText) |
| `rocket-trajectory` | RocketTrajectory | 성장 곡선 (milestones + finalValue) |
| `lethal-triangle` | LethalTriangle | 위험 요소 3종 경고 (vertices + centerLabel) |
| `horse-harness` | HorseHarnessDiagram | 모델+하네스 합성 (horseLabel/parts) |
| `react-loop` | ReActLoopDiagram | 순환 루프 다이어그램 (nodes/descendants) |
| `quadrant-matrix` | QuadrantMatrix | 2×2 분면 (xAxis/yAxis/quadrants) |
| `definition-formula` | DefinitionFormula | "X = A + B" 공식 정의 레이아웃 (title/caption/terms[]) |
| `animated-pie` | AnimatedPieChart | 애니메이션 파이차트 (segments[] with value/label/color) |
| `morphing-shape` | MorphingShape | 도형 모핑 (interpolatePath) |
| `metaphor-split` | MetaphorSplit | 은유 대비 2분할 (leftIcon/leftLabel/leftMetaphor + right) |
| `quadrant-matrix-v2` | QuadrantMatrix v2 | 축 라벨 가독성 개선판 (흰 배경 칩 + zIndex:10) |
| `dual-timeline` | DualTimeline | 상/하 이중 타임라인 (rows[] with behavior: repeat/accumulate) |
| `scale-bar` | ScaleBar | 1차원 스케일 축 + 마커 (leftLabel/rightLabel/markers[]/banner?) |
| `three-layer-architecture` | ThreeLayerArchitecture | 3계층 스택 (layers[] with name/chips/desc + flowLabels[]) |
| `pipeline-flow-setup` | SetupStepsSynced | 4카드 자막 싱크 순차 하이라이트 (scene prop) |
| `staggered-cards-overview` | StaggeredCards (overview 변종) | 헤더만 간략 표시, 디테일은 이어지는 씬에서 |
| `three-options-image-cards` | ThreeOptionsImageCards | 이미지 3카드 (options[] with imageSrc/label/sub/color) |
| `file-tree-detail` | FileTreeDetail | 파일 트리 + 운영 원칙 카드 (root/tree[]/principles[]) |
| `terminal-mock` | TerminalMock | CLI 타이핑 애니메이션 (prompt/commands[]) |
| `mcp-wiring` | McpWiring | 배선 다이어그램 + narration sync (nodes/edges/triggers) |
| `emphasis-pill` | EmphasisPill | 한 줄 강조 알약 (text/icon?/color?) |
| `critique-checklist` | CritiqueChecklistSynced | 3항목 자막 싱크 체크리스트 (첫째/둘째/셋째) |
| `lint-report` | LintReportCard | 분석 리포트 (claim vs counter + ⚠ conflict + conclusion) |
| `logo-meet` | BigTitle + StepBadge | subtitle |
| `default-scene` | GlassCard + BigTitle | subtitle |

## 목차
1. [TimedSubtitle](#timedsubtitle) - 시간 기반 하단 자막 (narration 문장 단위 순차 표시)
2. [GlassCard](#glasscard) - 글래스모피즘 카드
3. [TerminalBlock](#terminalblock) - 터미널 코드 블록
4. [SceneWithFade](#scenewithfade) - 씬 전환 래퍼
5. [애니메이션 유틸리티](#animation-utils) - BigTitle / StepBadge / **NumberedBadge** / **EmphasisPill** / ListItems / PipelineFlow
6. [시그니처 컴포넌트](#signature-components) - TweetCard / CodeEditorSplit / RocketTrajectory / LethalTriangle / HorseHarnessDiagram / ReActLoopDiagram / QuadrantMatrix / **QuadrantMatrix v2** / **DualTimeline** / **ThreeLayerArchitecture** / **FileTreeDetail** / **TerminalMock** / **McpWiring** / **LintReportCard**
7. [PPT 카드 패턴](#ppt-스타일-카드-패턴) - StaggeredCards / ComparisonCards / **MetaphorSplit** / **ThreeOptionsImageCards** / FlipCard / TimelineCards
8. [스페셜 차트](#special-charts) - AnimatedPieChart / **ScaleBar**
9. [인프라](#infrastructure) - DynamicBackground
10. **[자막 싱크 하이라이트](#자막-싱크-하이라이트-narration-synced-highlights)** - SetupStepsSynced / CritiqueChecklistSynced (narration 문장 단위 UI 순차 강조)
11. [iPadTemplate](ipad-template-pattern.md) - iPad Pro 배경 래퍼 (별도 파일)
12. [iPad 제약에 맞춘 축소 스펙](#ipad-제약에-맞춘-축소-스펙-ipad-overflow-compensation) - react-loop/quadrant-matrix/timeline-cards 등 세로 오버플로 대응 수치

---

## TimedSubtitle

시간 기반 하단 자막. narration을 문장 단위(`.` `?` `!` 기준)로 분리하고, 글자 수 비율로 타이밍을 배분하여 순차 표시한다.
TTS 음성과 동기화된 자막 효과를 제공한다.

```tsx
import React, { useMemo } from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

interface TimedSegment {
  text: string;
  startFrame: number;
  endFrame: number;
}

export const TimedSubtitle: React.FC<{
  narration: string;
  durationInFrames: number;
}> = ({ narration, durationInFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const segments = useMemo((): TimedSegment[] => {
    const sentences = narration
      .split(/(?<=[.?!。])\s*/)
      .map((s) => s.trim())
      .filter((s) => s.length > 0);

    if (sentences.length === 0) return [];

    const totalChars = sentences.reduce((sum, s) => sum + s.length, 0);
    let currentFrame = 0;

    return sentences.map((text) => {
      const ratio = text.length / totalChars;
      const segDuration = Math.round(ratio * durationInFrames);
      const seg: TimedSegment = {
        text,
        startFrame: currentFrame,
        endFrame: currentFrame + segDuration,
      };
      currentFrame += segDuration;
      return seg;
    });
  }, [narration, durationInFrames]);

  const current = segments.find(
    (s) => frame >= s.startFrame && frame < s.endFrame
  );
  if (!current) return null;

  const FADE = Math.min(Math.round(0.15 * fps), 5);
  const fadeIn = interpolate(
    frame,
    [current.startFrame, current.startFrame + FADE],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <div style={{
      position: "absolute", bottom: 60, left: 0, right: 0,
      display: "flex", justifyContent: "center", opacity: fadeIn, zIndex: 50,
    }}>
      <div style={{
        background: "rgba(0, 0, 0, 0.7)", backdropFilter: "blur(10px)",
        borderRadius: 12, padding: "14px 36px", maxWidth: 1400,
        border: "1px solid rgba(255, 255, 255, 0.08)",
      }}>
        <span style={{
          color: "#e2e8f0", fontSize: 36,
          fontFamily: "'CookieRun', sans-serif", fontWeight: 500,
          letterSpacing: "-0.02em", textShadow: "0 2px 8px rgba(0,0,0,0.5)",
        }}>{current.text}</span>
      </div>
    </div>
  );
};
```

## GlassCard

글래스모피즘 정보 카드. spring 바운스 입장 + 입장 후 미세 플로팅 효과.

```tsx
import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const GlassCard: React.FC<{
  children: React.ReactNode;
  width?: number | string;
  height?: number | string;
  style?: React.CSSProperties;
  delay?: number;
}> = ({ children, width = "auto", height = "auto", style, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // spring 바운스 입장 (자연스러운 물리 기반)
  const enterProgress = spring({
    frame: frame - Math.round(delay * fps),
    fps,
    config: { damping: 12, stiffness: 100, mass: 0.8 },
  });
  const opacity = interpolate(frame, [delay * fps, (delay + 0.3) * fps], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  const slideY = interpolate(enterProgress, [0, 1], [30, 0]);
  const scale = interpolate(enterProgress, [0, 1], [0.95, 1]);

  // 입장 후 미세 플로팅 (사인파 ±3px)
  const floatY = enterProgress >= 0.95
    ? Math.sin((frame / fps) * 1.8) * 3
    : 0;

  return (
    <div style={{
      width, height,
      background: "rgba(255, 255, 255, 0.05)",
      backdropFilter: "blur(20px)", WebkitBackdropFilter: "blur(20px)",
      borderRadius: 20,
      border: "1px solid rgba(255, 255, 255, 0.1)",
      boxShadow: "0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.1)",
      padding: 40, opacity,
      transform: `translateY(${slideY + floatY}px) scale(${scale})`,
      ...style,
    }}>{children}</div>
  );
};
```

## TerminalBlock

macOS 스타일 터미널 UI. 줄별 순차 등장 애니메이션.

```tsx
import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const TerminalBlock: React.FC<{
  lines: string[];
  highlightLine?: number;
  title?: string;
}> = ({ lines, highlightLine, title = "Terminal" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{
      width: 900, background: "rgba(13, 17, 23, 0.9)", borderRadius: 16,
      border: "1px solid rgba(255, 255, 255, 0.1)",
      boxShadow: "0 20px 60px rgba(0,0,0,0.5)", overflow: "hidden",
    }}>
      {/* Title bar with traffic lights */}
      <div style={{
        display: "flex", alignItems: "center", gap: 8, padding: "12px 16px",
        background: "rgba(255, 255, 255, 0.03)",
        borderBottom: "1px solid rgba(255, 255, 255, 0.06)",
      }}>
        <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#ff5f57" }} />
        <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#febc2e" }} />
        <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#28c840" }} />
        <span style={{
          marginLeft: 12, color: "rgba(255,255,255,0.4)", fontSize: 14,
          fontFamily: "'JetBrains Mono', monospace",
        }}>{title}</span>
      </div>
      {/* Lines with staggered animation */}
      <div style={{ padding: "20px 24px" }}>
        {lines.map((line, i) => {
          const lineDelay = i * 0.15;
          const lineOpacity = interpolate(frame, [lineDelay * fps, (lineDelay + 0.3) * fps], [0, 1], {
            extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          const isHighlighted = highlightLine === i;
          return (
            <div key={i} style={{
              opacity: lineOpacity, padding: "4px 8px", borderRadius: 4, marginBottom: 4,
              background: isHighlighted ? "rgba(16, 185, 129, 0.15)" : "transparent",
              borderLeft: isHighlighted ? "3px solid #10b981" : "3px solid transparent",
            }}>
              <span style={{
                fontFamily: "'JetBrains Mono', monospace", fontSize: 22,
                color: isHighlighted ? "#34d399" : "#e2e8f0", whiteSpace: "pre",
              }}>{line}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
```

## IconElement

SVG 아이콘 렌더러. 18종 내장 아이콘 (aws, claude, shield, key, gear, terminal, graph, check, rocket, lock, database, cloud, code, network, dollar, users, lightning, globe, puzzle).

영상 주제에 따라 새 아이콘을 ICONS 객체에 추가할 수 있다.

```tsx
import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

const ICONS: Record<string, { paths: string[]; color: string; viewBox?: string }> = {
  // 기본 제공 아이콘 (실제 프로젝트에서 필요한 아이콘의 SVG path를 추가)
  aws: { paths: ["M..."], color: "#FF9900", viewBox: "0 0 32 32" },
  claude: { paths: ["M..."], color: "#D97757" },
  shield: { paths: ["M..."], color: "#10b981" },
  // ... (영상 주제에 맞게 확장)
};

export const IconElement: React.FC<{
  name: string; size?: number; delay?: number;
  label?: string; glow?: boolean; pulse?: boolean;
}> = ({ name, size = 80, delay = 0, label, glow = true, pulse = false }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const icon = ICONS[name] || ICONS.aws;

  // spring 바운스 입장
  const springProgress = spring({
    frame: frame - Math.round(delay * fps),
    fps,
    config: { damping: 10, stiffness: 120, mass: 0.6 },
  });
  const opacity = interpolate(frame, [delay * fps, (delay + 0.25) * fps], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  const scale = interpolate(springProgress, [0, 1], [0.5, 1]);
  const pulseScale = pulse ? 1 + 0.03 * Math.sin((frame / fps) * 3) : 1;

  return (
    <div style={{
      display: "flex", flexDirection: "column", alignItems: "center", gap: 14,
      opacity, transform: `scale(${scale * pulseScale})`,
    }}>
      <div style={{
        width: size, height: size, borderRadius: size * 0.25,
        background: "linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02))",
        border: `1.5px solid ${icon.color}44`,
        display: "flex", alignItems: "center", justifyContent: "center",
        boxShadow: glow
          ? `0 0 40px ${icon.color}33, 0 0 80px ${icon.color}11, inset 0 1px 0 rgba(255,255,255,0.1)`
          : "0 4px 16px rgba(0,0,0,0.3)",
        position: "relative",
      }}>
        <svg viewBox={icon.viewBox || "0 0 48 48"} width={size * 0.55} height={size * 0.55}
          fill={icon.color} style={{ position: "relative", zIndex: 1 }}>
          {icon.paths.map((d, i) => <path key={i} d={d} />)}
        </svg>
      </div>
      {label && (
        <span style={{
          color: "rgba(255,255,255,0.75)", fontSize: Math.max(16, size * 0.2),
          fontFamily: "'CookieRun', sans-serif", fontWeight: 600,
        }}>{label}</span>
      )}
    </div>
  );
};
```

## BlogImage

블로그/소스 이미지를 씬에 삽입하는 컴포넌트. Ken Burns 효과(줌, 패닝), 슬라이드, 플로팅 등 다양한 애니메이션을 지원.

`public/images/` 디렉토리에 이미지를 배치하고 `staticFile()`로 참조한다.

```tsx
import React from "react";
import { Img, interpolate, useCurrentFrame, useVideoConfig, staticFile } from "remotion";

// animation types:
//   "zoom-in"    - 서서히 확대 (기본값, 정적 다이어그램에 적합)
//   "zoom-out"   - 확대 상태에서 축소 (설정 화면 등)
//   "pan-right"  - 좌→우 패닝 (아키텍처 다이어그램 등 가로가 긴 이미지)
//   "pan-left"   - 우→좌 패닝
//   "pan-up"     - 하→상 패닝 (세로가 긴 이미지, 타임라인 등)
//   "float"      - 부드러운 상하 플로팅 (알림, 채팅 스크린샷)
//   "slide-up"   - 아래에서 슬라이드 진입 (콘솔 화면)
//   "slide-left" - 왼쪽에서 슬라이드 진입 (좌측 패널)
//   "slide-right"- 오른쪽에서 슬라이드 진입 (우측 패널)
export const BlogImage: React.FC<{
  src: string;
  delay?: number;
  width?: number | string;
  height?: number | string;
  animation?: "zoom-in" | "zoom-out" | "pan-right" | "pan-left" | "pan-up" | "float" | "slide-up" | "slide-left" | "slide-right";
  style?: React.CSSProperties;
}> = ({ src, delay = 0.3, width = "100%", height, animation = "zoom-in", style }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // fade-in entrance
  const fadeIn = interpolate(frame, [delay * fps, (delay + 0.4) * fps], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  // continuous animation progress (0 → 1 over entire scene)
  const t = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  // entrance transform
  let entranceTransform = "";
  switch (animation) {
    case "slide-up":
      entranceTransform = `translateY(${interpolate(fadeIn, [0, 1], [60, 0])}px)`;
      break;
    case "slide-left":
      entranceTransform = `translateX(${interpolate(fadeIn, [0, 1], [80, 0])}px)`;
      break;
    case "slide-right":
      entranceTransform = `translateX(${interpolate(fadeIn, [0, 1], [-80, 0])}px)`;
      break;
    default:
      entranceTransform = `scale(${interpolate(fadeIn, [0, 1], [0.92, 1])})`;
  }

  // continuous Ken Burns / float transforms on the inner image
  let imgTransform = "";
  switch (animation) {
    case "zoom-in":
      imgTransform = `scale(${interpolate(t, [0, 1], [1, 1.08])})`;
      break;
    case "zoom-out":
      imgTransform = `scale(${interpolate(t, [0, 1], [1.1, 1])})`;
      break;
    case "pan-right":
      imgTransform = `scale(1.08) translateX(${interpolate(t, [0, 1], [-15, 15])}px)`;
      break;
    case "pan-left":
      imgTransform = `scale(1.08) translateX(${interpolate(t, [0, 1], [15, -15])}px)`;
      break;
    case "pan-up":
      imgTransform = `scale(1.08) translateY(${interpolate(t, [0, 1], [12, -12])}px)`;
      break;
    case "float":
      imgTransform = `scale(1.02) translateY(${Math.sin(t * Math.PI * 2) * 6}px)`;
      break;
    case "slide-up":
    case "slide-left":
    case "slide-right":
      imgTransform = `scale(${interpolate(t, [0, 1], [1, 1.04])})`;
      break;
  }

  // glow pulse
  const glowOpacity = 0.3 + Math.sin(t * Math.PI * 3) * 0.15;

  return (
    <div style={{
      opacity: fadeIn,
      transform: entranceTransform,
      borderRadius: 14,
      overflow: "hidden",
      boxShadow: `0 8px 32px rgba(0,0,0,0.4), 0 0 ${20 + glowOpacity * 20}px rgba(99,102,241,${glowOpacity}), 0 0 0 1px rgba(255,255,255,0.1)`,
      ...style,
    }}>
      <Img
        src={staticFile(`images/${src}`)}
        style={{
          width, height, objectFit: "contain", display: "block",
          transform: imgTransform,
          transformOrigin: "center center",
        }}
      />
    </div>
  );
};
```

### BlogImage 사용 예시
```tsx
// 아키텍처 다이어그램 - 좌→우 패닝
<BlogImage src="architecture.jpg" delay={0.3} width={880} animation="pan-right" />

// 콘솔 스크린샷 - 아래에서 슬라이드 진입
<BlogImage src="console.jpg" delay={0.3} width={820} animation="slide-up" />

// Slack 알림 - 부드러운 플로팅
<BlogImage src="slack-alert.jpg" delay={0.3} width={750} animation="float" />

// 나란히 배치 (좌/우 슬라이드)
<div style={{ display: "flex", gap: 24 }}>
  <BlogImage src="left-panel.jpg" delay={0.2} width={430} animation="slide-left" />
  <BlogImage src="right-panel.jpg" delay={0.5} width={430} animation="slide-right" />
</div>

// 세로 긴 이미지 - 하→상 패닝
<BlogImage src="timeline.jpg" delay={0.3} height={520} animation="pan-up" />
```

### 이미지-씬 매핑 가이드
이미지 내용에 따라 적합한 애니메이션을 선택:
| 이미지 유형 | 추천 animation | 이유 |
|------------|---------------|------|
| 아키텍처 다이어그램 | pan-right | 가로로 넓은 구조를 훑듯이 |
| 콘솔/설정 화면 | slide-up, zoom-out | 화면이 등장하는 느낌 |
| 코드 diff / 로그 | pan-left, pan-up | 코드를 읽는 방향으로 |
| 채팅/알림 | float | 메시지가 떠있는 느낌 |
| 분석 결과 | zoom-in | 점점 집중하는 느낌 |
| 좌우 비교 | slide-left + slide-right | 양쪽에서 진입 |
| 세로 긴 화면 | pan-up | 스크롤하듯 위로 이동 |

---

## SceneWithFade

씬 전환 crossfade 래퍼. 8프레임 fade in/out.

```tsx
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const SceneWithFade: React.FC<{
  children: React.ReactNode;
  durationInFrames: number;
  isFirst?: boolean;
  isLast?: boolean;
}> = ({ children, durationInFrames, isFirst = false, isLast = false }) => {
  const frame = useCurrentFrame();
  const FADE = 8;

  let opacity = 1;
  if (!isFirst) {
    opacity = Math.min(opacity, interpolate(frame, [0, FADE], [0, 1], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp",
    }));
  }
  if (!isLast) {
    opacity = Math.min(opacity, interpolate(frame, [durationInFrames - FADE, durationInFrames], [1, 0], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp",
    }));
  }

  return <AbsoluteFill style={{ opacity }}>{children}</AbsoluteFill>;
};
```

## 씬 전환 다양화 — Scene Transition Variety

@remotion/transitions 라이브러리가 설치되어 있다. 기본 crossfade(SceneWithFade) 외에 다양한 전환을 적용할 수 있다.

### TransitionSeries 패턴 (기본 Sequence 대체)

MainVideo에서 기존 `<Sequence>` 대신 `<TransitionSeries>`를 사용하면 씬 간 전환 효과를 자동 적용할 수 있다.

```tsx
import { TransitionSeries, linearTiming, springTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import { flip } from "@remotion/transitions/flip";
import { clockWipe } from "@remotion/transitions/clock-wipe";

// 씬 카테고리별 전환 효과 매핑
const getTransition = (fromCategory: string, toCategory: string, index: number) => {
  // intro → 본문: slide로 시작
  if (fromCategory === 'intro' && toCategory !== 'intro')
    return { effect: slide({ direction: 'from-right' }), timing: springTiming({ config: { damping: 12 } }) };
  // 본문 → outro: wipe로 마무리
  if (toCategory === 'outro')
    return { effect: wipe({ direction: 'from-left' }), timing: linearTiming({ durationInFrames: 15 }) };
  // 같은 카테고리 내: fade (기본, 안정적)
  if (fromCategory === toCategory)
    return { effect: fade(), timing: linearTiming({ durationInFrames: 8 }) };
  // 카테고리 전환: 교차 사용
  const effects = [
    { effect: slide({ direction: 'from-bottom' }), timing: springTiming({ config: { damping: 14 } }) },
    { effect: wipe({ direction: 'from-right' }), timing: linearTiming({ durationInFrames: 12 }) },
    { effect: fade(), timing: linearTiming({ durationInFrames: 10 }) },
    { effect: slide({ direction: 'from-right' }), timing: springTiming({ config: { damping: 12 } }) },
  ];
  return effects[index % effects.length];
};
```

### MainVideo with TransitionSeries

```tsx
export const MainVideo: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <TransitionSeries>
        {scenes.map((scene, i) => {
          const durationFrames = Math.round(scene.durationSec * fps);
          return (
            <React.Fragment key={scene.id}>
              <TransitionSeries.Sequence durationInFrames={durationFrames}>
                <IPadTemplate>
                  <SceneVisual scene={scene} />
                </IPadTemplate>
                <Mascot size={260} />
                <TimedSubtitle narration={scene.narration} durationInFrames={durationFrames} />
                <Audio src={staticFile(`audio/seg_${String(scene.id).padStart(2, '0')}.wav`)} />
              </TransitionSeries.Sequence>
              {i < scenes.length - 1 && (() => {
                const { effect, timing } = getTransition(scene.category, scenes[i+1].category, i);
                return <TransitionSeries.Transition presentation={effect} timing={timing} />;
              })()}
            </React.Fragment>
          );
        })}
      </TransitionSeries>
      <Audio src={staticFile("audio/bgm.mp3")} volume={0.1} />
    </AbsoluteFill>
  );
};
```

### 전환 효과 선택 가이드

| 전환 | 느낌 | 추천 상황 |
|------|------|---------|
| `fade()` | 부드럽고 안정적 | 같은 주제 내 씬 전환, 기본값 |
| `slide({direction})` | 역동적, 방향성 | 새 주제 시작, intro→본문 |
| `wipe({direction})` | 깔끔한 교체 | 카테고리 전환, 비교 씬 |
| `flip({direction})` | 극적, 주의 집중 | 반전, 결론 강조 |
| `clockWipe()` | 시계 방향 회전 | 시간 흐름, 타임라인 씬 |

### 전환 타이밍 옵션

```tsx
// 부드러운 선형 (추천: fade, wipe)
linearTiming({ durationInFrames: 10 })

// 물리 기반 스프링 (추천: slide, flip)
springTiming({ config: { damping: 12, stiffness: 100, mass: 0.8 } })
```

> **규칙**: 전환 효과를 과도하게 혼합하면 산만해진다. 카테고리 전환 시에만 다른 효과를 쓰고, 같은 카테고리 내에서는 fade를 기본으로 유지한다.

## Animation Utils

자주 쓰이는 애니메이션 헬퍼 패턴들.

### BigTitle - 큰 제목 텍스트
```tsx
const BigTitle: React.FC<{text: string; fontSize?: number}> = ({text, fontSize = 68}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = interpolate(frame, [0, 0.5 * fps], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  return (
    <div style={{
      fontSize, fontFamily: "'CookieRun', sans-serif", fontWeight: 800,
      color: "#f1f5f9", textAlign: "center",
      opacity: progress,
      transform: `translateY(${interpolate(progress, [0, 1], [30, 0])}px)`,
      textShadow: "0 4px 20px rgba(0,0,0,0.5)",
    }}>{text}</div>
  );
};
```

### StepBadge - 단계 뱃지 (spring 바운스)
```tsx
const StepBadge: React.FC<{step: string; color?: string}> = ({step, color = "#34d399"}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({
    frame,
    fps,
    config: { damping: 10, stiffness: 150, mass: 0.5 },
  });
  return (
    <div style={{
      background: `linear-gradient(135deg, ${color}, ${color}88)`,
      borderRadius: 16, padding: "10px 28px",
      transform: `scale(${scale})`,
      fontSize: 24, fontWeight: 700, color: "#0d1117",
      fontFamily: "'CookieRun', sans-serif", display: "inline-block",
    }}>{step}</div>
  );
};
```

### NumberedBadge — 번호 원 + 라벨 배지
StepBadge와 같은 자리에 쓰지만 앞에 **번호 원(circle)** 이 붙은 버전. 축 ①·②·③ / 단계 1·2·3 같이 **순서**가 중요한 씬에서 사용. 컬러는 씬별로 다르게 지정 (인디고 / 라임 / 핑크 등 대비).

```tsx
const NumberedBadge: React.FC<{ number: string; label: string; color: string }> = ({
  number, label, color,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 10, stiffness: 150, mass: 0.5 } });
  return (
    <div style={{
      display: "inline-flex", alignItems: "center", gap: 12,
      background: `linear-gradient(135deg, ${color}, ${color}88)`,
      borderRadius: 16, padding: "10px 28px",
      transform: `scale(${s})`, color: "#0d1117",
      fontFamily: "'CookieRun', sans-serif", fontSize: 22, fontWeight: 700,
    }}>
      <div style={{
        width: 28, height: 28, borderRadius: "50%",
        background: "rgba(255,255,255,0.35)", color: "#fff",
        display: "flex", alignItems: "center", justifyContent: "center",
        fontWeight: 900, fontSize: 18,
      }}>{number}</div>
      <span>{label}</span>
    </div>
  );
};
```

**사용 예**: 비교형 3연속 씬(축 1: 타이밍, 축 2: 저장, 축 3: 규모)에서 각 씬 badge에 번호를 부여하여 시청자의 "지금 몇 번째 축인지" 인지 부담을 덜어준다.

### EmphasisPill — 한 줄 강조 알약
"공통 본질은 X" / "핵심은 Y" 류의 결론 한 줄을 강조할 때 사용. 알약(pill) 모양 + 그라디언트 배경 + 아이콘 옵션. 씬 전체가 이 한 줄만 보여주는 짧은 전환 씬(8~12초)에 적합.

```tsx
const EmphasisPill: React.FC<{ text: string; icon?: string; color?: string }> = ({
  text, icon, color = "#a78bfa",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 12, stiffness: 120, mass: 0.6 } });
  return (
    <div style={{
      display: "inline-flex", alignItems: "center", gap: 16,
      background: `linear-gradient(135deg, ${color}22, ${color}08)`,
      border: `2.5px solid ${color}`,
      borderRadius: 999, padding: "18px 40px",
      transform: `scale(${s})`,
      boxShadow: `0 8px 32px ${color}33`,
      fontSize: 40, fontWeight: 800, color: "#1e293b",
      fontFamily: "'CookieRun', sans-serif",
    }}>
      {icon && <span style={{ fontSize: 48 }}>{icon}</span>}
      <span>{text}</span>
    </div>
  );
};
```

**언제 쓰나**: 섹션 브리지, 요약 결론, 공통 원칙 선언. 주위에 다른 텍스트 요소 없이 단독 배치하여 시선 집중.

### ListItems - 목록 아이템 (spring 입장 + 하이라이트 스캔)
입장 후 시간 흐름에 따라 현재 항목이 순서대로 초록 하이라이트됨.
```tsx
const ListItems: React.FC<{ items: string[]; icon?: string }> = ({ items, icon = "check" }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // 모든 아이템 입장 완료 후 시작되는 하이라이트 스캔
  const allInDelay = 0.3 + items.length * 0.3 + 0.4;
  const scanStartFrame = allInDelay * fps;
  const scanDuration = durationInFrames - scanStartFrame;
  const cycleFrames = scanDuration > 0 ? scanDuration / items.length : fps;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
      {items.map((item, i) => {
        const delay = 0.3 + i * 0.3;
        // spring 바운스 입장
        const springVal = spring({
          frame: frame - Math.round(delay * fps),
          fps,
          config: { damping: 12, stiffness: 100, mass: 0.7 },
        });
        const opacity = interpolate(frame, [delay * fps, (delay + 0.3) * fps], [0, 1], {
          extrapolateLeft: "clamp", extrapolateRight: "clamp",
        });

        // 하이라이트 스캔: 시간에 따라 순서대로 활성화
        const isScanning = frame >= scanStartFrame;
        const activeIndex = isScanning
          ? Math.floor(((frame - scanStartFrame) % (cycleFrames * items.length)) / cycleFrames)
          : -1;
        const isActive = activeIndex === i;
        const highlightGlow = isActive ? 0.6 + Math.sin((frame / fps) * 6) * 0.3 : 0;

        return (
          <div key={i} style={{
            display: "flex", alignItems: "center", gap: 16,
            opacity,
            transform: `translateX(${interpolate(springVal, [0, 1], [-30, 0])}px) scale(${isActive ? 1.03 : 1})`,
            background: isActive ? "rgba(52, 211, 153, 0.08)" : "transparent",
            borderRadius: 12, padding: "6px 12px", margin: "-6px -12px",
            boxShadow: isActive ? `inset 0 0 20px rgba(52,211,153,${highlightGlow * 0.15}), 0 0 12px rgba(52,211,153,${highlightGlow * 0.1})` : "none",
          }}>
            <IconElement name={icon} size={44} delay={delay} glow={false} />
            <span style={{
              fontSize: 28, color: isActive ? "#34d399" : "#e2e8f0",
              fontFamily: "'CookieRun', sans-serif", fontWeight: isActive ? 700 : 500,
            }}>{item}</span>
          </div>
        );
      })}
    </div>
  );
};
```

### PipelineFlow - 파이프라인 흐름 (spring 입장 + 순차 펄스)
단계들이 순서대로 빛나며 데이터 흐름을 시각화.
```tsx
const PipelineFlow: React.FC<{ steps: string[] }> = ({ steps }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // 입장 완료 후 순차 펄스 효과
  const allInTime = 0.2 + steps.length * 0.25 + 0.3;
  const pulseStartFrame = allInTime * fps;
  const pulseCycle = fps * 0.6;

  return (
    <div style={{ display: "flex", alignItems: "center", gap: 12, flexWrap: "wrap", justifyContent: "center" }}>
      {steps.map((step, i) => {
        const delay = 0.2 + i * 0.25;
        const springVal = spring({
          frame: frame - Math.round(delay * fps),
          fps,
          config: { damping: 11, stiffness: 130, mass: 0.6 },
        });
        const opacity = interpolate(frame, [delay * fps, (delay + 0.25) * fps], [0, 1], {
          extrapolateLeft: "clamp", extrapolateRight: "clamp",
        });

        // 순차 펄스: 입장 완료 후 순서대로 빛남
        const isPulsing = frame >= pulseStartFrame;
        const pulseIndex = isPulsing
          ? Math.floor(((frame - pulseStartFrame) % (pulseCycle * steps.length)) / pulseCycle)
          : -1;
        const isLit = pulseIndex === i;

        return (
          <React.Fragment key={i}>
            <div style={{
              background: isLit ? "rgba(52,211,153,0.15)" : "rgba(255,255,255,0.07)",
              borderRadius: 12, padding: "12px 20px",
              border: `1px solid ${isLit ? "rgba(52,211,153,0.4)" : "rgba(255,255,255,0.1)"}`,
              opacity,
              transform: `scale(${interpolate(springVal, [0, 1], [0.8, 1])})`,
              boxShadow: isLit ? "0 0 16px rgba(52,211,153,0.2)" : "none",
            }}>
              <span style={{ fontSize: 20, color: isLit ? "#34d399" : "#e2e8f0", fontFamily: "'CookieRun', sans-serif", fontWeight: isLit ? 700 : 500 }}>{step}</span>
            </div>
            {i < steps.length - 1 && (
              <span style={{
                fontSize: 24, opacity,
                color: pulseIndex === i ? "#34d399" : "rgba(52,211,153,0.5)",
                transform: `translateX(${pulseIndex === i ? 3 : 0}px)`,
              }}>→</span>
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
};
```

### 폰트 설정 (index.ts)

로컬 CookieRun 폰트를 `@font-face`로 로드한다. `public/fonts/`에 복사된 otf 파일을 `staticFile()`로 참조.
코드용 JetBrainsMono는 Google Fonts에서 로드.

```tsx
import { staticFile } from "remotion";
import { loadFont as loadJetBrains } from "@remotion/google-fonts/JetBrainsMono";

// CookieRun 로컬 폰트 로드
const cookieRunFaces = [
  { weight: "400", file: "CookieRun Regular.otf" },
  { weight: "700", file: "CookieRun Bold.otf" },
  { weight: "900", file: "CookieRun Black.otf" },
];

for (const face of cookieRunFaces) {
  const fontFace = new FontFace("CookieRun", `url(${staticFile(`fonts/${face.file}`)})`, {
    weight: face.weight,
    style: "normal",
  });
  fontFace.load().then((loaded) => {
    document.fonts.add(loaded);
  });
}

// 코드용 폰트
loadJetBrains("normal", { weights: ["400", "700"] });
```

---

## 고급 모션 패턴

기본 컴포넌트(spring 바운스 + interpolate)를 넘어서는 고급 애니메이션 패턴들.
`Easing`, SVG 애니메이션, 결정적 파티클, 모핑 등을 활용한다.

---

### WordByWordText — 단어별 순차 등장

단어 단위로 분리하여 시차(stagger) 진입. blur→clear 전환 + 글로우 효과.
자막이나 제목에 역동적인 느낌을 줄 때 사용.

```tsx
import React from "react";
import { spring, useCurrentFrame, useVideoConfig, interpolate } from "remotion";

export const WordByWordText: React.FC<{
  text: string;
  fontSize?: number;
  color?: string;
  delay?: number;         // 프레임 단위 시작 딜레이
  staggerFrames?: number; // 단어 간 간격 (프레임)
}> = ({ text, fontSize = 64, color = "#e2e8f0", delay = 0, staggerFrames = 5 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = text.split(" ");

  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 16, justifyContent: "center" }}>
      {words.map((word, i) => {
        const wordDelay = delay + i * staggerFrames;
        const prog = spring({
          frame: frame - wordDelay,
          fps,
          config: { damping: 12, stiffness: 200, mass: 0.5 },
        });
        const blur = interpolate(prog, [0, 0.5, 1], [8, 2, 0]);
        const y = interpolate(prog, [0, 1], [40, 0]);

        return (
          <span
            key={i}
            style={{
              fontSize,
              fontWeight: 900,
              color,
              opacity: prog,
              transform: `translateY(${y}px)`,
              filter: `blur(${blur}px)`,
              display: "inline-block",
              textShadow: `0 0 ${30 * prog}px rgba(99,102,241,${0.5 * prog})`,
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};
```

**사용 예시:**
```tsx
// 인트로 타이틀
<WordByWordText text="AI 에이전트의 미래" fontSize={72} delay={10} staggerFrames={4} />

// 소제목 (작고 빠르게)
<WordByWordText text="첫 번째 단계" fontSize={48} delay={5} staggerFrames={3} color="#34d399" />
```

---

### SVGPathDraw — 경로 드로잉 애니메이션

SVG `strokeDashoffset`을 이용하여 선이 그려지는 효과. 플로우차트, 파이프라인 시각화에 적합.
노드가 순차적으로 팝업되며 펄스 링 효과 동반.

```tsx
import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";

export const SVGPathDraw: React.FC<{
  delay?: number;
  nodes?: Array<{ cx: number; cy: number; label: string }>;
  pathD?: string;
  pathLength?: number;
  colors?: string[];
}> = ({
  delay = 0,
  nodes = [
    { cx: 200, cy: 300, label: "Script" },
    { cx: 560, cy: 180, label: "Scene" },
    { cx: 920, cy: 300, label: "Assets" },
    { cx: 1280, cy: 180, label: "Render" },
    { cx: 1640, cy: 300, label: "Output" },
  ],
  pathD = "M 200,300 C 380,100 380,100 560,180 C 740,260 740,260 920,300 C 1100,340 1100,100 1280,180 C 1460,260 1460,340 1640,300",
  pathLength = 2000,
  colors = ["#6366f1", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981"],
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = Math.max(0, frame - delay * fps);

  const drawProgress = interpolate(t, [0, 60], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  const glowOpacity = interpolate(t, [0, 30, 60], [0, 0.8, 0.4], {
    extrapolateRight: "clamp",
  });

  return (
    <svg viewBox="0 0 1920 500" width="100%" height="100%">
      <defs>
        <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
          <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.03)" strokeWidth="1" />
        </pattern>
        <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#6366f1" />
          <stop offset="50%" stopColor="#ec4899" />
          <stop offset="100%" stopColor="#10b981" />
        </linearGradient>
        <filter id="glow">
          <feGaussianBlur stdDeviation="6" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <rect width="1920" height="500" fill="url(#grid)" />

      {/* 글로우 레이어 */}
      <path
        d={pathD}
        fill="none"
        stroke="url(#lineGrad)"
        strokeWidth="8"
        strokeLinecap="round"
        strokeDasharray={pathLength}
        strokeDashoffset={pathLength * (1 - drawProgress)}
        opacity={glowOpacity}
        filter="url(#glow)"
      />
      {/* 메인 경로 */}
      <path
        d={pathD}
        fill="none"
        stroke="url(#lineGrad)"
        strokeWidth="3"
        strokeLinecap="round"
        strokeDasharray={pathLength}
        strokeDashoffset={pathLength * (1 - drawProgress)}
      />

      {/* 노드들 — 순차 팝업 + 펄스 링 */}
      {nodes.map((node, i) => {
        const nodeDelay = 15 + i * 12;
        const nodeProgress = interpolate(t, [nodeDelay, nodeDelay + 15], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: Easing.out(Easing.back(1.7)),
        });
        const ringPulse = Math.sin((t - nodeDelay) * 0.15) * 3 + 3;
        const color = colors[i % colors.length];

        return (
          <g key={i} opacity={nodeProgress}>
            <circle cx={node.cx} cy={node.cy} r={28 + ringPulse}
              fill="none" stroke={color} strokeWidth="1.5" opacity={0.4} />
            <circle cx={node.cx} cy={node.cy} r={24 * nodeProgress}
              fill={`${color}33`} stroke={color} strokeWidth="2" />
            <circle cx={node.cx} cy={node.cy} r={6 * nodeProgress} fill={color} />
            <text x={node.cx} y={node.cy + 55} textAnchor="middle"
              fill="#e2e8f0" fontSize="22" fontFamily="system-ui, sans-serif" fontWeight="600"
              opacity={nodeProgress}>
              {node.label}
            </text>
          </g>
        );
      })}
    </svg>
  );
};
```

**사용 예시:**
```tsx
// 기본 5단계 파이프라인
<SVGPathDraw delay={0.3} />

// 커스텀 노드 (3단계)
<SVGPathDraw
  delay={0.5}
  nodes={[
    { cx: 400, cy: 250, label: "입력" },
    { cx: 960, cy: 250, label: "처리" },
    { cx: 1520, cy: 250, label: "출력" },
  ]}
  pathD="M 400,250 C 680,100 680,400 960,250 C 1240,100 1240,400 1520,250"
  pathLength={1500}
/>
```

---

### CountUpNumber — 숫자 카운트업

0에서 목표 수치까지 카운트업. 도착 시 바운스 + 글로우 강조.
통계, KPI, 성과 지표 씬에 사용.

```tsx
import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";

export const CountUpNumber: React.FC<{
  from?: number;
  to: number;
  suffix?: string;
  prefix?: string;
  label: string;
  delay?: number;
  color?: string;
}> = ({ from = 0, to, suffix = "", prefix = "", label, delay = 0, color = "#6366f1" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = Math.max(0, frame - delay * fps);

  const progress = interpolate(t, [0, 45], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  const value = Math.round(from + (to - from) * progress);
  const glowIntensity = interpolate(progress, [0.8, 1], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // 도착 시 감쇠 바운스
  const bounceScale =
    progress >= 0.95
      ? 1 + Math.sin((t - 40) * 0.5) * 0.03 * Math.max(0, 1 - (t - 45) * 0.02)
      : interpolate(progress, [0, 1], [0.8, 1]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 8,
        transform: `scale(${bounceScale})`,
      }}
    >
      <div
        style={{
          fontSize: 96,
          fontWeight: 900,
          color,
          fontFamily: "'CookieRun', sans-serif",
          textShadow: `0 0 ${40 * glowIntensity}px ${color}88, 0 0 ${80 * glowIntensity}px ${color}44`,
          letterSpacing: "-0.04em",
        }}
      >
        {prefix}
        {value.toLocaleString()}
        {suffix}
      </div>
      <div
        style={{
          fontSize: 28,
          color: "rgba(226, 232, 240, 0.7)",
          fontFamily: "'CookieRun', sans-serif",
          fontWeight: 500,
          opacity: interpolate(t, [20, 35], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        }}
      >
        {label}
      </div>
    </div>
  );
};
```

**사용 예시:**
```tsx
<div style={{ display: "flex", gap: 100, justifyContent: "center" }}>
  <CountUpNumber to={2847} label="구독자" color="#6366f1" delay={0.3} />
  <CountUpNumber to={98} suffix="%" label="완성도" color="#10b981" delay={0.6} />
  <CountUpNumber to={156} prefix="+" label="새 기능" color="#ec4899" delay={0.9} />
</div>
```

---

### ProgressRing — 원형 프로그레스 링

SVG 원형 게이지가 채워지는 애니메이션. 스코어, 달성률, 성능 지표에 적합.
spring 진입 + Easing.out(cubic) 프로그레스 + 글로우 트랙.

```tsx
import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, Easing, spring } from "remotion";

export const ProgressRing: React.FC<{
  percentage: number;
  label: string;
  color?: string;
  size?: number;
  delay?: number;
}> = ({ percentage, label, color = "#6366f1", size = 200, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = Math.max(0, frame - delay * fps);

  const radius = size * 0.4;
  const circumference = 2 * Math.PI * radius;
  const strokeWidth = size * 0.08;

  const progress = interpolate(t, [0, 50], [0, percentage / 100], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  const dashOffset = circumference * (1 - progress);

  const enterScale = spring({
    frame: Math.round(t),
    fps,
    config: { damping: 12, stiffness: 100, mass: 0.8 },
  });

  const displayNum = Math.round(progress * 100);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 16,
        transform: `scale(${enterScale})`,
        opacity: interpolate(t, [0, 10], [0, 1], { extrapolateRight: "clamp" }),
      }}
    >
      <div style={{ position: "relative", width: size, height: size }}>
        <svg viewBox={`0 0 ${size} ${size}`} width={size} height={size} style={{ transform: "rotate(-90deg)" }}>
          {/* 배경 트랙 */}
          <circle cx={size / 2} cy={size / 2} r={radius} fill="none"
            stroke="rgba(255,255,255,0.08)" strokeWidth={strokeWidth} />
          {/* 글로우 */}
          <circle cx={size / 2} cy={size / 2} r={radius} fill="none"
            stroke={color} strokeWidth={strokeWidth + 8}
            strokeDasharray={circumference} strokeDashoffset={dashOffset}
            strokeLinecap="round" opacity={0.15} style={{ filter: "blur(8px)" }} />
          {/* 메인 프로그레스 */}
          <circle cx={size / 2} cy={size / 2} r={radius} fill="none"
            stroke={color} strokeWidth={strokeWidth}
            strokeDasharray={circumference} strokeDashoffset={dashOffset}
            strokeLinecap="round" />
        </svg>
        {/* 중앙 숫자 */}
        <div style={{
          position: "absolute", inset: 0,
          display: "flex", alignItems: "center", justifyContent: "center",
        }}>
          <span style={{
            fontSize: size * 0.28, fontWeight: 900, color,
            fontFamily: "'CookieRun', sans-serif", letterSpacing: "-0.04em",
          }}>
            {displayNum}%
          </span>
        </div>
      </div>
      <div style={{
        fontSize: 22, color: "rgba(226,232,240,0.7)",
        fontFamily: "'CookieRun', sans-serif", fontWeight: 500,
      }}>
        {label}
      </div>
    </div>
  );
};
```

**사용 예시:**
```tsx
<div style={{ display: "flex", gap: 80, justifyContent: "center" }}>
  <ProgressRing percentage={92} label="Performance" color="#6366f1" size={220} delay={0.2} />
  <ProgressRing percentage={78} label="Quality" color="#10b981" size={220} delay={0.5} />
  <ProgressRing percentage={95} label="Speed" color="#ec4899" size={220} delay={0.8} />
</div>
```

---

### MorphingShape — 형태 변환 도형

원→별→다이아→하트로 순환하는 도형 모핑. 회전 + 스케일 조합으로 시각적 전환 효과.
추상적 비주얼, 브랜딩 씬에 사용.

```tsx
import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";

export const MorphingShape: React.FC<{
  delay?: number;
  cycleDuration?: number; // 전체 사이클 초 (기본 8초)
}> = ({ delay = 0, cycleDuration = 8 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = Math.max(0, frame - delay * fps);
  const cycle = (t / fps) % cycleDuration;

  const shapes = [
    // 원
    "M 300,150 C 300,67 367,0 450,0 C 533,0 600,67 600,150 C 600,233 533,300 450,300 C 367,300 300,233 300,150 Z",
    // 별
    "M 450,0 L 518,114 L 647,114 L 543,186 L 580,300 L 450,228 L 320,300 L 357,186 L 253,114 L 382,114 Z",
    // 다이아몬드
    "M 450,0 L 600,150 L 450,300 L 300,150 Z",
    // 하트
    "M 450,80 C 450,80 350,0 275,0 C 175,0 150,80 150,130 C 150,280 450,300 450,300 C 450,300 750,280 750,130 C 750,80 725,0 625,0 C 550,0 450,80 450,80 Z",
  ];

  const stepDuration = cycleDuration / shapes.length;
  const shapeIndex = Math.floor(cycle / stepDuration);
  const nextIndex = (shapeIndex + 1) % shapes.length;
  const morphProgress = interpolate(cycle % stepDuration, [0, 0.3, stepDuration - 0.3, stepDuration], [0, 0, 1, 1], {
    extrapolateRight: "clamp",
  });

  const colors = ["#6366f1", "#ec4899", "#10b981", "#f59e0b"];
  const currentColor = colors[shapeIndex];
  const nextColor = colors[nextIndex];

  const rotation = interpolate(morphProgress, [0, 1], [0, 90]);
  const scale = interpolate(morphProgress, [0, 0.5, 1], [1, 0.85, 1], {
    easing: Easing.inOut(Easing.ease),
  });
  const pulseScale = 1 + Math.sin(t * 0.1) * 0.02;

  const activeShape = morphProgress < 0.5 ? shapes[shapeIndex] : shapes[nextIndex];
  const activeColor = morphProgress < 0.5 ? currentColor : nextColor;
  const activeLabel = ["Circle", "Star", "Diamond", "Heart"][morphProgress < 0.5 ? shapeIndex : nextIndex];

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 20 }}>
      <svg viewBox="100 -50 700 400" width="400" height="300"
        style={{ transform: `scale(${scale * pulseScale}) rotate(${rotation}deg)` }}>
        <defs>
          <filter id="morphGlow">
            <feGaussianBlur stdDeviation="10" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        <path d={activeShape} fill={activeColor} opacity={0.3} filter="url(#morphGlow)" />
        <path d={activeShape} fill="none" stroke={activeColor} strokeWidth="3"
          opacity={interpolate(Math.abs(morphProgress - 0.5), [0, 0.5], [0.3, 1])} />
        <path d={activeShape} fill={`${activeColor}22`}
          opacity={interpolate(Math.abs(morphProgress - 0.5), [0, 0.5], [0.3, 1])} />
      </svg>
      <div style={{
        fontSize: 24, color: "rgba(226,232,240,0.6)",
        fontFamily: "'CookieRun', sans-serif", fontWeight: 500,
      }}>
        {activeLabel}
      </div>
    </div>
  );
};
```

---

### ParticleConfetti — 결정적 파티클 시스템

Remotion의 `random()` (시드 기반)으로 재현 가능한 파티클 폭발 효과.
인트로, 아웃트로, 축하/완료 씬에 사용. 중력 시뮬레이션 포함.

```tsx
import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, random } from "remotion";

export const ParticleConfetti: React.FC<{
  count?: number;
  delay?: number;
  originX?: number;
  originY?: number;
  colors?: string[];
}> = ({
  count = 60,
  delay = 0,
  originX = 960,
  originY = 400,
  colors = ["#6366f1", "#ec4899", "#10b981", "#f59e0b", "#3b82f6", "#8b5cf6"],
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = Math.max(0, frame - delay * fps);

  const particles = Array.from({ length: count }, (_, i) => {
    const seed = `particle-${i}`;
    const angle = random(seed + "-angle") * Math.PI * 2;
    const speed = 200 + random(seed + "-speed") * 400;
    const rotSpeed = (random(seed + "-rot") - 0.5) * 720;
    const size = 6 + random(seed + "-size") * 12;
    const colorIdx = Math.floor(random(seed + "-color") * colors.length);
    const shape = random(seed + "-shape") > 0.5 ? "circle" : "rect";
    const gravity = 300 + random(seed + "-grav") * 200;

    const elapsed = t / fps;
    const x = originX + Math.cos(angle) * speed * elapsed;
    const y = originY + Math.sin(angle) * speed * elapsed + 0.5 * gravity * elapsed * elapsed;
    const rotation = rotSpeed * elapsed;
    const opacity = interpolate(t, [0, 10, 50, 70], [0, 1, 1, 0], {
      extrapolateRight: "clamp",
      extrapolateLeft: "clamp",
    });
    const scale = interpolate(t, [0, 8], [0, 1], { extrapolateRight: "clamp" });

    return { x, y, rotation, opacity, scale, size, color: colors[colorIdx], shape };
  });

  return (
    <div style={{ position: "absolute", inset: 0, overflow: "hidden", pointerEvents: "none" }}>
      {particles.map((p, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: p.x,
            top: p.y,
            width: p.size,
            height: p.shape === "circle" ? p.size : p.size * 0.6,
            borderRadius: p.shape === "circle" ? "50%" : 2,
            background: p.color,
            opacity: p.opacity,
            transform: `rotate(${p.rotation}deg) scale(${p.scale})`,
            boxShadow: `0 0 6px ${p.color}66`,
          }}
        />
      ))}
    </div>
  );
};
```

**사용 예시:**
```tsx
// 화면 중앙 폭발
<ParticleConfetti count={80} originX={960} originY={540} />

// 오른쪽 하단에서 적은 파티클
<ParticleConfetti count={30} originX={1600} originY={800} delay={0.5}
  colors={["#10b981", "#34d399", "#6ee7b7"]} />
```

---

### 고급 모션 이징 가이드

기본 `spring()`과 `interpolate()`에 더해, `Easing` 모듈로 더 다양한 커브를 적용할 수 있다.

```tsx
import { Easing } from "remotion";

// 자주 쓰이는 이징 조합
const easings = {
  // 부드러운 감속 (카드/텍스트 진입에 적합)
  smoothDecel: Easing.out(Easing.cubic),

  // 오버슈트 (팝업, 뱃지에 bounce 느낌)
  overshoot: Easing.out(Easing.back(1.7)),

  // 탄성 (아이콘, 작은 요소)
  elastic: Easing.out(Easing.elastic(1)),

  // 부드러운 양방향 (모핑, 전환)
  smoothInOut: Easing.inOut(Easing.ease),

  // 빠른 시작 → 느린 끝 (프로그레스 바)
  expDecel: Easing.out(Easing.exp),

  // CSS ease 동일
  ease: Easing.bezier(0.25, 0.1, 0.25, 1.0),
};

// 사용 예시
interpolate(frame, [0, 30], [0, 1], {
  easing: Easing.out(Easing.back(1.7)),  // 살짝 오버슈트 후 정착
  extrapolateRight: "clamp",
});
```

| 이징 | 느낌 | 추천 용도 |
|------|------|----------|
| `Easing.out(Easing.cubic)` | 부드러운 감속 | 대부분의 진입 애니메이션 |
| `Easing.out(Easing.back(1.7))` | 약간 오버슈트 | 팝업, 뱃지, 강조 요소 |
| `Easing.out(Easing.elastic(1))` | 탄성 바운스 | 작은 아이콘, 도트 |
| `Easing.inOut(Easing.ease)` | 양방향 부드러움 | 모핑, 루프 전환 |
| `Easing.out(Easing.exp)` | 급 시작 → 완만 종료 | 프로그레스, 카운트업 |
| `Easing.bezier(...)` | CSS cubic-bezier 동일 | 커스텀 커브 |

---

## PPT 스타일 카드 패턴

IT 발표 슬라이드처럼 항목들을 카드로 배치하고 순차 애니메이션으로 보여주는 패턴들.

---

### StaggeredCards — 그리드 카드 순차 등장

N×M 그리드에 카드가 위치별 방향으로 순차 진입. 진입 후 순환 하이라이트 + 악센트 바 확장.
기능 소개, 특징 나열, 서비스 항목 씬에 사용.

```tsx
import React from "react";
import { spring, useCurrentFrame, useVideoConfig, interpolate } from "remotion";

export interface CardItem {
  icon: string;
  title: string;
  description: string;
  color?: string;
}

export const StaggeredCards: React.FC<{
  cards: CardItem[];
  columns?: number;
  delay?: number;
  staggerMs?: number;
}> = ({ cards, columns = 3, delay = 0, staggerMs = 0.2 }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const allInFrame = (delay + cards.length * staggerMs + 0.5) * fps;
  const highlightCycle = durationInFrames - allInFrame;
  const cyclePerCard = highlightCycle > 0 ? highlightCycle / cards.length : fps;

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: `repeat(${columns}, 1fr)`,
        gap: 24,
        width: "100%",
        maxWidth: columns * 340 + (columns - 1) * 24,
      }}
    >
      {cards.map((card, i) => {
        const cardDelay = delay + i * staggerMs;
        const prog = spring({
          frame: frame - Math.round(cardDelay * fps),
          fps,
          config: { damping: 14, stiffness: 120, mass: 0.7 },
        });
        const opacity = interpolate(
          frame,
          [cardDelay * fps, (cardDelay + 0.3) * fps],
          [0, 1],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
        );

        const row = Math.floor(i / columns);
        const col = i % columns;
        const slideX = interpolate(prog, [0, 1], [(col < columns / 2 ? -1 : 1) * 40, 0]);
        const slideY = interpolate(prog, [0, 1], [30 + row * 10, 0]);
        const scale = interpolate(prog, [0, 1], [0.85, 1]);

        const isPostEntry = frame >= allInFrame;
        const activeIdx = isPostEntry
          ? Math.floor(((frame - allInFrame) % (cyclePerCard * cards.length)) / cyclePerCard)
          : -1;
        const isActive = activeIdx === i;
        const accentColor = card.color || "#6366f1";
        const floatY = prog >= 0.95 ? Math.sin((frame / fps) * 1.5 + i * 0.8) * 2 : 0;

        return (
          <div
            key={i}
            style={{
              opacity,
              transform: `translate(${slideX}px, ${slideY + floatY}px) scale(${scale * (isActive ? 1.04 : 1)})`,
              background: isActive
                ? `linear-gradient(135deg, ${accentColor}15, ${accentColor}08)`
                : "rgba(255,255,255,0.04)",
              backdropFilter: "blur(16px)",
              borderRadius: 20,
              border: `1.5px solid ${isActive ? `${accentColor}66` : "rgba(255,255,255,0.08)"}`,
              padding: "32px 28px",
              display: "flex",
              flexDirection: "column" as const,
              gap: 14,
              boxShadow: isActive
                ? `0 8px 40px ${accentColor}22, 0 0 20px ${accentColor}11`
                : "0 4px 20px rgba(0,0,0,0.3)",
            }}
          >
            <div style={{ fontSize: 48 }}>{card.icon}</div>
            <div style={{
              fontSize: 26, fontWeight: 800,
              color: isActive ? accentColor : "#f1f5f9",
              fontFamily: "'CookieRun', sans-serif", letterSpacing: "-0.02em",
            }}>
              {card.title}
            </div>
            <div style={{
              fontSize: 18, color: "rgba(226,232,240,0.65)",
              fontFamily: "'CookieRun', sans-serif", lineHeight: 1.5,
            }}>
              {card.description}
            </div>
            <div style={{
              height: 3, borderRadius: 2, marginTop: "auto",
              background: isActive
                ? `linear-gradient(90deg, ${accentColor}, transparent)`
                : "rgba(255,255,255,0.06)",
              width: isActive ? "100%" : "40%",
            }} />
          </div>
        );
      })}
    </div>
  );
};
```

**사용 예시:**
```tsx
// 3열 6카드 (2x3)
<StaggeredCards
  columns={3}
  delay={0.4}
  staggerMs={0.2}
  cards={[
    { icon: "🚀", title: "빠른 배포", description: "CI/CD 자동 빌드 및 배포", color: "#6366f1" },
    { icon: "🛡️", title: "보안 강화", description: "제로트러스트 아키텍처 기반", color: "#10b981" },
    { icon: "📊", title: "모니터링", description: "핵심 지표 실시간 확인", color: "#f59e0b" },
    { icon: "🔄", title: "오토 스케일링", description: "트래픽 기반 자동 조절", color: "#ec4899" },
    { icon: "💾", title: "데이터 백업", description: "다중 리전 자동 백업", color: "#3b82f6" },
    { icon: "🤖", title: "AI 최적화", description: "ML 기반 리소스 최적화", color: "#8b5cf6" },
  ]}
/>

// 2열 4카드
<StaggeredCards columns={2} cards={[...]} />
```

---

### ComparisonCards — Before/After 비교

좌우에서 슬라이드 진입 + 항목 시차 등장 + 중앙 VS 뱃지 팝업.
변경 전후, 기술 비교, 플랜 비교 씬에 사용.

```tsx
import React from "react";
import { spring, useCurrentFrame, useVideoConfig, interpolate } from "remotion";

export const ComparisonCards: React.FC<{
  left: { title: string; items: string[]; icon: string; color?: string };
  right: { title: string; items: string[]; icon: string; color?: string };
  vsText?: string;
  delay?: number;
}> = ({ left, right, vsText = "VS", delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = Math.max(0, frame - delay * fps);

  const leftColor = left.color || "#ef4444";
  const rightColor = right.color || "#10b981";

  const leftProg = spring({
    frame: Math.round(t), fps,
    config: { damping: 14, stiffness: 100, mass: 0.8 },
  });
  const leftX = interpolate(leftProg, [0, 1], [-120, 0]);

  const rightProg = spring({
    frame: Math.round(t) - 8, fps,
    config: { damping: 14, stiffness: 100, mass: 0.8 },
  });
  const rightX = interpolate(rightProg, [0, 1], [120, 0]);

  const vsProg = spring({
    frame: Math.round(t) - 18, fps,
    config: { damping: 10, stiffness: 180, mass: 0.5 },
  });
  const vsPulse = 1 + Math.sin(t * 0.12) * 0.05;

  const renderItems = (items: string[], side: "left" | "right", color: string) => {
    const baseDelay = side === "left" ? 15 : 20;
    return items.map((item, i) => {
      const itemOpacity = interpolate(t, [baseDelay + i * 6, baseDelay + i * 6 + 10], [0, 1], {
        extrapolateLeft: "clamp", extrapolateRight: "clamp",
      });
      const itemX = interpolate(t, [baseDelay + i * 6, baseDelay + i * 6 + 10],
        [side === "left" ? -20 : 20, 0],
        { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
      );
      return (
        <div key={i} style={{
          opacity: itemOpacity, transform: `translateX(${itemX}px)`,
          display: "flex", alignItems: "center", gap: 12,
          padding: "10px 16px", borderRadius: 10,
          background: "rgba(255,255,255,0.03)",
          border: "1px solid rgba(255,255,255,0.06)",
        }}>
          <div style={{
            width: 8, height: 8, borderRadius: "50%",
            background: color, boxShadow: `0 0 8px ${color}66`, flexShrink: 0,
          }} />
          <span style={{ fontSize: 22, color: "#e2e8f0", fontFamily: "'CookieRun', sans-serif" }}>
            {item}
          </span>
        </div>
      );
    });
  };

  const cardStyle = (color: string): React.CSSProperties => ({
    flex: 1,
    background: `linear-gradient(135deg, ${color}0a, ${color}05)`,
    backdropFilter: "blur(16px)",
    borderRadius: 24,
    border: `1.5px solid ${color}33`,
    padding: "36px 32px",
    display: "flex",
    flexDirection: "column",
    gap: 20,
  });

  return (
    <div style={{ display: "flex", alignItems: "stretch", gap: 60, width: "100%", maxWidth: 1400 }}>
      <div style={{ ...cardStyle(leftColor), opacity: leftProg, transform: `translateX(${leftX}px)` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 8 }}>
          <span style={{ fontSize: 44 }}>{left.icon}</span>
          <span style={{ fontSize: 32, fontWeight: 800, color: leftColor, fontFamily: "'CookieRun', sans-serif" }}>
            {left.title}
          </span>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {renderItems(left.items, "left", leftColor)}
        </div>
      </div>

      <div style={{
        display: "flex", alignItems: "center", justifyContent: "center", alignSelf: "center",
        width: 80, height: 80, borderRadius: "50%",
        background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
        transform: `scale(${vsProg * vsPulse})`, opacity: vsProg,
        boxShadow: "0 0 30px rgba(99,102,241,0.4), 0 0 60px rgba(99,102,241,0.2)",
        flexShrink: 0,
      }}>
        <span style={{ fontSize: 28, fontWeight: 900, color: "#fff", fontFamily: "'CookieRun', sans-serif" }}>
          {vsText}
        </span>
      </div>

      <div style={{ ...cardStyle(rightColor), opacity: rightProg, transform: `translateX(${rightX}px)` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 8 }}>
          <span style={{ fontSize: 44 }}>{right.icon}</span>
          <span style={{ fontSize: 32, fontWeight: 800, color: rightColor, fontFamily: "'CookieRun', sans-serif" }}>
            {right.title}
          </span>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {renderItems(right.items, "right", rightColor)}
        </div>
      </div>
    </div>
  );
};
```

**사용 예시:**
```tsx
<ComparisonCards
  delay={0.3}
  left={{
    icon: "😰", title: "Before", color: "#ef4444",
    items: ["수동 배포 — 2시간", "장애 30분 후 감지", "수동 스케일링"],
  }}
  right={{
    icon: "🎉", title: "After", color: "#10b981",
    items: ["자동 배포 — 5분", "실시간 10초 감지", "오토 스케일링"],
  }}
/>

// vsText 커스텀
<ComparisonCards vsText="→" left={{...}} right={{...}} />
```

---

### FlipCard — 카드 뒤집기 공개

키워드 카드가 scaleX 기반 2D 뒤집기로 상세 내용을 공개. "사실은..." 효과.
핵심 기술 소개, 퀴즈 형식, 키워드 → 설명 전환에 사용.

> **주의**: Remotion 렌더러에서 CSS 3D (`perspective`, `preserve-3d`, `backfaceVisibility`)는
> 안정적으로 동작하지 않으므로 `scaleX` 기반 2D 시뮬레이션을 사용한다.

```tsx
import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";

export const FlipCard: React.FC<{
  front: { icon: string; title: string };
  back: { title: string; description: string };
  flipAtFrame?: number;
  color?: string;
  width?: number;
  height?: number;
  delay?: number;
}> = ({
  front, back,
  flipAtFrame = 45,
  color = "#6366f1",
  width = 400,
  height = 280,
  delay = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = Math.max(0, frame - delay * fps);

  const enterProg = interpolate(t, [0, 15], [0, 1], {
    extrapolateRight: "clamp", easing: Easing.out(Easing.cubic),
  });
  const enterScale = interpolate(enterProg, [0, 1], [0.7, 1]);

  const flipDuration = 20;
  const flipRaw = interpolate(t, [flipAtFrame, flipAtFrame + flipDuration], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  const scaleX = flipRaw <= 0.5
    ? interpolate(flipRaw, [0, 0.5], [1, 0], { easing: Easing.in(Easing.cubic) })
    : interpolate(flipRaw, [0.5, 1], [0, 1], { easing: Easing.out(Easing.cubic) });

  const showBack = flipRaw > 0.5;

  const distFromCenter = Math.abs(flipRaw - 0.5);
  const liftY = interpolate(distFromCenter, [0, 0.5], [-15, 0], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  const flipGlow = interpolate(distFromCenter, [0, 0.5], [1, 0], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  const floatY = flipRaw >= 1 ? Math.sin(t * 0.08) * 3 : 0;

  return (
    <div style={{
      width, height, opacity: enterProg,
      transform: `scale(${enterScale}) scaleX(${Math.max(0.02, scaleX)}) translateY(${liftY + floatY}px)`,
      background: showBack
        ? `linear-gradient(135deg, ${color}22, ${color}0a)`
        : `linear-gradient(135deg, ${color}18, ${color}08)`,
      borderRadius: 24,
      border: `2px solid ${showBack ? `${color}66` : `${color}44`}`,
      display: "flex", flexDirection: "column",
      alignItems: "center", justifyContent: "center",
      gap: showBack ? 16 : 20, padding: "32px 28px",
      boxShadow: `0 12px 40px ${color}22`,
      overflow: "hidden",
    }}>
      {showBack ? (
        <>
          <span style={{ fontSize: 28, fontWeight: 800, color, fontFamily: "'CookieRun', sans-serif", textAlign: "center" }}>
            {back.title}
          </span>
          <span style={{ fontSize: 19, color: "rgba(226,232,240,0.75)", fontFamily: "'CookieRun', sans-serif", textAlign: "center", lineHeight: 1.6 }}>
            {back.description}
          </span>
        </>
      ) : (
        <>
          <span style={{ fontSize: 72 }}>{front.icon}</span>
          <span style={{ fontSize: 32, fontWeight: 800, color: "#f1f5f9", fontFamily: "'CookieRun', sans-serif" }}>
            {front.title}
          </span>
        </>
      )}
    </div>
  );
};

// 여러 카드 뒤집기 (시차)
export const FlipCardGrid: React.FC<{
  cards: Array<{
    front: { icon: string; title: string };
    back: { title: string; description: string };
    color?: string;
  }>;
  columns?: number;
  delay?: number;
  flipStagger?: number;
}> = ({ cards, columns = 3, delay = 0, flipStagger = 20 }) => {
  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: `repeat(${columns}, 1fr)`,
      gap: 32, width: "100%",
      maxWidth: columns * 420 + (columns - 1) * 32,
    }}>
      {cards.map((card, i) => (
        <FlipCard
          key={i}
          front={card.front}
          back={card.back}
          color={card.color || ["#6366f1", "#ec4899", "#10b981", "#f59e0b", "#3b82f6"][i % 5]}
          flipAtFrame={30 + i * flipStagger}
          delay={delay + i * 0.15}
          width={380}
          height={260}
        />
      ))}
    </div>
  );
};
```

**사용 예시:**
```tsx
<FlipCardGrid
  columns={3}
  delay={0.3}
  flipStagger={25}
  cards={[
    {
      front: { icon: "🔑", title: "인증" },
      back: { title: "OAuth 2.0 + PKCE", description: "코드 챌린지 기반 인증 플로우" },
      color: "#6366f1",
    },
    {
      front: { icon: "⚡", title: "성능" },
      back: { title: "Edge Computing", description: "엣지 서버리스로 레이턴시 80% 감소" },
      color: "#f59e0b",
    },
    {
      front: { icon: "🔒", title: "암호화" },
      back: { title: "E2E Encryption", description: "AES-256-GCM 종단간 암호화" },
      color: "#10b981",
    },
  ]}
/>
```

---

### TimelineCards — 타임라인 스텝 카드

중앙 세로선이 그려지면서 좌우 교차로 카드가 등장. 단계별 프로세스 설명에 사용.
중앙 도트 순환 글로우로 현재 단계 강조.

```tsx
import React from "react";
import { spring, useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";

export interface TimelineStep {
  number: number | string;
  title: string;
  description: string;
  icon?: string;
  color?: string;
}

export const TimelineCards: React.FC<{
  steps: TimelineStep[];
  delay?: number;
}> = ({ steps, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const lineProgress = interpolate(
    frame, [delay * fps, (delay + 1.5) * fps], [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }
  );

  const allInFrame = (delay + steps.length * 0.4 + 0.5) * fps;
  const postEntry = frame - allInFrame;
  const cycleFrames = (durationInFrames - allInFrame) / steps.length;
  const activeIdx = postEntry > 0
    ? Math.floor((postEntry % (cycleFrames * steps.length)) / cycleFrames)
    : -1;

  return (
    <div style={{ position: "relative", width: "100%", maxWidth: 1200 }}>
      {/* 중앙 세로선 — clipPath로 드로잉 효과 */}
      <div style={{
        position: "absolute", left: "50%", top: 0, bottom: 0, width: 3,
        background: "linear-gradient(180deg, #6366f1, #ec4899, #10b981)",
        transform: "translateX(-50%)", transformOrigin: "top",
        clipPath: `inset(0 0 ${(1 - lineProgress) * 100}% 0)`,
        boxShadow: "0 0 12px rgba(99,102,241,0.3)",
      }} />

      {steps.map((step, i) => {
        const isLeft = i % 2 === 0;
        const cardDelay = delay + 0.3 + i * 0.4;
        const prog = spring({
          frame: frame - Math.round(cardDelay * fps), fps,
          config: { damping: 14, stiffness: 110, mass: 0.7 },
        });
        const opacity = interpolate(
          frame, [cardDelay * fps, (cardDelay + 0.3) * fps], [0, 1],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
        );

        const slideX = interpolate(prog, [0, 1], [isLeft ? -80 : 80, 0]);
        const isActive = activeIdx === i;
        const color = step.color || ["#6366f1", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981"][i % 5];
        const floatY = prog >= 0.95 ? Math.sin((frame / fps) * 1.5 + i) * 2 : 0;

        return (
          <div key={i} style={{
            display: "flex", alignItems: "center",
            justifyContent: isLeft ? "flex-end" : "flex-start",
            padding: "16px 0", position: "relative",
          }}>
            {/* 중앙 도트 */}
            <div style={{
              position: "absolute", left: "50%",
              transform: `translateX(-50%) scale(${prog})`,
              width: isActive ? 20 : 14, height: isActive ? 20 : 14,
              borderRadius: "50%",
              background: isActive ? color : "rgba(255,255,255,0.2)",
              border: `2px solid ${color}`,
              boxShadow: isActive ? `0 0 16px ${color}88, 0 0 32px ${color}44` : "none",
              zIndex: 2,
            }} />

            {/* 카드 */}
            <div style={{
              width: "42%",
              marginLeft: isLeft ? 0 : "58%",
              marginRight: isLeft ? "58%" : 0,
              opacity,
              transform: `translateX(${slideX}px) translateY(${floatY}px)`,
              background: isActive
                ? `linear-gradient(135deg, ${color}12, ${color}06)`
                : "rgba(255,255,255,0.03)",
              backdropFilter: "blur(16px)",
              borderRadius: 18,
              border: `1.5px solid ${isActive ? `${color}55` : "rgba(255,255,255,0.08)"}`,
              padding: "24px 28px",
              boxShadow: isActive ? `0 8px 32px ${color}22` : "0 4px 16px rgba(0,0,0,0.2)",
            }}>
              <div style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: 10 }}>
                <div style={{
                  width: 40, height: 40, borderRadius: 12,
                  background: `${color}22`, border: `1.5px solid ${color}44`,
                  display: "flex", alignItems: "center", justifyContent: "center",
                  fontSize: 20, fontWeight: 900, color,
                  fontFamily: "'CookieRun', sans-serif", flexShrink: 0,
                }}>
                  {step.icon || step.number}
                </div>
                <span style={{
                  fontSize: 24, fontWeight: 800,
                  color: isActive ? color : "#f1f5f9",
                  fontFamily: "'CookieRun', sans-serif",
                }}>
                  {step.title}
                </span>
              </div>
              <div style={{
                fontSize: 17, color: "rgba(226,232,240,0.6)",
                fontFamily: "'CookieRun', sans-serif", lineHeight: 1.5,
              }}>
                {step.description}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
```

**사용 예시:**
```tsx
<TimelineCards
  delay={0.3}
  steps={[
    { number: 1, icon: "📝", title: "기획", description: "요구사항 분석, 아키텍처 설계", color: "#6366f1" },
    { number: 2, icon: "💻", title: "개발", description: "TDD 기반 구현, CI 통합 테스트", color: "#ec4899" },
    { number: 3, icon: "🚀", title: "배포", description: "Blue-Green 배포, 실시간 모니터링", color: "#10b981" },
    { number: 4, icon: "📊", title: "분석", description: "피드백 수집, A/B 테스트, 최적화", color: "#f59e0b" },
  ]}
/>
```

---

### MetaphorSplit — 은유 대비 2분할
ComparisonCards의 경량 버전 — 카드 내용을 **짧은 은유 문구 한 줄**로 축약. "도서관 vs 전담 사서" 같이 추상적 대비를 먼저 던지고 디테일은 뒤 씬에서 풀 때 사용. 좌/우 색상 대비 + 거대한 VS 디바이더.

```tsx
const MetaphorSplit: React.FC<{
  leftIcon: string; leftLabel: string; leftMetaphor: string;
  rightIcon: string; rightLabel: string; rightMetaphor: string;
  leftColor?: string; rightColor?: string;
}> = ({ leftIcon, leftLabel, leftMetaphor, rightIcon, rightLabel, rightMetaphor,
       leftColor = "#ef4444", rightColor = "#a3e635" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = (d: number) => spring({
    frame: frame - d, fps, config: { damping: 14, stiffness: 110 },
  });
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 36, justifyContent: "center" }}>
      {[
        { o: s(0),  col: leftColor,  icon: leftIcon,  label: leftLabel,  meta: leftMetaphor },
        null, // VS slot
        { o: s(10), col: rightColor, icon: rightIcon, label: rightLabel, meta: rightMetaphor },
      ].map((side, i) =>
        side === null ? (
          <div key="vs" style={{
            fontFamily: "'CookieRun', sans-serif", fontSize: 56, fontWeight: 900,
            padding: "12px 18px", background: "#0B1221", color: "#fff",
            border: "3px solid #fff", borderRadius: 16,
          }}>VS</div>
        ) : (
          <div key={i} style={{
            transform: `scale(${side.o})`, opacity: side.o,
            background: `linear-gradient(180deg, ${side.col}22, ${side.col}06)`,
            border: `3px solid ${side.col}88`, borderRadius: 24,
            padding: "36px 32px", maxWidth: 480,
            display: "flex", flexDirection: "column", alignItems: "center", gap: 16,
          }}>
            <div style={{ fontSize: 80 }}>{side.icon}</div>
            <div style={{ fontSize: 48, fontWeight: 900, color: side.col,
              fontFamily: "'CookieRun', sans-serif" }}>{side.label}</div>
            <div style={{ fontSize: 24, color: "#475569",
              fontFamily: "'CookieRun', sans-serif", textAlign: "center",
              maxWidth: 400 }}>{side.meta}</div>
          </div>
        )
      )}
    </div>
  );
};
```

**언제 쓰나**: 비교 섹션을 여는 첫 씬. 뒤에 QuadrantMatrix/DualTimeline 같은 더 정밀한 비교 씬이 이어질 때, **은유 선행 → 수치 대비 후행** 순서가 자연스럽다.

### ThreeOptionsImageCards — 이미지 3카드
StaggeredCards의 이미지 특화판 — 텍스트 대신 **아이콘 이미지(SVG/PNG)** 를 중심에 배치. CLI / Obsidian / MCP 같이 서로 다른 도구/방식을 한눈에 보여줄 때. 각 카드 하단에는 라벨 + 서브텍스트.

```tsx
const ThreeOptionsImageCards: React.FC<{
  options: Array<{
    imageSrc: string;   // staticFile(`images/...`)
    label: string;
    sub: string;
    color: string;      // border/glow 컬러
    imageTint?: string; // SVG fill override (선택)
  }>;
}> = ({ options }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div style={{ display: "flex", gap: 28, justifyContent: "center" }}>
      {options.map((o, i) => {
        const s = spring({ frame: frame - i * 6, fps,
          config: { damping: 14, stiffness: 120 } });
        return (
          <div key={i} style={{
            transform: `scale(${s})`, opacity: s,
            background: "rgba(255,255,255,0.6)",
            border: `3px solid ${o.color}88`, borderRadius: 20,
            padding: 32, width: 320, height: 380,
            display: "flex", flexDirection: "column",
            alignItems: "center", justifyContent: "center", gap: 20,
            boxShadow: `0 8px 32px ${o.color}22`,
          }}>
            <img src={o.imageSrc} style={{
              width: 160, height: 160, objectFit: "contain",
              filter: o.imageTint ? undefined : undefined,
            }} />
            <div style={{ fontSize: 28, fontWeight: 900, color: o.color,
              fontFamily: "'CookieRun', sans-serif" }}>{o.label}</div>
            <div style={{ fontSize: 18, color: "#64748b",
              fontFamily: "'CookieRun', sans-serif", textAlign: "center" }}>
              {o.sub}
            </div>
          </div>
        );
      })}
    </div>
  );
};
```

**에셋 주의**: SVG의 `fill` 컬러는 직접 인라인 속성으로 지정. CSS `filter: invert/hue-rotate` 트릭은 렌더 불안정 — **SVG 원본에 fill 속성 직접 삽입하는 방식이 권장**.

### 카드 패턴 선택 가이드

| 패턴 | 추천 씬 | 카드 수 |
|------|---------|--------|
| StaggeredCards | 기능 소개, 서비스 항목, 스펙 나열 | 3~6개 |
| ComparisonCards | Before/After, 기술 비교, 플랜 비교 | 2개 (좌/우) |
| **MetaphorSplit** | **비교 섹션의 오프닝 (은유 한 줄 대비)** | **2개 (좌/우)** |
| **ThreeOptionsImageCards** | **도구/방식 3종 (아이콘 이미지 중심)** | **3개** |
| FlipCardGrid | 키워드 → 상세, 퀴즈, 핵심 기술 공개 | 2~4개 |
| TimelineCards | 단계별 프로세스, 로드맵, 히스토리 | 3~6개 |

---

---

<a id="signature-components"></a>

## 시그니처 컴포넌트 (Signature Components)

특정 내러티브를 위해 설계된 전용 비주얼. 씬 톤에 강한 시그니처를 부여한다.

### TweetCard — 트위터 인용 카드

다크 테마 트위터 UI. 아바타 + 작성자/핸들/날짜 + 단어별 reveal + accentWords 펄싱 + 좋아요/리트윗 카운트업.

```tsx
import { TweetCard } from "./components/TweetCard";

<TweetCard
  author="Andrej Karpathy"
  handle="@karpathy"
  avatar="🤖"
  date="Apr 2026"
  text="The hottest new programming language is English."
  accentWords={["English", "programming"]}
  likes={52300}
  retweets={8100}
  delay={0.3}
/>
```

**주요 기법**: spring 입장 → `accentWords` 포함 단어에 `interpolateColors` hue shift + `drop-shadow` 펄스. 메트릭은 `Easing.out(Easing.exp)`로 카운트업.

**사용 씬 가이드**: 권위자 인용, 소셜 증거, 반전 후킹. 배경이 있는 iPad 프레임 내부에서도 대비가 강해 눈길을 끈다.

---

### CodeEditorSplit — 좌/우 코드 에디터 비교

2-Window IDE 레이아웃 + 중앙 ✕ 충돌 + 타이핑 효과 + 하단 경고 배너.

```tsx
import { CodeEditorSplit } from "./components/CodeEditorSplit";

<CodeEditorSplit
  leftTitle="Before"
  leftFile="legacy.ts"
  leftLines={[
    "// blind prompting",
    "const p = `Do X`;",
    "await llm(p);",
  ]}
  rightTitle="After"
  rightFile="engineered.ts"
  rightLines={[
    "// context engineering",
    "const ctx = buildContext({...});",
    "await llm(ctx);",
  ]}
  leftAccent="#ef4444"
  rightAccent="#10b981"
  warningText="Implicit context drift"
  delay={0.3}
/>
```

**주요 기법**: 각 Window는 slide-in (`interpolate(entry, [0,1], [±200, 0])`), 코드 라인은 `typingProgress`로 글자별 reveal. Syntax 하이라이트는 간단 정규식 기반 `dangerouslySetInnerHTML`.

**색상**: `leftAccent` / `rightAccent`를 대비로 주면 Before/After 대조가 명확. warningText는 경고 신호용 (펄싱).

---

### RocketTrajectory — 로켓 성장 곡선

베지어 곡선 path를 로켓(🚀)이 비행 + 마일스톤 노드 + 트레일 스파클 + 최종값 배지.

```tsx
import { RocketTrajectory } from "./components/RocketTrajectory";

<RocketTrajectory
  title="채택 속도"
  milestones={[
    { day: "Day 1", count: 1000, label: "launch" },
    { day: "Day 7", count: 10000, label: "viral" },
    { day: "Day 30", count: 100000, label: "scale" },
  ]}
  finalValue={1000000}
  finalSuffix="+"
  finalLabel="users"
  delay={0.3}
/>
```

**주요 기법**: `evolvePath` + `getPointAtLength`로 로켓 좌표 추출, `Math.atan2`로 진행 방향 따라 회전. 트레일은 path 뒤쪽에 점을 역방향 샘플링.

**사용 씬 가이드**: 성장 지표, 채택 속도, KPI 궤적. `PATH` 상수를 조정해 곡률 변경 가능.

---

### LethalTriangle — 치명적 3대 위험 요소

삼각형 + 3 꼭짓점 위험 요소 + 중앙 해골 펄스. 빨간색 danger 테마 전용.

```tsx
import { LethalTriangle } from "./components/LethalTriangle";

<LethalTriangle
  title="LETHAL TRIFECTA"
  subtitle="Simon Willison"
  vertices={[
    { label: "Private Data", icon: "🔒", description: "신뢰 구간 내부" },
    { label: "Untrusted Input", icon: "📥", description: "외부 유입" },
    { label: "External Comms", icon: "📡", description: "유출 경로" },
  ]}
  centerLabel="CRITICAL"
  centerIcon="💀"
  delay={0.3}
/>
```

**주요 기법**: 정삼각형 좌표 (`-π/2`, `π/6`, `5π/6`) + 에지별 `edgeProgress`로 순차 드로잉 → 꼭짓점 `Easing.out(Easing.back(2))` + 해골 danger 펄스.

**사용 씬 가이드**: 보안 원칙 경고, 3요소 충돌, Lethal Trifecta 유형 주제.

---

### HorseHarnessDiagram — 말+마구 은유 다이어그램

좌측 말 이모지(모델) + 중앙 `+` + 우측 마구 부품 4종 (그리드). 하네스 엔지니어링 비유 씬용.

```tsx
import { HorseHarnessDiagram } from "./components/HorseHarnessDiagram";

<HorseHarnessDiagram
  horseLabel="Model"
  horseSubtitle="LLM 자체"
  harnessLabel="+ Harness"
  parts={[
    { icon: "📜", name: "Prompt", description: "지시 계층", color: "#6366f1" },
    { icon: "🧠", name: "Context", description: "메모리/검색", color: "#ec4899" },
    { icon: "🛠", name: "Tools", description: "액션 인터페이스", color: "#f59e0b" },
    { icon: "🔄", name: "Loop", description: "반복/검증", color: "#10b981" },
  ]}
  delay={0.3}
/>
```

**주요 기법**: 좌측은 slide-in + bob (`Math.sin(sec * 1.5) * 6`) + 살짝 회전, 중앙 `+`는 `sec * 15deg` 회전, 우측 부품은 `spring` 스태거 + float.

---

### ReActLoopDiagram — 순환 루프 + 후손 뱃지

원형 path를 따라 노드 4개 배치 + 방향 화살표 + 순환하는 traveling dot + 중심 라벨 + 하단 후손 뱃지.

```tsx
import { ReActLoopDiagram } from "./components/ReActLoopDiagram";

<ReActLoopDiagram
  nodes={[
    { label: "Thought", icon: "💭", color: "#6366f1", description: "추론 생성" },
    { label: "Action", icon: "⚡", color: "#ec4899", description: "툴 호출" },
    { label: "Observation", icon: "👁", color: "#f59e0b", description: "결과 관찰" },
    { label: "Reflection", icon: "🔁", color: "#10b981", description: "자기 수정" },
  ]}
  centerLabel="ReAct"
  descendants={["CoT", "Tree-of-Thoughts", "Reflexion", "LangGraph"]}
  delay={0.3}
/>
```

**주요 기법**: 4개 노드 극좌표 배치, `evolvePath` 드로잉 → 완료 후 `(sec * 0.3) % 1`로 traveling dot 궤도. 색상은 `interpolateColors`로 구간별 전이.

**사용 씬 가이드**: ReAct/루프/순환 패턴, 가계도/후손 파생 표현. `centerLabel`과 `descendants` 생략 가능.

---

### QuadrantMatrix — 2×2 분면 매트릭스

X/Y 축 + 4분면 카드 + 활성 하이라이트 사이클. BCG 매트릭스, 위험/영향 매트릭스 류에 적합.

```tsx
import { QuadrantMatrix } from "./components/QuadrantMatrix";

<QuadrantMatrix
  xAxis={{ left: "Low Cost", right: "High Cost" }}
  yAxis={{ top: "High Value", bottom: "Low Value" }}
  quadrants={[
    { icon: "💎", title: "Gold", description: "저비용·고가치", color: "#10b981" },
    { icon: "🚀", title: "Invest", description: "고비용·고가치", color: "#6366f1" },
    { icon: "🗑", title: "Drop", description: "저비용·저가치", color: "#94a3b8" },
    { icon: "⚠", title: "Reconsider", description: "고비용·저가치", color: "#ef4444" },
  ]}
  centerLabel="2×2"
  delay={0.3}
/>
```

**주요 기법**: 축선은 `strokeDasharray`로 점선 드로잉, 4분면 카드는 코너에서 중앙으로 slide-in + rotate 보정. `activeIdx`가 45프레임마다 순회하며 해당 카드에 강조 글로우 부여.

**주의**: 세로 축 라벨은 `writing-mode: vertical-*` 대신 `rotate(-90/+90deg)` + `translate` 사용 (writing-mode는 텍스트 반전 버그 유발).

### QuadrantMatrix v2 — 축 라벨 가독성 개선판
기존 QuadrantMatrix에서 **축 라벨이 셀 경계에 묻혀 읽히지 않는 문제**를 해결한 개선판. 주요 변경:

1. **축 라벨을 흰 배경 칩 + `zIndex: 10`으로 감싸** 박스 경계 위에 또렷이 뜨게
2. **DotLabel(분면 중앙 점)을 분면 정중앙(25%/75%)** 로 이동 — 서브라벨까지 사분면 셀 안에 완전히 들어감
3. 대각선 화살표(두 점 연결) 끝점도 25%/75% 기준으로 재계산

```tsx
// 축 라벨 예시 (상단 화살표 위)
<div style={{
  position: "absolute", top: -32, left: "50%", transform: "translateX(-50%)",
  background: "#fff", padding: "4px 14px", borderRadius: 8,
  border: "2px solid #1e293b", boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
  fontSize: 18, fontWeight: 800, color: "#1e293b",
  fontFamily: "'CookieRun', sans-serif",
  zIndex: 10,
}}>▲ Active</div>

// DotLabel: 분면 정중앙 (25% / 75%)
const DotLabel: React.FC<{ x: string; y: string; color: string; emoji: string; label: string; sub: string }> = ...;
<DotLabel x="25%" y="75%" color="#ef4444" emoji="🔍" label="RAG" sub="수동 검색형" />
<DotLabel x="75%" y="25%" color="#a3e635" emoji="📚" label="LLM Wiki" sub="능동 사서형" />
```

**언제 쓰나**: QuadrantMatrix가 필요한데 축 이름(▲Active / ▼Passive / ◀Query / Ingest▶)이 박스 선과 겹쳐 읽히지 않을 때. 기본 QuadrantMatrix 대신 기본값으로 이 버전을 쓰는 것을 고려.

### DualTimeline — 상/하 이중 타임라인 비교
TimelineCards의 **비교형 변종** — 상단 행과 하단 행에 서로 다른 시간 거동을 배치하여 "반복 vs 누적", "동기 vs 비동기" 같은 시간축 차이를 시각화. 좌측 라벨 + 가로 타임라인 + 각 스텝 칩 + 푸터 요약.

```tsx
const DualTimeline: React.FC<{
  rows: Array<{
    label: string;         // "RAG" / "LLM Wiki"
    color: string;
    chips: string[];       // 타임라인 위 스텝 텍스트
    behavior: "repeat" | "accumulate";  // 반복(점선 루프) vs 누적(계단형 높이)
  }>;
  footerNote?: string;
}> = ({ rows, footerNote }) => {
  // 각 row의 타임라인을 spring + stagger로 그리고,
  // behavior=repeat이면 마지막 칩 뒤에 ↻ 무한 기호,
  // behavior=accumulate이면 칩 높이가 점점 커지며 누적 암시
  // ...
};
```

**언제 쓰나**: "A는 쿼리마다 재검색 / B는 Ingest 시점부터 누적" 같이 **시간 흐름에 따른 행동 차이**를 대비시킬 때. 단순 Before/After는 ComparisonCards로 충분하지만, 시간축 거동 대비는 DualTimeline이 적합.

### ThreeLayerArchitecture — 3계층 스택 다이어그램
계층(Layer) 아키텍처를 위→아래 스택으로 보여줌. 각 계층별 예시 칩 4~5개 + 계층 간 화살표 라벨(Ingest/Schema 같은 플로우 명).

```tsx
const ThreeLayerArchitecture: React.FC<{
  layers: Array<{
    name: string;           // "Schema" / "Wiki" / "Raw Sources"
    color: string;
    desc: string;
    chips: string[];        // 예시 파일/항목
    icon?: string;
  }>;
  flowLabels?: string[];    // 계층 사이 화살표 라벨 (길이 = layers.length - 1)
}> = ({ layers, flowLabels }) => {
  // 각 계층을 위→아래 수직 스택, 계층 사이는 두꺼운 세로 화살표 + 라벨
  // ...
};
```

**언제 쓰나**: 3~4 계층 소프트웨어 아키텍처, 데이터 파이프라인, 책임 계층 설명. **위/아래 의존 방향**이 명확한 계층 구조에 적합.

### FileTreeDetail — 파일 트리 + 운영 원칙 카드
레포/프로젝트 구조를 소개할 때의 시그니처. 좌측에 파일 트리(들여쓰기 + 아이콘), 우측에 운영 원칙 카드 N개. 트리의 각 엔트리는 파일명 + 간단한 코멘트.

```tsx
const FileTreeDetail: React.FC<{
  root: string;                    // "~/my-project/" 같은 루트 표기
  tree: Array<{                    // 중첩 구조
    name: string;
    type: "folder" | "file";
    comment?: string;
    depth: number;
    icon?: string;
  }>;
  principles: Array<{              // 우측 원칙 카드
    title: string;
    desc: string;
    color: string;
  }>;
}> = ({ root, tree, principles }) => {
  // 왼쪽 60% 트리 (monospace 폰트, │ ├─ └─ 문자로 가지),
  // 오른쪽 40% 원칙 카드 세로 스택 (spring stagger 입장)
  // ...
};
```

**에셋 고려**: 트리 텍스트는 `JetBrains Mono` 같은 모노스페이스 필수. 브랜칭 문자(`│ ├─ └─`)는 유니코드 그대로 사용하면 렌더링 양호.

### TerminalMock — CLI 타이핑 애니메이션
검은 터미널 창에 프롬프트 + 명령어 타이핑 애니메이션 + 출력. 명령어 문자수 기반 타이핑 시작 프레임을 계산하여 자연스러운 타자 연출. CodeEditorSplit의 **단일 터미널 버전**.

```tsx
const TerminalMock: React.FC<{
  prompt?: string;              // "$ " / "❯ " 등
  commands: Array<{
    cmd: string;
    output?: string;            // 선택적 출력 (명령어 끝나면 fade-in)
    delay?: number;             // 초 단위 시작 오프셋
  }>;
  showCursor?: boolean;
}> = ({ prompt = "$ ", commands, showCursor = true }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const CHARS_PER_SEC = 12;     // 타이핑 속도
  // 각 명령어의 시작 프레임과 현재까지 타이핑된 문자수를 계산
  // ...
};
```

**언제 쓰나**: CLI 도구 데모, 빌드/배포 커맨드 설명, 에이전트 프롬프트 예시. `showCursor`를 짝수 초마다 깜빡이게 하면 생동감 추가.

### McpWiring — 배선 다이어그램 (narration sync 지원)
중앙 서버 노드 + 주변 여러 클라이언트 노드를 curved SVG line으로 연결. 노드는 아이콘 + 라벨 + 배지. **narration sync** 기능 내장: 내레이션 문장을 `.?!` 단위로 분할하고 트리거 키워드 포함 문장 start에서 해당 노드가 하이라이트됨 (글로우 + scale).

```tsx
const McpWiring: React.FC<{
  nodes: Array<{
    id: string;           // 하이라이트 트리거용
    role: "server" | "client" | "source";
    label: string;
    x: number; y: number;
    icon?: string;
    badge?: string;
  }>;
  edges: Array<{ from: string; to: string; label?: string }>;
  // narration sync props (선택)
  narration?: string;
  audioDurationSec?: number;
  durationSec?: number;
  triggers?: Array<{ keyword: string; nodeIds: string[] }>;
}> = (...) => { /* ... */ };
```

**언제 쓰나**: MCP 서버 배선, 마이크로서비스 토폴로지, 데이터 소스 → 가공기 → 소비자 흐름. narration 트리거는 "설명 문장이 들어올 때마다 해당 노드가 순차로 커지는" 효과를 만들어 이해를 돕는다.

### LintReportCard — 분석 리포트 카드 (충돌/경고 출력)
CI/린트/리뷰 결과를 한 장 카드로 요약. 상단 헤더(리포트명 + severity 태그), 중단 좌/우 충돌 페이지 대비(CLAIM vs COUNTER) + 사이 ⚠ 스탬프, 하단 결론 배너.

```tsx
const LintReportCard: React.FC<{
  reportName: string;       // "lint_report.md"
  severity: "info" | "review" | "error";
  summary: string;          // "불일치 1건 — Adam vs 반례"
  claim: { file: string; excerpt: string; color?: string };
  counter: { file: string; excerpt: string; color?: string };
  conclusion: string;       // "사람이 확인할 지점을 LLM이 먼저 짚어준다"
}> = (...) => { /* ... */ };
```

**언제 쓰나**: 데모 씬에서 "도구가 뭘 잡아줬는지" 결과를 보여줄 때. Lint/CI/코드리뷰/AI 감사 결과 범용. 페이지 카드 사이 대시 라인 스캔 애니메이션을 넣으면 "비교 중" 연출 강화.

---

<a id="special-charts"></a>

## 스페셜 차트 (Special Charts)

### DefinitionFormula — 공식 정의 레이아웃

**"X = A + B"** 스타일의 정의 씬에 최적화된 3-stage reveal 패턴. 개념 정의 내레이션의 자연스러운 흐름(타이틀 → 설명 → 구성요소)에 동기화.

**레이아웃**:
```
        [TITLE BOX]                    ← stage 1: 타이틀 박스
   "한 줄 정의 캡션"                   ← stage 2: 단어별 reveal
  =   [⭕ 요소1]   +   [➡ 요소2]       ← stage 3: 공식 순차 reveal
```

```tsx
import { spring, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

type TermShape = "circle" | "line" | "square" | "custom";

const DefinitionFormula: React.FC<{
  title: string;                      // "GraphDB"
  titleColor?: string;                // 박스 테두리 색 (기본 mint)
  caption: string;                    // "데이터를 그래프 구조로 저장하는 DB"
  captionAccent?: string[];           // 캡션 내 강조 단어 ["그래프"]
  terms: Array<{                      // [{shape:'circle', label:'점', sub:'노드', color:'#FF7A3C'}, ...]
    shape: TermShape;
    label: string;
    subLabel?: string;
    color: string;
    customSvg?: React.ReactNode;
  }>;
  // 타이밍 (프레임 기준 30fps)
  titleStartFrame?: number;           // default 6
  captionStartFrame?: number;         // default 90 (~3s, 내레이션 "데이터를~"에 맞춤)
  formulaStartFrame?: number;         // default 310 (~10.3s, 내레이션 "요소1과 요소2~"에 맞춤)
  glowStartFrame?: number;            // default 480 (완성 glow 시작)
}> = ({
  title, titleColor = "#5EE6C1",
  caption, captionAccent = [],
  terms,
  titleStartFrame = 6,
  captionStartFrame = 90,
  formulaStartFrame = 310,
  glowStartFrame = 480,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleProg = spring({ frame: frame - titleStartFrame, fps, config: { damping: 14, stiffness: 180 } });
  const captionProg = spring({ frame: frame - captionStartFrame, fps, config: { damping: 14, stiffness: 160 } });
  const eqProg = spring({ frame: frame - formulaStartFrame, fps, config: { damping: 12, stiffness: 200 } });
  const termProgs = terms.map((_, i) =>
    spring({ frame: frame - formulaStartFrame - 30 - i * 60, fps, config: { damping: 10, stiffness: 180 } })
  );
  const glowProg = interpolate(frame, [glowStartFrame, glowStartFrame + 60], [0, 1], { extrapolateRight: "clamp" });
  const glowPulse = Math.sin((frame - glowStartFrame - 60) * 0.1) * 0.5 + 0.5;

  // Title box + Caption(WordByWordText) + Formula row ( = , Chip, + , Chip , ...)
  // 각 Chip은 shape에 따라 원 / 화살표 / 사각 / custom SVG를 그림.
  // stage3에서 terms를 순차 reveal: termProgs[i] 기반 opacity/scale.
  // ...
};
```

**주요 기법**:
- **타이밍 독립 파라미터**: `titleStartFrame / captionStartFrame / formulaStartFrame`을 씬의 내레이션 singpost 시점에 정확히 맞춤 (subtitle_timings.json 참조)
- **shape 렌더러**: `circle`(꽉 찬 원), `line`(화살표 엣지), `square`(사각), `custom`(외부 SVG 주입)
- **glow pulse**: 공식 완성 후 타이틀 박스에 `boxShadow`로 맥동 glow (sine wave × brand color 40% alpha)
- **캡션 accent**: `WordByWordText`를 재사용, `accentWords`에 강조 단어 전달

**사용 씬 가이드**:
- "X는 A와 B로 구성된다" 류 정의 씬
- 개념의 구성 요소 2~3개를 시각적 공식으로 제시 (GraphDB = 노드 + 엣지, ACID = 원자성 + 일관성 + 격리 + 지속성, Prompt = 지시 + 예시)
- `word-by-word`(문장 통째 reveal) / `glass-card`(선언형) / `flip-cards`(키워드→상세)와 차별점: **공식의 구조 자체**를 레이아웃으로 표현

**실전 레퍼런스**: graphrag 씬 3 (`vod/graphrag/graphrag-video/src/components/SceneVisual.tsx` Scene3).

---

### ScaleBar — 1차원 스케일 축 + 마커
Personal → Enterprise 같은 1차원 스펙트럼에 **두 개 이상의 점을 마커로** 찍어 포지셔닝을 시각화. 축 양 끝에 구간 라벨, 중간에 마커 + 라벨 + 서브 텍스트, 하단에 "Not either/or" 같은 배너 옵션.

```tsx
const ScaleBar: React.FC<{
  leftLabel: string;           // "Personal"
  rightLabel: string;          // "Enterprise"
  markers: Array<{
    position: number;          // 0.0 ~ 1.0
    color: string;
    label: string;
    sub?: string;
    side?: "top" | "bottom";   // 라벨 배치 (충돌 방지)
  }>;
  banner?: string;             // "Not either/or" 같은 하단 배너
}> = ({ leftLabel, rightLabel, markers, banner }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const drawProgress = spring({ frame, fps,
    config: { damping: 20, stiffness: 80 }});
  // 축 선을 좌→우 drawProgress 비율로 drawing,
  // 각 marker는 drawProgress가 position 넘으면 fade/pop-in
  return (
    <div style={{ width: 1200, position: "relative", padding: "80px 60px" }}>
      {/* 축 선 */}
      <div style={{
        height: 6, borderRadius: 3, background: "#e2e8f0",
        position: "relative",
      }}>
        <div style={{
          position: "absolute", top: 0, left: 0, height: "100%",
          width: `${drawProgress * 100}%`,
          background: "linear-gradient(90deg, #6366f1, #ec4899)",
          borderRadius: 3,
        }} />
      </div>
      {/* 구간 라벨 */}
      <div style={{
        display: "flex", justifyContent: "space-between", marginTop: 12,
        fontSize: 24, fontFamily: "'CookieRun', sans-serif", color: "#64748b",
      }}>
        <span>{leftLabel}</span>
        <span>{rightLabel}</span>
      </div>
      {/* 마커 */}
      {markers.map((m, i) => (
        <Marker key={i} {...m} drawProgress={drawProgress} />
      ))}
      {banner && (
        <div style={{
          marginTop: 48, textAlign: "center",
          fontSize: 36, fontWeight: 900, color: "#1e293b",
          fontFamily: "'CookieRun', sans-serif",
          padding: "14px 32px", background: "rgba(99,102,241,0.08)",
          border: "2px solid rgba(99,102,241,0.35)", borderRadius: 999,
          display: "inline-block",
        }}>{banner}</div>
      )}
    </div>
  );
};
```

**언제 쓰나**: "규모" 같은 1차원 축에 두 방식의 적정 위치를 찍을 때. QuadrantMatrix(2차원)는 과잉이고 ComparisonCards(2집합)는 축이 없을 때 중간 지점.

---

### AnimatedPieChart — 애니메이션 파이차트

`@remotion/shapes`의 `Pie` 컴포넌트 활용. 세그먼트 순차 채우기 + 완료 후 전체 회전 + explode 진동 + 역회전 중앙 라벨.

```tsx
import { AnimatedPieChart } from "./components/AnimatedPieChart";

<AnimatedPieChart
  segments={[
    { value: 45, label: "Prompt", color: "#6366f1" },
    { value: 30, label: "Context", color: "#ec4899" },
    { value: 25, label: "Harness", color: "#10b981" },
  ]}
  radius={160}
  delay={0.3}
/>
```

**주요 기법**: 각 세그먼트 `progress: segFill`로 부채꼴 확장. 전체 채워지면 `rotation = sec * 15`, 각 세그먼트 `midAngle` 방향으로 작게 폭발 (4px 진동). 중앙 라벨은 `rotate(-rotation)`으로 안정.

**사용 씬 가이드**: 비율/점유율, 구성 요소 분해, "절반은 맞았다" 류 반전.

---

<a id="infrastructure"></a>

## 인프라 (Infrastructure)

### DynamicBackground — 애니메이션 배경 레이어

`AbsoluteFill` 기반의 배경 레이어. `IPadTemplate` 내부에서 화면 전체를 덮어 정적 배경을 지속 모션으로 전환한다.

```tsx
import { DynamicBackground } from "./components/DynamicBackground";

<AbsoluteFill>
  <DynamicBackground accent="#6366f1" intensity={1} />
  {/* 씬 콘텐츠 */}
</AbsoluteFill>
```

**구성 레이어 (4중)**:
1. **Radial gradient 드리프트** — 2개 gradient가 대각선 방향으로 서서히 팬 (`sin/cos(t * 0.3)`)
2. **드리프팅 그리드** — 80×80 SVG pattern을 `gridOffset = (t * 20) % 80`으로 무한 스크롤
3. **Floating shapes 14개** — `@remotion/shapes` (원/별/삼각/육각) 랜덤 분포 + 궤도 운동 + 회전 + hue shift
4. **Light sweep** — 45° 대각선 `linear-gradient`가 `mixBlendMode: "screen"`으로 화면 쓸어감

**props**:
- `accent` — 그리드/색상 기준 (기본 `#6366f1`)
- `intensity` — 0~1로 전체 opacity 스케일링 (밝은 배경에서 0.6 권장)

**주의**: 내부에 14개 shapes + SVG pattern이 계속 렌더되므로 CPU 비용이 있다. 모든 씬에서 공통 사용 시 `IPadTemplate`에 한 번만 붙이는 것이 효율적.

---

### 이징 변주 가이드 — Easing Variety Guide

동일한 spring() 입장 반복을 피하기 위한 이징 선택 가이드.
같은 visual 타입이 연속되더라도 이징을 변주하면 시각적 리듬이 다양해진다.

| 상황 | 추천 이징 | 코드 |
|------|---------|------|
| 빠르게 팝업 (강조) | back 오버슈트 | `Easing.out(Easing.back(1.7))` |
| 부드럽게 등장 (기본) | cubic out | `Easing.out(Easing.cubic)` |
| 탄성 바운스 (유쾌) | elastic | `Easing.out(Easing.elastic(1))` |
| 점진적 가속→감속 | ease in-out | `Easing.inOut(Easing.ease)` |
| 급격한 감속 (극적) | exponential | `Easing.out(Easing.exp)` |
| 커스텀 곡선 | bezier | `Easing.bezier(0.25, 0.1, 0.25, 1)` |

**변주 규칙:**
- 같은 visual 타입이 2씬 연속 → 두 번째 씬은 다른 이징 사용
- 카드 계열(StaggeredCards, ComparisonCards, TimelineCards)이 연속 → 입장 방향/이징 교차
- intro/outro 씬 → `Easing.out(Easing.back())` 또는 `elastic`으로 임팩트
- 데이터 씬(CountUpNumber, ProgressRing) → `Easing.out(Easing.cubic)` 유지 (가독성 우선)

**spring() 변주:**
| 느낌 | damping | stiffness | mass |
|------|---------|-----------|------|
| 가볍고 빠른 | 14 | 200 | 0.4 |
| 기본 자연스러운 | 12 | 120 | 0.7 |
| 무겁고 느린 | 8 | 80 | 1.2 |
| 탄성 있는 바운스 | 6 | 150 | 0.5 |

---

## PPT-Style Animation Primitives

파워포인트/Keynote의 슬라이드 애니메이션을 **재사용 가능한 래퍼 컴포넌트**로 표준화한 9종 프리미티브.
`<PPTFlyIn direction="left">{children}</PPTFlyIn>` 형태로 어떤 카드/텍스트/이미지든 감싸서 입장 효과만 덧입힐 수 있다.

> **적용 범위 (중요):**
> - 프리미티브는 카드/요소의 **내부 연출**에만 적용된다. `SceneVisual`의 컴포넌트 매핑, visual 타입 분포, 다이버시티 예산/카테고리 집계에는 **영향 없음**.
> - 즉, `staggered-cards` 씬 안에서 카드 각각에 `PPTFlyIn`을 감싸도 visual 타입은 여전히 `staggered-cards` 1개로 집계된다.
> - 기존 GlassCard/StaggeredCards/ComparisonCards/TimelineCards 내부의 입장 로직을 **대체하지 않는다**. 새로 짜는 씬 또는 기존 씬을 리프레시할 때 외부 래퍼로 추가한다.

**공통 규칙:**
- 모든 프리미티브는 `delay` (초 단위), `durationFrames` (기본 15~20), `style` 오버라이드를 지원한다.
- 입장 후에도 정적이 되지 않도록 subtle float/glow를 유지한다 (정적 프레임 방지 원칙).
- Remotion API 관례 준수: `useCurrentFrame`, `useVideoConfig`, `spring`, `interpolate`, `Easing`만 사용. DOM 직접 조작 금지.
- 공통 import:
  ```tsx
  import React from "react";
  import { spring, interpolate, useCurrentFrame, useVideoConfig, Easing } from "remotion";
  ```

**2씬 이내 연속 사용 시 변주 원칙 (요약):**
- 같은 프리미티브 2회 연속 사용 금지는 아니지만, **이징/방향/staggerMs 중 1개 이상은 교차**한다.
- 상세 조합은 각 프리미티브 하단의 "연속 사용 시 변주" 섹션 참조.

---

### 1. PPTFlyIn — Fly-In / Slide-In

카드가 좌/우/상/하에서 spring 기반으로 날아 들어온다. 파워포인트의 "Fly In" 효과에 해당.

**Props:**
| prop | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| children | ReactNode | (required) | 감쌀 요소 |
| direction | `'left' \| 'right' \| 'top' \| 'bottom'` | `'left'` | 진입 방향 |
| delay | number | 0 | 시작 지연 (초) |
| distance | number | 200 | 오프스크린 거리 (px) |
| damping | number | 12 | spring damping |
| stiffness | number | 120 | spring stiffness |
| style | CSSProperties | - | 외부 style 오버라이드 |

```tsx
export const PPTFlyIn: React.FC<{
  children: React.ReactNode;
  direction?: "left" | "right" | "top" | "bottom";
  delay?: number;
  distance?: number;
  damping?: number;
  stiffness?: number;
  style?: React.CSSProperties;
}> = ({
  children,
  direction = "left",
  delay = 0,
  distance = 200,
  damping = 12,
  stiffness = 120,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const prog = spring({
    frame: frame - Math.round(delay * fps),
    fps,
    config: { damping, stiffness, mass: 0.7 },
  });
  const opacity = interpolate(
    frame,
    [delay * fps, (delay + 0.25) * fps],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const axis = direction === "left" || direction === "right" ? "X" : "Y";
  const sign = direction === "left" || direction === "top" ? -1 : 1;
  const offset = interpolate(prog, [0, 1], [sign * distance, 0]);

  return (
    <div
      style={{
        opacity,
        transform: `translate${axis}(${offset}px)`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};
```

**사용 예시:**
```tsx
// 왼쪽에서 날아오는 카드
<PPTFlyIn direction="left" delay={0.3}>
  <GlassCard>...</GlassCard>
</PPTFlyIn>

// 그리드 내 카드들에 방향 교차 적용
{cards.map((c, i) => (
  <PPTFlyIn
    key={i}
    direction={i % 2 === 0 ? "left" : "right"}
    delay={0.2 + i * 0.15}
  >
    <GlassCard>{c.title}</GlassCard>
  </PPTFlyIn>
))}
```

**연속 사용 시 변주:** 첫 씬 `direction="left", stiffness=120` → 다음 씬 `direction="bottom", stiffness=160, distance=120` 로 방향+속도 교차.

**적용 가능 컴포넌트:** GlassCard, StepBadge, BlogImage, IconElement, 커스텀 카드 어떤 것이든.

---

### 2. PPTFadeSequential — Appear / Fade-Sequential

자식 배열을 순차 페이드인. 파워포인트의 "Appear with timing" 효과.

**Props:**
| prop | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| items | ReactNode[] | (required) | 순차 등장할 항목들 |
| delay | number | 0 | 전체 시작 지연 (초) |
| staggerSec | number | 0.18 | 항목 간 간격 (초) |
| fadeDurationSec | number | 0.35 | 개별 페이드인 길이 (초) |
| liftY | number | 12 | 페이드인 시 살짝 올라오는 거리 (px) |
| style | CSSProperties | - | 컨테이너 style |

```tsx
export const PPTFadeSequential: React.FC<{
  items: React.ReactNode[];
  delay?: number;
  staggerSec?: number;
  fadeDurationSec?: number;
  liftY?: number;
  style?: React.CSSProperties;
}> = ({
  items,
  delay = 0,
  staggerSec = 0.18,
  fadeDurationSec = 0.35,
  liftY = 12,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16, ...style }}>
      {items.map((item, i) => {
        const itemDelay = delay + i * staggerSec;
        const opacity = interpolate(
          frame,
          [itemDelay * fps, (itemDelay + fadeDurationSec) * fps],
          [0, 1],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
        );
        const y = interpolate(opacity, [0, 1], [liftY, 0]);
        return (
          <div key={i} style={{ opacity, transform: `translateY(${y}px)` }}>
            {item}
          </div>
        );
      })}
    </div>
  );
};
```

**사용 예시:**
```tsx
<PPTFadeSequential
  delay={0.3}
  staggerSec={0.2}
  items={[
    <BigTitle text="첫 번째 포인트" key="a" />,
    <BigTitle text="두 번째 포인트" key="b" />,
    <BigTitle text="세 번째 포인트" key="c" />,
  ]}
/>
```

**연속 사용 시 변주:** 첫 씬 `staggerSec=0.18, liftY=12` → 다음 씬 `staggerSec=0.12, liftY=0` (더 촘촘하게 + lift 제거)로 리듬 변화.

**적용 가능 컴포넌트:** 불릿 포인트, 리스트, 이미지 시퀀스, StepBadge 나열.

---

### 3. PPTZoom — Zoom / Grow

중앙에서 확대 등장. 파워포인트 "Zoom In" + "Grow" 효과.

**Props:**
| prop | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| children | ReactNode | (required) | 감쌀 요소 |
| delay | number | 0 | 시작 지연 (초) |
| fromScale | number | 0 | 시작 스케일 (0~1) |
| damping | number | 12 | spring damping |
| stiffness | number | 110 | spring stiffness |
| origin | string | `'center'` | transform-origin |
| style | CSSProperties | - | 외부 style |

```tsx
export const PPTZoom: React.FC<{
  children: React.ReactNode;
  delay?: number;
  fromScale?: number;
  damping?: number;
  stiffness?: number;
  origin?: string;
  style?: React.CSSProperties;
}> = ({
  children,
  delay = 0,
  fromScale = 0,
  damping = 12,
  stiffness = 110,
  origin = "center",
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const prog = spring({
    frame: frame - Math.round(delay * fps),
    fps,
    config: { damping, stiffness, mass: 0.6 },
  });
  const scale = interpolate(prog, [0, 1], [fromScale, 1]);
  const opacity = interpolate(
    frame,
    [delay * fps, (delay + 0.2) * fps],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <div
      style={{
        opacity,
        transform: `scale(${scale})`,
        transformOrigin: origin,
        ...style,
      }}
    >
      {children}
    </div>
  );
};
```

**사용 예시:**
```tsx
// 중앙 강조 뱃지
<PPTZoom delay={0.4}>
  <StepBadge step="핵심" />
</PPTZoom>

// 각 카드를 왼쪽 상단 기준으로 grow (Prezi 스타일)
<PPTZoom delay={0.3} origin="top left" fromScale={0.5}>
  <GlassCard>...</GlassCard>
</PPTZoom>
```

**연속 사용 시 변주:** 첫 씬 `fromScale=0, stiffness=110` (Zoom) → 다음 씬 `fromScale=0.7, stiffness=180` (Grow, 덜 극적).

**적용 가능 컴포넌트:** BigTitle, StepBadge, IconElement, CountUpNumber, ProgressRing.

---

### 4. PPTWipe — Wipe

clip-path로 좌→우(또는 임의 방향)로 마스크를 걷어내며 내용을 노출. 파워포인트 "Wipe" 효과.

**Props:**
| prop | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| children | ReactNode | (required) | 감쌀 요소 |
| direction | `'left' \| 'right' \| 'top' \| 'bottom'` | `'left'` | 쓸어내는 방향 (시작점) |
| delay | number | 0 | 시작 지연 (초) |
| durationSec | number | 0.6 | 쓸어내는 길이 (초) |
| easing | (n: number) => number | `Easing.out(Easing.cubic)` | 이징 함수 |
| style | CSSProperties | - | 외부 style |

```tsx
export const PPTWipe: React.FC<{
  children: React.ReactNode;
  direction?: "left" | "right" | "top" | "bottom";
  delay?: number;
  durationSec?: number;
  easing?: (n: number) => number;
  style?: React.CSSProperties;
}> = ({
  children,
  direction = "left",
  delay = 0,
  durationSec = 0.6,
  easing = Easing.out(Easing.cubic),
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = interpolate(
    frame,
    [delay * fps, (delay + durationSec) * fps],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing }
  );
  const pct = (1 - progress) * 100;

  // inset(top right bottom left) — 해당 변에서 마스크 시작
  const inset = {
    left: `inset(0 ${pct}% 0 0)`,
    right: `inset(0 0 0 ${pct}%)`,
    top: `inset(0 0 ${pct}% 0)`,
    bottom: `inset(${pct}% 0 0 0)`,
  }[direction];

  return (
    <div
      style={{
        clipPath: inset,
        WebkitClipPath: inset,
        ...style,
      }}
    >
      {children}
    </div>
  );
};
```

**사용 예시:**
```tsx
// 좌→우 Wipe로 제목 등장
<PPTWipe direction="left" delay={0.3} durationSec={0.7}>
  <BigTitle text="결과 공개" fontSize={88} />
</PPTWipe>

// 상→하 Wipe로 이미지 밝히기
<PPTWipe direction="top" delay={0.5}>
  <BlogImage src="result.jpg" animation="zoom-in" />
</PPTWipe>
```

**연속 사용 시 변주:** 첫 씬 `direction="left", easing=Easing.out(Easing.cubic)` → 다음 씬 `direction="top", easing=Easing.inOut(Easing.ease)` 로 방향+이징 교차.

**적용 가능 컴포넌트:** BigTitle, TerminalBlock, BlogImage, WordByWordText.

---

### 5. PPTFloat — Float / Drift

카드가 아래쪽에서 살짝 떠오르면서 blur가 해제. 파워포인트 "Float In" + "Appear" 결합.

**Props:**
| prop | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| children | ReactNode | (required) | 감쌀 요소 |
| delay | number | 0 | 시작 지연 (초) |
| driftY | number | 40 | 시작 offsetY (px) |
| fromBlur | number | 12 | 시작 blur (px) |
| durationSec | number | 0.6 | 입장 길이 (초) |
| idleFloat | boolean | true | 입장 후 sin파 플로팅 유지 여부 |
| style | CSSProperties | - | 외부 style |

```tsx
export const PPTFloat: React.FC<{
  children: React.ReactNode;
  delay?: number;
  driftY?: number;
  fromBlur?: number;
  durationSec?: number;
  idleFloat?: boolean;
  style?: React.CSSProperties;
}> = ({
  children,
  delay = 0,
  driftY = 40,
  fromBlur = 12,
  durationSec = 0.6,
  idleFloat = true,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = interpolate(
    frame,
    [delay * fps, (delay + durationSec) * fps],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.cubic),
    }
  );
  const y = interpolate(progress, [0, 1], [driftY, 0]);
  const blur = interpolate(progress, [0, 1], [fromBlur, 0]);
  const floatY = idleFloat && progress >= 1 ? Math.sin((frame / fps) * 1.6) * 4 : 0;

  return (
    <div
      style={{
        opacity: progress,
        transform: `translateY(${y + floatY}px)`,
        filter: `blur(${blur}px)`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};
```

**사용 예시:**
```tsx
// 인용 카드가 부드럽게 떠오르며 등장
<PPTFloat delay={0.4} driftY={50} fromBlur={16}>
  <TweetCard author="..." handle="..." text="..." />
</PPTFloat>
```

**연속 사용 시 변주:** 첫 씬 `driftY=40, fromBlur=12` → 다음 씬 `driftY=20, fromBlur=6, idleFloat=false` (덜 드라마틱하게).

**적용 가능 컴포넌트:** TweetCard, BlogImage, GlassCard, 인용/증언 레이아웃.

---

### 6. PPTCascade — Stack / Cascade

카드 더미가 겹쳐 있다가 하나씩 위로 펼쳐지는 효과. 파워포인트 "Cover" + 카드 덱 애니메이션.

**Props:**
| prop | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| items | ReactNode[] | (required) | 스택에 쌓을 카드들 |
| delay | number | 0 | 전체 시작 지연 (초) |
| staggerSec | number | 0.22 | 카드 간 펼침 간격 (초) |
| offsetX | number | 40 | 펼쳐진 후 수평 간격 (px) |
| rotateVariance | number | 4 | 살짝 회전 변주 (deg) |
| stackDepth | number | 8 | 쌓인 상태의 카드 간 Y 간격 (px) |
| style | CSSProperties | - | 컨테이너 style |

```tsx
export const PPTCascade: React.FC<{
  items: React.ReactNode[];
  delay?: number;
  staggerSec?: number;
  offsetX?: number;
  rotateVariance?: number;
  stackDepth?: number;
  style?: React.CSSProperties;
}> = ({
  items,
  delay = 0,
  staggerSec = 0.22,
  offsetX = 40,
  rotateVariance = 4,
  stackDepth = 8,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const n = items.length;

  return (
    <div
      style={{
        position: "relative",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        ...style,
      }}
    >
      {items.map((item, i) => {
        const cardDelay = delay + i * staggerSec;
        const prog = spring({
          frame: frame - Math.round(cardDelay * fps),
          fps,
          config: { damping: 13, stiffness: 130, mass: 0.7 },
        });
        // 쌓인 상태: 중앙에 x=0, y=stackDepth*i
        // 펼쳐진 상태: x = (i - (n-1)/2) * offsetX, y=0
        const targetX = (i - (n - 1) / 2) * offsetX;
        const x = interpolate(prog, [0, 1], [0, targetX]);
        const y = interpolate(prog, [0, 1], [i * stackDepth, 0]);
        const rot = interpolate(
          prog,
          [0, 1],
          [0, ((i % 2 === 0 ? -1 : 1) * rotateVariance * (i + 1)) / n]
        );
        const opacity = interpolate(
          frame,
          [cardDelay * fps, (cardDelay + 0.25) * fps],
          [0, 1],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
        );

        return (
          <div
            key={i}
            style={{
              position: "absolute",
              opacity,
              transform: `translate(${x}px, ${y}px) rotate(${rot}deg)`,
              zIndex: n - i,
            }}
          >
            {item}
          </div>
        );
      })}
    </div>
  );
};
```

**사용 예시:**
```tsx
<PPTCascade
  delay={0.3}
  staggerSec={0.25}
  offsetX={320}
  rotateVariance={3}
  items={[
    <GlassCard key="a" width={280}><BigTitle text="1" /></GlassCard>,
    <GlassCard key="b" width={280}><BigTitle text="2" /></GlassCard>,
    <GlassCard key="c" width={280}><BigTitle text="3" /></GlassCard>,
  ]}
/>
```

**연속 사용 시 변주:** 첫 씬 `offsetX=320, rotateVariance=4` → 다음 씬 `offsetX=0, stackDepth=14, rotateVariance=0` (수직 타워 형태)로 공간 구성을 변화.

**적용 가능 컴포넌트:** 고정폭 GlassCard 덱, BlogImage 썸네일 나열, FlipCard 팩.

---

### 7. PPTRotateIn — Flip / Rotate-In (3D)

3D rotateY/rotateX 축 회전으로 입장. 파워포인트 "Swivel" / "Flip" 효과.

> **⚠️ 중요 주의사항 (텍스트 전용 카드에 금지):**
> - **텍스트 컴포넌트에는 `rotateX` / `rotateY`를 사용하지 않는다**. Remotion/Chromium 렌더러의 CSS 3D 구현 한계로 텍스트가 반전되거나(거울상) 서브픽셀 블러가 심하게 발생한다.
> - 텍스트가 포함된 카드를 뒤집고 싶다면 `FlipCard`가 사용하는 `scaleX` 기반 2D 시뮬레이션을 쓰거나, 이 프리미티브의 `axis="Z"` 옵션(2D rotate)을 사용한다.
> - 아이콘/도형/이미지 등 심볼릭 콘텐츠에는 rotateX/Y 사용 OK.
> - (재확인) `writing-mode: vertical-*`도 텍스트 반전 버그 원인이므로 `rotate(-90deg) translate(...)` 조합을 유지한다.

**Props:**
| prop | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| children | ReactNode | (required) | 감쌀 요소 (텍스트 전용이면 `axis="Z"` 사용) |
| axis | `'X' \| 'Y' \| 'Z'` | `'Y'` | 회전 축. Z는 2D safe |
| fromDeg | number | -90 | 시작 각도 |
| delay | number | 0 | 시작 지연 (초) |
| damping | number | 13 | spring damping |
| stiffness | number | 130 | spring stiffness |
| perspective | number | 1200 | 3D 원근 (axis=X/Y일 때만) |
| style | CSSProperties | - | 외부 style |

```tsx
export const PPTRotateIn: React.FC<{
  children: React.ReactNode;
  axis?: "X" | "Y" | "Z";
  fromDeg?: number;
  delay?: number;
  damping?: number;
  stiffness?: number;
  perspective?: number;
  style?: React.CSSProperties;
}> = ({
  children,
  axis = "Y",
  fromDeg = -90,
  delay = 0,
  damping = 13,
  stiffness = 130,
  perspective = 1200,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const prog = spring({
    frame: frame - Math.round(delay * fps),
    fps,
    config: { damping, stiffness, mass: 0.7 },
  });
  const deg = interpolate(prog, [0, 1], [fromDeg, 0]);
  const opacity = interpolate(
    frame,
    [delay * fps, (delay + 0.2) * fps],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const transform3D =
    axis === "Z"
      ? `rotate(${deg}deg)`
      : `perspective(${perspective}px) rotate${axis}(${deg}deg)`;

  return (
    <div
      style={{
        opacity,
        transform: transform3D,
        transformOrigin: "center center",
        ...style,
      }}
    >
      {children}
    </div>
  );
};
```

**사용 예시:**
```tsx
// 아이콘 — rotateY OK (심볼릭)
<PPTRotateIn axis="Y" fromDeg={-90} delay={0.3}>
  <IconElement name="shield" size={120} />
</PPTRotateIn>

// 텍스트 제목 — rotateZ (2D)로 안전하게
<PPTRotateIn axis="Z" fromDeg={-15} delay={0.3} stiffness={180}>
  <BigTitle text="주의!" fontSize={80} />
</PPTRotateIn>
```

**연속 사용 시 변주:** 첫 씬 `axis="Y", fromDeg=-90` → 다음 씬 `axis="Z", fromDeg=-20, stiffness=180` (3D → 2D로 톤 다운).

**적용 가능 컴포넌트:** IconElement, MorphingShape, 원형 뱃지, BlogImage. **텍스트 카드에는 `axis="Z"`만 허용.**

---

### 8. PPTBounce — Bounce / Overshoot

spring damping을 낮춰 튕기며 착지하는 효과. 파워포인트 "Bounce" 효과.

**Props:**
| prop | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| children | ReactNode | (required) | 감쌀 요소 |
| delay | number | 0 | 시작 지연 (초) |
| fromY | number | -160 | 시작 offsetY (위에서 떨어지는 거리, px) |
| damping | number | 6 | **낮게 유지 (튕김)** |
| stiffness | number | 140 | spring stiffness |
| mass | number | 0.55 | spring mass |
| style | CSSProperties | - | 외부 style |

```tsx
export const PPTBounce: React.FC<{
  children: React.ReactNode;
  delay?: number;
  fromY?: number;
  damping?: number;
  stiffness?: number;
  mass?: number;
  style?: React.CSSProperties;
}> = ({
  children,
  delay = 0,
  fromY = -160,
  damping = 6,
  stiffness = 140,
  mass = 0.55,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const prog = spring({
    frame: frame - Math.round(delay * fps),
    fps,
    config: { damping, stiffness, mass, overshootClamping: false },
  });
  const y = interpolate(prog, [0, 1], [fromY, 0]);
  // 착지 직후 미세 스쿼시
  const squash = interpolate(prog, [0.9, 1.0, 1.08], [1, 0.94, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const opacity = interpolate(
    frame,
    [delay * fps, (delay + 0.15) * fps],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <div
      style={{
        opacity,
        transform: `translateY(${y}px) scaleY(${squash})`,
        transformOrigin: "bottom center",
        ...style,
      }}
    >
      {children}
    </div>
  );
};
```

**사용 예시:**
```tsx
// 강조 뱃지가 위에서 뚝 떨어져 튕김
<PPTBounce delay={0.4} fromY={-200} damping={5}>
  <StepBadge step="NEW" />
</PPTBounce>

// 이모지 아이콘 더 활발하게
<PPTBounce delay={0.3} damping={4} stiffness={160}>
  <div style={{ fontSize: 96 }}>🎉</div>
</PPTBounce>
```

**연속 사용 시 변주:** 첫 씬 `damping=6, fromY=-160` → 다음 씬 `damping=9, fromY=-80` (바운스 감소, 더 차분하게).

**적용 가능 컴포넌트:** StepBadge, IconElement, 이모지, CountUpNumber 결과값.

---

### 9. PPTTypewriter — Typewriter / Reveal

글자 또는 줄 단위로 순차 공개. 파워포인트 "Typewriter" + 커서 깜박임.

**Props:**
| prop | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| text | string | (required) | 공개할 텍스트 |
| unit | `'char' \| 'line'` | `'char'` | 공개 단위 |
| delay | number | 0 | 시작 지연 (초) |
| charsPerSecond | number | 30 | 초당 공개 속도 (`unit='char'`) |
| linesPerSecond | number | 3 | 초당 공개 속도 (`unit='line'`) |
| cursor | boolean | true | 깜박이는 커서 표시 여부 |
| style | CSSProperties | - | 텍스트 컨테이너 style |

```tsx
export const PPTTypewriter: React.FC<{
  text: string;
  unit?: "char" | "line";
  delay?: number;
  charsPerSecond?: number;
  linesPerSecond?: number;
  cursor?: boolean;
  style?: React.CSSProperties;
}> = ({
  text,
  unit = "char",
  delay = 0,
  charsPerSecond = 30,
  linesPerSecond = 3,
  cursor = true,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const elapsedSec = Math.max(0, (frame - delay * fps) / fps);

  let visible: string;
  let isDone: boolean;

  if (unit === "line") {
    const lines = text.split("\n");
    const shown = Math.min(
      lines.length,
      Math.floor(elapsedSec * linesPerSecond)
    );
    visible = lines.slice(0, shown).join("\n");
    isDone = shown >= lines.length;
  } else {
    const total = text.length;
    const shown = Math.min(total, Math.floor(elapsedSec * charsPerSecond));
    visible = text.slice(0, shown);
    isDone = shown >= total;
  }

  // 커서 깜박임 (0.5Hz)
  const cursorOpacity =
    cursor && (!isDone || Math.floor(frame / (fps * 0.5)) % 2 === 0) ? 1 : 0;

  return (
    <span
      style={{
        fontFamily: "'CookieRun', sans-serif",
        whiteSpace: "pre-wrap",
        ...style,
      }}
    >
      {visible}
      {cursor && (
        <span
          style={{
            display: "inline-block",
            width: "0.5em",
            marginLeft: 2,
            opacity: cursorOpacity,
            color: "currentColor",
          }}
        >
          ▍
        </span>
      )}
    </span>
  );
};
```

**사용 예시:**
```tsx
// 제목을 타자기처럼 타이핑
<PPTTypewriter
  text="Hello, World!"
  delay={0.3}
  charsPerSecond={20}
  style={{ fontSize: 64, fontWeight: 900, color: "#1e293b" }}
/>

// 여러 줄 순차 공개 (코드/시)
<PPTTypewriter
  text={"line 1\nline 2\nline 3"}
  unit="line"
  linesPerSecond={2}
  cursor={false}
  style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 28 }}
/>
```

**연속 사용 시 변주:** 첫 씬 `unit="char", charsPerSecond=30, cursor=true` → 다음 씬 `unit="line", linesPerSecond=3, cursor=false` (라인 단위로 전환).

**적용 가능 컴포넌트:** BigTitle 대체, TerminalBlock의 라인 공개, 자막 스타일 서브타이틀.

---

### PPT 프리미티브 사용 원칙 요약

| 프리미티브 | 한 줄 역할 | 대표 사용처 |
|-----------|-----------|------------|
| `PPTFlyIn` | 좌/우/상/하 spring 슬라이드 | 카드, 뱃지, 사이드 패널 |
| `PPTFadeSequential` | 항목 순차 페이드 + 살짝 lift | 불릿 리스트, 이미지 나열 |
| `PPTZoom` | 중앙(또는 지정 origin)에서 grow | 강조 제목, 뱃지, KPI |
| `PPTWipe` | clip-path로 마스크 쓸기 | 제목, 이미지, 대제목 reveal |
| `PPTFloat` | blur + lift 해제하며 떠오름 | 인용, 증언, 부드러운 제품컷 |
| `PPTCascade` | 스택 덱이 하나씩 펼쳐짐 | 카드 덱, 단계 미리보기 |
| `PPTRotateIn` | 3D/2D 회전 입장 (텍스트는 axis="Z") | 아이콘, 로고, 심볼 |
| `PPTBounce` | 낮은 damping으로 튕기며 착지 | 축하, "NEW" 뱃지, 임팩트 |
| `PPTTypewriter` | 글자/줄 단위 타이핑 reveal | 제목 훅, 코드, 대사 |

**조합 규칙:**
- 한 씬에 **최대 2종**의 PPT 프리미티브만 섞는다 (과용 시 산만).
- `staggered-cards` 씬 내부라면: 각 카드를 `PPTFlyIn direction 교차` + 제목은 `PPTWipe` 정도로 제한.
- `delay` 설정 시 Section의 subtitle 타이밍, TimedSubtitle 세그먼트와 충돌하지 않도록 `0.2~0.5`초 사이로 유지.
- 다이버시티 예산에는 카운트되지 않으므로(visual 타입 분포 무관), 자유롭게 재사용 가능하다.

---

## 자막 싱크 하이라이트 (Narration-Synced Highlights)

**배경**: 긴 씬에서 내레이션이 "1단계… 2단계… 3단계…" 혹은 "첫째… 둘째… 셋째…"처럼 순차 개념을 열거할 때, 화면의 각 항목이 **해당 내레이션 문장이 시작하는 순간 하이라이트**되면 이해도가 눈에 띄게 올라간다. TimedSubtitle의 문장 경계 로직을 재사용하여 UI 요소에 동일한 타이밍 훅을 적용하는 패턴.

### 공통 로직 (sentence timing helper)

```tsx
// narration을 `.?!` 단위로 분할하고, 각 문장의 시작 프레임을 계산한다.
// TimedSubtitle과 동일한 로직 — subtitleStartsSec가 있으면 그것을 우선 사용,
// 없으면 narrationTts(또는 narration) 문자수 비율로 배분.
function useSentenceStarts(
  narration: string,
  audioDurationSec: number,
  fps: number,
  narrationTts?: string,
  subtitleStartsSec?: number[],
): number[] {
  const splitRe = /(?<=[.?!。])(?!\S)\s*/;
  const display = narration.split(splitRe).map(s => s.trim()).filter(Boolean);

  if (subtitleStartsSec && subtitleStartsSec.length === display.length) {
    return subtitleStartsSec.map(s => Math.round(s * fps));
  }
  const basisRaw = narrationTts ?? narration;
  const basis = basisRaw.split(splitRe).map(s => s.trim()).filter(Boolean);
  const use = basis.length === display.length ? basis : display;
  const total = use.reduce((s, x) => s + x.length, 0);
  const starts: number[] = [];
  let cum = 0;
  for (const s of use) {
    starts.push(Math.round((cum / total) * audioDurationSec * fps));
    cum += s.length;
  }
  return starts;
}
```

### SetupStepsSynced — 순차 하이라이트 4카드 (1·2·3·4단계)

모든 카드가 **초반에 한꺼번에 등장**하고, 이후 "1단계/2단계/…" 문장 시작에서 해당 카드가 **scale 1.04 + border 2.5px + glow**로 순차 활성화. 사라지지는 않음 (이전 단계가 "완료" 느낌으로 남음).

```tsx
const SetupStepsSynced: React.FC<{ scene: SceneData }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const starts = useSentenceStarts(
    scene.narration, scene.audioDurationSec, fps,
    scene.narrationTts, scene.subtitleStartsSec,
  );
  // 트리거 문장 인덱스 찾기: "1단계", "2단계", ... 포함 문장
  const steps = scene.narration.split(/(?<=[.?!。])(?!\S)\s*/);
  const triggers = [1, 2, 3, 4].map(n =>
    steps.findIndex(s => s.includes(`${n}단계`))
  );
  // 각 카드 active state = 해당 문장 start 이후 프레임
  const isActive = (i: number) => frame >= starts[triggers[i]];
  // ... 4개 카드 렌더, active일 때 스타일 강조
};
```

### CritiqueChecklistSynced — 순차 체크리스트 3항목 (첫째·둘째·셋째)

"비판 세 가지" 같은 씬에서 체크박스 3개가 초반 등장 후 "첫째…/둘째…/셋째…" 트리거에 맞춰 순차 체크됨.

```tsx
const CritiqueChecklistSynced: React.FC<{ scene: SceneData }> = ({ scene }) => {
  // 트리거 키워드: "첫째", "둘째", "셋째"
  const starts = useSentenceStarts(/* ... */);
  const triggers = ["첫째", "둘째", "셋째"].map(k =>
    scene.narration.split(/(?<=[.?!。])(?!\S)\s*/).findIndex(s => s.includes(k))
  );
  // 각 아이템 "체크" 상태 = frame >= starts[triggers[i]]
};
```

### 트리거 규약

- **순차 번호**: `"1단계"`·`"2단계"` 또는 `"첫째"`·`"둘째"`·`"셋째"` 문자열 포함 여부로 판정
- **키워드 기반**: 배선 다이어그램 같은 경우 `"파일로 두는"` → 노드 A, `"MCP 서버를 띄"` → 노드 B 식으로 명시적 매핑 (McpWiring 참고)
- **트리거 없는 경우**: `starts[i]` 전체를 균등 분배 (카드 수와 문장 수가 같다고 가정)

### 언제 쓰나

- "N단계 프로세스" 설명 씬 (셋업, 설치, 체크리스트)
- "세 가지 위험/장점/차이" 열거 씬
- 배선 다이어그램 / 아키텍처 다이어그램에서 설명 순서에 맞게 노드/엣지 강조
- **쓰지 말아야 할 곳**: 내레이션이 자유 서술형이라 문장별 트리거 포인트를 뽑을 수 없는 씬 (일반 StepBadge + 초반 입장 애니메이션이 더 안전)

### 짝: TimedSubtitle의 `subtitleStartsSec`

정확한 싱크가 필요하면 TimedSubtitle의 `subtitleStartsSec`을 채워둔 뒤, 같은 씬의 하이라이트 컴포넌트도 동일한 배열을 쓰게 만들면 **자막과 하이라이트가 동일한 프레임에 정렬**된다. wav silence gap 측정으로 산출하는 방식은 TimedSubtitle 섹션 참고.

---

## iPad 제약에 맞춘 축소 스펙 (iPad Overflow Compensation)

**배경**: IPadTemplate에 대칭 패딩(`paddingTop: 90, paddingBottom: 90`)과 inner `scale(1.15)`를 적용하면, 콘텐츠가 차지할 수 있는 세로 실영역은 **약 720px**. 외부 StepBadge/BigTitle 등 부속 요소 40~60px을 빼면 **핵심 비주얼은 약 660~680px 이내**로 들어가야 한다. 자막은 스크린 하단 가장자리(`bottom: 12`, 높이 ~72px)에 밀착되므로 콘텐츠 하단(y=912)과 자막 상단이 맞닿는다. 기본 크기가 이를 넘는 다이어그램은 아래 래퍼 패턴으로 축소한다.

### 범용 축소 래퍼 패턴

```tsx
<div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12 }}>
  <StepBadge step="..." color="..." />
  <div
    style={{
      transform: "scale(S)",
      transformOrigin: "center center",   // 절대 top center 쓰지 말 것 — 상단 쏠림 + 자막과 멀어짐
      marginTop: -M,
      marginBottom: -M,                   // M = 원본높이 × (1 - S) / 2
    }}
  >
    <HeavyDiagram {...props} />
  </div>
</div>
```

- **전제**: `HeavyDiagram`은 외곽에 고정 `width/height`를 갖는 SVG 기반 컴포넌트 (ReActLoopDiagram, QuadrantMatrix, HorseHarnessDiagram, RocketTrajectory, LethalTriangle, AnimatedPieChart 등)
- **transformOrigin**: 반드시 `"center center"`. `"top center"`로 하면 콘텐츠가 위로 쏠려 하단이 비고 자막과 간격이 벌어진다 (실제로 본 프로젝트에서 사용자 지적으로 수정한 이슈)
- **marginTop/Bottom**: `(원본높이 × (1 - scale)) / 2` — 대칭 음수 마진으로 레이아웃 플로우를 원본 높이 시절과 동일하게 유지한다. 한쪽만 적용하거나 비대칭으로 두면 세로 정렬이 깨진다
- **scale 하한**: 0.7 미만으로 내리면 텍스트 가독성이 깨진다. 더 줄여야 하면 컴포넌트 자체 스펙(아래)을 수정

### 검증된 축소 스펙 — 본 시그니처/제네릭 패턴

다음 수치는 2026-04-22 기준 iPad(`paddingTop: 90, paddingBottom: 90` 대칭 + inner `scale(1.15)`) 조합에서 실측 확정된 값이다. 콘텐츠 실 영역 높이 ≈720px, 자막은 스크린 하단 가장자리(`bottom: 12`).

| visual | 컴포넌트 | 원본 크기 | scale | margin (±) | 외곽 gap | 비고 |
|---|---|---|---|---|---|---|
| `react-loop` | ReActLoopDiagram | 1400×800 | **0.82** | 72 | 16 | StepBadge 포함 총 ≈712px |
| `quadrant-matrix` | QuadrantMatrix | 1200×700 | **0.9** | 36 | 12 | StepBadge 포함 총 ≈682px |
| `horse-harness` | HorseHarnessDiagram | 1200×700 | 0.9 권장 | 36 | 12 | Quadrant와 동일 기준 적용 가능 |
| `lethal-triangle` | LethalTriangle | 1200×800 | 0.82 | 72 | 12 | ReActLoop와 동일 기준 |
| `rocket-trajectory` | RocketTrajectory | 1400×700 | 필요 시 0.9 | 36 | 12 | — |

> 참고: scale·margin은 상한 기준이다. StepBadge나 추가 텍스트가 없어 부속 요소가 작다면 scale을 높여 그대로 써도 무방하다. **항상 Remotion Studio에서 프리뷰로 검증할 것.**

### 컴팩트화 스펙 — TimelineCards (세로 스택형)

`TimelineCards`는 step 수에 따라 높이가 선형 증가하므로 scale 대신 **컴포넌트 내부 스타일을 컴팩트 버전으로 변경**한다. 5개 스텝 기준 700px → 560px:

| 속성 | 원본 | 컴팩트 |
|---|---|---|
| 행 `padding` | `14px 0` | `6px 0` |
| 카드 `padding` | `"22px 26px"` | `"12px 18px"` |
| 카드 `borderRadius` | 18 | 14 |
| 아이콘 박스 크기 | 40 | 32 |
| 아이콘 `borderRadius` | 12 | 10 |
| 아이콘 `fontSize` | 20 | 17 |
| 제목 `fontSize` | 24 | 20 |
| 설명 `fontSize` | 17 | 14 |
| 헤더 `marginBottom` | 10 | 4 |
| `gap` (헤더 아이콘↔제목) | 14 | 12 |
| 씬 외곽 gap (StepBadge↔Timeline) | 20 | 8 |

6개 이상 스텝일 경우 범용 scale 래퍼(scale 0.85)와 병행하거나 스텝을 4~5개로 요약할 것.

### 조립 시 체크리스트

vp-video-composer가 씬 조립 후 반드시 수행:

1. `scene_plan.json`의 각 씬에서 visual이 위 표의 **축소 필요 패턴**에 해당하는지 확인
2. 해당하면 위 스펙대로 래퍼/컴팩트화 적용
3. Remotion Studio 프리뷰에서 각 씬이 iPad 프레임 위·아래로 벗어나지 않는지, 하단 자막과 겹치지 않는지 시각 검증
4. 새로운 헤비 다이어그램을 추가한다면 **컴포넌트 높이를 실측**한 뒤 수식 `M = H × (1 - S) / 2`로 마진 계산


---

## 긴 씬의 시간차 전개 패턴 (Long-Scene Stage Reveal)

**배경**: 한 씬 길이가 18초를 넘거나 narration에 정보 블록이 4개 이상 있으면, 비주얼이 처음부터 끝까지 고정되어 있을 때 **"정적으로 길게 떠 있다"**는 체감이 생긴다. 해결책은 narration 문장 구조와 맞춰 내부 요소가 **순차 등장·강조**되도록 구성하는 것.

### 적용 조건 (vp-video-composer가 자동 판별)

다음 중 **하나라도** 해당하면 스테이지 전개 패턴 적용:
1. `durationSec >= 18`
2. narration이 `.?!。`로 분리했을 때 **4개 문장 이상**
3. visual이 `glass-card`·`default-scene`·단일 `big-title` 등 **정적 카드 계열**

### Stage Reveal 템플릿

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring, Easing } from "remotion";

export const SceneNReveal: React.FC<{ delay?: number }> = ({ delay = 0.2 }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = Math.max(0, frame - delay * fps);
  const sec = t / fps;

  // 씬 전체 길이 대비 비율로 스테이지 분할 (N개 스테이지)
  const dur = (durationInFrames - delay * fps) / fps;
  const stages = [
    0,            // Stage 1 (타이틀) — 0부터
    dur * 0.22,   // Stage 2
    dur * 0.48,   // Stage 3
    dur * 0.78,   // Stage 4 (핵심 CTA/URL)
  ];

  const fadeInAt = (startSec: number, rampSec = 0.35) =>
    interpolate(sec, [startSec, startSec + rampSec], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.cubic),
    });

  const springAt = (startSec: number) =>
    spring({
      frame: Math.round((sec - startSec) * fps),
      fps,
      config: { damping: 14, stiffness: 110, mass: 0.7 },
    });

  return (
    <Container>
      {/* Stage 1: 타이틀 — 항상 보여짐, 누적 배치 (사라지지 않음) */}
      <Title opacity={fadeInAt(stages[0])} scale={springAt(stages[0])} />

      {/* Stage 2: slide-up + fade-in */}
      <Badges opacity={fadeInAt(stages[1])} ty={interpolate(fadeInAt(stages[1]), [0,1], [12, 0])} />

      {/* Stage 3: 다중 요소 개별 stagger (0.15초 간격) */}
      {items.map((item, i) => (
        <Item key={i} op={fadeInAt(stages[2] + i * 0.15, 0.25)} />
      ))}

      {/* Stage 4: 핵심 요소 강조 — glow 맥동 + 커서 깜빡임 */}
      <CTA
        opacity={fadeInAt(stages[3])}
        glow={0.3 + Math.sin(sec * 3.2) * 0.15}
        cursorOn={Math.floor(sec * 1.6) % 2 === 0}
      />
    </Container>
  );
};
```

### 설계 원칙

1. **누적 배치**: 새 스테이지 등장 시 이전 요소 **사라지지 않음** — 정보가 쌓이는 느낌
2. **마지막 스테이지는 CTA/핵심 정보** — URL, 접속 방법, 가격 등 행동 유도 요소를 맨 끝에 배치해 시청자 기억에 남김
3. **강조 연출 디테일**:
   - glow 맥동: `0.3 + Math.sin(sec * 3.2) * 0.15` (호흡 효과)
   - 커서 깜빡임: `Math.floor(sec * 1.6) % 2 === 0` (타이핑 메타포)
   - 모노스페이스 폰트 (JetBrains Mono): URL/코드 강조 시 사용
4. **narration 동기화**: 스테이지 구분점을 **narration 문장 경계**에 맞추면 자연스러움
5. **stage 수 가이드**: narration 문장 수에 맞춰 **3~5개** (너무 많으면 정신없음)

### 적용 예시 — 씬 3 "협업형 비주얼 디자인 도구 발표" (23.3초)

| Stage | 시간 | 내용 | 연출 |
|---|---|---|---|
| 1 | 0~5s | Anthropic 로고 + 타이틀 | spring 입장 (scale 0.92→1) |
| 2 | 5~11s | 공개일·프리뷰 배지 | 아래→위 slide-up |
| 3 | 11~18s | Pro·Max·Team·Enterprise 4개 순차 | 개별 spring (0.15s 간격) |
| 4 | 18~23s | claude.ai/design URL 강조 | glow 맥동 + 커서 깜빡임 + JetBrains Mono |

### 안티패턴

- 스테이지마다 **이전 요소 제거** — 시청자가 직전 정보를 따라잡기 어려움
- **모든 요소를 동시 입장** — 스테이지 분할 의미 없음 (=기존 정적 카드와 동일)
- **스테이지 5개 이상** — 긴 씬이라도 5개를 넘으면 전환이 산만해짐. 대신 각 스테이지 시간을 늘리는 방향
- **마지막 스테이지가 정보 요약** — CTA/핵심 숫자/URL 같은 **기억에 남을 요소**를 배치해야 함


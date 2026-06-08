// 9:16 Shorts template — 1080×1920 @ 30fps
// 시그니처 요소 3종 베이스: 카라오케 자막 + BGM 없음 + 상단 프로그레스 바
// 레퍼런스: claude-opensource-video/src/ShortCaveman.tsx
//
// 사용법:
//   1. SCENES 배열에 씬 데이터 채워넣기 (각 씬: section, narration, audioSrc, durationSec, content 컴포넌트)
//   2. content는 React.FC<{ frame: number }> 형태로 씬별 시각 요소를 렌더
//   3. Root.tsx에 Composition 등록 (id="Short", durationInFrames=TOTAL_FRAMES, 1080×1920)
//
// ⚠️ BGM은 절대 추가하지 말 것 (자동재생 무음 시청 대응)

import React, { useMemo } from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export const FPS = 30;

// ---------- 씬 데이터 ----------
// 컴포저가 채워넣는다. content는 씬별 시각 요소.

export type ShortSection = {
  /** 섹션 라벨 (예: "뭐 하는 도구?") — SectionLabel chip에 표시 */
  label: string;
  /** 섹션 색상 (주황 #f59e0b, 파랑 #3b82f6, 초록 #10b981 권장) */
  color: string;
};

export type ShortScene = {
  section: ShortSection;
  /** 자막 원문 (TTS narration과 동일하거나 변형) */
  narration: string;
  /** public/audio/<src> — 본편 TTS 재활용 또는 신규 */
  audioSrc: string;
  /** 씬 길이 (초). 모든 씬 합이 40~60s 권장 */
  durationSec: number;
  /** 씬별 시각 요소. AbsoluteFill 내부에 자유 배치 */
  Content: React.FC;
};

// 컴포저가 SCENES만 교체. 나머지 구조는 변경 금지.
export const SCENES: ShortScene[] = [
  // 예시: WHAT
  // {
  //   section: { label: "뭐 하는 도구?", color: "#f59e0b" },
  //   narration: "...",
  //   audioSrc: "seg_02.wav",
  //   durationSec: 9.4,
  //   Content: WhatSection,
  // },
];

const TOTAL_SEC = SCENES.reduce((sum, s) => sum + s.durationSec, 0);
export const TOTAL_FRAMES = Math.round(TOTAL_SEC * FPS);

const BG = "linear-gradient(180deg, #0b1120 0%, #1e293b 50%, #0b1120 100%)";

// ---------- 메인 컴포넌트 ----------

export const Short: React.FC = () => {
  let cursor = 0;
  return (
    <AbsoluteFill style={{ background: BG }}>
      {/* 상단 라디얼 액센트 */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at top, rgba(245,158,11,0.12) 0%, transparent 55%)",
        }}
      />

      {SCENES.map((scene, i) => {
        const frames = Math.round(scene.durationSec * FPS);
        const start = cursor;
        cursor += frames;
        return (
          <Sequence key={i} from={start} durationInFrames={frames}>
            {/* 섹션 라벨 칩 (각 씬 상단) */}
            <SectionLabelOverlay
              text={scene.section.label}
              color={scene.section.color}
            />
            {/* 씬 본문 */}
            <scene.Content />
            {/* 카라오케 자막 (시그니처) */}
            <ShortsSubtitle
              narration={scene.narration}
              durationInFrames={frames}
            />
            {/* TTS 오디오 */}
            <SceneAudio src={scene.audioSrc} durationFrames={frames} />
          </Sequence>
        );
      })}

      {/* 상단 프로그레스 바 (시그니처) */}
      <ProgressBar />
    </AbsoluteFill>
  );
};

// ---------- 시그니처 컴포넌트 (변경 금지) ----------

const SectionLabelOverlay: React.FC<{ text: string; color: string }> = ({
  text,
  color,
}) => (
  <div
    style={{
      position: "absolute",
      top: 90,
      left: 0,
      right: 0,
      display: "flex",
      justifyContent: "center",
      zIndex: 80,
    }}
  >
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        padding: "14px 32px",
        background: `${color}22`,
        border: `2px solid ${color}`,
        borderRadius: 999,
        color,
        fontSize: 36,
        fontWeight: 900,
        fontFamily: "'CookieRun', sans-serif",
        letterSpacing: "-0.02em",
      }}
    >
      {text}
    </div>
  </div>
);

const ShortsSubtitle: React.FC<{
  narration: string;
  durationInFrames: number;
}> = ({ narration, durationInFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const segments = useMemo(() => {
    const TARGET = 14;
    const MAX = 20;
    const words = narration
      .replace(/\s+/g, " ")
      .trim()
      .split(/(?<=[.,?!。、·:;])\s+|\s+/);

    const chunks: string[] = [];
    let buf = "";
    for (const w of words) {
      if (!w) continue;
      const next = buf ? buf + " " + w : w;
      if (next.length >= TARGET && buf.length > 0) {
        chunks.push(buf);
        buf = w;
      } else if (next.length > MAX) {
        if (buf) chunks.push(buf);
        buf = w;
      } else {
        buf = next;
      }
    }
    if (buf) chunks.push(buf);
    if (chunks.length === 0) return [];

    const totalChars = chunks.reduce((sum, c) => sum + c.length, 0);
    let cursor = 0;
    return chunks.map((text) => {
      const ratio = text.length / totalChars;
      const segDur = Math.round(ratio * durationInFrames);
      const seg = { text, start: cursor, end: cursor + segDur };
      cursor += segDur;
      return seg;
    });
  }, [narration, durationInFrames]);

  const current = segments.find((s) => frame >= s.start && frame < s.end);
  if (!current) return null;

  const FADE = Math.min(Math.round(0.18 * fps), 6);
  const opIn = interpolate(
    frame,
    [current.start, current.start + FADE],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  const opOut = interpolate(
    frame,
    [current.end - FADE, current.end],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  const opacity = Math.min(opIn, opOut);

  return (
    <div
      style={{
        position: "absolute",
        bottom: 400,
        left: 40,
        right: 40,
        display: "flex",
        justifyContent: "center",
        zIndex: 90,
        pointerEvents: "none",
        opacity,
      }}
    >
      <div
        style={{
          background: "rgba(0, 0, 0, 0.82)",
          backdropFilter: "blur(12px)",
          borderRadius: 18,
          padding: "22px 36px",
          border: "1px solid rgba(255, 255, 255, 0.1)",
          maxWidth: 980,
        }}
      >
        <KaraokeText
          text={current.text}
          start={current.start}
          end={current.end}
          frame={frame}
        />
      </div>
    </div>
  );
};

const KaraokeText: React.FC<{
  text: string;
  start: number;
  end: number;
  frame: number;
}> = ({ text, start, end, frame }) => {
  const progress = Math.max(
    0,
    Math.min(1, (frame - start) / Math.max(1, end - start)),
  );
  const lead = 0.04;
  const readPos = Math.min(1, progress + lead) * text.length;

  const tokens: { text: string; startChar: number; endChar: number }[] = [];
  {
    let cursor = 0;
    const parts = text.split(/(\s+)/);
    for (const p of parts) {
      tokens.push({ text: p, startChar: cursor, endChar: cursor + p.length });
      cursor += p.length;
    }
  }

  return (
    <div
      style={{
        fontSize: 44,
        fontFamily: "'CookieRun', sans-serif",
        fontWeight: 600,
        letterSpacing: "-0.02em",
        lineHeight: 1.35,
        textShadow: "0 2px 8px rgba(0,0,0,0.6)",
      }}
    >
      {tokens.map((tok, i) => {
        const isWhitespace = /^\s+$/.test(tok.text);
        const active =
          !isWhitespace &&
          readPos >= tok.startChar &&
          readPos < tok.endChar;
        return (
          <span
            key={i}
            style={{
              color: active ? "#fbbf24" : "#fff",
              textShadow: active
                ? "0 0 14px rgba(251,191,36,0.7), 0 2px 8px rgba(0,0,0,0.6)"
                : "0 2px 8px rgba(0,0,0,0.6)",
              transition: "color 80ms linear",
              whiteSpace: "pre",
            }}
          >
            {tok.text}
          </span>
        );
      })}
    </div>
  );
};

const SceneAudio: React.FC<{ src: string; durationFrames: number }> = ({
  src,
  durationFrames,
}) => (
  <Audio
    src={staticFile(`audio/${src}`)}
    volume={(f) => {
      const fadeFrames = Math.round(0.1 * FPS);
      if (f < fadeFrames) return f / fadeFrames;
      if (f > durationFrames - fadeFrames)
        return Math.max(0, (durationFrames - f) / fadeFrames);
      return 1;
    }}
  />
);

const ProgressBar: React.FC = () => {
  const frame = useCurrentFrame();
  const pct = Math.min(1, frame / TOTAL_FRAMES);
  return (
    <div
      style={{
        position: "absolute",
        top: 40,
        left: 40,
        right: 40,
        height: 6,
        borderRadius: 3,
        background: "rgba(255,255,255,0.1)",
        overflow: "hidden",
        zIndex: 100,
      }}
    >
      <div
        style={{
          width: `${pct * 100}%`,
          height: "100%",
          background: "linear-gradient(90deg, #f59e0b, #fbbf24)",
          boxShadow: "0 0 12px rgba(251,191,36,0.5)",
        }}
      />
    </div>
  );
};

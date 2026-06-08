---
name: video-production
description: |
  사용자가 직접 녹음한 wav를 받아 Remotion 기반 YouTube 영상으로 자동 조립하는 오케스트레이터 스킬.
  콘텐츠 기획·씬 분할·녹음 가이드는 content-production이 끝낸 상태를 전제로 한다.
  wav 정규화 → timing 측정 → 모션 디자인(선택) → Remotion 조립 → Studio 프리뷰 → 사용자 승인 → 최종 렌더까지 처리한다.
  "영상 제작", "비디오 제작", "영상 만들어줘", "녹음 끝났어 영상 만들어", "스크립트를 영상으로", "video production",
  "팀으로 영상 만들어줘", "하네스로 영상 제작" 등을 요청하면 이 스킬을 사용한다.
  단일 에이전트로 빠르게 만들고 싶으면 create-youtube 스킬을 사용할 것.
---

# YouTube 영상 제작 오케스트레이터

사용자 직접 녹음 wav를 입력으로 받아 Remotion 영상까지 조립하는 오케스트레이터.

## 전제 조건

이 스킬은 다음 산출물이 모두 준비된 상태에서 시작한다 (content-production이 만들어준 상태):

| 파일 | 만든 주체 |
|------|----------|
| `<project>/script/02_writer_script.md` | cp-script-writer |
| `<project>/_workspace/scene_plan.json` | cp-scene-architect |
| `<project>/_workspace/visual_allocation_audit.md` | cp-scene-architect |
| `<project>/_workspace/recording_guide.md` | content-production Phase 7 |
| `<project>/_workspace/audio/seg-NN.wav` | **사용자 직접 녹음** |

위 중 하나라도 빠져있으면 사용자에게 보고 후 적절한 단계로 안내한다 (대부분 `/content-production` 호출 또는 녹음 안내).

## 팀 구성

| 에이전트 | 역할 | 스킬 | Phase |
|---------|------|------|-------|
| (오케스트레이터) | wav 정규화 + timing 측정 | — | 1 |
| (오케스트레이터) | Audio Sync (멱등) | — | 2 |
| vp-motion-designer | 모션 패턴 설계/개선 (Remotion MCP) | remotion-assembly | 2.5 (선택) |
| vp-video-composer | Remotion 조립/렌더링 | remotion-assembly | 3-4 |

씬 분할(scene-analysis) + 음성 생성(voice-production)은 더 이상 video-production이 담당하지 않는다 — 각각 content-production 팀과 사용자가 책임.

## 컴포넌트 패턴 레퍼런스

| 파일 | 역할 | 주 사용자 |
|------|------|----------|
| `~/.claude/skills/remotion-assembly/references/pattern-catalog.md` | 선택용 (cp-scene-architect가 이미 사용) | (참고) |
| `~/.claude/skills/remotion-assembly/references/component-patterns.md` | 구현용 — 전체 패턴의 구현 코드 + props 스펙 | vp-video-composer, vp-motion-designer |

cp-scene-architect가 visual을 선택해서 scene_plan.json에 기록해 둔 상태이므로 video-production은 **구현만** 한다.

## 워크플로우

### Phase 0: 전제 조건 검증 + sync QA

진입 전에 `/content-qa` 호출 권장 — content-production 산출물(script, scene_plan, recording_guide)과 사용자 녹음(audio/)이 모두 sync된 상태인지 9개 layer 검증.

```bash
python3 ~/.claude/skills/content-qa/scripts/check_sync.py <project>
# FAIL이면: python3 ~/.claude/skills/content-qa/scripts/check_sync.py <project> --apply
```

특히 다음 위반은 video-production 진입 전 반드시 해결:
- Layer 6 (audio 누락) — 녹음 보강 필요
- Layer 1 (script ↔ scene_plan narration) — `--apply`로 자동 동기화
- Layer 2 (씬 개수 불일치) — `/content-production` Phase 6 재실행

상세: `~/.claude/skills/content-qa/SKILL.md`



오케스트레이터가 직접 다음을 확인:

```bash
cd <project>
required_files=(
    "script/02_writer_script.md"
    "_workspace/scene_plan.json"
    "_workspace/recording_guide.md"
)
for f in "${required_files[@]}"; do
    if [ ! -f "$f" ]; then
        echo "[FATAL] $f 누락 — /content-production 먼저 실행 필요"
        exit 1
    fi
done

if [ ! -d "_workspace/audio" ] || [ -z "$(ls -A _workspace/audio/seg-*.wav 2>/dev/null)" ]; then
    echo "[FATAL] _workspace/audio/seg-NN.wav 녹음 파일 없음"
    echo "  → recording_guide.md 보고 Audacity로 녹음하세요"
    exit 1
fi
```

폴더 구조 확인/생성:
```
<project>/
├── script/
├── thumbnail/
├── voice/
├── image/
├── output/
├── music/                          ← BGM (선택)
└── _workspace/
    ├── scene_plan.json
    ├── recording_guide.md
    ├── audio/                      ← 사용자 녹음 wav (입력)
    ├── tts/                        ← 정규화된 wav (Phase 1 산출)
    └── timing.json                 ← Phase 1 산출
```

### Phase 1: wav 정규화 + 타이밍 측정 (오케스트레이터 직접)

사용자 녹음(`_workspace/audio/seg-NN.wav`)은 어떤 샘플레이트/채널/비트심도여도 허용. 오케스트레이터가 표준 포맷으로 일괄 변환한다.

**1-A. wav 정규화**

```bash
cd <project>
~/.claude/skills/video-production/scripts/normalize_recordings.sh .
```

수행 내용:
- `_workspace/audio/seg-NN.wav` (사용자 녹음, 어떤 sr/ch/bits 든) →
- `_workspace/tts/seg_NN.wav` (24kHz / mono / 16-bit PCM)
- 앞부분 무음 trim (-50dB 이하 0.1s+) + 100ms 패딩
- 끝부분 자연 감쇠 보존 (의도적으로 trim 안 함)
- 파일명 정규화: `seg-01.wav` → `seg_01.wav` (scene_plan.json id 매칭)

**검증**:
- 출력 파일 수 = scene_plan.json 씬 수
- 각 wav: 24000Hz / mono / 16-bit (스크립트 내부 검증)

**1-B. 타이밍 측정**

```bash
cp ~/.claude/skills/video-production/scripts/generate_timing.py <project>/generate_timing.py
cd <project>
python3 generate_timing.py
```

산출: `_workspace/timing.json` (씬당 startSec, durationSec, audioDuration, subtitle, narration)

**PADDING_SEC=0.3 디폴트** — 사람 직접 녹음 + narration only 영상에 맞춰진 표준값. TTS 합성과 달리 사람 녹음은 씬 간 톤·볼륨 미세 편차 때문에 0.6초 패딩이 답답하게 들린다는 사용자 피드백 누적 결과 (claude-vs-codex 프로젝트 §10.4 검증).

**미세 조정**: 답답하면 0.4, 너무 빠르면 0.2. timing.json 재생성 → Phase 2 audio sync → Studio 핫리로드.

**검증**:
- `_workspace/timing.json` 존재 + 유효 JSON
- 씬 수 일치 (scene_plan.json과 동일)
- exit code 0 (누락 wav 없음)

### Phase 2: Audio Sync (오케스트레이터 직접, 멱등)

⚠️ **이 단계는 wav가 갱신될 때마다 무조건 실행한다.** 누락 시 Remotion이 옛 음성을 재생하는 사일런트 버그 (graphrag 프로젝트 2026-05-03 사고).

**Remotion 프로젝트 디렉터리 탐지**: `<project>/*-video/` 패턴.

```bash
cd <project>
REMOTION_DIR=$(ls -d *-video 2>/dev/null | head -1)

if [ -z "$REMOTION_DIR" ]; then
  echo "[Phase 2] Remotion 프로젝트 미생성 — Phase 3 이후 재동기화 필요"
else
  mkdir -p "$REMOTION_DIR/public/audio"
  cp _workspace/tts/seg_*.wav "$REMOTION_DIR/public/audio/"
  cp _workspace/timing.json "$REMOTION_DIR/public/audio/timing.json"
  if [ -f update_scenes_ts.py ]; then
    python3 update_scenes_ts.py
  fi
  echo "[Phase 2] Audio sync 완료"
fi
```

**검증**:
- `<remotion>/public/audio/seg_XX.wav` 파일 길이 = `_workspace/tts/seg_XX.wav`
- `<remotion>/public/audio/timing.json` 과 `_workspace/timing.json` identical
- `scenes.ts`의 `audioDurationSec` 오차 0.05s 이내

**최초 실행 케이스**: Remotion 프로젝트가 아직 없으면 이 단계 skip. Phase 3 완료 후 자동 재실행됨.

### Phase 2.5: 모션 디자인 개선 (선택적)

사용자가 모션 그래픽 개선을 요청한 경우에만 실행. 기본 파이프라인에서는 건너뛴다.

```
Agent(
  description: "모션 패턴 설계/개선",
  prompt: "~/.claude/agents/vp-motion-designer.md를 읽고 역할을 수행하라.
    ~/.claude/skills/remotion-assembly/SKILL.md를 참조한다.
    프로젝트 경로: <project>
    Remotion MCP로 API를 조회하여 모션 패턴을 개선/확장하라.
    기존 패턴: ~/.claude/skills/remotion-assembly/references/component-patterns.md
    씬 구조: <project>/_workspace/scene_plan.json
    Remotion 프로젝트: <project>/<project-name>-video/
    개선 대상: [사용자 지정 또는 전체 스캔]
    새 패턴은 Remotion Studio에서 프리뷰 확인 후 component-patterns.md에 반영하라.",
  model: "opus"
)
```

**트리거**: "모션 개선", "애니메이션 개선", "모션 패턴 추가" 같은 명시적 요청.

### Phase 3: 영상 조립 (vp-video-composer)

```
Agent(
  description: "Remotion 영상 조립",
  prompt: "~/.claude/agents/vp-video-composer.md를 읽고 역할을 수행하라.
    ~/.claude/skills/remotion-assembly/SKILL.md의 워크플로우를 따른다.
    프로젝트 경로: <project>
    scene_plan.json에서 직접 컴포넌트를 매핑하고 narration에서 props를 추출하라.
    Remotion 프로젝트 셋업 → 컴포넌트 구현 → 조립까지 진행하라.
    컴포넌트 패턴은 ~/.claude/skills/remotion-assembly/references/component-patterns.md를 참조.
    배경 표준은 ~/.claude/skills/remotion-assembly/references/dark-gradient-background.md를 참조.

    ⚠️ 배경/마스코트 정책 (2026-05-19 확정):
    - iPad 템플릿(IPadTemplate, background.png) 사용 금지
    - 마스코트(Mascot, mascot.png) 사용 금지
    - 표준 배경: 풀스크린 다크 그라디언트
        radial-gradient(ellipse at top, rgba(245,158,11,0.12) 0%, transparent 55%),
        linear-gradient(180deg, #0b1120 0%, #1e293b 50%, #0b1120 100%)
    - 콘텐츠 패딩: padding: '80px 120px 200px' (하단 200px = 자막 safe area)
    - 텍스트는 다크 톤에 맞는 slate-100~300 (#f1f5f9 / #e2e8f0 / #cbd5e1) 사용
    - 액센트는 amber #f59e0b 메인 + cyan/emerald/rose/violet 중 보조 1~2개
    - 점선·축·비활성 요소는 slate-700/800 금지, slate-400(#94a3b8) 또는 slate-500(#64748b) 사용

    ⚠️ 브랜드 로고 자동 매칭 필수:
    - ~/.claude/skills/remotion-assembly/references/brand-logos/manifest.yml을 로드
    - scene_plan.json의 각 씬에서 narration + subtitle + visual_note를 스캔하여
      logos[*].aliases와 case-insensitive 부분 일치하는 브랜드 탐지
    - 매칭된 브랜드의 SVG를 public/images/로 복사 (프로젝트 image/에 동명 파일이 있으면 프로젝트 우선)
    - SceneVisual.tsx의 해당 씬에 BrandLogo / QuadrantMatrix.logoSrc 등으로 주입
    - 결과를 <project>/_workspace/logo_matches.md에 리포트 (매칭 결과 + 미매칭 브랜드 언급)
    - 상세 절차는 remotion-assembly SKILL.md의 '브랜드 로고 자동 매칭' 섹션 참조

    ⚠️ 다크 그라디언트 캔버스 레이아웃 표준 (2026-05-19 확정):
    - 캔버스: 1920×1080 풀스크린, iPad 프레임/노치 없음
    - 콘텐츠 컨테이너: <AbsoluteFill style={{display:'flex', alignItems:'center', justifyContent:'center', padding:'80px 120px 200px'}}>
    - 콘텐츠 가용 영역: 1680×800 (iPad 720px 대비 +80px 여유)
    - TimedSubtitle: 캔버스 좌표 bottom: 96, left:50% + translateX(-50%), max-width: 1600
    - 자막 배경: rgba(11,17,32,0.78) + backdrop-filter blur(10px) + amber 0.18 보더
    - 상세: dark-gradient-background.md 'MainVideo.tsx 패턴' / '자막 표준' 섹션

    ⚠️ 긴 씬 스테이지 전개 필수 (durationSec ≥ 18 OR narration 4문장+ OR 정적 카드):
    - 별도 SceneNReveal 컴포넌트로 분리
    - 씬 길이 비율로 4 스테이지 분할 (0 / 0.22 / 0.48 / 0.78)
    - 누적 배치 (이전 스테이지 사라지지 않음)
    - 마지막 스테이지: URL/CTA/핵심 숫자 강조 (glow 맥동 + 커서 깜빡임)
    - 상세: component-patterns.md '긴 씬의 시간차 전개 패턴' 섹션

    ⚠️ 콘텐츠 오버플로 검증 (다크 그라디언트 캔버스):
    - 가용 콘텐츠 영역은 1680×800 (1920×1080에서 padding 80/120/200 적용 후)
    - 800px를 넘는 헤비 다이어그램(react-loop·quadrant-matrix·horse-harness·lethal-triangle·timeline-cards 6+스텝 등)은
      scale 0.85~0.9 + 대칭 음수 마진(M = H × (1 - S) / 2, transformOrigin: center center) 래퍼 적용
    - 대부분의 다이어그램(원본 700~800px)은 원본 그대로 들어감 — iPad 시절 강제 축소는 더 이상 필수가 아님
    - Remotion Studio 프리뷰에서 콘텐츠가 자막(bottom 96 영역)과 겹치지 않는지 시각 검증

    ⚠️ Phase 4 승인 게이트는 오케스트레이터가 담당한다:
    - Remotion Studio 실행과 최종 렌더링(npx remotion render)은 이 에이전트가 직접 수행하지 말 것
    - 이 에이전트는 프로젝트 조립과 TypeScript 컴파일 검증까지만 수행하고 종료한다",
  model: "opus"
)
```

**Phase 3 완료 후 오케스트레이터가 Phase 2를 한 번 더 실행** — composer가 update_scenes_ts.py를 처음 만들었기 때문.

### Phase 3.5: Whisper Pre-render Gate (사람 녹음 워크플로 기본 SKIP)

⚠️ **사용자 직접 녹음 워크플로에서는 기본적으로 skip한다.** Whisper Gate C는 TTS auto-trim 버그 방어용으로 설계됐는데, 사람이 직접 녹음하면 narration과 100% 일치하지 않는 자연스러운 변형이 다수 발생하여 모두 false positive로 잡힌다 (claude-vs-codex 프로젝트 §10.3에서 34건 위반 모두 false positive로 검증됨).

다만 **사용자가 명시적으로 요청**하면 실행 가능. 위반 검증 시 끝부분 단어가 의미상 일치하면 false positive로 판정해 강제 진행하도록 안내.

### Phase 4: 프리뷰 + 렌더링 (오케스트레이터 직접)

Phase 3 서브에이전트는 조립만 마치고 종료한다. 아래 단계는 **오케스트레이터(본 스킬을 실행하는 주 에이전트)**가 직접 수행한다 — 서브에이전트는 유저 턴을 대기할 수 없어 승인 게이트가 무시되기 쉽기 때문.

1. `cd <project>/<project-name>-video && nohup npx remotion studio --port 3123 --gl=angle > /tmp/remotion-studio.log 2>&1 & disown`
2. 사용자에게 `http://localhost:3123` 확인 요청 — **여기서 반드시 멈추고 사용자 응답을 기다릴 것**
3. 사용자 피드백 반영 (코드 수정 → 핫리로드로 즉시 반영)
4. **사용자의 명시적 승인("렌더링 진행", "승인" 등) 후에만** 최종 렌더링
5. `output/output.mp4` + `output/thumbnail.png` 생성

### Phase 3 ↔ Phase 4 금지사항

- 서브에이전트가 `npx remotion render`를 실행해서는 안 된다
- 서브에이전트가 Studio를 띄워 사용자에게 "확인해 주세요"를 자기 입으로 요청하는 것도 안 된다 (턴 대기 불가)
- 출력 파일명은 반드시 `output/output.mp4` + `output/thumbnail.png`로 고정 (임의 이름 금지)

### Phase 5: 완료

```
✅ 영상 제작 완료
- 영상: <project>/output/output.mp4
- 썸네일: <project>/output/thumbnail.png
- Remotion 프로젝트: <project>/<name>-video/
- 씬 수: N개, 총 길이: M분 S초
```

## 데이터 흐름

```
[content-production 산출물]
   ├─ script/02_writer_script.md
   ├─ _workspace/scene_plan.json
   └─ _workspace/recording_guide.md
        ↓
[사용자 직접 녹음] _workspace/audio/seg-NN.wav
        ↓
Phase 1-A: [오케스트레이터] normalize_recordings.sh
   _workspace/audio/seg-NN.wav (any sr/ch/bits)
   → _workspace/tts/seg_NN.wav (24kHz/mono/16-bit + 무음 trim + 100ms 패딩)
        ↓
Phase 1-B: [오케스트레이터] generate_timing.py (PADDING_SEC=0.3)
   → _workspace/timing.json
        ↓
Phase 2: [오케스트레이터] Audio Sync (멱등)
   _workspace/tts/*.wav → <project>-video/public/audio/
   _workspace/timing.json → <project>-video/public/audio/timing.json
   update_scenes_ts.py (존재 시)
        ↓
Phase 2.5 (선택): [vp-motion-designer] component-patterns.md 개선
        ↓
Phase 3: [vp-video-composer] Remotion 조립 + TypeScript 검증
        ↓
[오케스트레이터] Phase 2 재실행 (update_scenes_ts.py가 이제 존재하므로)
        ↓
Phase 4: [오케스트레이터] Studio 프리뷰 → 사용자 승인
        ↓
output/output.mp4 + output/thumbnail.png
```

## 에러 핸들링

| Phase | 에러 | 대응 |
|-------|------|------|
| 0 | scene_plan.json 누락 | `/content-production` 먼저 실행 안내, 진행 중단 |
| 0 | recording_guide.md 누락 | `/content-production` Phase 7 누락 — 사용자에게 보고 |
| 0 | _workspace/audio/ 비어있음 | 녹음 가이드 안내, 진행 중단 |
| 1-A | 어떤 wav가 normalize 실패 | 해당 파일 보고, 사용자에게 재녹음 요청 |
| 1-A | 출력 wav 수 ≠ 씬 수 | 누락 씬 ID 보고, 진행 중단 |
| 1-B | 특정 wav 누락 | 5초 무음 fallback + 누락 씬 ID 보고. exit 1 |
| 2 | Remotion 디렉터리 미탐지 | Phase 3 완료 후 재실행 (skip + 플래그) |
| 2 | 파일 복사 실패 | 디스크 공간/권한 확인, Fatal |
| 2.5 | Remotion MCP 응답 없음 | 공식 문서 URL 직접 참조로 fallback |
| 2.5 | 새 컴포넌트 빌드 실패 | TypeScript 에러 수정, 기존 패턴으로 fallback |
| 3 | 컴포넌트 매핑 실패 | 해당 씬은 default-scene (GlassCard + BigTitle)로 fallback |
| 3 | Remotion 셋업 실패 | Node.js v18+ 확인, 에러 보고 |
| 4 | GPU 렌더링 실패 | CPU 폴백 |

## 테스트 시나리오

### 정상 흐름
- 입력: content-production 산출물 7개 + `_workspace/audio/seg-01.wav~seg-NN.wav` (사용자 녹음)
- 기대: Phase 1 → tts/ + timing.json 생성. Phase 2 → public/audio sync. Phase 3 → Remotion 조립. Phase 4 → Studio 프리뷰 → 사용자 승인 → output.mp4 + thumbnail.png

### 에러 흐름 — 녹음 누락
- 입력: scene_plan.json은 58씬인데 `_workspace/audio/`에 50개만
- 기대: Phase 1-A에서 8개 누락 씬 ID 보고, "추가 녹음 후 다시 호출" 안내, 진행 중단

### 자동 연결 모드
- 입력: 사용자가 "녹음 끝났어. 영상 만들어줘"
- 기대: Phase 0 검증 통과 시 자동 진행. 검증 실패 시 누락 산출물 안내.

## 관련 스킬

- `content-production` — 이 스킬의 입력(scene_plan.json, recording_guide.md)을 만드는 선행 스킬
- `scene-analysis` — content-production이 사용 (cp-scene-architect)
- `voice-production` — TTS-only 워크플로용 (이 스킬에서는 사용 안 함, deprecated)
- `remotion-assembly` — vp-video-composer / vp-motion-designer가 사용

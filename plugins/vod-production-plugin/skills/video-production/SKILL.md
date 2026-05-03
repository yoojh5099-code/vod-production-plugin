---
name: video-production
description: |
  YouTube 영상을 대본부터 최종 렌더링까지 에이전트 팀으로 자동 제작하는 오케스트레이터 스킬.
  4명의 전문 에이전트(씬 분석, 음성 생성, 모션 디자인, 영상 조립)를 조율하여 완성된 MP4 영상과 썸네일을 산출한다.
  "영상 제작", "비디오 제작", "영상 만들어줘", "대본으로 영상 만들어줘", "스크립트를 영상으로", "video production",
  "팀으로 영상 만들어줘", "하네스로 영상 제작" 등을 요청하면 이 스킬을 사용한다.
  단일 에이전트로 빠르게 만들고 싶으면 create-youtube 스킬을 사용할 것.
---

# YouTube 영상 제작 오케스트레이터

4명의 전문 에이전트를 **Pipeline** 패턴으로 조율하여 YouTube 영상을 제작한다.

## 팀 구성

| 에이전트 | 역할 | 스킬 | Phase |
|---------|------|------|-------|
| vp-scene-architect | 씬 분석, 구조화 | scene-analysis | 1 |
| vp-voice-engineer | TTS 음성 + 타이밍 | voice-production | 2 |
| (오케스트레이터) | **Audio Sync (멱등)** — tts/timing을 public/audio로 동기화 | — | **2.1** |
| vp-motion-designer | 모션 패턴 설계/개선 (Remotion MCP 활용) | remotion-assembly | 2.5 (선택) |
| vp-video-composer | Remotion 조립/렌더링 (컴포넌트 매핑 + narration 파싱 포함) | remotion-assembly | 3-4 |

## 실행 모드

- Phase 1: **서브에이전트** (단일 에이전트, 순차)
- Phase 2: **서브에이전트** (단일 에이전트, 순차)
- Phase 2.1: **오케스트레이터 직접 실행** (멱등 sync, 무조건 실행)
- Phase 2.5: **서브에이전트** (단일 에이전트, 선택적 — 모션 개선 요청 시)
- Phase 3-4: **서브에이전트** (단일 에이전트, 순차)

## 컴포넌트 패턴 레퍼런스

패턴 관련 문서는 역할별로 분리되어 있다. 오케스트레이터는 **두 파일 모두 읽지 않는다** — 각 에이전트에 경로만 전달.

| 파일 | 역할 | 주 사용자 | 분량 |
|------|------|----------|------|
| `~/.claude/skills/remotion-assembly/references/pattern-catalog.md` | **선택용** — 7 의도 카테고리, 24 visual 타입, tier별 예산 규칙 | vp-scene-architect | ~150줄 |
| `~/.claude/skills/remotion-assembly/references/component-patterns.md` | **구현용** — 전체 패턴의 구현 코드와 props 스펙 | vp-video-composer, vp-motion-designer | ~2350줄 (Grep으로 섹션만 lazy load) |

### 다이버시티 예산 (pattern-catalog.md 발췌)

| tier | 개수 | 예산/영상 |
|------|------|----------|
| signature | 7 | **1회씩** |
| special | 3 | **2회 이하** |
| generic | 14 | **3회 이하** |

추가 규칙: 인접 씬 동일 visual 금지 · 3씬 이내 동일 visual 최대 2회 · 의도 카테고리 7 중 최소 5종 사용.
**위반 시 vp-scene-architect가 같은 카테고리 내 대체 패턴으로 자동 리밸런싱하고 `_workspace/visual_allocation_audit.md`에 기록.**

### 매핑 규칙
- 카테고리 미매칭 시 → `default-scene` (GlassCard + BigTitle) fallback
- 같은 visual이 2씬 이내 반복 → 이징/spring 변주 (component-patterns.md의 "이징 변주 가이드")
- 텍스트 컴포넌트는 **3D 회전 금지** (rotateX/rotateY — 반전 버그). FlipCardGrid만 의도적 예외.

### Studio 갤러리 프리뷰
`npx remotion studio --port 3123` → `Patterns` 폴더에서 25종 컴포지션 6초 단위 독립 프리뷰.
(씬 내부에서만 쓰는 WordByWordText / GlassCard / ParticleConfetti / MorphingShape / ConcentricRings는 갤러리 미노출)

## 워크플로우

### Phase 0: 준비

1. 프로젝트 경로를 확인한다 (사용자 지정 또는 기본값)
2. 필수 폴더 구조를 확인한다:
   ```
   <project>/
   ├── script/    ← 대본 (필수)
   ├── background/
   ├── music/     ← BGM (필수)
   ├── thumbnail/
   ├── voice/
   ├── image/
   ├── output/
   └── _workspace/
   ```
3. 누락된 폴더를 생성한다
4. script/ 폴더에 대본 파일이 있는지 확인 — 없으면 사용자에게 요청

### Phase 1: 씬 분석 (순차)

`vp-scene-architect`를 서브에이전트로 실행한다:

```
Agent(
  description: "씬 분석",
  prompt: "~/.claude/agents/vp-scene-architect.md를 읽고 역할을 수행하라.
    ~/.claude/skills/scene-analysis/SKILL.md의 워크플로우를 따른다.
    Visual 선택은 반드시 ~/.claude/skills/remotion-assembly/references/pattern-catalog.md의
    카테고리 매핑과 다이버시티 예산 규칙을 따른다 (component-patterns.md는 읽지 말 것).
    프로젝트 경로: <project>
    산출물 2개:
      1. <project>/_workspace/scene_plan.json (visual + visual_category + visual_tier 포함)
      2. <project>/_workspace/visual_allocation_audit.md (예산 검증 리포트)",
  model: "opus"
)
```

**검증**:
- `_workspace/scene_plan.json` 존재 + 유효한 JSON
- `_workspace/visual_allocation_audit.md` 존재 + 예산 위반 없음 확인
- 각 씬에 `visual_category`, `visual_tier` 필드 존재

### Phase 2: 음성 생성 (순차)

`vp-voice-engineer`를 서브에이전트로 실행한다:

```
Agent(
  description: "TTS 음성 생성",
  prompt: "~/.claude/agents/vp-voice-engineer.md를 읽고 역할을 수행하라.
    ~/.claude/skills/voice-production/SKILL.md의 워크플로우를 따른다.
    프로젝트 경로: <project>
    scene_plan.json을 읽고 TTS 음성을 생성하라.
    결과를 <project>/_workspace/tts/에 저장하고 <project>/_workspace/timing.json을 작성하라.

    ⚠️ 영문→한글 발음 치환 필수:
    - narration에 Figma, Anthropic, Claude, Datadog, Canva, Opus 4.7 같은 영문 고유명/버전이 있으면
      표준 치환 맵(voice-production SKILL.md 참조)으로 narration_tts 필드를 생성
    - TTS는 narration_tts 우선, 자막은 원본 narration 유지 — 시청자는 화면 영문 + 음성 한국어 발음
    - 새 브랜드가 있으면 프로젝트별로 치환 맵 확장",
  model: "opus"
)
```

**검증**:
- `_workspace/timing.json` 존재 + 씬 수 일치
- `_workspace/tts/seg_*.wav` 파일들 존재
- **generate_tts.py exit code 0** — 1이면 Gate B 위반. 사용자에게 해당 씬 ID + cps 수치 보고하고 수동 확인 요청. **절대 자동으로 다음 phase로 넘어가지 말 것**

### Phase 2.1: Audio Sync (멱등, 오케스트레이터 직접 실행)

⚠️ **이 단계는 최초 실행이든 재생성이든 무조건 실행한다.** Phase 2가 성공했으면 항상 뒤따른다. `vp-voice-engineer` 재실행 후 이 단계를 누락하면 Remotion이 옛 음성을 계속 재생하는 사일런트 버그가 발생한다 (graphrag 프로젝트 2026-05-03 실제 사고).

**왜 오케스트레이터가 직접 하는가**: 서브에이전트 위임은 불필요한 복잡도. 단순 파일 복사 + Python 스크립트 한 번 실행이므로 오케스트레이터 Bash 한 번으로 처리.

**Remotion 프로젝트 디렉터리 탐지**: `<project>/*-video/` 또는 `<project>/graphrag-video/` 같은 패턴. `<project>` 안에 `public/audio/` 를 갖는 디렉터리가 target.

**실행 단계**:
```bash
cd <project>
REMOTION_DIR=$(ls -d *-video 2>/dev/null | head -1)  # 예: graphrag-video

# Remotion 프로젝트가 아직 없으면(최초 실행 전) 이 phase는 skip하고 Phase 3 후에 실행
if [ -z "$REMOTION_DIR" ]; then
  echo "[Phase 2.1] Remotion 프로젝트 미생성 — Phase 3 이후 재동기화 필요"
  # Phase 3 완료 시 오케스트레이터가 Phase 2.1을 한 번 더 실행
else
  mkdir -p "$REMOTION_DIR/public/audio"
  cp _workspace/tts/seg_*.wav "$REMOTION_DIR/public/audio/"
  cp _workspace/timing.json "$REMOTION_DIR/public/audio/timing.json"
  # scenes.ts의 startSec/durationSec/audioDurationSec/subtitleStartsSec 갱신
  if [ -f update_scenes_ts.py ]; then
    python3 update_scenes_ts.py
  fi
  echo "[Phase 2.1] Audio sync 완료"
fi
```

**검증**:
- `<project>/<project>-video/public/audio/seg_XX.wav` 각 파일의 길이가 `_workspace/tts/seg_XX.wav`와 일치 (ffprobe로 체크)
- `<project>/<project>-video/public/audio/timing.json` 과 `_workspace/timing.json` 이 identical
- `scenes.ts`의 `audioDurationSec` 값이 실제 wav 길이와 오차 0.05s 이내

**update_scenes_ts.py가 없는 경우**: Phase 3에서 composer가 scenes.ts를 처음 생성할 것이므로, 이 경우 Phase 2.1의 copy 부분만 수행하고 scenes.ts 갱신은 skip. Phase 3 완료 후 composer가 자동 생성.

### Phase 2.5: 모션 디자인 개선 (선택적)

사용자가 모션 그래픽 개선을 요청한 경우에만 실행한다. 기본 파이프라인에서는 건너뛴다.

`vp-motion-designer`를 서브에이전트로 실행한다:

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

**트리거 조건**:
- 사용자가 "모션 개선", "애니메이션 개선", "모션 디자인" 등을 명시적으로 요청
- 사용자가 "모션 패턴 추가", "새 컴포넌트" 등을 요청
- 오케스트레이터가 component-patterns.md 보강이 필요하다고 판단

**검증**:
- 새/수정된 컴포넌트가 빌드 에러 없이 컴파일됨
- Remotion Studio에서 프리뷰 정상 렌더링
- component-patterns.md에 새 패턴이 올바른 포맷으로 추가됨

### Phase 3: 영상 조립 (순차)

`vp-video-composer`를 서브에이전트로 실행한다:

```
Agent(
  description: "Remotion 영상 조립",
  prompt: "~/.claude/agents/vp-video-composer.md를 읽고 역할을 수행하라.
    ~/.claude/skills/remotion-assembly/SKILL.md의 워크플로우를 따른다.
    프로젝트 경로: <project>
    scene_plan.json에서 직접 컴포넌트를 매핑하고 narration에서 props를 추출하라.
    Remotion 프로젝트 셋업 → 컴포넌트 구현 → 조립까지 진행하라.
    컴포넌트 패턴은 ~/.claude/skills/remotion-assembly/references/component-patterns.md를 참조.
    iPad 템플릿은 ~/.claude/skills/remotion-assembly/references/ipad-template-pattern.md를 참조.

    ⚠️ 브랜드 로고 자동 매칭 필수:
    - ~/.claude/skills/remotion-assembly/references/brand-logos/manifest.yml을 로드
    - scene_plan.json의 각 씬에서 narration + subtitle + visual_note를 스캔하여
      logos[*].aliases와 case-insensitive 부분 일치하는 브랜드 탐지
    - 매칭된 브랜드의 SVG를 public/images/로 복사 (프로젝트 image/에 동명 파일이 있으면 프로젝트 우선)
    - SceneVisual.tsx의 해당 씬에 BrandLogo / QuadrantMatrix.logoSrc 등으로 주입
    - 결과를 <project>/_workspace/logo_matches.md에 리포트 (매칭 결과 + 미매칭 브랜드 언급)
    - 상세 절차는 remotion-assembly SKILL.md의 "브랜드 로고 자동 매칭" 섹션 참조

    ⚠️ IPadTemplate 레이아웃 표준 (2026-04-22 확정):
    - 콘텐츠 패딩: paddingTop: 90, paddingBottom: 90 (대칭) — 콘텐츠 수직 중심 스크린 정중앙(y=501)
    - Mascot: overlay prop, right: 20, bottom: 20, size: 180 (iPad 스크린 내부 우하단 고정)
    - TimedSubtitle: overlay prop, bottom: 12, left: 50% + translateX(-50%), max-width: 1400 (스크린 하단 가장자리 중앙)
    - 상세: ipad-template-pattern.md "표준 레이아웃" 섹션

    ⚠️ 긴 씬 스테이지 전개 필수 (durationSec ≥ 18 OR narration 4문장+ OR 정적 카드):
    - 별도 SceneNReveal 컴포넌트로 분리
    - 씬 길이 비율로 4 스테이지 분할 (0 / 0.22 / 0.48 / 0.78)
    - 누적 배치 (이전 스테이지 사라지지 않음)
    - 마지막 스테이지: URL/CTA/핵심 숫자 강조 (glow 맥동 + 커서 깜빡임)
    - 상세: component-patterns.md "긴 씬의 시간차 전개 패턴" 섹션

    ⚠️ iPad 오버플로 검증 필수:
    - iPad 스크린 유효 콘텐츠 영역은 세로 ≈720px — 이를 넘는 visual은 위아래가 잘리거나 자막과 겹친다
    - component-patterns.md의 'iPad 제약에 맞춘 축소 스펙' 섹션 표를 보고,
      scene_plan.json에 react-loop/quadrant-matrix/horse-harness/lethal-triangle/timeline-cards 등이 있으면
      해당 스펙의 scale·margin·gap을 반드시 적용하라 (래퍼 수식: M = H × (1 - S) / 2, transformOrigin은 center center)
    - Remotion Studio 프리뷰에서 각 씬이 iPad 프레임 위·아래로 벗어나지 않는지 시각 검증

    ⚠️ Phase 4 승인 게이트는 오케스트레이터가 담당한다:
    - Remotion Studio 실행과 최종 렌더링(npx remotion render)은 이 에이전트가 직접 수행하지 말 것
    - 이 에이전트는 프로젝트 조립과 TypeScript 컴파일 검증까지만 수행하고 종료한다",
  model: "opus"
)
```

### Phase 3.5: Whisper Pre-render Gate (Gate C, 오케스트레이터 직접 실행)

⚠️ Phase 3 완료 후 **Phase 4 Studio를 띄우기 전에** 반드시 실행한다. TTS auto-trim 버그가 Gate A/B를 둘 다 빠져나간 edge case를 최종 방어한다.

**목적**: 각 씬 wav를 Whisper로 전사해 **narration_tts 마지막 15자**가 전사에 포함되는지 확인. 포함되지 않으면 해당 씬의 끝부분이 잘렸다는 강력한 신호.

**실행**:
```bash
cd <project>
python3 <<'EOF'
import json, re, subprocess, sys, wave, os

SCENE_PLAN = "_workspace/scene_plan.json"
PUBLIC_AUDIO = None
for d in os.listdir("."):
    if d.endswith("-video") and os.path.isdir(f"{d}/public/audio"):
        PUBLIC_AUDIO = f"{d}/public/audio"
        break
assert PUBLIC_AUDIO, "Remotion public/audio 디렉터리를 찾을 수 없음"

try:
    import whisper
except ImportError:
    print("[WARN] whisper 미설치 — pip install openai-whisper 후 다시 실행. Gate C skip.")
    sys.exit(0)

model = whisper.load_model("medium")
scenes = json.load(open(SCENE_PLAN))["scenes"]
violations = []
for s in scenes:
    sid = s["id"]
    wav = f"{PUBLIC_AUDIO}/seg_{sid:02d}.wav"
    if not os.path.exists(wav):
        violations.append((sid, "wav 없음"))
        continue
    text_expected = (s.get("narration_tts") or s["narration"]).strip()
    tail = re.sub(r"[\s'\"'\"()\[\].,?!]", "", text_expected)[-15:]
    result = model.transcribe(wav, language="ko", fp16=False)
    transcript = re.sub(r"[\s'\"'\"()\[\].,?!]", "", result["text"])
    if tail not in transcript:
        violations.append((sid, f"tail='{tail}' not in transcript"))
        print(f"[GATE-C FAIL] 씬 {sid}: 마지막 15자 누락")
        print(f"   expected tail: {tail}")
        print(f"   transcript:    {transcript[-40:]}")
if violations:
    print(f"\n[FATAL] Gate C 위반 씬 {len(violations)}개: {[v[0] for v in violations]}")
    sys.exit(1)
print("[DONE] Gate C 통과 — 모든 씬의 마지막 15자가 전사에 포함됨")
EOF
```

**실패 시**:
1. 렌더 중단
2. 사용자에게 위반 씬 ID + 해당 `narration_tts` 끝부분 + 전사 끝부분 보고
3. 선택지 제시: (a) TTS 재생성(해당 씬만), (b) 해당 씬 수동 청취 후 승인 시 강제 진행, (c) 중단하고 원고 수정

**비용**: Whisper medium 1회 로드(~30s) + 씬당 1~3s 전사. 25씬 영상 기준 총 2~3분. 렌더 시간(10~30분)에 비하면 미미.

**Gate A/B/C 역할 분담**:
- Gate A (trim ratio): 매 문장 생성 직후, 공짜
- Gate B (char/sec): 씬 단위, 공짜
- Gate C (Whisper): 렌더 직전 1회, 2~3분 — 최종 안전망

### Phase 4: 프리뷰 + 렌더링 (오케스트레이터가 직접 담당)

Phase 3 서브에이전트는 조립만 마치고 종료한다. 아래 단계는 **오케스트레이터(본 스킬을 실행하는 주 에이전트)**가 직접 수행한다 — 서브에이전트에게 위임하지 말 것. 서브에이전트는 유저 턴을 대기할 수 없어 승인 게이트가 무시되기 쉽기 때문.

1. **Gate C 통과 확인** (Phase 3.5) — 실패면 여기서 중단
2. `cd <project>/<project-name>-video && npx remotion studio --port 3123 --gl=angle` (백그라운드 실행)
3. 사용자에게 `http://localhost:3123` 확인 요청 — **여기서 반드시 멈추고 사용자 응답을 기다릴 것**
4. 사용자 피드백 반영 (코드 수정 → 핫리로드로 즉시 반영)
5. **사용자의 명시적 승인("렌더링 진행", "승인" 등) 후에만** 최종 렌더링
6. `output/output.mp4` + `output/thumbnail.png` 생성

### Phase 3 ↔ Phase 4 금지사항

- 서브에이전트가 `npx remotion render`를 실행해서는 안 된다
- 서브에이전트가 Studio를 띄워 사용자에게 "확인해 주세요"를 자기 입으로 요청하는 것도 안 된다 (턴 대기 불가)
- 출력 파일명은 반드시 `output/output.mp4` + `output/thumbnail.png`로 고정 (임의 이름 금지)

### Phase 5: 완료

최종 산출물 보고:
```
✅ 영상 제작 완료
- 영상: <project>/output/output.mp4
- 썸네일: <project>/output/thumbnail.png
- Remotion 프로젝트: <project>/<name>-video/
- 씬 수: N개, 총 길이: M분 S초
```

## 데이터 흐름

```
[script/] ──┐
[background/]──┤
[thumbnail/]───┘
       ↓
  Phase 1: [vp-scene-architect]
       ↓
  _workspace/scene_plan.json
       ↓
  Phase 2: [vp-voice-engineer]
       │  Gate A (MIN_KEEP_RATIO) + Gate B (char/sec) 필수 통과
       ↓
  _workspace/tts/seg_XX.wav + _workspace/timing.json
       ↓
  Phase 2.1: [오케스트레이터] Audio Sync (멱등)
       │  _workspace/tts/*.wav → <project>-video/public/audio/
       │  _workspace/timing.json → <project>-video/public/audio/timing.json
       │  update_scenes_ts.py (존재 시)
       ↓
  Phase 2.5 (선택): [vp-motion-designer] + Remotion MCP
       │  component-patterns.md 개선/확장
       ↓
  Phase 3: [vp-video-composer]
       │  scene_plan.json에서 직접 컴포넌트 매핑 + narration 파싱
       │  (최초 실행이면 update_scenes_ts.py도 이 단계에서 생성)
       ↓
  [오케스트레이터] Phase 2.1 재실행 (update_scenes_ts.py가 이제 존재하므로)
       ↓
  [오케스트레이터] Whisper Pre-render Gate (Gate C)
       │  각 씬 wav를 Whisper로 전사 → narration_tts 마지막 15자 포함 검증
       │  실패 시: 사용자 에스컬레이션 + 렌더 중단
       ↓
  Phase 4: [오케스트레이터] Remotion Studio → 사용자 확인
       ↓ (승인)
  output/output.mp4 + output/thumbnail.png
```

## 에러 핸들링

| Phase | 에러 | 대응 |
|-------|------|------|
| 0 | script/ 비어있음 | 사용자에게 대본 요청, 진행 중단 |
| 0 | music/ 비어있음 | 경고 후 BGM 없이 진행 |
| 1 | 대본 파싱 실패 | 지원 형식 안내, 진행 중단 |
| 2 | TTS 모델 미설치 | Fatal — 설치 안내 |
| 2 | TTS 부분 실패 | 실패 세그먼트에 무음 fallback, 계속 진행 |
| 2 | **Gate B 위반 (exit code 1)** | **사용자 에스컬레이션 — 씬 ID + cps 수치 보고, 다음 phase 진행 금지** |
| 2.1 | Remotion 디렉터리 미탐지 | Phase 3 완료 후 재실행 (skip + 플래그) |
| 2.1 | 파일 복사 실패 | 디스크 공간/권한 확인, Fatal |
| 2.5 | Remotion MCP 응답 없음 | 공식 문서 URL 직접 참조로 fallback |
| 2.5 | 새 컴포넌트 빌드 실패 | TypeScript 에러 수정, 기존 패턴으로 fallback |
| 3 | 컴포넌트 매핑 실패 | 해당 씬은 default-scene (GlassCard + BigTitle)로 fallback |
| 3 | Remotion 셋업 실패 | Node.js v18+ 확인, 에러 보고 |
| 3.5 | **Gate C 위반 (Whisper)** | **렌더 중단, 위반 씬 보고, 재생성/수동승인/원고수정 중 선택** |
| 3.5 | Whisper 미설치 | 경고 후 Gate C skip (소프트 페일), 계속 진행하되 Phase 4에서 사용자 청취 확인 필수 |
| 4 | GPU 렌더링 실패 | CPU 폴백 |

## 테스트 시나리오

### 정상 흐름
- 입력: `vod/test/script/script.json` (10씬), BGM in `music/`, voice ref
- 기대: Phase 1 → scene_plan.json (10씬). Phase 2 → 10 wav + timing.json. Phase 3 → Remotion 프로젝트 완성 (scene_plan.json에서 직접 컴포넌트 매핑). Phase 4 → Studio 프리뷰 → 승인 → output.mp4 + thumbnail.png

### 에러 흐름 — TTS 모델 없음
- 입력: 동일, 단 ~/models/Qwen3-TTS-Base 없음
- 기대: Phase 2에서 voice-engineer가 Fatal 보고. 오케스트레이터가 에러 보고 + 모델 설치 안내

### 자동 연결 모드
- 입력: "이 주제로 기획부터 영상까지 한번에 해줘"
- 기대: content-production(기획) 실행 → script/script.json 생성 → video-production(제작) 자동 실행

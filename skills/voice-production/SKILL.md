---
name: voice-production
description: |
  YouTube 영상의 씬별 TTS 음성을 생성하고 타이밍 데이터를 추출하는 스킬.
  vp-voice-engineer 에이전트가 사용한다. Qwen3-TTS-Base 모델로 voice cloning 기반 음성을 생성하고, 실제 오디오 길이를 측정하여 timing.json을 만든다.
  직접 트리거되지 않으며, video-production 오케스트레이터를 통해 실행된다.
---

# 음성 제작 스킬

씬별 TTS 음성을 생성하고 정확한 타이밍 데이터를 추출한다. 타이밍 데이터는 영상의 씬 길이 결정과 음성-자막 싱크의 기준이 된다.

## TTS 모델 설정

- **모델 경로**: `~/models/Qwen3-TTS-Base` (로컬 영구 저장)
- **dtype**: `torch.bfloat16`
- **레퍼런스 음성**: `~/.claude/skills/voice-production/reference/yoojh_voice_ref.wav` (스킬에 번들)
- **레퍼런스 텍스트**: `"안녕하세요 저는 AWS Technical Account Manager 유재혁 입니다"`
  - 프로젝트 `voice/` 폴더에 별도 파일이 있으면 우선 사용
- **핵심 규칙**: `ref_audio`/`ref_text`를 매 호출마다 직접 전달
- **금지**: `create_voice_clone_prompt` 사용 금지 — 품질 저하 원인

상세 코드 패턴: `~/.claude/skills/create-youtube/references/tts-generation.md` 참조

## 워크플로우

### 1. 씬 데이터 로드 + 영문→한글 발음 치환

`<project>/_workspace/scene_plan.json`에서 각 씬 데이터를 읽는다.

**TTS 입력 우선순위**:
1. `narration_tts` 필드가 있으면 → TTS 입력으로 사용 (영문→한글 발음 치환본)
2. 없으면 → `narration` 필드 사용

**자막은 항상 원본 `narration`** — TTS 입력과 자막은 scenes.ts에서 분리 관리된다. 시청자는 화면에서 영문 브랜드명을 보면서 한국어 발음으로 듣게 됨.

#### narration_tts 생성 규칙

원고에 영문 브랜드·제품·모델명이 있으면 한국어 발음 표기로 치환하여 `narration_tts`를 scene_plan.json에 기록한다. Qwen3-TTS는 한국어 문맥에서 영문 스펠링을 자모 철자로 읽거나 어색한 영어식 발음을 얹는 경향이 있어, 사전 치환이 품질에 결정적이다.

**표준 치환 맵 (긴 것부터 먼저 적용)**:

```python
REPLACEMENTS = [
    # 모델·제품 (긴 것 우선)
    ("Claude Opus 4.7", "클로드 오퍼스 사점칠"),
    ("Opus 4.7", "오퍼스 사점칠"),
    ("Claude Design", "클로드 디자인"),
    ("Claude Code", "클로드 코드"),
    ("Claude Pro", "클로드 프로"),
    ("Claude", "클로드"),
    # 회사·서비스
    ("Anthropic", "앤트로픽"),
    ("Figma", "피그마"),
    ("Datadog", "데이터독"),
    ("Canva", "캔바"),
    ("Brilliant", "브릴리언트"),
    ("Adobe", "어도비"),
    ("GeekNews", "긱뉴스"),
    # URL
    ("claude.ai/design", "클로드 닷 에이아이 슬래시 디자인"),
    # 플랜
    ("Max", "맥스"),
    ("Team", "팀"),
    ("Enterprise", "엔터프라이즈"),
    # 형식 약어
    ("DOCX", "닥스"),
    ("PPTX", "피피티"),
    ("PDF", "피디에프"),
    ("HTML", "에이치티엠엘"),
    ("AI", "에이아이"),
    ("PM", "피엠"),
    ("SNS", "에스엔에스"),
]
```

**규칙**:
- 숫자 버전은 한국어 숫자로 (`4.7` → `사점칠`, `3.5` → `삼점오`)
- URL은 도메인 단위로 분리해 한국어로 설명 (`claude.ai/design` → `클로드 닷 에이아이 슬래시 디자인`)
- **긴 문자열부터 먼저 치환** (예: `Claude Design`이 `Claude`보다 먼저 등장해야 정확히 변환됨)
- 프로젝트에 등장하는 고유 브랜드가 표준 맵에 없으면 프로젝트별로 확장

**적용 방법**:

```python
import json, re
with open('_workspace/scene_plan.json') as f:
    plan = json.load(f)
for s in plan['scenes']:
    tts = s['narration']
    for en, ko in REPLACEMENTS:
        tts = tts.replace(en, ko)
    s['narration_tts'] = tts
with open('_workspace/scene_plan.json', 'w') as f:
    json.dump(plan, f, ensure_ascii=False, indent=2)
```

### 2. TTS 생성 스크립트 작성 (dummy-suffix + auto-trim)

`<project>/generate_tts.py`를 작성한다. 템플릿: `scripts/generate_tts_template.py`

#### 2-1. 왜 dummy-suffix + auto-trim인가

Qwen3-TTS는 autoregressive 오디오 코덱 토큰 생성 모델이고, 학습 데이터가 silence-trimmed 코퍼스라 **문장 끝 모음이 완전 감쇠하기 전에 EOS 토큰을 예측**한다. 결과적으로 `narration`을 그대로 넣으면 wav 마지막 20ms에서 peak가 cliff처럼 떨어지고(예: 4576 → 2), 사람 귀에는 "요/다/니다" 끝이 잘린 것처럼 들린다.

해결은 텍스트 쪽에서 EOS를 뒤로 미는 것:

1. `narration_tts` 뒤에 `" 네."` 더미 문장을 붙여 TTS 투입
2. 모델은 "아직 문장이 안 끝났네"라고 판단 → 본문 모음을 자연 감쇠까지 전부 생성한 뒤 "네"를 뽑음
3. 20ms 블록 envelope 역스캔으로 본문과 dummy 사이의 silence gap을 찾아 **silence 시작 + 100ms 지점에서 절단**

이 방식은 2026-04-30 프로젝트(llm-wiki)에서 33개 씬 전수 검증 완료.

#### 2-2. Auto-trim 파라미터 (2026-05-03 개정)

| 파라미터 | 값 | 설명 |
|---|---|---|
| `DUMMY_SUFFIX` | `" 네."` | EOS 밀기용 더미. 한국어 평서문·의문문·인용구 모두에서 유효 |
| `SILENCE_THR` | `200` | int16 기준. peak < 200이면 silence로 간주 |
| `LOUD_THR` | `600` | peak > 600 = 발화 중 (dummy_end 탐지용) |
| `TAIL_MARGIN_SEC` | `0.10` | silence 시작 이후 이만큼 여유 두고 trim (본문 tail 여운 보존) |
| `FALLBACK_MARGIN_SEC` | `0.15` | silence gap 탐지 실패 시 dummy_end에서 이만큼 앞에서 자름 |
| `MIN_DUMMY_GAP_SEC` | `0.08` | dummy-본문 사이 silence gap 최소 길이. 이보다 짧으면 fallback |

⚠️ **`MIN_SILENCE_SEC` 제거됨 (2026-05-03)**: 구버전은 본문 안쪽에서 "첫 250ms silence"를 역방향 탐색해 본문 끝으로 인정했으나, 한국어 쉼표/말줄임/열거의 중간 pause에 오탐해 뒤쪽 음성을 통째로 자르는 사고가 발생했다 (graphrag 프로젝트 씬 10: 17.54s → 8.75s로 절반 소실). 새 알고리즘은 **dummy 경계 바로 앞 silence만** 기준으로 쓰고 본문 내부는 scan하지 않는다.

#### 2-2B. 검증 Gate (필수 적용)

TTS 생성은 알고리즘 버그가 재발해도 최종 영상에 오염이 섞이지 않도록 **이중 Gate**로 방어한다:

**Gate A — MIN_KEEP_RATIO (템플릿 내장)**
- trim 결과가 raw 길이의 50% 미만이면 trim 거부하고 raw wav를 그대로 사용
- 알고리즘이 본문 내부에서 잘못된 경계를 찾는 최악의 경우를 방어
- 비용 0, 무조건 활성화

**Gate B — char/sec 비율 (템플릿 내장)**
- 각 씬의 `len(narration_tts) / audio_duration`을 계산
- 허용 범위: `3.0 ≤ cps ≤ 25.0` (한국어 평균 12~15 기준의 극단 이탈만 잡음)
- 위반 시 해당 씬 최대 2회 재생성 (`MAX_RETRIES = 2`)
- 재시도 소진되어도 위반하면 **exit code 1로 fatal 종료** — 오케스트레이터가 감지해서 사용자에게 에스컬레이션
- 로그에 `[GATE-B]` / `[GATE-B FAIL]` 프리픽스로 기록

**왜 문장 단위가 아니라 씬 단위인가**: 문장 단위는 SENTENCE_SPLIT_RE로 분해해야 하고 edge case가 많음. 씬 단위도 한 문장만 잘려도 전체 cps가 눈에 띄게 이탈하므로 실용적으로 충분.

#### 2-3. Edge case

- **의문문 종결 (`~까요?`, `~뭘까요?`)**: 억양이 상승이라 tail 감쇠가 짧음 → 정상 처리됨
- **인용구 종결 (`~'입니다'.`)**: 인용부호 + 마침표 + dummy 사이에 TTS가 2차 재피크를 만들 수 있음 → 탐지된 trim 지점이 너무 앞쪽이면 raw wav 청취로 확인
- **"다/니다" 종결**: `ㄴ/ㄷ` 종성이 비음/파열음이라 원래 모델이 tight-cut하는 경향이 강함 → dummy 효과 가장 큼
- **외래어 + 종결 (`~compiler 레포입니다`)**: 외래어 뒤 종결은 문제없이 처리

#### 2-4. 핵심 구조

```python
DUMMY_SUFFIX = " 네."
MIN_SILENCE_SEC = 0.25
SILENCE_THR = 200
TAIL_MARGIN_SEC = 0.10

for scene in scenes:
    text = scene.get("narration_tts") or scene["narration"]
    raw_path = f"_workspace/tts/_raw/seg_{scene['id']:02d}_raw.wav"
    out_path = f"_workspace/tts/seg_{scene['id']:02d}.wav"

    # 1. 더미 붙여 생성
    model.generate_voice_clone(
        text=text + DUMMY_SUFFIX,
        ref_audio=ref_audio, ref_text=ref_text, output_path=raw_path)

    # 2. envelope 역스캔으로 trim 지점 찾아 자르기
    trim_frame = find_trim_point(raw_path)  # 템플릿의 함수 그대로 사용
    # ... trimmed = frames[:trim_frame*...] 저장
```

상세 구현은 `scripts/generate_tts_template.py` 그대로 복사 사용.

**문장 단위 버전**: 자막을 문장 단위로 독립 싱크하려면 `scripts/generate_tts_per_sentence_template.py` 사용 — 각 문장을 별도 TTS 호출로 생성 후 250ms silence padding으로 concat, subtitleStartsSec를 실측 기반으로 수학적 계산. Whisper round-trip보다 정확하며 후처리 스크립트(extract_subtitle_timings.py) 불필요.

### 3. TTS 실행

```bash
cd <project>
python3 generate_tts.py
```

### 4. 타이밍 측정 스크립트 작성

`<project>/generate_timing.py`를 작성한다. 템플릿: `scripts/generate_timing_template.py`

핵심: 각 wav 파일의 **실제 오디오 길이를 측정**하여 timing.json을 생성한다. 스크립트에 지정된 시간이 아닌 실측값을 사용해야 음성 싱크가 정확하다.

**씬 간 패딩 0.6초 (마지막 씬은 0.3초)** — 씬 전환 시 목소리가 "잘리는 느낌" 방지. 과거 0.3초 고정이었으나 실사용에서 호흡이 부족하다는 피드백이 반복되어 표준을 상향 조정함. 마지막 씬만 짧게 유지하는 이유는 영상 말미에 불필요한 공백이 생기지 않도록 하기 위함.

```python
import wave, json, os

SCENE_PAD = 0.6       # 씬 간 여유 패딩 (전환 끊김 방지)
LAST_SCENE_PAD = 0.3  # 마지막 씬은 꼬리 공백 줄이기 위해 짧게

scene_plan = json.load(open("_workspace/scene_plan.json"))
scenes = scene_plan["scenes"]
timing = []
current_sec = 0.0

for i, scene in enumerate(scenes):
    wav_path = f"_workspace/tts/seg_{scene['id']:02d}.wav"
    with wave.open(wav_path, 'r') as w:
        audio_duration = w.getnframes() / w.getframerate()

    pad = LAST_SCENE_PAD if i == len(scenes) - 1 else SCENE_PAD
    duration = audio_duration + pad

    timing.append({
        "id": scene["id"],
        "startSec": round(current_sec, 3),
        "durationSec": round(duration, 3),
        "audioDuration": round(audio_duration, 3),  # wav 실측값 — 오디오 fade in/out에서 참조
        "subtitle": scene["subtitle"],
        "narration": scene["narration"],
        "visual_desc": scene.get("visual_note", "")
    })
    current_sec += duration

json.dump(timing, open("_workspace/timing.json", "w"), ensure_ascii=False, indent=2)
```

> **`audioDuration` 필드는 반드시 wav 실측값만 담는다 (패딩 제외).** vp-video-composer가 씬별 오디오 fade in/out을 계산할 때 "실제 음성이 끝나는 지점"을 알아야 하기 때문. 이 값이 없으면 패딩 구간까지 볼륨이 감쇠해 페이드 타이밍이 어긋난다.

### 5. 타이밍 실행 및 검증

```bash
cd <project>
python3 generate_timing.py
```

검증:
- 모든 `seg_XX.wav` 파일이 존재하는지 확인
- 각 세그먼트가 0.5초 이상, 30초 이하인지 확인
- timing.json의 씬 수가 scene_plan.json과 일치하는지 확인

### 6. 긴 세그먼트 알림

10초 초과 세그먼트 발견 시 `vp-image-artist`에게 SendMessage로 알린다:
> "씬 {id}의 오디오가 {duration}초입니다. 이미지 추가 생성이 필요합니다."

## 에러 핸들링

| 에러 | 대응 |
|------|------|
| 모델 미설치 | Fatal — "~/models/Qwen3-TTS-Base가 없습니다" 보고 |
| 특정 세그먼트 생성 실패 | 1회 재시도. 재실패 시 5초 무음 wav 생성 + 로그 기록 |
| 오디오 0.5초 미만 | 경고 로그 (내레이션이 너무 짧을 수 있음) |
| 오디오 30초 초과 | 경고 로그 (내레이션 분할 검토 필요) |
| Auto-trim silence gap 탐지 실패 | dummy_end에서 150ms 앞에서 자르는 fallback. 로그에 씬 id 표시 — 청취 확인 필요 |

## 검증 체크리스트

- [ ] 모든 seg_XX.wav 파일이 _workspace/tts/에 존재
- [ ] timing.json이 유효한 JSON
- [ ] timing.json 씬 수 = scene_plan.json 씬 수
- [ ] startSec가 순차 증가
- [ ] generate_tts.py, generate_timing.py가 프로젝트 루트에 저장됨
- [ ] **Gate A/B 통과**: 로그에 `[GATE-B FAIL]` 또는 `trim 거부` 가 없음
- [ ] **exit code 0**: `python3 generate_tts.py` 종료 코드 확인 (1이면 Gate B 실패)

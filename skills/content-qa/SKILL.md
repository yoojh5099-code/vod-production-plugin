---
name: content-qa
description: |
  YouTube 영상 제작 파이프라인의 산출물 9종이 서로 sync되어 있는지 검증하고, 깨진 sync는 자동으로 복구하는 스킬.
  스크립트(script/02_writer_script.md)를 수정한 직후, 사용자 녹음 후, video-production 진입 전, Studio 프리뷰가 어색할 때 등 sync 의심이 있을 때마다 호출한다.
  '/content-qa', 'qa', 'sync 확인', 'sync 검증', '대본 수정했어 sync해줘', '문서 sync', '파일 동기화', 'check sync' 요청 시 이 스킬을 사용한다.
  content-production 또는 video-production이 만든 모든 산출물이 검증 대상.
---

# Content QA — 산출물 Sync 검증·복구 스킬

YouTube 제작 파이프라인의 9개 산출물이 일관된 상태인지 검증하고, sync가 깨졌으면 자동 복구한다. content-production 7개 Phase + video-production 5개 Phase 사이에서 사용자가 임의로 파일을 수정해도 다시 sync 상태로 되돌릴 수 있게 하는 안전망.

## 언제 호출하는가

| 시점 | 검증할 layer | 자주 발생하는 위반 |
|---|---|---|
| **스크립트 다듬은 직후** | 1, 2, 4 | script narration ≠ scene_plan narration |
| **수동으로 scene_plan.json 편집했을 때** | 1, 3, 5 | id 깨짐, narration_tts 잔존 |
| **녹음 후 video-production 진입 전** | 6 | seg-NN.wav 누락 |
| **normalize_recordings.sh 실패 후** | 7 | tts/ 비어있거나 사양 불일치 |
| **Studio 음성-자막 어긋남** | 8, 9 | timing.json ≠ public/audio/timing.json |
| **/content-qa 호출** | **1~9 모두** | (전체 검증) |

## 검증 layer 9종

| # | Layer | 검증 내용 | Auto-fix |
|---|---|---|---|
| 1 | script ↔ scene_plan narration | `## H:MM — 라벨` 헤더 본문이 scene_plan.json `narration`과 1:1 일치 | ✅ |
| 2 | 씬 개수 일치 | script 헤더 개수 == scene_plan.json 씬 수 | ❌ (케이스 C 안내) |
| 3 | scene_plan id 무결성 | id가 1부터 연속, 중복·빈칸 없음 | ✅ |
| 4 | recording_guide ↔ scene_plan | 씬별 대본·발음표가 scene_plan 기준 최신 | ✅ (재생성) |
| 5 | narration_tts 잔존 검사 | 사용자 직접 녹음 워크플로엔 narration_tts 없어야 함 | ✅ (필드 제거) |
| 6 | audio/ ↔ scene_plan | `_workspace/audio/seg-NN.wav` 가 모든 씬에 존재 | ❌ (사용자 녹음 필요) |
| 7 | tts/ 사양 + 씬 수 | 24kHz/mono/16-bit, audio/와 동일 씬 수 | ✅ (normalize 재실행) |
| 8 | timing.json 실측 | audioDuration이 실제 wav 길이와 ±0.05s 이내 | ✅ (generate_timing 재실행) |
| 9 | Remotion sync | `*-video/public/audio/` 의 wav·timing.json이 _workspace와 identical | ✅ (Phase 2 sync 재실행) |

## 사용법

```bash
# Dry-run (기본 — 변경 없이 sync 상태만 보고)
python3 ~/.claude/skills/content-qa/scripts/check_sync.py <project>

# 자동 복구 (auto-fixable layer만 실제로 변경)
python3 ~/.claude/skills/content-qa/scripts/check_sync.py <project> --apply

# 특정 layer만 검사
python3 ~/.claude/skills/content-qa/scripts/check_sync.py <project> --layers 1,2,4
```

산출물:
- 콘솔에 layer별 PASS / WARN / FAIL 리포트
- `<project>/_workspace/qa_report.md` — 마지막 실행 결과 영구 기록 (사용자가 추후 검토 가능)

## 워크플로우 (오케스트레이터로 실행할 때)

오케스트레이터(claude code 자체)가 이 스킬을 호출했을 때:

1. **dry-run으로 먼저 실행** — `check_sync.py <project>` (수정 없이)
2. **결과 분석**
   - 모든 layer PASS → "sync OK" 보고하고 종료
   - 1개 이상 FAIL이지만 모두 auto-fix 가능 → 사용자에게 "이런 sync 위반을 자동 복구할 거예요" 보고 + 승인 요청
   - auto-fix 불가 FAIL (layer 2, 6) → 사용자에게 어떤 액션 필요한지 안내 (씬 분할 재실행 / 녹음 보강)
3. **사용자 승인 후 `--apply` 재실행**
4. **재검증** — dry-run 한 번 더 돌려서 모든 layer PASS 확인
5. 사용자에게 최종 리포트 (`qa_report.md` 경로 안내)

## 케이스별 대응 가이드

### 케이스 A: 문장 다듬기 (의미 동일)
- Layer 1만 FAIL 예상
- `--apply` 한 번이면 끝

### 케이스 B: 톤 변경 (핵심 메시지 어조 시프트)
- Layer 1 FAIL + 추가로 SEO·썸네일 재검토 권장
- `check_sync.py`는 톤 변경 자동 탐지 못함 (의미론적 검증은 LLM 영역)
- 콘솔 리포트 끝에 "톤이 바뀐 것 같으면 cp-seo-optimizer 와 cp-thumbnail-planner 를 재실행하세요" 안내 출력

### 케이스 C: 씬 구조 변경 (씬 추가/삭제/순서)
- Layer 2 FAIL — auto-fix 불가
- 콘솔 리포트: "씬 분할이 다시 필요. /content-production Phase 6 재실행 권장"
- 다른 layer는 검증 skip (씬 매핑이 무너진 상태에서 검사 무의미)

### 케이스 D: 녹음 누락
- Layer 6 FAIL — auto-fix 불가
- 콘솔 리포트: "씬 N이 audio/ 에 없음. recording_guide.md §5 참고해서 추가 녹음 후 다시 호출"

### 케이스 E: Remotion 음성-자막 어긋남
- Layer 8 또는 9 FAIL 예상
- `--apply` 로 timing 재측정 + Phase 2 sync 자동 실행
- Studio 핫리로드로 즉시 확인 가능

## 데이터 흐름

```
[사용자 임의 수정]
   script/02_writer_script.md, scene_plan.json 등 임의 편집
       ↓
[/content-qa 호출]
       ↓
   Layer 1~9 검증 (dry-run)
       ↓
   FAIL 발견 → 사용자 승인 → --apply
       ↓
   Auto-fix 가능한 것만 자동 복구:
   - script narration → scene_plan narration 동기화
   - scene_plan id 재정렬
   - recording_guide.md 재생성 (generate_recording_guide.py)
   - narration_tts 필드 제거
   - tts/ 재정규화 (normalize_recordings.sh)
   - timing.json 재측정 (generate_timing.py)
   - public/audio/ 동기화 (Phase 2 sync)
       ↓
   재검증 → 모든 layer PASS
       ↓
   qa_report.md 산출
```

## 에러 핸들링

| 상황 | 대응 |
|------|------|
| 프로젝트에 scene_plan.json 없음 | "/content-production Phase 6 먼저 실행" 안내 후 종료 |
| script/02_writer_script.md 없음 | "/content-production Phase 3 먼저 실행" 안내 후 종료 |
| 헤더 패턴 불일치 (`## H:MM — 라벨` 아님) | 어떤 헤더를 못 찾았는지 보고. layer 1·2·4 skip |
| Layer 1 FAIL인데 씬 개수 일치 + narration 모두 존재 | 정상 동기화 가능 |
| Layer 2 FAIL (씬 개수 다름) | layer 1·4 skip — sync 안 함, 케이스 C 안내 |
| Layer 6 FAIL (audio 누락) | layer 7·8·9 skip — 녹음이 먼저 |
| Remotion 디렉터리 없음 | layer 9 skip — 정상 (Phase 3 미실행) |

## 테스트 시나리오

### 정상 흐름 (모든 layer PASS)
- 입력: 깨끗하게 sync된 프로젝트
- 기대: 9개 layer 모두 PASS, "sync OK" 보고

### 스크립트 다듬은 후 (Layer 1 FAIL)
- 입력: script 한 씬 narration 문장 다듬음, scene_plan.json은 미수정
- 기대: dry-run에서 Layer 1 FAIL + 변경 diff 출력. --apply 후 동기화 + recording_guide 재생성. 재검증 PASS.

### 씬 추가 (Layer 2 FAIL)
- 입력: script에 씬 1개 추가, scene_plan은 그대로
- 기대: Layer 2 FAIL 보고 + "/content-production Phase 6 재실행" 안내. layer 1·4 skip.

### 녹음 누락 (Layer 6 FAIL)
- 입력: 5씬 영상인데 audio/에 4개만
- 기대: Layer 6 FAIL + 누락 씬 ID 보고. layer 7·8·9 skip.

## 관련 스킬

- `content-production` — 산출물 1~5 생성 (script, scene_plan, recording_guide 등)
- `video-production` — 산출물 6~9 생성 (audio, tts, timing.json, Remotion sync)
- 두 스킬 사이 어디서나 호출 가능. 사용자가 직접 파일을 수정하는 모든 시점이 트리거.

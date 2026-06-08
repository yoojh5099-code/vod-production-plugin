#!/usr/bin/env python3
"""scene_plan.json → recording_guide.md 산출.

cp-scene-architect가 만든 scene_plan.json을 읽어 사용자 직접 녹음용 가이드를
생성한다. 산출물은 콘텐츠 팀의 마지막 산출물로, 사용자가 Audacity를 켜고
녹음만 하면 video-production으로 그대로 흘러갈 수 있도록 정보를 모은다.

사용법:
    python3 generate_recording_guide.py [<project_root>]

기본 project_root는 현재 디렉터리.

산출:
    <project_root>/_workspace/recording_guide.md

검증:
    - scene_plan.json 존재
    - 모든 씬에 narration / subtitle / id 필드 존재
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# 영문 브랜드 → 한국어 발음 표 (사용자 직접 녹음용)
# voice-production의 narration_tts 치환 맵과 다름:
# - 사람은 영문을 자기 식으로 자연스럽게 읽으므로 발음만 안내
# - "꼭 이렇게 읽어야 함"이 아니라 "낭독 흐름에 자연스럽게 녹이도록 1회 연습 권장"
DEFAULT_PRONUNCIATION_GUIDE = [
    ("Claude Code", "클로드 코드"),
    ("Claude Pro", "클로드 프로"),
    ("Claude Opus 4.7", "클로드 오퍼스 사점칠"),
    ("Opus 4.7", "오퍼스 사점칠"),
    ("Claude", "클로드"),
    ("Codex", "코덱스"),
    ("OpenCode", "오픈코드"),
    ("OpenRouter", "오픈라우터"),
    ("OpenAI", "오픈에이아이"),
    ("Anthropic", "앤트로픽"),
    ("ChatGPT Plus", "챗지피티 플러스"),
    ("ChatGPT Pro", "챗지피티 프로"),
    ("Gemini", "제미나이"),
    ("Figma", "피그마"),
    ("Datadog", "데이터독"),
    ("Canva", "캔바"),
    ("Adobe", "어도비"),
    ("AWS", "에이더블유에스"),
    ("API", "에이피아이"),
    ("AI", "에이아이"),
    ("PM", "피엠"),
    ("URL", "유알엘"),
]


def detect_brands_in_scenes(scenes: list[dict], guide: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """씬 전체 narration에서 실제 등장하는 브랜드만 추려 가이드 표를 만든다."""
    full_text = "\n".join(s.get("narration", "") for s in scenes)
    detected: list[tuple[str, str]] = []
    seen: set[str] = set()
    for en, ko in guide:
        if en in full_text and en not in seen:
            detected.append((en, ko))
            seen.add(en)
    return detected


def estimate_duration_sec(narration: str) -> float:
    """한국어 평균 350~400자/분 기준으로 발화 시간 추정. 글자 수만 사용."""
    char_count = len(re.sub(r"\s", "", narration))
    return round(char_count / (375 / 60), 1)


def render(plan: dict, project_root: Path) -> str:
    scenes = plan["scenes"]
    meta = plan.get("meta", {})
    title = meta.get("title", "(제목 미정)")
    pronunciation = detect_brands_in_scenes(scenes, DEFAULT_PRONUNCIATION_GUIDE)

    total_estimated = sum(
        s.get("estimated_duration_sec") or estimate_duration_sec(s.get("narration", ""))
        for s in scenes
    )
    total_min = int(total_estimated // 60)
    total_sec = int(total_estimated % 60)

    lines: list[str] = []
    lines.append(f"# 녹음 가이드 — {title}\n")
    lines.append(f"- 씬 수: **{len(scenes)}**")
    lines.append(f"- 추정 본편 길이: **약 {total_min}분 {total_sec}초** (실측은 timing.json)")
    lines.append(f"- 저장 위치: `_workspace/audio/seg-NN.wav`")
    lines.append("")

    lines.append("## 1. wav 파일 사양 (필수)\n")
    lines.append("| 항목 | 값 | 비고 |")
    lines.append("|---|---|---|")
    lines.append("| 포맷 | WAV PCM | Audacity Export → \"WAV (Microsoft) 16-bit PCM\" |")
    lines.append("| 샘플레이트 | **24000 Hz 권장** | 다른 값으로 녹음해도 video-production이 일괄 변환함 |")
    lines.append("| 채널 | **모노 권장** | 스테레오로 녹음해도 자동 mono down-mix |")
    lines.append("| 비트심도 | 16-bit signed PCM | |")
    lines.append("| 파일명 | `seg-01.wav` ~ `seg-NN.wav` | scene_plan.json `id` 기준 0-padded 2자리 |")
    lines.append("| 저장 위치 | `_workspace/audio/` | video-production이 자동으로 `_workspace/tts/`로 정규화 복사 |")
    lines.append("")

    lines.append("## 2. Audacity 셋업 (한 번만)\n")
    lines.append("1. **Edit → Preferences → Recording** — \"Software Playthrough\" 끔, \"Sound Activated Recording\" 끔")
    lines.append("2. **좌하단 Project Rate** = `24000` 권장 (44100Hz도 허용 — 자동 변환됨)")
    lines.append("3. **Tracks → New → Mono Track**")
    lines.append("4. 입력 게인: 평소 발화 시 피크가 -12dB ~ -6dB 사이에 들어오도록. 빨간 클립 절대 금지")
    lines.append("5. 마이크 위치: 입에서 15~20cm, 약간 비스듬히. 팝 필터 권장")
    lines.append("6. 환경: 에어컨/팬 끄고, 키보드/마우스 클릭 소리 차단")
    lines.append("")

    lines.append("## 3. 톤 가이드\n")
    lines.append("- 담백·실용적, 1인칭 (\"저는\", \"제 경험으로는\")")
    lines.append("- 빨리 읽기 금지. 분당 약 350~400자 페이스")
    lines.append("- 단정·하입 금지 (\"최고\", \"100%\", \"역대급\" X)")
    lines.append("- 시점부 평가 톤 (\"2026년 5월 기준으로는…\")")
    lines.append("")

    if pronunciation:
        lines.append("## 4. 영문 브랜드 발음 가이드 (이 영상에 등장하는 것만)\n")
        lines.append("사람이 직접 읽으므로 \"꼭 이렇게\"가 아니라 \"녹음 흐름에 자연스럽게 녹이도록 1회 발화 연습\"이면 충분.\n")
        lines.append("| 표기 | 발음 |")
        lines.append("|---|---|")
        for en, ko in pronunciation:
            lines.append(f"| {en} | {ko} |")
        lines.append("")

    lines.append("## 5. 씬별 대본 (낭독용)\n")
    lines.append("씬 1개 = 파일 1개. 한 호흡에 못 가면 그 씬만 다시 찍는다. 다른 씬 영향 없음.\n")

    for s in scenes:
        sid = s["id"]
        narration = s.get("narration", "").strip()
        subtitle = s.get("subtitle", "").strip()
        est = s.get("estimated_duration_sec") or estimate_duration_sec(narration)
        filename = f"seg-{sid:02d}.wav"
        lines.append(f"### 씬 {sid:02d} — `{filename}`")
        lines.append(f"- 추정 길이: 약 {est:.1f}초 ({len(re.sub(r'[\\s]', '', narration))}자)")
        if subtitle:
            lines.append(f"- 자막: {subtitle}")
        lines.append("")
        lines.append("> " + narration.replace("\n", "\n> "))
        lines.append("")

    lines.append("## 6. 녹음 후 검증 체크리스트\n")
    lines.append(f"- [ ] `_workspace/audio/` 안에 `seg-01.wav` ~ `seg-{len(scenes):02d}.wav` 가 빠짐없이 존재")
    lines.append("- [ ] 각 씬 0.5초 이상, 30초 이하")
    lines.append("- [ ] 클리핑 없음 (피크 < 0dB)")
    lines.append("- [ ] 톤·볼륨 균일 (씬 1과 마지막 씬을 연속 재생해 들어보기)")
    lines.append("- [ ] 끝음(\"~요\", \"~다\") 잘림 없는지 확인")
    lines.append("")
    lines.append("## 7. 다음 단계\n")
    lines.append("녹음이 끝나면 다음 메시지로 진행:\n")
    lines.append("> \"녹음 끝났어. video-production 돌려줘\"\n")
    lines.append("video-production이 자동으로:")
    lines.append("1. `_workspace/audio/*.wav` → `_workspace/tts/*.wav` 정규화 (24kHz/mono/16-bit, 무음 trim, 100ms 패딩)")
    lines.append("2. `_workspace/timing.json` 생성 (실측 wav 길이 기반)")
    lines.append("3. Remotion 프로젝트 조립")
    lines.append("4. Studio 프리뷰 + 사용자 승인 → 최종 렌더")

    return "\n".join(lines)


def main(argv: list[str]) -> int:
    project_root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    plan_path = project_root / "_workspace" / "scene_plan.json"
    if not plan_path.exists():
        print(f"[FATAL] scene_plan.json 없음: {plan_path}", file=sys.stderr)
        return 1

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    scenes = plan.get("scenes")
    if not scenes:
        print("[FATAL] scene_plan.json 에 scenes 배열 없음", file=sys.stderr)
        return 1

    for s in scenes:
        if "id" not in s or "narration" not in s:
            print(f"[FATAL] 씬에 id 또는 narration 없음: {s}", file=sys.stderr)
            return 1

    output = render(plan, project_root)
    out_path = project_root / "_workspace" / "recording_guide.md"
    out_path.write_text(output, encoding="utf-8")
    print(f"[OK] {out_path} 생성 ({len(scenes)}씬)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

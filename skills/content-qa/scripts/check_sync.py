#!/usr/bin/env python3
"""content-qa — 영상 제작 산출물 9 layer sync 검증 + 자동 복구.

사용법:
    python3 check_sync.py <project> [--apply] [--layers 1,2,4]

기본은 dry-run (수정 없이 리포트만). --apply 시 auto-fixable layer 실제 변경.

산출:
    <project>/_workspace/qa_report.md
    + 콘솔 layer별 PASS/WARN/FAIL/SKIP 보고

종료 코드:
    0 = 모든 layer PASS 또는 dry-run에서 fixable FAIL만 (사용자 결정 필요)
    1 = auto-fix 불가 FAIL 존재 (layer 2, 6 등 — 사용자 액션 필요)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import wave
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

# ===== 공용 데이터 모델 =====

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"
SKIP = "SKIP"


@dataclass
class LayerResult:
    layer: int
    name: str
    status: str
    summary: str
    details: list[str] = field(default_factory=list)
    auto_fixable: bool = False
    fixed: bool = False


# ===== 유틸 =====

TIME_HEADER_RE = re.compile(r"^##\s+(\d+):(\d{2})\s*[—–\-]\s*(.+?)\s*$")
ANY_H2_RE = re.compile(r"^##\s+", re.MULTILINE)


def parse_script(path: Path) -> list[dict]:
    """script/02_writer_script.md 의 시간 헤더 + 본문 추출.

    헤더 형식: '## 0:12 — 정의' 또는 '## 0:12 - 정의' (em-dash 또는 hyphen)
    본문: 다음 ## 헤더 직전까지 (시간 헤더든 다른 ## 헤더든 모두 본문 종료 지점).
    이렇게 해야 마지막 씬 뒤에 '## 핵심 키워드' 같은 메타 섹션이 본문에 섞이지 않음.
    """
    text = path.read_text(encoding="utf-8")
    # 모든 ## 헤더 위치
    h2_positions = [m.start() for m in ANY_H2_RE.finditer(text)]
    # 시간 헤더만 골라내기
    time_headers = []
    for m in re.finditer(r"^##\s+.+$", text, re.MULTILINE):
        tm = TIME_HEADER_RE.match(m.group(0))
        if tm:
            time_headers.append((m.start(), m.end(), tm))

    sections = []
    for i, (start_pos, end_pos, tm) in enumerate(time_headers):
        # 다음 ## 헤더 (어떤 종류든) 직전까지가 본문
        next_h2 = next((p for p in h2_positions if p > start_pos), len(text))
        body = text[end_pos:next_h2].strip()
        body = "\n".join(line for line in body.splitlines() if line.strip())
        if not body:
            continue
        sections.append({
            "time_label": f"{tm.group(1)}:{tm.group(2)}",
            "label": tm.group(3).strip(),
            "narration": body,
        })
    return sections


def normalize_text(s: str) -> str:
    """비교용 정규화 — 공백/줄바꿈/구두점 미세 차이 흡수."""
    s = re.sub(r"\s+", " ", s).strip()
    return s


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def find_remotion_dir(project: Path) -> Path | None:
    candidates = sorted(project.glob("*-video"))
    for c in candidates:
        if c.is_dir():
            return c
    return None


def get_wav_duration(path: Path) -> float:
    with wave.open(str(path), "r") as w:
        return w.getnframes() / w.getframerate()


def get_wav_sr_ch_bits(path: Path) -> tuple[int, int, int]:
    with wave.open(str(path), "r") as w:
        return w.getframerate(), w.getnchannels(), w.getsampwidth() * 8


# ===== Layer 1: script ↔ scene_plan narration =====

def layer1_script_scene_narration(project: Path, apply: bool) -> LayerResult:
    name = "script ↔ scene_plan narration"
    script_path = project / "script" / "02_writer_script.md"
    plan_path = project / "_workspace" / "scene_plan.json"
    if not script_path.exists() or not plan_path.exists():
        return LayerResult(1, name, SKIP, "script 또는 scene_plan.json 없음", auto_fixable=False)

    sections = parse_script(script_path)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    scenes = plan.get("scenes", [])

    if len(sections) != len(scenes):
        return LayerResult(
            1, name, SKIP,
            f"씬 개수 불일치(script {len(sections)} vs plan {len(scenes)}) — Layer 2 위임",
            auto_fixable=False,
        )

    # narration 본문에서 인용 표시(>) 제거 후 비교
    def clean_quote(s: str) -> str:
        return "\n".join(line.lstrip("> ").strip() for line in s.splitlines() if line.strip())

    diffs = []
    for sec, scene in zip(sections, scenes):
        script_narr = normalize_text(clean_quote(sec["narration"]))
        plan_narr = normalize_text(scene.get("narration", ""))
        if script_narr != plan_narr:
            diffs.append({
                "id": scene.get("id"),
                "label": sec["label"],
                "script": clean_quote(sec["narration"])[:120],
                "plan": scene.get("narration", "")[:120],
            })

    if not diffs:
        return LayerResult(1, name, PASS, f"{len(scenes)}씬 모두 일치", auto_fixable=True)

    details = [f"씬 {d['id']} ({d['label']}):" for d in diffs]
    for d in diffs:
        details.append(f"  - script: {d['script']}")
        details.append(f"  - plan:   {d['plan']}")

    if apply:
        # script narration을 plan에 반영
        for sec, scene in zip(sections, scenes):
            scene["narration"] = clean_quote(sec["narration"])
        plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        return LayerResult(
            1, name, PASS,
            f"{len(diffs)}개 씬 narration을 script 기준으로 동기화 완료",
            details=details, auto_fixable=True, fixed=True,
        )
    return LayerResult(
        1, name, FAIL,
        f"{len(diffs)}개 씬에서 narration 불일치 (--apply 시 자동 동기화)",
        details=details, auto_fixable=True,
    )


# ===== Layer 2: 씬 개수 일치 =====

def layer2_scene_count(project: Path, apply: bool) -> LayerResult:
    name = "씬 개수 일치"
    script_path = project / "script" / "02_writer_script.md"
    plan_path = project / "_workspace" / "scene_plan.json"
    if not script_path.exists() or not plan_path.exists():
        return LayerResult(2, name, SKIP, "script 또는 scene_plan.json 없음")

    sections = parse_script(script_path)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    scenes = plan.get("scenes", [])

    if len(sections) == len(scenes):
        return LayerResult(2, name, PASS, f"{len(sections)}씬 일치")
    return LayerResult(
        2, name, FAIL,
        f"script {len(sections)}씬 ≠ scene_plan {len(scenes)}씬 — auto-fix 불가",
        details=[
            "씬 구조가 변경됨 (케이스 C).",
            "→ /content-production Phase 6 (cp-scene-architect) 재실행 권장",
            "→ 또는 script의 헤더 구조가 깨졌는지 확인 (## H:MM — 라벨)",
        ],
        auto_fixable=False,
    )


# ===== Layer 3: scene_plan id 무결성 =====

def layer3_scene_id_integrity(project: Path, apply: bool) -> LayerResult:
    name = "scene_plan id 무결성"
    plan_path = project / "_workspace" / "scene_plan.json"
    if not plan_path.exists():
        return LayerResult(3, name, SKIP, "scene_plan.json 없음")

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    scenes = plan.get("scenes", [])
    ids = [s.get("id") for s in scenes]
    expected = list(range(1, len(scenes) + 1))

    if ids == expected:
        return LayerResult(3, name, PASS, f"id 1~{len(scenes)} 연속")

    if apply:
        for i, scene in enumerate(scenes, start=1):
            scene["id"] = i
        plan["meta"]["total_scenes"] = len(scenes)
        plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        return LayerResult(
            3, name, PASS,
            f"id를 1~{len(scenes)} 1-base로 재정렬 완료",
            details=[f"이전: {ids[:10]}{'...' if len(ids) > 10 else ''}"],
            auto_fixable=True, fixed=True,
        )
    return LayerResult(
        3, name, FAIL,
        f"id가 1-base 연속이 아님 (현재: {ids[:10]}{'...' if len(ids) > 10 else ''})",
        details=["--apply 시 1~N으로 재정렬"],
        auto_fixable=True,
    )


# ===== Layer 4: recording_guide ↔ scene_plan =====

def layer4_recording_guide(project: Path, apply: bool) -> LayerResult:
    name = "recording_guide ↔ scene_plan"
    plan_path = project / "_workspace" / "scene_plan.json"
    guide_path = project / "_workspace" / "recording_guide.md"

    if not plan_path.exists():
        return LayerResult(4, name, SKIP, "scene_plan.json 없음")

    if not guide_path.exists():
        if apply:
            return _regenerate_recording_guide(project, name, "recording_guide.md 생성됨", auto_fixable=True)
        return LayerResult(
            4, name, FAIL,
            "recording_guide.md 없음 (--apply 시 자동 생성)",
            auto_fixable=True,
        )

    # 간이 검증: scene_plan의 narration이 recording_guide §5에 모두 등장하는지
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    guide_text = guide_path.read_text(encoding="utf-8")
    missing = []
    for s in plan.get("scenes", []):
        narr_head = s.get("narration", "")[:30].strip()
        if narr_head and narr_head not in guide_text:
            missing.append((s.get("id"), narr_head))

    if not missing:
        # plan보다 guide의 mtime이 오래된 경우만 경고
        if guide_path.stat().st_mtime < plan_path.stat().st_mtime:
            if apply:
                return _regenerate_recording_guide(
                    project, name,
                    "scene_plan이 더 최신이라 recording_guide 재생성",
                    auto_fixable=True,
                )
            return LayerResult(
                4, name, WARN,
                "내용은 일치하지만 scene_plan보다 guide가 오래됨 (--apply 시 재생성)",
                auto_fixable=True,
            )
        return LayerResult(4, name, PASS, "recording_guide 최신 + 내용 일치")

    if apply:
        return _regenerate_recording_guide(
            project, name,
            f"{len(missing)}개 씬 누락 → 재생성 완료",
            auto_fixable=True,
            details=[f"누락 씬 {sid}: {head!r}..." for sid, head in missing[:5]],
        )
    return LayerResult(
        4, name, FAIL,
        f"{len(missing)}개 씬 narration이 guide에 없음 (--apply 시 재생성)",
        details=[f"씬 {sid}: {head!r}..." for sid, head in missing[:5]],
        auto_fixable=True,
    )


def _regenerate_recording_guide(project: Path, name: str, summary: str, **kw) -> LayerResult:
    script = Path.home() / ".claude/skills/content-production/scripts/generate_recording_guide.py"
    res = run(["python3", str(script), str(project)])
    details = list(kw.get("details", []))
    if res.returncode != 0:
        return LayerResult(
            4, name, FAIL,
            f"generate_recording_guide.py 실패 (exit {res.returncode})",
            details=details + [res.stderr.strip()[:200]],
            auto_fixable=True,
        )
    details.append(res.stdout.strip())
    return LayerResult(4, name, PASS, summary, details=details, auto_fixable=True, fixed=True)


# ===== Layer 5: narration_tts 잔존 검사 =====

def layer5_narration_tts_check(project: Path, apply: bool) -> LayerResult:
    name = "narration_tts 잔존 검사"
    plan_path = project / "_workspace" / "scene_plan.json"
    if not plan_path.exists():
        return LayerResult(5, name, SKIP, "scene_plan.json 없음")

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    has_tts = [s.get("id") for s in plan.get("scenes", []) if "narration_tts" in s]

    if not has_tts:
        return LayerResult(5, name, PASS, "narration_tts 필드 없음 (사람 녹음 워크플로 정합)")

    if apply:
        for s in plan.get("scenes", []):
            s.pop("narration_tts", None)
        plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        return LayerResult(
            5, name, PASS,
            f"{len(has_tts)}개 씬에서 narration_tts 제거 완료",
            details=[f"제거된 씬: {has_tts}"],
            auto_fixable=True, fixed=True,
        )
    return LayerResult(
        5, name, FAIL,
        f"{len(has_tts)}개 씬에 narration_tts 잔존 (--apply 시 제거)",
        details=[f"잔존 씬: {has_tts}"],
        auto_fixable=True,
    )


# ===== Layer 6: audio/ ↔ scene_plan =====

def layer6_audio_completeness(project: Path, apply: bool) -> LayerResult:
    name = "audio/ ↔ scene_plan"
    plan_path = project / "_workspace" / "scene_plan.json"
    audio_dir = project / "_workspace" / "audio"
    if not plan_path.exists():
        return LayerResult(6, name, SKIP, "scene_plan.json 없음")
    if not audio_dir.exists():
        return LayerResult(
            6, name, FAIL,
            f"_workspace/audio/ 디렉터리 없음 — 사용자 녹음 필요",
            details=["recording_guide.md §5 참고해서 녹음 후 다시 실행"],
            auto_fixable=False,
        )

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    expected_ids = [s["id"] for s in plan.get("scenes", [])]
    missing = []
    for sid in expected_ids:
        # seg-01.wav 또는 seg_01.wav 둘 다 허용
        candidates = list(audio_dir.glob(f"seg-{sid:02d}.wav")) + list(audio_dir.glob(f"seg_{sid:02d}.wav"))
        if not candidates:
            missing.append(sid)

    if not missing:
        return LayerResult(6, name, PASS, f"{len(expected_ids)}개 씬 모두 녹음됨")

    return LayerResult(
        6, name, FAIL,
        f"{len(missing)}개 씬 녹음 누락 — 사용자 액션 필요",
        details=[f"누락 씬 ID: {missing}", "→ recording_guide.md 참고해서 추가 녹음"],
        auto_fixable=False,
    )


# ===== Layer 7: tts/ 사양 + 씬 수 =====

def layer7_tts_normalization(project: Path, apply: bool) -> LayerResult:
    name = "tts/ 사양 + 씬 수"
    audio_dir = project / "_workspace" / "audio"
    tts_dir = project / "_workspace" / "tts"
    plan_path = project / "_workspace" / "scene_plan.json"

    if not plan_path.exists():
        return LayerResult(7, name, SKIP, "scene_plan.json 없음")

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    expected_ids = [s["id"] for s in plan.get("scenes", [])]

    audio_count = len(list(audio_dir.glob("seg-*.wav"))) + len(list(audio_dir.glob("seg_*.wav"))) if audio_dir.exists() else 0
    if audio_count == 0:
        return LayerResult(7, name, SKIP, "audio/ 비어있음 — Layer 6 위임")

    issues = []
    if not tts_dir.exists() or not list(tts_dir.glob("seg_*.wav")):
        issues.append(f"tts/ 비어있음 (audio/ 는 {audio_count}개)")
    else:
        tts_files = sorted(tts_dir.glob("seg_*.wav"))
        if len(tts_files) != len(expected_ids):
            issues.append(f"tts/ 파일 {len(tts_files)} ≠ 씬 {len(expected_ids)}")
        for f in tts_files:
            sr, ch, bits = get_wav_sr_ch_bits(f)
            if (sr, ch, bits) != (24000, 1, 16):
                issues.append(f"{f.name}: {sr}Hz/{ch}ch/{bits}bit (표준 24000/1/16 아님)")

    if not issues:
        return LayerResult(7, name, PASS, f"{len(expected_ids)}개 wav 모두 24kHz/mono/16-bit")

    if apply:
        script = Path.home() / ".claude/skills/video-production/scripts/normalize_recordings.sh"
        res = run([str(script), str(project)])
        if res.returncode != 0:
            return LayerResult(
                7, name, FAIL,
                f"normalize_recordings.sh 실패 (exit {res.returncode})",
                details=issues + [res.stderr.strip()[:200]],
                auto_fixable=True,
            )
        return LayerResult(
            7, name, PASS,
            "normalize_recordings.sh 재실행 완료",
            details=issues,
            auto_fixable=True, fixed=True,
        )
    return LayerResult(
        7, name, FAIL,
        f"{len(issues)}건 사양 불일치 (--apply 시 normalize 재실행)",
        details=issues,
        auto_fixable=True,
    )


# ===== Layer 8: timing.json 실측 =====

def layer8_timing_accuracy(project: Path, apply: bool) -> LayerResult:
    name = "timing.json 실측"
    timing_path = project / "_workspace" / "timing.json"
    tts_dir = project / "_workspace" / "tts"

    if not timing_path.exists() or not tts_dir.exists() or not list(tts_dir.glob("seg_*.wav")):
        return LayerResult(8, name, SKIP, "timing.json 또는 tts/ 없음")

    timing = json.loads(timing_path.read_text(encoding="utf-8"))
    drift = []
    for entry in timing:
        sid = entry["id"]
        wav = tts_dir / f"seg_{sid:02d}.wav"
        if not wav.exists():
            drift.append(f"씬 {sid}: wav 누락")
            continue
        actual = get_wav_duration(wav)
        recorded = entry.get("audioDuration", 0)
        if abs(actual - recorded) > 0.05:
            drift.append(f"씬 {sid}: 실측 {actual:.3f}s vs 기록 {recorded:.3f}s (Δ{abs(actual-recorded):.3f}s)")

    if not drift:
        return LayerResult(8, name, PASS, f"{len(timing)}개 씬 timing 정확 (Δ ≤ 0.05s)")

    if apply:
        script = Path.home() / ".claude/skills/video-production/scripts/generate_timing.py"
        res = run(["python3", str(script), str(project)])
        if res.returncode != 0:
            return LayerResult(
                8, name, FAIL,
                f"generate_timing.py 실패 (exit {res.returncode})",
                details=drift + [res.stderr.strip()[:200]],
                auto_fixable=True,
            )
        return LayerResult(
            8, name, PASS,
            "timing.json 재측정 완료",
            details=drift,
            auto_fixable=True, fixed=True,
        )
    return LayerResult(
        8, name, FAIL,
        f"{len(drift)}건 timing drift (--apply 시 재측정)",
        details=drift[:10],
        auto_fixable=True,
    )


# ===== Layer 9: Remotion sync =====

def layer9_remotion_sync(project: Path, apply: bool) -> LayerResult:
    name = "Remotion public/audio sync"
    remotion_dir = find_remotion_dir(project)
    if remotion_dir is None:
        return LayerResult(9, name, SKIP, "Remotion 프로젝트 없음 (Phase 3 미실행)")

    public_audio = remotion_dir / "public" / "audio"
    tts_dir = project / "_workspace" / "tts"
    timing_src = project / "_workspace" / "timing.json"
    timing_dst = public_audio / "timing.json"

    if not tts_dir.exists() or not list(tts_dir.glob("seg_*.wav")):
        return LayerResult(9, name, SKIP, "tts/ 비어있음 — Layer 7 위임")

    issues = []
    if not public_audio.exists():
        issues.append("public/audio/ 디렉터리 없음")
    else:
        # wav 파일 개수·길이 비교
        for wav in sorted(tts_dir.glob("seg_*.wav")):
            dst = public_audio / wav.name
            if not dst.exists():
                issues.append(f"{wav.name} 미동기화")
                continue
            src_dur = get_wav_duration(wav)
            dst_dur = get_wav_duration(dst)
            if abs(src_dur - dst_dur) > 0.01:
                issues.append(f"{wav.name}: src {src_dur:.3f}s vs public {dst_dur:.3f}s")

        # timing.json 비교
        if not timing_dst.exists():
            issues.append("public/audio/timing.json 미동기화")
        elif timing_src.exists() and timing_src.read_bytes() != timing_dst.read_bytes():
            issues.append("timing.json 내용 불일치")

    if not issues:
        return LayerResult(9, name, PASS, "Remotion sync OK")

    if apply:
        public_audio.mkdir(parents=True, exist_ok=True)
        for wav in tts_dir.glob("seg_*.wav"):
            shutil.copy2(wav, public_audio / wav.name)
        if timing_src.exists():
            shutil.copy2(timing_src, timing_dst)
        # update_scenes_ts.py 가 있으면 실행
        sync_script = project / "update_scenes_ts.py"
        details = list(issues)
        if sync_script.exists():
            res = run(["python3", str(sync_script)], cwd=project)
            if res.returncode != 0:
                details.append(f"update_scenes_ts.py 실패: {res.stderr.strip()[:200]}")
            else:
                details.append("update_scenes_ts.py 실행 완료")
        return LayerResult(
            9, name, PASS,
            "Remotion public/audio 재동기화 완료",
            details=details,
            auto_fixable=True, fixed=True,
        )
    return LayerResult(
        9, name, FAIL,
        f"{len(issues)}건 sync 불일치 (--apply 시 재동기화)",
        details=issues[:10],
        auto_fixable=True,
    )


# ===== 오케스트레이션 =====

LAYERS: list[tuple[int, str, Callable]] = [
    (1, "script ↔ scene_plan narration", layer1_script_scene_narration),
    (2, "씬 개수 일치", layer2_scene_count),
    (3, "scene_plan id 무결성", layer3_scene_id_integrity),
    (4, "recording_guide ↔ scene_plan", layer4_recording_guide),
    (5, "narration_tts 잔존 검사", layer5_narration_tts_check),
    (6, "audio/ ↔ scene_plan", layer6_audio_completeness),
    (7, "tts/ 사양 + 씬 수", layer7_tts_normalization),
    (8, "timing.json 실측", layer8_timing_accuracy),
    (9, "Remotion public/audio sync", layer9_remotion_sync),
]


def render_console(results: list[LayerResult], apply: bool) -> None:
    badge = {PASS: "✅", WARN: "⚠️ ", FAIL: "❌", SKIP: "⏭️ "}
    print()
    print("=" * 70)
    print("Content QA — Sync Verification" + (" (APPLIED)" if apply else " (DRY-RUN)"))
    print("=" * 70)
    for r in results:
        fixed_mark = " (자동복구됨)" if r.fixed else ""
        print(f"{badge[r.status]} Layer {r.layer}: {r.name} — {r.summary}{fixed_mark}")
        for d in r.details[:8]:
            print(f"     {d}")
        if len(r.details) > 8:
            print(f"     ... (+{len(r.details)-8}건 더)")
    print("=" * 70)

    pass_count = sum(1 for r in results if r.status == PASS)
    fail_count = sum(1 for r in results if r.status == FAIL)
    fixable_fail = sum(1 for r in results if r.status == FAIL and r.auto_fixable)
    blocked_fail = fail_count - fixable_fail

    if fail_count == 0:
        print(f"\n✅ 모든 layer PASS ({pass_count}/{len(results)})")
    elif apply:
        print(f"\n📊 PASS {pass_count} / FAIL {fail_count}")
        if blocked_fail:
            print(f"⚠️  사용자 액션 필요: {blocked_fail}건 (auto-fix 불가)")
    else:
        print(f"\n📊 PASS {pass_count} / FAIL {fail_count}")
        if fixable_fail:
            print(f"💡 --apply 옵션으로 {fixable_fail}건 자동 복구 가능")
        if blocked_fail:
            print(f"⚠️  사용자 액션 필요: {blocked_fail}건 (auto-fix 불가)")


def render_report(project: Path, results: list[LayerResult], apply: bool) -> Path:
    from datetime import datetime
    out = project / "_workspace" / "qa_report.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append("# Content QA Report\n")
    lines.append(f"- 실행 시각: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"- 프로젝트: {project}")
    lines.append(f"- 모드: {'APPLY (자동 복구 실행)' if apply else 'DRY-RUN (검증만)'}")
    lines.append("")
    lines.append("| Layer | 검증 | 결과 | 요약 | 자동복구 |")
    lines.append("|---|---|---|---|---|")
    for r in results:
        fix_mark = "✅ 적용됨" if r.fixed else ("가능" if r.auto_fixable else "—")
        lines.append(f"| {r.layer} | {r.name} | {r.status} | {r.summary} | {fix_mark} |")
    lines.append("")
    for r in results:
        if r.details:
            lines.append(f"## Layer {r.layer} 상세")
            for d in r.details:
                lines.append(f"- {d}")
            lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", help="프로젝트 루트 경로")
    parser.add_argument("--apply", action="store_true", help="auto-fixable layer 자동 복구")
    parser.add_argument("--layers", default="", help="검사할 layer (쉼표 구분, 예: 1,2,4)")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    if not project.exists():
        print(f"[FATAL] 프로젝트 경로 없음: {project}", file=sys.stderr)
        return 1

    selected: set[int] | None = None
    if args.layers:
        selected = {int(x) for x in args.layers.split(",")}

    results: list[LayerResult] = []
    for num, name, fn in LAYERS:
        if selected and num not in selected:
            continue
        try:
            r = fn(project, args.apply)
        except Exception as e:
            r = LayerResult(num, name, FAIL, f"검증 중 예외: {type(e).__name__}: {e}")
        results.append(r)

    render_console(results, args.apply)
    report = render_report(project, results, args.apply)
    print(f"\n📄 리포트: {report}")

    blocked = sum(1 for r in results if r.status == FAIL and not r.auto_fixable)
    return 1 if blocked > 0 else 0


if __name__ == "__main__":
    sys.exit(main())

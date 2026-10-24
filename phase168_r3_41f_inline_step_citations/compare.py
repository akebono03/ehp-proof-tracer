"""Fail closed on completed or compatibility Narrative regressions."""
from __future__ import annotations

from difflib import unified_diff
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

PACKAGE = Path(__file__).resolve().parent
OUT = PACKAGE / "output"
UNCHANGED = ("pi3_2", "pi4_3", "pi5_4", "pi6_5", "legacy_explicit", "direct_fallback")


def compare_captures() -> dict:
    before = json.loads((OUT / "capture_before.json").read_text(encoding="utf-8"))
    after = json.loads((OUT / "capture_after.json").read_text(encoding="utf-8"))
    if before["completed"] != after["completed"]:
        raise AssertionError("Completed case metadata changed")
    for name in UNCHANGED:
        if (OUT / f"{name}_before.md").read_bytes() != (OUT / f"{name}_after.md").read_bytes():
            raise AssertionError("Completed or compatibility Narrative changed: " + name)
        print("UNCHANGED", name)
    a, b = before["partial_prefix"], after["partial_prefix"]
    for field in ("steps", "references", "reference_bodies", "cited_steps",
                  "reference_issues", "qed_absent", "goals_kept", "diagnostics_kept",
                  "audit_reconstruction_only"):
        if a[field] != b[field]:
            raise AssertionError("Certified prefix changed outside inline citations: " + field)
    if not (a["cited_steps"] > 0 and a["missing_step_citations"] > 0):
        raise AssertionError("Baseline did not reproduce the missing inline citation bug")
    if b["missing_step_citations"] != 0:
        raise AssertionError("Inline citation tags are still missing")
    old = (OUT / "certified_prefix_before.md").read_text(encoding="utf-8").splitlines(keepends=True)
    new = (OUT / "certified_prefix_after.md").read_text(encoding="utf-8").splitlines(keepends=True)
    diff = "".join(unified_diff(old, new, fromfile="certified_prefix_before.md",
                                tofile="certified_prefix_after.md"))
    (OUT / "certified_prefix.diff").write_text(diff, encoding="utf-8")
    report = {"phase": "168 R3-41F", "mode": "RENDERER_ONLY_INLINE_CITATIONS",
              "completed_four_byte_identical": True,
              "legacy_byte_identical": True, "direct_fallback_byte_identical": True,
              "prefix_before": a, "prefix_after": b,
              "no_new_citations": True,
              "not_a_genuine_partial_search": True,
              "full_pytest_run": False}
    (OUT / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 168 R3-41F — 未完成 ProofStep の既存 Reference 番号を本文に接続", "",
             "完成4群と legacy / fallback は変更前後バイト単位で同一。", "",
             f"- Certified prefix の既存 Reference: {b['references']}件",
             f"- Reference 本文: {b['reference_bodies']}件",
             f"- 引用を持つステップ: {b['cited_steps']}件",
             f"- 修正前のステップ引用欠落: {a['missing_step_citations']}件",
             f"- 修正後のステップ引用欠落: {b['missing_step_citations']}件", "",
             "この部分証明は完成証明からの再構成監査例であり、実探索から得た PARTIAL ではない。", "",
             "実探索5群が証明ステップ0件だったことは今回の修正では解消しない。", "",
             "全体 pytest は Phase 168 の終了時まで実行しない。", ""]
    (OUT / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    archive_path = OUT / "review_bundle.zip"
    with ZipFile(archive_path, "w", ZIP_DEFLATED) as archive:
        for file in sorted(OUT.iterdir()):
            if file.suffix in (".md", ".txt", ".json", ".diff"):
                archive.write(file, file.name)
    print("FOUR_COMPLETED_NARRATIVES_BYTE_IDENTICAL")
    print("EXPLICIT_LEGACY_AND_DIRECT_FALLBACK_BYTE_IDENTICAL")
    print("CITED_PREFIX_INLINE_CITATIONS", a["missing_step_citations"], "->", b["missing_step_citations"])
    print("REPORT", OUT / "audit.md")
    print("UPLOAD_BUNDLE", archive_path)
    return report


if __name__ == "__main__":
    compare_captures()

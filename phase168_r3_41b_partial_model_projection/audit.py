"""Compare the original incomplete-state semantics with R3-41B Model rendering."""
from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from phase165_r52_partial_proof import (
    ProofSearchStatus, make_partial_proof_result, render_partial_proof_markdown,
)
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from proof import ProofRule, ProofStep

PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"


def _cases():
    return (
        ("not_searched", make_partial_proof_result(
            n=100, k=20, status=ProofSearchStatus.NOT_SEARCHED,
            open_goals=("target",),
        )),
        ("partial", make_partial_proof_result(
            n=3, k=2, status=ProofSearchStatus.PARTIAL,
            proven_steps=(ProofStep("observed", (), ProofRule.GIVEN),),
            open_goals=("unknown",), references=("Unscreened reference",),
        )),
        ("search_failed", make_partial_proof_result(
            n=17, k=4, status=ProofSearchStatus.SEARCH_FAILED,
            open_goals=("no-rule",), diagnostics=("No applicable typed rule",),
        )),
    )


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    items = []
    for name, result in _cases():
        legacy = render_partial_proof_markdown(result)
        model = build_proof_narrative_model(result)
        common = render_model_backed_narrative_markdown(result, model)
        (OUTPUT / f"{name}_fallback.md").write_text(legacy, encoding="utf-8")
        (OUTPUT / f"{name}_common.md").write_text(common, encoding="utf-8")
        requirements = {
            "status": "探索状態：" in common,
            "goal": "## 未解決 Goal" in common,
            "diagnostics": ("## 探索診断" in common if result.diagnostics else True),
            "observed_step": ("observed" in common if result.proven_steps else True),
            "qed_absent": "□" not in common,
            "no_unscreened_reference": "Unscreened reference" not in common,
        }
        item = {"case": name, "requirements": requirements,
                "legacy_length": len(legacy), "common_length": len(common),
                "model_citations": len(model.citations)}
        if not all(requirements.values()):
            raise AssertionError(f"Incomplete model lost information: {name} {requirements}")
        print(name, "status", requirements["status"], "goals", requirements["goal"],
              "diagnostics", requirements["diagnostics"], "QED", not requirements["qed_absent"])
        items.append(item)
    report = {"phase": "168 R3-41B", "mode": "FOCUSED_PARTIAL_MODEL_VALIDATION",
              "cases": items, "completed_narratives_byte_identical": True,
              "full_pytest_run": False}
    (OUTPUT / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 168 R3-41B — 共通 Partial Narrative 監査", "",
             "既存 ProofStep のみ表示し、未解決 Goal は証明済みとしない。", "",
             "| Case | 状態 | Goal | 診断 | ステップ | QEDなし |",
             "|---|---|---|---|---|---|"]
    for item in items:
        c = item["requirements"]
        lines.append("| " + item["case"] + " | " + " | ".join(
            "PASS" if c[key] else "FAIL"
            for key in ("status", "goal", "diagnostics", "observed_step", "qed_absent")
        ) + " |")
    lines.extend(("", "- 既存完成4群の全文比較は compare.py で別途確認。",
                  "- 既存 Web fallback と明示 legacy API は維持。",
                  "- 全体 pytest は実行しない。", ""))
    (OUTPUT / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    bundle = OUTPUT / "review_bundle.zip"
    with ZipFile(bundle, "w", ZIP_DEFLATED) as archive:
        for path in sorted(OUTPUT.glob("*.json")) + sorted(OUTPUT.glob("*.md")):
            archive.write(path, path.name)
    print("REPORT", OUTPUT / "audit.md")
    print("UPLOAD_BUNDLE", bundle)


if __name__ == "__main__":
    main()

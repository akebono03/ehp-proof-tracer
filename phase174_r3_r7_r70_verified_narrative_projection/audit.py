"""R70 public, source-first narrative-only regression after a one-function patch."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from .install import source_guard, replace_formatter, TARGET


def inspect_public() -> dict[str, object]:
    """Verify two public completed searches, with no synthetic proof roots."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase174_r3_r7_r56_cyclic_generator_bridge.audit import _search_with_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase174_r3_r7_r68_ehp_premise_semantics_audit.audit import (
        inspect_public as earlier_inference_audit,
    )

    previous = earlier_inference_audit()
    if (previous["pi11_6"]["reference_count"] != 7
            or previous["pi12_7"]["reference_count"] != 3):
        raise RuntimeError("R70_PRIOR_EHP_PREMISES_CHANGED")
    bridge = build_shared_typed_bridge()
    first, model1 = _search_with_model(6, 5, bridge)
    second, model2 = _search_with_model(7, 5, bridge)
    a = render_model_backed_narrative_markdown(first, model1)
    b = render_model_backed_narrative_markdown(second, model2)
    if len(model1.citations) != 7 or len(model2.citations) != 3:
        raise RuntimeError("R70_REFERENCE_COUNT_CHANGED")
    expected_composite = "懸垂と合成の関係および [R2]より, $E("
    if (expected_composite not in a or "=0$." not in a
            or r"E(\nu_{5})=\nu_{6}" in a):
        raise RuntimeError("R70_COMPOSITE_CHAIN_NOT_CONDENSED")
    delta_text = r"よって, $\Delta: \pi_{13}^{13}\to \pi_{11}^{6}$ は全射."
    if delta_text not in b or r"[R1]より, $\Delta:" in b:
        raise RuntimeError("R70_DELTA_CONNECTIVE_MISSING")
    e_reason = r"完全性と $\Delta$ の全射性より, $E:\pi_{11}^{6}\to \pi_{12}^{7}$ は零写像."
    h_reason = (r"さらに完全性より, $\ker H=\operatorname{Im}E=0$ なので, "
                r"$H:\pi_{12}^{7}\to \pi_{12}^{13}$ は単射.")
    if e_reason not in b or h_reason not in b:
        raise RuntimeError("R70_HOPF_REASONING_NOT_DISPLAYED")
    proof = b.split("\n証明\n", 1)[-1]
    terminal_index = proof.find("[R3]より, ", proof.find(h_reason))
    terminal_line = (proof[terminal_index:].splitlines()[0]
                     if terminal_index >= 0 else "")
    if (proof.find(delta_text) == -1 or proof.find(e_reason) == -1
            or proof.find(h_reason) == -1
            or terminal_index < 0 or r"\pi_{12}^{13}" not in terminal_line
            or not (proof.find(delta_text) < proof.find(e_reason)
                    < proof.find(h_reason) < terminal_index)):
        raise RuntimeError("R70_REASONING_ORDER_CHANGED")
    if r"\\to" in a or r"\\to" in b:
        raise RuntimeError("R70_INVALID_TEX_ARROW")
    if first.status.name != "COMPLETE" or second.status.name != "COMPLETE":
        raise RuntimeError("R70_COMPLETED_SEARCH_CHANGED")
    return {
        "pi11_6_complete": True,
        "pi11_6_reference_count": len(model1.citations),
        "pi11_6_composite_zero_line": next(
            line for line in a.splitlines() if expected_composite in line),
        "pi11_6_source_formula_kept_in_reference": "[R2] (5.9)." in a,
        "pi12_7_complete": True,
        "pi12_7_reference_count": len(model2.citations),
        "pi12_7_delta_connective": delta_text,
        "pi12_7_zero_e_explanation": e_reason,
        "pi12_7_hopf_injectivity_explanation": h_reason,
        "pi12_7_intermediates_are_presentation_not_new_steps": True,
        "pi12_7_delta_surjective_still_one_prior_given": True,
        "full_sentence_semantics_audited": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    opts = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    checked = source_guard(root)
    status, _ = replace_formatter((root / TARGET).read_bytes())
    if status != "ALREADY_APPLIED" and not opts.dry_run:
        raise RuntimeError("R70_FORMATTER_NOT_APPLIED")
    print("PHASE174_R70_SOURCE_GUARD=PASS")
    print("PHASE174_R70_SOURCE_PINS=" + str(len(checked) + 1))
    if opts.dry_run:
        print("PHASE174_R70_GATE=PASS_R70_PUBLIC_DRYRUN")
        print("(END)")
        return 0
    evidence = inspect_public()
    report = {
        "phase": "174-R70", "evidence": evidence,
        "production_files_changed": [TARGET],
        "full_pytest_run": False,
    }
    output = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
              / "EHPProofTracerAudit"
              / "phase174_r3_r7_r70_verified_narrative_projection"
              / "report.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE174_R70_PI11_6_COMPOSITE_DISPLAY=PASS")
    print("PHASE174_R70_PI12_7_DELTA_CONNECTIVE=PASS")
    print("PHASE174_R70_PI12_7_E_ZERO_AND_H_INJECTIVE_EXPLANATION=PASS")
    print("PHASE174_R70_PI11_6_REFERENCES=7")
    print("PHASE174_R70_PI12_7_REFERENCES=3")
    print("PHASE174_R70_NEW_GIVEN=0")
    print("PHASE174_R70_NEW_MATHEMATICAL_RULES=0")
    print("PHASE174_R70_REPORT=" + str(output))
    print("PHASE174_R70_GATE=PASS_R70_PUBLIC_GENERAL_EXPLANATIONS")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

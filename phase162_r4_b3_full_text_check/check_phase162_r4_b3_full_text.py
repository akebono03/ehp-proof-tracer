"""Phase 162 R4-B3: read-only full-text inspection of derived common narrative."""
from pathlib import Path
import json

from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_stable_eta_proof_replay import build_toda_stable_eta_proof_replay
from toda_group_proof_narrative_renderer import (
    _phase158_baseline_render_toda_group_proof_narrative_markdown,
)


def inspect_derived_narratives(output_directory: Path) -> dict:
    output_directory.mkdir(parents=True, exist_ok=True)
    results = {}
    for n in (4, 5):
        key = f"pi_{n + 1}^{n}"
        target_result = _method_evidence_data(n, 1)[0].source_replay.group_result
        base_result = _method_evidence_data(3, 1)[0].source_replay.group_result
        integration = build_toda_stable_eta_proof_replay(
            target_result, base_result, max_depth=3
        )
        markdown = _phase158_baseline_render_toda_group_proof_narrative_markdown(
            integration.presentation
        )
        filename = f"{key}_derived_common.md"
        (output_directory / filename).write_text(markdown, encoding="utf-8")
        head, separator, tail = markdown.partition("## 証明\n")
        body = tail if separator else ""
        reference_text = head.partition("## 使用する結果")[2].partition("---")[0]
        flags = {
            "has_proof_section": bool(separator),
            "has_toda45_reference": "(4.5)" in reference_text,
            "has_target_in_reference": f"\\pi_{{{n + 1}}}^{{{n}}}" in reference_text,
            "body_has_symbolic_eta_n": r"\eta_{n}" in body,
            "body_has_symbolic_group_n": r"\pi_{n + 1}^{n}" in body,
            "body_has_transport_appendage": "証明木に記録された群構造の移送について" in body,
            "body_has_duplicate_transition": "これより, これより" in body or "これより, 以上より" in body,
            "qed_count": body.count(r"\square"),
            "derived_root_rule": (
                integration.presentation.root_step.inference_rule.name
                if integration.presentation.root_step.inference_rule is not None
                else None
            ),
        }
        results[key] = {"file": filename, "flags": flags}
        print("=" * 72)
        print(f"{key}: NEW PROOF TREE -> COMMON RENDERER (FULL MARKDOWN)")
        print("=" * 72)
        print(markdown)
        print("CHECK:", json.dumps(flags, ensure_ascii=False))
    (output_directory / "check.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("Saved all files in:", output_directory.resolve())
    return results


if __name__ == "__main__":
    inspect_derived_narratives(Path(__file__).resolve().parent / "audit_output")

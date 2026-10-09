"""Read-only provenance versus narrative audit for the reconstructed pi_5^3 proof."""
from collections import Counter
from pathlib import Path
import re

from phase162_pi5_3_renderer_audit import render_phase162_pi5_3_reconstructed_proof
from proof import ProofRule, ProofStep
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from tests.test_phase59_toda52_pi4_2_transport import build_phase59_2_data
from toda_rules import toda_eta_family_definition_statement


def main() -> None:
    pi4_step = build_phase59_2_data()["result_steps"][0]
    definitions = tuple(
        ProofStep(
            conclusion=toda_eta_family_definition_statement(index),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for index in (3, 4)
    )
    ehp_leaves = build_phase59_3_data()["premise_steps"]
    audit = render_phase162_pi5_3_reconstructed_proof(
        pi4_step, definitions, ehp_leaves
    )
    root = audit.final_step
    markdown = audit.markdown
    print("=== Root proof conclusion ===")
    print(repr(root.conclusion))
    print("=== Root immediate premises ===")
    for index, step in enumerate(root.premises, start=1):
        print(f"{index}: rule={step.rule.value}, inference={getattr(step.inference_rule, 'name', None)}")
        print("  conclusion:", repr(step.conclusion))
        print("  premise_count:", len(step.premises))
    print("=== Provenance statistics ===")
    steps_by_id = {id(node.proof_step): node.proof_step for node in audit.presentation.nodes}
    print("nodes:", len(steps_by_id), "edges:", len(audit.presentation.edges))
    print("proof rules:", dict(Counter(step.rule.value for step in steps_by_id.values())))
    print("=== EHP and transport inference conclusions ===")
    keywords = ("suspension", "eta-square", "transport", "exactness", "hopf", "delta")
    for node in audit.presentation.nodes:
        step = node.proof_step
        name = getattr(step.inference_rule, "name", "") or ""
        if any(word in name.lower() for word in keywords):
            print(f"depth={node.depth} inference={name} | conclusion={str(step.conclusion)[:240]}")
    print("=== Narrative defects (observed, not repaired) ===")
    checks = {
        "broken_exactness_math": len(re.findall(r"\$\$[^\n]*\$ は完全である\.\$ は完全である", markdown)),
        "repeated_connectors": len(re.findall(r"これより,\s*これより,", markdown)),
        "dangling_connector_lines": len(re.findall(r"(?m)^これより,\s*$", markdown)),
        "stable_generic_reference": len(re.findall(r"E\^\{n - 3\}", markdown)),
        "reference_5_3": len(re.findall(r"\[R\d+\] \(5\.3\)", markdown)),
        "pi5_3_conclusion": len(re.findall(r"\\pi_\{5\}\^\{3\}", markdown)),
    }
    for key, count in checks.items():
        print(f"{key}: {count}")
    print("=== Full narrative saved by previous audit ===")
    print("Renderer is called without replacing or editing its Markdown output.")
    output = Path(__file__).resolve().parent / "pi5_3_narrative_provenance_report.txt"
    output.write_text(
        "ROOT\n" + repr(root.conclusion) + "\n\n" +
        "DIRECT PREMISES\n" + "\n".join(repr(s.conclusion) for s in root.premises) +
        "\n\nDEFECT COUNTS\n" + "\n".join(f"{k}: {v}" for k, v in checks.items()) +
        "\n\nCOMPLETE RENDERED MARKDOWN\n" + markdown,
        encoding="utf-8",
    )
    print("Report:", output)


if __name__ == "__main__":
    main()

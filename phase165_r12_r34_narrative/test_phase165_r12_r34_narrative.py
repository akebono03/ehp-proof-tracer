from phase165_r12_r34_narrative import ordered_display_steps, completed_step_text, completed_provenance_key
from proof import ProofStep, ProofRule, InferenceRule


def test_r34_ancestry_is_postorder_without_modifying_steps():
    leaf = ProofStep("cited", (), ProofRule.GIVEN)
    root = ProofStep("final", (leaf,), ProofRule.INFERENCE, inference_rule=InferenceRule("rule"))
    assert ordered_display_steps(root) == (leaf, root)
    assert root.premises == (leaf,)


def test_r34_quotient_rule_has_japanese_description():
    step = ProofStep("final", (), ProofRule.INFERENCE,
                     inference_rule=InferenceRule("infinite cyclic quotient structure"))
    result = completed_step_text(step, lambda obj: str(obj), lambda obj: "internal rule")
    assert "第一同型定理" in result
    assert "infinite cyclic quotient structure" not in result


def test_r34_other_rules_keep_existing_renderer():
    step = ProofStep("example", (), ProofRule.INFERENCE, inference_rule=InferenceRule("other"))
    assert completed_step_text(step,str,lambda item: "original") == "original"


def test_r34_provenance_label_only_changes_on_complete():
    assert completed_provenance_key(True) == "generic-complete-proof"
    assert completed_provenance_key(False) == "generic-partial-proof"

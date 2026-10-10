from proof import InferenceRule, ProofRule, ProofStep
from phase163_r4_r11_ancestry_diagnosis import diagnose_incomplete_ancestry


def test_r4_r11_diagnosis_records_missing_rule_in_ancestor():
    leaf = ProofStep("axiom", (), ProofRule.GIVEN)
    ancestor = ProofStep("middle", (leaf,), ProofRule.INFERENCE)
    root = ProofStep("goal", (ancestor,), ProofRule.INFERENCE, inference_rule=InferenceRule("goal_rule"))
    findings = diagnose_incomplete_ancestry(root)
    assert [(f.path, f.issue) for f in findings] == [
        ("root/premise[0]", "INFERENCE_RULE_MISSING")
    ]


def test_r4_r11_diagnosis_records_missing_premises_without_promoting():
    root = ProofStep("goal", (), ProofRule.INFERENCE, inference_rule=InferenceRule("rule"))
    findings = diagnose_incomplete_ancestry(root)
    assert len(findings) == 1
    assert findings[0].issue == "INFERENCE_PREMISES_MISSING"
    assert root.premises == ()


def test_r4_r11_diagnosis_accepts_structurally_complete_tree():
    leaf = ProofStep("axiom", (), ProofRule.GIVEN)
    root = ProofStep("goal", (leaf,), ProofRule.INFERENCE, inference_rule=InferenceRule("rule"))
    assert diagnose_incomplete_ancestry(root) == ()


def test_r4_r11_diagnosis_rejects_non_proofstep_root():
    try:
        diagnose_incomplete_ancestry("not-a-step")
    except TypeError as exc:
        assert "root" in str(exc)
    else:
        raise AssertionError("TypeError expected")

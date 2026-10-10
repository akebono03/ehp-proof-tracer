from proof import InferenceRule, ProofRule, ProofStep
from phase163_r4_r11_shared_origin import find_missing_origins


def _missing(name: str) -> ProofStep:
    return ProofStep(
        conclusion=name,
        premises=(),
        rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name=f"source_{name}"),
    )


def _parent(name: str, children: tuple[ProofStep, ...]) -> ProofStep:
    return ProofStep(
        conclusion=name,
        premises=children,
        rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name=f"parent_{name}"),
    )


def test_shared_identity_across_roots_is_one_origin():
    missing = _missing("same")
    left = _parent("left", (missing,))
    right = _parent("right", (missing,))
    entries = find_missing_origins((("a", left), ("b", right)))
    assert len(entries) == 1
    assert entries[0].components == ("a", "b")
    assert entries[0].paths == ("a:root/premise[0]", "b:root/premise[0]")


def test_equal_conclusions_but_distinct_nodes_remain_separate():
    first = _missing("same")
    second = _missing("same")
    assert len(find_missing_origins((("a", first), ("b", second)))) == 2


def test_shared_dag_multiple_paths_retained():
    missing = _missing("shared")
    root = _parent("root", (missing, missing))
    entries = find_missing_origins((("a", root),))
    assert len(entries) == 1
    assert entries[0].paths == ("a:root/premise[0]", "a:root/premise[1]")


def test_complete_inference_is_not_reported():
    leaf = ProofStep(conclusion="fact", premises=(), rule=ProofRule.GIVEN)
    root = _parent("goal", (leaf,))
    assert find_missing_origins((("a", root),)) == ()


def test_missing_rule_is_separately_reported():
    leaf = ProofStep(conclusion="leaf", premises=(), rule=ProofRule.GIVEN)
    root = ProofStep(conclusion="goal", premises=(leaf,), rule=ProofRule.INFERENCE)
    entries = find_missing_origins((("a", root),))
    assert len(entries) == 1
    assert entries[0].issue == "INFERENCE_RULE_MISSING"
    assert entries[0].premise_count == 1


def test_reject_non_proofstep_root():
    import pytest
    with pytest.raises(TypeError):
        find_missing_origins((("a", "not a step"),))

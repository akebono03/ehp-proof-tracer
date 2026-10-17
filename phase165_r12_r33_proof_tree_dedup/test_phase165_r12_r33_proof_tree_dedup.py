from proof import InferenceRule, PremisePattern, ProofRule, ProofStep
from phase165_r12_r33_proof_tree_dedup import same_completed_proof_tree
from phase165_r6_2_r4_r8_dedup import append_unique_verified_derivation


def _proof(leaf, name='test inference'):
    rule = InferenceRule(name=name, premise_patterns=(PremisePattern(statement_type=str),))
    return ProofStep(conclusion='result', premises=(leaf,), rule=ProofRule.INFERENCE, inference_rule=rule)


def test_identical_derivation_with_same_leaf_is_deduplicated():
    leaf = ProofStep(conclusion='source', premises=(), rule=ProofRule.GIVEN)
    left, right = _proof(leaf), _proof(leaf)
    assert same_completed_proof_tree(left, right)
    options = [left]
    append_unique_verified_derivation(options, right)
    assert len(options) == 1


def test_distinct_fixed_source_leaves_are_preserved():
    leaf1 = ProofStep(conclusion='source', premises=(), rule=ProofRule.GIVEN)
    leaf2 = ProofStep(conclusion='source', premises=(), rule=ProofRule.GIVEN)
    assert not same_completed_proof_tree(_proof(leaf1), _proof(leaf2))


def test_distinct_rules_are_preserved():
    leaf = ProofStep(conclusion='source', premises=(), rule=ProofRule.GIVEN)
    assert not same_completed_proof_tree(_proof(leaf, 'rule A'), _proof(leaf, 'rule B'))


def test_same_conclusion_is_insufficient():
    leaf1 = ProofStep(conclusion='source 1', premises=(), rule=ProofRule.GIVEN)
    leaf2 = ProofStep(conclusion='source 2', premises=(), rule=ProofRule.GIVEN)
    assert not same_completed_proof_tree(_proof(leaf1), _proof(leaf2))

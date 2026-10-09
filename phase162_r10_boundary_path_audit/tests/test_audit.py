from dataclasses import replace

import pytest

from proof import ProofRule, ProofStep
from phase162_r10_boundary_path_audit.audit import ancestors, snapshot


def test_ancestors_preserve_dependency_order():
    leaf = ProofStep(conclusion="known", premises=(), rule=ProofRule.GIVEN)
    root = ProofStep(conclusion="result", premises=(leaf,), rule=ProofRule.INFERENCE)
    assert ancestors(root) == (leaf, root)
    assert snapshot(root)[1]["premise_indices"] == [1]


def test_ancestors_deduplicate_shared_object():
    leaf = ProofStep(conclusion="known", premises=(), rule=ProofRule.GIVEN)
    root = ProofStep(conclusion="result", premises=(leaf, leaf), rule=ProofRule.INFERENCE)
    assert ancestors(root) == (leaf, root)
    assert snapshot(root)[1]["premise_indices"] == [1, 1]


def test_ancestors_reject_cycle():
    root = ProofStep(conclusion="result", premises=(), rule=ProofRule.INFERENCE)
    object.__setattr__(root, "premises", (root,))
    with pytest.raises(ValueError, match="Cyclic"):
        ancestors(root)

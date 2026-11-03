"""Repository-backed tests for the public result sidecar; not Web completion."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_partial_proof import (
    CertifiedAbstractStructure,
    GroupStructureStatus,
    ProofSearchStatus,
    make_partial_proof_result,
)
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r7_source_first_abstract_certificate.search import (
    search_source_first_abstract,
)
from phase173_r4_r15r8_public_abstract_sidecar.attach import (
    attach_certified_abstract_structure,
)
from proof import ProofRule, ProofStep


@pytest.fixture(scope="module")
def verified_k31():
    """Use a real source-first certificate and the real registry once."""
    bridge = build_shared_typed_bridge()
    goal = exact_prior_database_result(4, 31)
    certificate = search_source_first_abstract(k=31, bridge=bridge)
    assert certificate is not None
    assert certificate.root_step.inference_rule.match_guard(
        certificate.root_step.premises, (),
    )
    return bridge, goal, certificate


def _pending(goal):
    return make_partial_proof_result(
        n=4, k=31, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=(goal,), diagnostics=("named goal unresolved",),
    )


def test_genuine_abstract_proof_attached_without_named_promotion(verified_k31) -> None:
    bridge, goal, certificate = verified_k31
    base = _pending(goal)
    result = attach_certified_abstract_structure(
        base, n=4, k=31, goal=goal, bridge=bridge,
    )
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.conclusion is None
    assert result.open_goals == base.open_goals
    assert result.structure_status is GroupStructureStatus.UNKNOWN
    assert result.diagnostics == base.diagnostics
    assert result.abstract_structure is not None
    assert result.abstract_structure.invariant_summands == (("finite", 2),) * 8
    assert result.abstract_structure.proof_step.rule is ProofRule.INFERENCE
    assert result.abstract_structure.proof_step.conclusion == certificate.conclusion


def test_forged_named_complete_or_mismatched_group_is_rejected(verified_k31) -> None:
    bridge, goal, _ = verified_k31
    result = attach_certified_abstract_structure(
        _pending(goal), n=4, k=31, goal=goal, bridge=bridge,
    )
    assert result.abstract_structure is not None
    with pytest.raises(ValueError, match="verified inference root"):
        replace(result.abstract_structure, group=TodaPrimaryGroup(36, 4))
    with pytest.raises(ValueError, match="abstract-only"):
        replace(result, target=TodaPrimaryGroup(36, 4))
    with pytest.raises(ValueError, match="abstract-only"):
        replace(result, structure_status=GroupStructureStatus.KNOWN)
    fake = ProofStep(result.abstract_structure.proof_step.conclusion, (), ProofRule.GIVEN)
    with pytest.raises(ValueError, match="verified inference root"):
        replace(result.abstract_structure, proof_step=fake)


def test_nonmatching_target_and_other_sphere_preserve_old_status(verified_k31) -> None:
    bridge, goal, _ = verified_k31
    base = _pending(goal)
    assert attach_certified_abstract_structure(base, n=4, k=31,
                                               goal=exact_prior_database_result(4, 4),
                                               bridge=bridge) is base
    assert attach_certified_abstract_structure(base, n=5, k=31,
                                               goal=goal, bridge=bridge) is base


def test_canonical_public_selector_preserves_named_partial(verified_k31, monkeypatch) -> None:
    """Only mock the unrelated named search; abstract evidence is authentic."""
    import phase165_r55_nk_only_goal as public
    import phase173_r4_r15r8_public_abstract_sidecar.attach as attachment

    bridge, goal, certificate = verified_k31
    pending = _pending(goal)
    monkeypatch.setattr(public, "search_shared_group_goal", lambda **kwargs: pending)
    monkeypatch.setattr(public, "resolve_specialized_goal_citing_id", lambda *args: None)
    monkeypatch.setattr(attachment, "search_source_first_abstract",
                        lambda **kwargs: certificate)
    result = public.search_group_from_registered_goal(
        n=4, k=31, bridge=bridge, goal=goal, proof_order_catalog=object(),
    )
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.conclusion is None
    assert result.open_goals == (goal,)
    assert result.abstract_structure is not None
    assert result.abstract_structure.invariant_summands == (("finite", 2),) * 8

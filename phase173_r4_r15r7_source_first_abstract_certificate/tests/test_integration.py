"""Source-verified integration contracts for n=4 abstract Toda 4.4 proofs."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e4_ordered_db_prior.db_prior import (
    exact_prior_database_result,
    verified_db_step,
)
from phase173_r4_r10_general_toda56_core.core import checked_general_inputs
from phase173_r4_r15r6_abstract_toda44_rule.abstract_rule import (
    canonical_abstract_result,
)
from phase173_r4_r15r7_source_first_abstract_certificate.search import (
    search_source_first_abstract,
)
from phase173_r4_r15r7_source_first_abstract_certificate.source import (
    screened_abstract_context,
)
from proof import ProofRule


@pytest.fixture(scope="module")
def bridge():
    return build_shared_typed_bridge()


@pytest.mark.parametrize("k", (4, 7, 8, 31))
def test_abstract_root_reconstructed_from_real_sources(bridge, k: int) -> None:
    result = search_source_first_abstract(k=k, bridge=bridge)
    assert result is not None
    assert result.root_step.conclusion == canonical_abstract_result(result.proof_target)
    assert result.root_step.rule is ProofRule.INFERENCE
    assert result.root_step.inference_rule.match_guard(result.root_step.premises, ())
    assert len(result.root_step.premises) == 4
    assert result.root_step.premises[0].rule is ProofRule.GIVEN
    assert result.root_step.premises[3].rule is ProofRule.INFERENCE
    for prior in result.root_step.premises[1:3]:
        assert verified_db_step(
            prior, proof_target=result.proof_target,
            bridge=result.source_context,
        )
    assert result.public_group_complete is False


def test_k31_is_abstract_eight_2_summands_without_named_certificate(bridge) -> None:
    result = search_source_first_abstract(k=31, bridge=bridge)
    assert result is not None
    assert result.conclusion.invariant_summands == (("finite", 2),) * 8
    assert not result.named_generator_shape_matched
    assert checked_general_inputs(result.proof_target) is None
    assert result.public_group_complete is False


def test_k8_original_epsilon_named_goal_still_requires_generator_proof(bridge) -> None:
    result = search_source_first_abstract(k=8, bridge=bridge)
    assert result is not None
    assert not result.named_generator_shape_matched
    assert checked_general_inputs(result.proof_target) is None


def test_forged_target_and_missing_source_fail_closed(bridge) -> None:
    target = exact_prior_database_result(4, 31)
    invalid = replace(target, rhs=exact_prior_database_result(4, 4).rhs)
    source = (Path(__file__).resolve().parents[2] / "sources" / "toda" /
              "Toda_05_2.tex").read_text(encoding="utf-8-sig")
    assert screened_abstract_context(
        bridge, proof_target=invalid, chapter=source,
    ) is None
    with pytest.raises(ValueError):
        screened_abstract_context(
            bridge, proof_target=target, chapter="not the original source",
        )


def test_non_eligible_stems_rejected() -> None:
    for stem in (True, 0, 1, 2, -1, 3.0):
        assert search_source_first_abstract(k=stem) is None

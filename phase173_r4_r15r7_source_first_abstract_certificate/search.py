"""Reconstruct a source-first abstract certificate using existing proof checks.

This is a separate abstract certificate, not a COMPLETE result for the named
registered group and not a new alternative to the canonical Web query API.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step,
    exact_prior_database_result,
    verified_db_step,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
    expand_cited_lemma54_hopf,
)
from phase173_r4_r10_general_toda56_core.core import (
    checked_abstract_inputs,
    checked_general_inputs,
)
from phase173_r4_r15r6_abstract_toda44_rule.abstract_rule import (
    TodaProp44AbstractGroupResult,
    canonical_abstract_result,
    expand_abstract_toda44,
)
from phase173_r4_r15r7_source_first_abstract_certificate.source import (
    screened_abstract_context,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin


@dataclass(frozen=True)
class AbstractSearchCertificate:
    """One verified abstract inference, explicitly separate from named proof."""

    proof_target: object
    conclusion: TodaProp44AbstractGroupResult
    root_step: ProofStep
    source_context: RegistryBridgeResult
    named_generator_shape_matched: bool

    @property
    def public_group_complete(self) -> bool:
        """This certificate never establishes the registered named group."""
        return False


def _screened_given_conclusions(screened: RegistryBridgeResult) -> tuple[object, ...]:
    """Obtain only exact fixed claims from screened proof links."""
    return tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and not link.step.premises
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
        and link.step.conclusion
        == screened.registry.assertion(link.assertion_id).content
    )


def search_source_first_abstract(
    *, k: int, bridge: RegistryBridgeResult | None = None,
) -> AbstractSearchCertificate | None:
    """Derive one checked abstract root for any eligible k; never name its basis.

    The common registered backward solver resolves only original literature
    source and Hopf subgoals. Two DB hypotheses are separately admitted and
    rechecked by the existing R10E4 API. The standard inference matcher then
    reconstructs the Proposition 4.4 root from those four proven steps.
    """
    if type(k) is not int or k < 3:
        return None
    target = exact_prior_database_result(4, k)
    conclusion = canonical_abstract_result(target)
    if conclusion is None:
        return None
    inputs = checked_abstract_inputs(target)
    if inputs is None:
        return None
    if bridge is None:
        bridge = build_shared_typed_bridge()
    root = Path(__file__).resolve().parents[1]
    chapter = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(
        encoding="utf-8-sig",
    )
    screened = screened_abstract_context(
        bridge, proof_target=target, chapter=chapter,
    )
    if screened is None:
        return None
    available = _screened_given_conclusions(screened)
    theorem = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    if available.count(theorem) != 1 or available.count(lemma) != 1:
        return None

    def source_provider(goal: object):
        return expand_cited_lemma54_hopf(goal, available)

    context_id = next(iter(screened.registry._assertions))
    theorem_step = reconstruct_registered_goal(
        theorem, screened, context_id, source_provider,
        lookup_mode="typed_reference",
    )
    hopf_goal = canonical_hopf_relation()
    hopf_step = reconstruct_registered_goal(
        hopf_goal, screened, context_id, source_provider,
        lookup_mode="typed_reference",
    )
    first_step = admitted_db_step(
        inputs[0], proof_target=target, bridge=screened,
    )
    second_step = admitted_db_step(
        inputs[1], proof_target=target, bridge=screened,
    )
    if (first_step is None or second_step is None
            or not verified_db_step(first_step, proof_target=target, bridge=screened)
            or not verified_db_step(second_step, proof_target=target, bridge=screened)):
        return None
    if (theorem_step.rule is not ProofRule.GIVEN
            or hopf_step.rule is not ProofRule.INFERENCE):
        return None
    proposals = expand_abstract_toda44(
        conclusion, available, proof_target=target, bridge=screened,
    )
    if len(proposals) != 1:
        return None
    proposal = proposals[0]
    if proposal.subgoals != (
        theorem, inputs[0], inputs[1], hopf_goal,
    ):
        return None
    premises = (theorem_step, first_step, second_step, hopf_step)
    matches = tuple(
        match for match in find_inference_matches_for_rule(
            proposal.rule, premises,
        )
        if match.premises == premises
    )
    if len(matches) != 1:
        return None
    root_step = derive_inference_proof_step(matches[0])
    if (root_step.rule is not ProofRule.INFERENCE
            or root_step.conclusion != conclusion
            or root_step.premises != premises
            or not proposal.rule.match_guard(root_step.premises, ())):
        return None
    return AbstractSearchCertificate(
        proof_target=target,
        conclusion=conclusion,
        root_step=root_step,
        source_context=screened,
        named_generator_shape_matched=checked_general_inputs(target) is not None,
    )

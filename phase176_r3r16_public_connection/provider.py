"""Public bridge for the already-verified typed two-step right-zero inference.

No newly asserted group relation or generator image is inserted as a GIVEN.
Both children remain proof obligations of the ordinary recursive search.
"""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero
from phase176_r3r15_shared_extra_provider_probe.provider import build_screened_extra_provider
from proof import ProofRule, ProofStep
from unified_statement_registry import AssertionOrigin


def build_public_lemma57_right_provider(bridge: RegistryBridgeResult):
    """Use only a uniquely screened, cited Lemma 5.7 fixed-statement leaf."""
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("typed screened source bridge required")
    accepted = []
    for link in bridge.proof_links:
        step = link.step
        if (not isinstance(step, ProofStep)
                or step.rule is not ProofRule.GIVEN
                or step.premises
                or type(step.conclusion) is not TodaLemma57ExplicitNuPrimeZero):
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        reference = bridge.registry.reference(assertion.reference_id)
        citation = getattr(getattr(step, "inference_rule", None), "literature_reference", None)
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or assertion.content != step.conclusion
                or reference.publication_position is None
                or citation is None
                or citation.locator != "Lemma 5.7"):
            continue
        accepted.append(step)
    if len(accepted) == 1:
        return build_screened_extra_provider(tuple(accepted))

    def no_candidates(goal: object) -> tuple:
        return ()

    return no_candidates

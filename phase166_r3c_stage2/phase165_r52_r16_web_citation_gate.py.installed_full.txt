"""R52-R16: screen proof-context references before ordinary web search.

Source adoption and independent chronological verification are different trust
policies. The former is restricted to known R38 and R13 adopted sources;
all other fixed statements require the established R15 citation judgment.
"""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase164_r2_citation_eligibility import assess_phase164_r2_citation
from proof import ProofRule
from unified_statement_registry import AssertionOrigin


def screen_shared_proof_context(
    bridge: RegistryBridgeResult,
    *,
    goal: object,
    citing_assertion_id: str,
    verified_assertion_ids: tuple[str, ...] = (),
    explicit_publication_target: bool = False,
) -> RegistryBridgeResult:
    """Filter proof links, keeping the registry and its source records intact.

    The adopted path is a previously accepted translated-source convention,
    NOT independent original-edition or publication-order verification.
    Unrecognized unordered sources are not promoted to this path.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not isinstance(verified_assertion_ids, tuple):
        raise TypeError("verified_assertion_ids must be a tuple")
    bridge.registry.assertion(citing_assertion_id)
    accepted = []
    if explicit_publication_target:
        from phase166_r3c_publication_order import precedes_citing_assertion
    for link in bridge.proof_links:
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if type(assertion.content) is type(goal) and assertion.content == goal:
            continue
        step = link.step
        if step is None or step.rule is not ProofRule.GIVEN:
            continue
        if type(step.conclusion) is not type(assertion.content) or step.conclusion != assertion.content:
            raise ValueError("fixed reference has inconsistent GIVEN proof link")
        if explicit_publication_target:
            if precedes_citing_assertion(bridge, assertion.assertion_id, citing_assertion_id):
                accepted.append(link)
            continue
        # A source admitted under the explicit adopted-Tex convention keeps its
        # existing trust boundary; this is not a citation-order certification.
        adopted = (
            assertion.assertion_id.startswith("shared:")
            and (
                ":adopted:assertion:" in assertion.assertion_id
                or ":toda:adopted:prop5.1:finite_dimensional" in assertion.assertion_id
                or assertion.assertion_id.endswith(":adopted:assertion:prop42:general")
            )
        )
        if adopted:
            accepted.append(link)
            continue
        # All other sources, including those without a known publication
        # position, must satisfy the already-implemented strict R15 policy.
        decision = assess_phase164_r2_citation(
            bridge, assertion.assertion_id, citing_assertion_id,
            verified_assertion_ids=verified_assertion_ids,
        )
        if decision.usable:
            accepted.append(link)
    return RegistryBridgeResult(bridge.registry, bridge.records, tuple(accepted))

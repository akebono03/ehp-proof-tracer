"""R3R2: source-bound Hopf codomain and independent premise diagnostics.

The source boundary changes an obligation, never a fact or proof rule.
Every diagnostic reconstructs its own ProofStep with the ordinary canonical
backward resolver and the same screened earlier references as the main root.
"""
from __future__ import annotations

from phase165_r3_recursive_search import (
    GoalExpansion,
    RegisteredGoalUnresolved,
    SourceBoundGoal,
    reconstruct_registered_goal,
)
from phase171_r2j_r2_cyclic_hopf_surjective.source import _eligible_group_instance
from phase175_r3_pi73_hopf_lift.rule import RULE_NAME
from proof import ProofRule, ProofStep, Relation, RelationType


def source_bound_hopf_codomain(
    proposal: GoalExpansion, available: tuple[object, ...],
) -> GoalExpansion | None:
    """Replace only a sourced cyclic codomain obligation with a bound goal.

    The identified source must be present in the already screened GIVEN
    conclusions.  SourceBoundGoal forces a proof by INFERENCE, thereby
    preventing an earlier database relation from short-circuiting the proof.
    An ambiguous or missing cited source yields no candidate.
    """
    if not isinstance(proposal, GoalExpansion) or not isinstance(available, tuple):
        return None
    if proposal.rule.name != RULE_NAME or len(proposal.subgoals) != 3:
        return None
    injective, codomain, image = proposal.subgoals
    if (not isinstance(codomain, Relation)
            or codomain.relation_type is not RelationType.EQUALITY):
        return None
    sources = tuple(
        source for source in available
        if isinstance(source, Relation)
        and _eligible_group_instance(source, codomain)
    )
    if len(sources) != 1:
        return None
    return GoalExpansion(
        rule=proposal.rule,
        subgoals=(injective, SourceBoundGoal(codomain, sources[0]), image),
    )


def inspect_independent_obligation(
    name: str,
    goal: object,
    screened: object,
    citing_assertion_id: str,
    provider: object,
) -> dict[str, object]:
    """Observe one independent real proof search; never claim a proof by route count.

    A DIRECT_GIVEN result may be evidence for a later theorem but cannot
    discharge the R3 Hopf-lift rule, which requires three INFERENCE parents.
    The source-bound case retains the actual conclusion from its inferred
    ProofStep and reports it separately from the bound wrapper.
    """
    if not isinstance(name, str) or not name:
        raise ValueError("R3R2 nonempty obligation name required")
    if not callable(provider):
        raise TypeError("R3R2 provider must be callable")
    actual = goal.conclusion if isinstance(goal, SourceBoundGoal) else goal
    offered = provider(actual)
    if not isinstance(offered, tuple) or not all(
        isinstance(option, GoalExpansion) for option in offered
    ):
        raise TypeError("R3R2 provider contract changed")
    observed: list[str] = []
    proved: list[str] = []

    def progress(kind: str, target: object, step: ProofStep | None) -> None:
        if kind == "unresolved":
            if len(observed) < 20:
                observed.append(repr(target)[:700])
        elif kind == "proved":
            if not isinstance(step, ProofStep):
                raise TypeError("R3R2 proved event requires a real ProofStep")
            if len(proved) < 20:
                proved.append(repr(step.conclusion)[:700])
        else:
            raise ValueError("R3R2 unexpected progress kind")

    try:
        step = reconstruct_registered_goal(
            goal, screened, citing_assertion_id, provider,
            lookup_mode="typed_reference_publication", progress_observer=progress,
        )
    except RegisteredGoalUnresolved as exc:
        status = "UNRESOLVED"
        proof_rule = None
        premise_count = None
        diagnostic = str(exc)[:900]
    else:
        if not isinstance(step, ProofStep) or step.conclusion != actual:
            raise RuntimeError("R3R2 inferred conclusion does not match obligation")
        proof_rule = step.rule.value
        premise_count = len(step.premises)
        status = (
            "INFERRED" if step.rule is ProofRule.INFERENCE and step.premises
            else "UNBACKED_INFERENCE_REJECTED" if step.rule is ProofRule.INFERENCE
            else "DIRECT_GIVEN_NOT_ACCEPTABLE" if step.rule is ProofRule.GIVEN
            else "OTHER_PROOF_RULE_NOT_ACCEPTABLE"
        )
        diagnostic = None

    return {
        "name": name,
        "goal": repr(goal)[:2400],
        "source_bound": isinstance(goal, SourceBoundGoal),
        "offered_routes": len(offered),
        "offered_rules": [option.rule.name for option in offered[:20]],
        "status": status,
        "actual_proof_rule": proof_rule,
        "actual_premise_count": premise_count,
        "diagnostic": diagnostic,
        "observed_unresolved_count": len(observed),
        "observed_unresolved": observed,
        "observed_proved": proved,
    }

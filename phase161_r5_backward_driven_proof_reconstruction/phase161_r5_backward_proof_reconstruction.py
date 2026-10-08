"""Phase 161 R5: reconstruct n=3 EHP proof from backward goals.

Only independently supplied leaf proof steps are accepted. This is a
concrete, seven-rule reconstruction, not a general-purpose theorem prover.
"""

from dataclasses import dataclass

from homotopy_groups import (
    TodaPrimaryGroup,
    TodaSuspensionIsomorphismStatement,
    TodaSuspensionMap,
)
from phase161_r3_backward_goal_schema import expand_phase161_r3_goal
from phase161_r4_literature_premise_matching import (
    expand_phase161_r4_literature_goal,
    match_phase161_r4_existing_premises,
)
from proof import (
    ProofRule,
    ProofStep,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from toda_rules import TodaProp42ExactnessStatement


@dataclass(frozen=True)
class BackwardReconstructionResult:
    goal: object
    final_step: ProofStep
    derived_steps: tuple[ProofStep, ...]
    leaf_steps: tuple[ProofStep, ...]


def phase161_r5_target_goal() -> TodaSuspensionIsomorphismStatement:
    return TodaSuspensionIsomorphismStatement(
        map=TodaSuspensionMap(
            source_group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=2),
            target_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        )
    )


def reconstruct_phase161_r5_goal(
    goal: object,
    available_leaf_steps: tuple[ProofStep, ...],
) -> BackwardReconstructionResult:
    """Execute the goal-derived seven-rule dependency tree bottom-up.

    The input pool must contain independent literature-derived proof steps and
    four already established exactness witnesses. Derived map-property steps
    and the goal itself are never accepted from the pool.
    """
    if goal != phase161_r5_target_goal() or type(goal) is not TodaSuspensionIsomorphismStatement:
        raise ValueError("Phase 161 R5 supports only E: pi_4^2 -> pi_5^3 isomorphism")
    if not isinstance(available_leaf_steps, tuple) or any(
        not isinstance(step, ProofStep) for step in available_leaf_steps
    ):
        raise TypeError("available_leaf_steps must be a tuple of ProofStep")

    # Prevent accidental use of known completed map-property proofs as leaves.
    exactness_steps = tuple(
        step for step in available_leaf_steps
        if isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    if any(step.rule is not ProofRule.GIVEN or step.premises for step in exactness_steps):
        raise ValueError("Exactness witnesses must be independently supplied GIVEN leaves")
    literature_steps = tuple(
        step for step in available_leaf_steps
        if step.rule is ProofRule.INFERENCE
        and not isinstance(step.conclusion, TodaProp42ExactnessStatement)
    )
    leaf_pool = literature_steps + exactness_steps
    created = []
    used = []
    visiting = set()
    cache = {}

    def resolve(current_goal):
        if current_goal in cache:
            return cache[current_goal]
        if current_goal in visiting:
            raise ValueError("Cyclic backward goal dependency")
        visiting.add(current_goal)
        try:
            expansion = expand_phase161_r3_goal(current_goal)
            if expansion is not None:
                premise_steps = tuple(resolve(child) for child in expansion.subgoals)
                matches = tuple(
                    match for match in find_inference_matches_for_rule(
                        expansion.inference_rule, premise_steps
                    )
                    if tuple(match.premises) == premise_steps
                )
                if len(matches) != 1:
                    raise ValueError(f"Production rule does not accept exact subgoals: {current_goal!r}")
                result = apply_inference_match(matches[0])
                if result.conclusion != current_goal or result.rule is not ProofRule.INFERENCE:
                    raise ValueError("Production conclusion does not match backward goal")
                created.append(result)
                cache[current_goal] = result
                return result

            literature_plan = expand_phase161_r4_literature_goal(current_goal)
            if literature_plan is not None:
                matches = match_phase161_r4_existing_premises(literature_plan, literature_steps)
                if len(matches) != 1:
                    raise ValueError(f"Expected one independently justified literature match: {current_goal!r}; found {len(matches)}")
                match = matches[0]
                inference_matches = tuple(
                    candidate for candidate in find_inference_matches_for_rule(
                        literature_plan.inference_rule, match.premises
                    )
                    if candidate.premises == match.premises
                )
                if len(inference_matches) != 1:
                    raise ValueError("Production matcher rejected literature evidence")
                result = apply_inference_match(inference_matches[0])
                if result.conclusion != current_goal:
                    raise ValueError("Literature production conclusion mismatch")
                used.extend(match.premises)
                created.append(result)
                cache[current_goal] = result
                return result

            # Exactness is an independent input, not inferred or invented here.
            if isinstance(current_goal, TodaProp42ExactnessStatement):
                matches = tuple(step for step in exactness_steps if step.conclusion == current_goal)
                if len(matches) != 1:
                    raise ValueError(f"Missing or ambiguous independent exactness: {current_goal!r}")
                used.append(matches[0])
                cache[current_goal] = matches[0]
                return matches[0]
            raise ValueError(f"Unresolved backward goal: {current_goal!r}")
        finally:
            visiting.remove(current_goal)

    final = resolve(goal)
    if len(created) != 7:
        raise ValueError(f"Expected exactly seven freshly derived production steps, got {len(created)}")
    unique_used = tuple(dict.fromkeys(id(step) for step in used))
    used_by_id = {id(step): step for step in used}
    return BackwardReconstructionResult(
        goal=goal,
        final_step=final,
        derived_steps=tuple(created),
        leaf_steps=tuple(used_by_id[key] for key in unique_used),
    )

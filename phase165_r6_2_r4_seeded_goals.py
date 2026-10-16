"""General backward premise generation from conclusion and typed source anchors.

An anchor binds variables; it does not prove any remaining premise.
Every emitted subgoal must still be checked by the canonical proof search.
"""
from __future__ import annotations

from itertools import product

from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r23_conclusion_unification import _instantiate_nested, unify_inference_conclusion
from phase165_r8_rule_provider import _pattern_variable_names, _unresolved_pattern
from proof import (
    InferenceRule, PremisePattern, ProofRule, ProofStep, Relation,
    match_premise_pattern, merge_variable_bindings,
)


def generate_seeded_backward_goals(
    goal: object,
    rules: tuple[InferenceRule, ...],
    cited_steps: tuple[ProofStep, ...],
    *,
    max_candidates: int = 2048,
) -> tuple[GoalExpansion, ...]:
    """Bind otherwise free premise variables to cited GIVEN statements.

    All proposed conclusions and premises remain unproved search goals.
    No unknown witness, theorem or source is manufactured.
    """
    if not isinstance(rules, tuple) or any(not isinstance(rule, InferenceRule) for rule in rules):
        raise TypeError("rules must be a tuple of InferenceRule")
    if not isinstance(cited_steps, tuple) or any(
        not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN
        for step in cited_steps
    ):
        raise TypeError("cited_steps must contain only typed GIVEN ProofSteps")
    if type(max_candidates) is not int or max_candidates < 1:
        raise ValueError("max_candidates must be a positive integer")
    expansions = []
    attempts = 0
    for rule in rules:
        unified = unify_inference_conclusion(rule, goal)
        if unified is None or not rule.premise_patterns:
            continue
        templates = []
        for premise in rule.premise_patterns:
            if not isinstance(premise, PremisePattern):
                break
            if premise.relation_pattern is not None and premise.statement_pattern is not None:
                break
            template = premise.relation_pattern if premise.relation_pattern is not None else premise.statement_pattern
            if template is None:
                break
            templates.append(template)
        if len(templates) != len(rule.premise_patterns):
            continue
        bound_names = {binding.variable.name for binding in unified.bindings}
        required = set().union(*(_pattern_variable_names(t) for t in templates))
        # Goal-bound rules are already handled by the existing generic provider.
        if required <= bound_names:
            continue
        # A typed source can anchor a premise. Other premises remain goals.
        options = []
        for pattern in rule.premise_patterns:
            matches = []
            for step in cited_steps:
                binding = match_premise_pattern(pattern, step)
                if binding is not None:
                    matches.append(binding)
            options.append(tuple(matches))
        # Also permit no source anchor for each premise; do not invent bindings.
        for chosen in product(*((None,) + row for row in options)):
            if all(x is None for x in chosen):
                continue
            attempts += 1
            if attempts > max_candidates:
                raise ValueError("seeded backward search budget exceeded")
            bindings = unified.bindings
            for match in chosen:
                if match is not None:
                    bindings = merge_variable_bindings(bindings + match)
                    if bindings is None:
                        break
            if bindings is None or not required <= {x.variable.name for x in bindings}:
                continue
            subgoals = []
            for premise, template in zip(rule.premise_patterns, templates):
                concrete = _instantiate_nested(template, bindings)
                if _unresolved_pattern(concrete):
                    break
                if premise.statement_type is not None and not isinstance(concrete, premise.statement_type):
                    break
                if premise.relation_pattern is not None and not isinstance(concrete, Relation):
                    break
                if premise.relation_type is not None and (not isinstance(concrete, Relation) or concrete.relation_type is not premise.relation_type):
                    break
                subgoals.append(concrete)
            if len(subgoals) == len(templates):
                proposal = GoalExpansion(rule, tuple(subgoals))
                if not any(old.rule is rule and old.subgoals == proposal.subgoals for old in expansions):
                    expansions.append(proposal)
    return tuple(expansions)

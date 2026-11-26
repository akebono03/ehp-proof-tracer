"""Compress a certified Prop 2.5 application followed by RHS associativity."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase176_r3r55_equality_display_isolated.projection import is_transitivity, rendered_math
from phase177_r3_unsigned_delta_composition_isolated.rule import RULE_NAME, unsigned_prop25_inputs
from phase177_r10_composition_associativity_isolated.rule import (
    RULE_NAME as ASSOCIATIVITY_RULE, is_composition_associativity_equality,
)
from phase177_r17r4r1_prop25_suspension_elision.projection import replayed
from proof import ProofRule


def project_prop25_equality_chain(model, order, suppressed=frozenset(), protected=frozenset()):
    """Return exclusive intermediate indices and final citation-bearing sentences.

    Do not change the model, references, typed statements or premise edges.
    Only the actual cited Prop 2.5 step and an uncited, replayable associativity
    step may be replaced by their already-proved transitivity conclusion.
    """
    if (model.status is not ProofSearchStatus.COMPLETE or model.open_goals
            or type(model.root_index) is not int
            or len(model.steps) != len(model.step_citation_numbers)):
        return frozenset(), {}
    steps = model.steps
    numbers = model.step_citation_numbers
    try:
        scope = root_ancestor_step_indices(steps, model.root_index)
    except ValueError:
        return frozenset(), {}
    positions = {i: p for p, i in enumerate(order)}
    if len(positions) != len(order) or not set(positions) <= scope:
        return frozenset(), {}
    lookup = {id(step): i for i, step in enumerate(steps)}
    if len(lookup) != len(steps):
        return frozenset(), {}
    parents = {i: tuple(lookup.get(id(p)) for p in step.premises)
               for i, step in enumerate(steps)}
    if any(p is None for ps in parents.values() for p in ps):
        return frozenset(), {}
    citations = {c.number for c in model.citations}
    hidden, sentences = set(), {}
    for i in order:
        step = steps[i]
        unavailable = set(suppressed) | set(protected) | hidden | set(sentences)
        if (i in unavailable or step.rule is not ProofRule.INFERENCE
                or step.inference_rule is None
                or step.inference_rule.name != 'equality transitivity'
                or len(step.premises) != 2 or numbers[i]):
            continue
        prop, assoc = step.premises
        p, a = parents[i]
        if (p == a or model.root_index in (p, a)
                or any(j not in positions or j in unavailable or positions[j] >= positions[i]
                       for j in (p, a))
                or prop.rule is not ProofRule.INFERENCE or prop.inference_rule is None
                or prop.inference_rule.name != RULE_NAME or len(prop.premises) not in (2, 3)
                or assoc.rule is not ProofRule.INFERENCE or assoc.inference_rule is None
                or assoc.inference_rule.name != ASSOCIATIVITY_RULE or assoc.premises or numbers[a]
                or not is_composition_associativity_equality(assoc.conclusion)
                or not is_transitivity(step.conclusion, prop.conclusion, assoc.conclusion)):
            continue
        source, base, *identity = prop.premises
        c, b, *aux = parents[p]
        if (source.rule is not ProofRule.GIVEN or source.premises
                or len(numbers[c]) != 1 or not set(numbers[c]) <= citations
                or not set(numbers[p]) <= set(numbers[c])
                or b not in positions or b in unavailable or positions[b] >= positions[p]
                or any(j not in suppressed or j in protected for j in aux)
                or unsigned_prop25_inputs(prop.conclusion, base.conclusion,
                                           identity[0].conclusion if identity else None)
                    != tuple(parent.conclusion for parent in prop.premises)):
            continue
        if any(j != i and ({p, a} & set(ps)) for j, ps in parents.items()):
            continue
        if not all(replayed(s) for s in (prop, assoc, step)):
            continue
        span = typed_endpoints(step.conclusion.rhs)
        if span is None or typed_endpoints(prop.conclusion.rhs) != span:
            continue
        latex = rendered_math(step.conclusion)
        if not all(rendered_math(s.conclusion) for s in (prop, assoc, base)) or not latex:
            continue
        tags = ', '.join(f'[R{number}]' for number in numbers[c])
        hidden.update((p, a))
        sentences[i] = f'{tags}を用いて, ${latex}$.'
    return frozenset(hidden), sentences

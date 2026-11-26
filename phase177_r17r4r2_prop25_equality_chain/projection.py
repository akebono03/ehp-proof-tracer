"""Compress a certified Prop 2.5 application followed by RHS associativity."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase176_r3r55_equality_display_isolated.projection import is_symmetry, is_transitivity, rendered_math
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
    branch (direct or followed by symmetry) may be replaced by their
    already-proved transitivity conclusion.
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
                or p not in positions or p in unavailable or positions[p] >= positions[i]
                or a not in positions or a in protected or a in hidden or a in sentences
                or positions[a] >= positions[i]
                or prop.rule is not ProofRule.INFERENCE or prop.inference_rule is None
                or prop.inference_rule.name != RULE_NAME or len(prop.premises) not in (2, 3)
                or assoc.rule is not ProofRule.INFERENCE or assoc.inference_rule is None
                or numbers[a]
                or not is_transitivity(step.conclusion, prop.conclusion, assoc.conclusion)):
            continue
        # The general equality display may already suppress the symmetry
        # line. Still verify its entire typed branch and exclusive consumers.
        witness_index = a
        if assoc.inference_rule.name == 'equality symmetry':
            if len(assoc.premises) != 1:
                continue
            witness_index, = parents[a]
            if (witness_index in (p, a, i, model.root_index)
                    or witness_index not in positions or witness_index in protected
                    or witness_index in hidden or witness_index in sentences
                    or positions[witness_index] >= positions[a]
                    or numbers[witness_index]
                    or not is_symmetry(assoc.conclusion, steps[witness_index].conclusion)
                    or not replayed(assoc)):
                continue
        witness = steps[witness_index]
        if (witness.rule is not ProofRule.INFERENCE or witness.inference_rule is None
                or witness.inference_rule.name != ASSOCIATIVITY_RULE or witness.premises
                or not is_composition_associativity_equality(witness.conclusion)
                or not replayed(witness)):
            continue
        # No intermediate may have an additional consumer, even if that
        # consumer is already hidden by another display projection.
        consumers = {p: {i}, a: {i}}
        if witness_index != a:
            consumers[witness_index] = {a}
        if any({j for j, ps in parents.items() if k in ps} != allowed
               for k, allowed in consumers.items()):
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
        if not all(replayed(s) for s in (prop, step)):
            continue
        span = typed_endpoints(step.conclusion.rhs)
        if span is None or typed_endpoints(prop.conclusion.rhs) != span:
            continue
        latex = rendered_math(step.conclusion)
        if not all(rendered_math(s.conclusion) for s in (prop, assoc, witness, base)) or not latex:
            continue
        tags = ', '.join(f'[R{number}]' for number in numbers[c])
        hidden.update(consumers)
        sentences[i] = f'{tags}を用いて, ${latex}$.'
    return frozenset(hidden), sentences

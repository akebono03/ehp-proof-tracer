"""Elide exclusive, uncited definitional suspension branches used by Prop 2.5."""
from __future__ import annotations

from expression import Suspension
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase169_r10eq_r1_universal_stable_definition.definition import is_defined_stable_image
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase176_r3r55_equality_display_isolated.projection import (
    equality, is_composition_transport, is_symmetry, is_transitivity,
)
from phase177_r3_unsigned_delta_composition_isolated.rule import RULE_NAME, unsigned_prop25_inputs
from phase177_r5_general_suspension_equality_isolated.rule import (
    IMAGE_RULE, NOTATION_RULE, is_iterated_notation_equality, suspension_image_input,
)
from proof import ProofRule, apply_inference_match, find_inference_matches_for_rule
from web_group_proof_common import _group_proof_statement_latex


def replayed(step):
    """Check the actual inference and its original typed premises, without search."""
    if step.rule is not ProofRule.INFERENCE or step.inference_rule is None:
        return False
    return any(
        result.conclusion == step.conclusion and result.premises == step.premises
        for match in find_inference_matches_for_rule(step.inference_rule, step.premises)
        for result in (apply_inference_match(match),)
    )


def definitional_step(step):
    """Accept only checked suspension notation, images and equality transport."""
    if step.rule is not ProofRule.INFERENCE or step.inference_rule is None:
        return False
    name, value = step.inference_rule.name, step.conclusion
    parents = tuple(p.conclusion for p in step.premises)
    if name == 'stable representative definitional suspension':
        return not parents and type(value) is GeneratorImage and is_defined_stable_image(value) and replayed(step)
    if not equality(value):
        return False
    span = typed_endpoints(value.lhs)
    if span is None or typed_endpoints(value.rhs) != span:
        return False
    if name == NOTATION_RULE:
        valid = not parents and is_iterated_notation_equality(value)
    elif name == IMAGE_RULE:
        valid = len(parents) == 1 and suspension_image_input(value) == parents[0]
    elif name == 'equality symmetry':
        valid = len(parents) == 1 and is_symmetry(value, parents[0])
    elif name == 'equality transitivity':
        valid = len(parents) == 2 and is_transitivity(value, *parents)
    elif name == 'suspension preserves equality':
        valid = (len(parents) == 1 and equality(parents[0])
                 and type(value.lhs) is Suspension and type(value.rhs) is Suspension
                 and value.lhs.expression == parents[0].lhs
                 and value.rhs.expression == parents[0].rhs)
    elif name in ('equality preserved under left composition', 'equality preserved under right composition'):
        valid = len(parents) == 1 and is_composition_transport(value, parents[0])
    else:
        valid = False
    return valid and replayed(step)


def project_prop25_suspension_elision(model, order, suppressed=frozenset(), protected=frozenset()):
    """Return only body indices; never mutate the proof, order or source mapping.

    The whole auxiliary branch must be independently replayable, have no
    citation or GIVEN, and have no consumer outside that branch and its one
    actual unsigned Prop 2.5 application. Leave everything on ambiguity.
    """
    if (model.status is not ProofSearchStatus.COMPLETE or model.open_goals
            or type(model.root_index) is not int
            or len(model.steps) != len(model.step_citation_numbers)):
        return frozenset()
    steps = model.steps
    try:
        scope = root_ancestor_step_indices(steps, model.root_index)
    except ValueError:
        return frozenset()
    positions = {i: p for p, i in enumerate(order)}
    if len(positions) != len(order) or not set(positions) <= scope:
        return frozenset()
    lookup = {id(s): i for i, s in enumerate(steps)}
    if len(lookup) != len(steps):
        return frozenset()
    parents = {i: tuple(lookup.get(id(p)) for p in s.premises) for i, s in enumerate(steps)}
    if any(p is None for ps in parents.values() for p in ps):
        return frozenset()
    hidden = set()
    for i in order:
        step = steps[i]
        if (i in suppressed or i in protected or i in hidden
                or step.rule is not ProofRule.INFERENCE or step.inference_rule is None
                or step.inference_rule.name != RULE_NAME or len(step.premises) != 3):
            continue
        cite, base, identity = step.premises
        c, b, a = parents[i]
        if (cite.rule is not ProofRule.GIVEN or cite.premises
                or not model.step_citation_numbers[c]
                or base.rule is not ProofRule.INFERENCE
                or identity.rule is not ProofRule.INFERENCE
                or unsigned_prop25_inputs(step.conclusion, base.conclusion, identity.conclusion)
                    != tuple(p.conclusion for p in step.premises)
                or not replayed(step)
                or b not in positions or b in suppressed or b in hidden
                or positions[b] >= positions[i]):
            continue
        if not all(_group_proof_statement_latex(s.conclusion)[0] is not None
                   and _group_proof_statement_latex(s.conclusion)[1] is None for s in (base, step)):
            continue
        branch = set()
        pending = [a]
        valid = True
        while pending:
            j = pending.pop()
            if j in branch:
                continue
            if (j not in scope or j not in positions or j in protected or j in (model.root_index, i, b, c)
                    or positions[j] >= positions[i] or model.step_citation_numbers[j]
                    or not definitional_step(steps[j])):
                valid = False
                break
            branch.add(j)
            pending.extend(parents[j])
        if not valid or not branch:
            continue
        # Preserve a shared witness, even when another user has no displayed line.
        if any(j not in branch | {i} and branch.intersection(ps) for j, ps in parents.items()):
            continue
        if any(positions[p] >= positions[j] for j in branch for p in parents[j]):
            continue
        hidden.update(branch)
    return frozenset(hidden)

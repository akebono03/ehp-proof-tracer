"""Omit a repeated, already emitted, certified direct-source equality."""
from __future__ import annotations

from expression import MapApplication
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r2_8_3_generator_identity.identity import _generator_identity, _master_records
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase176_r3r55_equality_display_isolated.projection import equality, rendered_math
from phase177_r17r4r1_prop25_suspension_elision.projection import replayed
from proof import ProofRule


def same_expression(left, right):
    """Exact value, or the existing registered generator identity at typed endpoints."""
    if type(left) is type(right) and left == right:
        return True
    if type(left) is MapApplication or type(right) is MapApplication:
        return (type(left) is type(right) is MapApplication
                and left.map == right.map
                and same_expression(left.expression, right.expression))
    span = typed_endpoints(left)
    if span is None or typed_endpoints(right) != span:
        return False
    try:
        records = _master_records()
        first = _generator_identity(left, records)
        second = _generator_identity(right, records)
    except (OSError, ValueError, KeyError, TypeError):
        return False
    return first is not None and first == second


def same_equality(left, right):
    """Never identify distinct typed equations just because their TeX agrees."""
    return (equality(left) and equality(right)
            and left.source == right.source and left.note == right.note
            and same_expression(left.lhs, right.lhs)
            and same_expression(left.rhs, right.rhs))


def direct_source(model, index, sentence, scope):
    """Identify one actual cited GIVEN premise and a replayable direct inference."""
    if index not in scope or index == model.root_index:
        return None
    step = model.steps[index]
    if (step.rule is not ProofRule.INFERENCE or step.inference_rule is None
            or not equality(step.conclusion) or len(step.premises) != 1):
        return None
    leaf, = step.premises
    if leaf.rule is not ProofRule.GIVEN or leaf.premises:
        return None
    indices = [j for j in scope if model.steps[j] is leaf]
    if len(indices) != 1:
        return None
    j, = indices
    numbers = model.step_citation_numbers[j]
    own = model.step_citation_numbers[index]
    if (not numbers or len(set(numbers)) != len(numbers)
            or (own and own != numbers)
            or not set(numbers) <= {c.number for c in model.citations}):
        return None
    latex = rendered_math(step.conclusion)
    tags = ', '.join(f'[R{n}]' for n in numbers)
    if not latex or sentence != f'{tags}より, ${latex}$.':
        return None
    if not replayed(step):
        return None
    return (step, leaf, numbers)


def omit_duplicate_cited_equality(model, index, sentence, retained, protected=frozenset()):
    """Use only sentences already emitted by the renderer, never infer a new fact.

    Retained is a caller-owned per-render dictionary of actual earlier indices.
    Return True only for an equivalent, same-source and same-rule direct reading.
    Preserve different sources, different typed claims, roots, partial proofs,
    special protected projections and every original ProofStep/citation.
    """
    if (model.status is not ProofSearchStatus.COMPLETE or model.open_goals
            or type(model.root_index) is not int
            or len(model.steps) != len(model.step_citation_numbers)
            or index in protected or index == model.root_index):
        return False
    if not sentence.startswith('[R') or 'より, $' not in sentence:
        return False
    try:
        scope = root_ancestor_step_indices(model.steps, model.root_index)
    except ValueError:
        return False
    current = direct_source(model, index, sentence, scope)
    if current is None:
        return False
    step, leaf, numbers = current
    previous = retained.setdefault(sentence, [])
    # Do not deduplicate an ambiguous visible string or a repeated index.
    matched = bool(previous)
    for j in previous:
        if j == index or j in protected:
            matched = False
            break
        old = direct_source(model, j, sentence, scope)
        if old is None:
            matched = False
            break
        earlier, old_leaf, old_numbers = old
        if (old_numbers != numbers
                or type(old_leaf.conclusion) is not type(leaf.conclusion)
                or old_leaf.conclusion != leaf.conclusion
                or earlier.inference_rule.name != step.inference_rule.name
                or earlier.inference_rule.literature_reference != step.inference_rule.literature_reference
                or not same_equality(earlier.conclusion, step.conclusion)):
            matched = False
            break
    if matched:
        return True
    previous.append(index)
    return False

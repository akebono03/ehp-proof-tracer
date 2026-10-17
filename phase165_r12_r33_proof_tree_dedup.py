"""Conservative recursive equality for completed proof trees, with provenance."""
from __future__ import annotations

from proof import ProofRule, ProofStep


def _callable_signature(fn):
    if fn is None:
        return None
    code = getattr(fn, '__code__', None)
    if code is None:
        return ('opaque', id(fn))
    closure = getattr(fn, '__closure__', None) or ()
    values = []
    for cell in closure:
        try:
            value = cell.cell_contents
        except ValueError:
            return ('opaque', id(fn))
        if callable(value):
            values.append(_callable_signature(value))
        else:
            values.append((type(value), repr(value)))
    return (code.co_code, code.co_consts, code.co_names,
            code.co_varnames, fn.__defaults__, tuple(values))


def _same_inference_rule(left, right):
    if left is right:
        return True
    if left is None or right is None:
        return False
    return (left.name == right.name
            and left.description == right.description
            and left.premise_patterns == right.premise_patterns
            and left.conclusion_pattern == right.conclusion_pattern
            and left.literature_reference == right.literature_reference
            and _callable_signature(left.conclusion_builder)
                == _callable_signature(right.conclusion_builder)
            and _callable_signature(left.match_guard)
                == _callable_signature(right.match_guard))


def same_completed_proof_tree(left: object, right: object) -> bool:
    """Only collapse equivalent inferred trees with identical cited leaf provenance.

    Distinct fixed-source leaf objects are deliberately not merged. Cycles are
    refused, rather than treated as evidence of equivalence.
    """
    active = set()

    def compare(a, b):
        if not isinstance(a, ProofStep) or not isinstance(b, ProofStep):
            return False
        pair = (id(a), id(b))
        if pair in active:
            return False
        if (type(a.conclusion) is not type(b.conclusion)
                or a.conclusion != b.conclusion or a.rule != b.rule
                or a.note != b.note
                or a.foundational_reference != b.foundational_reference
                or len(a.premises) != len(b.premises)):
            return False
        if a.rule is ProofRule.GIVEN:
            return a is b and a.premises == ()
        if a.rule is not ProofRule.INFERENCE:
            return False
        if not _same_inference_rule(a.inference_rule, b.inference_rule):
            return False
        active.add(pair)
        try:
            return all(compare(x, y) for x, y in zip(a.premises, b.premises))
        finally:
            active.remove(pair)

    return (isinstance(left, ProofStep)
            and isinstance(right, ProofStep)
            and left.rule is ProofRule.INFERENCE
            and right.rule is ProofRule.INFERENCE
            and compare(left, right))

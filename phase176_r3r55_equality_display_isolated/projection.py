"""Presentation-only suppression based on actual certified premise edges."""
from __future__ import annotations

from expression import Composition, Suspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase172_r2_suspension_relation_display.projection import same_typed_generator
from phase174_r3_r6_r3_common_narrative.projection import project_verified_cyclic_extension_reason
from phase176_r3r50_strict_nu_prime_connection.notation import alias_hopf_input
from proof import ProofRule, Relation, RelationType
from web_group_proof_common import _group_proof_statement_latex


def equality(value):
    return type(value) is Relation and value.relation_type is RelationType.EQUALITY


def is_transitivity(result, first, second):
    return (all(equality(x) for x in (result, first, second))
            and first.rhs == second.lhs and result.lhs == first.lhs
            and result.rhs == second.rhs)


def is_symmetry(result, parent):
    return (equality(result) and equality(parent)
            and result.lhs == parent.rhs and result.rhs == parent.lhs)


def is_composition_transport(result, parent):
    if not (equality(result) and equality(parent)
            and type(result.lhs) is Composition and type(result.rhs) is Composition):
        return False
    a, b = result.lhs, result.rhs
    return ((a.left == b.left and a.right == parent.lhs and b.right == parent.rhs)
            or (a.right == b.right and a.left == parent.lhs and b.left == parent.rhs))


def is_finite_cyclic_conversion(structure, relation):
    return (type(structure) is CyclicStructureStatement and equality(relation)
            and type(structure.group) is TodaPrimaryGroup
            and type(structure.order) is int and structure.order >= 2
            and type(relation.rhs) is FiniteCyclicGroup
            and relation.lhs == structure.group
            and relation.rhs.order == structure.order
            and relation.rhs.generator == structure.generator)


def rendered_math(statement):
    latex, fallback = _group_proof_statement_latex(statement)
    return latex if latex is not None and fallback is None else None


def looks_identical(statement):
    """A final display guard, never a proof of typed equality."""
    latex = rendered_math(statement)
    if not latex or latex.count('=') != 1:
        return False
    left, right = (part.strip() for part in latex.split('='))
    return bool(left) and left == right


def project_redundant_equalities(model, display_order, already_hidden=frozenset(),
                                 protected=frozenset()):
    """Return indices/reasons; do not mutate model, rules, order or citations.

    A notation identity must have an actual same-witness derivation, or be
    composed solely of already established notation transports. A repeated
    equation must consume a retained earlier equation. Direct citations,
    GIVENs, the root and explicitly protected projections are not suppressed.
    """
    if (getattr(model, 'status', None) is not ProofSearchStatus.COMPLETE
            or getattr(model, 'open_goals', ())):
        return {}
    steps = getattr(model, 'steps', None)
    numbers = getattr(model, 'step_citation_numbers', None)
    root = getattr(model, 'root_index', None)
    if (not isinstance(steps, tuple) or not isinstance(numbers, tuple)
            or len(steps) != len(numbers) or type(root) is not int):
        return {}
    try:
        scope = root_ancestor_step_indices(steps, root)
    except ValueError:
        return {}
    order = tuple(display_order)
    if len(order) != len(set(order)) or any(type(i) is not int or i not in scope for i in order):
        return {}
    lookup = {id(step): i for i, step in enumerate(steps)}
    if len(lookup) != len(steps):
        return {}
    parents = {i: tuple(lookup.get(id(p)) for p in steps[i].premises) for i in scope}
    if any(p not in scope for row in parents.values() for p in row):
        return {}
    known = set(order).difference(already_hidden)
    eligible = known.difference(protected, {root})
    hidden = {}
    aliases = set()
    retained = set()

    def cited_witness(w):
        if (w not in retained or w in protected or steps[w].rule is not ProofRule.INFERENCE
                or type(steps[w].conclusion) is not GeneratorSuspension
                or type(steps[w].conclusion.map) is not TodaSuspensionMap
                or typed_sentence(steps[w].conclusion, steps[w]) is None):
            return False
        ancestry = root_ancestor_step_indices(steps, w)
        return any(steps[j].rule is ProofRule.GIVEN and numbers[j] for j in ancestry)

    def base_alias(i, a, b):
        rel = steps[i].conclusion
        first, second = steps[a].conclusion, steps[b].conclusion
        if (not is_transitivity(rel, first, second)
                or not same_typed_generator(rel.lhs, rel.rhs)
                or type(first.rhs) is not Suspension
                or len(parents[a]) != 1 or len(parents[b]) != 1):
            return False
        p = parents[a][0]
        if len(parents[p]) != 1 or parents[p] != parents[b]:
            return False
        w = parents[p][0]
        if not cited_witness(w) or not is_symmetry(first, steps[p].conclusion):
            return False
        witness = steps[w].conclusion
        return (all(steps[j].rule is ProofRule.INFERENCE and not numbers[j]
                    and j in already_hidden for j in (a, b, p))
                and same_typed_generator(first.rhs.expression, witness.source_generator)
                and same_typed_generator(rel.lhs, witness.target_generator)
                and same_typed_generator(rel.rhs, witness.target_generator))

    def same_math(a, b):
        x, y = rendered_math(a), rendered_math(b)
        return x is not None and x == y

    for i in order:
        if i not in known:
            continue
        step, ps = steps[i], parents[i]
        rel = step.conclusion
        if (i not in eligible or step.rule is not ProofRule.INFERENCE
                or numbers[i] or step.inference_rule is None):
            retained.add(i)
            continue
        reason = None
        if equality(rel) and looks_identical(rel):
            if len(ps) == 2 and base_alias(i, *ps):
                reason = 'same_cited_suspension_witness'
            elif len(ps) == 1 and ps[0] in aliases and is_composition_transport(rel, steps[ps[0]].conclusion):
                reason = 'composition_of_notation_identity'
            elif (len(ps) == 2 and all(p in aliases for p in ps)
                  and is_transitivity(rel, *(steps[p].conclusion for p in ps))):
                reason = 'transitivity_of_notation_identities'
            if reason:
                aliases.add(i)
        elif equality(rel) and len(ps) == 1 and ps[0] in retained and ps[0] not in protected:
            previous = steps[ps[0]].conclusion
            if is_symmetry(rel, previous) and rendered_math(previous) is not None and rendered_math(rel) is not None:
                reason = 'symmetry_of_retained_equality'
            elif alias_hopf_input(rel, previous) is not None and same_math(rel, previous):
                reason = 'strict_notation_transport_of_retained_equality'
        elif equality(rel) and len(ps) == 2:
            a, b = ps
            if (a in retained and a not in protected and b in aliases
                    and is_transitivity(rel, steps[a].conclusion, steps[b].conclusion)
                    and same_math(rel, steps[a].conclusion)):
                reason = 'retained_equality_followed_by_notation_identity'
        elif (type(rel) is CyclicStructureStatement and root in known and root not in protected
              and steps[root].rule is ProofRule.INFERENCE and not numbers[root]
              and parents[root] == (i,) and is_finite_cyclic_conversion(rel, steps[root].conclusion)
              and all(j == root or i not in parents[j] for j in scope)
              and typed_sentence(rel, step) is None
              and project_verified_cyclic_extension_reason(rel, step) is None
              and same_math(rel, steps[root].conclusion)):
            reason = 'finite_cyclic_structure_repeated_by_root'
        if reason:
            hidden[i] = reason
        else:
            retained.add(i)
    return hidden

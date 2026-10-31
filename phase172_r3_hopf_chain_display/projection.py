"""Source-bound shortening of a verified right-Hopf composition derivation.

This module neither performs inference nor constructs ProofSteps. It recognizes
one already proven premise graph and returns only display indices/citation IDs.
Unrecognized graphs are left unchanged, without deducing equivalence from TeX.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import Composition, MapApplication
from map_facts import EHP_H_MAP
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase168_r3_27_typed_statement_projection import typed_sentence
from proof import ProofRule, Relation, RelationType


@dataclass(frozen=True)
class VerifiedHopfDisplay:
    """Locations of retained mathematics and omitted intermediate prose."""

    image_index: int
    formula_index: int
    hidden_indices: frozenset[int]
    formula_citations: tuple[int, ...]
    image_citations: tuple[int, ...]


def project_verified_hopf_chain(
    model: object,
    display_order: tuple[int, ...],
    already_hidden: set[int] | frozenset[int],
) -> VerifiedHopfDisplay | None:
    """Compress only the exact cited, inferred, right-Hopf equality chain.

    Requires the original suspension witness to be visible, its derived
    equality and symmetry already hidden by R2, a cited right-Hopf formula,
    a cited generator-image GIVEN, and an inferred H-image used by surjectivity.
    Other branches and all ProofSteps/citations remain untouched.
    """
    if (getattr(model, "status", None) is not ProofSearchStatus.COMPLETE
            or getattr(model, "open_goals", ())):
        return None
    steps = getattr(model, "steps", None)
    citations = getattr(model, "step_citation_numbers", None)
    root = getattr(model, "root_index", None)
    if (not isinstance(steps, tuple) or not isinstance(citations, tuple)
            or len(steps) != len(citations) or type(root) is not int):
        return None
    try:
        root_scope = root_ancestor_step_indices(steps, root)
    except ValueError:
        return None
    order = tuple(display_order)
    if (any(type(i) is not int or i not in root_scope for i in order)
            or len(order) != len(set(order))):
        return None
    visible = set(order).difference(already_hidden)
    lookup = {id(step): i for i, step in enumerate(steps)}
    if len(lookup) != len(steps):
        return None

    def index(node: object) -> int | None:
        by_identity = lookup.get(id(node))
        if by_identity is not None:
            return by_identity
        matching = [i for i, step in enumerate(steps) if step == node]
        return matching[0] if len(matching) == 1 else None

    def premise_indices(node: object, count: int) -> tuple[int, ...] | None:
        parents = getattr(node, "premises", ())
        if len(parents) != count:
            return None
        indices = tuple(index(parent) for parent in parents)
        if (any(i is None or i not in root_scope for i in indices)
                or len(indices) != len(set(indices))):
            return None
        return indices

    def inferred_relation(i: int) -> bool:
        statement = steps[i].conclusion
        return (steps[i].rule is ProofRule.INFERENCE
                and isinstance(statement, Relation)
                and statement.relation_type is RelationType.EQUALITY)

    def consumers_of(i: int) -> set[int]:
        return {
            j for j in root_scope
            if any(index(parent) == i for parent in steps[j].premises)
        }

    def source_numbers(i: int) -> tuple[int, ...] | None:
        try:
            scope = root_ancestor_step_indices(steps, i)
        except ValueError:
            return None
        numbers = tuple(dict.fromkeys(
            n for j in sorted(scope) for n in citations[j]
        ))
        return numbers if numbers else None

    for surj_index in order:
        surj = steps[surj_index]
        if (surj.rule is not ProofRule.INFERENCE
                or not isinstance(surj.conclusion, MapSurjective)):
            continue
        for image_node in surj.premises:
            image_idx = index(image_node)
            if (image_idx is None or image_idx not in visible
                    or not inferred_relation(image_idx)):
                continue
            image = steps[image_idx].conclusion
            if (not isinstance(image.lhs, MapApplication)
                    or image.lhs.map != EHP_H_MAP
                    or not isinstance(image.lhs.expression, Composition)):
                continue
            pair = premise_indices(image_node, 2)
            if pair is None:
                continue
            join_idx, normalize_idx = pair
            if not inferred_relation(join_idx) or not inferred_relation(normalize_idx):
                continue
            join, normalized = steps[join_idx].conclusion, steps[normalize_idx].conclusion
            if (join.lhs != image.lhs or normalized.lhs != join.rhs
                    or normalized.rhs != image.rhs):
                continue
            join_parents = premise_indices(steps[join_idx], 2)
            if join_parents is None:
                continue
            hopf_equality_idx, substitution_idx = join_parents
            if (not inferred_relation(hopf_equality_idx)
                    or not inferred_relation(substitution_idx)):
                continue
            hopf_equality = steps[hopf_equality_idx].conclusion
            substitution = steps[substitution_idx].conclusion
            if (hopf_equality.lhs != join.lhs
                    or hopf_equality.rhs != substitution.lhs
                    or substitution.rhs != join.rhs):
                continue
            substitution_parents = premise_indices(steps[substitution_idx], 2)
            hopf_parent = premise_indices(steps[hopf_equality_idx], 1)
            normalize_parent = premise_indices(steps[normalize_idx], 1)
            if (substitution_parents is None or hopf_parent is None
                    or normalize_parent is None):
                continue
            formula_idx, cited_image_idx = substitution_parents
            composition_idx = hopf_parent[0]
            direct_idx = normalize_parent[0]
            if (not inferred_relation(formula_idx)
                    or not inferred_relation(composition_idx)
                    or not inferred_relation(direct_idx)):
                continue
            formula = steps[formula_idx].conclusion
            composition = steps[composition_idx].conclusion
            if (substitution.lhs != formula.lhs or not isinstance(formula.lhs, MapApplication)
                    or formula.lhs.map != EHP_H_MAP
                    or composition.lhs != image.lhs.expression
                    or composition.rhs != hopf_equality.rhs.expression
                    or not isinstance(hopf_equality.rhs, MapApplication)
                    or hopf_equality.rhs.map != EHP_H_MAP
                    or hopf_equality.lhs != image.lhs):
                continue
            formula_parent = premise_indices(steps[formula_idx], 1)
            composition_parent = premise_indices(steps[composition_idx], 1)
            direct_parent = premise_indices(steps[direct_idx], 1)
            if (formula_parent is None or composition_parent is None
                    or direct_parent is None):
                continue
            formula_source_idx = formula_parent[0]
            symmetry_idx = composition_parent[0]
            witness_idx = direct_parent[0]
            symmetry_parent = premise_indices(steps[symmetry_idx], 1)
            if (symmetry_parent is None or symmetry_parent[0] != direct_idx
                    or not inferred_relation(symmetry_idx)):
                continue
            if (steps[symmetry_idx].conclusion.lhs != steps[direct_idx].conclusion.rhs
                    or steps[symmetry_idx].conclusion.rhs != steps[direct_idx].conclusion.lhs):
                continue
            witness = steps[witness_idx]
            formula_source = steps[formula_source_idx]
            cited_image = steps[cited_image_idx]
            if (witness_idx not in visible or formula_idx not in visible
                    or cited_image_idx not in visible or image_idx not in visible
                    or direct_idx not in already_hidden or symmetry_idx not in already_hidden
                    or witness.rule is not ProofRule.INFERENCE
                    or not isinstance(witness.conclusion, GeneratorSuspension)
                    or typed_sentence(witness.conclusion, witness) is None
                    or formula_source.rule is not ProofRule.GIVEN
                    or cited_image.rule is not ProofRule.GIVEN
                    or not citations[formula_source_idx] or not citations[cited_image_idx]
                    or not isinstance(cited_image.conclusion, Relation)
                    or cited_image.conclusion.relation_type is not RelationType.EQUALITY
                    or not isinstance(cited_image.conclusion.lhs, MapApplication)
                    or cited_image.conclusion.lhs.map != EHP_H_MAP):
                continue
            hidden = frozenset((composition_idx, hopf_equality_idx, substitution_idx,
                                join_idx, normalize_idx))
            if (not hidden.issubset(visible) or image_idx in hidden
                    or formula_idx in hidden or cited_image_idx in hidden
                    or any(not inferred_relation(i) or citations[i] for i in hidden)):
                continue
            expected_consumers = {
                composition_idx: {hopf_equality_idx},
                hopf_equality_idx: {join_idx},
                substitution_idx: {join_idx},
                join_idx: {image_idx},
                normalize_idx: {image_idx},
            }
            if any(consumers_of(i) != expected for i, expected in expected_consumers.items()):
                continue
            formula_citations = tuple(citations[formula_source_idx])
            chain_citations = source_numbers(image_idx)
            if chain_citations is None:
                continue
            # Citation for the source suspension must be reachable through its
            # own actual premise graph, rather than a renderer-generated label.
            suspension_citations = source_numbers(witness_idx)
            if (suspension_citations is None
                    or not set(suspension_citations).issubset(chain_citations)
                    or not set(formula_citations).issubset(chain_citations)
                    or not set(citations[cited_image_idx]).issubset(chain_citations)):
                continue
            return VerifiedHopfDisplay(
                image_index=image_idx,
                formula_index=formula_idx,
                hidden_indices=hidden,
                formula_citations=formula_citations,
                image_citations=chain_citations,
            )
    return None

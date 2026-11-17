"""Shared certified finite-cyclic Hopf-lift conclusion presentation.

This module reads a completed, verified Proof Tree and already rendered lines.
It never performs a search, registers a mathematical rule or adds a ProofStep.
It refuses presentation changes if any source, image or displayed anchor is
ambiguous. It is intentionally independent of concrete sphere dimensions.
"""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase168_r3_27_typed_statement_projection import group_tex, typed_sentence
from phase175_r3_pi73_hopf_lift.rule import RULE_NAME, hopf_lift_inputs
from proof import ProofRule, Relation, RelationType
from toda_human_readable_renderer import render_toda_public_group_generator_latex
from web_group_proof_common import _group_proof_statement_latex

VERIFIED_PRIOR_LIFT_NAME = "verified prior DB Hopf cyclic generator preimage lift"


def _unique_index_by_identity(steps: tuple, wanted: object, scope: frozenset[int]) -> int | None:
    """Require an actual ProofStep object, not a merely equal fake step."""
    found = [i for i in scope if steps[i] is wanted]
    return found[0] if len(found) == 1 else None


def _source_numbers(model, step_index: int, scope: frozenset[int]) -> tuple[int, ...]:
    """Return citation numbers of real GIVEN ancestors of one proved step."""
    try:
        ancestry = root_ancestor_step_indices(model.steps, step_index)
    except ValueError:
        return ()
    if not ancestry.issubset(scope):
        return ()
    source_numbers = set()
    for index in ancestry:
        step = model.steps[index]
        if step.rule is ProofRule.GIVEN:
            source_numbers.update(model.step_citation_numbers[index])
    known = {citation.number for citation in model.citations}
    if not source_numbers.issubset(known):
        return ()
    return tuple(sorted(source_numbers))


def _certified_hopf_lift(model):
    """Identify one consumed instance of the existing general Hopf lift rule."""
    if (getattr(model, "status", None) is not ProofSearchStatus.COMPLETE
            or getattr(model, "open_goals", ())):
        return None
    steps = getattr(model, "steps", None)
    citations = getattr(model, "step_citation_numbers", None)
    registered_citations = getattr(model, "citations", None)
    root_index = getattr(model, "root_index", None)
    if (not isinstance(steps, tuple) or not isinstance(citations, tuple)
            or len(steps) != len(citations)
            or not isinstance(registered_citations, tuple) or not registered_citations
            or type(root_index) is not int
            or not 0 <= root_index < len(steps)):
        return None
    try:
        scope = root_ancestor_step_indices(steps, root_index)
    except ValueError:
        return None
    root = steps[root_index]
    claim = root.conclusion
    if (root.rule is not ProofRule.INFERENCE
            or not isinstance(claim, Relation)
            or claim.relation_type is not RelationType.EQUALITY
            or not isinstance(claim.lhs, TodaPrimaryGroup)
            or not isinstance(claim.rhs, FiniteCyclicGroup)):
        return None
    candidates = []
    for index in scope:
        step = steps[index]
        cyclic = step.conclusion
        name = getattr(getattr(step, "inference_rule", None), "name", None)
        if (index == root_index or step.rule is not ProofRule.INFERENCE
                or not isinstance(cyclic, CyclicStructureStatement)
                or cyclic.group != claim.lhs or cyclic.order != claim.rhs.order
                or name not in (RULE_NAME, VERIFIED_PRIOR_LIFT_NAME)
                or len(step.premises) != 3 or citations[index]):
            continue
        injectivity, codomain, image = step.premises
        if (injectivity.rule is not ProofRule.INFERENCE
                or image.rule is not ProofRule.INFERENCE
                or not isinstance(injectivity.conclusion, MapInjective)):
            continue
        # The original general lift proves the codomain by INFERENCE.
        # The verified-prior variant explicitly admits a citation-bearing
        # earlier database GIVEN, validated by its own existing rule/trust gate.
        if (name == RULE_NAME and codomain.rule is not ProofRule.INFERENCE):
            continue
        if (name == VERIFIED_PRIOR_LIFT_NAME
                and (codomain.rule is not ProofRule.GIVEN
                     or bool(codomain.premises))):
            continue
        required = hopf_lift_inputs(cyclic, codomain.conclusion, image.conclusion)
        if required is None or tuple(parent.conclusion for parent in step.premises) != required:
            continue
        positions = tuple(
            _unique_index_by_identity(steps, parent, scope)
            for parent in step.premises
        )
        if any(pos is None for pos in positions) or len(set(positions)) != 3:
            continue
        # The lift must be on the actual root path; all three certified
        # premises must be the exact premises consumed by that inference.
        candidates.append((scope, root, step, positions))
    return candidates[0] if len(candidates) == 1 else None


def project_verified_hopf_lift_conclusion(lines: list[str], model) -> list[str]:
    """Explain generator-surjectivity/isomorphism and hide one duplicate.

    The isomorphism is the direct verbal consequence of the *existing* typed
    general lift's proved injectivity + proved finite cyclic target + proved
    generator image. This function creates neither MapSurjective nor a theorem.
    """
    original = list(lines)
    if original.count("証明") != 1 or original.count("□") != 1:
        return original
    certificate = _certified_hopf_lift(model)
    if certificate is None:
        return original
    scope, root, cyclic_step, positions = certificate
    injective_step, codomain_step, image_step = cyclic_step.premises
    group_relation = root.conclusion
    codomain_relation = codomain_step.conclusion
    image_relation = image_step.conclusion
    # The existing lift's typed generator identity is already checked by
    # hopf_lift_inputs().  Its internal CyclicStructureStatement may use a
    # different generator spelling from the published root Relation.  Match
    # the two *displayed* copies of the root's certified conclusion instead.
    root_latex, root_fallback = _group_proof_statement_latex(group_relation)
    codomain_latex, codomain_fallback = _group_proof_statement_latex(codomain_relation)
    if (root_fallback is not None or codomain_fallback is not None
            or not root_latex or not codomain_latex):
        return original
    source_group = group_tex(group_relation.lhs)
    target_group = group_tex(codomain_relation.lhs)
    if not source_group or not target_group:
        return original
    # The general Hopf-lift premise already certifies the *typed* generator
    # identity. A source generator can have a different internal spelling from
    # the canonical public group generator; do not compare their TeX strings.
    # Use the same public generator renderer as the cited codomain equation.
    try:
        generator_tex = render_toda_public_group_generator_latex(
            codomain_relation.rhs.generator,
        )
    except (TypeError, ValueError, AttributeError):
        return original
    if not generator_tex:
        return original
    boundary = original.index("証明")
    final = f"以上より, ${root_latex}$."
    intermediate = f"${root_latex}$."
    intermediate_indices = [
        i for i in range(boundary + 1, len(original))
        if original[i] == intermediate
    ]
    final_indices = [
        i for i in range(boundary + 1, len(original))
        if original[i] == final
    ]
    # R3R11 has already certified every equality in its compact Hopf chain.
    # Match the source numbers of the actual proved image step, not a guessed
    # generator-name spelling or a narrative line from an unrelated proof.
    image_sources = _source_numbers(model, positions[2], scope)
    image_prefix = (
        ", ".join(f"[R{number}]" for number in image_sources)
        + "より, $H("
    )
    image_indices = [
        i for i in range(boundary + 1, len(original))
        if len(image_sources) >= 2
        and original[i].startswith(image_prefix)
        and original[i].endswith(f"={generator_tex}$.")
        and original[i].count("$") == 2
    ]
    # The common renderer inserts spacing after "H:" and decorates the
    # sentence using the proved exactness premises. Reuse that same typed
    # sentence instead of guessing its textual punctuation or whitespace.
    # The certificate has already identified this exact MapInjective step.
    injectivity_sentence = typed_sentence(
        injective_step.conclusion, injective_step,
    )
    if (not isinstance(injectivity_sentence, str)
            or not injectivity_sentence.endswith("は単射.")):
        return original
    injection_indices = [
        i for i in range(boundary + 1, len(original))
        if original[i] == injectivity_sentence
    ]
    if (len(intermediate_indices) != 1 or len(final_indices) != 1
            or len(image_indices) != 1 or len(injection_indices) != 1):
        return original
    duplicate_at = intermediate_indices[0]
    final_at = final_indices[0]
    if not (injection_indices[0] < image_indices[0] < duplicate_at < final_at):
        return original
    source_numbers = _source_numbers(model, positions[1], scope)
    # The target group structure must already be displayed with its real
    # unique source. Without that source binding, leave all text untouched.
    if len(source_numbers) != 1:
        return original
    expected = f"[R{source_numbers[0]}]より, ${codomain_latex}$."
    if original.count(expected) != 1:
        return original
    source_prefix = f"[R{source_numbers[0]}]より, "
    surjective = (
        f"{source_prefix}${generator_tex}$ は ${target_group}$ の生成元であり, "
        "$H$ の像に含まれるので, $H$ は全射."
    )
    isomorphism = "すでに $H$ は単射なので, $H$ は同型."
    changed = []
    for index, line in enumerate(original):
        if index == duplicate_at:
            changed.extend((surjective, "", isomorphism))
        else:
            changed.append(line)
    return changed

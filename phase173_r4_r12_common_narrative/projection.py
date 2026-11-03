"""Project source-certified Toda Proposition 4.4 proof roots into one narrative.

This module cannot prove a goal or create a citation. The verified root, exact
source steps, and citation identities are mandatory. pi_7^4 retains its fully
reviewed legacy wording; later roots share one dimension-independent path.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import (
    ProofNarrativeModel,
    root_ancestor_step_indices,
)
from phase169_r10e4_ordered_db_prior.db_prior import DB_LOCATOR_PREFIX
from phase172_r5_prior_reference_display.projection import (
    display_prior_reference_locator,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
)
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from proof import ProofRule, ProofStep
from toda_human_readable_renderer import (
    render_toda_public_group_generator_latex,
    render_toda_public_group_relation_latex,
)
from phase173_r4_r4_typed_generator_audit.audit import _group_components

LEGACY_ROOT = "Toda (5.6) pi_7^4 source-bound direct-sum presentation"
SOURCE_FIRST_ROOT = "Toda Proposition 4.4 source-first n=4 typed direct-sum transport"
GENERIC_ROOT = "Toda Proposition 4.4 generic n=4 typed direct-sum transport"


def _step_index(model: ProofNarrativeModel, step: ProofStep) -> int:
    matches = [i for i, value in enumerate(model.steps) if value is step]
    if len(matches) != 1:
        matches = [i for i, value in enumerate(model.steps) if value == step]
    if len(matches) != 1:
        raise ValueError("Ambiguous proof ancestor in narrative model")
    return matches[0]


def _source_number(
    model: ProofNarrativeModel, step: ProofStep, *, locator: str | None = None,
    db_prior: bool = False,
) -> int:
    index = _step_index(model, step)
    numbers = model.step_citation_numbers[index]
    if len(numbers) != 1:
        raise ValueError("Missing or ambiguous cited source")
    number = numbers[0]
    citation = next((item for item in model.citations if item.number == number), None)
    if citation is None or index not in citation.step_indices:
        raise ValueError("Unbound source citation")
    actual = citation.reference.locator or citation.reference.label
    if locator is not None and actual != locator:
        raise ValueError("Source locator does not match the proof")
    if db_prior:
        if (not isinstance(actual, str)
                or not actual.startswith(DB_LOCATOR_PREFIX)
                or display_prior_reference_locator(citation, model) is None):
            raise ValueError("A prior DB source is not authenticated")
    return number


def _generator_image_lines(
    first: object, second: object, dimension: int,
) -> tuple[str, ...]:
    left = _group_components(first)
    right = _group_components(second)
    if left is None or right is None:
        raise ValueError("Unsupported source group presentation")
    if not left and not right:
        return ("両側の先行群はいずれも零群であり、生成元の像を確認する必要はない.",)
    result: list[str] = []
    for component in left:
        generator = render_toda_public_group_generator_latex(component.generator)
        if not isinstance(generator, str) or not generator:
            raise ValueError("Unrenderable verified suspension generator")
        result.append(
            rf"$\Phi_{{{dimension}}}({generator},0)=E({generator})$."
        )
    for component in right:
        generator = render_toda_public_group_generator_latex(component.generator)
        if not isinstance(generator, str) or not generator:
            raise ValueError("Unrenderable verified composition generator")
        result.append(
            rf"$\Phi_{{{dimension}}}(0,{generator})=\nu_4\circ({generator})$."
        )
    return tuple(result)


def project_verified_toda56_narrative(
    result: PartialProofResult, model: ProofNarrativeModel, markdown: str,
) -> str:
    """Preserve other renderers; rewrite only independently verified n=4 roots.

    The printed identities are the component images of the already proved
    Proposition 4.4 map. No unpublished generator alias is asserted here.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    if not isinstance(markdown, str):
        raise TypeError("markdown must be str")
    if (result.target.sphere_dimension != 4
            or result.status is not ProofSearchStatus.COMPLETE):
        return markdown
    if model.root_index is None or model.root_index >= len(model.steps):
        raise ValueError("Complete Toda narrative requires a root")
    root = model.steps[model.root_index]
    root_name = getattr(getattr(root, "inference_rule", None), "name", None)
    if result.target.group_dimension == 7 and root_name == LEGACY_ROOT:
        from phase173_r4_r1_narrative_source_fix.projection import (
            project_verified_pi74_narrative,
        )
        return project_verified_pi74_narrative(result, model, markdown)
    if root_name not in (SOURCE_FIRST_ROOT, GENERIC_ROOT):
        return markdown
    if (model.status is not ProofSearchStatus.COMPLETE or result.open_goals
            or model.open_goals or model.target != result.target
            or root.conclusion != result.conclusion
            or root.rule is not ProofRule.INFERENCE
            or len(root.premises) != 4
            or not root.inference_rule.match_guard(root.premises, {})
            or "使用する結果" not in markdown):
        raise ValueError("Unverified Toda direct-sum narrative root")
    ancestors = root_ancestor_step_indices(model.steps, model.root_index)
    theorem, first, second, hopf = root.premises
    if (theorem.rule is not ProofRule.GIVEN
            or type(theorem.conclusion) is not TodaProp44UniversalStatement
            or theorem.conclusion != TodaProp44UniversalStatement()
            or first.rule is not ProofRule.GIVEN
            or second.rule is not ProofRule.GIVEN
            or hopf.rule is not ProofRule.INFERENCE
            or hopf.conclusion != canonical_hopf_relation()
            or len(hopf.premises) != 1
            or hopf.premises[0].rule is not ProofRule.GIVEN
            or type(hopf.premises[0].conclusion) is not TodaLemma54TypedSource
            or hopf.premises[0].conclusion != TodaLemma54TypedSource()):
        raise ValueError("Typed Toda sources are incomplete")
    source_steps = (theorem, first, second, hopf.premises[0])
    if any(_step_index(model, step) not in ancestors for step in source_steps):
        raise ValueError("Unrelated source citation cannot be used")
    prop_n = _source_number(model, theorem, locator="Proposition 4.4")
    first_n = _source_number(model, first, db_prior=True)
    second_n = _source_number(model, second, db_prior=True)
    lemma_n = _source_number(model, hopf.premises[0], locator="Lemma 5.4")
    if len({prop_n, first_n, second_n, lemma_n}) != 4:
        raise ValueError("Four independently cited premises required")
    dimension = result.target.group_dimension
    first_formula = render_toda_public_group_relation_latex(first.conclusion)
    second_formula = render_toda_public_group_relation_latex(second.conclusion)
    target_formula = render_toda_public_group_relation_latex(result.conclusion)
    if not all(isinstance(x, str) and x for x in
               (first_formula, second_formula, target_formula)):
        raise ValueError("Unsupported typed group structure")
    if root_name == GENERIC_ROOT and not isinstance(result.conclusion, TodaPrimaryGroupZeroStatement):
        from phase173_r4_r10_general_toda56_core.core import checked_general_inputs
        if checked_general_inputs(result.conclusion) != (first.conclusion, second.conclusion):
            raise ValueError("General root generator shape changed")
    image_lines = _generator_image_lines(first.conclusion, second.conclusion, dimension)
    marker = "\n証明\n"
    if markdown.count(marker) != 1:
        raise ValueError("Unexpected canonical narrative sections")
    references = markdown.split(marker, 1)[0].rstrip()
    lines = [
        references, "", "証明", "",
        f"$\\pi_{{{dimension}}}^4$ の群構造を決定する.", "",
        f"[R{prop_n}]の一般形は次の同型である.", "",
        r"$\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}"
        r"\xrightarrow{\ \cong\ }\pi_i^n,\quad"
        r"(\beta,\gamma)\longmapsto E\beta+\alpha\circ\gamma$", "",
        f"[R{lemma_n}]より $H(\\nu_4)=\\iota_7$ である.", "",
        f"[R{prop_n}]を $n=4$, $i={dimension}$, $\\alpha=\\nu_4$ に特殊化する.", "",
        rf"$\Phi_{{{dimension}}}:\pi_{{{dimension - 1}}}^3\oplus"
        rf"\pi_{{{dimension}}}^7\xrightarrow{{\ \cong\ }}\pi_{{{dimension}}}^4,"
        r"\quad(\beta,\gamma)\longmapsto E\beta+\nu_4\circ\gamma$", "",
        f"[R{first_n}]より ${first_formula}$.", "",
        f"[R{second_n}]より ${second_formula}$.", "",
        "生成元の対応は、この同型写像の成分ごとに次のようになる.", "",
    ]
    for image_line in image_lines:
        lines.extend((image_line, ""))
    lines.extend((f"したがって ${target_formula}$.", "", "□", ""))
    return "\n".join(lines)

"""Format an existing abstract certificate; do not infer mathematical facts.

The default Model-backed renderer and legacy Web adapter share this
formatter. No n/k special case or alternate Narrative pipeline exists.
"""
from __future__ import annotations

from phase165_r52_partial_proof import (
    CertifiedAbstractStructure,
    PartialProofResult,
    ProofSearchStatus,
)


def abstract_invariants_latex(invariants: tuple[tuple[str, int], ...]) -> str:
    """Format *already certified* invariant summands without generator names."""
    if not isinstance(invariants, tuple):
        raise TypeError("abstract invariant summands must be a tuple")
    counts: dict[tuple[str, int], int] = {}
    for item in invariants:
        if not isinstance(item, tuple) or len(item) != 2:
            raise ValueError("abstract invariant summand must be a pair")
        kind, order = item
        if not (
            (kind == "free" and type(order) is int and order == 0)
            or (kind == "finite" and type(order) is int and order >= 2)
        ):
            raise ValueError("unsupported abstract invariant summand")
        counts[item] = counts.get(item, 0) + 1
    if not counts:
        return "0"
    expressions: list[str] = []
    for (kind, order), count in sorted(counts.items()):
        atom = r"\mathbb{Z}" if kind == "free" else rf"\mathbb{{Z}}/{order}"
        if count > 1:
            atom = rf"\left({atom}\right)^{{{count}}}"
        expressions.append(atom)
    return r" \oplus ".join(expressions)


def render_certified_abstract_section(result: PartialProofResult) -> str:
    """Return one source-derived abstract-only section, or empty Markdown.

    The current named Goal, public COMPLETE flag, references and open goals
    remain entirely owned by the canonical search and Narrative renderer.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("expected canonical PartialProofResult")
    structure = result.abstract_structure
    if structure is None:
        return ""
    if (
        not isinstance(structure, CertifiedAbstractStructure)
        or structure.group != result.target
        or result.status not in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
        or result.conclusion is not None
    ):
        raise ValueError("unverified abstract result cannot be presented as a certificate")
    return _render_abstract_claim(result.target, structure)


def _verified_abstract_progress_lines(
    structure: CertifiedAbstractStructure,
) -> tuple[str, ...]:
    """Present actual certified premises, without adopting named-generator goals.

    The certificate's original typed inference guard has already checked its
    four premises. Their registered source metadata is used only for display.
    No new proof step, citation identity, or mathematical conclusion is made.
    """
    from web_group_proof_common import _group_proof_statement_latex

    root = structure.proof_step
    if len(root.premises) != 4:
        raise ValueError("verified abstract inference requires four premises")
    theorem_step, first_prior, second_prior, hopf_step = root.premises

    def source_label(step: object) -> str | None:
        rule = getattr(step, "inference_rule", None)
        reference = getattr(rule, "literature_reference", None)
        if reference is None:
            return None
        label = reference.locator or reference.label
        return label if isinstance(label, str) and label.strip() else None

    def verified_math(step: object) -> str | None:
        try:
            latex, fallback = _group_proof_statement_latex(step.conclusion)
        except (TypeError, ValueError):
            return None
        return f"${latex}$" if latex is not None and fallback is None else None

    theorem_label = source_label(root)
    theorem_description = (
        f"{theorem_label} の適用前提となる定理を検証した."
        if theorem_label is not None else "一般定理の前提を検証した."
    )
    lines = [theorem_description]
    for prior in (first_prior, second_prior):
        formula = verified_math(prior)
        locator = source_label(prior)
        if formula is not None and locator is not None:
            lines.append(f"先行データベースの {formula} を {locator} により確認した.")
        elif formula is not None:
            lines.append(f"先行データベースの検証済み結果 {formula} を確認した.")
        else:
            lines.append("先行データベースの型付き結果を検証した.")

    hopf_formula = verified_math(hopf_step)
    hopf_locator = source_label(hopf_step)
    if hopf_formula is not None and hopf_locator is not None:
        lines.append(f"{hopf_locator} から {hopf_formula} を導いた.")
    elif hopf_formula is not None:
        lines.append(f"検証済みの Hopf 関係 {hopf_formula} を導いた.")
    else:
        lines.append("検証済みの Hopf 関係を前提として確認した.")

    theorem_reference = theorem_label or "検証済みの一般定理"
    lines.append(
        f"これらの検証済み前提を使い, {theorem_reference} により"
        "抽象群構造を導いた."
    )
    return tuple(lines)


def _render_abstract_claim(target: object, structure: CertifiedAbstractStructure) -> str:
    """Show certified progress and the abstract claim, never named generators."""
    if type(target.group_dimension) is not int or type(target.sphere_dimension) is not int:
        raise ValueError("abstract result has nonconcrete group dimensions")
    invariant_latex = abstract_invariants_latex(structure.invariant_summands)
    target_latex = rf"\pi_{{{target.group_dimension}}}^{{{target.sphere_dimension}}}"
    progress = "\n\n".join(_verified_abstract_progress_lines(structure))
    return (
        "## 検証済みの途中経過\n\n"
        + progress
        + "\n\n"
        + "## 証明済みの抽象群構造\n\n"
        + rf"${target_latex} \cong {invariant_latex}$."
        + "\n\n"
        + "これは出典検査済みの抽象群 ProofStep による結論であり、"
        + "登録済みの先行 DB 群を前提とする。"
        + "記名生成元の対応は未証明であり、上記の未解決 Goal と探索状態は変わらない。"
    )


def render_certified_abstract_model_section(model: object) -> str:
    """Render only certificate evidence explicitly carried by ProofNarrativeModel."""
    from phase168_r3_3_proof_narrative_model import ProofNarrativeModel

    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("expected canonical ProofNarrativeModel")
    structure = model.abstract_structure
    if structure is None:
        return ""
    if (
        not isinstance(structure, CertifiedAbstractStructure)
        or structure.group != model.target
        or model.status not in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
        or model.root_index is not None
    ):
        raise ValueError("unverified Model abstract result cannot be presented")
    return _render_abstract_claim(model.target, structure)

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


def _render_abstract_claim(target: object, structure: CertifiedAbstractStructure) -> str:
    """Format only an already certified abstract structure, never identify generators."""
    if type(target.group_dimension) is not int or type(target.sphere_dimension) is not int:
        raise ValueError("abstract result has nonconcrete group dimensions")
    invariant_latex = abstract_invariants_latex(structure.invariant_summands)
    target_latex = rf"\pi_{{{target.group_dimension}}}^{{{target.sphere_dimension}}}"
    return (
        "## 証明済みの抽象群構造\n\n"
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

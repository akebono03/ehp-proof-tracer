"""Phase 169 R3K: presentation-only projection of proven map properties.

The caller supplies canonical ProofSteps and source-linked Narrative Model data.
Nothing here derives a conclusion, interprets the statement semantically, or adds a citation.
"""
from __future__ import annotations

import re

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from proof import ProofRule, Relation, RelationType


_PROPERTY_WORDS = {
    "surjective": "全射",
    "injective": "単射",
    "the zero map": "零写像",
    "an isomorphism": "同型",
}
_PROPERTY_PATTERN = re.compile(
    r"\s*(?:\\text\{\s*is\s+"
    r"(surjective|injective|the zero map|an isomorphism)\s*\}"
    r"|is\s+(surjective|injective|the zero map|an isomorphism))\s*$"
)


def project_proven_map_property(step, latex: str) -> str | None:
    """Translate a known suffix without changing the map or its proof.

    The renderer uses the returned *whole sentence* only for derived ProofSteps.
    An unknown suffix, an unproved step, or a non-LaTeX field stays unchanged.
    """
    if step.rule is not ProofRule.INFERENCE or not isinstance(latex, str):
        return None
    match = _PROPERTY_PATTERN.search(latex)
    if match is None:
        return None
    words = match.group(1) or match.group(2)
    math = latex[:match.start()].rstrip()
    if not math:
        return None
    return f"${math}$ は{_PROPERTY_WORDS[words]}."


def duplicate_group_relation_notice(model, step_index: int, previous_latex: set[str]) -> str | None:
    """Replace a repeated *display* with its source tags, never a new proof.

    Only typed cyclic group relations are eligible, and the root is preserved.
    The caller records a formula in previous_latex only after it has been shown.
    """
    from web_group_proof_common import _group_proof_statement_latex
    step = model.steps[step_index]
    fact = step.conclusion
    if (model.root_index == step_index
            or not isinstance(fact, Relation)
            or fact.relation_type is not RelationType.EQUALITY
            or not isinstance(fact.lhs, TodaPrimaryGroup)
            or not isinstance(fact.rhs, FiniteCyclicGroup)):
        return None
    latex, fallback = _group_proof_statement_latex(fact)
    if fallback is not None or not latex or latex not in previous_latex:
        return None
    numbers = model.step_citation_numbers[step_index]
    if not numbers:
        return ""
    references = ", ".join(f"[R{number}]" for number in numbers)
    return references + "による導出も同じ群構造を示す."

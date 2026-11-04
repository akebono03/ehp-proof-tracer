# Phase 173 final R1: full replacement test files

Only three historical test files are changed. Every import and test
function is included below without abbreviated code.

## `tests/test_phase167_r2_range_dedup.py`

```python
"""Phase 167 reference rules under the Phase 168 common Model Renderer."""
from web_group_proof import build_standard_web_group_proof_view


def _reference_text(n: int, k: int) -> str:
    view = build_standard_web_group_proof_view(n, k, 2, "narrative")
    assert view.key == "generic-complete-proof"
    lines = view.rendered_lines

    def is_section(line, title):
        return (line.kind in ("text", "heading")
                and line.prefix == title and line.statement_latex is None
                and line.suffix == "")

    first = next(i for i, line in enumerate(lines)
                 if is_section(line, "使用する結果"))
    # The canonical Web layout replaces the old Proof heading with a
    # single separator; Reference assertions must exclude the proof body.
    separators = [
        i for i, line in enumerate(lines)
        if i > first and line.kind == "separator"
    ]
    assert len(separators) == 1
    last = separators[0]
    assert first < last
    return "\n".join(
        " ".join((line.prefix, line.statement_latex or "", line.suffix))
        for line in lines[first + 1:last]
    )


def test_phase167_r2_pi32_diagonal_range_once():
    reference = _reference_text(2, 1)
    diagonal = next(line for line in reference.splitlines() if r"\pi_{n}^{n}" in line)
    assert diagonal.count(r"n\ge 1") == 1
    assert reference.count(r"\pi_{n}^{n}") == 1
    assert r"\pi_i^1=0" in reference
    assert "Proposition 5.1" in reference


def test_phase167_r2_pi43_diagonal_range_once():
    reference = _reference_text(3, 1)
    diagonal = next(line for line in reference.splitlines() if r"\pi_{n}^{n}" in line)
    assert diagonal.count(r"n\ge 1") == 1
    assert reference.count(r"\pi_{n}^{n}") == 1
    assert r"\pi_i^n=0" in reference
    assert "Proposition 5.1" in reference
```

## `tests/test_phase167_r2_shared_reference.py`

```python
"""Phase 167 shared reference projection under the Phase 168 Web route."""
from web_group_proof import build_standard_web_group_proof_view
from toda_group_proof_narrative_references import (
    TodaGroupProofNarrativeReferenceEntry,
    render_toda_group_proof_narrative_reference_entries_markdown,
)
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep


def test_phase167_r2_pi43_reference_has_two_general_results():
    view = build_standard_web_group_proof_view(3, 1, 2, "narrative")
    assert view.key == "generic-complete-proof"
    lines = view.rendered_lines

    def is_section(line, title):
        return (line.kind in ("text", "heading")
                and line.prefix == title and line.statement_latex is None
                and line.suffix == "")

    reference_index = next(
        i for i, line in enumerate(lines)
        if is_section(line, "使用する結果")
    )
    # The common Web layout turns the former Proof heading into exactly one
    # separator. Keep the boundary semantic instead of relying on the old title.
    separators = [
        i for i, line in enumerate(lines)
        if i > reference_index and line.kind == "separator"
    ]
    assert len(separators) == 1
    proof_index = separators[0]
    reference_lines = lines[reference_index + 1:proof_index]
    reference_text = "\n".join(
        " ".join((line.prefix, line.statement_latex or "", line.suffix))
        for line in reference_lines
    )
    assert r"\pi_{n}^{n}" in reference_text
    assert r"\pi_i^n=0" in reference_text
    assert "Proposition 5.1" in reference_text
    assert reference_text.count(r"\pi_{n}^{n}") == 1


def test_phase167_r2_other_references_keep_common_statement_lines():
    ref = LiteratureReference(label="Generic source", locator="Generic source")
    step = ProofStep(
        conclusion="general claim",
        premises=(),
        rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="generic",
            literature_reference=ref,
        ),
    )
    entry = TodaGroupProofNarrativeReferenceEntry(
        number=1,
        reference=ref,
        proof_steps=(step,),
    )
    rendered = render_toda_group_proof_narrative_reference_entries_markdown(
        (entry,),
        {1: ("$x=y$",)},
    )
    assert "$x=y$" in rendered
    assert "**[R1] Generic source.**" in rendered
```

## `tests/test_phase167_r2_unified_reference.py`

```python
"""Phase 167 general references against the current common Renderer output."""
from web_group_proof import build_standard_web_group_proof_view


def _reference_text(n: int, k: int) -> str:
    view = build_standard_web_group_proof_view(n, k, 2, "narrative")
    assert view.key == "generic-complete-proof"
    lines = view.rendered_lines

    def is_section(line, title):
        return (line.kind in ("text", "heading")
                and line.prefix == title and line.statement_latex is None
                and line.suffix == "")

    first = next(i for i, line in enumerate(lines)
                 if is_section(line, "使用する結果"))
    # The canonical Web layout replaces the old Proof heading with a
    # single separator; Reference assertions must exclude the proof body.
    separators = [
        i for i, line in enumerate(lines)
        if i > first and line.kind == "separator"
    ]
    assert len(separators) == 1
    last = separators[0]
    assert first < last
    return "\n".join(
        " ".join((line.prefix, line.statement_latex or "", line.suffix))
        for line in lines[first + 1:last]
    )


def test_phase167_r2_pi32_reference_uses_general_form():
    text = _reference_text(2, 1)
    assert r"\pi_i^1=0" in text
    assert r"\pi_{n}^{n}" in text
    assert r"\pi_{3}^{3}" not in text
    assert r"\pi_{2}^{1}" not in text
    assert "Proposition 5.1" in text


def test_phase167_r2_pi43_reference_uses_general_form():
    text = _reference_text(3, 1)
    assert r"\pi_{n}^{n}" in text
    assert r"\pi_i^n=0" in text
    assert text.count(r"\pi_{n}^{n}") == 1
    assert "Proposition 5.1" in text
```

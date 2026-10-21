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
    reference_index = next(
        i for i, line in enumerate(lines)
        if line.kind == "heading" and line.prefix == "使用する結果"
    )
    proof_index = next(
        i for i, line in enumerate(lines)
        if i > reference_index
        and line.kind == "heading"
        and line.prefix == "証明"
    )
    reference_lines = lines[reference_index + 1:proof_index]
    reference_text = "\n".join(
        " ".join((line.prefix, line.statement_latex or "", line.suffix))
        for line in reference_lines
    )
    assert r"\pi_{n}^{n}" in reference_text
    assert r"\pi_{i}^{n}" in reference_text
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

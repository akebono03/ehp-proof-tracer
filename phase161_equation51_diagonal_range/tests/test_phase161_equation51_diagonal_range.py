from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from toda_literature_statement_boundary import get_toda_fixed_statement_component
from toda_group_proof_narrative_references import (
    TodaGroupProofNarrativeReferenceEntry,
    render_toda_group_proof_narrative_reference_entries_markdown,
)


def test_phase161_equation51_diagonal_range_catalog():
    component = get_toda_fixed_statement_component("(5.1)", "diagonal_identity_group")
    assert component.range_text == "n >= 1"


def test_phase161_equation51_diagonal_range_reference_rendering():
    step = ProofStep(
        conclusion="diagonal identity group",
        premises=(),
        rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(
            name="Toda (5.1) diagonal identity group",
            literature_reference=LiteratureReference(label="Toda (5.1)", locator="(5.1)"),
        ),
    )
    entry = TodaGroupProofNarrativeReferenceEntry(
        number=1,
        reference=LiteratureReference(label="Toda (5.1)", locator="(5.1)"),
        proof_steps=(step,),
    )
    rendered = render_toda_group_proof_narrative_reference_entries_markdown((entry,))
    assert r"\pi_{n}^{n}" in rendered
    assert r"(n \ge 1)" in rendered
    assert rendered.count(r"(n \ge 1)") == 1

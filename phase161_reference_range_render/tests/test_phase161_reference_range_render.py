from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from toda_group_proof_narrative_references import (
    TodaGroupProofNarrativeReferenceEntry,
    render_toda_group_proof_narrative_reference_entries_markdown,
)


def _entry(number, locator, name):
    reference = LiteratureReference(label='Toda ' + locator, locator=locator)
    step = ProofStep(
        conclusion=name,
        premises=(),
        rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name=name, literature_reference=reference),
    )
    return TodaGroupProofNarrativeReferenceEntry(number=number, reference=reference, proof_steps=(step,))


def test_phase161_reference_range_is_rendered_from_catalog():
    entries = (
        _entry(1, '(5.2)', 'Toda 5.2 eta_2 composition isomorphism'),
        _entry(2, 'Proposition 5.1', 'Toda Proposition 5.1 finite-dimensional integration'),
    )
    rendered = render_toda_group_proof_narrative_reference_entries_markdown(
        entries,
        {
            1: (r'$\eta_2\circ-:\pi_i^3\to\pi_i^2$ は同型.',),
            2: (r'$\pi_{n+1}^n=\mathbb{Z}/2\{\eta_n\}$.',),
        },
    )
    assert r'(i \ge 3)' in rendered
    assert r'(n \ge 3)' in rendered


def test_phase161_reference_range_unrelated_reference_unchanged():
    entry = _entry(1, 'Proposition 5.1', 'Toda Proposition 5.1 pi_3^2 group relation')
    statement = r'$\pi_3^2=\mathbb{Z}\{\eta_2\}$.'
    rendered = render_toda_group_proof_narrative_reference_entries_markdown(
        (entry,), {1: (statement,)}
    )
    assert statement in rendered
    assert r'\ge' not in rendered

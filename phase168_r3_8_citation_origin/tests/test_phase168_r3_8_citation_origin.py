from phase168_r3_3_proof_narrative_model import NarrativeCitation, ProofNarrativeModel
from phase168_r3_8_citation_origin import inspect_citation_origins
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep


def _model(refs):
    steps = tuple(ProofStep(
        conclusion=index, premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name=f"step-{index}"),
    ) for index in range(len(refs)))
    citations = tuple(NarrativeCitation(
        number=index + 1,
        reference=LiteratureReference(label=label, locator=locator),
        step_indices=(index,),
    ) for index, (label, locator) in enumerate(refs))
    return ProofNarrativeModel(
        steps=steps,
        citations=citations,
        step_citation_numbers=tuple((i + 1,) for i in range(len(refs))),
        root_index=len(steps) - 1 if steps else None,
    )


def test_two_expected_sources_are_recognized():
    report = inspect_citation_origins(_model((
        ("Toda (5.1)", "(5.1)"),
        ("Toda Proposition 5.1", "Proposition 5.1"),
    )))
    assert report.matches_expected_sources
    assert report.unexpected_locators == ()
    assert report.repeated_locators == ()


def test_same_locator_with_different_labels_is_reported_not_removed():
    report = inspect_citation_origins(_model((
        ("Toda (5.1)", "(5.1)"),
        ("(5.1)", "(5.1)"),
        ("Proposition 5.1", "Proposition 5.1"),
    )))
    assert report.matches_expected_sources
    assert report.repeated_locators == ("(5.1)",)
    assert report.origins[1].duplicate_locator_of == 1
    assert len(report.origins) == 3


def test_other_source_is_reported_even_when_expected_two_exist():
    report = inspect_citation_origins(_model((
        ("(5.1)", "(5.1)"),
        ("Proposition 4.2", "Proposition 4.2"),
        ("Proposition 5.1", "Proposition 5.1"),
    )))
    assert not report.matches_expected_sources
    assert report.unexpected_locators == ("Proposition 4.2",)


def test_missing_expected_source_does_not_get_invented():
    report = inspect_citation_origins(_model((("(5.1)", "(5.1)"),)))
    assert report.missing_locators == ("Proposition 5.1",)
    assert len(report.origins) == 1

from types import SimpleNamespace

from phase168_r3_7_cutover_gate import inspect_narrative_cutover
from phase168_r3_3_proof_narrative_model import NarrativeCitation, ProofNarrativeModel
from proof import LiteratureReference


def _model():
    citation = NarrativeCitation(1, LiteratureReference(label="Proposition 5.1", locator="Proposition 5.1"), (0,))
    return ProofNarrativeModel((), (citation,), (), None)


def _line(prefix, suffix=""):
    return SimpleNamespace(prefix=prefix, suffix=suffix)


def test_matching_reference_and_body_pass():
    report = inspect_narrative_cutover(_model(), (_line("**[R1] Proposition 5.1.**"), _line("[R1]より, ")))
    assert report.safe_to_reuse_legacy_body
    assert report.body_numbers == (1,)


def test_missing_reference_rejects_cutover():
    report = inspect_narrative_cutover(_model(), (_line("証明"),))
    assert not report.safe_to_reuse_legacy_body
    assert "differ" in report.issues[0]


def test_wrong_reference_identity_rejects_cutover():
    report = inspect_narrative_cutover(_model(), (_line("**[R1] (5.2).**"),))
    assert not report.safe_to_reuse_legacy_body


def test_dangling_body_number_rejects_cutover():
    report = inspect_narrative_cutover(_model(), (_line("**[R1] Proposition 5.1.**"), _line("[R9]より, ")))
    assert not report.safe_to_reuse_legacy_body
    assert report.body_numbers == (9,)

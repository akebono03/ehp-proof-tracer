from phase168_r3_41p12_publication_boundary_audit.audit import (
    citation_numbers_in_proof,
    evaluate_publication,
)


def test_prior_when_target_is_bound_and_every_source_precedes():
    allowed = {("a", "target"), ("b", "target")}
    status = evaluate_publication("target", ["a", "b"], lambda a, b: (a, b) in allowed)
    assert status == "PRIOR"


def test_missing_target_is_not_accepted():
    assert evaluate_publication(None, ["a"], lambda a, b: True) == "UNVERIFIABLE_TARGET"


def test_missing_source_is_not_accepted():
    assert evaluate_publication("target", [], lambda a, b: True) == "MISSING_LINK"


def test_self_and_later_source_are_not_prior():
    assert evaluate_publication("target", ["target"], lambda a, b: a != b) == "NOT_PRIOR"
    assert evaluate_publication("target", ["a", "later"], lambda a, b: a == "a") == "NOT_PRIOR"


def test_citation_parser_only_reads_proof_markers():
    assert citation_numbers_in_proof("[R2]から[R10]を使う。 [R2]") == {2, 10}

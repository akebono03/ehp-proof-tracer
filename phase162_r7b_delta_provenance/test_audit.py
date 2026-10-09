"""Focused tests for the Delta(iota_5) provenance diagnostic."""
from types import SimpleNamespace

from audit import DELTA_MARKERS, build_report, delta_paragraphs


def test_delta_paragraphs_retains_only_target_and_preserves_repetition():
    target = r"$\Delta\left(\iota_{5}\right)=\pm a$."
    markdown = target + "\n\n" + r"$\eta_3=E\eta_2$." + "\n\n" + target
    assert delta_paragraphs(markdown) == (target, target)


def test_delta_audit_supports_empty_provenance_without_mutation():
    root = SimpleNamespace()
    presentation = SimpleNamespace(root_step=root, nodes=(), edges=())
    audit = SimpleNamespace(final_step=root, presentation=presentation, markdown="ordinary")
    report = build_report(audit, ())
    assert "Root preserved: True" in report
    assert "Matching ProofStep identities: 0" in report
    assert "No deduplication was attempted." in report


def test_delta_marker_is_explicit_not_all_delta_formulas():
    assert DELTA_MARKERS == (r"\Delta\left(\iota_{5}\right)", r"\Delta(\iota_{5})")
    assert delta_paragraphs(r"$\Delta(\iota_{6})=0$.") == ()

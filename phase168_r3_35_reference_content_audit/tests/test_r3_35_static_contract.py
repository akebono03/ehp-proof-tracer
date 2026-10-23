from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]


def test_model_has_linked_assertion_ids():
    source = (PROJECT / "phase168_r3_3_proof_narrative_model.py").read_text(encoding="utf-8")
    assert "assertion_ids" in source
    assert "reference_ids" in source


def test_renderer_reference_section_uses_model_citations():
    source = (PROJECT / "phase168_r3_5_model_renderer.py").read_text(encoding="utf-8")
    assert "for citation in model.citations" in source
    assert "citation.reference.locator" in source

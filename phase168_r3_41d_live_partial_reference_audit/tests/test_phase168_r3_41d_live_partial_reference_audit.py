"""Focused tests for the read-only citation and partial-section audit."""
from __future__ import annotations

from types import SimpleNamespace

from phase168_r3_41d_live_partial_reference_audit.audit_core import (
    audit_citation_projection,
    markdown_reference_text,
    normalize_visible,
    section_bullets,
    web_line_text,
    web_reference_text,
)


def _fake_view(reference_heading: str, reference_body: str):
    def line(text: str):
        return SimpleNamespace(prefix=text, statement_latex=None,
                               suffix="", segments=(), kind="text")
    return SimpleNamespace(rendered_lines=(
        line("使用する結果"), line(reference_heading), line(reference_body),
        line("証明"), line("以上より"),
    ))


def _fake_model(bodies=(r"$\pi_{4}^{3}=\mathbb{Z}/2\{\eta_{3}\}$.",),
                assertion_ids=("a",)):
    step = SimpleNamespace(rule=SimpleNamespace(value="given"), inference_rule=None)
    ref = SimpleNamespace(locator="Proposition 5.1", label="Proposition 5.1")
    citation = SimpleNamespace(number=1, reference=ref, step_indices=(0,),
                               assertion_ids=assertion_ids, reference_ids=("r",),
                               statement_bodies=bodies)
    model = SimpleNamespace(steps=(step,), citations=(citation,),
                            step_citation_numbers=((1,),))
    bridge = SimpleNamespace(proof_links=(SimpleNamespace(step=step, assertion_id="a"),))
    return model, bridge


def test_reference_body_is_checked_in_both_raw_and_web_sections():
    model, bridge = _fake_model()
    body = model.citations[0].statement_bodies[0]
    raw = ("使用する結果\n\n**[R1] Proposition 5.1.**\n\n"
           + body + "\n\n証明\n\n以上より\n")
    view = _fake_view("[R1] Proposition 5.1.", normalize_visible(body))
    result = audit_citation_projection(model, bridge, raw, view)
    assert result["issues"] == []
    assert result["citations"][0]["raw_heading_count"] == 1
    assert result["citations"][0]["bodies"][0]["web_reference_present"]


def test_registered_reference_without_body_is_reported_as_gap():
    model, bridge = _fake_model(bodies=())
    raw = "使用する結果\n\n**[R1] Proposition 5.1.**\n\n証明\n"
    view = _fake_view("[R1] Proposition 5.1.", "")
    result = audit_citation_projection(model, bridge, raw, view)
    assert "REGISTERED_ASSERTION_BODY_MISSING:R1" in result["issues"]
    assert result["citations"][0]["body_count"] == 0


def test_reference_body_missing_only_from_web_is_detected():
    model, bridge = _fake_model()
    body = model.citations[0].statement_bodies[0]
    raw = "使用する結果\n\n**[R1] Proposition 5.1.**\n\n" + body + "\n\n証明\n"
    view = _fake_view("[R1] Proposition 5.1.", "OTHER BODY")
    result = audit_citation_projection(model, bridge, raw, view)
    assert "REFERENCE_BODY_NOT_IN_WEB:R1" in result["issues"]
    assert "REFERENCE_BODY_NOT_RENDERED:R1" not in result["issues"]


def test_section_bullets_separate_goals_and_diagnostics():
    text = ("使用する結果\n\n証明\n\n## 未解決 Goal\n\n"
            "- first\n- second\n\n## 探索診断\n\n- missing rule\n")
    assert section_bullets(text, "未解決 Goal") == (True, ("first", "second"))
    assert section_bullets(text, "探索診断") == (True, ("missing rule",))
    assert section_bullets(text, "不存在") == (False, ())


def test_web_heading_prefix_is_preserved_and_proof_excluded_from_reference():
    heading = SimpleNamespace(prefix="探索診断", statement_latex=None,
                              suffix="", segments=(), kind="heading")
    assert web_line_text(heading) == "探索診断"
    view = _fake_view("[R1] Proposition 5.1.", "reference content")
    assert "reference content" in web_reference_text(view)
    assert "以上より" not in web_reference_text(view)
    assert markdown_reference_text("使用する結果\n証明\n") == "使用する結果"


def test_assertion_not_in_screened_proof_links_is_rejected():
    model, bridge = _fake_model(assertion_ids=("other-assertion",))
    body = model.citations[0].statement_bodies[0]
    raw = "使用する結果\n\n**[R1] Proposition 5.1.**\n\n" + body + "\n\n証明\n"
    view = _fake_view("[R1] Proposition 5.1.", normalize_visible(body))
    result = audit_citation_projection(model, bridge, raw, view)
    assert "UNMATCHED_ASSERTION_LINK:R1" in result["issues"]
    assert "USED_PROOF_LINK_OMITTED_FROM_MODEL" in result["issues"]

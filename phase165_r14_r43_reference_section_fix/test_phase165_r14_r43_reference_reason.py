from pathlib import Path
from phase165_r14_r41_proof_transfer import build_phase165_r41_pi32_common_replay
from phase165_r14_r43_reference_reason import _reference_rows, _exactness_reason_rows
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown


def _presentation():
    group = build_standard_toda_report(n=2,k=1).candidates[0].source_candidate.group_result
    return build_toda_group_proof_presentation(
        build_phase165_r41_pi32_common_replay(group,2,"narrative"))


def test_all_fixed_reference_locators_are_in_root_ancestry():
    rows = _reference_rows(_presentation())
    assert any("(5.1)" in r for r in rows)
    assert any("Proposition 4.2" in r for r in rows)
    assert any("Proposition 5.1" in r for r in rows)


def test_mathematical_reasons_depend_on_inference_steps():
    lines = _exactness_reason_rows(_presentation())
    assert any(r"\ker H" in line for line in lines)
    assert any(r"\operatorname{Im}\Delta" in line for line in lines)
    assert any(r"\operatorname{Im}H" in line for line in lines)


def test_public_narrative_has_nonempty_references():
    text = render_toda_group_proof_narrative_markdown(_presentation())
    section = text.split("使用する結果",1)[1].split("証明",1)[0]
    assert "(5.1)" in section
    assert "Proposition 4.2" in section
    assert "Proposition 5.1" in section


def test_public_narrative_has_exactness_explanations():
    text = render_toda_group_proof_narrative_markdown(_presentation())
    assert r"\operatorname{Im}\Delta=\ker E=0" in text
    assert r"\ker H=\operatorname{Im}E=0" in text
    assert r"\operatorname{Im}H=\ker\Delta" in text


def test_no_preexisting_rendering_regression():
    text = render_toda_group_proof_narrative_markdown(_presentation())
    assert "GeneratorImage" not in text
    assert "generic injective and surjective imply isomorphism" not in text
    assert "完全列" in text


def test_empty_reference_section_with_divider_is_populated(monkeypatch):
    import phase165_r14_r43_reference_reason as module
    monkeypatch.setattr(module, "_reference_rows", lambda p: ("Toda (5.1): $\\pi_2^1=0$",))
    monkeypatch.setattr(module, "_exactness_reason_rows", lambda p: ())
    original = "## 使用する結果\n\n---\n\n## 証明\n既存の証明.\n"
    result = module.enrich_common_narrative(object(), original)
    section = result.split("使用する結果", 1)[1].split("証明", 1)[0]
    assert "Toda (5.1)" in section
    assert "既存の証明." in result


def test_existing_nonempty_references_are_not_duplicated(monkeypatch):
    import phase165_r14_r43_reference_reason as module
    monkeypatch.setattr(module, "_reference_rows", lambda p: ("Toda (5.1): $x$",))
    monkeypatch.setattr(module, "_exactness_reason_rows", lambda p: ())
    original = "## 使用する結果\n[R1] Toda (5.1)\n---\n## 証明\n証明本文.\n"
    assert module.enrich_common_narrative(object(), original) == original

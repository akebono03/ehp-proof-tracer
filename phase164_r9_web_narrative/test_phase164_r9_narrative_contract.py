import pytest
from phase164_r9_narrative_contract import normalize_public_narrative_contract


def test_removes_repeated_subwindow_only():
    full = r'\pi_6^3\xrightarrow{H}\pi_6^5\xrightarrow{\Delta}\pi_4^2\xrightarrow{E}\pi_5^3\xrightarrow{H}\pi_5^5\xrightarrow{\Delta}\pi_3^2'
    part = r'\pi_6^5\xrightarrow{\Delta}\pi_4^2\xrightarrow{E}\pi_5^3\xrightarrow{H}\pi_5^5'
    text = '\\[\n' + full + '\n\\]\n\n証明\n\\[\n' + part + '\n\\]\n'
    result = normalize_public_narrative_contract(text)
    assert result.count(r'\[') == 1
    assert full in result
    assert '証明' in result


def test_keeps_different_sequence():
    text = '\\[\n\\pi_a\\to\\pi_b\\to\\pi_c\n\\]\n\\[\n\\pi_x\\to\\pi_y\\to\\pi_z\n\\]\n'
    assert normalize_public_narrative_contract(text) == text


def test_normalizes_connectors_without_moving_proof_claims():
    text = '完全性より, これより, $H$ は零写像.\n\n完全性より,\n\n完全性より,\n\n$E$ は全射.\n'
    result = normalize_public_narrative_contract(text)
    assert '完全性より, $H$ は零写像.' in result
    assert result.count('完全性より,') == 2
    assert '$E$ は全射.' in result


def test_preserves_other_sections_and_math():
    source = '## 使用する結果\n[R1] (5.3).\n## 証明\n$\\eta_3^2$\n□\n'
    assert normalize_public_narrative_contract(source) == source


def test_rejects_non_string():
    with pytest.raises(TypeError):
        normalize_public_narrative_contract(None)

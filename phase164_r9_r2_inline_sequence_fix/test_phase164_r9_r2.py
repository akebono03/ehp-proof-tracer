import pytest
from phase164_r9_narrative_contract import normalize_public_narrative_contract


FULL = (r'\pi_{6}^{3}\xrightarrow{H}\pi_{6}^{5}\xrightarrow{\Delta}'
        r'\pi_{4}^{2}\xrightarrow{E}\pi_{5}^{3}\xrightarrow{H}'
        r'\pi_{5}^{5}\xrightarrow{\Delta}\pi_{3}^{2}')
PART = (r'\pi_{6}^{5}\xrightarrow{\Delta}\pi_{4}^{2}'
        r'\xrightarrow{E}\pi_{5}^{3}\xrightarrow{H}\pi_{5}^{5}')


def test_inline_duplicate_subwindow_is_removed():
    raw = '## 証明\n$' + FULL + '$.\n\n[R1]より, $H$ は全射.\n\n$' + PART + '$.\n'
    normalized = normalize_public_narrative_contract(raw)
    assert normalized.count(r'\pi_{6}^{5}') == 1
    assert '[R1]より' in normalized
    assert '$' + PART + '$' not in normalized


def test_mixed_display_to_inline_is_removed():
    raw = '## 証明\n\\[\n' + FULL + '\n\\]\n\n$' + PART + '$.\n'
    assert normalize_public_narrative_contract(raw).count(r'\pi_{6}^{5}') == 1


def test_map_mismatch_does_not_remove():
    other = PART.replace(r'\xrightarrow{E}', r'\xrightarrow{H}')
    raw = '## 証明\n$' + FULL + '$\n$' + other + '$\n'
    assert '$' + other + '$' in normalize_public_narrative_contract(raw)


def test_unrelated_math_and_reference_not_affected():
    raw = '## 使用する結果\n[R1] (5.3).\n$' + PART + '$\n## 証明\n$' + FULL + '$\n'
    assert normalize_public_narrative_contract(raw) == raw


def test_connector_normalization_and_type_validation():
    raw = '完全性より, これより, $H$ は零写像.\n完全性より,\n\n完全性より,\n$E$ は全射.\n'
    normalized = normalize_public_narrative_contract(raw)
    assert '完全性より, これより,' not in normalized
    assert normalized.count('完全性より,') == 2
    with pytest.raises(TypeError):
        normalize_public_narrative_contract(None)

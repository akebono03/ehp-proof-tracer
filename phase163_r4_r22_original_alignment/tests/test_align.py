from pathlib import Path

import pytest

from phase163_r4_r22_original_alignment.align import (
    NEW_17,
    NEW_DX,
    OLD_17,
    OLD_DX,
    align,
    build_report,
)


def test_corrects_two_unique_spans():
    source = OLD_DX + '\n' + OLD_17
    revised = align(source)
    assert NEW_DX in revised
    assert NEW_17 in revised
    assert OLD_DX not in revised


def test_preserves_unrelated_text():
    source = 'OTHER CONTENT\n' + OLD_DX + '\n' + OLD_17 + '\nTRAILER'
    revised = align(source)
    assert revised.startswith('OTHER CONTENT\n')
    assert revised.endswith('\nTRAILER')


def test_rejects_missing_span():
    with pytest.raises(ValueError):
        align(OLD_DX)


def test_rejects_duplicate_span():
    with pytest.raises(ValueError):
        align(OLD_DX + OLD_DX + OLD_17)


def test_build_report_preserves_original(tmp_path: Path):
    source = tmp_path / 'source.tex'
    original = (r'S^{m+n}' + '\n' +
                r'\shrink_{m,n}:S^m\times S^n\longrightarrow S^{m+n}' + '\n' +
                OLD_DX + '\n' + OLD_17)
    source.write_text(original, encoding='utf-8')
    result = build_report(source, tmp_path / 'out')
    assert source.read_text(encoding='utf-8') == original
    assert result['confirmed_corrections'] == 2
    assert (tmp_path / 'out' / 'alignment_review.csv').is_file()
    assert NEW_17 in (tmp_path / 'out' / 'Toda_01_corrected.tex').read_text(encoding='utf-8')

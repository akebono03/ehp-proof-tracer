import pytest
from phase163_r4_r21_original_alignment.align import OLD_BLOCK, NEW_BLOCK, align, verify_source, run


def test_corrected_equation_is_map_not_isomorphism():
    result = align('前文\n' + OLD_BLOCK + '\n後文')
    assert NEW_BLOCK in result
    assert r'\shrink_{m,n}:S^m\times S^n\longrightarrow S^{m+n}' in result
    assert r'\psi_{m+n}(x,y)' in result
    assert r'S^{m+n+1}' not in result


def test_no_unintended_replacement():
    assert align('前文\n' + OLD_BLOCK + '\n後文').startswith('前文\n')
    with pytest.raises(ValueError):
        align('対象なし')


def test_duplicate_block_fails():
    with pytest.raises(ValueError):
        align(OLD_BLOCK + OLD_BLOCK)


def test_sha_guard(tmp_path):
    p=tmp_path/'source.tex'
    p.write_text('異なる TeX',encoding='utf-8')
    with pytest.raises(ValueError):
        verify_source(p)


def test_report_marks_not_exhaustive(tmp_path):
    src=tmp_path/'source.tex'
    src.write_bytes((tmp_path/'missing').read_bytes() if False else b'wrong')
    with pytest.raises(ValueError):
        run(src,tmp_path/'out')

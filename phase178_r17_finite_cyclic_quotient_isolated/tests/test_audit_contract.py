import pytest

from phase178_r17_finite_cyclic_quotient_isolated.audit import ANCHOR, INSERT, digest, reviewed_production


def test_exact_public_connection():
    base = 'before\n'+ANCHOR+'after\n'
    assert reviewed_production(base)=='before\n'+ANCHOR+INSERT+'after\n'


@pytest.mark.parametrize('base',['unrelated',ANCHOR+ANCHOR,ANCHOR+INSERT])
def test_wrong_base_fails_closed(base):
    with pytest.raises(RuntimeError,match='BASE_ANCHOR_CHANGED'):
        reviewed_production(base)


def test_normalization_only_line_endings_and_bom():
    assert digest(b'a\r\nb\r\n')==digest(b'a\nb\n')==digest(b'\xef\xbb\xbfa\nb\n')
    assert digest(b'a\nb\n')!=digest(b'a\n b\n')

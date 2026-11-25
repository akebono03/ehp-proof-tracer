"""Focused contracts, no repository mutation or full pytest execution."""
import pytest
from phase176_closeout_r1_test_scope_repair import repair


def test_inventory_exact():
    base={'tests/test_expression.py','tests/test_hopf_rules.py'}
    info=repair.verify_inventory(base,base|set(repair.PINS))
    assert info['introduced']==sorted(repair.PINS)
    for changed in (base,base|set(repair.PINS)|{'tests/test_new.py'},set(repair.PINS)):
        with pytest.raises(RuntimeError):
            repair.verify_inventory(base,changed)


def test_collection_only_strict():
    assert '--collect-only' in repair.COLLECT_COMMAND
    assert repair.COLLECT_COMMAND[-1]=='tests'
    assert repair.parse_collection('3546 tests collected in 5.00s\n',0)[0]==3546
    for output,code in [('3546 tests collected in 5.00s',2),('3545 tests collected in 5.00s',0),('3547 tests collected in 5.00s',0),('3546/3547 tests collected (1 deselected) in 5.00s',0),('1 error in 5.00s',2)]:
        with pytest.raises(RuntimeError):
            repair.parse_collection(output,code)


def test_blob_and_eol():
    for raw in (b'a\n',b'a\r\n'):
        assert repair.same_blob(raw,repair.blob(b'a\r\n'))
        assert not repair.same_blob(raw+b'b',repair.blob(b'a\r\n'))


def test_archive_preserves_exact_bytes(monkeypatch,tmp_path):
    monkeypatch.setattr(repair,'ROOT',tmp_path)
    raw={'tests/a.py':b'a\r\n','tests/tests/b.py':b''}
    monkeypatch.setattr(repair,'PINS',{n:repair.blob(v) for n,v in raw.items()})
    for n,v in raw.items():
        p=tmp_path/n
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(v)
    result=repair.archive_files()
    for n,v in raw.items():
        assert not (tmp_path/n).exists()
        assert repair.archive_path(n).read_bytes()==v
        assert result[n]['sha256']==repair.sha(v)
        assert repair.archive_path(n).suffix=='.txt'


def test_archive_conflict_never_unlinks_sources(monkeypatch,tmp_path):
    monkeypatch.setattr(repair,'ROOT',tmp_path)
    raw={'tests/a.py':b'a','tests/b.py':b'b'}
    monkeypatch.setattr(repair,'PINS',{n:repair.blob(v) for n,v in raw.items()})
    for n,v in raw.items():
        p=tmp_path/n
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(v)
    conflict=repair.archive_path('tests/b.py')
    conflict.parent.mkdir(parents=True,exist_ok=True)
    conflict.write_bytes(b'keep me')
    with pytest.raises(FileExistsError):
        repair.archive_files()
    assert conflict.read_bytes()==b'keep me'
    assert all((tmp_path/n).read_bytes()==v for n,v in raw.items())
    assert not repair.archive_path('tests/a.py').exists()

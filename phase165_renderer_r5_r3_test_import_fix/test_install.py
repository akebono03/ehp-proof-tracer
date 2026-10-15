from pathlib import Path
import ast
import pytest
from install import OLD, NEW, TARGET, BACKUP, install, restore

def test_exact_two_legacy_imports_are_replaced(tmp_path: Path) -> None:
    p = tmp_path / TARGET
    p.parent.mkdir(parents=True)
    p.write_text('def a():\n    ' + OLD + '\ndef b():\n    ' + OLD + '\n', encoding='utf-8')
    report = install(tmp_path)
    assert report['status'] == 'INSTALLED'
    assert p.read_text(encoding='utf-8').count(NEW) == 2
    assert not any(isinstance(n, ast.ImportFrom) and n.module == 'toda_group_proof_generic_narrative_renderer' for n in ast.walk(ast.parse(p.read_text(encoding='utf-8'))))
    assert restore(tmp_path)['status'] == 'RESTORED'
    assert p.read_text(encoding='utf-8').count(OLD) == 2

def test_refuse_any_different_import_shape(tmp_path: Path) -> None:
    p = tmp_path / TARGET
    p.parent.mkdir(parents=True)
    p.write_text('x = 1\n', encoding='utf-8')
    with pytest.raises(RuntimeError, match='Unexpected imports'):
        install(tmp_path)
    assert p.read_text(encoding='utf-8') == 'x = 1\n'
    assert not (tmp_path / BACKUP).exists()

def test_bom_is_preserved_and_reinstall_is_safe(tmp_path: Path) -> None:
    p = tmp_path / TARGET
    p.parent.mkdir(parents=True)
    data = ('def a():\n    ' + OLD + '\ndef b():\n    ' + OLD + '\n').encode('utf-8')
    p.write_bytes(b'\xef\xbb\xbf'+data)
    assert install(tmp_path)['status']=='INSTALLED'
    assert p.read_bytes().startswith(b'\xef\xbb\xbf')
    assert install(tmp_path)['status']=='ALREADY_INSTALLED'
    assert restore(tmp_path)['status']=='RESTORED'
    assert p.read_bytes()==b'\xef\xbb\xbf'+data

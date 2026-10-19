from pathlib import Path
from tempfile import TemporaryDirectory

from phase165_r6_8_3_runtime_retire.retire import ROOTS, plan


def test_production_dependency_protects_legacy_file():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        for name in ROOTS:
            (root / name).write_text('', encoding='utf-8')
        (root / 'web_app.py').write_text('import phase162_ehp_leaf_inputs\n', encoding='utf-8')
        (root / 'phase162_ehp_leaf_inputs.py').write_text('', encoding='utf-8')
        info = plan(root)
        assert 'phase162_ehp_leaf_inputs.py' in info['protected']
        assert 'phase162_ehp_leaf_inputs.py' not in info['retirable']


def test_archive_consumers_do_not_block_retirement():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        for name in ROOTS:
            (root / name).write_text('', encoding='utf-8')
        (root / 'phase162_ehp_leaf_inputs.py').write_text('', encoding='utf-8')
        archive = root / 'old_archive'
        archive.mkdir()
        (archive / 'audit.py').write_text('import phase162_ehp_leaf_inputs\n', encoding='utf-8')
        info = plan(root)
        assert info['safe_to_apply']
        assert 'phase162_ehp_leaf_inputs.py' in info['retirable']


def test_unknown_dynamic_import_fails_closed():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        for name in ROOTS:
            (root / name).write_text('', encoding='utf-8')
        (root / 'web_app.py').write_text('import importlib\nimportlib.import_module(module_name)\n', encoding='utf-8')
        info = plan(root)
        assert not info['safe_to_apply']

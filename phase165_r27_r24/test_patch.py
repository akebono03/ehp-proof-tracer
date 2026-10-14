import ast
from pathlib import Path
import pytest

from phase165_r27_r24.apply import transform


def _source():
    return (Path(__file__).resolve().parent.parent / 'toda_calculation_facade.py').read_text(encoding='utf-8')


def test_r24_standard_entry_rejects_legacy_bootstrap():
    import toda_calculation_facade as module
    with pytest.raises(RuntimeError, match='Legacy standard calculation is retired'):
        module.build_standard_toda_report(3, 1)


def test_r24_production_imports_removed():
    tree=ast.parse(_source())
    forbidden={'standard_production_repository','phase164_r7_repository_root_resolution'}
    assert not any(isinstance(n,ast.ImportFrom) and n.module in forbidden for n in tree.body)
    assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='build_standard_production_proof_repository' for n in ast.walk(tree))


def test_r24_repository_injected_entry_retained():
    import toda_calculation_facade as module
    assert callable(module.build_toda_report)
    import inspect
    assert list(inspect.signature(module.build_toda_report).parameters)==['repository','n','k']


def test_r24_installer_idempotent():
    source=_source()
    assert transform(source)==source

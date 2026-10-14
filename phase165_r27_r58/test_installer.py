import ast
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply import NEW_FUNCTION, transform, apply


BASE = '''from typing import TextIO
from proof_repository import ProofRepository
from toda_calculation_facade import build_toda_report
from toda_calculation_result import TodaCalculationStatus

def _write_markdown(stream, markdown):
    stream.write(markdown)

def _run_group_command(repository: ProofRepository, n: int, k: int, stdout: TextIO, stderr: TextIO) -> int:
    result = build_toda_report(repository, n=n, k=k)
    if result.status is TodaCalculationStatus.NOT_FOUND:
        return 0
    return 0

def other():
    return 7
'''


def test_convert():
    updated, changed = transform(BASE)
    assert changed
    ast.parse(updated)
    assert 'build_standard_toda_partial_result(n=n, k=k)' in updated
    assert 'build_toda_report(' not in updated


def test_unused_imports_removed():
    updated, _ = transform(BASE)
    assert 'from toda_calculation_facade' not in updated
    assert 'from toda_calculation_result' not in updated


def test_other_function_preserved():
    updated, _ = transform(BASE)
    assert 'def other():\n    return 7' in updated


def test_idempotent():
    updated, _ = transform(BASE)
    same, changed = transform(updated)
    assert not changed and same == updated


def test_unknown_route_blocked():
    with pytest.raises(RuntimeError, match='unknown existing'):
        transform(BASE.replace('build_toda_report(repository, n=n, k=k)', 'magic(repository)'))


def test_wrong_signature_blocked():
    with pytest.raises(RuntimeError, match='unknown signature'):
        transform(BASE.replace('n: int, k: int,', 'n: int, x: int,'))


def test_apply_and_repeat(tmp_path):
    (tmp_path/'cli.py').write_text(BASE, encoding='utf-8')
    (tmp_path/'toda_typed_group_facade.py').write_text('', encoding='utf-8')
    (tmp_path/'phase165_r52_partial_proof.py').write_text('', encoding='utf-8')
    assert apply(tmp_path)['status'] == 'CHANGED'
    assert apply(tmp_path)['status'] == 'ALREADY_INSTALLED'


def test_missing_required_file(tmp_path):
    with pytest.raises(RuntimeError, match='missing required'):
        apply(tmp_path)


def test_backup_conflict(tmp_path):
    (tmp_path/'cli.py').write_text(BASE, encoding='utf-8')
    (tmp_path/'toda_typed_group_facade.py').write_text('', encoding='utf-8')
    (tmp_path/'phase165_r52_partial_proof.py').write_text('', encoding='utf-8')
    (tmp_path/'phase165_r27_r58_backup').mkdir()
    (tmp_path/'phase165_r27_r58_backup'/'cli.py').write_text('not original', encoding='utf-8')
    with pytest.raises(RuntimeError, match='backup conflict'):
        apply(tmp_path)

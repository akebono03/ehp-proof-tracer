import ast
from pathlib import Path
from apply import NEW, patch, apply


def sample(old=True):
    body = '''def build_standard_web_group_proof_view(n, k, max_depth=2, mode="narrative"):
  result = build_standard_toda_report(n=n, k=k)
  return result
''' if old else NEW
    return '''from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_calculation_result import (\n  TodaCalculationStatus,\n)\n\n''' + body


def test_r33_replaces_old_entry_and_imports():
    after, changed = patch(sample())
    assert changed
    assert 'result = build_standard_toda_report' not in after
    assert 'from toda_calculation_facade' not in after
    assert 'from toda_calculation_result' not in after
    assert 'search_group_structure_automatically(n=n, k=k)' in after
    ast.parse(after)


def test_r33_idempotent():
    after, _ = patch(sample())
    again, changed = patch(after)
    assert not changed
    assert again == after


def test_r33_preserves_shared_legacy_import_if_used_elsewhere():
    src = sample() + '\ndef historical():\n  return build_standard_toda_report(n=2, k=1)\n'
    after, changed = patch(src)
    assert changed
    assert 'from toda_calculation_facade import' in after
    assert 'def historical()' in after


def test_r33_install_realistic_fixture(tmp_path):
    target = tmp_path / 'web_group_proof.py'
    target.write_text(sample())
    apply(tmp_path)
    assert 'search_group_structure_automatically' in target.read_text()
    apply(tmp_path)
    assert (tmp_path / 'phase165_r27_r33_web_group_proof_backup.py.bak').exists()

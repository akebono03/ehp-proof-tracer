"""R3-41P9 audit-only tests; no project files are changed."""
from __future__ import annotations

import ast
from pathlib import Path

from phase168_r3_41p9_trust_path_audit import audit


def test_baselines_exist_for_three_groups():
    for name, _, _ in audit.CASES:
        path = audit.BASELINES / (name + '.md')
        assert path.is_file()
        text = path.read_text(encoding='utf-8')
        assert '使用する結果' in text
        assert '証明' in text


def test_only_read_only_source_fingerprints():
    observed = audit.source_fingerprints()
    assert len(observed) == len(audit.SOURCE_FILES)
    assert all(len(sha) == 64 for sha in observed.values())


def test_counterfeit_result_does_not_certify_match_guard():
    status = audit.forged_result_model_acceptance()
    assert status['matcher_accepts'] is False
    assert status['partial_result_accepts'] is True
    assert status['narrative_model_accepts'] is True
    assert status['contains_explicit_verified_derivation_certificate'] is False


def test_audit_functions_not_application_patchers():
    module = ast.parse((audit.PACKAGE / 'audit.py').read_text(encoding='utf-8'))
    source = ast.unparse(module)
    for forbidden in ('write_bytes', 'replace(', 'unlink(', 'apply_patch'):
        assert forbidden not in source


def test_report_generation_is_total_on_error():
    path = audit.OUTPUT / 'audit.md'
    audit.OUTPUT.mkdir(parents=True, exist_ok=True)
    audit.write_report({'cases': {}, 'status': 'ERROR'})
    assert 'AUDIT_STATUS' in path.read_text(encoding='utf-8')

from __future__ import annotations

import json
from pathlib import Path

import pytest

from runtime_audit import collect, markdown


def _project(tmp_path: Path) -> Path:
    for name in ('phase165_r8_rule_provider.py', 'rule_catalog.py', 'phase165_r57_r26_generic_search_connection.py', 'phase165_r52_r9_shared_math.py'):
        (tmp_path / name).write_text('', encoding='utf-8')
    return tmp_path


def test_runtime_probe_process_error_is_not_success(tmp_path: Path) -> None:
    result = collect(_project(tmp_path), timeout=5)
    assert result['runtime']['status'] in ('PROBE_ERROR', 'PROCESS_ERROR')
    assert result['runtime']['count_comparison']['runtime_proof_verified'] == 0


def test_summary_does_not_claim_backward_proof(tmp_path: Path) -> None:
    result = collect(_project(tmp_path), timeout=5)
    counts = result['runtime']['count_comparison']
    assert counts['runtime_goal_verified'] == 0
    assert counts['runtime_proof_verified'] == 0


def test_static_candidate_count_is_reported(tmp_path: Path) -> None:
    (tmp_path / 'ehp_rules.py').write_text('def sample_inference_rule():\n    return InferenceRule(name="x")\n', encoding='utf-8')
    result = collect(_project(tmp_path), timeout=5)
    assert result['runtime']['count_comparison']['ast_eligible_factories'] == 1
    assert result['runtime']['ast_candidate_ids_by_module']['ehp_rules'] == ['ehp_rules.sample_inference_rule']


def test_markdown_contains_caveat(tmp_path: Path) -> None:
    result = collect(_project(tmp_path), timeout=5)
    rendered = markdown(result)
    assert '具体 Goal に対する逆向き適用実証' in rendered
    assert 'factory 名との直接対応は未確定' in rendered


def test_reports_json_serializable(tmp_path: Path) -> None:
    result = collect(_project(tmp_path), timeout=5)
    assert json.loads(json.dumps(result, ensure_ascii=False))['phase'] == '165 R6-2 R4-A-R2'

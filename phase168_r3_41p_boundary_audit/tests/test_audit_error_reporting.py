"""R3-41P1: failures remain visible and cannot block report generation."""
from __future__ import annotations

import json
from pathlib import Path

from phase168_r3_41p_boundary_audit import audit


def test_static_audit_finds_math_recheck_and_name_dependency(tmp_path, monkeypatch):
    monkeypatch.setattr(audit, "PROJECT", tmp_path)
    source = tmp_path / "mock_renderer.py"
    source.write_text(
        'def render(step):\n'
        '    specialize_typed_statement(step, step)\n'
        '    getattr(step.inference_rule, "name", None)\n'
        '    return step\n',
        encoding="utf-8",
    )
    result = audit.scan_file(source)
    names = {finding["identifier"] for finding in result["findings"]}
    assert "specialize_typed_statement" in names
    assert "getattr(inference_rule, 'name')" in names


def test_report_records_group_failure_and_preserves_successful_group():
    report = {
        "sources": {"git": {"branch": "develop", "head": "a", "status": ""}, "static": []},
        "runtime": {
            "pi3_2": {"audit_error": "Traceback: simulated failure"},
            "pi4_3": {
                "proof_steps": 25,
                "references": 4,
                "no_unused_reference": True,
                "bidirectional_provenance_consistent": True,
                "benchmark_all_present": True,
                "proof_diff_lines": 29,
                "reference_diff_lines": 0,
            },
        },
        "error": "Group audit failures: pi3_2",
    }
    rendered = audit.render_report(report)
    assert "pi3_2 | — | — | ERROR" in rendered
    assert "pi4_3 | 25 | 4 | PASS | PASS" in rendered
    assert "Traceback: simulated failure" in rendered


def test_main_writes_full_report_on_audit_failure(tmp_path, monkeypatch, capsys):
    project = tmp_path / "ehp_root"
    project.mkdir()
    (project / audit.SOURCE_FILES[0]).write_text("# mock\n", encoding="utf-8")
    output = tmp_path / "reports"
    output.mkdir()
    monkeypatch.setattr(audit, "PROJECT", project)
    monkeypatch.setattr(audit, "OUT", output)
    monkeypatch.setattr(audit, "source_trace", lambda: {
        "git": {"branch": "develop", "head": "a", "status": ""},
        "static": [],
        "missing": [],
    })
    monkeypatch.setattr(audit, "runtime_audit", lambda: {
        "pi3_2": {"audit_error": "failed deliberately"},
    })
    exit_code = audit.main()
    assert exit_code == 1
    report = json.loads((output / "audit.json").read_text(encoding="utf-8"))
    assert report["error"] == "Group audit failures: pi3_2"
    assert "failed deliberately" in (output / "audit.md").read_text(encoding="utf-8")
    assert "AUDIT_ERROR" in capsys.readouterr().out

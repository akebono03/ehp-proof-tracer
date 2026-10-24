"""Self-contained unit tests for the Phase 168 R3-41P4 audit package."""
from __future__ import annotations

import hashlib
from types import SimpleNamespace

from phase168_r3_41p4_residual_boundary_audit import audit


def test_digest_is_standard_sha256():
    assert audit.sha256_bytes(b"R3-41P4") == hashlib.sha256(b"R3-41P4").hexdigest()


def test_index_of_step_rejects_ambiguous_value_match():
    first = SimpleNamespace(x=1)
    second = SimpleNamespace(x=1)
    distinct = SimpleNamespace(x=2)
    model = SimpleNamespace(steps=(first, second, distinct))
    assert audit.index_of_step(model, first) == 0
    assert audit.index_of_step(model, distinct) == 2
    assert audit.index_of_step(model, SimpleNamespace(x=1)) is None


def test_static_audit_classifies_rule_name_and_math_checks(tmp_path, monkeypatch):
    module = tmp_path / "renderer.py"
    module.write_text(
        "def check(proof):\n"
        "    return getattr(proof.inference_rule, 'name', '')\n"
        "def validate(x):\n"
        "    return prop42_exactness_indices(x)\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(audit, "PROJECT", tmp_path)
    monkeypatch.setattr(audit, "FILES", ("renderer.py",))
    rows = audit.scan_static()
    assert not rows["missing"]
    names = {f["name"] for f in rows["files"][0]["findings"]}
    assert names == {"inference_rule.name", "prop42_exactness_indices"}


def test_markdown_report_handles_no_runtime(tmp_path, monkeypatch):
    monkeypatch.setattr(audit, "OUT", tmp_path)
    payload = {"git": {"branch": "develop", "head": "a123"},
               "static": {"files": []}, "runtime": {}}
    audit.write_report(payload)
    text = (tmp_path / "audit.md").read_text(encoding="utf-8")
    assert "R3-41P4" in text
    assert "Phase 168" in text
    assert "全体 pytest" in text

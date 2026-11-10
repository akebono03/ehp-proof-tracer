"""Focused R56R1 audit Path regression without fabricated mathematical proofs."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

import pytest

from phase174_r3_r7_r56r1_audit_path_fix.install import (
    BASELINE_SHA256,
    PATCHED_SHA256,
    OLD_LINE,
    NEW_LINE,
    _read_lf,
    _sha,
    patch_source,
)


PACKAGE = Path(__file__).resolve().parents[1]
BASELINE_FILE = PACKAGE / "audit_FULL_AFTER.py"


def test_exact_r56_original_zip_hash_and_one_line_patch() -> None:
    corrected = BASELINE_FILE.read_text(encoding="utf-8")
    original = corrected.replace(NEW_LINE, OLD_LINE)
    assert corrected.count(NEW_LINE) == 1
    assert _sha(original) == BASELINE_SHA256
    assert _sha(corrected) == PATCHED_SHA256
    assert patch_source(original) == corrected
    ast.parse(corrected)


def test_fails_closed_for_missing_or_tampered_original() -> None:
    corrected = BASELINE_FILE.read_text(encoding="utf-8")
    original = corrected.replace(NEW_LINE, OLD_LINE)
    with pytest.raises(RuntimeError):
        patch_source(corrected)
    with pytest.raises(RuntimeError):
        patch_source(original.replace(OLD_LINE, "    destination = 'tampered'"))
    with pytest.raises(RuntimeError):
        patch_source(original.replace("import argparse", "import random"))


def test_uniform_crlf_is_accepted_without_normalizing_git_blob_hash() -> None:
    corrected = BASELINE_FILE.read_text(encoding="utf-8")
    crlf = corrected.replace("\n", "\r\n").encode("utf-8")
    normalized, eol = _read_lf(crlf)
    assert eol == "\r\n"
    assert normalized == corrected
    assert hashlib.sha256(crlf).hexdigest() != PATCHED_SHA256
    with pytest.raises(RuntimeError):
        _read_lf(b"first\r\nsecond\n")


@pytest.mark.parametrize("dry_run", (False, True))
def test_actual_audit_main_writes_report_after_completed_inspection(
    dry_run: bool, monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    source = BASELINE_FILE.read_text(encoding="utf-8")
    tree = ast.parse(source)
    nodes = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "main"]
    assert len(nodes) == 1
    isolated = ast.Module(body=nodes, type_ignores=[])
    inspection_calls = []

    def fake_review() -> dict[str, object]:
        return {"local_head": "test-only-head", "source_guard": "PASS"}

    def fake_inspect() -> dict[str, object]:
        inspection_calls.append(True)
        return {"gate": "PASS_R56_TWO_GENERAL_RULES_SOURCE_FIRST_PUBLIC",
                "pi11_6_complete": True, "pi12_7_complete": True}

    scope = {
        "argparse": argparse,
        "json": json,
        "os": os,
        "Path": Path,
        "tempfile": tempfile,
        "review": fake_review,
        "inspect_public": fake_inspect,
    }
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(sys, "argv", ["audit"] + (["--dry-run"] if dry_run else []))
    exec(compile(isolated, str(BASELINE_FILE), "exec"), scope)
    assert scope["main"]() == 0
    report = (tmp_path / "EHPProofTracerAudit" / "phase174_r3_r7_r56"
              / ("preflight.json" if dry_run else "public_proofs.json"))
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["source_guard"] == "PASS"
    assert data["inspection"] is None if dry_run else data["inspection"]["pi11_6_complete"]
    assert len(inspection_calls) == (0 if dry_run else 1)

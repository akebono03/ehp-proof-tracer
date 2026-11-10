"""Tests executable without the EHP production repository."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

from phase174_r3_r7_r55r3r2_narrative_removal.install import (
    PACKAGE, REFERENCE_OLD, REFERENCE_LEGACY, REFERENCE_SHARED,
    RENDERER_OLD, RENDERER_LEGACY, TYPED_OLD, TYPED_SHARED,
    _once,
)


def test_patch_anchors_are_unique_and_source_first() -> None:
    assert 'project_cited_general_reference_body' in REFERENCE_LEGACY
    assert 'phase174_r3_r7_r55r3_common_proof_display' not in REFERENCE_SHARED
    assert _once(REFERENCE_OLD, REFERENCE_OLD, REFERENCE_SHARED, 'reference') == REFERENCE_SHARED
    assert 'project_certified_proof_sentence' in RENDERER_LEGACY
    assert 'project_certified_proof_sentence' not in RENDERER_OLD


def test_shared_typed_block_is_syntactically_valid() -> None:
    mock = 'def typed_sentence(statement, step):\n' + TYPED_SHARED
    mock += '    return None\n'
    ast.parse(mock)
    assert 'step.premises' not in TYPED_SHARED
    assert 'n==6' not in TYPED_SHARED
    assert r'\mathrm{upper}' not in TYPED_SHARED
    assert r'\mathrm{lower}' not in TYPED_SHARED


def test_reference_formatter_cannot_infer_proof_steps() -> None:
    source = (PACKAGE / 'reference_body_helper.txt').read_text(encoding='utf-8')
    ast.parse(source)
    assert 'ProofStep(' not in source
    assert 'InferenceRule(' not in source
    assert 'project_certified_proof_sentence' not in source
    assert '_typed_upper_delta_transition' not in source


def test_old_modules_deletion_is_whitelisted_by_zip_hash() -> None:
    data = json.loads((PACKAGE / 'legacy_manifest.json').read_text(encoding='utf-8'))
    assert set(data['packages']) == {
        'phase174_r3_r7_r55r3_common_proof_display',
        'phase174_r3_r7_r55r3r1_public_sentence_correction',
    }
    for files in data['packages'].values():
        assert 'install.py' in files
        assert 'run.ps1' in files
        assert all(len(value) == 1 and len(value[0]) == 64 for value in files.values())

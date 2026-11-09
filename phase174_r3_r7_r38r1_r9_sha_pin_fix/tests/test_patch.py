"""R38R1 one-character pin repair — isolated tests without repository mutation."""
from __future__ import annotations

import ast
import hashlib
import importlib.util
from pathlib import Path

import pytest

from phase174_r3_r7_r38r1_r9_sha_pin_fix import install


def _module_for_replacement():
    spec = importlib.util.spec_from_file_location('r38r1_reviewed_module', install.REPLACEMENT)
    assert spec is not None and spec.loader is not None
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def test_only_one_pin_character_changes_and_imports_functions_stay_identical():
    old = install.BASELINE.read_text(encoding='utf8')
    new = install.REPLACEMENT.read_text(encoding='utf8')
    assert new == old.replace(install.OLD_R9_BLOB, install.CORRECT_R9_BLOB)
    before = ast.parse(old)
    after = ast.parse(new)
    old_functions = {x.name: ast.get_source_segment(old, x) for x in before.body
                     if isinstance(x, ast.FunctionDef)}
    new_functions = {x.name: ast.get_source_segment(new, x) for x in after.body
                     if isinstance(x, ast.FunctionDef)}
    assert old_functions == new_functions
    old_imports = [ast.dump(x) for x in before.body
                   if isinstance(x, (ast.Import, ast.ImportFrom))]
    new_imports = [ast.dump(x) for x in after.body
                   if isinstance(x, (ast.Import, ast.ImportFrom))]
    assert old_imports == new_imports


def test_all_reviewed_r38_blob_pins_are_exactly_40_hex_digits():
    module = _module_for_replacement()
    assert module.PINNED['phase174_r3_r7_r9_composition_associativity/rule.py'] == install.CORRECT_R9_BLOB
    assert all(len(v) == 40 and all(c in '0123456789abcdef' for c in v)
               for v in module.PINNED.values())


def test_original_r38_malformed_pin_is_39_and_corrected_pin_is_40():
    assert len(install.OLD_R9_BLOB) == 39
    assert len(install.CORRECT_R9_BLOB) == 40
    assert install.CORRECT_R9_BLOB == install.OLD_R9_BLOB + 'e'


def test_existing_blob_guard_remains_strict_for_bad_pins_and_accepts_clean_data():
    module = _module_for_replacement()
    data = b'R38R1 reviewed clean source'
    sha = module.git_blob(data)
    assert module.matches_blob(data, sha)
    assert module.matches_blob(data.replace(b'\n',b'\r\n'),sha)
    assert not module.matches_blob(data, sha[:-1])
    assert not module.matches_blob(data + b'x', sha)


def test_pinned_installer_contents_are_exactly_reviewed():
    assert install.sha256_of(install.BASELINE.read_bytes()) == install.OLD_SHA256
    assert install.sha256_of(install.REPLACEMENT.read_bytes()) == install.NEW_SHA256
    assert install.NEW_SHA256 != install.OLD_SHA256
    assert (install.PACKAGE / 'CHANGED_TOP_LEVEL_FULL.py').read_text(encoding='utf8').startswith('PINNED = {')

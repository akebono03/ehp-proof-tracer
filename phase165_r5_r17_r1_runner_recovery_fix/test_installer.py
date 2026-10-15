from __future__ import annotations

import ast
from pathlib import Path

from install import GUARD_MODULES, MODULES, TESTS, imports_retired_module


def test_deletion_manifest_is_explicit():
    assert len(MODULES) == 4
    assert len(TESTS) == 5
    assert len(set(MODULES + TESTS)) == 9
    assert GUARD_MODULES == {Path(path).stem for path in MODULES}


def test_ast_detects_normal_imports():
    assert imports_retired_module('import phase162_r3_narrative_connection') == {'phase162_r3_narrative_connection'}
    assert imports_retired_module('from toda_group_proof_narrative_concrete_transport import render_concrete_transport_proof_from_steps') == {'toda_group_proof_narrative_concrete_transport'}


def test_ast_ignores_ordinary_strings_and_comments():
    assert imports_retired_module('s = "import phase162_web_narrative_integration"\n# import phase162_r3_narrative_connection') == set()


def test_ast_ignores_shared_renderer():
    assert imports_retired_module('from phase165_r52_partial_proof import render_partial_proof_markdown') == set()


def test_source_is_valid_python():
    source = Path(__file__).with_name('install.py').read_text(encoding='utf-8')
    ast.parse(source)

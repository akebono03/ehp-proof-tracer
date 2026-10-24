"""Guard the new early uses of Relation against delayed imports."""
from __future__ import annotations

import ast
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]


def test_relation_is_bound_before_suppression_scan():
    function = ast.parse((PACKAGE / "renderer_function_full.py").read_text(encoding="utf-8")).body[0]
    assert isinstance(function, ast.FunctionDef)
    imports = [node for node in function.body if isinstance(node, ast.ImportFrom)]
    positions = [(position, node) for position, node in enumerate(function.body)
                 if isinstance(node, ast.ImportFrom) and node.module == "proof"
                 and any(alias.name == "Relation" for alias in node.names)]
    assert len(positions) == 1
    index, statement = positions[0]
    assert index <= 2
    assert {item.name for item in statement.names} == {"ProofRule", "Relation"}
    assert all(not (isinstance(item, ast.ImportFrom) and item.module == "proof"
                    and any(alias.name == "Relation" for alias in item.names))
               for item in function.body[index + 1:])


def test_repaired_function_changes_only_import_position():
    function = (PACKAGE / "renderer_function_full.py").read_text(encoding="utf-8")
    before = function.replace("    from proof import ProofRule, Relation\n",
                              "    from proof import ProofRule\n", 1)
    anchor = "    from homotopy_groups import TodaPrimaryGroup\n"
    assert before.count(anchor) == 1
    before = before.replace(anchor, "    from proof import Relation\n" + anchor, 1)
    expected = (PACKAGE / "renderer_function_before_fix.py").read_text(encoding="utf-8")
    assert before == expected


def test_incomplete_branch_and_unchanged_module_imports():
    function = (PACKAGE / "renderer_function_full.py").read_text(encoding="utf-8")
    original = (PACKAGE / "renderer_before.py").read_text(encoding="utf-8")
    full = (PACKAGE / "renderer_full_file.py").read_text(encoding="utf-8")
    assert '"## 未解決 Goal"' in function
    assert 'if incomplete:' in function
    assert original.split("def render_model_backed_narrative_markdown", 1)[0] == full.split(
        "def render_model_backed_narrative_markdown", 1)[0]
    assert function in full

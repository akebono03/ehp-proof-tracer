"""Adjust the Phase 164 web test to the Phase 165 fail-closed contract."""
import ast
from pathlib import Path

root = Path(__file__).resolve().parent.parent
target = root / "tests" / "test_phase164_r5_r2_unified_web_display.py"
source = target.read_text(encoding="utf-8-sig")
tree = ast.parse(source)

import_line = "from phase165_goal_only_search import GoalSearchIncompleteError"
if import_line not in source:
    anchor = "import phase164_r5_r2_common_replay as selector"
    if source.count(anchor) != 1:
        raise RuntimeError("Unexpected test imports; no change applied")
    source = source.replace(anchor, import_line + "\n" + anchor, 1)

tree = ast.parse(source)
matches = [
    node for node in tree.body
    if isinstance(node, ast.FunctionDef)
    and node.name == "test_pi53_common_narrative_is_renderable"
]
new_function = """def test_pi53_common_narrative_requires_registered_goal_catalog():
    with pytest.raises(
        GoalSearchIncompleteError,
        match="Registered goal/rule catalog not configured",
    ):
        web.build_standard_web_group_proof_view(3, 2, 2, "narrative")
"""
if len(matches) == 1:
    node = matches[0]
    lines = source.splitlines(keepends=True)
    start = node.lineno - 1
    end = node.end_lineno
    source = "".join(lines[:start]) + new_function + "".join(lines[end:])
elif "def test_pi53_common_narrative_requires_registered_goal_catalog():" in source:
    print("Test contract already updated.")
else:
    raise RuntimeError("Expected test function not found; no change applied")
ast.parse(source)
target.write_text(source, encoding="utf-8")
print("Updated Phase 164 R5-R2 test contract for Phase 165 fail-closed.")

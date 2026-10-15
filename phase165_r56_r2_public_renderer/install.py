"""Fail-closed, idempotent installer: replace only the R56 presentation adapter."""
from __future__ import annotations

import ast
import shutil
from pathlib import Path

package = Path(__file__).resolve().parent
root = package.parent
target = root / "phase165_r56_presentation_adapter.py"
source = package / target.name
if not target.is_file():
    raise SystemExit("R56 presentation adapter is not installed")
old = target.read_text(encoding="utf-8")
new = source.read_text(encoding="utf-8")
tree = ast.parse(old)
ast.parse(new)
if len([x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == "render_completed_shared_narrative"]) != 1:
    raise SystemExit("Unexpected R56 adapter: no unique target function")
if "render_toda_group_proof_generic_proof_markdown" not in old and old != new:
    raise SystemExit("Unexpected R56 adapter version: refusing modification")
for path, pattern in (
    (root / "phase165_r52_partial_proof.py", "render_completed_shared_narrative"),
    (root / "toda_group_proof_narrative_renderer.py", "def render_toda_group_proof_narrative_markdown("),
    (root / "test_phase165_r56_common_renderer.py", "test_r56_pi32_completed_common_presentation"),
    (root / "phase165_r55_nk_only_goal.py", "search_group_from_registered_goal"),
):
    if not path.is_file() or pattern not in path.read_text(encoding="utf-8"):
        raise SystemExit(f"Required R55/R56 baseline missing: {path}")
if old != new:
    backup = root / "phase165_r56_presentation_adapter.py.phase165_r56_r2_backup"
    if not backup.exists():
        shutil.copy2(target, backup)
    target.write_text(new, encoding="utf-8")
    print("R56-R2: restored existing public narrative renderer entry point")
else:
    print("R56-R2: public narrative entry point already installed")
print("Only phase165_r56_presentation_adapter.py changed; no renderer rules modified")

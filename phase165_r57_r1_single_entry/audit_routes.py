"""Read-only inventory of public/legacy proof renderer call sites."""
from __future__ import annotations
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEYS = (
    "render_toda_group_proof_narrative_markdown",
    "render_toda_group_proof_generic_proof_markdown",
    "render_toda_partial_proof_narrative_markdown",
    "build_phase165_pi32_web_view",
    "search_group_structure_automatically",
)
# Only immediate production *.py at repository root. Phase folders and archived tests
# are reported separately by the repository; do not infer deletion safety from this alone.

def collect():
    found = {key: [] for key in KEYS}
    for path in sorted(ROOT.glob("*.py")):
        if path.name.endswith(".bak") or path.name.startswith("test_") or path.name.startswith("audit_"):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (UnicodeError, SyntaxError):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            target = node.func
            name = target.id if isinstance(target, ast.Name) else target.attr if isinstance(target, ast.Attribute) else None
            if name in found:
                found[name].append(f"{path.name}:{node.lineno}")
    return {"scope":"production root Python AST calls; not a full dynamic dependency analysis", "call_sites":found,"automatic_deletion":False}


if __name__ == "__main__":
    result = collect()
    path = ROOT / "phase165_r57_r1_renderer_inventory.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))

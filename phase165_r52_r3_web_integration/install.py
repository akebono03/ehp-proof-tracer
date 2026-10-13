"""Install R52-R3 without replacing legacy production renderers."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

ROOT = Path.cwd()
BUNDLE = Path(__file__).resolve().parent
SOURCE = ROOT / "web_group_proof.py"
ADAPTER = ROOT / "phase165_r52_r3_web_adapter.py"
MARKER = "# Phase 165 R52-R3 explicit partial-result Web entry"
APPEND = '''\n\n# Phase 165 R52-R3 explicit partial-result Web entry\ndef build_web_partial_group_proof_view(\n    result, *, max_depth: int = 2, mode: str = "narrative",\n) -> WebGroupProofView:\n    """Render typed partial evidence through the shared WebGroupProofView."""\n    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view\n\n    return build_partial_web_group_proof_view(\n        result, max_depth=max_depth, mode=mode,\n    )\n'''


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError("Run from the repository root: web_group_proof.py missing")
    if not (ROOT / "phase165_r52_partial_proof.py").is_file():
        raise FileNotFoundError("R52 model must be installed first")
    if not (ROOT / "phase165_r52_r2_search_adapter.py").is_file():
        raise FileNotFoundError("R52-R2 search adapter must be installed first")
    current = SOURCE.read_text(encoding="utf-8-sig")
    tree = ast.parse(current)
    required = {"WebGroupProofView", "WebGroupProofStepView", "_build_group_proof_rendered_lines", "_group_proof_statement_latex", "_group_proof_rule_name"}
    observed = {node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    if not required <= observed:
        raise RuntimeError("Current Web renderer contract changed; no files modified")
    if MARKER not in current and "def build_web_partial_group_proof_view(" in current:
        raise RuntimeError("A non-R52 partial Web entry already exists")
    payload = (BUNDLE / "phase165_r52_r3_web_adapter.py").read_text(encoding="utf-8")
    ast.parse(payload)
    if MARKER not in current:
        updated = current.rstrip("\n") + APPEND
        ast.parse(updated)
        shutil.copy2(SOURCE, SOURCE.with_name("web_group_proof.phase165_r52_r3_backup.py"))
        SOURCE.write_text(updated, encoding="utf-8")
        print("Added explicit partial Web entry to common web_group_proof.py")
    else:
        print("R52-R3 common Web entry already installed")
    ADAPTER.write_text(payload, encoding="utf-8")
    print("Installed phase165_r52_r3_web_adapter.py")


if __name__ == "__main__":
    main()

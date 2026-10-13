"""Remove only R43's redundant post-renderer hook; preserve R42 proof and renderer."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def remove_r43_hook(source: str) -> str:
    tree = ast.parse(source)
    candidates = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "render_toda_group_proof_narrative_markdown"
    ]
    if not candidates:
        raise RuntimeError("Common renderer definition is missing")
    node = candidates[-1]
    lines = source.splitlines(keepends=True)
    body = "".join(lines[node.lineno - 1:node.end_lineno])
    if "phase165_r43_shared_narrative_enrichment" not in body:
        return source
    old = """  # phase165_r43_shared_narrative_enrichment
  from phase165_r14_r43_reference_reason import enrich_common_narrative
  return enrich_common_narrative(presentation, rendered)
"""
    new = """  return rendered
"""
    if body.count(old) != 1:
        raise RuntimeError("Unexpected R43 hook layout; no files changed")
    updated = "".join(lines[:node.lineno - 1]) + body.replace(old, new, 1) + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    return updated


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    renderer = root / "toda_group_proof_narrative_renderer.py"
    original = renderer.read_text(encoding="utf-8")
    updated = remove_r43_hook(original)
    if original != updated:
        backup = root / "toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py"
        if not backup.exists():
            shutil.copy2(renderer, backup)
        renderer.write_text(updated, encoding="utf-8")
        print("Removed R43 post-renderer hook; backup:", backup.name)
    else:
        print("R43 post-renderer hook already absent")
    addon = root / "phase165_r14_r43_reference_reason.py"
    if addon.exists():
        remaining = renderer.read_text(encoding="utf-8")
        if "phase165_r14_r43_reference_reason" in remaining:
            raise RuntimeError("R43 module still referenced; manual inspection required")
        # R43 generated files are kept as rollback material under a known backup
        # name instead of deleting unknown user changes.
        backup = root / "phase165_r14_r43_reference_reason.phase165_r44_removed.py"
        if backup.exists():
            if addon.read_bytes() != backup.read_bytes():
                raise RuntimeError("Existing R43 backup differs; refusing to overwrite")
            addon.unlink()
        else:
            addon.rename(backup)
        print("Retired unused R43 add-on:",backup.name)
    assert "phase165_r43_shared_narrative_enrichment" not in renderer.read_text(encoding="utf-8")
    print("R42 typed ProofStep and generic formatter not changed")


if __name__ == "__main__":
    main()

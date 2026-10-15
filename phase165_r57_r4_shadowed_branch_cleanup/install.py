"""R57-R4: remove shadowed public renderer and unreferenced dedicated helper only."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

TARGET_NAME = "toda_group_proof_narrative_renderer.py"
PUBLIC_NAME = "render_toda_group_proof_narrative_markdown"
SHADOWED_HELPER = "_phase159_render_pi_n_plus_1_n_stable_transport_narrative"


def _module_defs(source: str) -> list[ast.FunctionDef]:
    module = ast.parse(source)
    return [node for node in module.body if isinstance(node, ast.FunctionDef)]


def _find_shadowed_public_definition(source: str) -> ast.FunctionDef | None:
    definitions = [node for node in _module_defs(source) if node.name == PUBLIC_NAME]
    if len(definitions) <= 1:
        return None
    return definitions[0]


def _root_python_reference_files(root: Path, name: str, target: Path) -> tuple[str, ...]:
    # Conservative: only count references outside this file; never delete a helper
    # if some live root-level module even mentions its name.
    return tuple(sorted(path.name for path in root.glob("*.py")
                        if path != target and name in path.read_text(encoding="utf-8-sig")))


def _remove_ranges(source: str, ranges: tuple[tuple[int, int], ...]) -> str:
    lines = source.splitlines(keepends=True)
    for start, end in sorted(ranges, reverse=True):
        del lines[start - 1:end]
    return "".join(lines)


def clean_shadowed_public_renderer(source: str, *, external_helper_references: tuple[str, ...] = ()) -> tuple[str, tuple[str, ...]]:
    """Drop only a dead top-level public definition and a provably unused helper.

    Do not touch the latest binding, an earlier version captured in an alias,
    or a helper with any external consumer. No rendering logic is rewritten.
    """
    definitions = _module_defs(source)
    public = [node for node in definitions if node.name == PUBLIC_NAME]
    if len(public) < 2:
        return source, ()
    first = public[0]
    # A public definition captured before the next redefinition is not dead.
    statements = ast.parse(source).body
    next_public_line = public[1].lineno
    captures = [node for node in statements if first.end_lineno < node.lineno < next_public_line
                and isinstance(node, (ast.Assign, ast.AnnAssign))
                and any(isinstance(child, ast.Name) and child.id == PUBLIC_NAME
                        for child in ast.walk(node))]
    if captures:
        if len(public) == 2:
            return source, ()
        raise RuntimeError("first renderer definition is captured before redefinition; no removal")

    removal = [(first.lineno, first.end_lineno)]
    removed = [f"{PUBLIC_NAME} lines {first.lineno}-{first.end_lineno}"]
    helper = next((node for node in definitions if node.name == SHADOWED_HELPER), None)
    if helper is not None and not external_helper_references:
        tree = ast.parse(source)
        refs = [node for node in ast.walk(tree) if isinstance(node, ast.Name)
                and node.id == SHADOWED_HELPER and isinstance(node.ctx, ast.Load)]
        # Only the removed first definition may reference the helper.
        if refs and all(first.lineno <= ref.lineno <= first.end_lineno for ref in refs):
            removal.append((helper.lineno, helper.end_lineno))
            removed.append(f"{SHADOWED_HELPER} lines {helper.lineno}-{helper.end_lineno}")

    changed = _remove_ranges(source, tuple(removal))
    ast.parse(changed)
    assert len([node for node in _module_defs(changed) if node.name == PUBLIC_NAME]) == len(public) - 1
    return changed, tuple(removed)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    target = root / TARGET_NAME
    if not target.is_file():
        raise FileNotFoundError(target)
    raw = target.read_bytes()
    source = raw.decode("utf-8-sig")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    reference_files = _root_python_reference_files(root, SHADOWED_HELPER, target)
    changed, removed = clean_shadowed_public_renderer(
        source, external_helper_references=reference_files,
    )
    if not removed:
        print("R57-R4 already installed or no shadowed public definition found")
        return 0
    # Fail-closed for an unanticipated layout: the removed definition must be
    # preceded by the phase159 transport helper and the final public definition
    # must still be present.
    if len([node for node in _module_defs(source) if node.name == PUBLIC_NAME]) < 3:
        raise RuntimeError("expected at least three historical public definitions; refusing patch")
    assert "def render_toda_group_proof_narrative_markdown(" in changed
    backup = target.with_name(target.name + ".phase165_r57_r4_backup")
    if not backup.exists():
        shutil.copy2(target, backup)
    bytes_out = changed.replace("\r\n", "\n").replace("\n", newline).encode("utf-8")
    target.write_bytes(bytes_out)
    print("R57-R4 removed only unreachable public renderer definition(s):")
    for name in removed:
        print(" - " + name)
    if reference_files:
        print("Dedicated helper retained because root references exist: " + ", ".join(reference_files))
    print("Current public renderer and its stable transport branch unchanged")
    print("Full pytest NOT run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

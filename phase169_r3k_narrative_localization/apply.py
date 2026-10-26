"""Guarded installer for a single full-function Renderer replacement."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "phase168_r3_5_model_renderer.py"
HELPER = ROOT / "phase169_r3k_narrative_projection.py"
HELPER_SOURCE = HERE / "phase169_r3k_narrative_projection.py"
OUTPUT = HERE / "output"
EXPECTED_BLOB = "66509896c60d431427e3c18e70a911d7bebe8d7c"
ANCHOR = '            if isinstance(step.conclusion, TodaProp42ExactnessStatement):\n                statement_latex = statement_latex.replace(r" \\text{ is exact}", "")\n                lines.append(f"{prefix}${statement_latex}$ は完全.")\n            else:\n                lines.append(f"{prefix}${statement_latex}$.")\n            lines.append("")'
ANCHOR_TWO = '    for index in order:\n        if index in suppressed_body_indices:\n            continue\n        step = model.steps[index]\n        statement = step.conclusion\n        if incomplete:'
REPLACEMENT = '            if isinstance(step.conclusion, TodaProp42ExactnessStatement):\n                statement_latex = statement_latex.replace(r" \\text{ is exact}", "")\n                lines.append(f"{prefix}${statement_latex}$ は完全.")\n            else:\n                from phase169_r3k_narrative_projection import project_proven_map_property\n                projected = project_proven_map_property(step, statement_latex)\n                lines.append(f"{prefix}{projected}" if projected is not None\n                             else f"{prefix}${statement_latex}$.")\n            lines.append("")'
REPLACEMENT_TWO = '    displayed_cyclic_math = set()\n    for index in order:\n        if index in suppressed_body_indices:\n            continue\n        step = model.steps[index]\n        statement = step.conclusion\n        if not incomplete:\n            from phase169_r3k_narrative_projection import duplicate_group_relation_notice\n            notice = duplicate_group_relation_notice(model, index, displayed_cyclic_math)\n            if notice is not None:\n                if notice:\n                    lines.extend((notice, ""))\n                continue\n            from homotopy_groups import FiniteCyclicGroup\n            if (isinstance(statement, Relation)\n                    and statement.relation_type is RelationType.EQUALITY\n                    and isinstance(statement.lhs, TodaPrimaryGroup)\n                    and isinstance(statement.rhs, FiniteCyclicGroup)):\n                latex, problem = _group_proof_statement_latex(statement)\n                if latex is not None and problem is None:\n                    displayed_cyclic_math.add(latex)\n        if incomplete:'


def git_blob(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def patch_function(source: str) -> tuple[str, str]:
    if source.count(ANCHOR) != 1:
        raise ValueError("Renderer's certified body-line branch changed")
    if 'from phase169_r3k_narrative_projection import' in source:
        raise ValueError("Renderer is already patched or has an unreviewed implementation")
    if source.count(ANCHOR_TWO) != 1:
        raise ValueError("Renderer display-loop anchor changed")
    revised = source.replace(ANCHOR, REPLACEMENT, 1).replace(ANCHOR_TWO, REPLACEMENT_TWO, 1)
    ast.parse(revised)
    tree = ast.parse(revised)
    function = next((item for item in tree.body if isinstance(item, ast.FunctionDef)
                     and item.name == "render_model_backed_narrative_markdown"), None)
    if function is None or function.end_lineno is None:
        raise ValueError("whole renderer function not found")
    lines = revised.splitlines(keepends=True)
    complete_function = "".join(lines[function.lineno - 1:function.end_lineno])
    if complete_function.count("project_proven_map_property") != 2 or complete_function.count("duplicate_group_relation_notice") != 2:
        raise ValueError("whole replacement function has unexpected projection count")
    return revised, complete_function


def install() -> None:
    OUT = OUTPUT
    OUT.mkdir(exist_ok=True)
    git_head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    print("Git HEAD:", git_head, flush=True)
    original = TARGET.read_bytes()
    source = original.decode("utf-8-sig")
    # CRLF/LF are treated equivalently only for source text, not the Git blob.
    source = source.replace("\r\n", "\n")
    checked = subprocess.run(["git", "show", "HEAD:phase168_r3_5_model_renderer.py"],
                             cwd=ROOT, capture_output=True, check=True).stdout.decode("utf-8-sig")
    checked = checked.replace("\r\n", "\n")
    if source != checked:
        raise ValueError("REFUSED: Renderer differs from committed Git HEAD")
    if git_blob(checked.encode("utf-8")) != EXPECTED_BLOB:
        # Repository may represent CRLF in Git; reject unreviewed content.
        raise ValueError("REFUSED: Renderer is not the reviewed Phase 169 baseline")
    if HELPER.exists():
        if HELPER.read_bytes() != HELPER_SOURCE.read_bytes():
            raise ValueError("REFUSED: helper filename already exists with different content")
        raise ValueError("REFUSED: helper is already installed")
    revised, complete_function = patch_function(source)
    generated = revised.replace("\n", "\r\n") if b"\r\n" in original else revised
    # Confirm both complete sources parse before writing to the repository.
    ast.parse(revised)
    ast.parse(HELPER_SOURCE.read_text(encoding="utf-8"))
    (OUT / "phase168_r3_5_model_renderer.py.before").write_bytes(original)
    (OUT / "phase168_r3_5_model_renderer.py.full.py").write_text(revised, encoding="utf-8")
    (OUT / "render_model_backed_narrative_markdown.full.py").write_text(complete_function,encoding="utf-8")
    try:
        HELPER.write_bytes(HELPER_SOURCE.read_bytes())
        TARGET.write_bytes(generated.encode("utf-8"))
    except BaseException:
        TARGET.write_bytes(original)
        if HELPER.exists():
            HELPER.unlink()
        raise
    print("PATCHED:",TARGET)
    print("NEW_MODULE:",HELPER)
    print("FULL_FUNCTION:",OUT / "render_model_backed_narrative_markdown.full.py")
    print("FULL_FILE:",OUT / "phase168_r3_5_model_renderer.py.full.py")


def restore() -> None:
    old = OUTPUT / "phase168_r3_5_model_renderer.py.before"
    full = OUTPUT / "phase168_r3_5_model_renderer.py.full.py"
    if not old.is_file() or not full.is_file():
        raise ValueError("no complete backup and installed reference exist")
    installed = full.read_text(encoding="utf-8")
    current = TARGET.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    if installed != current:
        raise ValueError("REFUSED: current renderer has unknown changes")
    if HELPER.read_bytes() != HELPER_SOURCE.read_bytes():
        raise ValueError("REFUSED: installed helper has unknown changes")
    TARGET.write_bytes(old.read_bytes())
    HELPER.unlink()
    print("RESTORED:",TARGET)
    print("REMOVED:",HELPER)


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in ("install", "restore"):
        raise SystemExit("Usage: python -m phase169_r3k_narrative_localization.apply install|restore")
    try:
        if sys.argv[1] == "install":
            install()
        else:
            restore()
    except (ValueError, OSError, subprocess.CalledProcessError, UnicodeError) as exc:
        print("R3K_REFUSED:",str(exc),file=sys.stderr)
        return 6
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

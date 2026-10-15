"""Install one shared typed statement prose case, guarded and reversible."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path.cwd()
TARGET = ROOT / "toda_group_proof_generic_narrative_renderer.py"
NAME = "_render_generic_narrative_statement_prose"
MARKER = "  # phase165_r56_r1_generator_suspension: shared typed statement prose\n"
ANCHOR = '  kind = type(statement).__name__\n'
ADDITION = (
    MARKER
    + '  if kind == "GeneratorSuspension":\n'
    + '    map_name = _generic_group_map_name(statement.map)\n'
    + '    if map_name is not None:\n'
    + '      return (\n'
    + '        "$" + map_name + "("\n'
    + '        + render_toda_expression_latex(statement.source_generator)\n'
    + '        + ") = "\n'
    + '        + render_toda_expression_latex(statement.target_generator)\n'
    + '        + "$."\n'
    + '      )\n'
)


def main() -> None:
    if not TARGET.is_file():
        raise SystemExit(f"Expected project root and {TARGET.name}")
    source = TARGET.read_text(encoding="utf-8")
    tree = ast.parse(source)
    funcs = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == NAME]
    if len(funcs) != 1:
        raise SystemExit("Expected exactly one existing shared prose function; no changes made")
    node = funcs[0]
    lines = source.splitlines(keepends=True)
    start, end = node.lineno - 1, node.end_lineno
    segment = "".join(lines[start:end])
    if MARKER not in segment:
        if segment.count(ANCHOR) != 1:
            raise SystemExit("Expected shared function anchor absent or duplicated; no changes made")
        updated = segment.replace(ANCHOR, ANCHOR + ADDITION, 1)
        new_source = "".join(lines[:start]) + updated + "".join(lines[end:])
        ast.parse(new_source)
        backup = TARGET.with_name(TARGET.name + ".phase165_r56_r1_backup")
        if backup.exists():
            raise SystemExit("Backup already exists for an uninstalled patch; inspect manually")
        backup.write_text(source, encoding="utf-8")
        TARGET.write_text(new_source, encoding="utf-8")
        print(f"Updated {TARGET.name}; backup: {backup.name}")
    else:
        print("R56-R1 common statement prose already installed")
    current = TARGET.read_text(encoding="utf-8")
    parsed = ast.parse(current)
    fn = next(n for n in parsed.body if isinstance(n, ast.FunctionDef) and n.name == NAME)
    full = "".join(current.splitlines(keepends=True)[fn.lineno - 1:fn.end_lineno])
    # Existing import section remains unchanged; full function is provided.
    report = ROOT / "phase165_r56_r1_generator_suspension_fix" / "CHANGED_CODE.md"
    report.write_text(
        "# R56-R1 変更後の関数全文\n\n変更対象: `toda_group_proof_generic_narrative_renderer.py` の "
        "`_render_generic_narrative_statement_prose()`。import の変更なし。\n\n"
        "```python\n" + full.rstrip() + "\n```\n",
        encoding="utf-8",
    )
    print("Full replacement function written to CHANGED_CODE.md")


if __name__ == "__main__":
    main()

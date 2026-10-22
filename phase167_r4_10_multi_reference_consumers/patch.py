from __future__ import annotations
import ast
from datetime import datetime
from pathlib import Path
import shutil

ROOT = Path.cwd()
TARGET = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
PACKAGE = Path(__file__).resolve().parent
FUNCTION = "link_toda_group_proof_narrative_reference_body_consumers"
START = "    consumers = list(dict.fromkeys(consumers))\n"
END = "  for reference_number, source_steps in (\n    source_steps_by_number.items()\n  ):\n"
NEW = '    consumers = list(dict.fromkeys(consumers))\n    if not consumers:\n      continue\n    source_formulas = {\n      _render_generic_narrative_step(step).strip().rstrip(".。")\n      for step in source_steps\n      if _render_generic_narrative_step(step)\n    }\n    # One literature reference may have several independent specializations.\n    # Remove a displayed general form, if present, without discarding any\n    # of its concrete consequences.\n    for old_index in range(len(lines) - 1, -1, -1):\n      stripped = lines[old_index].strip().rstrip(".。")\n      if any(\n        stripped == marker + "より, " + formula\n        or stripped == marker + "より、" + formula\n        for formula in source_formulas\n      ):\n        del lines[old_index]\n        consumers = [\n          (index - (1 if old_index < index else 0), rendered)\n          for index, rendered in consumers\n          if index != old_index\n        ]\n    # Never attach two different source references to the same visible line.\n    # Preserve already-cited lines and keep the complete concrete result.\n    for index, derived_line in consumers:\n      existing = lines[index].strip()\n      if existing.startswith("[R"):\n        continue\n      lines[index] = marker + "より, " + derived_line.rstrip(".。") + "."\n'

def transform(source: str) -> tuple[str, str]:
    tree = ast.parse(source)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == FUNCTION]
    if len(nodes) != 1:
        raise RuntimeError("Expected one reference consumer function")
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    a = sum(map(len, lines[:node.lineno - 1]))
    b = sum(map(len, lines[:node.end_lineno]))
    function = source[a:b]
    if function.count(START) != 1 or function.count(END) != 1:
        raise RuntimeError("R4-9 anchors missing or ambiguous; no change")
    begin = function.index(START)
    end = function.index(END, begin)
    old = function[begin:end]
    if "if len(consumers) != 1:" not in old or "lines[index] = marker" not in old:
        raise RuntimeError("Unexpected version of R4-9; no change")
    updated_function = function[:begin] + NEW + function[end:]
    updated = source[:a] + updated_function + source[b:]
    ast.parse(updated)
    return updated, updated_function

def main() -> None:
    if not TARGET.is_file():
        raise SystemExit("Run from repository root")
    original = TARGET.read_bytes()
    newline = "\r\n" if b"\r\n" in original else "\n"
    content = original.decode("utf-8-sig").replace("\r\n", "\n")
    updated, function = transform(content)
    folder = ROOT / "phase167_r4_10_reference_backup" / datetime.now().strftime("%Y%m%dT%H%M%S%f")
    folder.mkdir(parents=True)
    backup = folder / TARGET.name
    shutil.copy2(TARGET, backup)
    bom = b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b""
    TARGET.write_bytes(bom + updated.replace("\n", newline).encode("utf-8"))
    (PACKAGE / "modified_function_full.py").write_text(function, encoding="utf-8")
    print("PATCHED:", TARGET)
    print("BACKUP:", backup)
    print("FULL_FUNCTION:", PACKAGE / "modified_function_full.py")

if __name__ == "__main__":
    main()

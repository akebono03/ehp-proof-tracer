from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'toda_group_proof_narrative_renderer.py'
BACKUP = ROOT / 'toda_group_proof_narrative_renderer.py.phase162_exactness_math.bak'
START = 'def _phase159_public_exactness_latex(\n'
END = '\ndef _phase159_consolidate_public_exactness_lines(\n'
NEW = '''def _phase159_public_exactness_latex(\n  line: str,\n) -> str | None:\n  """Extract only the math body of an inline EHP exactness statement.\n\n  Reject malformed or prose-containing delimiters rather than re-wrapping\n  the full sentence in another pair of dollar signs.\n  """\n  if not isinstance(line, str):\n    raise TypeError("line must be a str")\n\n  stripped = line.strip()\n  if not stripped.startswith("$"):\n    return None\n\n  closing_math = stripped.find("$", 1)\n  if closing_math <= 1:\n    return None\n\n  latex = stripped[1:closing_math]\n  suffix = stripped[closing_math + 1:]\n  if suffix not in ("", ".", " は完全である."):\n    return None\n\n  if (\n    "$" in latex\n    or r"\\xrightarrow{" not in latex\n    or not latex.startswith(r"\\pi_{")\n  ):\n    return None\n\n  return latex.replace("Δ", r"\\Delta")\n\n'''

def main() -> None:
    source = TARGET.read_text(encoding='utf-8')
    if source.count(START) != 1 or source.count(END) != 1:
        raise RuntimeError('Expected unique exactness parser boundaries')
    a = source.index(START)
    b = source.index(END, a)
    old = source[a:b]
    if old == NEW:
        print('Already patched:', TARGET)
        return
    if 'closing_math = stripped.rfind(' not in old:
        raise RuntimeError('Current parser differs from audited upstream')
    updated = source[:a] + NEW + source[b:]
    ast.parse(updated, filename=str(TARGET))
    if not BACKUP.exists():
        BACKUP.write_text(source, encoding='utf-8')
    TARGET.write_text(updated, encoding='utf-8')
    print('Updated:', TARGET)
    print('Backup:', BACKUP)

if __name__ == '__main__':
    main()

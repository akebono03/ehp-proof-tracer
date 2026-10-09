from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'toda_group_proof_narrative_exactness_display_contributions.py'
BACKUP = ROOT / 'toda_group_proof_narrative_exactness_display_contributions.py.phase162_exactness_window.bak'
START = 'def _exactness_window_latex(\n'
END = '\ndef extract_toda_group_proof_narrative_exactness_display_contributions(\n'
REPLACEMENT = '''def _exactness_window_latex(
  proof_step: ProofStep,
) -> str:
  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
  )

  exactness_suffix = "$ は完全である."
  if (
    rendered.startswith("$")
    and rendered.endswith(exactness_suffix)
  ):
    return rendered[1:-len(exactness_suffix)]

  if (
    len(rendered) >= 2
    and rendered.startswith("$")
    and rendered.endswith("$")
  ):
    return rendered[1:-1]

  return rendered

'''


def main() -> None:
    source = TARGET.read_text(encoding='utf-8')
    if source.count(START) != 1 or source.count(END) != 1:
        raise RuntimeError('Exactness window function anchors are not unique')
    start = source.index(START)
    end = source.index(END, start)
    original = source[start:end]
    if original == REPLACEMENT:
        print('Already applied:', TARGET)
        return
    if 'rendered.endswith(' not in original or 'return rendered' not in original:
        raise RuntimeError('Unexpected original _exactness_window_latex function; no changes made')
    updated = source[:start] + REPLACEMENT + source[end:]
    ast.parse(updated, filename=str(TARGET))
    if not BACKUP.exists():
        BACKUP.write_text(source, encoding='utf-8')
    TARGET.write_text(updated, encoding='utf-8')
    print('Updated:', TARGET)
    print('Backup:', BACKUP)


if __name__ == '__main__':
    main()

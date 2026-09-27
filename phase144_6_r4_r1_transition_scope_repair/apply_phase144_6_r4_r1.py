from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"


def main() -> int:
  source = TARGET.read_text(encoding="utf-8-sig")

  old = """      extract_toda_group_proof_narrative_step_transitions(
        presentation,
        tuple(
          local_body_blocks
        ),
      )
"""
  new = """      extract_toda_group_proof_narrative_step_transitions(
        presentation,
        blocks,
      )
"""

  count = source.count(old)

  if count != 1:
    raise RuntimeError(
      "expected exactly one local-body step-transition call; "
      f"found {count}"
    )

  source = source.replace(
    old,
    new,
    1,
  )

  ast.parse(source)
  TARGET.write_text(
    source,
    encoding="utf-8",
  )

  print(
    "Phase 144-6-R4-R1 transition-scope repair applied."
  )
  print(
    "Changed only: "
    "toda_group_proof_narrative_argument_multi_renderer.py"
  )
  print(
    "Repair: step transitions now receive the complete "
    "presentation block partition."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

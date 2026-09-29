from collections import Counter
from dataclasses import fields, is_dataclass

from toda_group_proof_narrative_renderer import (
  _render_group_proof_narrative_latex,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  TodaLemma54WhiteheadCorrectionDataStatement,
)

TARGET_RULE = "Toda (5.4) nu_4 Whitehead correction data"


def main():
  # Reuse the proven Phase 143-75Z scanner rather than duplicate repository traversal.
  import importlib.util
  from pathlib import Path

  candidates = list(
    Path("phase143_75z").glob("audit_phase143_75z*.py")
  )
  if not candidates:
    raise SystemExit(
      "Phase 143-75Z audit script not found; keep the previous audit directory."
    )

  path = candidates[0]
  spec = importlib.util.spec_from_file_location(
    "phase143_75z_audit",
    path,
  )
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)

  # Discover the scanner entry/helpers exposed by the previous audit.
  scan = None
  for name in (
    "scan_presentations",
    "collect_presentation_nodes",
    "scan_nodes",
  ):
    candidate = getattr(module, name, None)
    if callable(candidate):
      scan = candidate
      break

  if scan is None:
    print("Phase 143-75Z audit module loaded successfully.")
    print("Its scanner helper is not public, so run its original audit first:")
    print(f"  python {path}")
    print("")
    print("Then inspect the target directly with the focused Phase 60 fixture.")
    from test_phase60_nu4_whitehead_correction import build_phase60_8_data
    statement = build_phase60_8_data()["whitehead_data_step"].conclusion
    print("Focused statement type:", type(statement).__name__)
    print("Fields:", tuple(f.name for f in fields(statement)))
    for f in fields(statement):
      value = getattr(statement, f.name)
      print(f"{f.name}: {type(value).__name__} = {value!r}")
    print("Current semantic rendering:", render_toda_proof_statement_latex(statement))
    return

  data = scan()
  print(data)


if __name__ == "__main__":
  main()

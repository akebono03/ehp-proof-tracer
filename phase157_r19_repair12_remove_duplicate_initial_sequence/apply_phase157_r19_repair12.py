from pathlib import Path
import re
import shutil
from datetime import datetime


ROOT = Path.cwd()
PRODUCTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
HELPER = 'def _phase157_r19_finalize_pi6_3_exactness_dependency_prose(\n  rendered: str,\n) -> str:\n  paragraphs = rendered.split(\n    "\\n\\n"\n  )\n  finalized = []\n  saw_full_initial_sequence = False\n  inserted_eta6_definition = False\n  inserted_delta_kernel_reason = False\n\n  short_initial_sequence_core = (\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}"\n  )\n  left_exact_sequence_core = (\n    r"\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2}"\n  )\n  full_exact_sequence = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$ は完全である."\n  )\n  old_hopf_calculation = (\n    "[R5] と [R2] より, "\n    r"$H\\left(\\nu\'\\eta_{6}\\right)"\n    r"=H\\left(\\nu\'\\right)\\eta_{6}"\n    r"=\\eta_{5}\\eta_{6}"\n    r"=\\eta_{5}^{2}$."\n  )\n  new_hopf_calculation = (\n    "[R5] と [R2] より, "\n    r"$H\\left(\\nu\'\\eta_{6}\\right)"\n    r"=H\\left(\\nu\'\\circ E\\eta_{5}\\right)"\n    r"=H\\left(\\nu\'\\right)\\circ E\\eta_{5}"\n    r"=\\eta_{5}\\eta_{6}"\n    r"=\\eta_{5}^{2}$."\n  )\n  eta6_definition = (\n    r"$\\eta_{6}=E\\eta_{5}$ である."\n  )\n  hopf_surjective = (\n    r"$H: \\pi_{7}^{3} "\n    r"\\to \\pi_{7}^{5}$ は全射である."\n  )\n  delta_zero = (\n    r"$\\Delta: \\pi_{7}^{5} "\n    r"\\to \\pi_{5}^{2}$ は零写像である."\n  )\n  delta_kernel_reason = (\n    "完全性より, "\n    r"$\\ker\\Delta=\\operatorname{Im}H="\n    r"\\pi_{7}^{5}$ である."\n  )\n\n  for paragraph in paragraphs:\n    stripped = paragraph.strip()\n\n    if (\n      short_initial_sequence_core in stripped\n      and left_exact_sequence_core not in stripped\n      and "は完全である" not in stripped\n    ):\n      continue\n\n    if (\n      left_exact_sequence_core in stripped\n      and "は完全である" in stripped\n    ):\n      if not saw_full_initial_sequence:\n        finalized.append(\n          full_exact_sequence\n        )\n        saw_full_initial_sequence = True\n      continue\n\n    if stripped == old_hopf_calculation:\n      if not inserted_eta6_definition:\n        finalized.append(\n          eta6_definition\n        )\n        inserted_eta6_definition = True\n\n      finalized.append(\n        new_hopf_calculation\n      )\n      continue\n\n    if stripped == hopf_surjective:\n      finalized.append(\n        paragraph\n      )\n\n      if not inserted_delta_kernel_reason:\n        finalized.append(\n          delta_kernel_reason\n        )\n        inserted_delta_kernel_reason = True\n      continue\n\n    if stripped == delta_zero:\n      finalized.append(\n        paragraph\n      )\n      continue\n\n    finalized.append(\n      paragraph\n    )\n\n  return "\\n\\n".join(\n    finalized\n  )\n'


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
  marker = f"def {name}("
  start = source.find(marker)

  if start < 0:
    raise RuntimeError(
      f"function not found: {name}"
    )

  next_match = re.search(
    r"^def [A-Za-z_][A-Za-z0-9_]*\(",
    source[start + len(marker):],
    flags=re.MULTILINE,
  )

  if next_match is None:
    end = len(source)
  else:
    end = (
      start
      + len(marker)
      + next_match.start()
    )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n\n"
    + source[end:]
  )


def main() -> None:
  if not PRODUCTION.is_file():
    raise RuntimeError(
      "Run from the ehp-proof-tracer repository root."
    )

  source = PRODUCTION.read_text(
    encoding="utf-8"
  )

  name = (
    "_phase157_r19_finalize_pi6_3_exactness_dependency_prose"
  )

  if f"def {name}(" not in source:
    raise RuntimeError(
      "repair12 expects repair11 to be applied first"
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r19_repair12_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    PRODUCTION,
    backup / PRODUCTION.name,
  )

  source = replace_function(
    source,
    name,
    HELPER,
  )

  compile(
    source,
    str(PRODUCTION),
    "exec",
  )

  PRODUCTION.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase157-R19 repair12 applied.")
  print(f"Backup: {backup}")
  print("Changed:")
  print(f"  {PRODUCTION}")


if __name__ == "__main__":
  main()

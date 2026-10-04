from pathlib import Path
import re
import shutil
from datetime import datetime


ROOT = Path.cwd()
PRODUCTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
R19_TEST = ROOT / "tests" / "test_phase157_r19_pi6_3_reference_dependency_restoration.py"

HELPER = 'def _phase157_r19_finalize_pi6_3_exactness_dependency_prose(\n  rendered: str,\n) -> str:\n  paragraphs = rendered.split(\n    "\\n\\n"\n  )\n  finalized = []\n  saw_full_initial_sequence = False\n  inserted_eta6_definition = False\n  inserted_delta_kernel_reason = False\n\n  short_initial_sequence = (\n    r"$\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$."\n  )\n  left_exact_sequence = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2}$ は完全である."\n  )\n  full_exact_sequence = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$ は完全である."\n  )\n  old_hopf_calculation = (\n    "[R5] と [R2] より, "\n    r"$H\\left(\\nu\'\\eta_{6}\\right)"\n    r"=H\\left(\\nu\'\\right)\\eta_{6}"\n    r"=\\eta_{5}\\eta_{6}"\n    r"=\\eta_{5}^{2}$."\n  )\n  new_hopf_calculation = (\n    "[R5] と [R2] より, "\n    r"$H\\left(\\nu\'\\eta_{6}\\right)"\n    r"=H\\left(\\nu\'\\circ E\\eta_{5}\\right)"\n    r"=H\\left(\\nu\'\\right)\\circ E\\eta_{5}"\n    r"=\\eta_{5}\\eta_{6}"\n    r"=\\eta_{5}^{2}$."\n  )\n  eta6_definition = (\n    r"$\\eta_{6}=E\\eta_{5}$ である."\n  )\n  hopf_surjective = (\n    r"$H: \\pi_{7}^{3} "\n    r"\\to \\pi_{7}^{5}$ は全射である."\n  )\n  delta_zero = (\n    r"$\\Delta: \\pi_{7}^{5} "\n    r"\\to \\pi_{5}^{2}$ は零写像である."\n  )\n  delta_kernel_reason = (\n    "完全性より, "\n    r"$\\ker\\Delta=\\operatorname{Im}H="\n    r"\\pi_{7}^{5}$ である."\n  )\n\n  for paragraph in paragraphs:\n    stripped = paragraph.strip()\n\n    if stripped == short_initial_sequence:\n      finalized.append(\n        full_exact_sequence\n      )\n      saw_full_initial_sequence = True\n      continue\n\n    if stripped == left_exact_sequence:\n      if not saw_full_initial_sequence:\n        finalized.append(\n          full_exact_sequence\n        )\n        saw_full_initial_sequence = True\n      continue\n\n    if stripped == old_hopf_calculation:\n      if not inserted_eta6_definition:\n        finalized.append(\n          eta6_definition\n        )\n        inserted_eta6_definition = True\n\n      finalized.append(\n        new_hopf_calculation\n      )\n      continue\n\n    if stripped == hopf_surjective:\n      finalized.append(\n        paragraph\n      )\n\n      if not inserted_delta_kernel_reason:\n        finalized.append(\n          delta_kernel_reason\n        )\n        inserted_delta_kernel_reason = True\n      continue\n\n    if stripped == delta_zero:\n      finalized.append(\n        paragraph\n      )\n      continue\n\n    finalized.append(\n      paragraph\n    )\n\n  return "\\n\\n".join(\n    finalized\n  )\n'
R19_DELTA_TEST = 'def test_phase157_r19_pi6_3_delta_zero_has_shallow_dependency_support():\n  _, body = _reference_and_body()\n\n  full_exactness = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$ は完全である."\n  )\n  eta6_definition = (\n    r"$\\eta_{6}=E\\eta_{5}$ である."\n  )\n  hopf_value = (\n    r"$H\\left(\\nu\'\\eta_{6}\\right)"\n    r"=H\\left(\\nu\'\\circ E\\eta_{5}\\right)"\n    r"=H\\left(\\nu\'\\right)\\circ E\\eta_{5}"\n    r"=\\eta_{5}\\eta_{6}"\n    r"=\\eta_{5}^{2}$."\n  )\n  pi7_5 = (\n    r"$\\pi_{7}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$."\n  )\n  surjective = (\n    r"$H: \\pi_{7}^{3} \\to \\pi_{7}^{5}$ は全射である."\n  )\n  kernel_reason = (\n    "完全性より, "\n    r"$\\ker\\Delta=\\operatorname{Im}H="\n    r"\\pi_{7}^{5}$ である."\n  )\n  delta_zero = (\n    r"$\\Delta: \\pi_{7}^{5} \\to \\pi_{5}^{2}$ は零写像である."\n  )\n  injective = (\n    r"$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ は単射である."\n  )\n\n  assert full_exactness in body\n  assert eta6_definition in body\n  assert "[R5] と [R2] より" in body\n  assert hopf_value in body\n  assert "[R3]より" in body\n  assert pi7_5 in body\n  assert surjective in body\n  assert kernel_reason in body\n  assert delta_zero in body\n  assert injective in body\n\n  assert body.index(\n    full_exactness\n  ) < body.index(\n    eta6_definition\n  )\n  assert body.index(\n    eta6_definition\n  ) < body.index(\n    hopf_value\n  )\n  assert body.index(\n    hopf_value\n  ) < body.index(\n    pi7_5\n  )\n  assert body.index(\n    pi7_5\n  ) < body.index(\n    surjective\n  )\n  assert body.index(\n    surjective\n  ) < body.index(\n    kernel_reason\n  )\n  assert body.index(\n    kernel_reason\n  ) < body.index(\n    delta_zero\n  )\n  assert body.index(\n    delta_zero\n  ) < body.index(\n    injective\n  )\n\n  assert (\n    r"$\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} \\pi_{6}^{3}$."\n    not in body\n  )\n'


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
  for path in (
    PRODUCTION,
    R19_TEST,
  ):
    if not path.is_file():
      raise RuntimeError(
        f"missing file: {path}"
      )

  production = PRODUCTION.read_text(
    encoding="utf-8"
  )
  r19_test = R19_TEST.read_text(
    encoding="utf-8"
  )

  finalizer_name = (
    "_phase157_r19_finalize_pi6_3_public_narrative"
  )

  if f"def {finalizer_name}(" not in production:
    raise RuntimeError(
      "R19 finalizer was not found"
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r19_repair11_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  for path in (
    PRODUCTION,
    R19_TEST,
  ):
    shutil.copy2(
      path,
      backup / path.name,
    )

  helper_name = (
    "_phase157_r19_finalize_pi6_3_exactness_dependency_prose"
  )

  if f"def {helper_name}(" not in production:
    insertion_marker = (
      f"def {finalizer_name}("
    )
    insertion_index = production.find(
      insertion_marker
    )

    if insertion_index < 0:
      raise RuntimeError(
        "finalizer insertion point not found"
      )

    production = (
      production[:insertion_index]
      + HELPER.rstrip()
      + "\n\n\n"
      + production[insertion_index:]
    )

  old_return_prelude = """  rendered = "\\n\\n".join(
    paragraphs
  )

  rendered = rendered.replace(
"""

  new_return_prelude = """  rendered = "\\n\\n".join(
    paragraphs
  )

  rendered = (
    _phase157_r19_finalize_pi6_3_exactness_dependency_prose(
      rendered
    )
  )

  rendered = rendered.replace(
"""

  if old_return_prelude not in production:
    raise RuntimeError(
      "R19 finalizer rendered join point not found"
    )

  production = production.replace(
    old_return_prelude,
    new_return_prelude,
    1,
  )

  r19_test = replace_function(
    r19_test,
    "test_phase157_r19_pi6_3_delta_zero_has_shallow_dependency_support",
    R19_DELTA_TEST,
  )

  compile(
    production,
    str(PRODUCTION),
    "exec",
  )
  compile(
    r19_test,
    str(R19_TEST),
    "exec",
  )

  PRODUCTION.write_text(
    production,
    encoding="utf-8",
    newline="\n",
  )
  R19_TEST.write_text(
    r19_test,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase157-R19 repair11 applied.")
  print(f"Backup: {backup}")
  print("Changed:")
  print(f"  {PRODUCTION}")
  print(f"  {R19_TEST}")


if __name__ == "__main__":
  main()

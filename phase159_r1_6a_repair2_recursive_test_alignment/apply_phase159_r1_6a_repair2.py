from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
TEST = ROOT / "tests" / "test_phase159_r1_6a_foundational_reference_identity.py"

REPLACEMENT_TEST = 'def test_phase159_r1_6a_pi3_2_foundational_premises_keep_identity():\n  presentation = (\n    _phase159_r1_6a_pi3_2_presentation()\n  )\n\n  expected = {\n    pi_2_1_zero_fact():\n      "sphere.circle.higher_zero",\n    pi_3_3_free_cyclic_fact():\n      "sphere.identity_group",\n    e_pi_1_1_to_pi_2_2_isomorphism_fact():\n      (\n        "sphere.low_dimensional."\n        "suspension_isomorphism"\n      ),\n  }\n\n  found = {}\n  seen_step_ids = set()\n\n  def visit(\n    proof_step,\n  ):\n    step_id = id(\n      proof_step\n    )\n\n    if step_id in seen_step_ids:\n      return\n\n    seen_step_ids.add(\n      step_id\n    )\n\n    if proof_step.conclusion in expected:\n      identity = (\n        proof_step.foundational_reference\n      )\n\n      assert identity is not None\n\n      found[\n        proof_step.conclusion\n      ] = identity.key\n\n    for premise in proof_step.premises:\n      if hasattr(\n        premise,\n        "conclusion",\n      ):\n        visit(\n          premise\n        )\n\n  visit(\n    presentation.root_step\n  )\n\n  assert found == expected\n'

def replace_test_function(
  source,
  function_name,
  replacement,
):
  marker = (
    "def "
    + function_name
    + "("
  )
  start = source.find(
    marker
  )

  if start < 0:
    raise RuntimeError(
      "test function not found: "
      + function_name
    )

  next_function = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  end = (
    len(
      source
    )
    if next_function < 0
    else next_function + 1
  )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n"
    + source[end:]
  )

def main():
  if not TEST.exists():
    raise FileNotFoundError(
      TEST
    )

  stamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase159_r1_6a_repair2_backup_"
      + stamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TEST,
    backup_dir / TEST.name,
  )

  source = TEST.read_text(
    encoding="utf-8-sig"
  )

  source = replace_test_function(
    source,
    "test_phase159_r1_6a_pi3_2_foundational_premises_keep_identity",
    REPLACEMENT_TEST,
  )

  TEST.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159-R1-6a repair2 applied."
  )
  print(
    "Backup:",
    backup_dir,
  )
  print(
    "Production code changes: none"
  )
  print(
    "Aligned the focused test with recursive foundational ancestry."
  )

if __name__ == "__main__":
  main()

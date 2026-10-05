from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_repair3"
BACKUP.mkdir(exist_ok=True)

DEPENDENCY = ROOT / "toda_proof_dependency.py"
CONTRIBUTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
R11_TEST = ROOT / "tests" / "test_phase157_r11_reference_reason_punctuation.py"


def backup(path: Path) -> None:
  destination = BACKUP / path.name

  if not destination.exists():
    shutil.copy2(
      path,
      destination,
    )


for path in (
  DEPENDENCY,
  CONTRIBUTION,
  R11_TEST,
):
  backup(
    path
  )


def ensure_hopf_surjective_map_property() -> None:
  text = DEPENDENCY.read_text(
    encoding="utf-8"
  )

  import_line = (
    "  TodaHopfInvariantSurjectiveStatement,\n"
  )

  if import_line not in text:
    anchor = (
      "  TodaHopfInvariantZeroStatement,\n"
    )

    if anchor not in text:
      raise RuntimeError(
        "could not locate Hopf map-property import anchor"
      )

    text = text.replace(
      anchor,
      import_line + anchor,
      1,
    )

    print(
      "Applied: import TodaHopfInvariantSurjectiveStatement"
    )
  else:
    print(
      "Already applied: Hopf surjective import"
    )

  tuple_line = (
    "      TodaHopfInvariantSurjectiveStatement,\n"
  )

  if tuple_line not in text:
    anchor = (
      "      TodaHopfInvariantZeroStatement,\n"
    )

    if anchor not in text:
      raise RuntimeError(
        "could not locate MAP_PROPERTY tuple anchor"
      )

    text = text.replace(
      anchor,
      tuple_line + anchor,
      1,
    )

    print(
      "Applied: classify Hopf surjective as MAP_PROPERTY"
    )
  else:
    print(
      "Already applied: Hopf surjective MAP_PROPERTY classification"
    )

  DEPENDENCY.write_text(
    text,
    encoding="utf-8",
  )


def ensure_terminal_punctuation_agnostic_reference_reuse() -> None:
  text = CONTRIBUTION.read_text(
    encoding="utf-8"
  )

  new_block = '''      for line in lines:
        stripped_line = line.strip()
        statement_core = statement_line.rstrip(
          ".,"
        )
        stripped_line_core = stripped_line.rstrip(
          ".,"
        )

        if stripped_line_core == statement_core:
          updated_lines.append(
            marker
            + "より, "
            + stripped_line_core
            + "."
          )
          continue

        if statement_line not in line:
          updated_lines.append(
            line
          )
          continue
'''

  if new_block in text:
    print(
      "Already applied: punctuation-agnostic Reference reuse"
    )
    return

  old_block = '''      for line in lines:
        if statement_line not in line:
          updated_lines.append(
            line
          )
          continue

        if line.strip() == statement_line:
          updated_lines.append(
            marker
            + "より, "
            + statement_line
          )
          continue
'''

  count = text.count(
    old_block
  )

  if count != 1:
    raise RuntimeError(
      "expected exactly one Reference/body exact-match block, "
      f"found {count}"
    )

  CONTRIBUTION.write_text(
    text.replace(
      old_block,
      new_block,
      1,
    ),
    encoding="utf-8",
  )

  print(
    "Applied: Reference/body reuse ignores terminal comma/period differences"
  )


def append_role_regression_test() -> None:
  text = R11_TEST.read_text(
    encoding="utf-8"
  )

  test_name = (
    "def test_phase157_r11_r11_hopf_surjectivity_is_dependency_map_property():"
  )

  if test_name in text:
    print(
      "Already applied: Hopf surjectivity dependency-role regression test"
    )
    return

  import_block = '''from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
'''

  replacement_import_block = '''from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_dependency import (
  TodaProofDependencyRole,
  classify_toda_proof_step_role,
)
'''

  if replacement_import_block not in text:
    if import_block not in text:
      raise RuntimeError(
        "could not locate R11 test import anchor"
      )

    text = text.replace(
      import_block,
      replacement_import_block,
      1,
    )

  new_test = r'''


def test_phase157_r11_r11_hopf_surjectivity_is_dependency_map_property():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )

  stack = [
    group_result.proof_step,
  ]
  visited = set()
  hopf_surjective_steps = []

  while stack:
    proof_step = stack.pop()
    proof_step_id = id(
      proof_step
    )

    if proof_step_id in visited:
      continue

    visited.add(
      proof_step_id
    )

    inference_rule = (
      proof_step.inference_rule
    )

    if (
      inference_rule is not None
      and inference_rule.name
      == "Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity"
    ):
      hopf_surjective_steps.append(
        proof_step
      )

    stack.extend(
      reversed(
        proof_step.premises
      )
    )

  assert hopf_surjective_steps

  for proof_step in hopf_surjective_steps:
    assert (
      classify_toda_proof_step_role(
        proof_step
      )
      is TodaProofDependencyRole.MAP_PROPERTY
    )
'''

  R11_TEST.write_text(
    text.rstrip()
    + new_test
    + "\n",
    encoding="utf-8",
  )

  print(
    "Added: Hopf surjectivity dependency-role regression test"
  )


ensure_hopf_surjective_map_property()
ensure_terminal_punctuation_agnostic_reference_reuse()
append_role_regression_test()

print("")
print("Phase157 R11-R11 repair3 applied successfully.")

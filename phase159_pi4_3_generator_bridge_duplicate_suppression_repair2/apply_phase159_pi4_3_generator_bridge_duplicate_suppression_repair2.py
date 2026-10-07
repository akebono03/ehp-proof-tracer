from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent

SEMANTICS_PATH = (
  REPO_ROOT
  / "toda_group_proof_narrative_group_structure_semantics.py"
)
CONTRIBUTION_PATH = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
OLD_IDENTITY_PATH = (
  REPO_ROOT
  / "toda_group_proof_narrative_statement_identity.py"
)
OLD_TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi4_3_semantic_final_conclusion_dedup.py"
)
NEW_TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi4_3_generator_bridge_duplicate_suppression.py"
)


OLD_IMPORT = """from toda_group_proof_narrative_statement_identity import (
  toda_group_proof_narrative_statement_semantic_key,
)
"""

OLD_INSERT_PREAMBLE = """  root_semantic_key = (
    toda_group_proof_narrative_statement_semantic_key(
      presentation.root_step.conclusion
    )
  )
  argument_conclusion_semantic_keys = {
    toda_group_proof_narrative_statement_semantic_key(
      conclusion_step.conclusion
    )
    for argument in arguments
    for conclusion_step in (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      ),
    )
    if conclusion_step is not None
  }
  root_conclusion_owned_by_argument = (
    root_semantic_key
    in argument_conclusion_semantic_keys
  )

"""

OLD_LOOP_GUARD = """      if (
        root_conclusion_owned_by_argument
        and (
          toda_group_proof_narrative_statement_semantic_key(
            contribution.proof_step.conclusion
          )
          == root_semantic_key
        )
      ):
        continue

"""

OLD_FUNCTION_START = (
  "def extract_toda_group_structure_narrative_redundant_direct_premise_step_ids(\n"
)


def rollback_repair1(
  source: str,
) -> str:
  source = source.replace(
    OLD_IMPORT,
    "",
    1,
  )
  source = source.replace(
    OLD_INSERT_PREAMBLE,
    "",
    1,
  )
  source = source.replace(
    OLD_LOOP_GUARD,
    "",
    1,
  )

  return source


def replace_semantics_function(
  source: str,
) -> str:
  start = source.find(
    OLD_FUNCTION_START
  )

  if start < 0:
    raise RuntimeError(
      "group-structure redundant-premise function not found"
    )

  replacement = 'def _toda_group_structure_narrative_generator_equivalent_via_direct_bridge(\n  left_generator,\n  right_generator,\n  direct_premise_steps: tuple[\n    ProofStep,\n    ...,\n  ],\n) -> bool:\n  if left_generator == right_generator:\n    return True\n\n  equivalent_values = [\n    left_generator,\n  ]\n  changed = True\n\n  while changed:\n    changed = False\n\n    for premise_step in direct_premise_steps:\n      statement = premise_step.conclusion\n\n      if (\n        not isinstance(\n          statement,\n          Relation,\n        )\n        or statement.relation_type\n        is not RelationType.EQUALITY\n      ):\n        continue\n\n      lhs = statement.lhs\n      rhs = statement.rhs\n      lhs_known = any(\n        lhs == value\n        for value in equivalent_values\n      )\n      rhs_known = any(\n        rhs == value\n        for value in equivalent_values\n      )\n\n      if lhs_known and not rhs_known:\n        equivalent_values.append(\n          rhs\n        )\n        changed = True\n\n      if rhs_known and not lhs_known:\n        equivalent_values.append(\n          lhs\n        )\n        changed = True\n\n  return any(\n    right_generator == value\n    for value in equivalent_values\n  )\n\n\ndef _toda_group_structure_narrative_group_equivalent_via_direct_bridge(\n  left_group,\n  right_group,\n  direct_premise_steps: tuple[\n    ProofStep,\n    ...,\n  ],\n) -> bool:\n  if type(\n    left_group\n  ) is not type(\n    right_group\n  ):\n    return False\n\n  if isinstance(\n    left_group,\n    FreeCyclicGroup,\n  ):\n    return (\n      _toda_group_structure_narrative_generator_equivalent_via_direct_bridge(\n        left_group.generator,\n        right_group.generator,\n        direct_premise_steps,\n      )\n    )\n\n  if isinstance(\n    left_group,\n    FiniteCyclicGroup,\n  ):\n    if left_group.order != right_group.order:\n      return False\n\n    return (\n      _toda_group_structure_narrative_generator_equivalent_via_direct_bridge(\n        left_group.generator,\n        right_group.generator,\n        direct_premise_steps,\n      )\n    )\n\n  return False\n\n\ndef extract_toda_group_structure_narrative_redundant_direct_premise_step_ids(\n  conclusion_step: ProofStep,\n) -> frozenset[\n  int\n]:\n  if not isinstance(\n    conclusion_step,\n    ProofStep,\n  ):\n    raise TypeError(\n      "conclusion_step must be a ProofStep"\n    )\n\n  conclusion_fact = (\n    _toda_group_structure_narrative_fact(\n      conclusion_step.conclusion\n    )\n  )\n\n  if conclusion_fact is None:\n    return frozenset()\n\n  (\n    conclusion_target,\n    conclusion_group,\n  ) = conclusion_fact\n\n  conclusion_key = (\n    toda_group_structure_narrative_semantic_key(\n      conclusion_group\n    )\n  )\n  direct_premise_steps = (\n    conclusion_step.premises\n  )\n  redundant_step_ids = set()\n\n  for premise_step in direct_premise_steps:\n    premise_fact = (\n      _toda_group_structure_narrative_fact(\n        premise_step.conclusion\n      )\n    )\n\n    if premise_fact is None:\n      continue\n\n    (\n      premise_target,\n      premise_group,\n    ) = premise_fact\n\n    if premise_target != conclusion_target:\n      continue\n\n    premise_key = (\n      toda_group_structure_narrative_semantic_key(\n        premise_group\n      )\n    )\n\n    if premise_key == conclusion_key:\n      redundant_step_ids.add(\n        id(\n          premise_step\n        )\n      )\n      continue\n\n    if (\n      _toda_group_structure_narrative_group_equivalent_via_direct_bridge(\n        premise_group,\n        conclusion_group,\n        direct_premise_steps,\n      )\n    ):\n      redundant_step_ids.add(\n        id(\n          premise_step\n        )\n      )\n\n  return frozenset(\n    redundant_step_ids\n  )\n'

  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n"
  )


def main() -> int:
  contribution_source = (
    CONTRIBUTION_PATH.read_text(
      encoding="utf-8",
    )
  )
  rolled_back_contribution = (
    rollback_repair1(
      contribution_source
    )
  )
  CONTRIBUTION_PATH.write_text(
    rolled_back_contribution,
    encoding="utf-8",
  )

  semantics_source = (
    SEMANTICS_PATH.read_text(
      encoding="utf-8",
    )
  )
  updated_semantics = (
    replace_semantics_function(
      semantics_source
    )
  )
  SEMANTICS_PATH.write_text(
    updated_semantics,
    encoding="utf-8",
  )

  if OLD_IDENTITY_PATH.exists():
    OLD_IDENTITY_PATH.unlink()

  if OLD_TEST_PATH.exists():
    OLD_TEST_PATH.unlink()

  NEW_TEST_PATH.write_text(
    (
      PACKAGE_ROOT
      / "test_phase159_pi4_3_generator_bridge_duplicate_suppression.py"
    ).read_text(
      encoding="utf-8",
    ),
    encoding="utf-8",
  )

  print(
    "Phase 159 generator-bridge duplicate suppression repair2 applied."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

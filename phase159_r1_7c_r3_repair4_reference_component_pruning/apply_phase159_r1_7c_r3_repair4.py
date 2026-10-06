from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TARGET = REPO_ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase159_r1_7c_r3_repair4_reference_component_pruning.py"
)
BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"
OUTPUT_DIR = PACKAGE_DIR / "output_after_apply"

INSERT_MARKER = "def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n"

HELPERS = r'''def _phase159_r1_7c_r3_repair4_aggregate_zero_component_line(
  statement,
  target_group: TodaPrimaryGroup,
) -> str | None:
  if not isinstance(
    target_group,
    TodaPrimaryGroup,
  ):
    raise TypeError(
      "target_group must be a TodaPrimaryGroup"
    )

  if not is_dataclass(
    statement
  ):
    return None

  target_sphere_dimension = (
    target_group.sphere_dimension
  )

  if (
    not isinstance(
      target_sphere_dimension,
      int,
    )
    or isinstance(
      target_sphere_dimension,
      bool,
    )
  ):
    return None

  statement_values = tuple(
    getattr(
      statement,
      field.name,
    )
    for field in fields(
      statement
    )
  )
  range_statements = tuple(
    value
    for value in statement_values
    if isinstance(
      value,
      ScalarGreaterEqualStatement,
    )
  )

  for value in statement_values:
    if not isinstance(
      value,
      TodaPrimaryGroupZeroStatement,
    ):
      continue

    template_group = value.group
    symbol = (
      template_group.sphere_dimension
    )

    if not isinstance(
      symbol,
      ScalarSymbol,
    ):
      continue

    specialized_group = (
      _phase159_r1_7c_r3_specialize_primary_group(
        template_group,
        symbol,
        target_sphere_dimension,
      )
    )

    if specialized_group != target_group:
      continue

    applicable_range = next(
      (
        range_statement
        for range_statement in range_statements
        for left, right in (
          (
            _phase157_r20_reference_scalar_value(
              range_statement.left,
              symbol,
              target_sphere_dimension,
            ),
            _phase157_r20_reference_scalar_value(
              range_statement.right,
              symbol,
              target_sphere_dimension,
            ),
          ),
        )
        if (
          left is not None
          and right is not None
          and left >= right
        )
      ),
      None,
    )

    if applicable_range is None:
      continue

    return (
      "$"
      + render_toda_primary_group_latex(
        template_group
      )
      + " = 0$, $"
      + _render_scalar_latex(
        applicable_range.left
      )
      + r" \ge "
      + _render_scalar_latex(
        applicable_range.right
      )
      + "$ が成り立つ."
    )

  return None


def prune_toda_group_proof_narrative_root_zero_direct_premise_references(
  presentation: TodaGroupProofPresentation,
  reference_entries,
  statement_lines_by_reference_number,
):
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  plan = (
    _phase159_r1_7c_r3_root_zero_direct_premise_plan(
      presentation
    )
  )

  if plan is None:
    return (
      reference_entries,
      statement_lines_by_reference_number,
    )

  (
    support_records,
    decomposition_step,
    _,
    _,
  ) = plan

  required_records = tuple(
    (
      support_step,
      support_kind,
      summand,
    )
    for (
      summand,
      support_step,
      support_kind,
    ) in support_records
  ) + (
    (
      decomposition_step,
      "decomposition",
      None,
    ),
  )

  required_by_reference = {}

  for (
    required_step,
    required_kind,
    target_group,
  ) in required_records:
    reference = (
      extract_toda_group_proof_step_literature_reference(
        required_step
      )
    )

    if reference is None:
      continue

    required_by_reference.setdefault(
      reference,
      [],
    ).append(
      (
        required_step,
        required_kind,
        target_group,
      )
    )

  if not required_by_reference:
    return (
      reference_entries,
      statement_lines_by_reference_number,
    )

  pruned_entries = []

  for entry in reference_entries:
    required_for_entry = (
      required_by_reference.get(
        entry.reference,
      )
    )

    if not required_for_entry:
      pruned_entries.append(
        entry
      )
      continue

    required_step_ids = {
      id(
        required_step
      )
      for (
        required_step,
        _,
        _,
      ) in required_for_entry
    }

    retained_steps = tuple(
      proof_step
      for proof_step in entry.proof_steps
      if id(
        proof_step
      ) in required_step_ids
    )

    if not retained_steps:
      pruned_entries.append(
        entry
      )
      continue

    pruned_entries.append(
      replace(
        entry,
        proof_steps=retained_steps,
      )
    )

  pruned_entries = tuple(
    pruned_entries
  )
  pruned_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      pruned_entries,
    )
  )

  for entry in pruned_entries:
    required_for_entry = (
      required_by_reference.get(
        entry.reference,
      )
    )

    if not required_for_entry:
      continue

    aggregate_records = tuple(
      (
        required_step,
        target_group,
      )
      for (
        required_step,
        required_kind,
        target_group,
      ) in required_for_entry
      if required_kind == "aggregate_zero"
    )

    if len(
      aggregate_records
    ) != 1:
      continue

    (
      aggregate_step,
      target_group,
    ) = aggregate_records[0]
    component_line = (
      _phase159_r1_7c_r3_repair4_aggregate_zero_component_line(
        aggregate_step.conclusion,
        target_group,
      )
    )

    if component_line is None:
      continue

    pruned_lines[
      entry.number
    ] = (
      component_line,
    )

  return (
    pruned_entries,
    pruned_lines,
  )


'''

CALL_OLD = '''  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
'''

CALL_NEW = '''  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    prune_toda_group_proof_narrative_root_zero_direct_premise_references(
      presentation,
      reference_entries,
      statement_lines_by_reference_number,
    )
  )

  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
'''


def extract_function(
  text: str,
  function_name: str,
) -> str:
  marker = "def " + function_name + "("
  start = text.find(marker)

  if start < 0:
    raise RuntimeError(
      "function not found: "
      + function_name
    )

  next_function = text.find(
    "\ndef ",
    start + len(marker),
  )

  if next_function < 0:
    return text[start:]

  return text[
    start:
    next_function + 1
  ]


def main() -> None:
  if not TARGET.exists():
    raise FileNotFoundError(
      f"repository target not found: {TARGET}"
    )

  source = TARGET.read_text(
    encoding="utf-8"
  )

  required_r3_symbols = (
    "def _phase159_r1_7c_r3_root_zero_direct_premise_plan(",
    "def _phase159_r1_7c_r3_specialize_primary_group(",
    "TodaPrimaryGroupZeroStatement",
  )

  missing = tuple(
    symbol
    for symbol in required_r3_symbols
    if symbol not in source
  )

  if missing:
    raise RuntimeError(
      "R3 base implementation is required before repair4: "
      + ", ".join(missing)
    )

  already_applied = (
    "def prune_toda_group_proof_narrative_root_zero_direct_premise_references("
    in source
  )

  if not already_applied:
    BACKUP_DIR.mkdir(
      parents=True,
      exist_ok=True,
    )
    backup = BACKUP_DIR / TARGET.name

    if not backup.exists():
      shutil.copy2(
        TARGET,
        backup,
      )

    marker_count = source.count(
      INSERT_MARKER
    )

    if marker_count != 1:
      raise RuntimeError(
        "expected one render function marker; "
        f"found {marker_count}"
      )

    source = source.replace(
      INSERT_MARKER,
      HELPERS + INSERT_MARKER,
      1,
    )

    call_count = source.count(
      CALL_OLD
    )

    if call_count != 1:
      raise RuntimeError(
        "expected one reference-section hook; "
        f"found {call_count}"
      )

    source = source.replace(
      CALL_OLD,
      CALL_NEW,
      1,
    )

    TARGET.write_text(
      source,
      encoding="utf-8",
    )

  TEST_TARGET.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    PACKAGE_DIR
    / "test_phase159_r1_7c_r3_repair4_reference_component_pruning.py",
    TEST_TARGET,
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  current = TARGET.read_text(
    encoding="utf-8"
  )

  (
    OUTPUT_DIR
    / "prune_reference_function_after.txt"
  ).write_text(
    extract_function(
      current,
      "prune_toda_group_proof_narrative_root_zero_direct_premise_references",
    ),
    encoding="utf-8",
  )

  (
    OUTPUT_DIR
    / "render_multi_argument_function_after.txt"
  ).write_text(
    extract_function(
      current,
      "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
    ),
    encoding="utf-8",
  )

  print(
    "Phase 159 R1-7c R3 repair4 applied."
  )
  print(
    "Production file:",
    TARGET,
  )
  print(
    "Focused test:",
    TEST_TARGET,
  )
  print(
    "Already applied:",
    already_applied,
  )
  print(
    "Full changed render function:",
    OUTPUT_DIR
    / "render_multi_argument_function_after.txt",
  )


if __name__ == "__main__":
  main()

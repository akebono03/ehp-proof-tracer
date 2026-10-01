from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent


def find_repository_root() -> Path:
  candidates = (
    PACKAGE_DIR.parent,
    Path.cwd(),
  )

  for candidate in candidates:
    if (
      (
        candidate
        / "toda_group_proof_narrative_contribution_renderer.py"
      ).is_file()
      and (
        candidate
        / "toda_group_proof_narrative_renderer.py"
      ).is_file()
      and (
        candidate
        / "tests"
      ).is_dir()
    ):
      return candidate.resolve()

  raise SystemExit(
    "EHP Proof Tracer repository root was not found."
  )


def replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(old)

  if count != 1:
    raise SystemExit(
      f"{label}: expected exactly one replacement target, found {count}."
    )

  return text.replace(
    old,
    new,
    1,
  )


def patch_contribution_renderer(
  repo: Path,
) -> None:
  path = (
    repo
    / "toda_group_proof_narrative_contribution_renderer.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  old = '''def suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
  presentation: TodaGroupProofPresentation,
  body_markdown: str,
  reference_entries,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  suppressed_fragments = set()
  aggregate_reference_labels = set()

  for entry in reference_entries:
    for aggregate_step in entry.proof_steps:
      component = (
        _phase153_r6_reference_aggregate_component(
          presentation,
          entry,
          aggregate_step,
        )
      )

      if component is None:
        continue

      retained_premises = tuple(
        premise_step
        for premise_step in aggregate_step.premises
        if premise_step.conclusion == component
      )

      if len(
        retained_premises
      ) != 1:
        continue

      aggregate_reference_labels.add(
        entry.reference.label
      )

      for premise_step in aggregate_step.premises:
        if premise_step is retained_premises[0]:
          continue

        independent_consumers = tuple(
          edge.parent_step
          for edge in presentation.edges
          if (
            edge.premise_step
            is premise_step
            and edge.parent_step
            is not aggregate_step
          )
        )

        if independent_consumers:
          continue

        rendered = (
          _render_generic_narrative_step(
            premise_step
          )
        )

        if rendered:
          suppressed_fragments.add(
            rendered
          )

  if not suppressed_fragments and not aggregate_reference_labels:
    return body_markdown

  lines = []

  for line in body_markdown.splitlines():
    if any(
      fragment in line
      for fragment in suppressed_fragments
    ):
      continue

    if (
      any(
        reference_label in line
        for reference_label in aggregate_reference_labels
      )
      and (
        "有限次元結果を得る" in line
        or "有限次元結果を示す" in line
      )
    ):
      continue

    lines.append(
      line
    )

  compacted_lines = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()

    if is_blank and previous_blank:
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  return "\\n".join(
    compacted_lines
  ).strip()


'''

  new = '''def _phase153_r7_reaches_root_without_step(
  presentation: TodaGroupProofPresentation,
  source_step: ProofStep,
  excluded_step: ProofStep,
) -> bool:
  children_by_step_id = {}

  for edge in presentation.edges:
    if edge.parent_step is excluded_step:
      continue

    children_by_step_id.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  target_id = id(
    presentation.root_step
  )
  stack = [
    source_step,
  ]
  visited = set()

  while stack:
    current = stack.pop()
    current_id = id(
      current
    )

    if current_id in visited:
      continue

    visited.add(
      current_id
    )

    if current_id == target_id:
      return True

    stack.extend(
      children_by_step_id.get(
        current_id,
        (),
      )
    )

  return False


def suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
  presentation: TodaGroupProofPresentation,
  body_markdown: str,
  reference_entries,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  suppressed_fragments = set()
  aggregate_reference_labels = set()

  for entry in reference_entries:
    for aggregate_step in entry.proof_steps:
      component = (
        _phase153_r6_reference_aggregate_component(
          presentation,
          entry,
          aggregate_step,
        )
      )

      if component is None:
        continue

      retained_premises = tuple(
        premise_step
        for premise_step in aggregate_step.premises
        if premise_step.conclusion == component
      )

      if len(
        retained_premises
      ) != 1:
        continue

      aggregate_reference_labels.add(
        entry.reference.label
      )

      for premise_step in aggregate_step.premises:
        if premise_step is retained_premises[0]:
          continue

        if (
          _phase153_r7_reaches_root_without_step(
            presentation,
            premise_step,
            aggregate_step,
          )
        ):
          continue

        rendered = (
          _render_generic_narrative_step(
            premise_step
          )
        )

        if rendered:
          suppressed_fragments.add(
            rendered
          )

  if not suppressed_fragments and not aggregate_reference_labels:
    return body_markdown

  lines = []

  for line in body_markdown.splitlines():
    if any(
      fragment in line
      for fragment in suppressed_fragments
    ):
      continue

    if (
      any(
        reference_label in line
        for reference_label in aggregate_reference_labels
      )
      and (
        "有限次元結果を得る" in line
        or "有限次元結果を示す" in line
      )
    ):
      continue

    lines.append(
      line
    )

  compacted_lines = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()

    if is_blank and previous_blank:
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  return "\\n".join(
    compacted_lines
  ).strip()


'''

  text = replace_once(
    text,
    old,
    new,
    "Phase 153-R7 aggregate suppression function",
  )

  path.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )


def install_test(
  repo: Path,
) -> None:
  shutil.copy2(
    (
      PACKAGE_DIR
      / "tests"
      / "test_phase153_r7_independent_root_path.py"
    ),
    (
      repo
      / "tests"
      / "test_phase153_r7_independent_root_path.py"
    ),
  )


def main() -> None:
  repo = find_repository_root()

  backup_dir = (
    repo
    / "phase153_r7_independent_root_path_repair_r3_backup"
  )
  backup_dir.mkdir(
    exist_ok=True
  )

  production_path = (
    repo
    / "toda_group_proof_narrative_contribution_renderer.py"
  )
  backup_path = (
    backup_dir
    / production_path.name
  )

  if not backup_path.exists():
    shutil.copy2(
      production_path,
      backup_path,
    )

  patch_contribution_renderer(
    repo
  )
  install_test(
    repo
  )

  print(
    "Phase 153-R7 independent-root-path repair R3 applied."
  )
  print(
    "Changed:"
  )
  print(
    "  toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "Added:"
  )
  print(
    "  tests/test_phase153_r7_independent_root_path.py"
  )


if __name__ == "__main__":
  main()

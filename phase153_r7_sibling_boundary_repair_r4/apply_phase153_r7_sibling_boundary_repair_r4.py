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
  count = text.count(
    old
  )

  if count != 1:
    raise SystemExit(
      f"{label}: expected exactly one replacement target, "
      f"found {count}."
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

  old_helper = '''def _phase153_r7_reaches_root_without_step(
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


'''

  new_helper = '''def _phase153_r7_reaches_root_without_steps(
  presentation: TodaGroupProofPresentation,
  source_step: ProofStep,
  excluded_steps: tuple[
    ProofStep,
    ...,
  ],
) -> bool:
  excluded_step_ids = {
    id(
      proof_step
    )
    for proof_step in excluded_steps
  }
  children_by_step_id = {}

  for edge in presentation.edges:
    if (
      id(
        edge.parent_step
      )
      in excluded_step_ids
    ):
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
      child_step
      for child_step in children_by_step_id.get(
        current_id,
        (),
      )
      if (
        id(
          child_step
        )
        not in excluded_step_ids
      )
    )

  return False


'''

  text = replace_once(
    text,
    old_helper,
    new_helper,
    "R7 root-reachability helper",
  )

  old_loop = '''      for premise_step in aggregate_step.premises:
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
'''

  new_loop = '''      unselected_premises = tuple(
        premise_step
        for premise_step in aggregate_step.premises
        if premise_step is not retained_premises[0]
      )

      for premise_step in unselected_premises:
        blocked_sibling_steps = tuple(
          sibling_step
          for sibling_step in unselected_premises
          if sibling_step is not premise_step
        )

        if (
          _phase153_r7_reaches_root_without_steps(
            presentation,
            premise_step,
            (
              aggregate_step,
              *blocked_sibling_steps,
            ),
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
'''

  text = replace_once(
    text,
    old_loop,
    new_loop,
    "R7 sibling suppression loop",
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
      / "test_phase153_r7_sibling_boundary.py"
    ),
    (
      repo
      / "tests"
      / "test_phase153_r7_sibling_boundary.py"
    ),
  )


def main() -> None:
  repo = find_repository_root()

  backup_dir = (
    repo
    / "phase153_r7_sibling_boundary_repair_r4_backup"
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
    "Phase 153-R7 sibling-boundary repair R4 applied."
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
    "  tests/test_phase153_r7_sibling_boundary.py"
  )


if __name__ == "__main__":
  main()

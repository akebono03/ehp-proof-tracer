from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent
TARGET_PATH = ROOT / "toda_group_proof_narrative_renderer.py"
BACKUP_PATH = (
  ROOT
  / "toda_group_proof_narrative_renderer.py.phase132_8_backup"
)


def replace_exact(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(
    old
  )

  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one match, found {count}"
    )

  return text.replace(
    old,
    new,
    1,
  )


def main() -> None:
  if not TARGET_PATH.exists():
    raise RuntimeError(
      "toda_group_proof_narrative_renderer.py "
      "was not found in the repository root"
    )

  original = TARGET_PATH.read_text(
    encoding="utf-8",
  )

  if not BACKUP_PATH.exists():
    shutil.copy2(
      TARGET_PATH,
      BACKUP_PATH,
    )

  old_append = '''def _append_narrative_for_step(
  lines: list[str],
  presentation: TodaGroupProofPresentation,
  parent_step: ProofStep,
  active_step_ids: set[int],
) -> None:
  parent_id = id(
    parent_step
  )

  if parent_id in active_step_ids:
    return

  active_step_ids.add(
    parent_id
  )

  edges = (
    _narrative_edges_for_parent(
      presentation,
      parent_step,
    )
  )

  for index, edge in enumerate(
    edges
  ):
    premise_step = edge.premise_step

    premise_edges = (
      _narrative_edges_for_parent(
        presentation,
        premise_step,
      )
    )

    if premise_edges:
      _append_narrative_for_step(
        lines,
        presentation,
        premise_step,
        active_step_ids,
      )

      lines.append(
        (
          "これらから、"
          + _render_group_proof_narrative_fact(
            premise_step
          )
          + "を得る。"
        )
      )
      continue

    lines.append(
      (
        _premise_lead(
          index,
          len(
            edges
          ),
        )
        + "、"
        + _render_group_proof_narrative_fact(
          premise_step
        )
        + "を用いる。"
      )
    )

  active_step_ids.remove(
    parent_id
  )
'''

  new_append = '''def _append_narrative_for_step(
  lines: list[str],
  presentation: TodaGroupProofPresentation,
  parent_step: ProofStep,
  active_step_ids: set[int],
  expanded_step_ids: set[int],
) -> None:
  parent_id = id(
    parent_step
  )

  if parent_id in active_step_ids:
    return

  active_step_ids.add(
    parent_id
  )

  edges = (
    _narrative_edges_for_parent(
      presentation,
      parent_step,
    )
  )

  for index, edge in enumerate(
    edges
  ):
    premise_step = edge.premise_step
    premise_id = id(
      premise_step
    )
    premise_fact = (
      _render_group_proof_narrative_fact(
        premise_step
      )
    )
    lead = (
      _premise_lead(
        index,
        len(
          edges
        ),
      )
    )

    if premise_id in expanded_step_ids:
      lines.append(
        (
          lead
          + "、既出の"
          + premise_fact
          + "を用いる。"
        )
      )
      continue

    premise_edges = (
      _narrative_edges_for_parent(
        presentation,
        premise_step,
      )
    )

    if premise_edges:
      _append_narrative_for_step(
        lines,
        presentation,
        premise_step,
        active_step_ids,
        expanded_step_ids,
      )

      lines.append(
        (
          "これらから、"
          + premise_fact
          + "を得る。"
        )
      )
    else:
      lines.append(
        (
          lead
          + "、"
          + premise_fact
          + "を用いる。"
        )
      )

    expanded_step_ids.add(
      premise_id
    )

  active_step_ids.remove(
    parent_id
  )
'''

  updated = replace_exact(
    original,
    old_append,
    new_append,
    "_append_narrative_for_step",
  )

  old_call = '''    _append_narrative_for_step(
      lines,
      presentation,
      presentation.root_step,
      set(),
    )
'''

  new_call = '''    _append_narrative_for_step(
      lines,
      presentation,
      presentation.root_step,
      set(),
      set(),
    )
'''

  updated = replace_exact(
    updated,
    old_call,
    new_call,
    "root narrative traversal call",
  )

  TARGET_PATH.write_text(
    updated,
    encoding="utf-8",
  )

  print(
    "Phase 132-8 applied successfully."
  )
  print(
    f"Backup: {BACKUP_PATH.name}"
  )


if __name__ == "__main__":
  main()

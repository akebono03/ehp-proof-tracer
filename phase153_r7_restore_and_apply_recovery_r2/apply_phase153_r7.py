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

  marker = (
    "def suppress_toda_group_proof_narrative_reference_body_duplicates(\n"
  )

  addition = """def suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
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


"""

  if marker not in text:
    raise SystemExit(
      "aggregate suppression insertion marker not found."
    )

  text = text.replace(
    marker,
    addition + marker,
    1,
  )

  old = """  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      rendered,
      statement_lines_by_reference_number,
    )
  )
"""

  new = """  rendered = (
    suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
      presentation,
      rendered,
      reference_entries,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      rendered,
      statement_lines_by_reference_number,
    )
  )
"""

  text = replace_once(
    text,
    old,
    new,
    "generic proof-body suppression integration",
  )

  path.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )


def patch_narrative_renderer(
  repo: Path,
) -> None:
  path = (
    repo
    / "toda_group_proof_narrative_renderer.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  old = """from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
  suppress_toda_group_proof_narrative_reference_body_duplicates,
)
"""

  new = """from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
  suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry,
  suppress_toda_group_proof_narrative_reference_body_duplicates,
)
"""

  text = replace_once(
    text,
    old,
    new,
    "narrative renderer imports",
  )

  old = """      suppressed_body = (
        suppress_toda_group_proof_narrative_reference_body_duplicates(
          body,
          statement_lines_by_reference_number,
        )
      )
"""

  new = """      suppressed_body = (
        suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
          presentation,
          body,
          reference_entries,
        )
      )
      suppressed_body = (
        suppress_toda_group_proof_narrative_reference_body_duplicates(
          suppressed_body,
          statement_lines_by_reference_number,
        )
      )
"""

  text = replace_once(
    text,
    old,
    new,
    "legacy proof-body suppression integration",
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
      / "test_phase153_r7_proof_body_relevance.py"
    ),
    (
      repo
      / "tests"
      / "test_phase153_r7_proof_body_relevance.py"
    ),
  )


def main() -> None:
  repo = find_repository_root()

  backup_dir = (
    repo
    / "phase153_r7_backup_before_apply"
  )
  backup_dir.mkdir(
    exist_ok=True
  )

  for filename in (
    "toda_group_proof_narrative_contribution_renderer.py",
    "toda_group_proof_narrative_renderer.py",
  ):
    source = repo / filename
    backup = backup_dir / filename

    if not backup.exists():
      shutil.copy2(
        source,
        backup,
      )

  patch_contribution_renderer(
    repo
  )
  patch_narrative_renderer(
    repo
  )
  install_test(
    repo
  )

  print(
    "Phase 153-R7 patch applied."
  )
  print(
    "Changed:"
  )
  print(
    "  toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "  toda_group_proof_narrative_renderer.py"
  )
  print(
    "Added:"
  )
  print(
    "  tests/test_phase153_r7_proof_body_relevance.py"
  )
  print(
    "Backup:"
  )
  print(
    "  phase153_r7_backup_before_apply/"
  )


if __name__ == "__main__":
  main()

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent


def find_repository_root() -> Path:
  for candidate in (
    PACKAGE_DIR.parent,
    Path.cwd(),
  ):
    if (
      (
        candidate
        / "toda_group_proof_narrative_renderer.py"
      ).is_file()
      and (
        candidate
        / "toda_group_proof_narrative_references.py"
      ).is_file()
    ):
      return candidate.resolve()

  raise SystemExit(
    "EHP Proof Tracer repository root was not found."
  )


def restore_renderer_from_r13_backup(
  repo: Path,
) -> None:
  backup = (
    repo
    / "phase153_closure_repair_r13_backup"
    / "toda_group_proof_narrative_renderer.py"
  )
  target = (
    repo
    / "toda_group_proof_narrative_renderer.py"
  )

  if not backup.is_file():
    raise SystemExit(
      "R13 renderer backup was not found: "
      + str(
        backup
      )
    )

  shutil.copy2(
    backup,
    target,
  )


def replace_connector(
  repo: Path,
) -> None:
  path = (
    repo
    / "toda_group_proof_narrative_renderer.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  start_marker = (
    "def _phase153_r3_10_connect_public_reference_section(\n"
  )
  end_marker = (
    "\ndef _wrap_phase150_rc4_generic_public_narrative(\n"
  )

  start = text.find(
    start_marker
  )
  if start < 0:
    raise SystemExit(
      "R13 specialized public Reference connector start was not found."
    )

  end = text.find(
    end_marker,
    start,
  )
  if end < 0:
    raise SystemExit(
      "R13 specialized public Reference connector end was not found."
    )

  replacement = '''def _phase153_r3_10_connect_public_reference_section(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  if presentation.max_depth < 2:
    return rendered

  lines = rendered.splitlines()
  reference_header = "## 使用する結果"
  proof_header = "## 証明"

  try:
    reference_index = lines.index(
      reference_header
    )
    proof_index = lines.index(
      proof_header
    )
  except ValueError:
    return rendered

  if reference_index >= proof_index:
    return rendered

  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )

  if not reference_entries:
    return rendered

  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )

  proof_body = "\\n".join(
    lines[
      proof_index
      + 1:
    ]
  ).lstrip()

  (
    used_reference_entries,
    used_statement_lines,
    filtered_proof_body,
  ) = (
    filter_toda_group_proof_narrative_reference_entries_by_body_usage(
      reference_entries,
      statement_lines_by_reference_number,
      proof_body,
    )
  )

  (
    filtered_reference_entries,
    filtered_statement_lines,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      used_reference_entries,
      used_statement_lines,
      presentation.root_step,
    )
  )

  if (
    len(
      filtered_reference_entries
    )
    != len(
      used_reference_entries
    )
  ):
    return rendered

  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      filtered_reference_entries,
      filtered_statement_lines,
    )
  )

  if not reference_section:
    return rendered

  prefix_lines = lines[
    :reference_index
  ]

  while (
    prefix_lines
    and not prefix_lines[
      -1
    ].strip()
  ):
    prefix_lines.pop()

  return (
    "\\n".join(
      (
        *prefix_lines,
        "",
        reference_header,
        "",
        reference_section,
        "",
        proof_header,
        "",
        filtered_proof_body,
      )
    ).rstrip()
    + "\\n"
  )


'''

  updated = (
    text[
      :start
    ]
    + replacement
    + text[
      end
      + 1:
    ]
  )

  path.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )


def install_test(
  repo: Path,
) -> None:
  source = (
    PACKAGE_DIR
    / "test_phase153_closure_repair_r13_syntax_repair_r1.py"
  )
  target = (
    repo
    / "tests"
    / "test_phase153_closure_repair_r13_syntax_repair_r1.py"
  )
  shutil.copy2(
    source,
    target,
  )


def main() -> None:
  repo = find_repository_root()

  restore_renderer_from_r13_backup(
    repo
  )
  replace_connector(
    repo
  )
  install_test(
    repo
  )

  print(
    "Phase 153 closure repair R13 syntax repair R1 applied."
  )
  print(
    "Restored and repaired:"
  )
  print(
    "  toda_group_proof_narrative_renderer.py"
  )
  print(
    "Kept from R13:"
  )
  print(
    "  toda_group_proof_narrative_references.py"
  )
  print(
    "Added:"
  )
  print(
    "  tests/test_phase153_closure_repair_r13_syntax_repair_r1.py"
  )


if __name__ == "__main__":
  main()

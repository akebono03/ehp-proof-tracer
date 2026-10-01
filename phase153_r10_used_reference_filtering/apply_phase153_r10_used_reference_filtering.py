from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent


def find_repository_root() -> Path:
  for candidate in (
    PACKAGE_DIR.parent,
    Path.cwd(),
  ):
    if (
      (candidate / "toda_group_proof_narrative_references.py").is_file()
      and (candidate / "toda_group_proof_narrative_contribution_renderer.py").is_file()
      and (candidate / "toda_group_proof_narrative_renderer.py").is_file()
      and (candidate / "tests").is_dir()
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
      f"{label}: expected exactly one replacement target, found {count}."
    )

  return text.replace(
    old,
    new,
    1,
  )


def patch_references(
  repo: Path,
) -> None:
  path = (
    repo
    / "toda_group_proof_narrative_references.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  text = replace_once(
    text,
    "from dataclasses import dataclass\n",
    "from dataclasses import (\n  dataclass,\n  replace,\n)\n",
    "R10 dataclasses import",
  )

  marker = (
    "def render_toda_group_proof_narrative_reference_entries_markdown(\n"
  )

  helper = r'''def filter_toda_group_proof_narrative_reference_entries_by_body_usage(
  entries: tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
  body_markdown: str,
) -> tuple[
  tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
  str,
]:
  if not isinstance(
    entries,
    tuple,
  ):
    raise TypeError(
      "entries must be a tuple"
    )

  if not all(
    isinstance(
      entry,
      TodaGroupProofNarrativeReferenceEntry,
    )
    for entry in entries
  ):
    raise TypeError(
      "entries must contain only "
      "TodaGroupProofNarrativeReferenceEntry objects"
    )

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  used_entries = tuple(
    entry
    for entry in entries
    if (
      "[R"
      + str(
        entry.number
      )
      + "]"
    )
    in body_markdown
  )

  number_map = {
    entry.number: new_number
    for new_number, entry in enumerate(
      used_entries,
      start=1,
    )
  }

  filtered_entries = tuple(
    replace(
      entry,
      number=number_map[
        entry.number
      ],
    )
    for entry in used_entries
  )

  filtered_statement_lines = {
    number_map[
      entry.number
    ]: statement_lines_by_reference_number[
      entry.number
    ]
    for entry in used_entries
    if entry.number in statement_lines_by_reference_number
  }

  def replace_marker(
    match,
  ):
    old_number = int(
      match.group(
        1
      )
    )
    new_number = number_map.get(
      old_number
    )

    if new_number is None:
      return match.group(
        0
      )

    return (
      "[R"
      + str(
        new_number
      )
      + "]"
    )

  filtered_body = re.sub(
    r"\[R([0-9]+)\]",
    replace_marker,
    body_markdown,
  )

  return (
    filtered_entries,
    filtered_statement_lines,
    filtered_body,
  )


'''

  if (
    "def filter_toda_group_proof_narrative_reference_entries_by_body_usage("
    in text
  ):
    raise SystemExit(
      "R10 filtering helper is already present."
    )

  if marker not in text:
    raise SystemExit(
      "R10 filtering helper insertion marker not found."
    )

  path.write_text(
    text.replace(
      marker,
      helper + marker,
      1,
    ),
    encoding="utf-8",
    newline="\n",
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

  old_import = '''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  render_toda_group_proof_narrative_reference_entries_markdown,
  select_toda_group_proof_narrative_reference_statement_steps,
)
'''

  new_import = '''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
  render_toda_group_proof_narrative_reference_entries_markdown,
  select_toda_group_proof_narrative_reference_statement_steps,
)
'''

  text = replace_once(
    text,
    old_import,
    new_import,
    "R10 contribution renderer import",
  )

  old = '''  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      rendered,
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

  new = '''  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      rendered,
      statement_lines_by_reference_number,
    )
  )
  (
    reference_entries,
    statement_lines_by_reference_number,
    rendered,
  ) = (
    filter_toda_group_proof_narrative_reference_entries_by_body_usage(
      reference_entries,
      statement_lines_by_reference_number,
      rendered,
    )
  )
  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
'''

  text = replace_once(
    text,
    old,
    new,
    "R10 generic reference filtering",
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

  old_import = '''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
'''

  new_import = '''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
'''

  text = replace_once(
    text,
    old_import,
    new_import,
    "R10 narrative renderer import",
  )

  old = '''      suppressed_body = (
        suppress_toda_group_proof_narrative_reference_body_duplicates(
          suppressed_body,
          statement_lines_by_reference_number,
        )
      )
      rendered = (
        rendered[
          :body_start
        ]
        + suppressed_body
        + "\\n"
      )
'''

  new = '''      suppressed_body = (
        suppress_toda_group_proof_narrative_reference_body_duplicates(
          suppressed_body,
          statement_lines_by_reference_number,
        )
      )
      (
        filtered_reference_entries,
        filtered_statement_lines,
        suppressed_body,
      ) = (
        filter_toda_group_proof_narrative_reference_entries_by_body_usage(
          reference_entries,
          statement_lines_by_reference_number,
          suppressed_body,
        )
      )
      filtered_reference_section = (
        render_toda_group_proof_narrative_reference_entries_markdown(
          filtered_reference_entries,
          filtered_statement_lines,
        )
      )
      prefix_lines = [
        "# Group proof narrative",
        "",
        theorem + "を用いる。",
        "",
      ]

      if filtered_reference_section:
        prefix_lines.extend(
          (
            "## 使用する結果",
            "",
            filtered_reference_section,
            "",
            "## 証明",
            "",
          )
        )

      rendered = (
        "\\n".join(
          prefix_lines
        )
        + suppressed_body
        + "\\n"
      )
'''

  text = replace_once(
    text,
    old,
    new,
    "R10 legacy reference filtering",
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
      / "test_phase153_r10_used_reference_filtering.py"
    ),
    (
      repo
      / "tests"
      / "test_phase153_r10_used_reference_filtering.py"
    ),
  )


def main() -> None:
  repo = find_repository_root()
  backup_dir = (
    repo
    / "phase153_r10_used_reference_filtering_backup"
  )
  backup_dir.mkdir(
    exist_ok=True
  )

  for filename in (
    "toda_group_proof_narrative_references.py",
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

  patch_references(
    repo
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
    "Phase 153-R10 Used Reference filtering applied."
  )
  print(
    "Changed:"
  )
  print(
    "  toda_group_proof_narrative_references.py"
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
    "  tests/test_phase153_r10_used_reference_filtering.py"
  )


if __name__ == "__main__":
  main()

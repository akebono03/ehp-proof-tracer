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


def patch_file(
  repo: Path,
) -> None:
  path = (
    repo
    / "toda_group_proof_narrative_contribution_renderer.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  old = '''def suppress_toda_group_proof_narrative_reference_body_duplicates(
  body_markdown: str,
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
) -> str:
  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  lines = body_markdown.splitlines()

  for reference_number, statement_lines in (
    statement_lines_by_reference_number.items()
  ):
    if (
      isinstance(
        reference_number,
        bool,
      )
      or not isinstance(
        reference_number,
        int,
      )
    ):
      raise TypeError(
        "statement_lines_by_reference_number keys "
        "must be integers"
      )

    if not isinstance(
      statement_lines,
      tuple,
    ):
      raise TypeError(
        "statement_lines_by_reference_number values "
        "must be tuples"
      )

    marker = (
      "[R"
      + str(
        reference_number
      )
      + "]"
    )

    for statement_line in statement_lines:
      if not isinstance(
        statement_line,
        str,
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must contain only strings"
        )

      if not statement_line:
        continue

      updated_lines = []

      for line in lines:
        if statement_line not in line:
          updated_lines.append(
            line
          )
          continue

        if line.strip() == statement_line:
          continue

        if marker in line:
          prefix = line.split(
            marker,
            1,
          )[0]

          updated_lines.append(
            prefix
            + marker
            + "を用いる。"
          )
          continue

        updated_lines.append(
          line.replace(
            statement_line,
            marker,
          )
        )

      lines = updated_lines

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

  new = '''def suppress_toda_group_proof_narrative_reference_body_duplicates(
  body_markdown: str,
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
) -> str:
  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  lines = body_markdown.splitlines()

  for reference_number, statement_lines in (
    statement_lines_by_reference_number.items()
  ):
    if (
      isinstance(
        reference_number,
        bool,
      )
      or not isinstance(
        reference_number,
        int,
      )
    ):
      raise TypeError(
        "statement_lines_by_reference_number keys "
        "must be integers"
      )

    if not isinstance(
      statement_lines,
      tuple,
    ):
      raise TypeError(
        "statement_lines_by_reference_number values "
        "must be tuples"
      )

    marker = (
      "[R"
      + str(
        reference_number
      )
      + "]"
    )

    for statement_line in statement_lines:
      if not isinstance(
        statement_line,
        str,
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must contain only strings"
        )

      if not statement_line:
        continue

      updated_lines = []

      for line in lines:
        if statement_line not in line:
          updated_lines.append(
            line
          )
          continue

        if line.strip() == statement_line:
          continue

        if marker in line:
          updated_lines.append(
            marker
            + "を用いる。"
          )
          continue

        replaced_line = line.replace(
          statement_line,
          marker,
        )

        if (
          marker in replaced_line
          and (
            replaced_line.rstrip().endswith(
              marker
              + "を得る。"
            )
            or replaced_line.rstrip().endswith(
              marker
              + "を得る."
            )
          )
        ):
          updated_lines.append(
            marker
            + "を用いる。"
          )
          continue

        updated_lines.append(
          replaced_line
        )

      lines = updated_lines

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
    "Reference-use prose normalization",
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
      / "test_phase153_r8_reference_use_prose_normalization.py"
    ),
    (
      repo
      / "tests"
      / "test_phase153_r8_reference_use_prose_normalization.py"
    ),
  )


def main() -> None:
  repo = find_repository_root()

  backup_dir = (
    repo
    / "phase153_r8_reference_use_prose_normalization_backup"
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

  patch_file(
    repo
  )
  install_test(
    repo
  )

  print(
    "Phase 153-R8 reference-use prose normalization applied."
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
    "  tests/test_phase153_r8_reference_use_prose_normalization.py"
  )


if __name__ == "__main__":
  main()

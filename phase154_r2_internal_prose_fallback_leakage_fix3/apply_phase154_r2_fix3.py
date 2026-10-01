from pathlib import Path
import shutil

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = (
    REPO_ROOT
    / "toda_group_proof_narrative_contribution_renderer.py"
)
BACKUP = (
    REPO_ROOT
    / "phase154_r2_internal_prose_fallback_leakage_fix3"
    / "backup_before_fix3"
    / TARGET.name
)

FUNCTION = 'def suppress_toda_group_proof_narrative_reference_body_duplicates(\n  body_markdown: str,\n  statement_lines_by_reference_number: dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n) -> str:\n  if not isinstance(\n    body_markdown,\n    str,\n  ):\n    raise TypeError(\n      "body_markdown must be a str"\n    )\n\n  if not isinstance(\n    statement_lines_by_reference_number,\n    dict,\n  ):\n    raise TypeError(\n      "statement_lines_by_reference_number must be a dict"\n    )\n\n  lines = body_markdown.splitlines()\n\n  for reference_number, statement_lines in (\n    statement_lines_by_reference_number.items()\n  ):\n    if (\n      isinstance(\n        reference_number,\n        bool,\n      )\n      or not isinstance(\n        reference_number,\n        int,\n      )\n    ):\n      raise TypeError(\n        "statement_lines_by_reference_number keys "\n        "must be integers"\n      )\n\n    if not isinstance(\n      statement_lines,\n      tuple,\n    ):\n      raise TypeError(\n        "statement_lines_by_reference_number values "\n        "must be tuples"\n      )\n\n    marker = (\n      "[R"\n      + str(\n        reference_number\n      )\n      + "]"\n    )\n\n    for statement_line in statement_lines:\n      if not isinstance(\n        statement_line,\n        str,\n      ):\n        raise TypeError(\n          "statement_lines_by_reference_number values "\n          "must contain only strings"\n        )\n\n      if not statement_line:\n        continue\n\n      updated_lines = []\n\n      for line in lines:\n        if statement_line not in line:\n          updated_lines.append(\n            line\n          )\n          continue\n\n        if line.strip() == statement_line:\n          continue\n\n        if marker in line:\n          updated_lines.append(\n            marker\n            + "を用いる。"\n          )\n          continue\n\n        replaced_line = line.replace(\n          statement_line,\n          marker,\n        )\n\n        if (\n          marker in replaced_line\n          and (\n            replaced_line.rstrip().endswith(\n              marker\n              + "を得る。"\n            )\n            or replaced_line.rstrip().endswith(\n              marker\n              + "を得る."\n            )\n          )\n        ):\n          updated_lines.append(\n            marker\n            + "を用いる。"\n          )\n          continue\n\n        if replaced_line.rstrip().endswith(\n          marker\n        ):\n          updated_lines.append(\n            replaced_line.rstrip()\n            + "を用いる。"\n          )\n          continue\n\n        updated_lines.append(\n          replaced_line\n        )\n\n      lines = updated_lines\n\n  compacted_lines = []\n  previous_blank = False\n\n  for line in lines:\n    is_blank = not line.strip()\n\n    if is_blank and previous_blank:\n      continue\n\n    compacted_lines.append(\n      line\n    )\n    previous_blank = is_blank\n\n  return "\\n".join(\n    compacted_lines\n  ).strip()\n'


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
    marker = (
        "def "
        + name
        + "("
    )
    start = source.find(
        marker
    )

    if start < 0:
        raise RuntimeError(
            "function not found: "
            + name
        )

    next_def = source.find(
        "\ndef ",
        start + len(
            marker
        ),
    )

    if next_def < 0:
        suffix = ""
    else:
        suffix = source[
            next_def + 1:
        ]

    return (
        source[
            :start
        ]
        + replacement.rstrip()
        + "\n\n"
        + suffix
    )


def main() -> int:
    if not TARGET.exists():
        raise RuntimeError(
            "missing production file: "
            + str(
                TARGET
            )
        )

    BACKUP.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    shutil.copy2(
        TARGET,
        BACKUP,
    )

    source = TARGET.read_text(
        encoding="utf-8",
    )
    source = replace_function(
        source,
        "suppress_toda_group_proof_narrative_reference_body_duplicates",
        FUNCTION,
    )
    TARGET.write_text(
        source,
        encoding="utf-8",
    )

    test_source = (
        Path(__file__).resolve().parent
        / "tests"
        / "test_phase154_r2_fix3_reference_marker_completion.py"
    )
    test_target = (
        REPO_ROOT
        / "tests"
        / "test_phase154_r2_fix3_reference_marker_completion.py"
    )
    shutil.copy2(
        test_source,
        test_target,
    )

    print(
        "updated:",
        TARGET.name,
    )
    print(
        "added:",
        test_target.relative_to(
            REPO_ROOT
        ),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )

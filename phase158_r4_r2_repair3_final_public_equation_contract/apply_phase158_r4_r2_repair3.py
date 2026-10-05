
from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
R4_R2_PACKAGE = (
  REPO_ROOT
  / "phase158_r4_r2_equation_numbering_and_prose_repair"
)
R4_R2_BACKUP = (
  R4_R2_PACKAGE
  / "backup_before_apply"
)
BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"


def _backup(
  path: Path,
) -> None:
  relative = path.relative_to(
    REPO_ROOT
  )
  target = (
    BACKUP_DIR
    / relative
  )
  target.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    path,
    target,
  )


def _replace_once(
  path: Path,
  old: str,
  new: str,
) -> None:
  text = path.read_text(
    encoding="utf-8"
  )

  if old not in text:
    raise SystemExit(
      "replacement anchor not found: "
      + str(path)
    )

  path.write_text(
    text.replace(
      old,
      new,
      1,
    ),
    encoding="utf-8",
  )


def main() -> int:
  contribution_path = (
    REPO_ROOT
    / "toda_group_proof_narrative_contribution_renderer.py"
  )
  renderer_path = (
    REPO_ROOT
    / "toda_group_proof_narrative_renderer.py"
  )
  phase158_test_path = (
    REPO_ROOT
    / "tests"
    / "test_phase158_r4_equation_numbering_and_prose.py"
  )

  for path in (
    contribution_path,
    renderer_path,
    phase158_test_path,
  ):
    _backup(
      path
    )

  original_contribution_path = (
    R4_R2_BACKUP
    / "toda_group_proof_narrative_contribution_renderer.py"
  )

  if not original_contribution_path.exists():
    raise SystemExit(
      "R4-R2 contribution-renderer backup was not found: "
      + str(
        original_contribution_path
      )
    )

  shutil.copy2(
    original_contribution_path,
    contribution_path,
  )

  insertion_anchor = '''def _phase158_normalize_public_narrative_contract(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
'''

  helper = r'''def _phase158_public_equation_tag_number(
  line: str,
) -> int | None:
  marker = r"\tag{"
  marker_index = line.find(
    marker
  )

  if marker_index < 0:
    return None

  number_start = (
    marker_index
    + len(
      marker
    )
  )
  number_end = line.find(
    "}",
    number_start,
  )

  if number_end < 0:
    return None

  number_text = line[
    number_start:
    number_end
  ]

  if not number_text.isdigit():
    return None

  return int(
    number_text
  )


def _phase158_public_equation_connector_numbers(
  line: str,
) -> tuple[
  int,
  ...,
] | None:
  stripped = line.strip()
  suffix = "より,"

  if not stripped.endswith(
    suffix
  ):
    return None

  reference_text = stripped[
    :-len(
      suffix
    )
  ].strip()

  if not reference_text:
    return None

  if " と " in reference_text:
    left, right = reference_text.rsplit(
      " と ",
      1,
    )
    pieces = tuple(
      (
        *(
          piece.strip()
          for piece in left.split(
            ","
          )
          if piece.strip()
        ),
        right.strip(),
      )
    )
  else:
    pieces = (
      reference_text,
    )

  numbers = []

  for piece in pieces:
    if (
      not piece.startswith(
        "("
      )
      or not piece.endswith(
        ")"
      )
    ):
      return None

    number_text = piece[
      1:-1
    ]

    if not number_text.isdigit():
      return None

    numbers.append(
      int(
        number_text
      )
    )

  return tuple(
    numbers
  )


def _phase158_render_public_equation_connector(
  numbers: tuple[
    int,
    ...,
  ],
) -> str:
  references = tuple(
    "("
    + str(
      number
    )
    + ")"
    for number in numbers
  )

  if len(
    references
  ) == 1:
    return (
      references[
        0
      ]
      + " より,"
    )

  return (
    ", ".join(
      references[
        :-1
      ]
    )
    + " と "
    + references[
      -1
    ]
    + " より,"
  )


def _phase158_normalize_public_equation_numbers(
  proof_body: list[
    str
  ],
) -> list[
  str
]:
  connector_numbers_by_index = {}
  referenced_numbers = set()

  for index, line in enumerate(
    proof_body
  ):
    numbers = (
      _phase158_public_equation_connector_numbers(
        line
      )
    )

    if numbers is None:
      continue

    connector_numbers_by_index[
      index
    ] = numbers
    referenced_numbers.update(
      numbers
    )

  retained_old_numbers = []
  seen_old_numbers = set()

  for line in proof_body:
    number = (
      _phase158_public_equation_tag_number(
        line
      )
    )

    if (
      number is None
      or number not in referenced_numbers
      or number in seen_old_numbers
    ):
      continue

    retained_old_numbers.append(
      number
    )
    seen_old_numbers.add(
      number
    )

  number_map = {
    old_number: new_number
    for new_number, old_number in enumerate(
      retained_old_numbers,
      start=1,
    )
  }

  result = []
  emitted_old_numbers = set()

  for index, source_line in enumerate(
    proof_body
  ):
    line = source_line
    tag_number = (
      _phase158_public_equation_tag_number(
        line
      )
    )

    if tag_number is not None:
      old_marker = (
        r"\tag{"
        + str(
          tag_number
        )
        + "}"
      )

      if (
        tag_number not in number_map
        or tag_number in emitted_old_numbers
      ):
        line = line.replace(
          old_marker,
          "",
          1,
        )
      else:
        line = line.replace(
          old_marker,
          (
            r"\tag{"
            + str(
              number_map[
                tag_number
              ]
            )
            + "}"
          ),
          1,
        )
        emitted_old_numbers.add(
          tag_number
        )

    connector_numbers = (
      connector_numbers_by_index.get(
        index
      )
    )

    if connector_numbers is not None:
      if all(
        number in number_map
        for number in connector_numbers
      ):
        line = (
          _phase158_render_public_equation_connector(
            tuple(
              number_map[
                number
              ]
              for number in connector_numbers
            )
          )
        )
      else:
        line = (
          "これより,"
          if len(
            connector_numbers
          ) == 1
          else "これらより,"
        )

    result.append(
      line
    )

  return result


''' + insertion_anchor

  _replace_once(
    renderer_path,
    insertion_anchor,
    helper,
  )

  normalization_anchor = '''  proof_body = (
    _phase158_strip_terminal_qed_lines(
      proof_body
    )
  )

  lines = [
'''

  normalization_replacement = '''  proof_body = (
    _phase158_strip_terminal_qed_lines(
      proof_body
    )
  )
  proof_body = (
    _phase158_normalize_public_equation_numbers(
      proof_body
    )
  )

  lines = [
'''

  _replace_once(
    renderer_path,
    normalization_anchor,
    normalization_replacement,
  )

  test_text = phase158_test_path.read_text(
    encoding="utf-8"
  )

  helper_start = test_text.index(
    "def _connector_numbers("
  )
  next_test = test_text.index(
    "\ndef test_phase158_r4_public_equation_tags_are_used_and_compact",
    helper_start,
  )

  new_helper = r'''def _connector_numbers(
  rendered: str,
) -> set[int]:
  result = set()

  for line in rendered.splitlines():
    stripped = line.strip()
    suffix = "より,"

    if not stripped.endswith(
      suffix
    ):
      continue

    reference_text = stripped[
      :-len(
        suffix
      )
    ].strip()

    if " と " in reference_text:
      left, right = reference_text.rsplit(
        " と ",
        1,
      )
      pieces = tuple(
        (
          *(
            piece.strip()
            for piece in left.split(
              ","
            )
            if piece.strip()
          ),
          right.strip(),
        )
      )
    else:
      pieces = (
        reference_text,
      )

    numbers = []

    for piece in pieces:
      if (
        not piece.startswith(
          "("
        )
        or not piece.endswith(
          ")"
        )
      ):
        numbers = []
        break

      number_text = piece[
        1:-1
      ]

      if not number_text.isdigit():
        numbers = []
        break

      numbers.append(
        int(
          number_text
        )
      )

    result.update(
      numbers
    )

  return result

'''

  phase158_test_path.write_text(
    (
      test_text[
        :helper_start
      ]
      + new_helper
      + test_text[
        next_test + 1:
      ]
    ),
    encoding="utf-8",
  )

  print(
    "Phase 158-R4-R2 repair3 applied."
  )
  print(
    "Production changes:"
  )
  print(
    "  restored pre-R4-R2 contribution renderer"
  )
  print(
    "  added final public equation normalization "
    "to toda_group_proof_narrative_renderer.py"
  )
  print(
    "Test changes:"
  )
  print(
    "  tests/test_phase158_r4_equation_numbering_and_prose.py"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

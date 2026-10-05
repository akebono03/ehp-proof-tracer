
from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
PREVIOUS_PACKAGE = (
  REPO_ROOT
  / "phase158_r4_r2_equation_numbering_and_prose_repair"
)
PREVIOUS_BACKUP = (
  PREVIOUS_PACKAGE
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
  equation_path = (
    REPO_ROOT
    / "toda_group_proof_narrative_equation_numbering.py"
  )
  contribution_path = (
    REPO_ROOT
    / "toda_group_proof_narrative_contribution_renderer.py"
  )
  phase144_test_path = (
    REPO_ROOT
    / "tests"
    / "test_phase144_5_generic_definition_order_equations.py"
  )
  repair47_test_path = (
    REPO_ROOT
    / "tests"
    / "test_phase157_r20_repair47_injective_image_order_reason.py"
  )
  phase158_test_path = (
    REPO_ROOT
    / "tests"
    / "test_phase158_r4_equation_numbering_and_prose.py"
  )

  for path in (
    equation_path,
    contribution_path,
    phase144_test_path,
    repair47_test_path,
    phase158_test_path,
  ):
    _backup(
      path
    )

  original_equation_path = (
    PREVIOUS_BACKUP
    / "toda_group_proof_narrative_equation_numbering.py"
  )

  if not original_equation_path.exists():
    raise SystemExit(
      "Previous R4-R2 equation-numbering backup not found: "
      + str(
        original_equation_path
      )
    )

  shutil.copy2(
    original_equation_path,
    equation_path,
  )

  old_normalizer = r'''def normalize_toda_group_proof_narrative_equation_numbers(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )
  referenced_numbers = set()

  for paragraph in paragraphs:
    numbers = (
      _toda_group_proof_narrative_equation_reference_numbers(
        paragraph
      )
    )

    if numbers is None:
      continue

    referenced_numbers.update(
      numbers
    )

  visible_numbers = []

  for paragraph in paragraphs:
    number = (
      _toda_group_proof_narrative_equation_tag_number(
        paragraph
      )
    )

    if (
      number is None
      or number
      not in referenced_numbers
      or number
      in visible_numbers
    ):
      continue

    visible_numbers.append(
      number
    )

  number_map = {
    old_number: new_number
    for new_number, old_number in enumerate(
      visible_numbers,
      start=1,
    )
  }

  normalized_paragraphs = []

  for paragraph in paragraphs:
    tag_number = (
      _toda_group_proof_narrative_equation_tag_number(
        paragraph
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

      if tag_number not in number_map:
        paragraph = paragraph.replace(
          old_marker,
          "",
          1,
        )
      else:
        paragraph = paragraph.replace(
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

    reference_numbers = (
      _toda_group_proof_narrative_equation_reference_numbers(
        paragraph
      )
    )

    if reference_numbers is not None:
      mapped = tuple(
        number_map.get(
          number,
          number,
        )
        for number in reference_numbers
      )

      if len(
        mapped
      ) == 1:
        reference_text = (
          "("
          + str(
            mapped[
              0
            ]
          )
          + ")"
        )
      else:
        reference_text = (
          ", ".join(
            "("
            + str(
              number
            )
            + ")"
            for number in mapped[
              :-1
            ]
          )
          + " と "
          + "("
          + str(
            mapped[
              -1
            ]
          )
          + ")"
        )

      paragraph = (
        reference_text
        + " より, "
      )

    normalized_paragraphs.append(
      paragraph
    )

  return "\n\n".join(
    normalized_paragraphs
  )
'''

  new_normalizer = r'''def normalize_toda_group_proof_narrative_equation_numbers(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )
  referenced_numbers = set()

  for paragraph in paragraphs:
    numbers = (
      _toda_group_proof_narrative_equation_reference_numbers(
        paragraph
      )
    )

    if numbers is None:
      continue

    referenced_numbers.update(
      numbers
    )

  visible_numbers = []

  for paragraph in paragraphs:
    number = (
      _toda_group_proof_narrative_equation_tag_number(
        paragraph
      )
    )

    if (
      number is None
      or number
      not in referenced_numbers
      or number
      in visible_numbers
    ):
      continue

    visible_numbers.append(
      number
    )

  number_map = {
    old_number: new_number
    for new_number, old_number in enumerate(
      visible_numbers,
      start=1,
    )
  }

  normalized_paragraphs = []
  emitted_tag_numbers = set()

  for paragraph in paragraphs:
    tag_number = (
      _toda_group_proof_narrative_equation_tag_number(
        paragraph
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
        or tag_number in emitted_tag_numbers
      ):
        paragraph = paragraph.replace(
          old_marker,
          "",
          1,
        )
      else:
        paragraph = paragraph.replace(
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
        emitted_tag_numbers.add(
          tag_number
        )

    reference_numbers = (
      _toda_group_proof_narrative_equation_reference_numbers(
        paragraph
      )
    )

    if reference_numbers is not None:
      if any(
        number not in number_map
        for number in reference_numbers
      ):
        paragraph = (
          "これより, "
          if len(
            reference_numbers
          ) == 1
          else "これらより, "
        )
      else:
        mapped = tuple(
          number_map[
            number
          ]
          for number in reference_numbers
        )

        if len(
          mapped
        ) == 1:
          reference_text = (
            "("
            + str(
              mapped[
                0
              ]
            )
            + ")"
          )
        else:
          reference_text = (
            ", ".join(
              "("
              + str(
                number
              )
              + ")"
              for number in mapped[
                :-1
              ]
            )
            + " と "
            + "("
            + str(
              mapped[
                -1
              ]
            )
            + ")"
          )

        paragraph = (
          reference_text
          + " より, "
        )

    normalized_paragraphs.append(
      paragraph
    )

  return "\n\n".join(
    normalized_paragraphs
  )
'''

  _replace_once(
    contribution_path,
    old_normalizer,
    new_normalizer,
  )

  phase144_test_path.write_text(
    r'''import inspect

from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_equation_numbering import (
  number_toda_group_proof_narrative_equations,
  toda_group_proof_narrative_equation_reference,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _render_multi_argument(
  n,
  k,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  return (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )


def test_phase144_5_r2_equation_reference_uses_parenthesized_number():
  assert (
    toda_group_proof_narrative_equation_reference(
      7
    )
    == "(7)"
  )


def test_phase144_5_r2_pi6_3_keeps_definition_and_order_purposes():
  rendered = _render_multi_argument(
    3,
    3,
  )

  assert r"$\nu'$ を定める." in rendered
  assert (
    r"$\nu'$ の位数を決定するために, "
    r"次の完全列を考える."
    in rendered
  )


def test_phase144_5_r2_numbering_has_no_target_hardcoding():
  source = inspect.getsource(
    number_toda_group_proof_narrative_equations
  )

  forbidden_fragments = (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
''',
    encoding="utf-8",
  )

  old_repair47_test = r'''def test_phase157_r20_repair47_public_narrative_places_reason_before_eta_order():
  (
    raw,
    presentation,
    reason_sidecar,
  ) = _repair47_data()

  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  body = rendered.split(
    "\n## 証明\n",
    1,
  )[1]

  reason_text = (
    r"$\pi_{5}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$ "
    "と $E$ の単射性より, "
    r"$E(\eta_{2}^{3})="
    r"\eta_{3}^{3}\neq0$ であり, "
    "単射写像は元の位数を保つ."
  )
  order_text = (
    r"$\operatorname{ord}"
    r"\left(\eta_{3}^{3}\right) = 2$."
  )

  assert reason_text in body
  assert order_text in body
  assert body.index(
    reason_text
  ) < body.index(
    order_text
  )
'''

  new_repair47_test = r'''def test_phase157_r20_repair47_public_narrative_places_reason_before_eta_order():
  (
    raw,
    presentation,
    reason_sidecar,
  ) = _repair47_data()

  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  body = rendered.split(
    "\n## 証明\n",
    1,
  )[1]

  reason_tail = (
    r"$E(\eta_{2}^{3})="
    r"\eta_{3}^{3}\neq0$ であり, "
    "単射写像は元の位数を保つ."
  )
  order_text = (
    r"$\operatorname{ord}"
    r"\left(\eta_{3}^{3}\right) = 2$."
  )

  assert "この群構造と" not in body
  assert reason_tail in body
  assert order_text in body
  assert body.index(
    reason_tail
  ) < body.index(
    order_text
  )
'''

  _replace_once(
    repair47_test_path,
    old_repair47_test,
    new_repair47_test,
  )

  old_phase158_test = r'''def test_phase158_r4_pi6_has_no_ambiguous_group_structure_anaphora():
  rendered = _render(
    3,
    3,
  )

  assert (
    "この群構造と"
    not in rendered
  )
  assert (
    r"$\pi_{5}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$ "
    "と $E$ の単射性より"
    in rendered
  )
'''

  new_phase158_test = r'''def test_phase158_r4_pi6_has_no_ambiguous_group_structure_anaphora():
  rendered = _render(
    3,
    3,
  )

  assert (
    "この群構造と"
    not in rendered
  )
  assert (
    r"$E(\eta_{2}^{3})="
    r"\eta_{3}^{3}\neq0$"
    in rendered
  )
  assert (
    "単射写像は元の位数を保つ."
    in rendered
  )
'''

  _replace_once(
    phase158_test_path,
    old_phase158_test,
    new_phase158_test,
  )

  print(
    "Phase 158-R4-R2 repair1 applied."
  )
  print(
    "Production changes:"
  )
  print(
    "  restored toda_group_proof_narrative_equation_numbering.py"
  )
  print(
    "  refined public equation normalization in "
    "toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "Test changes:"
  )
  print(
    "  tests/test_phase144_5_generic_definition_order_equations.py"
  )
  print(
    "  tests/test_phase157_r20_repair47_injective_image_order_reason.py"
  )
  print(
    "  tests/test_phase158_r4_equation_numbering_and_prose.py"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

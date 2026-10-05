
from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"


def _backup(path: Path) -> None:
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

  text = text.replace(
    old,
    new,
    1,
  )
  path.write_text(
    text,
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
  reason_path = (
    REPO_ROOT
    / "toda_group_proof_narrative_reason_renderer.py"
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
  reason_vocab_test_path = (
    REPO_ROOT
    / "tests"
    / "test_phase150_rc4_7d_generic_reason_vocabulary.py"
  )
  public_route_test_path = (
    REPO_ROOT
    / "tests"
    / "test_phase150_rc4_7d_3_public_narrative_generic_route.py"
  )
  new_test_path = (
    REPO_ROOT
    / "tests"
    / "test_phase158_r4_equation_numbering_and_prose.py"
  )

  for path in (
    equation_path,
    contribution_path,
    reason_path,
    phase144_test_path,
    repair47_test_path,
    reason_vocab_test_path,
    public_route_test_path,
  ):
    _backup(
      path
    )

  _replace_once(
    equation_path,
    '''from proof import (
  ProofStep,
)
''',
    '''from proof import (
  ProofStep,
  Relation,
  RelationType,
)
''',
  )

  _replace_once(
    equation_path,
    '''def _numbered_step_line(
  proof_step: ProofStep,
  equation_number: int,
) -> str:
''',
    '''def _is_toda_group_proof_narrative_equation_numbering_source(
  source_step: ProofStep,
  target_step: ProofStep,
) -> bool:
  source_rendered = (
    _render_generic_narrative_step(
      source_step
    )
  )
  target_rendered = (
    _render_generic_narrative_step(
      target_step
    )
  )

  if (
    source_rendered
    and source_rendered
    == target_rendered
  ):
    return False

  conclusion = (
    source_step.conclusion
  )

  if (
    isinstance(
      conclusion,
      Relation,
    )
    and conclusion.relation_type
    is RelationType.EQUALITY
    and conclusion.lhs
    == conclusion.rhs
  ):
    return False

  return True


def _numbered_step_line(
  proof_step: ProofStep,
  equation_number: int,
) -> str:
''',
  )

  _replace_once(
    equation_path,
    '''  for transition in transitions:
    target_id = id(transition.target_step)
    current = sources_by_target.get(
      target_id,
      (),
    )
''',
    '''  for transition in transitions:
    if not (
      _is_toda_group_proof_narrative_equation_numbering_source(
        transition.source_step,
        transition.target_step,
      )
    ):
      continue

    target_id = id(transition.target_step)
    current = sources_by_target.get(
      target_id,
      (),
    )
''',
  )

  marker = '''def order_toda_group_proof_narrative_order_support(
  presentation: TodaGroupProofPresentation,
  markdown: str,
) -> str:
'''
  helper = r'''def _toda_group_proof_narrative_equation_reference_numbers(
  paragraph: str,
) -> tuple[
  int,
  ...,
] | None:
  stripped = paragraph.strip()

  if (
    not stripped.startswith(
      "("
    )
    or "より," not in stripped
  ):
    return None

  reference_text, suffix = (
    stripped.split(
      "より,",
      1,
    )
  )

  if suffix.strip():
    return None

  normalized = (
    reference_text
    .strip()
    .replace(
      " と ",
      ", ",
    )
  )
  pieces = tuple(
    piece.strip()
    for piece in normalized.split(
      ","
    )
    if piece.strip()
  )

  if not pieces:
    return None

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


def normalize_toda_group_proof_narrative_equation_numbers(
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


''' + marker

  _replace_once(
    contribution_path,
    marker,
    helper,
  )

  _replace_once(
    contribution_path,
    '''  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
''',
    '''  rendered = (
    normalize_toda_group_proof_narrative_equation_numbers(
      rendered
    )
  )

  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
''',
  )

  _replace_once(
    reason_path,
    '''    return (
      "この群構造と $E$ の単射性より, "
      f"$E({source_generator_latex})"
      f"={target_latex}\\\\neq0$ であり, "
      "単射写像は元の位数を保つ.\\n"
      "したがって, "
    )
''',
    '''    group_structure = (
      _render_generic_narrative_step(
        reason.premise_steps[
          0
        ]
      )
    )

    return (
      f"{group_structure} と $E$ の単射性より, "
      f"$E({source_generator_latex})"
      f"={target_latex}\\\\neq0$ であり, "
      "単射写像は元の位数を保つ.\\n"
      "したがって, "
    )
''',
  )

  _replace_once(
    reason_path,
    '''  if reason.kind is TodaGroupProofNarrativeReasonKind.GROUP_ORDER_DERIVATION:
    return (
      "この群構造と写像による移送の結果を合わせると, "
      "対象の群の位数と写像の単射性が決まる.\\nしたがって, "
    )
''',
    '''  if reason.kind is TodaGroupProofNarrativeReasonKind.GROUP_ORDER_DERIVATION:
    return (
      "群構造に関する結果と写像による移送の結果を合わせると, "
      "対象の群の位数と写像の単射性が決まる.\\nしたがって, "
    )
''',
  )

  phase144_replacement = r'''import inspect
import re

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


def test_phase144_5_r2_render_equivalent_transitions_are_not_numbered():
  rendered = _render_multi_argument(
    3,
    3,
  )

  assert (
    r"$2\nu' = \eta_{3}^{3}\tag{"
    not in rendered
  )
  assert (
    r"$H\left(\nu'\right) = \eta_{5}\tag{"
    not in rendered
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


def test_phase144_5_r2_reflexive_support_equations_are_not_numbered():
  rendered = _render_multi_argument(
    3,
    3,
  )

  assert (
    r"$\eta_{3}^{3} = \eta_{3}^{3}\tag{"
    not in rendered
  )
  assert (
    r"$\eta_{5} = \eta_{5}\tag{"
    not in rendered
  )


def test_phase144_5_r2_pi6_3_has_no_duplicate_equation_tags():
  rendered = _render_multi_argument(
    3,
    3,
  )

  tags = tuple(
    int(
      value
    )
    for value in re.findall(
      r"\\tag\{(\d+)\}",
      rendered,
    )
  )

  assert len(
    tags
  ) == len(
    set(
      tags
    )
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
'''
  phase144_test_path.write_text(
    phase144_replacement,
    encoding="utf-8",
  )

  _replace_once(
    repair47_test_path,
    '''  reason_text = (
    "この群構造と $E$ の単射性より, "
    r"$E(\\eta_{2}^{3})="
    r"\\eta_{3}^{3}\\neq0$ であり, "
    "単射写像は元の位数を保つ."
  )
''',
    '''  reason_text = (
    r"$\\pi_{5}^{2} = "
    r"\\mathbb{Z}/2\\{\\eta_{2}\\eta_{3}\\eta_{4}\\}$ "
    "と $E$ の単射性より, "
    r"$E(\\eta_{2}^{3})="
    r"\\eta_{3}^{3}\\neq0$ であり, "
    "単射写像は元の位数を保つ."
  )
''',
  )

  _replace_once(
    reason_vocab_test_path,
    '''def test_phase150_rc4_7d_pi16_order_and_final_reasons():
 r,m=_data(9,7); k={x.kind for x in r.reasons}; assert TodaGroupProofNarrativeReasonKind.GROUP_ORDER_DERIVATION in k; assert TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION in k; assert 'この群構造と写像による移送の結果を合わせると' in m
''',
    '''def test_phase150_rc4_7d_pi16_order_and_final_reasons():
 r,m=_data(9,7); k={x.kind for x in r.reasons}; assert TodaGroupProofNarrativeReasonKind.GROUP_ORDER_DERIVATION in k; assert TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION in k; assert '群構造に関する結果と写像による移送の結果を合わせると' in m
''',
  )

  _replace_once(
    public_route_test_path,
    '''  phrase = (
    "この群構造と写像による移送の結果を合わせると"
  )
''',
    '''  phrase = (
    "群構造に関する結果と写像による移送の結果を合わせると"
  )
''',
  )

  new_test_path.write_text(
    (
      PACKAGE_DIR
      / "test_phase158_r4_equation_numbering_and_prose.py"
    ).read_text(
      encoding="utf-8"
    ),
    encoding="utf-8",
  )

  print(
    "Phase 158-R4-R2 applied."
  )
  print(
    "Production code:"
  )
  print(
    "  toda_group_proof_narrative_equation_numbering.py"
  )
  print(
    "  toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "  toda_group_proof_narrative_reason_renderer.py"
  )
  print(
    "Existing tests:"
  )
  print(
    "  tests/test_phase144_5_generic_definition_order_equations.py"
  )
  print(
    "  tests/test_phase157_r20_repair47_injective_image_order_reason.py"
  )
  print(
    "  tests/test_phase150_rc4_7d_generic_reason_vocabulary.py"
  )
  print(
    "  tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py"
  )
  print(
    "New test:"
  )
  print(
    "  tests/test_phase158_r4_equation_numbering_and_prose.py"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

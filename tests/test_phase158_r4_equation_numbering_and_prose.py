import re

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TAG_RE = re.compile(
  r"\\tag\{(\d+)\}"
)


def _render(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def _tag_numbers(
  rendered: str,
) -> tuple[
  int,
  ...,
]:
  return tuple(
    int(
      value
    )
    for value in TAG_RE.findall(
      rendered
    )
  )


def _connector_numbers(
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

def test_phase158_r4_public_equation_tags_are_used_and_compact():
  for n, k in (
    (3, 3),
    (5, 3),
  ):
    rendered = _render(
      n,
      k,
    )
    tags = _tag_numbers(
      rendered
    )
    references = _connector_numbers(
      rendered
    )

    assert len(
      tags
    ) == len(
      set(
        tags
      )
    )
    assert set(
      tags
    ) == references
    assert tags == tuple(
      range(
        1,
        len(
          tags
        )
        + 1,
      )
    )


def test_phase158_r4_pi6_has_no_ambiguous_group_structure_anaphora():
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


def test_phase158_r4_pi16_has_no_ambiguous_group_structure_anaphora():
  rendered = _render(
    9,
    7,
  )

  assert (
    "この群構造と"
    not in rendered
  )
  assert (
    "群構造に関する結果と"
    "写像による移送の結果を合わせると"
    in rendered
  )

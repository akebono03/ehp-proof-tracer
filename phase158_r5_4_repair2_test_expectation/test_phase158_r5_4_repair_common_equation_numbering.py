import re

import pytest

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)


def _render_multi_argument(
  n: int,
  k: int,
) -> str:
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


def _tag_lines(
  markdown: str,
):
  tags = {}

  for line_number, line in enumerate(
    markdown.splitlines(),
    start=1,
  ):
    for match in re.finditer(
      r"\\tag\{(\d+)\}",
      line,
    ):
      tags[
        int(
          match.group(
            1
          )
        )
      ] = line_number

  return tags


def _reference_lines(
  markdown: str,
):
  references = {}

  for line_number, line in enumerate(
    markdown.splitlines(),
    start=1,
  ):
    line_without_tags = re.sub(
      r"\\tag\{\d+\}",
      "",
      line,
    )

    if "より" not in line_without_tags:
      continue

    for match in re.finditer(
      r"\((\d+)\)",
      line_without_tags,
    ):
      references.setdefault(
        int(
          match.group(
            1
          )
        ),
        [],
      ).append(
        line_number
      )

  return references


@pytest.mark.parametrize(
  "n,k",
  (
    (3, 3),
    (5, 3),
    (8, 7),
    (4, 6),
    (5, 7),
    (9, 7),
  ),
)
def test_phase158_r5_4_repair_numbers_only_equations_referenced_later(
  n,
  k,
):
  rendered = _render_multi_argument(
    n,
    k,
  )
  tags = _tag_lines(
    rendered
  )
  references = _reference_lines(
    rendered
  )

  assert set(
    tags
  ) == set(
    references
  )

  for number, tag_line in tags.items():
    assert all(
      tag_line < reference_line
      for reference_line in references[
        number
      ]
    )


def test_phase158_r5_4_repair_pi8_5_does_not_create_forward_equation_references(
):
  rendered = _render_multi_argument(
    5,
    3,
  )

  assert r"\tag{" not in rendered
  assert "(1) より, " not in rendered
  assert "(2) より, " not in rendered

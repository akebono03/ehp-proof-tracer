import re

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _data(
  depth: int,
):
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=depth,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  semantic_sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=semantic_sidecar,
  )
  return (
    raw,
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
  )


def test_phase156_r5_repair11_raw_graph_keeps_proposition51_reference():
  (
    raw,
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
  ) = _data(
    2
  )
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  locators = {
    entry.reference.locator
    for entry in entries
  }

  assert "Proposition 5.1" in locators


def test_phase156_r5_repair11_public_pi6_keeps_current_proof_required_references_depth2():
  (
    raw,
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
  ) = _data(
    2
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  headers = re.findall(
    r"\*\*\[R\d+\] ([^\n]+?)\.\*\*",
    rendered,
  )

  assert headers == [
    "Proposition 5.6",
    "(5.3)",
    "Proposition 5.3",
    "Proposition 5.1",
    "Proposition 2.2",
  ]


def test_phase156_r5_repair11_public_pi6_keeps_current_proof_required_references_depth3():
  raw = _data(
    3
  )[
    0
  ]
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  headers = re.findall(
    r"\*\*\[R\d+\] ([^\n]+?)\.\*\*",
    rendered,
  )

  for required in (
    "Proposition 5.6",
    "(5.3)",
    "Proposition 5.3",
    "Proposition 5.1",
    "Proposition 2.2",
  ):
    assert required in headers

  assert "Lemma 5.2" not in rendered


def test_phase156_r5_repair11_reference_numbers_are_compact_after_pruning():
  raw = _data(
    2
  )[
    0
  ]
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  numbers = [
    int(
      number
    )
    for number in re.findall(
      r"\*\*\[R(\d+)\] ",
      rendered,
    )
  ]

  assert numbers == list(
    range(
      1,
      len(
        numbers
      )
      + 1,
    )
  )

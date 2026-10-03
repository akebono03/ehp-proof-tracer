import re

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_frontier_step_ids,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
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
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  empty_lines = {
    entry.number: ()
    for entry in entries
  }
  entries, _ = exclude_toda_group_proof_narrative_root_reference(
    entries,
    empty_lines,
    presentation.root_step,
  )
  return (
    raw,
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    entries,
  )


def test_phase156_r5_repair12_proposition51_is_not_on_reference_frontier():
  (
    raw,
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    entries,
  ) = _data(
    2
  )
  frontier_step_ids = (
    _toda_group_proof_narrative_reference_frontier_step_ids(
      presentation,
      entries,
    )
  )
  prop51 = next(
    entry
    for entry in entries
    if entry.reference.locator == "Proposition 5.1"
  )

  assert all(
    id(
      proof_step
    )
    not in frontier_step_ids
    for proof_step in prop51.proof_steps
  )


def test_phase156_r5_repair12_53_and_direct_parent_references_are_on_frontier():
  (
    raw,
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    entries,
  ) = _data(
    2
  )
  frontier_step_ids = (
    _toda_group_proof_narrative_reference_frontier_step_ids(
      presentation,
      entries,
    )
  )

  frontier_locators = {
    entry.reference.locator
    for entry in entries
    if any(
      id(
        proof_step
      )
      in frontier_step_ids
      for proof_step in entry.proof_steps
    )
  }

  assert "(5.3)" in frontier_locators
  assert "Proposition 5.3" in frontier_locators
  assert "Lemma 5.4" in frontier_locators
  assert "(5.2)" in frontier_locators
  assert "Proposition 5.1" not in frontier_locators


def test_phase156_r5_repair12_public_depth2_reference_headers_are_frontier_only():
  (
    raw,
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    entries,
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
    "(5.3)",
    "Proposition 5.3",
    "Lemma 5.4",
    "(5.2)",
  ]


def test_phase156_r5_repair12_public_depth3_prunes_proposition51():
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

  assert "Proposition 5.1" not in headers
  assert "(5.3)" in headers
  assert "Proposition 5.3" in headers
  assert "Lemma 5.4" in headers
  assert "(5.2)" in headers

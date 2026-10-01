from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _phase154_r5_reference_source_steps_by_number,
  _phase154_r5_unique_visible_non_root_consumer_line,
  link_toda_group_proof_narrative_reference_body_consumers,
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
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _raw_presentation(
  n: int,
  k: int,
):
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
  return build_toda_group_proof_presentation(
    replay
  )


def _render_group(
  n: int,
  k: int,
) -> str:
  return render_toda_group_proof_narrative_markdown(
    _raw_presentation(
      n,
      k,
    )
  )


def test_phase154_r5_fix1_repair1_pi11_4_links_prop44_reference_to_consumer():
  rendered = _render_group(
    4,
    7,
  )

  assert (
    r"[R2]より, $\nu_{4}$ の分解写像は同型写像である."
    in rendered
  )
  assert "まず, [R2]を用いる." not in rendered
  assert (
    r"このことから, $\nu_{4}$ の分解写像は同型写像である."
    not in rendered
  )


def test_phase154_r5_fix1_repair1_consumer_is_unique_and_non_root():
  raw_presentation = _raw_presentation(
    4,
    7,
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
    )
  )
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  statement_lines = {
    entry.number: tuple(
      ()
    )
    for entry in entries
  }
  entries, _ = (
    exclude_toda_group_proof_narrative_root_reference(
      entries,
      statement_lines,
      presentation.root_step,
    )
  )
  sources = (
    _phase154_r5_reference_source_steps_by_number(
      presentation,
      entries,
    )
  )
  body = (
    "まず, [R3]を用いる。\n"
    r"このことから, $\nu_{4}$ の分解写像は同型写像である."
    "\n"
    r"$\pi_{11}^{4} = 0$"
  )

  assert (
    _phase154_r5_unique_visible_non_root_consumer_line(
      presentation,
      sources[3],
      body,
    )
    == r"$\nu_{4}$ の分解写像は同型写像である."
  )


def test_phase154_r5_fix1_repair1_keeps_root_only_reference_neutral():
  rendered = _render_group(
    4,
    7,
  )

  assert "[R1]を用いる." in rendered
  assert r"[R1]より, $\pi_{11}^{4} = 0" not in rendered


def test_phase154_r5_fix1_repair1_does_not_duplicate_consumer_fact():
  rendered = _render_group(
    4,
    7,
  )
  consumer = (
    r"$\nu_{4}$ の分解写像は同型写像である."
  )

  assert rendered.count(
    consumer
  ) == 1


def test_phase154_r5_fix1_repair1_preserves_final_conclusion():
  rendered = _render_group(
    4,
    7,
  )

  assert r"\pi_{11}^{4} = 0" in rendered

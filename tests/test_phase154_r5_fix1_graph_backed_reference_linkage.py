from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  link_toda_group_proof_narrative_reference_body_consumers,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
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


def _presentation(
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
    _presentation(
      n,
      k,
    )
  )


def test_phase154_r5_fix1_pi11_4_links_prop44_reference_to_visible_consumer():
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
  assert r"\pi_{11}^{4} = 0" in rendered


def test_phase154_r5_fix1_pi11_4_keeps_root_only_reference_neutral():
  rendered = _render_group(
    4,
    7,
  )

  assert "[R1]を用いる." in rendered
  assert r"[R1]より, $\pi_{11}^{4} = 0" not in rendered


def test_phase154_r5_fix1_does_not_duplicate_linked_consumer_fact():
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


def test_phase154_r5_fix1_linkage_helper_keeps_ambiguous_or_missing_marker_body():
  raw_presentation = _presentation(
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
  body = (
    "参照記号を含まない本文.\n"
    r"$\nu_{4}$ の分解写像は同型写像である."
  )

  assert (
    link_toda_group_proof_narrative_reference_body_consumers(
      presentation,
      body,
      entries,
    )
    == body
  )


def test_phase154_r5_fix1_keeps_r2_internal_fallback_repairs():
  pi10_4 = _render_group(
    4,
    6,
  )
  pi11_4 = _render_group(
    4,
    7,
  )

  assert (
    "Toda (5.6) nu_4 decomposition integration"
    not in pi10_4
  )
  assert r"\text{ is injective}" not in pi11_4
  assert r"\text{ is exact}" not in pi11_4
  assert "である.を用いる." not in pi11_4

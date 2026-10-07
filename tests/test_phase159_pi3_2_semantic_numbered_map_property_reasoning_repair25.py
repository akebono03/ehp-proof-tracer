from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _generic_group_map_name,
)
from toda_group_proof_narrative_renderer import (
  _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning,
  _phase159_recursive_map_property_triples,
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
  TodaGroupProofNarrativeReasonKind,
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


def test_phase159_repair25_pi3_2_exactness_reason_uses_semantic_map_name():
  presentation = _presentation(
    2,
    1,
  )
  semantic_presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      semantic_presentation
    )
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      semantic_presentation,
      semantic_sidecar,
    )
  )

  hopf_exactness_reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
      and _generic_group_map_name(
        getattr(
          reason.conclusion_step.conclusion,
          "map",
          None,
        )
      )
      == "H"
    )
  )

  assert len(
    hopf_exactness_reasons
  ) == 2


def test_phase159_repair25_pi11_6_recursive_semantic_triple_exists():
  presentation = _presentation(
    6,
    5,
  )
  triples = (
    _phase159_recursive_map_property_triples(
      presentation
    )
  )

  hopf_triples = tuple(
    triple
    for triple in triples
    if (
      _generic_group_map_name(
        getattr(
          triple[
            2
          ].conclusion,
          "map",
          None,
        )
      )
      == "H"
      and getattr(
        getattr(
          triple[
            2
          ].conclusion,
          "map",
          None,
        ),
        "source_group",
        None,
      )
      is not None
    )
  )

  assert hopf_triples


def test_phase159_repair25_pi11_6_keeps_numbered_reasoning_without_prose_matching():
  presentation = _presentation(
    6,
    5,
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  assert (
    "\\[\n"
    r"H: \pi_{7}^{3} \to \pi_{7}^{5}"
    r"\quad\text{は単射}. \qquad (1)"
    "\n\\]"
    in rendered
  )
  assert (
    "\\[\n"
    r"H: \pi_{7}^{3} \to \pi_{7}^{5}"
    r"\quad\text{は全射}. \qquad (2)"
    "\n\\]"
    in rendered
  )
  assert (
    r"(1), (2) より, "
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は同型."
    in rendered
  )


def test_phase159_repair25_text_only_helper_still_refuses_semantic_inference():
  rendered = (
    "# Group proof narrative\n\n"
    "## 証明\n\n"
    "$F: A \\to B$ は単射.\n"
    "$F: A \\to B$ は全射.\n"
    "$F: A \\to B$ は同型.\n\n"
    "□\n"
  )

  normalized = (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      rendered
    )
  )

  assert normalized == rendered

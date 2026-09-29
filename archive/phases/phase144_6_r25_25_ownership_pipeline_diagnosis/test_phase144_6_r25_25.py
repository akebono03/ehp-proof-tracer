from phase144_6_r25_25_ownership_pipeline_diagnosis.audit_phase144_6_r25_25 import (
  TARGETS,
  _data,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)


def test_phase144_6_r25_25_r25_24_experiment_is_rolled_back():
  import toda_group_proof_narrative_method_evidence as method_evidence
  import toda_group_proof_narrative_argument_multi_renderer as multi_renderer

  method_source = (
    method_evidence
    .extract_toda_group_proof_narrative_argument_method_evidence
    .__code__
  )

  assert (
    "minimal_ownership"
    not in method_source.co_varnames
  )
  assert (
    "minimal_ownership"
    not in open(
      multi_renderer.__file__,
      encoding="utf-8",
    ).read()
  )


def test_phase144_6_r25_25_six_group_pipeline_constructs():
  for n, k in TARGETS:
    (
      presentation,
      blocks,
      sidecar,
      arguments,
    ) = _data(
      n,
      k,
    )

    base_markdown = (
      render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
      )
    )
    proof_chains = (
      build_toda_group_proof_narrative_proof_chains(
        presentation,
        sidecar,
        arguments,
      )
    )
    ordered = (
      build_toda_group_proof_narrative_ordered_contributions(
        presentation,
        blocks,
        sidecar,
        arguments,
        proof_chains,
        current_markdown=base_markdown,
      )
    )

    assert isinstance(
      base_markdown,
      str,
    )
    assert len(
      ordered
    ) == len(
      arguments
    )

import pytest

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def _complete_data(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = (
    build_complete_toda_group_result_proof_replay(
      group_result
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=sidecar,
    )
  )
  return (
    presentation,
    blocks,
    sidecar,
    arguments,
  )


@pytest.mark.parametrize(
  "n,k",
  TARGETS,
)
def test_phase144_6_r25_24_minimal_evidence_is_subset_of_legacy_evidence(
  n,
  k,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _complete_data(
    n,
    k,
  )

  for argument_index in range(
    len(
      arguments
    )
  ):
    legacy = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    minimal = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
        minimal_ownership=True,
      )
    )

    assert all(
      block in legacy
      for block in minimal
    )


def test_phase144_6_r25_24_complete_replay_has_strict_evidence_reduction():
  strict_reduction_found = False

  for n, k in TARGETS:
    (
      presentation,
      blocks,
      sidecar,
      arguments,
    ) = _complete_data(
      n,
      k,
    )

    for argument_index in range(
      len(
        arguments
      )
    ):
      legacy = (
        extract_toda_group_proof_narrative_argument_method_evidence(
          presentation,
          blocks,
          sidecar,
          arguments,
          argument_index,
        )
      )
      minimal = (
        extract_toda_group_proof_narrative_argument_method_evidence(
          presentation,
          blocks,
          sidecar,
          arguments,
          argument_index,
          minimal_ownership=True,
        )
      )
      if len(
        minimal
      ) < len(
        legacy
      ):
        strict_reduction_found = True
        break

    if strict_reduction_found:
      break

  assert strict_reduction_found


def test_phase144_6_r25_24_legacy_default_is_unchanged():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _complete_data(
    3,
    3,
  )

  default = (
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      sidecar,
      arguments,
      0,
    )
  )
  explicit_legacy = (
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      sidecar,
      arguments,
      0,
      minimal_ownership=False,
    )
  )

  assert default == explicit_legacy


def test_phase144_6_r25_24_rejects_non_boolean_minimal_ownership():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _complete_data(
    3,
    3,
  )

  with pytest.raises(
    TypeError,
    match="minimal_ownership must be a boolean",
  ):
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      sidecar,
      arguments,
      0,
      minimal_ownership=1,
    )


def test_phase144_6_r25_24_generic_narrative_still_reaches_pi6_conclusion():
  (
    presentation,
    _blocks,
    _sidecar,
    _arguments,
  ) = _complete_data(
    3,
    3,
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert (
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    in rendered
  )
  assert "(1) と (2) より、" in rendered


def test_phase144_6_r25_24_minimal_evidence_contains_only_exactness_blocks():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _complete_data(
    3,
    3,
  )

  for argument_index in range(
    len(
      arguments
    )
  ):
    minimal = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
        minimal_ownership=True,
      )
    )

    assert all(
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
      for block in minimal
    )

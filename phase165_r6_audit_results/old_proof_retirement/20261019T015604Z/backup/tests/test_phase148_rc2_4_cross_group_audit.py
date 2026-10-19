import pytest

from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_display_contributions import (
  extract_toda_group_proof_narrative_exactness_display_contributions,
)
from toda_group_proof_narrative_exactness_exposure import (
  TodaGroupProofNarrativeExactnessExposureClass,
  classify_toda_group_proof_narrative_exactness_component_exposure,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


CASES = (
  ("pi_6^3", 3, 3),
  ("pi_8^5", 5, 3),
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _case_data(
  n,
  k,
):
  presentation, blocks, sidecar, arguments = (
    _method_evidence_data(
      n,
      k,
    )
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  records = []

  for argument_index, argument in enumerate(
    arguments
  ):
    evidence = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    components = (
      build_toda_group_proof_narrative_exactness_method_components(
        evidence
      )
    )
    relevant_groups = (
      extract_toda_group_proof_narrative_argument_relevant_groups(
        presentation,
        blocks,
        argument,
      )
    )

    for component in components:
      exposure = (
        classify_toda_group_proof_narrative_exactness_component_exposure(
          relevant_groups,
          components,
          component,
        )
      )
      latex_values = tuple(
        contribution.latex
        for block in component.evidence_blocks
        for contribution in (
          extract_toda_group_proof_narrative_exactness_display_contributions(
            presentation,
            block,
          )
        )
      )
      records.append(
        (
          argument.role,
          exposure,
          component,
          latex_values,
        )
      )

  return (
    presentation,
    blocks,
    sidecar,
    arguments,
    rendered,
    tuple(
      records
    ),
  )


@pytest.mark.parametrize(
  "_label,n,k",
  CASES,
)
def test_phase148_rc2_4_all_component_evidence_remains_retrievable(
  _label,
  n,
  k,
):
  (
    _presentation,
    _blocks,
    _sidecar,
    _arguments,
    _rendered,
    records,
  ) = _case_data(
    n,
    k,
  )

  for (
    _role,
    _exposure,
    component,
    latex_values,
  ) in records:
    assert component.evidence_blocks
    assert latex_values


@pytest.mark.parametrize(
  "_label,n,k",
  CASES,
)
def test_phase148_rc2_4_unowned_recursive_contributions_are_not_visible(
  _label,
  n,
  k,
):
  (
    _presentation,
    _blocks,
    _sidecar,
    _arguments,
    rendered,
    records,
  ) = _case_data(
    n,
    k,
  )

  for (
    _role,
    exposure,
    _component,
    latex_values,
  ) in records:
    if (
      exposure
      is not TodaGroupProofNarrativeExactnessExposureClass
      .UNOWNED_RECURSIVE
    ):
      continue

    for latex in latex_values:
      assert latex not in rendered


def test_phase148_rc2_4_pi6_3_owned_short_exact_sequence_remains_visible():
  (
    _presentation,
    _blocks,
    _sidecar,
    _arguments,
    rendered,
    records,
  ) = _case_data(
    3,
    3,
  )

  assert any(
    exposure
    is TodaGroupProofNarrativeExactnessExposureClass
    .OWNED_PRIMARY
    for (
      _role,
      exposure,
      _component,
      _latex_values,
    ) in records
  )
  assert (
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
    in rendered
  )


def test_phase148_rc2_4_pi12_5_owned_component_still_exists():
  (
    _presentation,
    _blocks,
    _sidecar,
    _arguments,
    _rendered,
    records,
  ) = _case_data(
    5,
    7,
  )

  assert any(
    exposure
    is TodaGroupProofNarrativeExactnessExposureClass
    .OWNED_PRIMARY
    for (
      _role,
      exposure,
      _component,
      _latex_values,
    ) in records
  )


def test_phase148_rc2_4_pi15_8_has_no_exactness_component():
  (
    _presentation,
    _blocks,
    _sidecar,
    _arguments,
    _rendered,
    records,
  ) = _case_data(
    8,
    7,
  )

  assert records == ()


def test_phase148_rc2_4_no_sample_has_ambiguous_relevant_component():
  for _label, n, k in CASES:
    (
      _presentation,
      _blocks,
      _sidecar,
      _arguments,
      _rendered,
      records,
    ) = _case_data(
      n,
      k,
    )

    assert all(
      exposure
      is not TodaGroupProofNarrativeExactnessExposureClass
      .AMBIGUOUS_RELEVANT
      for (
        _role,
        exposure,
        _component,
        _latex_values,
      ) in records
    )

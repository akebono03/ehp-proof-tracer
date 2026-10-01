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
          exposure,
          latex_values,
        )
      )

  return rendered, tuple(records)


def test_phase149_rc3_3_pi6_3_short_exact_sequence_precedes_group_conclusion():
  rendered, _records = _case_data(
    3,
    3,
  )
  short_exact = (
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
  )
  group_conclusion = (
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
  )

  assert short_exact in rendered
  assert group_conclusion in rendered
  assert (
    rendered.index(
      short_exact
    )
    < rendered.index(
      group_conclusion
    )
  )


@pytest.mark.parametrize(
  "_label,n,k",
  CASES,
)
def test_phase149_rc3_3_unowned_recursive_exactness_remains_hidden(
  _label,
  n,
  k,
):
  rendered, records = _case_data(
    n,
    k,
  )

  for exposure, latex_values in records:
    if (
      exposure
      is not TodaGroupProofNarrativeExactnessExposureClass
      .UNOWNED_RECURSIVE
    ):
      continue

    for latex in latex_values:
      assert latex not in rendered


def test_phase149_rc3_3_pi6_3_calculation_chain_remains_numbered():
  rendered, _records = _case_data(
    3,
    3,
  )

  assert r"\tag{1}" in rendered
  assert r"\tag{2}" in rendered
  assert r"\tag{3}" in rendered
  assert "(1) と (2) より、" in rendered

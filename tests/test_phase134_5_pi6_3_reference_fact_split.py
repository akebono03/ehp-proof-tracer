from pathlib import Path
import sys

TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
  sys.path.insert(
    0,
    str(TESTS_DIR),
  )

from test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


def _phase144_6_pi6_3_renderings():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  expected = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  actual = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  return (
    expected,
    actual,
  )


def test_phase144_6_supersedes_legacy_pi6_3_narrative_contract():
  expected, actual = (
    _phase144_6_pi6_3_renderings()
  )

  assert actual == expected


def test_phase144_6_pi6_3_generic_route_preserves_target():
  _, actual = (
    _phase144_6_pi6_3_renderings()
  )

  assert (
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    in actual
  )

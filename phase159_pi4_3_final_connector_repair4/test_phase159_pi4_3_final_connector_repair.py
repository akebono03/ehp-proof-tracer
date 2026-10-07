from toda_group_proof_narrative_contribution_renderer import (
  suppress_toda_group_proof_narrative_dangling_connectors,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


PI4_3_CONCLUSION = (
  r"\pi_{4}^{3} = "
  r"\mathbb{Z}/2\{\eta_{3}\}"
)


def _render_phase159_pi4_3_public_narrative() -> str:
  (
    presentation,
    _,
    _,
    _,
  ) = _method_evidence_data(
    3,
    1,
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase159_pi4_3_moves_trailing_connector_to_following_derivation():
  markdown = "\n\n".join(
    (
      (
        r"$\pi_{3}^{2} = "
        r"\mathbb{Z}\{\eta_{2}\}$"
        "\n"
        "以上より,"
      ),
      (
        "$"
        + PI4_3_CONCLUSION
        + "$"
      ),
    )
  )

  rendered = (
    suppress_toda_group_proof_narrative_dangling_connectors(
      markdown
    )
  )

  assert (
    "\n以上より,"
    not in rendered
  )
  assert (
    "以上より, "
    + "$"
    + PI4_3_CONCLUSION
    + "$"
  ) in rendered


def test_phase159_pi4_3_public_final_conclusion_keeps_connector_once():
  rendered = (
    _render_phase159_pi4_3_public_narrative()
  )
  proof_marker = "\n## 証明\n\n"

  assert proof_marker in rendered

  proof_body = rendered.split(
    proof_marker,
    1,
  )[1]

  assert proof_body.count(
    PI4_3_CONCLUSION
  ) == 1
  assert (
    "以上より, "
    + "$"
    + PI4_3_CONCLUSION
    + "$."
  ) in proof_body
  assert rendered.rstrip().endswith(
    "□"
  )

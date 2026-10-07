from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


def main() -> int:
  (
    presentation,
    _,
    _,
    _,
  ) = _method_evidence_data(
    3,
    1,
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  print(
    rendered
  )

  proof_marker = "\n## 証明\n\n"

  if proof_marker not in rendered:
    raise RuntimeError(
      "public proof marker not found"
    )

  proof_body = rendered.split(
    proof_marker,
    1,
  )[1]

  conclusion = (
    r"\pi_{4}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\}"
  )

  print(
    "proof_body_conclusion_count="
    + str(
      proof_body.count(
        conclusion
      )
    )
  )
  print(
    "connected_final_conclusion="
    + str(
      (
        "以上より, "
        + "$"
        + conclusion
        + "$."
      )
      in proof_body
    )
  )

  if proof_body.count(
    conclusion
  ) != 1:
    raise RuntimeError(
      "pi4_3 conclusion is not unique in proof body"
    )

  if (
    "以上より, "
    + "$"
    + conclusion
    + "$."
  ) not in proof_body:
    raise RuntimeError(
      "connected final conclusion not found"
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

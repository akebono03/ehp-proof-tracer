from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


def main() -> None:
  (
    presentation,
    _,
    _,
    _,
  ) = _method_evidence_data(
    2,
    1,
  )

  print(
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


if __name__ == "__main__":
  main()

from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def main() -> None:
  for n, k in (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ):
    (
      presentation,
      blocks,
      sidecar,
      arguments,
    ) = _method_evidence_data(
      n,
      k,
    )
    rendered = (
      render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
      )
    )

    print(
      "=" * 78
    )
    print(
      f"n={n}, k={k}"
    )
    print(
      rendered
    )


if __name__ == "__main__":
  main()

from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


CASES = (
  (3, 4),
  (4, 5),
  (6, 5),
  (4, 6),
  (5, 6),
  (7, 7),
)


def main():
  for n, k in CASES:
    (
      presentation,
      blocks,
      sidecar,
      arguments,
    ) = _method_evidence_data(
      n,
      k,
    )

    rendered = render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )

    print("=" * 78)
    print(f"n={n}, k={k}")
    print(
      "raw_eta_definition=",
      "TodaEtaFamilyDefinitionStatement" in rendered,
    )
    print(rendered)


if __name__ == "__main__":
  main()

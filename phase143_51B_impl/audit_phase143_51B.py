from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


_OLD_FALLBACKS = (
  "Toda Proposition 5.6 pi_8^5 quotient by E^2 pi_6^3",
  "Toda (5.14) second short exact sequence",
  "Toda Proposition 5.15 sigma_8 transported decomposition",
  "Toda (4.8) pi_16^9 order sixteen and E4 injective",
)


def main():
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

    remaining = tuple(
      fallback
      for fallback in _OLD_FALLBACKS
      if fallback in rendered
    )

    print("=" * 78)
    print(
      f"n={n}, k={k}, "
      f"remaining_aggregate_fallbacks={remaining}"
    )
    print("=" * 78)
    print(rendered)
    print()


if __name__ == "__main__":
  main()

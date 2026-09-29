from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


_INTERNAL_MARKERS = (
  " integration",
  " specialization",
  " semantics",
  " branch",
  " bridge",
  "TodaProp",
  "TodaSigmaFamilyDefinitionStatement",
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
      marker
      for marker in _INTERNAL_MARKERS
      if marker in rendered
    )

    print("=" * 78)
    print(
      f"n={n}, k={k}, "
      f"remaining_internal_markers={remaining}"
    )
    print("=" * 78)
    print(
      rendered
    )
    print()


if __name__ == "__main__":
  main()

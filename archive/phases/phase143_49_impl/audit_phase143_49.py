import re

from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


BLOCK_LABEL_PATTERN = re.compile(
  r"\[B\d{2}\]"
)


def audit_case(
  n: int,
  k: int,
) -> None:
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
  labels = BLOCK_LABEL_PATTERN.findall(
    rendered
  )

  print("=" * 78)
  print(
    f"n={n}, k={k}, dependency_labels={len(labels)}"
  )
  print("=" * 78)
  print(
    rendered
  )
  print()


def main() -> None:
  for n, k in (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ):
    audit_case(
      n,
      k,
    )


if __name__ == "__main__":
  main()

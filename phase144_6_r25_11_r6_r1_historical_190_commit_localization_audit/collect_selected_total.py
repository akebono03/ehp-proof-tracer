import importlib.util
from pathlib import Path
import sys

from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def _load_foundation():
  path = (
    Path("tests")
    / "test_phase144_6_r5_18_production_generic_proof_chain_foundation.py"
  )
  name = "_r25_11_r6_r1_foundation"
  spec = importlib.util.spec_from_file_location(
    name,
    path,
  )
  if spec is None or spec.loader is None:
    raise ImportError(
      f"cannot load {path}"
    )
  module = importlib.util.module_from_spec(
    spec
  )
  sys.modules[name] = module
  spec.loader.exec_module(module)
  return module


def main():
  foundation = _load_foundation()
  counts = []

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      _aggregate,
      proof_chains,
    ) = foundation._context(
      n,
      k,
    )
    base_markdown = (
      render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )
    ordered = (
      build_toda_group_proof_narrative_ordered_contributions(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        proof_chains,
        current_markdown=base_markdown,
      )
    )
    count = sum(
      len(
        contributions
      )
      for contributions in ordered
    )
    counts.append(
      (
        n,
        k,
        count,
      )
    )

  total = sum(
    count
    for _n, _k, count in counts
  )
  groups = ",".join(
    f"pi_{n + k}^{n}={count}"
    for n, k, count in counts
  )
  print(
    f"TOTAL={total};{groups}"
  )


if __name__ == "__main__":
  main()

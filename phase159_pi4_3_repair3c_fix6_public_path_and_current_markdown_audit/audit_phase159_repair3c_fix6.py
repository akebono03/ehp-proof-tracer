from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TESTS_DIR = REPO_ROOT / "tests"

for path in (
  REPO_ROOT,
  TESTS_DIR,
):
  if str(path) not in sys.path:
    sys.path.insert(
      0,
      str(path),
    )


from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
)


TARGET_TYPES = (
  TodaDeltaImageUpToSignStatement,
  TodaDeltaImageFreeCyclicStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
)


def _selected_type_names(rows):
  return tuple(
    type(
      row.proof_step.conclusion
    ).__name__
    for argument_rows in rows
    for row in argument_rows
  )


def main():
  print("=" * 78)
  print("Phase 159 - pi_4^3 repair3c fix6 audit")
  print("Public path and current_markdown contract")
  print("=" * 78)
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print()

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      _aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(
      n,
      k,
    )
    base = (
      render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )
    default_rows = (
      build_toda_group_proof_narrative_ordered_contributions(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        proof_chains,
      )
    )
    explicit_rows = (
      build_toda_group_proof_narrative_ordered_contributions(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        proof_chains,
        current_markdown=base,
      )
    )
    default_ids = tuple(
      tuple(
        id(
          row.proof_step
        )
        for row in argument_rows
      )
      for argument_rows in default_rows
    )
    explicit_ids = tuple(
      tuple(
        id(
          row.proof_step
        )
        for row in argument_rows
      )
      for argument_rows in explicit_rows
    )

    print(
      f"TARGET pi_{n+k}^{n}: "
      f"default={sum(len(x) for x in default_rows)} "
      f"explicit={sum(len(x) for x in explicit_rows)} "
      f"same={default_ids == explicit_ids}"
    )

  print()
  print("=" * 78)
  print("PI_4^3")
  print("=" * 78)

  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    _aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(
    3,
    1,
  )
  base = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  default_rows = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
    )
  )
  explicit_rows = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
      current_markdown=base,
    )
  )
  public = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  print(
    f"default_count={sum(len(x) for x in default_rows)}"
  )
  print(
    f"explicit_count={sum(len(x) for x in explicit_rows)}"
  )
  print(
    "default_target_types="
    + repr(
      tuple(
        name
        for name in _selected_type_names(
          default_rows
        )
        if name in {
          cls.__name__
          for cls in TARGET_TYPES
        }
      )
    )
  )
  print(
    "explicit_target_types="
    + repr(
      tuple(
        name
        for name in _selected_type_names(
          explicit_rows
        )
        if name in {
          cls.__name__
          for cls in TARGET_TYPES
        }
      )
    )
  )

  print()
  print("PUBLIC PRESENCE")
  probes = (
    (
      "direct_delta",
      r"\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}",
    ),
    (
      "image_delta",
      r"\operatorname{Im}\Delta = \mathbb{Z}\{2\eta_{2}\}",
    ),
    (
      "kernel_E",
      r"\ker E = \mathbb{Z}\{2\eta_{2}\}",
    ),
    (
      "E_surjective",
      r"E: \pi_{3}^{2} \to \pi_{4}^{3}",
    ),
  )

  for label, needle in probes:
    print(
      f"{label}={needle in public}"
    )

  print()
  print("PUBLIC NARRATIVE")
  print("-" * 78)
  print(
    public
  )
  print("-" * 78)

  print()
  print("=" * 78)
  print("repair3c fix6 audit complete")
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print("=" * 78)


if __name__ == "__main__":
  main()

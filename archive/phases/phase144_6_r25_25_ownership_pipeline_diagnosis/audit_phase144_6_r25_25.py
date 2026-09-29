from collections import Counter

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_display_contributions import (
  extract_toda_group_proof_narrative_exactness_display_contributions,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_primary_exactness_component,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def _data(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = (
    build_complete_toda_group_result_proof_replay(
      group_result
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=sidecar,
    )
  )
  return (
    presentation,
    blocks,
    sidecar,
    arguments,
  )


def _exactness_count(
  blocks,
):
  return sum(
    block.role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .EXACTNESS
    for block in blocks
  )


def _exactness_contribution_count(
  presentation,
  blocks,
):
  return sum(
    len(
      extract_toda_group_proof_narrative_exactness_display_contributions(
        presentation,
        block,
      )
    )
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    )
  )


def main():
  print(
    "Phase 144-6 R25-25 ownership pipeline diagnosis"
  )
  print(
    "Production behavior: R25-23 baseline after R25-24 rollback"
  )
  print()

  for n, k in TARGETS:
    (
      presentation,
      blocks,
      sidecar,
      arguments,
    ) = _data(
      n,
      k,
    )

    base_markdown = (
      render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
      )
    )
    proof_chains = (
      build_toda_group_proof_narrative_proof_chains(
        presentation,
        sidecar,
        arguments,
      )
    )
    ordered_contributions = (
      build_toda_group_proof_narrative_ordered_contributions(
        presentation,
        blocks,
        sidecar,
        arguments,
        proof_chains,
        current_markdown=base_markdown,
      )
    )
    final_markdown = (
      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
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
      f"pi_{n + k}^{n}"
    )
    print(
      "=" * 78
    )
    print(
      "presentation nodes:",
      len(
        presentation.nodes
      ),
    )
    print(
      "all blocks:",
      len(
        blocks
      ),
    )
    print(
      "all exactness blocks:",
      _exactness_count(
        blocks
      ),
    )
    print(
      "all exactness display contributions:",
      _exactness_contribution_count(
        presentation,
        blocks,
      ),
    )
    print(
      "arguments:",
      len(
        arguments
      ),
    )
    print(
      "base markdown chars:",
      len(
        base_markdown
      ),
    )
    print(
      "final markdown chars:",
      len(
        final_markdown
      ),
    )
    print(
      "contribution insertion delta:",
      len(
        final_markdown
      )
      - len(
        base_markdown
      ),
    )

    contribution_types = Counter(
      type(
        contribution.proof_step.conclusion
      ).__name__
      for contributions in ordered_contributions
      for contribution in contributions
    )
    print(
      "ordered contributions:",
      sum(
        len(
          contributions
        )
        for contributions in ordered_contributions
      ),
    )
    print(
      "ordered contribution statement types:",
      dict(
        contribution_types
      ),
    )
    print()

    for argument_index, argument in enumerate(
      arguments
    ):
      local_body = (
        extract_toda_group_proof_narrative_argument_local_body_blocks(
          presentation,
          blocks,
          sidecar,
          arguments,
          argument_index,
        )
      )
      evidence = (
        extract_toda_group_proof_narrative_argument_method_evidence(
          presentation,
          blocks,
          sidecar,
          arguments,
          argument_index,
        )
      )
      relevant_groups = (
        extract_toda_group_proof_narrative_argument_relevant_groups(
          presentation,
          blocks,
          argument,
        )
      )
      components = (
        build_toda_group_proof_narrative_exactness_method_components(
          evidence
        )
      )
      primary = (
        select_toda_group_proof_narrative_primary_exactness_component(
          relevant_groups,
          components,
        )
      )
      ordered = ordered_contributions[
        argument_index
      ]

      if not (
        local_body
        or evidence
        or ordered
      ):
        continue

      print(
        f"argument {argument_index:03d} "
        f"role={argument.role.value}"
      )
      print(
        "  local_body:",
        len(
          local_body
        ),
        "exactness=",
        _exactness_count(
          local_body
        ),
      )
      print(
        "  method_evidence:",
        len(
          evidence
        ),
      )
      print(
        "  exactness_components:",
        len(
          components
        ),
        "component_windows=",
        tuple(
          len(
            component.windows
          )
          for component in components
        ),
      )
      print(
        "  primary_component:",
        (
          "none"
          if primary is None
          else (
            f"windows={len(primary.windows)} "
            f"evidence_blocks={len(primary.evidence_blocks)}"
          )
        ),
      )
      print(
        "  ordered_contributions:",
        len(
          ordered
        ),
        "types=",
        tuple(
          type(
            contribution.proof_step.conclusion
          ).__name__
          for contribution in ordered
        ),
      )

    print()


if __name__ == "__main__":
  main()

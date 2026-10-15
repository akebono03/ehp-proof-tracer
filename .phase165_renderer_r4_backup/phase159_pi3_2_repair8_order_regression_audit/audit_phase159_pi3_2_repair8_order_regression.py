from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _contribution_insertion_indices,
  _insert_toda_group_proof_narrative_argument_contributions,
  _provider_anchor_index,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


H_INJECTIVE_VERBOSE = (
  r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
  "は単射である."
)
H_INJECTIVE_CONCISE = (
  r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
  "は単射."
)
H_SURJECTIVE_VERBOSE = (
  r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
  "は全射である."
)
H_SURJECTIVE_CONCISE = (
  r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
  "は全射."
)
H_ISOMORPHISM = (
  r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
  "は同型写像である."
)
E_ISOMORPHISM = (
  r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ "
  "は同型写像である."
)
DELTA_ZERO = (
  r"$\Delta: \pi_{3}^{3} \to \pi_{1}^{1}$ "
  "は零写像である."
)


def positions(
  markdown: str,
):
  names = (
    (
      "E_ISOMORPHISM",
      E_ISOMORPHISM,
    ),
    (
      "DELTA_ZERO",
      DELTA_ZERO,
    ),
    (
      "H_SURJECTIVE_VERBOSE",
      H_SURJECTIVE_VERBOSE,
    ),
    (
      "H_SURJECTIVE_CONCISE",
      H_SURJECTIVE_CONCISE,
    ),
    (
      "H_INJECTIVE_VERBOSE",
      H_INJECTIVE_VERBOSE,
    ),
    (
      "H_INJECTIVE_CONCISE",
      H_INJECTIVE_CONCISE,
    ),
    (
      "H_ISOMORPHISM",
      H_ISOMORPHISM,
    ),
  )

  return tuple(
    (
      name,
      markdown.find(
        text
      ),
    )
    for name, text in names
  )


def report_stage(
  lines,
  name: str,
  markdown: str,
) -> None:
  lines.append(
    "## "
    + name
  )
  lines.append(
    ""
  )

  for label, index in positions(
    markdown
  ):
    lines.append(
      label
      + "="
      + str(
        index
      )
    )

  lines.append(
    ""
  )

  for index, paragraph in enumerate(
    markdown.split(
      "\n\n"
    )
  ):
    if any(
      fragment in paragraph
      for fragment in (
        r"\pi_{1}^{1} \to \pi_{2}^{2}",
        r"\Delta: \pi_{3}^{3}",
        r"H: \pi_{3}^{2} \to \pi_{3}^{3}",
      )
    ):
      lines.append(
        "P"
        + str(
          index
        )
        + ": "
        + repr(
          paragraph
        )
      )

  lines.append(
    ""
  )


def main() -> int:
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    2,
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
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
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
      current_markdown=base,
    )
  )
  indices = (
    _contribution_insertion_indices(
      base,
      blocks,
      arguments,
      ordered,
    )
  )
  inserted = (
    _insert_toda_group_proof_narrative_argument_contributions(
      presentation,
      base,
      blocks,
      arguments,
      ordered,
    )
  )
  connected = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  public = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  lines = [
    "# Phase 159 pi3_2 repair8 order regression audit",
    "",
    "## Contribution placement",
    "",
  ]

  for argument_index, contributions in enumerate(
    ordered
  ):
    if not contributions:
      continue

    lines.append(
      "argument_"
      + str(
        argument_index
      )
      + "_role="
      + str(
        arguments[
          argument_index
        ].role
      )
    )

    for contribution_index, contribution in enumerate(
      contributions
    ):
      rendered = (
        _render_generic_narrative_step(
          contribution.proof_step
        )
      )
      provider_anchor_index = (
        _provider_anchor_index(
          base,
          blocks,
          contribution.provider_keys,
        )
      )
      insertion_index = indices[
        argument_index
      ][
        contribution_index
      ]

      lines.extend(
        (
          "  contribution_"
          + str(
            contribution_index
          )
          + "="
          + repr(
            rendered
          ),
          "    placement="
          + str(
            contribution.placement
          ),
          "    provider_anchor="
          + str(
            contribution.provider_anchor
          ),
          "    provider_anchor_index="
          + repr(
            provider_anchor_index
          ),
          "    insertion_index="
          + repr(
            insertion_index
          ),
        )
      )

  lines.append(
    ""
  )

  report_stage(
    lines,
    "00 BASE",
    base,
  )
  report_stage(
    lines,
    "01 INSERTED CONTRIBUTIONS",
    inserted,
  )
  report_stage(
    lines,
    "02 FULL CONTRIBUTION RENDERER",
    connected,
  )
  report_stage(
    lines,
    "03 PUBLIC",
    public,
  )

  lines.extend(
    (
      "## Public markdown",
      "",
      public,
      "",
    )
  )

  output = "\n".join(
    lines
  )

  output_path = (
    Path(__file__).resolve().parent
    / "phase159_pi3_2_repair8_order_regression_audit.txt"
  )
  output_path.write_text(
    output,
    encoding="utf-8",
  )

  print(
    output
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

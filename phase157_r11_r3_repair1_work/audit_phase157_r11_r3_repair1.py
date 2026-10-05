from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _insert_toda_group_proof_narrative_argument_contributions,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_reason_renderer import (
  insert_toda_group_proof_narrative_reason_prose,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGET_FRAGMENTS = (
  (
    "unwanted_suspension_iso",
    r"$E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型写像である.",
  ),
  (
    "needed_pi6_5_group",
    r"$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$",
  ),
)


def _presentation():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )


def _print_presence(
  label: str,
  markdown: str,
) -> None:
  print()
  print(label)
  print("-" * len(label))

  for fragment_label, fragment in TARGET_FRAGMENTS:
    line_numbers = tuple(
      number
      for number, line in enumerate(
        markdown.splitlines(),
        start=1,
      )
      if fragment in line
    )
    print(
      f"{fragment_label}: "
      f"present={bool(line_numbers)} "
      f"lines={line_numbers}"
    )


def main() -> None:
  presentation = _presentation()
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
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

  contribution_markdown = (
    _insert_toda_group_proof_narrative_argument_contributions(
      presentation,
      base_markdown,
      blocks,
      arguments,
      ordered_contributions,
    )
  )

  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      sidecar,
    )
  )

  reason_markdown = (
    insert_toda_group_proof_narrative_reason_prose(
      contribution_markdown,
      reason_sidecar,
    )
  )

  final_markdown = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  print("=" * 78)
  print("Phase157 R11-R3 repair1 — statement origin audit")
  print("=" * 78)
  print("target: pi_6^3, max_depth=2")
  print(f"reasons: {len(reason_sidecar.reasons)}")

  _print_presence(
    "Stage 1: base_markdown",
    base_markdown,
  )
  _print_presence(
    "Stage 2: contribution_markdown",
    contribution_markdown,
  )
  _print_presence(
    "Stage 3: reason_markdown",
    reason_markdown,
  )
  _print_presence(
    "Stage 4: final_markdown",
    final_markdown,
  )

  print()
  print("Reason rows related to target fragments")
  print("---------------------------------------")

  matched_reason = False

  for index, reason in enumerate(
    reason_sidecar.reasons
  ):
    values = (
      str(
        reason.conclusion_step.conclusion
      ),
      str(
        getattr(
          reason,
          "reason",
          "",
        )
      ),
      str(
        reason
      ),
    )

    if not any(
      (
        "pi_4" in value
        or "pi_5" in value
        or "pi_6" in value
        or "suspension" in value.lower()
        or "eta_5" in value
        or "η₅" in value
      )
      for value in values
    ):
      continue

    matched_reason = True
    print(
      f"R{index:03d}: "
      f"conclusion_type="
      f"{type(reason.conclusion_step.conclusion).__name__}"
    )
    print(
      "  conclusion="
      + str(
        reason.conclusion_step.conclusion
      ).replace(
        "\n",
        " ",
      )
    )
    print(
      "  reason="
      + str(
        reason
      ).replace(
        "\n",
        " ",
      )
    )

  if not matched_reason:
    print(
      "(no reason row matched the configured diagnostic terms)"
    )

  output_dir = PACKAGE_DIR / "output"
  output_dir.mkdir(
    exist_ok=True
  )

  stages = (
    ("01_base.md", base_markdown),
    ("02_contributions.md", contribution_markdown),
    ("03_reasons.md", reason_markdown),
    ("04_final.md", final_markdown),
  )

  for filename, markdown in stages:
    (
      output_dir
      / filename
    ).write_text(
      markdown,
      encoding="utf-8",
    )

  print()
  print("R11-R3 repair1 origin audit completed.")


if __name__ == "__main__":
  main()

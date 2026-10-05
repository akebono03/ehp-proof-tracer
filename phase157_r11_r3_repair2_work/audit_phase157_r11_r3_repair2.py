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


TARGETS = (
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


def _presence(markdown):
  rows = {}
  for label, fragment in TARGETS:
    lines = tuple(
      number
      for number, line in enumerate(
        markdown.splitlines(),
        start=1,
      )
      if fragment in line
    )
    rows[label] = lines
  return rows


def main():
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

  base = (
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
  ordered = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      sidecar,
      arguments,
      proof_chains,
      current_markdown=base,
    )
  )
  contributions = (
    _insert_toda_group_proof_narrative_argument_contributions(
      presentation,
      base,
      blocks,
      arguments,
      ordered,
    )
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      sidecar,
    )
  )
  reasons = (
    insert_toda_group_proof_narrative_reason_prose(
      contributions,
      reason_sidecar,
    )
  )
  final = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  stages = (
    ("stage1_base", base),
    ("stage2_contributions", contributions),
    ("stage3_reasons", reasons),
    ("stage4_final", final),
  )

  print("=" * 72)
  print("Phase157 R11-R3 repair2 - compact statement origin audit")
  print("=" * 72)

  for stage_name, markdown in stages:
    print(stage_name)
    presence = _presence(
      markdown
    )
    for label, lines in presence.items():
      print(
        f"  {label}: "
        f"present={bool(lines)} "
        f"lines={lines}"
      )

  print()
  print("matching reason conclusions")
  print("---------------------------")

  for index, reason in enumerate(
    reason_sidecar.reasons
  ):
    conclusion_type = type(
      reason.conclusion_step.conclusion
    ).__name__
    conclusion_text = str(
      reason.conclusion_step.conclusion
    )

    interesting = (
      "group_dimension=4" in conclusion_text
      and "sphere_dimension=2" in conclusion_text
      and "group_dimension=5" in conclusion_text
      and "sphere_dimension=3" in conclusion_text
    ) or (
      "group_dimension=6" in conclusion_text
      and "sphere_dimension=5" in conclusion_text
    )

    if not interesting:
      continue

    owner = getattr(
      reason,
      "owner_argument_index",
      None,
    )
    reference_application = getattr(
      reason,
      "reference_application",
      None,
    )
    inference_name = None

    inference_rule = (
      reason.conclusion_step.inference_rule
    )
    if inference_rule is not None:
      inference_name = inference_rule.name

    print(
      f"  reason[{index}]: "
      f"type={conclusion_type} "
      f"owner={owner} "
      f"reference_application={reference_application} "
      f"inference={inference_name}"
    )

  print()
  print("done")


if __name__ == "__main__":
  main()

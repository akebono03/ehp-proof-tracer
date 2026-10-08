from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(
  REPO_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan,
  _toda_group_proof_narrative_reference_frontier_step_ids,
  _toda_group_proof_narrative_reference_internal_step_ids,
  _toda_group_proof_narrative_reference_owned_step_ids,
  specialize_toda_group_proof_narrative_fixed_composition_isomorphism_application,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
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


def main():
  report = build_standard_toda_report(
    n=2,
    k=2,
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
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=semantic_sidecar,
  )

  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      entries,
      presentation.root_step,
    )
  )
  statement_lines = {
    entry.number: ()
    for entry in entries
  }
  entries, _ = (
    exclude_toda_group_proof_narrative_root_reference(
      entries,
      statement_lines,
      presentation.root_step,
    )
  )

  frontier_ids = (
    _toda_group_proof_narrative_reference_frontier_step_ids(
      presentation,
      entries,
    )
  )
  owned_ids = (
    _toda_group_proof_narrative_reference_owned_step_ids(
      presentation,
      entries,
    )
  )
  internal_ids = (
    _toda_group_proof_narrative_reference_internal_step_ids(
      presentation,
      entries,
    )
  )

  print(
    "=" * 78
  )
  print(
    "Phase 161-R4-R2 pi_4^2 post-render audit"
  )
  print(
    "=" * 78
  )

  print()
  print(
    "[Reference entries after fixed boundary + root exclusion]"
  )

  for entry in entries:
    print(
      f"R{entry.number}: "
      f"{entry.reference.locator}"
    )

    for proof_step in entry.proof_steps:
      print(
        "  "
        f"id={id(proof_step)} "
        f"rule={proof_step.rule_name!r} "
        f"type={type(proof_step.conclusion).__name__} "
        f"frontier={id(proof_step) in frontier_ids} "
        f"owned={id(proof_step) in owned_ids} "
        f"internal={id(proof_step) in internal_ids}"
      )

  print()
  print(
    "[Presentation steps relevant to (5.2) / Proposition 4.4]"
  )

  for node in presentation.nodes:
    proof_step = node.proof_step
    rule = (
      proof_step.rule_name
      or ""
    )

    if (
      "5.2" not in rule
      and "4.4" not in rule
    ):
      continue

    reference = (
      None
      if proof_step.inference_rule is None
      else proof_step.inference_rule.literature_reference
    )

    print(
      f"id={id(proof_step)} "
      f"rule={rule!r} "
      f"type={type(proof_step.conclusion).__name__} "
      f"reference={None if reference is None else reference.locator!r} "
      f"frontier={id(proof_step) in frontier_ids} "
      f"owned={id(proof_step) in owned_ids} "
      f"internal={id(proof_step) in internal_ids}"
    )

  plan = (
    _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan(
      presentation,
      entries,
    )
  )

  print()
  print(
    "[Specialization plan]"
  )
  print(
    "plan is None:",
    plan is None,
  )

  if plan is not None:
    (
      entry,
      fixed_step,
      source_step,
      specialized_source,
      specialized_target,
      source_generator,
      target_generator,
      target_dimension,
    ) = plan

    print(
      "reference number:",
      entry.number,
    )
    print(
      "target dimension:",
      target_dimension,
    )
    print(
      "specialized source:",
      specialized_source,
    )
    print(
      "specialized target:",
      specialized_target,
    )
    print(
      "source generator:",
      source_generator,
    )
    print(
      "target generator:",
      target_generator,
    )

  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )

  print()
  print(
    "[Final public Narrative - full]"
  )
  print(
    rendered
  )

  reference, body = rendered.split(
    "---",
    1,
  )

  print()
  print(
    "[Final body paragraphs - repr]"
  )

  for index, paragraph in enumerate(
    body.split(
      "\n\n"
    ),
    start=1,
  ):
    print(
      f"{index:02d}: {paragraph!r}"
    )

  print()
  print(
    "[Diagnostics]"
  )
  print(
    "exact specialized sentence:",
    (
      r"[R1]を $i=4$ に適用すると, "
      r"$\eta_{2}\circ -: "
      r"\pi_{4}^{3} \to \pi_{4}^{2}$ "
      r"は同型である."
    )
    in body,
  )
  print(
    "contains specialized groups:",
    (
      r"\pi_{4}^{3} \to \pi_{4}^{2}"
      in body
    ),
  )
  print(
    "contains i=4:",
    "$i=4$" in body,
  )
  print(
    "contains Proposition 4.4 reference:",
    "Proposition 4.4" in reference,
  )
  print(
    "contains general Prop44 map body:",
    (
      r"\pi_{i - 1}^{1} \oplus "
      r"\pi_{i}^{3} \to "
      r"\pi_{i}^{2}"
    )
    in body,
  )
  print(
    "contains second-summand body:",
    "分解写像の第二成分"
    in body,
  )
  print(
    "contains generator transport:",
    r"\eta_{3} \mapsto"
    in body,
  )


if __name__ == "__main__":
  main()

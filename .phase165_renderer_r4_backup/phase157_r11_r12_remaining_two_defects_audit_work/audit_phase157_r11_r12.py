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
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  filter_phase157_r3_pi6_3_reference_entries,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _raw_presentation():
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

  return build_toda_group_proof_presentation(
    replay
  )


def _rule_name(
  step,
):
  rule = step.inference_rule
  return (
    None
    if rule is None
    else rule.name
  )


def _locator(
  step,
):
  reference = (
    extract_toda_group_proof_step_literature_reference(
      step
    )
  )
  return (
    None
    if reference is None
    else reference.locator
  )


def _reference_entry(
  presentation,
):
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      entries,
      presentation.root_step,
    )
  )
  entries = (
    filter_phase157_r3_pi6_3_reference_entries(
      entries,
      presentation.root_step,
    )
  )

  return next(
    entry
    for entry in entries
    if entry.reference.locator == "(5.3)"
  )


def main():
  raw = _raw_presentation()
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  entry = _reference_entry(
    presentation
  )

  print("=" * 78)
  print("Phase157 R11-R12 — remaining two defects audit")
  print("=" * 78)
  print(
    f"raw nodes={len(raw.nodes)} edges={len(raw.edges)}"
  )
  print(
    f"closure nodes={len(presentation.nodes)} edges={len(presentation.edges)}"
  )
  print()

  entry_step_ids = {
    id(
      step
    )
    for step in entry.proof_steps
  }

  boundary_used_step_ids = {
    id(
      edge.premise_step
    )
    for edge in presentation.edges
    if (
      edge.premise_step
      is not presentation.root_step
      and extract_toda_group_proof_step_literature_reference(
        edge.premise_step
      )
      == entry.reference
      and extract_toda_group_proof_step_literature_reference(
        edge.parent_step
      )
      != entry.reference
    )
  }

  entry_external_used_step_ids = {
    id(
      edge.premise_step
    )
    for edge in presentation.edges
    if id(
      edge.parent_step
    ) not in entry_step_ids
  }

  used_candidate_step_ids = (
    boundary_used_step_ids
    | entry_external_used_step_ids
  )

  used_premises = tuple(
    edge.premise_step
    for edge in presentation.edges
    if id(
      edge.premise_step
    ) in used_candidate_step_ids
  )

  print("(5.3) ENTRY CANDIDATES")
  print("----------------------")

  for index, step in enumerate(
    entry.proof_steps,
    start=1,
  ):
    rendered = (
      _render_generic_narrative_step(
        step
      )
    )
    identity_used = (
      id(
        step
      )
      in used_candidate_step_ids
    )
    equal_matches = tuple(
      premise
      for premise in used_premises
      if premise.conclusion == step.conclusion
    )

    print(
      f"[{index}] id={id(step)}"
    )
    print(
      f"  rule={_rule_name(step)!r}"
    )
    print(
      f"  rendered={rendered!r}"
    )
    print(
      f"  identity_used={identity_used}"
    )
    print(
      f"  equal_used_matches={len(equal_matches)}"
    )

    for match_index, match in enumerate(
      equal_matches,
      start=1,
    ):
      print(
        f"    match[{match_index}] "
        f"id={id(match)} "
        f"locator={_locator(match)!r} "
        f"rule={_rule_name(match)!r} "
        f"rendered={_render_generic_narrative_step(match)!r}"
      )

  print()
  print("USED PREMISES")
  print("-------------")

  for index, premise in enumerate(
    used_premises,
    start=1,
  ):
    print(
      f"[{index}] "
      f"id={id(premise)} "
      f"locator={_locator(premise)!r} "
      f"rule={_rule_name(premise)!r}"
    )
    print(
      f"  rendered={_render_generic_narrative_step(premise)!r}"
    )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      raw
    )
  )
  _, body = rendered.split(
    "\n## 証明\n",
    1,
  )
  paragraphs = body.split(
    "\n\n"
  )

  print()
  print("BODY ORDER TARGETS")
  print("------------------")

  targets = (
    r"\tag{4}",
    r"\tag{5}",
    r"\tag{6}",
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である.",
    r"$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$.",
  )

  for index, paragraph in enumerate(
    paragraphs
  ):
    if any(
      target in paragraph
      for target in targets
    ):
      print(
        f"paragraph[{index}]: {paragraph!r}"
      )

  print()
  print("SURJECTIVITY PREMISE ORDER")
  print("--------------------------")

  for node in presentation.nodes:
    step = node.proof_step

    if _rule_name(
      step
    ) != (
      "Toda Proposition 5.3 n=3 "
      "Hopf eta_5 surjectivity"
    ):
      continue

    print(
      f"surjectivity id={id(step)} "
      f"rendered={_render_generic_narrative_step(step)!r}"
    )

    for premise_index, premise in enumerate(
      step.premises,
      start=1,
    ):
      print(
        f"  premise[{premise_index}] "
        f"id={id(premise)} "
        f"rule={_rule_name(premise)!r} "
        f"rendered={_render_generic_narrative_step(premise)!r}"
      )

      for sub_index, subpremise in enumerate(
        premise.premises,
        start=1,
      ):
        print(
          f"    subpremise[{sub_index}] "
          f"id={id(subpremise)} "
          f"rule={_rule_name(subpremise)!r} "
          f"rendered={_render_generic_narrative_step(subpremise)!r}"
        )

  print()
  print("done")


if __name__ == "__main__":
  main()

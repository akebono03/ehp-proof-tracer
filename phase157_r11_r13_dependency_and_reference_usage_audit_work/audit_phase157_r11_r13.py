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


from proof import (
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
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


TARGET_RENDERED_FRAGMENTS = (
  r"\operatorname{ord}\left(\eta_{3}^{3}\right) = 2",
  r"E: \pi_{5}^{2} \to \pi_{6}^{3}",
  r"H: \pi_{6}^{3} \to \pi_{6}^{5}",
  r"\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}",
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
  inference_rule = step.inference_rule
  return (
    None
    if inference_rule is None
    else inference_rule.name
  )


def _describe_step(
  label,
  step,
):
  print(
    f"{label}: "
    f"id={id(step)} "
    f"rule={_rule_name(step)!r}"
  )
  print(
    f"  rendered={_render_generic_narrative_step(step)!r}"
  )

  for index, premise in enumerate(
    step.premises,
    start=1,
  ):
    print(
      f"  premise[{index}] "
      f"id={id(premise)} "
      f"rule={_rule_name(premise)!r} "
      f"rendered={_render_generic_narrative_step(premise)!r}"
    )


def _find_nodes_by_fragment(
  presentation,
  fragment,
):
  return tuple(
    node.proof_step
    for node in presentation.nodes
    if fragment
    in _render_generic_narrative_step(
      node.proof_step
    )
  )


def main():
  raw = _raw_presentation()
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )

  print("=" * 78)
  print("Phase157 R11-R13 — dependency and Reference usage audit")
  print("=" * 78)
  print(
    f"raw nodes={len(raw.nodes)} edges={len(raw.edges)}"
  )
  print(
    f"closure nodes={len(presentation.nodes)} edges={len(presentation.edges)}"
  )

  print()
  print("TARGET STEP DEPENDENCIES")
  print("------------------------")

  for fragment in TARGET_RENDERED_FRAGMENTS:
    matches = _find_nodes_by_fragment(
      presentation,
      fragment,
    )
    print()
    print(
      f"fragment={fragment!r} matches={len(matches)}"
    )
    for index, step in enumerate(
      matches,
      start=1,
    ):
      _describe_step(
        f"match[{index}]",
        step,
      )

  print()
  print("REFERENCE ENTRIES / OUTGOING USE")
  print("--------------------------------")

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

  consumers_by_step_id = {}

  for edge in presentation.edges:
    consumers_by_step_id.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  for entry in entries:
    print()
    print(
      f"[R{entry.number}] "
      f"locator={entry.reference.locator!r} "
      f"label={entry.reference.label!r}"
    )

    for index, step in enumerate(
      entry.proof_steps,
      start=1,
    ):
      consumers = tuple(
        consumers_by_step_id.get(
          id(
            step
          ),
          (),
        )
      )
      print(
        f"  step[{index}] "
        f"rule={_rule_name(step)!r} "
        f"rendered={_render_generic_narrative_step(step)!r}"
      )
      print(
        f"    consumers={len(consumers)}"
      )
      for c_index, consumer in enumerate(
        consumers,
        start=1,
      ):
        print(
          f"      consumer[{c_index}] "
          f"rule={_rule_name(consumer)!r} "
          f"rendered={_render_generic_narrative_step(consumer)!r}"
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
  print("PUBLIC BODY ORDER")
  print("-----------------")

  order_targets = (
    r"\operatorname{ord}\left(\eta_{3}^{3}\right) = 2",
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である.",
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である.",
    r"$0\longrightarrow \pi_{5}^{2}",
    r"$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$.",
    "[R3]",
  )

  for index, paragraph in enumerate(
    paragraphs
  ):
    if any(
      target in paragraph
      for target in order_targets
    ):
      print(
        f"paragraph[{index}]: {paragraph!r}"
      )

  print()
  print("BODY REFERENCES")
  print("---------------")
  for marker in (
    "[R1]",
    "[R2]",
    "[R3]",
    "[R4]",
  ):
    print(
      f"{marker}: count={body.count(marker)}"
    )

  print()
  print("done")


if __name__ == "__main__":
  main()

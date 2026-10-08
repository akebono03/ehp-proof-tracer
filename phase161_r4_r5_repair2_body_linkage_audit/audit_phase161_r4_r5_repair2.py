from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPO_ROOT),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
)
from toda_group_proof_narrative_renderer import (
  _render_generic_narrative_step,
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


def _rule_name(
  proof_step,
) -> str:
  if proof_step.inference_rule is not None:
    return proof_step.inference_rule.name

  return proof_step.rule.value


def main():
  report = build_standard_toda_report(
    n=2,
    k=2,
  )
  result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    result,
    max_depth=3,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )

  print(
    "=" * 78
  )
  print(
    "Phase 161-R4-R5 repair2 body-linkage audit"
  )
  print(
    "=" * 78
  )
  print()

  print(
    "[Final public Narrative]"
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
    "[Body paragraphs containing Reference markers]"
  )
  for index, paragraph in enumerate(
    body.split(
      "\n\n"
    ),
    start=1,
  ):
    if "[R" in paragraph:
      print(
        f"{index:02d}: {paragraph!r}"
      )

  print()
  print(
    "[Proposition 5.1 Reference entries before public filtering]"
  )

  prop51_entries = tuple(
    entry
    for entry in entries
    if entry.reference.locator
    == "Proposition 5.1"
  )

  for entry in prop51_entries:
    print(
      f"entry number={entry.number}"
    )

    for proof_step in entry.proof_steps:
      print(
        "  step "
        f"id={id(proof_step)} "
        f"rule={_rule_name(proof_step)!r}"
      )
      print(
        "    rendered="
        f"{_render_generic_narrative_step(proof_step)!r}"
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

  print()
  print(
    "[Consumer chains from Proposition 5.1 steps]"
  )

  for entry in prop51_entries:
    for proof_step in entry.proof_steps:
      queue = [
        (
          proof_step,
          0,
        ),
      ]
      visited = set()

      while queue:
        current, depth = queue.pop(
          0
        )
        current_id = id(
          current
        )

        if current_id in visited:
          continue

        visited.add(
          current_id
        )

        reference_value = (
          extract_toda_group_proof_step_literature_reference(
            current
          )
        )

        print(
          "  "
          + "  " * depth
          + f"id={current_id} "
          + f"rule={_rule_name(current)!r} "
          + "ref="
          + (
            repr(
              reference_value.locator
            )
            if reference_value is not None
            else "None"
          )
        )
        print(
          "  "
          + "  " * depth
          + "rendered="
          + repr(
            _render_generic_narrative_step(
              current
            )
          )
        )

        if depth >= 3:
          continue

        for consumer in consumers_by_step_id.get(
          current_id,
          (),
        ):
          queue.append(
            (
              consumer,
              depth + 1,
            )
          )

  print()
  print(
    "[Diagnostics]"
  )
  print(
    "R2 occurrences in body:",
    body.count(
      "[R2]"
    ),
  )
  print(
    "pi_4^3 paragraph:",
    next(
      (
        paragraph
        for paragraph in body.split(
          "\n\n"
        )
        if (
          r"\pi_{4}^{3} = "
          r"\mathbb{Z}/2\{\eta_{3}\}"
          in paragraph
        )
      ),
      None,
    ),
  )

  print()
  print(
    "Audit completed. Production changes: NONE"
  )


if __name__ == "__main__":
  main()

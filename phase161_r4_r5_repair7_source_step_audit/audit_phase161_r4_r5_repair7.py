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
from toda_group_proof_narrative_contribution_renderer import (
  _phase154_r5_reference_source_steps_by_number,
  _phase154_r5_unique_visible_non_root_consumer_line,
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
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


def _rule_name(
  step,
) -> str:
  if step.inference_rule is None:
    return step.rule.value

  return step.inference_rule.name


def _reference_locator(
  step,
):
  reference = (
    extract_toda_group_proof_step_literature_reference(
      step
    )
  )

  if reference is None:
    return None

  return reference.locator


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
  sources_by_number = (
    _phase154_r5_reference_source_steps_by_number(
      presentation,
      entries,
    )
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )
  body = rendered.split(
    "---",
    1,
  )[1]

  print(
    "=" * 78
  )
  print(
    "Phase 161-R4-R5 repair7 source-step audit"
  )
  print(
    "=" * 78
  )

  print()
  print(
    "[All reference entries]"
  )

  for entry in entries:
    print(
      f"R{entry.number}: "
      f"{entry.reference.locator}"
    )

    for step in entry.proof_steps:
      print(
        "  entry step "
        f"id={id(step)} "
        f"rule={_rule_name(step)!r} "
        f"ref={_reference_locator(step)!r}"
      )
      print(
        "    rendered="
        f"{_render_generic_narrative_step(step)!r}"
      )

  prop51_entries = tuple(
    entry
    for entry in entries
    if entry.reference.locator
    == "Proposition 5.1"
  )

  print()
  print(
    "[Proposition 5.1 source steps]"
  )

  for entry in prop51_entries:
    source_steps = sources_by_number.get(
      entry.number,
      (),
    )

    print(
      f"entry R{entry.number}"
    )

    for step in source_steps:
      print(
        "  source "
        f"id={id(step)} "
        f"rule={_rule_name(step)!r} "
        f"ref={_reference_locator(step)!r}"
      )
      print(
        "    rendered="
        f"{_render_generic_narrative_step(step)!r}"
      )

    consumer_line = (
      _phase154_r5_unique_visible_non_root_consumer_line(
        presentation,
        source_steps,
        body,
      )
    )

    print(
      "  consumer_line=",
      repr(
        consumer_line
      ),
    )

  print()
  print(
    "[Relevant graph nodes]"
  )

  for node in presentation.nodes:
    step = node.proof_step
    rendered_step = (
      _render_generic_narrative_step(
        step
      )
    )

    if (
      "Proposition 5.1"
      in _rule_name(step)
      or "pi_4^3"
      in _rule_name(step)
      or r"\pi_{4}^{3}"
      in rendered_step
      or r"\pi_{n + 1}^{n}"
      in rendered_step
    ):
      print(
        f"id={id(step)} "
        f"rule={_rule_name(step)!r} "
        f"ref={_reference_locator(step)!r}"
      )
      print(
        "  rendered="
        f"{rendered_step!r}"
      )
      print(
        "  premises=",
        tuple(
          (
            id(premise),
            _rule_name(premise),
          )
          for premise in step.premises
          if hasattr(
            premise,
            "conclusion",
          )
        ),
      )

  print()
  print(
    "[Final body]"
  )
  print(
    body
  )

  print()
  print(
    "Audit completed. Production changes: NONE"
  )


if __name__ == "__main__":
  main()

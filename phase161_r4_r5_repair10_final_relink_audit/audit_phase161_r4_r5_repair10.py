from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPO_ROOT),
  )


import toda_group_proof_narrative_contribution_renderer as contribution_renderer
import toda_group_proof_narrative_renderer as narrative_renderer

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_references import (
  extract_toda_group_proof_step_literature_reference,
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


def _interesting_lines(
  body: str,
) -> tuple[str, ...]:
  return tuple(
    line
    for line in body.splitlines()
    if (
      "[R" in line
      or r"\pi_{n + 1}^{n}" in line
      or r"\pi_{4}^{3}" in line
    )
  )


def _entry_summary(
  entries,
):
  return tuple(
    (
      entry.number,
      entry.reference.locator,
      tuple(
        (
          _rule_name(
            step
          ),
          _reference_locator(
            step
          ),
          contribution_renderer._render_generic_narrative_step(
            step
          ),
        )
        for step in entry.proof_steps
      ),
    )
    for entry in entries
  )


def main():
  original = (
    contribution_renderer
    .link_toda_group_proof_narrative_reference_body_consumers
  )
  call_count = 0

  def wrapped(
    presentation,
    body_markdown,
    reference_entries,
  ):
    nonlocal call_count
    call_count += 1

    print()
    print(
      "=" * 78
    )
    print(
      f"REFERENCE BODY CONSUMER CALL {call_count} BEFORE"
    )
    print(
      "=" * 78
    )

    print(
      "entries:"
    )
    for summary in _entry_summary(
      reference_entries
    ):
      print(
        " ",
        summary,
      )

    sources_by_number = (
      contribution_renderer
      ._phase154_r5_reference_source_steps_by_number(
        presentation,
        reference_entries,
      )
    )

    print(
      "source/consumer:"
    )

    for entry in reference_entries:
      source_steps = sources_by_number.get(
        entry.number,
        (),
      )
      consumer = (
        contribution_renderer
        ._phase154_r5_unique_visible_non_root_consumer_line(
          presentation,
          source_steps,
          body_markdown,
        )
      )

      print(
        f"  R{entry.number} "
        f"{entry.reference.locator}: "
        f"consumer={consumer!r}"
      )

      for step in source_steps:
        print(
          "    source "
          f"rule={_rule_name(step)!r} "
          f"ref={_reference_locator(step)!r} "
          "rendered="
          f"{contribution_renderer._render_generic_narrative_step(step)!r}"
        )

    print(
      "body interesting lines BEFORE:"
    )
    for line in _interesting_lines(
      body_markdown
    ):
      print(
        "  ",
        line,
      )

    result = original(
      presentation,
      body_markdown,
      reference_entries,
    )

    print(
      "body interesting lines AFTER:"
    )
    for line in _interesting_lines(
      result
    ):
      print(
        "  ",
        line,
      )

    return result

  contribution_renderer.link_toda_group_proof_narrative_reference_body_consumers = (
    wrapped
  )
  narrative_renderer.link_toda_group_proof_narrative_reference_body_consumers = (
    wrapped
  )

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
  presentation = build_toda_group_proof_presentation(
    replay
  )

  print()
  print(
    "#" * 78
  )
  print(
    "START FINAL PUBLIC RENDER"
  )
  print(
    "#" * 78
  )

  rendered = (
    narrative_renderer
    .render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  print()
  print(
    "#" * 78
  )
  print(
    "FINAL PUBLIC NARRATIVE"
  )
  print(
    "#" * 78
  )
  print(
    rendered
  )

  print()
  print(
    "#" * 78
  )
  print(
    "FINAL DIAGNOSTICS"
  )
  print(
    "#" * 78
  )
  print(
    "Reference-body consumer calls:",
    call_count,
  )

  reference, body = rendered.split(
    "---",
    1,
  )

  print(
    "Final Proposition 5.1 header:",
    next(
      (
        line
        for line in reference.splitlines()
        if "Proposition 5.1" in line
      ),
      None,
    ),
  )
  print(
    "Final body general Prop.5.1 count:",
    body.count(
      r"\pi_{n + 1}^{n}"
    ),
  )
  print(
    "Final body pi_4^3 paragraphs:",
    tuple(
      paragraph
      for paragraph in body.split(
        "\n\n"
      )
      if r"\pi_{4}^{3}" in paragraph
    ),
  )

  print()
  print(
    "Audit completed. Production changes: NONE"
  )


if __name__ == "__main__":
  main()

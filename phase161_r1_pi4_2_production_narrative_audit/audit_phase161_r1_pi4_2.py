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
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
  build_toda_group_result_proof_replay,
)


def _rule_name(
  step,
) -> str:
  inference_rule = getattr(
    step,
    "inference_rule",
    None,
  )

  if inference_rule is not None:
    name = getattr(
      inference_rule,
      "name",
      None,
    )
    if name:
      return str(
        name
      )

  rule = getattr(
    step,
    "rule",
    None,
  )
  return str(
    rule
  )


def _reference_locator(
  step,
) -> str:
  inference_rule = getattr(
    step,
    "inference_rule",
    None,
  )

  if inference_rule is None:
    return "-"

  reference = getattr(
    inference_rule,
    "literature_reference",
    None,
  )

  if reference is None:
    return "-"

  locator = getattr(
    reference,
    "locator",
    None,
  )

  if locator is None:
    return "-"

  return str(
    locator
  )


def _source_entry_field(
  source_entry,
  name,
):
  value = getattr(
    source_entry,
    name,
    None,
  )

  if value is None:
    return "-"

  return value


def _print_step(
  label,
  step,
  depth=None,
  role=None,
):
  print(
    label
  )

  if depth is not None:
    print(
      "  depth:",
      depth,
    )

  if role is not None:
    print(
      "  role:",
      role,
    )

  print(
    "  rule:",
    _rule_name(
      step
    ),
  )
  print(
    "  reference:",
    _reference_locator(
      step
    ),
  )
  print(
    "  conclusion type:",
    type(
      step.conclusion
    ).__name__,
  )
  print(
    "  conclusion:",
    repr(
      step.conclusion
    ),
  )
  print(
    "  direct premises:",
    len(
      step.premises
    ),
  )


def _section(
  title,
):
  print()
  print(
    "=" * 78
  )
  print(
    title
  )
  print(
    "=" * 78
  )


def main():
  report = build_standard_toda_report(
    n=2,
    k=2,
  )

  if not report.candidates:
    raise RuntimeError(
      "No production candidate was found for pi_4^2."
    )

  candidate = report.candidates[
    0
  ]
  source_candidate = (
    candidate.source_candidate
  )
  result = (
    source_candidate.group_result
  )
  root = result.proof_step

  _section(
    "Phase 161-R1 / pi_4^2 production result"
  )

  print(
    "candidate count:",
    len(
      report.candidates
    ),
  )
  print(
    "target:",
    repr(
      result.target
    ),
  )
  print(
    "group structure:",
    repr(
      result.group_structure
    ),
  )
  print(
    "generators:",
    repr(
      result.generators
    ),
  )
  print(
    "generator orders:",
    repr(
      result.generator_orders
    ),
  )

  source_entry = result.source_entry

  print(
    "source theorem:",
    _source_entry_field(
      source_entry,
      "theorem",
    ),
  )
  print(
    "source phase:",
    _source_entry_field(
      source_entry,
      "phase",
    ),
  )
  print(
    "source repository key:",
    _source_entry_field(
      source_entry,
      "repository_key",
    ),
  )

  _section(
    "Root proof step"
  )
  _print_step(
    "ROOT",
    root,
  )

  _section(
    "Direct root premises"
  )

  for index, premise in enumerate(
    root.premises,
    start=1,
  ):
    _print_step(
      f"P{index}",
      premise,
    )

  _section(
    "Complete production provenance"
  )

  complete_replay = (
    build_complete_toda_group_result_proof_replay(
      result
    )
  )

  print(
    "complete replay max depth:",
    complete_replay.max_depth,
  )
  print(
    "complete replay step count:",
    len(
      complete_replay.steps
    ),
  )

  for index, replay_step in enumerate(
    complete_replay.steps,
    start=1,
  ):
    _print_step(
      f"S{index}",
      replay_step.proof_step,
      depth=replay_step.depth,
      role=replay_step.role,
    )

  _section(
    "Public Narrative using current standard depth=2 presentation"
  )

  replay = build_toda_group_result_proof_replay(
    result,
    max_depth=2,
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  print(
    rendered
  )

  _section(
    "Narrative diagnostics"
  )

  checks = (
    (
      "target result",
      r"\pi_{4}^{2}",
    ),
    (
      "expected generator eta2 eta3",
      r"\eta_{2}\eta_{3}",
    ),
    (
      "Toda (5.2) locator",
      "(5.2)",
    ),
    (
      "Proposition 4.4 locator",
      "Proposition 4.4",
    ),
    (
      "proof heading",
      "## 証明",
    ),
    (
      "QED",
      "□",
    ),
  )

  for label, fragment in checks:
    print(
      f"{label}:",
      fragment in rendered,
    )

  print()
  print(
    "AUDIT COMPLETE"
  )
  print(
    "No production source file was modified."
  )


if __name__ == "__main__":
  main()

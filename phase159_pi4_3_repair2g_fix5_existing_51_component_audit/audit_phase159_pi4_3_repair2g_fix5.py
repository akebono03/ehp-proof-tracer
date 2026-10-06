from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      ROOT
    ),
  )

from toda_calculation_facade import (
  build_standard_toda_report,
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
from toda_literature_statement_boundary import (
  classify_toda_literature_statement_step,
  get_toda_fixed_statement_components,
)
from toda_proof_dependency import (
  extract_toda_recursive_proof_provenance,
)


def _rule_name(
  step,
) -> str | None:
  if step.inference_rule is None:
    return None

  return step.inference_rule.name


def _reference_locator(
  step,
) -> str | None:
  reference = (
    extract_toda_group_proof_step_literature_reference(
      step
    )
  )

  if reference is None:
    return None

  return reference.locator


def _boundary_text(
  step,
) -> str:
  boundary = (
    classify_toda_literature_statement_step(
      step
    )
  )

  if boundary is None:
    return "NONE"

  return (
    boundary.classification.value
    + " / "
    + boundary.reference_locator
    + " / "
    + str(
      boundary.component_key
    )
  )


def _group_data(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
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
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  provenance = (
    extract_toda_recursive_proof_provenance(
      group_result
    )
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      raw
    )
  )

  return (
    group_result,
    raw,
    closure,
    provenance,
    rendered,
  )


def _print_51_steps(
  title: str,
  steps,
) -> None:
  print(
    title
  )

  matches = []

  for step in steps:
    locator = _reference_locator(
      step
    )
    boundary = (
      classify_toda_literature_statement_step(
        step
      )
    )

    if (
      locator != "(5.1)"
      and (
        boundary is None
        or boundary.reference_locator != "(5.1)"
      )
    ):
      continue

    matches.append(
      step
    )

  print(
    "count:",
    len(
      matches
    ),
  )

  for index, step in enumerate(
    matches,
    start=1,
  ):
    print(
      f"[{index}] type={type(step.conclusion).__name__}"
    )
    print(
      "    rule:",
      _rule_name(
        step
      ),
    )
    print(
      "    reference:",
      _reference_locator(
        step
      ),
    )
    print(
      "    boundary:",
      _boundary_text(
        step
      ),
    )
    print(
      "    conclusion:",
      repr(
        step.conclusion
      ),
    )


def _print_reference_entries(
  title: str,
  presentation,
) -> None:
  print(
    title
  )

  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )

  print(
    "entry count:",
    len(
      entries
    ),
  )

  for entry in entries:
    print(
      f"[R{entry.number}] locator={entry.reference.locator} "
      f"steps={len(entry.proof_steps)}"
    )

    for step in entry.proof_steps:
      print(
        "    ",
        type(
          step.conclusion
        ).__name__,
        "|",
        _boundary_text(
          step
        ),
        "|",
        _rule_name(
          step
        ),
      )


def _audit_group(
  n: int,
  k: int,
  label: str,
) -> None:
  (
    group_result,
    raw,
    closure,
    provenance,
    rendered,
  ) = _group_data(
    n,
    k,
  )

  print()
  print(
    "=" * 72
  )
  print(
    label
  )
  print(
    "=" * 72
  )
  print(
    "raw nodes:",
    len(
      raw.nodes
    ),
  )
  print(
    "closure nodes:",
    len(
      closure.nodes
    ),
  )
  print(
    "provenance nodes:",
    len(
      provenance.nodes
    ),
  )

  _print_51_steps(
    "-- recursive provenance (5.1) steps --",
    tuple(
      node.proof_step
      for node in provenance.nodes
    ),
  )

  _print_51_steps(
    "-- raw depth2 (5.1) steps --",
    tuple(
      node.proof_step
      for node in raw.nodes
    ),
  )

  _print_51_steps(
    "-- closure depth2 (5.1) steps --",
    tuple(
      node.proof_step
      for node in closure.nodes
    ),
  )

  _print_reference_entries(
    "-- raw reference entries --",
    raw,
  )

  _print_reference_entries(
    "-- closure reference entries --",
    closure,
  )

  print(
    "-- public Narrative --"
  )
  print(
    rendered
  )


def main() -> int:
  print(
    "Phase159 pi_4^3 repair2g fix5 audit"
  )
  print(
    "Production code changes: NONE"
  )
  print(
    "Existing test changes: NONE"
  )
  print()

  print(
    "=== active (5.1) fixed components ==="
  )

  components = (
    get_toda_fixed_statement_components(
      "(5.1)"
    )
  )

  for index, component in enumerate(
    components,
    start=1,
  ):
    print(
      f"[{index}] key={component.component_key} "
      f"role={component.statement_role.value} "
      f"order={component.order}"
    )

  _audit_group(
    2,
    1,
    "pi_3^2",
  )
  _audit_group(
    3,
    1,
    "pi_4^3",
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

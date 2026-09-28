from difflib import unified_diff

from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  _context,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)


def _occurrence_count(text, fragment):
  if not fragment:
    return 0
  return text.count(fragment)


def main():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)

  base = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )
  ordered = build_toda_group_proof_narrative_ordered_contributions(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
    current_markdown=base,
  )
  connected = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  populated = tuple(
    (argument_index, rows)
    for argument_index, rows in enumerate(ordered)
    if rows
  )

  print("=" * 78)
  print("Phase 144-6-R5-43-1 pi_6^3 connected Narrative output audit")
  print("production changes: none")
  print("=" * 78)
  print()
  print("A. Summary")
  print("-" * 78)
  print(f"arguments={len(arguments)}")
  print(f"populated_arguments={len(populated)}")
  print(f"contributions={sum(len(rows) for _, rows in populated)}")
  print(f"base_chars={len(base)}")
  print(f"connected_chars={len(connected)}")
  print(f"delta_chars={len(connected) - len(base)}")
  print()

  print("B. Contribution inventory")
  print("-" * 78)
  for argument_index, rows in populated:
    conclusion = extract_toda_group_proof_narrative_argument_conclusion_step(
      arguments[argument_index]
    )
    conclusion_line = (
      ""
      if conclusion is None
      else _render_generic_narrative_step(conclusion)
    )
    print(
      f"argument={argument_index} "
      f"role={arguments[argument_index].role.value} "
      f"count={len(rows)}"
    )
    print(f"conclusion={conclusion_line}")
    for position, row in enumerate(rows, start=1):
      line = _render_generic_narrative_step(row.proof_step)
      connected_index = connected.find(line)
      conclusion_index = connected.find(conclusion_line)
      print(
        f"C{position}: "
        f"placement={row.placement.value} "
        f"provider_anchor={row.provider_anchor} "
        f"occurrences={_occurrence_count(connected, line)} "
        f"before_conclusion={connected_index < conclusion_index}"
      )
      print(f"  {line}")
  print()

  print("C. Base -> connected unified diff")
  print("-" * 78)
  diff = unified_diff(
    base.splitlines(),
    connected.splitlines(),
    fromfile="pi6_base",
    tofile="pi6_connected",
    lineterm="",
  )
  for line in diff:
    print(line)
  print()

  print("D. Connected Narrative full text")
  print("-" * 78)
  print(connected)
  print()

  print("E. Mechanical checks")
  print("-" * 78)
  checks = []
  checks.append(("connected_differs_from_base", connected != base))
  checks.append(("exactly_one_populated_argument", len(populated) == 1))
  checks.append((
    "exactly_five_contributions",
    sum(len(rows) for _, rows in populated) == 5,
  ))

  for argument_index, rows in populated:
    conclusion = extract_toda_group_proof_narrative_argument_conclusion_step(
      arguments[argument_index]
    )
    conclusion_line = _render_generic_narrative_step(conclusion)
    contribution_lines = tuple(
      _render_generic_narrative_step(row.proof_step)
      for row in rows
    )
    positions = tuple(connected.find(line) for line in contribution_lines)
    checks.append((
      "contribution_order_preserved",
      positions == tuple(sorted(positions)),
    ))
    checks.append((
      "all_contributions_present_once",
      all(
        _occurrence_count(connected, line) == 1
        for line in contribution_lines
      ),
    ))
    checks.append((
      "all_contributions_before_argument_conclusion",
      all(
        connected.find(line) < connected.find(conclusion_line)
        for line in contribution_lines
      ),
    ))

  for name, passed in checks:
    print(f"{name}: {'PASS' if passed else 'FAIL'}")

  if not all(passed for _, passed in checks):
    raise SystemExit(1)


if __name__ == "__main__":
  main()

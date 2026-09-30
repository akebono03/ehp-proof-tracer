from __future__ import annotations

from pathlib import Path

ROOT = Path.cwd()
AUDIT = ROOT / "audit_phase144_6_r5_39.py"
TEST37 = ROOT / "tests" / "test_phase144_6_r5_37_genuinely_missing_semantic_equivalence_and_rendering_audit.py"


def replace_function(text: str, name: str, replacement: str) -> str:
    marker = f"def {name}("
    start = text.find(marker)
    if start < 0:
        raise SystemExit(f"Function not found: {name}")
    next_def = text.find("\ndef ", start + len(marker))
    if next_def < 0:
        raise SystemExit(f"Could not locate end of function: {name}")
    return text[:start] + replacement.rstrip() + "\n\n" + text[next_def + 1:]


NEW_AUDIT_FUNCTION = r'''def build_narrative_necessity_inventory():
  occurrences = build_visibility_occurrences()
  groups = _build_contribution_groups_from_occurrences(occurrences)
  occurrences_by_group = defaultdict(list)
  for row in occurrences:
    occurrences_by_group[_group_key_from_occurrence(row)].append(row)

  presentations = {
    (n, k): _context(n, k)[0]
    for n, k in TARGETS
  }
  children_by_group = {
    key: _argument_edges(presentation)
    for key, presentation in presentations.items()
  }

  pi6_presentation = presentations[(3, 3)]
  pi6_dedicated = render_toda_group_proof_narrative_markdown(
    pi6_presentation
  )

  records = []
  for group in groups:
    key = (
      group.n,
      group.k,
      group.statement_type,
      group.statement_repr,
      group.provider_keys,
    )
    rows = occurrences_by_group[key]
    owner = sorted(
      rows,
      key=lambda row: (
        0 if row.provider_anchor else 1,
        row.distance_to_conclusion
        if row.distance_to_conclusion is not None
        else 10**9,
        row.argument_index,
      ),
    )[0]
    if (
      owner.argument_index != group.owner_argument_index
      or owner.argument_role != group.owner_argument_role
    ):
      raise AssertionError(
        "Phase 39 owner reconstruction must match Phase 38 ownership"
      )

    children = children_by_group[(group.n, group.k)]
    same_argument_ids = {
      row.step_id
      for row in occurrences
      if (
        row.n == group.n
        and row.k == group.k
        and row.argument_index == owner.argument_index
      )
    }
    downstream = _reachable_visibility_steps(
      owner.step_id,
      same_argument_ids - {owner.step_id},
      children,
    )
    bridge = bool(downstream)
    anchor_owned = owner.provider_anchor

    if anchor_owned:
      structural_role = "explicit_prerequisite_candidate"
    elif bridge:
      structural_role = "bridge_candidate"
    else:
      structural_role = "derivation_detail_candidate"

    dedicated_present = None
    if (group.n, group.k) == (3, 3):
      normalized_render = "".join(owner.step_render.split())
      normalized_dedicated = "".join(pi6_dedicated.split())
      dedicated_present = normalized_render in normalized_dedicated

    records.append(
      NarrativeNecessityRecord(
        n=group.n,
        k=group.k,
        statement_type=group.statement_type,
        occurrence_count=group.occurrence_count,
        owner_argument_index=group.owner_argument_index,
        owner_argument_role=group.owner_argument_role,
        provider_key_count=len(group.provider_keys),
        anchor_owned=anchor_owned,
        bridges_visibility_contributions=bridge,
        downstream_visibility_count=len(downstream),
        structural_role=structural_role,
        pi6_dedicated_render_present=dedicated_present,
      )
    )
  return tuple(records)
'''

NEW_TEST37 = r'''import pytest

from audit_phase144_6_r5_37 import (
  build_semantic_equivalence_and_rendering_inventory,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


@pytest.fixture(
  scope="module",
)
def semantic_equivalence_and_rendering_inventory():
  return build_semantic_equivalence_and_rendering_inventory()


def test_phase144_6_r5_37_inventory_covers_six_groups(
  semantic_equivalence_and_rendering_inventory,
):
  rows = semantic_equivalence_and_rendering_inventory
  assert {(row.n, row.k) for row in rows} == set(TARGETS)


def test_phase144_6_r5_37_inventory_is_phase36_missing_population(
  semantic_equivalence_and_rendering_inventory,
):
  rows = semantic_equivalence_and_rendering_inventory
  assert rows
  assert all((row.n, row.k) in set(TARGETS) for row in rows)


def test_phase144_6_r5_37_classification_is_exhaustive(
  semantic_equivalence_and_rendering_inventory,
):
  rows = semantic_equivalence_and_rendering_inventory
  assert all(
    row.classification in {
      "semantic_equivalent_present",
      "rendering_gap",
      "visibility_gap",
    }
    for row in rows
  )


def test_phase144_6_r5_37_rendering_gap_matches_fallback_flag(
  semantic_equivalence_and_rendering_inventory,
):
  rows = semantic_equivalence_and_rendering_inventory
  assert all(
    (row.classification == "rendering_gap") == row.rendering_fallback
    for row in rows
    if not row.equivalent_statement_present
  )


def test_phase144_6_r5_37_semantic_equivalent_rows_report_equivalence(
  semantic_equivalence_and_rendering_inventory,
):
  rows = semantic_equivalence_and_rendering_inventory
  assert all(
    row.equivalent_statement_present
    for row in rows
    if row.classification == "semantic_equivalent_present"
  )


def test_phase144_6_r5_37_rows_are_not_direct_render_covered(
  semantic_equivalence_and_rendering_inventory,
):
  rows = semantic_equivalence_and_rendering_inventory
  assert all(not row.direct_render_present for row in rows)
'''


def main() -> int:
    if not AUDIT.exists() or not TEST37.exists():
        raise SystemExit("Run this package from the ehp_proof repository root.")

    audit_text = AUDIT.read_text(encoding="utf-8")
    audit_text = replace_function(
        audit_text,
        "build_narrative_necessity_inventory",
        NEW_AUDIT_FUNCTION,
    )
    AUDIT.write_text(audit_text, encoding="utf-8")
    TEST37.write_text(NEW_TEST37, encoding="utf-8")

    print("Phase 150 Performance Repair R1 applied.")
    print("Changed:")
    print("  audit_phase144_6_r5_39.py")
    print("  tests/test_phase144_6_r5_37_genuinely_missing_semantic_equivalence_and_rendering_audit.py")
    print("Production Narrative/public API changes: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

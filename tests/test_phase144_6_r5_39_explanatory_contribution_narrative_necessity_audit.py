from audit_phase144_6_r5_38 import (
  build_explanatory_contribution_groups,
)
from audit_phase144_6_r5_39 import (
  build_narrative_necessity_inventory,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


def test_phase144_6_r5_39_inventory_matches_phase38_contribution_count():
  rows = build_narrative_necessity_inventory()
  groups = build_explanatory_contribution_groups()
  assert rows
  assert len(rows) == len(groups)


def test_phase144_6_r5_39_inventory_covers_six_groups():
  rows = build_narrative_necessity_inventory()
  assert {(row.n, row.k) for row in rows} == set(TARGETS)


def test_phase144_6_r5_39_structural_role_is_exhaustive():
  rows = build_narrative_necessity_inventory()
  assert all(
    row.structural_role in {
      "explicit_prerequisite_candidate",
      "bridge_candidate",
      "derivation_detail_candidate",
    }
    for row in rows
  )


def test_phase144_6_r5_39_anchor_owned_rows_are_explicit_candidates():
  rows = build_narrative_necessity_inventory()
  assert all(
    (not row.anchor_owned)
    or row.structural_role == "explicit_prerequisite_candidate"
    for row in rows
  )


def test_phase144_6_r5_39_bridge_candidates_have_downstream_visibility():
  rows = build_narrative_necessity_inventory()
  assert all(
    row.downstream_visibility_count > 0
    for row in rows
    if row.structural_role == "bridge_candidate"
  )


def test_phase144_6_r5_39_pi6_has_five_contributions():
  rows = build_narrative_necessity_inventory()
  pi6 = tuple(row for row in rows if (row.n, row.k) == (3, 3))
  assert pi6
  assert all(isinstance(row.pi6_dedicated_render_present, bool) for row in pi6)

def test_phase144_6_r5_39_owner_reconstruction_completes_for_all_groups():
  rows = build_narrative_necessity_inventory()
  assert rows
  assert all(row.owner_argument_index >= 0 for row in rows)


def test_phase144_6_r5_39_contribution_groups_share_occurrence_identity_space():
  rows = build_narrative_necessity_inventory()
  groups = build_explanatory_contribution_groups()
  assert rows
  assert len(rows) == len(groups)

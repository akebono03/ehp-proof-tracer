from audit_phase144_6_r5_28 import (
  MISSING_6_KEYS,
  build_missing6_owner_selection,
  build_missing6_ownership_candidates,
  build_six_group_ownership_inventory,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


def test_phase144_6_r5_28_finds_candidates_for_all_missing6_facts():
  candidates = build_missing6_ownership_candidates()

  assert {candidate.key for candidate in candidates} == set(MISSING_6_KEYS)


def test_phase144_6_r5_28_missing6_candidates_have_local_body_owner():
  candidates = build_missing6_ownership_candidates()

  assert all(candidate.in_local_body for candidate in candidates)


def test_phase144_6_r5_28_inventory_covers_all_six_groups():
  inventory = build_six_group_ownership_inventory()

  assert tuple((item.n, item.k) for item in inventory) == TARGETS


def test_phase144_6_r5_28_records_shared_local_body_steps():
  inventory = build_six_group_ownership_inventory()

  assert sum(item.multi_argument_step_identities for item in inventory) > 0


def test_phase144_6_r5_28_records_shared_provider_steps():
  inventory = build_six_group_ownership_inventory()

  assert sum(item.multi_provider_step_identities for item in inventory) > 0


def test_phase144_6_r5_28_hypothetical_rule_selects_one_owner_per_missing_fact():
  selected = build_missing6_owner_selection()

  assert set(selected) == set(MISSING_6_KEYS)
  assert all(owner is not None for owner in selected.values())

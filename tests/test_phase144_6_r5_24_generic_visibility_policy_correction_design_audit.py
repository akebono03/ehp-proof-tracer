from functools import lru_cache
from audit_phase144_6_r5_24 import (
  BodyLossStage,
  build_group_protection_impacts,
  build_visible_fact_body_traces,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


_uncached_build_group_protection_impacts = build_group_protection_impacts

@lru_cache(maxsize=1)
def build_group_protection_impacts():
  return _uncached_build_group_protection_impacts()


_uncached_build_visible_fact_body_traces = build_visible_fact_body_traces

@lru_cache(maxsize=1)
def build_visible_fact_body_traces():
  return _uncached_build_visible_fact_body_traces()


def test_phase144_6_r5_24_audits_all_six_representative_groups():
  impacts = build_group_protection_impacts()

  assert tuple((impact.n, impact.k) for impact in impacts) == TARGETS


def test_phase144_6_r5_24_reports_hypothetical_provider_release_counts():
  impacts = build_group_protection_impacts()

  assert all(impact.newly_released_steps >= 0 for impact in impacts)
  assert all(
    impact.protected_supporting_provider_steps >= 0
    for impact in impacts
  )


def test_phase144_6_r5_24_pi6_has_provider_steps_currently_hidden():
  impact = build_group_protection_impacts()[0]

  assert impact.newly_released_steps >= 1


def test_phase144_6_r5_24_traces_both_phase23_local_body_visible_hopf_facts():
  traces = build_visible_fact_body_traces()

  assert tuple(trace.key for trace in traces) == (
    "hopf_nu_prime",
    "hopf_nu_eta6",
  )


def test_phase144_6_r5_24_visible_hopf_facts_are_not_frontier_losses():
  traces = build_visible_fact_body_traces()

  assert all(not trace.frontier_hidden_arguments for trace in traces)
  assert all(trace.loss_stage is not BodyLossStage.FRONTIER for trace in traces)


def test_phase144_6_r5_24_classifies_post_frontier_loss_stage():
  traces = build_visible_fact_body_traces()

  assert all(isinstance(trace.loss_stage, BodyLossStage) for trace in traces)

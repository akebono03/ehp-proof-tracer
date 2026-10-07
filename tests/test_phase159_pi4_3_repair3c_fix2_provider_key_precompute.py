import inspect

import toda_group_proof_narrative_contribution_ordering as module


def test_phase159_repair3c_fix2_provider_keys_are_precomputed_once_per_argument():
  source = inspect.getsource(
    module._build_visibility_occurrences
  )

  assert (
    "_provider_keys_by_step_id("
    in source
  )
  assert (
    "provider_keys=provider_keys_by_step_id.get("
    in source
  )
  assert (
    "provider_keys=_provider_keys_for_step("
    not in source
  )


def test_phase159_repair3c_fix2_precompute_uses_one_chain_build_per_provider():
  source = inspect.getsource(
    module._provider_keys_by_step_id
  )

  assert (
    "for provider in proof_chain.providers:"
    in source
  )
  assert (
    "_anchored_chain_step_ids("
    in source
  )
  assert (
    "_necessity_for_chain("
    not in source
  )


def test_phase159_repair3c_fix2_legacy_provider_key_contract_is_unchanged():
  source = inspect.getsource(
    module._provider_keys_for_step
  )

  assert (
    "if step_id in chain_ids:"
    in source
  )
  assert (
    "_anchored_chain_step_ids("
    in source
  )
  assert (
    "_necessity_for_chain("
    not in source
  )

import inspect

import toda_group_proof_narrative_contribution_ordering as module


def test_phase159_repair3c_fix1_provider_keys_use_chain_membership_without_necessity_recomputation():
  source = inspect.getsource(
    module._provider_keys_for_step
  )

  assert (
    "_anchored_chain_step_ids("
    in source
  )
  assert (
    "_necessity_for_chain("
    not in source
  )
  assert (
    "if step_id in chain_ids:"
    in source
  )

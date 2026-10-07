from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
BACKUP_DIR = PACKAGE_DIR / "backup_before_fix2"

TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_ordering.py"
)
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi4_3_repair3c_fix2_provider_key_precompute.py"
)
TEST_SOURCE = (
  PACKAGE_DIR
  / "payload"
  / "tests"
  / TEST_TARGET.name
)

OLD_PROVIDER_KEYS = 'def _provider_keys_for_step(\n  presentation: TodaGroupProofPresentation,\n  local_body: tuple[TodaGroupProofNarrativeBlock, ...],\n  proof_chain: TodaGroupProofNarrativeProofChain,\n  conclusion_step: ProofStep,\n  step_id: int,\n) -> tuple[tuple[str, int], ...]:\n  keys = []\n\n  for provider in proof_chain.providers:\n    if provider.supporting_block is None:\n      continue\n\n    provider_chain = TodaGroupProofNarrativeProofChain(\n      argument_index=proof_chain.argument_index,\n      argument=proof_chain.argument,\n      providers=(\n        provider,\n      ),\n    )\n\n    (\n      chain_ids,\n      _anchors,\n      _distances,\n    ) = _anchored_chain_step_ids(\n      presentation,\n      local_body,\n      provider_chain,\n      conclusion_step,\n    )\n\n    if step_id in chain_ids:\n      keys.append(\n        _provider_key(\n          provider\n        )\n      )\n\n  return tuple(\n    keys\n  )\n'
NEW_PROVIDER_KEYS = 'def _provider_keys_for_step(\n  presentation: TodaGroupProofPresentation,\n  local_body: tuple[TodaGroupProofNarrativeBlock, ...],\n  proof_chain: TodaGroupProofNarrativeProofChain,\n  conclusion_step: ProofStep,\n  step_id: int,\n) -> tuple[tuple[str, int], ...]:\n  keys = []\n\n  for provider in proof_chain.providers:\n    if provider.supporting_block is None:\n      continue\n\n    provider_chain = TodaGroupProofNarrativeProofChain(\n      argument_index=proof_chain.argument_index,\n      argument=proof_chain.argument,\n      providers=(\n        provider,\n      ),\n    )\n\n    (\n      chain_ids,\n      _anchors,\n      _distances,\n    ) = _anchored_chain_step_ids(\n      presentation,\n      local_body,\n      provider_chain,\n      conclusion_step,\n    )\n\n    if step_id in chain_ids:\n      keys.append(\n        _provider_key(\n          provider\n        )\n      )\n\n  return tuple(\n    keys\n  )\n'
NEW_HELPER = 'def _provider_keys_by_step_id(\n  presentation: TodaGroupProofPresentation,\n  local_body: tuple[TodaGroupProofNarrativeBlock, ...],\n  proof_chain: TodaGroupProofNarrativeProofChain,\n  conclusion_step: ProofStep,\n) -> dict[int, tuple[tuple[str, int], ...]]:\n  keys_by_step_id = defaultdict(\n    list\n  )\n\n  for provider in proof_chain.providers:\n    if provider.supporting_block is None:\n      continue\n\n    provider_chain = TodaGroupProofNarrativeProofChain(\n      argument_index=proof_chain.argument_index,\n      argument=proof_chain.argument,\n      providers=(\n        provider,\n      ),\n    )\n\n    (\n      chain_ids,\n      _anchors,\n      _distances,\n    ) = _anchored_chain_step_ids(\n      presentation,\n      local_body,\n      provider_chain,\n      conclusion_step,\n    )\n\n    provider_key = _provider_key(\n      provider\n    )\n\n    for step_id in chain_ids:\n      keys_by_step_id[\n        step_id\n      ].append(\n        provider_key\n      )\n\n  return {\n    step_id: tuple(\n      provider_keys\n    )\n    for step_id, provider_keys\n    in keys_by_step_id.items()\n  }\n'
OLD_VISIBILITY_FRAGMENT = '    step_by_id = {\n      id(step): step\n      for block in local_body\n      for step in block.steps\n    }\n\n    for step_id in chain_ids & hidden_ids:\n'
NEW_VISIBILITY_FRAGMENT = '    step_by_id = {\n      id(step): step\n      for block in local_body\n      for step in block.steps\n    }\n    provider_keys_by_step_id = (\n      _provider_keys_by_step_id(\n        presentation,\n        local_body,\n        proof_chains[\n          argument_index\n        ],\n        conclusion_step,\n      )\n    )\n\n    for step_id in chain_ids & hidden_ids:\n'
OLD_OCCURRENCE_FRAGMENT = '          provider_keys=_provider_keys_for_step(\n            presentation,\n            local_body,\n            proof_chains[argument_index],\n            conclusion_step,\n            step_id,\n          ),\n'
NEW_OCCURRENCE_FRAGMENT = '          provider_keys=provider_keys_by_step_id.get(\n            step_id,\n            (),\n          ),\n'


def _replace_once(
  text,
  old,
  new,
  label,
):
  count = text.count(
    old
  )

  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one match, found {count}"
    )

  return text.replace(
    old,
    new,
    1,
  )


def main():
  if not TARGET.exists():
    raise FileNotFoundError(
      TARGET
    )

  text = TARGET.read_text(
    encoding="utf-8-sig",
  )

  if NEW_HELPER.strip() not in text:
    text = _replace_once(
      text,
      OLD_PROVIDER_KEYS,
      NEW_PROVIDER_KEYS
      + "\n\n"
      + NEW_HELPER,
      "provider-key helper insertion",
    )

  text = _replace_once(
    text,
    OLD_VISIBILITY_FRAGMENT,
    NEW_VISIBILITY_FRAGMENT,
    "visibility provider-key precompute insertion",
  )
  text = _replace_once(
    text,
    OLD_OCCURRENCE_FRAGMENT,
    NEW_OCCURRENCE_FRAGMENT,
    "visibility provider-key lookup",
  )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    TARGET,
    BACKUP_DIR
    / TARGET.name,
  )

  TARGET.write_text(
    text,
    encoding="utf-8",
  )

  if not TEST_SOURCE.exists():
    raise FileNotFoundError(
      TEST_SOURCE
    )

  TEST_TARGET.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    TEST_SOURCE,
    TEST_TARGET,
  )

  print(
    "Phase 159 repair3c fix2 applied."
  )
  print(
    "Modified:",
    TARGET.name,
  )
  print(
    "Added:",
    TEST_TARGET.relative_to(
      REPO_ROOT
    ),
  )


if __name__ == "__main__":
  main()

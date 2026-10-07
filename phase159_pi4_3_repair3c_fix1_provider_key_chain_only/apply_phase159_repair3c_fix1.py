from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
BACKUP_DIR = PACKAGE_DIR / "backup_before_fix1"

TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_ordering.py"
)
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi4_3_repair3c_fix1_provider_key_chain_only.py"
)
TEST_SOURCE = (
  PACKAGE_DIR
  / "payload"
  / "tests"
  / TEST_TARGET.name
)

OLD = 'def _provider_keys_for_step(\n  presentation: TodaGroupProofPresentation,\n  local_body: tuple[TodaGroupProofNarrativeBlock, ...],\n  proof_chain: TodaGroupProofNarrativeProofChain,\n  conclusion_step: ProofStep,\n  step_id: int,\n) -> tuple[tuple[str, int], ...]:\n  keys = []\n  for provider in proof_chain.providers:\n    if provider.supporting_block is None:\n      continue\n    provider_chain = TodaGroupProofNarrativeProofChain(\n      argument_index=proof_chain.argument_index,\n      argument=proof_chain.argument,\n      providers=(provider,),\n    )\n    chain_ids, _, _, _ = _necessity_for_chain(\n      presentation,\n      local_body,\n      provider_chain,\n      conclusion_step,\n    )\n    if step_id in chain_ids:\n      keys.append(_provider_key(provider))\n  return tuple(keys)\n'
NEW = 'def _provider_keys_for_step(\n  presentation: TodaGroupProofPresentation,\n  local_body: tuple[TodaGroupProofNarrativeBlock, ...],\n  proof_chain: TodaGroupProofNarrativeProofChain,\n  conclusion_step: ProofStep,\n  step_id: int,\n) -> tuple[tuple[str, int], ...]:\n  keys = []\n\n  for provider in proof_chain.providers:\n    if provider.supporting_block is None:\n      continue\n\n    provider_chain = TodaGroupProofNarrativeProofChain(\n      argument_index=proof_chain.argument_index,\n      argument=proof_chain.argument,\n      providers=(\n        provider,\n      ),\n    )\n\n    (\n      chain_ids,\n      _anchors,\n      _distances,\n    ) = _anchored_chain_step_ids(\n      presentation,\n      local_body,\n      provider_chain,\n      conclusion_step,\n    )\n\n    if step_id in chain_ids:\n      keys.append(\n        _provider_key(\n          provider\n        )\n      )\n\n  return tuple(\n    keys\n  )\n'


def main():
  if not TARGET.exists():
    raise FileNotFoundError(
      TARGET
    )

  text = TARGET.read_text(
    encoding="utf-8-sig",
  )

  count = text.count(
    OLD
  )

  if count != 1:
    raise RuntimeError(
      "_provider_keys_for_step replacement target "
      f"must match exactly once, found {count}"
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

  updated = text.replace(
    OLD,
    NEW,
    1,
  )

  TARGET.write_text(
    updated,
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
    "Phase 159 repair3c fix1 applied."
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

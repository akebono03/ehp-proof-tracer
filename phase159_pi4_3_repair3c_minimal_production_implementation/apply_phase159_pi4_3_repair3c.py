from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
PAYLOAD_DIR = PACKAGE_DIR / "payload"
BACKUP_DIR = PACKAGE_DIR / "backup_before_repair3c"

ORDERING_PATH = REPO_ROOT / "toda_group_proof_narrative_contribution_ordering.py"
GENERIC_RENDERER_PATH = REPO_ROOT / "toda_group_proof_generic_narrative_renderer.py"
TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi4_3_repair3c_provider_ancestry_contributions.py"
)

OLD_ANCHORED = 'def _anchored_chain_step_ids(\n  presentation: TodaGroupProofPresentation,\n  local_body: tuple[TodaGroupProofNarrativeBlock, ...],\n  proof_chain: TodaGroupProofNarrativeProofChain,\n  conclusion_step: ProofStep,\n) -> tuple[frozenset[int], frozenset[int], dict[int, int]]:\n  local_ids = {\n    id(step)\n    for block in local_body\n    for step in block.steps\n  }\n  anchors = _provider_anchor_step_ids(proof_chain) & local_ids\n  distances = _reverse_distances(presentation, conclusion_step)\n  parents = _parents_by_premise(presentation)\n  chain_ids = {id(conclusion_step)}\n  queue = deque(\n    step\n    for block in local_body\n    for step in block.steps\n    if id(step) in anchors\n  )\n  visited = set(anchors)\n\n  while queue:\n    step = queue.popleft()\n    step_id = id(step)\n    if step_id not in distances:\n      continue\n    chain_ids.add(step_id)\n    for parent in parents.get(step_id, ()):\n      parent_id = id(parent)\n      if parent_id not in local_ids:\n        continue\n      if parent_id not in distances:\n        continue\n      if distances[parent_id] >= distances[step_id]:\n        continue\n      chain_ids.add(parent_id)\n      if parent_id in visited:\n        continue\n      visited.add(parent_id)\n      queue.append(parent)\n\n  return frozenset(chain_ids), frozenset(anchors), distances\n'
NEW_ANCHORED = 'def _anchored_chain_step_ids(\n  presentation: TodaGroupProofPresentation,\n  local_body: tuple[TodaGroupProofNarrativeBlock, ...],\n  proof_chain: TodaGroupProofNarrativeProofChain,\n  conclusion_step: ProofStep,\n) -> tuple[frozenset[int], frozenset[int], dict[int, int]]:\n  local_ids = {\n    id(step)\n    for block in local_body\n    for step in block.steps\n  }\n  anchors = (\n    _provider_anchor_step_ids(\n      proof_chain\n    )\n    & local_ids\n  )\n  distances = _reverse_distances(\n    presentation,\n    conclusion_step,\n  )\n  parents = _parents_by_premise(\n    presentation\n  )\n  premises = _premises_by_parent(\n    presentation\n  )\n  chain_ids = {\n    id(\n      conclusion_step\n    )\n  }\n\n  downstream_queue = deque(\n    step\n    for block in local_body\n    for step in block.steps\n    if id(step) in anchors\n  )\n  downstream_visited = set(\n    anchors\n  )\n\n  while downstream_queue:\n    step = downstream_queue.popleft()\n    step_id = id(\n      step\n    )\n\n    if step_id not in distances:\n      continue\n\n    chain_ids.add(\n      step_id\n    )\n\n    for parent in parents.get(\n      step_id,\n      (),\n    ):\n      parent_id = id(\n        parent\n      )\n\n      if parent_id not in local_ids:\n        continue\n      if parent_id not in distances:\n        continue\n      if (\n        distances[\n          parent_id\n        ]\n        >= distances[\n          step_id\n        ]\n      ):\n        continue\n\n      chain_ids.add(\n        parent_id\n      )\n\n      if parent_id in downstream_visited:\n        continue\n\n      downstream_visited.add(\n        parent_id\n      )\n      downstream_queue.append(\n        parent\n      )\n\n  upstream_queue = deque(\n    step\n    for block in local_body\n    for step in block.steps\n    if id(step) in anchors\n  )\n  upstream_visited = set(\n    anchors\n  )\n\n  while upstream_queue:\n    step = upstream_queue.popleft()\n    step_id = id(\n      step\n    )\n\n    if step_id not in distances:\n      continue\n\n    for premise in premises.get(\n      step_id,\n      (),\n    ):\n      premise_id = id(\n        premise\n      )\n\n      if premise_id not in local_ids:\n        continue\n      if premise_id not in distances:\n        continue\n      if (\n        distances[\n          premise_id\n        ]\n        <= distances[\n          step_id\n        ]\n      ):\n        continue\n\n      chain_ids.add(\n        premise_id\n      )\n\n      if premise_id in upstream_visited:\n        continue\n\n      upstream_visited.add(\n        premise_id\n      )\n      upstream_queue.append(\n        premise\n      )\n\n  return (\n    frozenset(\n      chain_ids\n    ),\n    frozenset(\n      anchors\n    ),\n    distances,\n  )\n'
OLD_NECESSITY = 'def _necessity_for_chain(\n  presentation: TodaGroupProofPresentation,\n  local_body: tuple[TodaGroupProofNarrativeBlock, ...],\n  proof_chain: TodaGroupProofNarrativeProofChain,\n  conclusion_step: ProofStep,\n) -> tuple[\n  frozenset[int],\n  frozenset[int],\n  dict[int, int],\n  dict[int, tuple[int, ...]],\n]:\n  chain_ids, anchors, distances = _anchored_chain_step_ids(\n    presentation,\n    local_body,\n    proof_chain,\n    conclusion_step,\n  )\n  parents = _parents_by_premise(presentation)\n  conclusion_id = id(conclusion_step)\n  reachable_anchors = tuple(\n    anchor_id\n    for anchor_id in anchors\n    if _can_reach_conclusion(\n      anchor_id,\n      conclusion_id,\n      parents,\n      chain_ids,\n    )\n  )\n  necessity = {}\n  for step_id in chain_ids:\n    necessity[step_id] = tuple(\n      anchor_id\n      for anchor_id in reachable_anchors\n      if (\n        step_id != anchor_id\n        and not _can_reach_conclusion(\n          anchor_id,\n          conclusion_id,\n          parents,\n          chain_ids,\n          removed_id=step_id,\n        )\n      )\n    )\n  return chain_ids, anchors, distances, necessity\n'
NEW_NECESSITY = 'def _necessity_for_chain(\n  presentation: TodaGroupProofPresentation,\n  local_body: tuple[TodaGroupProofNarrativeBlock, ...],\n  proof_chain: TodaGroupProofNarrativeProofChain,\n  conclusion_step: ProofStep,\n) -> tuple[\n  frozenset[int],\n  frozenset[int],\n  dict[int, int],\n  dict[int, tuple[int, ...]],\n]:\n  (\n    chain_ids,\n    anchors,\n    distances,\n  ) = _anchored_chain_step_ids(\n    presentation,\n    local_body,\n    proof_chain,\n    conclusion_step,\n  )\n  parents = _parents_by_premise(\n    presentation\n  )\n  conclusion_id = id(\n    conclusion_step\n  )\n  reachable_anchors = tuple(\n    anchor_id\n    for anchor_id in anchors\n    if _can_reach_conclusion(\n      anchor_id,\n      conclusion_id,\n      parents,\n      chain_ids,\n    )\n  )\n  necessity = {}\n\n  for step_id in chain_ids:\n    required_by = []\n\n    for anchor_id in reachable_anchors:\n      if step_id == anchor_id:\n        continue\n\n      downstream_required = (\n        not _can_reach_conclusion(\n          anchor_id,\n          conclusion_id,\n          parents,\n          chain_ids,\n          removed_id=step_id,\n        )\n      )\n      upstream_prerequisite = (\n        _can_reach_conclusion(\n          step_id,\n          anchor_id,\n          parents,\n          chain_ids,\n        )\n      )\n\n      if (\n        downstream_required\n        or upstream_prerequisite\n      ):\n        required_by.append(\n          anchor_id\n        )\n\n    necessity[\n      step_id\n    ] = tuple(\n      required_by\n    )\n\n  return (\n    chain_ids,\n    anchors,\n    distances,\n    necessity,\n  )\n'
OLD_IMPORT_DELTA = '  TodaDeltaInjectiveStatement,\n  TodaDeltaKernelFreeCyclicStatement,\n'
NEW_IMPORT_DELTA = '  TodaDeltaImageFreeCyclicStatement,\n  TodaDeltaInjectiveStatement,\n  TodaDeltaKernelFreeCyclicStatement,\n'
OLD_IMPORT_SUSPENSION = '  TodaSuspensionInjectiveStatement,\n  TodaSuspensionIsomorphismStatement,\n  TodaSuspensionSurjectiveStatement,\n'
NEW_IMPORT_SUSPENSION = '  TodaSuspensionInjectiveStatement,\n  TodaSuspensionIsomorphismStatement,\n  TodaSuspensionKernelFreeCyclicStatement,\n  TodaSuspensionSurjectiveStatement,\n'
OLD_PROSE_TAIL = '  if isinstance(\n    statement,\n    _GENERIC_INJECTIVE_STATEMENT_TYPES,\n  ):\n'
NEW_PROSE_TAIL = '  if isinstance(\n    statement,\n    TodaDeltaImageFreeCyclicStatement,\n  ):\n    map_name = _generic_group_map_name(\n      statement.map\n    )\n\n    if map_name is None:\n      return None\n\n    return (\n      r"$\\operatorname{Im}"\n      + map_name\n      + " = "\n      + render_toda_raw_group_structure_latex(\n        statement.image_group\n      )\n      + "$."\n    )\n\n  if isinstance(\n    statement,\n    TodaSuspensionKernelFreeCyclicStatement,\n  ):\n    map_name = _generic_group_map_name(\n      statement.map\n    )\n\n    if map_name is None:\n      return None\n\n    return (\n      r"$\\ker "\n      + map_name\n      + " = "\n      + render_toda_raw_group_structure_latex(\n        statement.kernel_group\n      )\n      + "$."\n    )\n\n  if isinstance(\n    statement,\n    _GENERIC_INJECTIVE_STATEMENT_TYPES,\n  ):\n'


def _replace_once(text, old, new, label):
  count = text.count(old)
  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one match, found {count}"
    )
  return text.replace(old, new, 1)


def _backup(path):
  relative = path.relative_to(REPO_ROOT)
  destination = BACKUP_DIR / relative
  destination.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(path, destination)


def main():
  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  for target in (
    ORDERING_PATH,
    GENERIC_RENDERER_PATH,
  ):
    if not target.exists():
      raise FileNotFoundError(target)
    _backup(target)

  ordering = ORDERING_PATH.read_text(
    encoding="utf-8-sig",
  )
  ordering = _replace_once(
    ordering,
    OLD_ANCHORED,
    NEW_ANCHORED,
    "_anchored_chain_step_ids",
  )
  ordering = _replace_once(
    ordering,
    OLD_NECESSITY,
    NEW_NECESSITY,
    "_necessity_for_chain",
  )
  ORDERING_PATH.write_text(
    ordering,
    encoding="utf-8",
  )

  renderer = GENERIC_RENDERER_PATH.read_text(
    encoding="utf-8-sig",
  )
  renderer = _replace_once(
    renderer,
    OLD_IMPORT_DELTA,
    NEW_IMPORT_DELTA,
    "delta statement imports",
  )
  renderer = _replace_once(
    renderer,
    OLD_IMPORT_SUSPENSION,
    NEW_IMPORT_SUSPENSION,
    "suspension statement imports",
  )
  renderer = _replace_once(
    renderer,
    OLD_PROSE_TAIL,
    NEW_PROSE_TAIL,
    "semantic prose insertion",
  )
  GENERIC_RENDERER_PATH.write_text(
    renderer,
    encoding="utf-8",
  )

  source_test = (
    PAYLOAD_DIR
    / "tests"
    / TEST_PATH.name
  )
  if not source_test.exists():
    raise FileNotFoundError(source_test)

  TEST_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(source_test, TEST_PATH)

  print("Phase 159 pi_4^3 repair3c applied.")
  print("Modified:", ORDERING_PATH.name)
  print("Modified:", GENERIC_RENDERER_PATH.name)
  print("Added:", TEST_PATH.relative_to(REPO_ROOT))


if __name__ == "__main__":
  main()

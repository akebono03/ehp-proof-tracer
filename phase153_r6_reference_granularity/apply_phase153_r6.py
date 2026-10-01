from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent


def find_repository_root() -> Path:
  candidates = (
    PACKAGE_DIR.parent,
    Path.cwd(),
  )

  for candidate in candidates:
    if (
      (candidate / "toda_group_proof_narrative_references.py").is_file()
      and (
        candidate
        / "toda_group_proof_narrative_contribution_renderer.py"
      ).is_file()
      and (candidate / "tests").is_dir()
    ):
      return candidate.resolve()

  raise SystemExit(
    "EHP Proof Tracer repository root was not found."
  )


def replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(old)

  if count != 1:
    raise SystemExit(
      f"{label}: expected exactly one replacement target, "
      f"found {count}."
    )

  return text.replace(
    old,
    new,
    1,
  )


def patch_references(
  repo: Path,
) -> None:
  path = repo / "toda_group_proof_narrative_references.py"
  text = path.read_text(
    encoding="utf-8"
  )

  old = r'''def select_toda_group_proof_narrative_reference_statement_steps(
  entry: TodaGroupProofNarrativeReferenceEntry,
  candidate_steps: tuple[ProofStep, ...],
  proof_edges: tuple[TodaProofEdge, ...],
  root_step: ProofStep | None = None,
) -> tuple[ProofStep, ...]:
  if not isinstance(
    entry,
    TodaGroupProofNarrativeReferenceEntry,
  ):
    raise TypeError(
      "entry must be a "
      "TodaGroupProofNarrativeReferenceEntry"
    )

  if not isinstance(
    candidate_steps,
    tuple,
  ):
    raise TypeError(
      "candidate_steps must be a tuple"
    )

  if not all(
    isinstance(
      step,
      ProofStep,
    )
    for step in candidate_steps
  ):
    raise TypeError(
      "candidate_steps must contain only "
      "ProofStep objects"
    )

  if (
    root_step is not None
    and not isinstance(
      root_step,
      ProofStep,
    )
  ):
    raise TypeError(
      "root_step must be a ProofStep or None"
    )

  entry_step_ids = {
    id(
      step
    )
    for step in entry.proof_steps
  }
  seen_candidate_step_ids = set()

  for step in candidate_steps:
    step_id = id(
      step
    )

    if step_id not in entry_step_ids:
      raise ValueError(
        "candidate_steps must contain only "
        "steps from entry.proof_steps"
      )

    if step_id in seen_candidate_step_ids:
      raise ValueError(
        "candidate_steps must not contain "
        "the same ProofStep more than once"
      )

    seen_candidate_step_ids.add(
      step_id
    )

  if not isinstance(
    proof_edges,
    tuple,
  ):
    raise TypeError(
      "proof_edges must be a tuple"
    )

  if not all(
    isinstance(
      edge,
      TodaProofEdge,
    )
    for edge in proof_edges
  ):
    raise TypeError(
      "proof_edges must contain only "
      "TodaProofEdge objects"
    )

  eligible_candidates = tuple(
    step
    for step in candidate_steps
    if step is not root_step
  )

  if not eligible_candidates:
    return ()

  proof_used_step_ids = {
    id(
      edge.premise_step
    )
    for edge in proof_edges
  }

  proof_used_candidates = tuple(
    step
    for step in eligible_candidates
    if id(
      step
    ) in proof_used_step_ids
  )

  if proof_used_candidates:
    return proof_used_candidates

  return (
    eligible_candidates[0],
  )
'''

  new = r'''def select_toda_group_proof_narrative_reference_statement_steps(
  entry: TodaGroupProofNarrativeReferenceEntry,
  candidate_steps: tuple[ProofStep, ...],
  proof_edges: tuple[TodaProofEdge, ...],
  root_step: ProofStep | None = None,
) -> tuple[ProofStep, ...]:
  if not isinstance(
    entry,
    TodaGroupProofNarrativeReferenceEntry,
  ):
    raise TypeError(
      "entry must be a "
      "TodaGroupProofNarrativeReferenceEntry"
    )

  if not isinstance(
    candidate_steps,
    tuple,
  ):
    raise TypeError(
      "candidate_steps must be a tuple"
    )

  if not all(
    isinstance(
      step,
      ProofStep,
    )
    for step in candidate_steps
  ):
    raise TypeError(
      "candidate_steps must contain only "
      "ProofStep objects"
    )

  if (
    root_step is not None
    and not isinstance(
      root_step,
      ProofStep,
    )
  ):
    raise TypeError(
      "root_step must be a ProofStep or None"
    )

  entry_step_ids = {
    id(
      step
    )
    for step in entry.proof_steps
  }
  seen_candidate_step_ids = set()

  for step in candidate_steps:
    step_id = id(
      step
    )

    if step_id not in entry_step_ids:
      raise ValueError(
        "candidate_steps must contain only "
        "steps from entry.proof_steps"
      )

    if step_id in seen_candidate_step_ids:
      raise ValueError(
        "candidate_steps must not contain "
        "the same ProofStep more than once"
      )

    seen_candidate_step_ids.add(
      step_id
    )

  if not isinstance(
    proof_edges,
    tuple,
  ):
    raise TypeError(
      "proof_edges must be a tuple"
    )

  if not all(
    isinstance(
      edge,
      TodaProofEdge,
    )
    for edge in proof_edges
  ):
    raise TypeError(
      "proof_edges must contain only "
      "TodaProofEdge objects"
    )

  eligible_candidates = tuple(
    step
    for step in candidate_steps
    if step is not root_step
  )

  if not eligible_candidates:
    return ()

  boundary_used_step_ids = {
    id(
      edge.premise_step
    )
    for edge in proof_edges
    if (
      edge.premise_step
      is not root_step
      and extract_toda_group_proof_step_literature_reference(
        edge.premise_step
      )
      == entry.reference
      and extract_toda_group_proof_step_literature_reference(
        edge.parent_step
      )
      != entry.reference
    )
  }

  boundary_used_candidates = tuple(
    step
    for step in eligible_candidates
    if id(
      step
    ) in boundary_used_step_ids
  )

  if boundary_used_candidates:
    return boundary_used_candidates

  proof_used_step_ids = {
    id(
      edge.premise_step
    )
    for edge in proof_edges
  }

  proof_used_candidates = tuple(
    step
    for step in eligible_candidates
    if id(
      step
    ) in proof_used_step_ids
  )

  if proof_used_candidates:
    return proof_used_candidates

  return (
    eligible_candidates[0],
  )
'''

  patched = replace_once(
    text,
    old,
    new,
    "toda_group_proof_narrative_references.py",
  )

  path.write_text(
    patched,
    encoding="utf-8",
    newline="\n",
  )


def install_tests(
  repo: Path,
) -> None:
  source = (
    PACKAGE_DIR
    / "tests"
    / "test_phase153_r6_reference_granularity.py"
  )
  destination = (
    repo
    / "tests"
    / "test_phase153_r6_reference_granularity.py"
  )

  shutil.copy2(
    source,
    destination,
  )


def main() -> None:
  repo = find_repository_root()

  backup_dir = (
    repo
    / "phase153_r6_backup_before_apply"
  )
  backup_dir.mkdir(
    exist_ok=True
  )

  production_path = (
    repo
    / "toda_group_proof_narrative_references.py"
  )
  backup_path = (
    backup_dir
    / "toda_group_proof_narrative_references.py"
  )

  if not backup_path.exists():
    shutil.copy2(
      production_path,
      backup_path,
    )

  patch_references(
    repo
  )
  install_tests(
    repo
  )

  print(
    "Phase 153-R6 patch applied."
  )
  print(
    "Changed:"
  )
  print(
    "  toda_group_proof_narrative_references.py"
  )
  print(
    "Added:"
  )
  print(
    "  tests/test_phase153_r6_reference_granularity.py"
  )
  print(
    "Backup:"
  )
  print(
    "  phase153_r6_backup_before_apply/"
  )


if __name__ == "__main__":
  main()

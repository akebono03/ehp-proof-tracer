from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent


def find_repository_root() -> Path:
    candidates = [
        PACKAGE_DIR.parent,
        Path.cwd(),
    ]

    for candidate in candidates:
        if (
            (candidate / "toda_group_proof_narrative_references.py").is_file()
            and (candidate / "toda_group_proof_narrative_contribution_renderer.py").is_file()
            and (candidate / "tests").is_dir()
        ):
            return candidate.resolve()

    raise SystemExit(
        "EHP Proof Tracer repository root was not found. "
        "Extract this package directly under the repository root, "
        "or run it from the repository root."
    )


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"{label}: expected exactly one replacement target, found {count}."
        )
    return text.replace(old, new, 1)


def patch_references(repo: Path) -> None:
    path = repo / "toda_group_proof_narrative_references.py"
    text = path.read_text(encoding="utf-8")

    old = r'''def select_toda_group_proof_narrative_reference_statement_steps(
  entry: TodaGroupProofNarrativeReferenceEntry,
  candidate_steps: tuple[ProofStep, ...],
  proof_edges: tuple[TodaProofEdge, ...],
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

  if not candidate_steps:
    return ()

  proof_used_step_ids = {
    id(
      edge.premise_step
    )
    for edge in proof_edges
  }

  proof_used_candidates = tuple(
    step
    for step in candidate_steps
    if id(
      step
    ) in proof_used_step_ids
  )

  if proof_used_candidates:
    return proof_used_candidates

  return (
    candidate_steps[0],
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
    path.write_text(patched, encoding="utf-8", newline="\n")


def patch_contribution_renderer(repo: Path) -> None:
    path = repo / "toda_group_proof_narrative_contribution_renderer.py"
    text = path.read_text(encoding="utf-8")

    old = r'''      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
      )
'''

    new = r'''      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
'''

    patched = replace_once(
        text,
        old,
        new,
        "toda_group_proof_narrative_contribution_renderer.py",
    )
    path.write_text(patched, encoding="utf-8", newline="\n")


def install_test(repo: Path) -> None:
    source = PACKAGE_DIR / "tests" / "test_phase153_r5_reference_selection.py"
    destination = repo / "tests" / "test_phase153_r5_reference_selection.py"
    shutil.copy2(source, destination)


def main() -> None:
    repo = find_repository_root()

    backup_dir = repo / "phase153_r5_backup_before_apply"
    backup_dir.mkdir(exist_ok=True)

    for relative in (
        "toda_group_proof_narrative_references.py",
        "toda_group_proof_narrative_contribution_renderer.py",
    ):
        source = repo / relative
        destination = backup_dir / relative
        if not destination.exists():
            shutil.copy2(source, destination)

    patch_references(repo)
    patch_contribution_renderer(repo)
    install_test(repo)

    print("Phase 153-R5 patch applied.")
    print("Changed:")
    print("  toda_group_proof_narrative_references.py")
    print("  toda_group_proof_narrative_contribution_renderer.py")
    print("Added:")
    print("  tests/test_phase153_r5_reference_selection.py")
    print("Backup:")
    print("  phase153_r5_backup_before_apply/")


if __name__ == "__main__":
    main()

from pathlib import Path

TARGET = Path("toda_group_proof_narrative_references.py")
START = "def select_toda_group_proof_narrative_reference_statement_steps("
END = "\ndef filter_toda_group_proof_narrative_reference_entries_by_step_usage("

REPLACEMENT = 'def select_toda_group_proof_narrative_reference_statement_steps(\n  entry: TodaGroupProofNarrativeReferenceEntry,\n  candidate_steps: tuple[ProofStep, ...],\n  proof_edges: tuple[TodaProofEdge, ...],\n  root_step: ProofStep | None = None,\n) -> tuple[ProofStep, ...]:\n  if not isinstance(\n    entry,\n    TodaGroupProofNarrativeReferenceEntry,\n  ):\n    raise TypeError(\n      "entry must be a "\n      "TodaGroupProofNarrativeReferenceEntry"\n    )\n\n  if not isinstance(\n    candidate_steps,\n    tuple,\n  ):\n    raise TypeError(\n      "candidate_steps must be a tuple"\n    )\n\n  if not all(\n    isinstance(\n      step,\n      ProofStep,\n    )\n    for step in candidate_steps\n  ):\n    raise TypeError(\n      "candidate_steps must contain only "\n      "ProofStep objects"\n    )\n\n  if (\n    root_step is not None\n    and not isinstance(\n      root_step,\n      ProofStep,\n    )\n  ):\n    raise TypeError(\n      "root_step must be a ProofStep or None"\n    )\n\n  entry_step_ids = {\n    id(\n      step\n    )\n    for step in entry.proof_steps\n  }\n  seen_candidate_step_ids = set()\n\n  for step in candidate_steps:\n    step_id = id(\n      step\n    )\n\n    if step_id not in entry_step_ids:\n      raise ValueError(\n        "candidate_steps must contain only "\n        "steps from entry.proof_steps"\n      )\n\n    if step_id in seen_candidate_step_ids:\n      raise ValueError(\n        "candidate_steps must not contain "\n        "the same ProofStep more than once"\n      )\n\n    seen_candidate_step_ids.add(\n      step_id\n    )\n\n  if not isinstance(\n    proof_edges,\n    tuple,\n  ):\n    raise TypeError(\n      "proof_edges must be a tuple"\n    )\n\n  if not all(\n    isinstance(\n      edge,\n      TodaProofEdge,\n    )\n    for edge in proof_edges\n  ):\n    raise TypeError(\n      "proof_edges must contain only "\n      "TodaProofEdge objects"\n    )\n\n  eligible_candidates = tuple(\n    step\n    for step in candidate_steps\n    if step is not root_step\n  )\n\n  if not eligible_candidates:\n    return ()\n\n  boundary_used_step_ids = {\n    id(\n      edge.premise_step\n    )\n    for edge in proof_edges\n    if (\n      edge.premise_step\n      is not root_step\n      and extract_toda_group_proof_step_literature_reference(\n        edge.premise_step\n      )\n      == entry.reference\n      and extract_toda_group_proof_step_literature_reference(\n        edge.parent_step\n      )\n      != entry.reference\n    )\n  }\n\n  boundary_used_candidates = tuple(\n    step\n    for step in eligible_candidates\n    if id(\n      step\n    ) in boundary_used_step_ids\n  )\n\n  if boundary_used_candidates:\n    return boundary_used_candidates\n\n  entry_external_used_step_ids = {\n    id(\n      edge.premise_step\n    )\n    for edge in proof_edges\n    if id(\n      edge.parent_step\n    ) not in entry_step_ids\n  }\n\n  entry_external_used_candidates = tuple(\n    step\n    for step in eligible_candidates\n    if id(\n      step\n    ) in entry_external_used_step_ids\n  )\n\n  if entry_external_used_candidates:\n    return entry_external_used_candidates\n\n  return (\n    eligible_candidates[0],\n  )\n'


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    start = text.index(START)
    end = text.index(END, start)
    updated = text[:start] + REPLACEMENT + text[end:]
    TARGET.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()

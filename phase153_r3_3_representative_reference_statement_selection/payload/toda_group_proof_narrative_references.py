from dataclasses import dataclass
import re

from proof import (
  LiteratureReference,
  ProofStep,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_proof_dependency import (
  TodaProofEdge,
)


@dataclass(frozen=True)
class TodaGroupProofNarrativeReferenceEntry:
  number: int
  reference: LiteratureReference
  proof_steps: tuple[ProofStep, ...]

  def __post_init__(self) -> None:
    if isinstance(self.number, bool) or not isinstance(self.number, int):
      raise TypeError("number must be an int")
    if self.number <= 0:
      raise ValueError("number must be positive")
    if not isinstance(self.reference, LiteratureReference):
      raise TypeError("reference must be a LiteratureReference")
    if not isinstance(self.proof_steps, tuple):
      raise TypeError("proof_steps must be a tuple")
    if not self.proof_steps:
      raise ValueError("proof_steps must not be empty")
    if not all(isinstance(step, ProofStep) for step in self.proof_steps):
      raise TypeError("proof_steps must contain only ProofStep objects")


def _infer_toda_group_proof_literature_reference_from_rule_name(
  rule_name: str,
) -> LiteratureReference | None:
  if not isinstance(rule_name, str):
    raise TypeError("rule_name must be a str")

  named_match = re.match(
    r"^Toda (Proposition|Lemma|Theorem|Equation) ([0-9]+(?:\.[0-9]+)*)\b",
    rule_name,
  )
  if named_match is not None:
    kind, number = named_match.groups()
    locator = f"{kind} {number}"
    return LiteratureReference(
      label=f"Toda {locator}",
      locator=locator,
    )

  parenthesized_match = re.match(
    r"^Toda \(([0-9]+(?:\.[0-9]+)*)\)\b",
    rule_name,
  )
  if parenthesized_match is not None:
    number = parenthesized_match.group(1)
    locator = f"({number})"
    return LiteratureReference(
      label=f"Toda {locator}",
      locator=locator,
    )

  bare_equation_match = re.match(
    r"^Toda ([0-9]+\.[0-9]+)\b",
    rule_name,
  )
  if bare_equation_match is not None:
    number = bare_equation_match.group(1)
    locator = f"({number})"
    return LiteratureReference(
      label=f"Toda {locator}",
      locator=locator,
    )

  return None


def extract_toda_group_proof_step_literature_reference(
  proof_step: ProofStep,
) -> LiteratureReference | None:
  if not isinstance(proof_step, ProofStep):
    raise TypeError("proof_step must be a ProofStep")

  inference_rule = proof_step.inference_rule
  if inference_rule is None:
    return None

  if inference_rule.literature_reference is not None:
    return inference_rule.literature_reference

  return _infer_toda_group_proof_literature_reference_from_rule_name(
    inference_rule.name
  )


def build_toda_group_proof_narrative_reference_entries(
  presentation: TodaGroupProofPresentation,
) -> tuple[TodaGroupProofNarrativeReferenceEntry, ...]:
  if not isinstance(presentation, TodaGroupProofPresentation):
    raise TypeError("presentation must be a TodaGroupProofPresentation")

  references = []
  steps_by_reference = []

  for node in presentation.nodes:
    proof_step = node.proof_step
    reference = extract_toda_group_proof_step_literature_reference(
      proof_step
    )
    if reference is None:
      continue

    try:
      index = references.index(reference)
    except ValueError:
      references.append(reference)
      steps_by_reference.append([proof_step])
    else:
      steps_by_reference[index].append(proof_step)

  return tuple(
    TodaGroupProofNarrativeReferenceEntry(
      number=number,
      reference=reference,
      proof_steps=tuple(proof_steps),
    )
    for number, (reference, proof_steps) in enumerate(
      zip(references, steps_by_reference),
      start=1,
    )
  )


def select_toda_group_proof_narrative_reference_statement_steps(
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


def render_toda_group_proof_narrative_reference_entries_markdown(
  entries: tuple[TodaGroupProofNarrativeReferenceEntry, ...],
) -> str:
  if not isinstance(entries, tuple):
    raise TypeError("entries must be a tuple")
  if not entries:
    return ""

  lines = ["使用する結果を先にまとめる.", ""]

  for entry in entries:
    if not isinstance(entry, TodaGroupProofNarrativeReferenceEntry):
      raise TypeError(
        "entries must contain only "
        "TodaGroupProofNarrativeReferenceEntry objects"
      )
    title = entry.reference.locator or entry.reference.label
    lines.append(f"**[R{entry.number}] {title}.**")

  return "\n".join(lines)

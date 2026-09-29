from dataclasses import dataclass

from proof import (
  LiteratureReference,
  ProofStep,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
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


def extract_toda_group_proof_step_literature_reference(
  proof_step: ProofStep,
) -> LiteratureReference | None:
  if not isinstance(proof_step, ProofStep):
    raise TypeError("proof_step must be a ProofStep")
  if proof_step.inference_rule is None:
    return None
  return proof_step.inference_rule.literature_reference


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

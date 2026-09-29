from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8-sig")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"{path}: expected exactly one match, found {count}"
        )
    path.write_text(text.replace(old, new), encoding="utf-8")


def main() -> int:
    proof_path = ROOT / "proof.py"
    old = '''@dataclass(frozen=True)
class InferenceRule:
  name: str
  description: str | None = None
  premise_patterns: tuple[PremisePattern, ...] = ()
  conclusion_builder: Any = None
  conclusion_pattern: Any = None
  match_guard: Any = None
'''
    new = '''@dataclass(frozen=True)
class InferenceRule:
  name: str
  description: str | None = None
  premise_patterns: tuple[PremisePattern, ...] = ()
  conclusion_builder: Any = None
  conclusion_pattern: Any = None
  match_guard: Any = None
  literature_reference: LiteratureReference | None = None
'''
    replace_once(proof_path, old, new)

    (ROOT / "toda_group_proof_narrative_references.py").write_text(
'''from dataclasses import dataclass

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
''',
        encoding="utf-8",
    )

    (ROOT / "tests" / "test_phase144_6_r3_structured_references.py").write_text(
'''from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_group_proof_narrative_references import (
  TodaGroupProofNarrativeReferenceEntry,
  extract_toda_group_proof_step_literature_reference,
  render_toda_group_proof_narrative_reference_entries_markdown,
)


def test_phase144_6_r3_inference_rule_preserves_structured_literature_reference():
  reference = LiteratureReference(
    label="Toda Prop.5.1",
    author="H. Toda",
    title="Composition Methods in Homotopy Groups of Spheres",
    year=1962,
    locator="Proposition 5.1",
  )
  rule = InferenceRule(
    name="test rule",
    literature_reference=reference,
  )
  step = ProofStep(
    conclusion="test conclusion",
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=rule,
  )

  assert (
    extract_toda_group_proof_step_literature_reference(step)
    is reference
  )


def test_phase144_6_r3_step_without_structured_reference_remains_unreferenced():
  step = ProofStep(
    conclusion="test conclusion",
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name="Toda Proposition 5.1 text only",
    ),
  )

  assert extract_toda_group_proof_step_literature_reference(step) is None


def test_phase144_6_r3_reference_renderer_uses_structured_locator_not_rule_name():
  reference = LiteratureReference(
    label="Toda Prop.5.1",
    locator="Proposition 5.1",
  )
  step = ProofStep(
    conclusion="test conclusion",
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name="internal implementation name",
      literature_reference=reference,
    ),
  )
  entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=reference,
    proof_steps=(step,),
  )

  rendered = render_toda_group_proof_narrative_reference_entries_markdown(
    (entry,)
  )

  assert "**[R1] Proposition 5.1.**" in rendered
  assert "internal implementation name" not in rendered
''',
        encoding="utf-8",
    )

    print("Phase 144-6-R3 structured-reference foundation applied.")
    print("Changed: proof.py")
    print("Added: toda_group_proof_narrative_references.py")
    print("Added: tests/test_phase144_6_r3_structured_references.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

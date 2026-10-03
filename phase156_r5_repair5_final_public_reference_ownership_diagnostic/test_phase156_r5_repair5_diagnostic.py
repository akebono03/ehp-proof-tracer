from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_group_proof_narrative_references import (
  TodaGroupProofNarrativeReferenceEntry,
)
from phase156_r5_repair5_final_public_reference_ownership_diagnostic.diagnose_phase156_r5_repair5 import (
  _map_public_headers_to_entries,
  _proof_body_text,
  _public_headers,
)


def _entry(
  number: int,
  locator: str,
):
  reference = LiteratureReference(
    label=locator,
    locator=locator,
  )
  step = ProofStep(
    conclusion=locator,
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=locator,
      literature_reference=reference,
    ),
  )

  return TodaGroupProofNarrativeReferenceEntry(
    number=number,
    reference=reference,
    proof_steps=(
      step,
    ),
  )


def test_phase156_r5_repair5_maps_renumbered_public_header_by_title():
  entries = (
    _entry(
      1,
      "Proposition 5.15",
    ),
    _entry(
      2,
      "Lemma 5.13",
    ),
  )
  rendered = "\n".join(
    (
      "**[R1] Lemma 5.13.**",
      "$A = B$",
    )
  )
  headers = _public_headers(
    rendered
  )
  mapped, unmatched = (
    _map_public_headers_to_entries(
      headers,
      entries,
    )
  )

  assert unmatched == ()
  assert len(
    mapped
  ) == 1
  assert mapped[
    0
  ][
    1
  ] == 1
  assert mapped[
    0
  ][
    3
  ].number == 2


def test_phase156_r5_repair5_body_text_prefers_proof_heading():
  rendered = "\n".join(
    (
      "**[R1] Lemma 5.13.**",
      "$A = B$",
      "",
      "## 証明",
      "",
      "$C = D$",
    )
  )

  assert _proof_body_text(
    rendered,
    "**[R1] Lemma 5.13.**\n$A = B$",
  ) == "$C = D$"


def test_phase156_r5_repair5_body_text_removes_exact_raw_prefix():
  prefix = "\n".join(
    (
      "使用する結果を先にまとめる.",
      "",
      "**[R1] Lemma 5.13.**",
      "$A = B$",
    )
  )
  rendered = (
    prefix
    + "\n\n"
    + "まず, $C = D$."
  )

  assert _proof_body_text(
    rendered,
    prefix,
  ) == "まず, $C = D$."

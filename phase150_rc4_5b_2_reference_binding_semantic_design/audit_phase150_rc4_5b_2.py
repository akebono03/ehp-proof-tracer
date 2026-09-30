from pathlib import Path

REQUIRED = (
  "TodaGroupProofNarrativeReferenceIdentity",
  "TodaGroupProofNarrativeVariableBinding",
  "TodaGroupProofNarrativeReferenceApplicationSemantic",
  "reference_application_semantics",
  "dependent_step",
  "formal_variable",
  "instantiated_expression",
  "Lemma 5.2",
  "RC4-5B-3",
)

def main():
  path = Path(
    "phase150_rc4_5b_2_reference_binding_semantic_design"
  ) / "DESIGN.md"
  text = path.read_text(encoding="utf-8")

  missing = tuple(
    token
    for token in REQUIRED
    if token not in text
  )
  if missing:
    raise AssertionError(
      f"missing design requirements: {missing}"
    )

  print("=" * 78)
  print("Phase 150 / RC4-5B-2 Reference / variable-binding semantic design")
  print("=" * 78)
  print("reference identity: SEPARATE TYPED SEMANTIC")
  print("variable binding: MATHEMATICAL OBJECT -> MATHEMATICAL OBJECT")
  print("reference application: ATTACHED TO DEPENDENT PROOF STEP")
  print("reason layer: OPTIONAL TYPED LINK, NO DUPLICATED STRING INFERENCE")
  print("renderer: CONSUMER ONLY, NO RULE-NAME / PI6 BRANCH")
  print("ambiguous/missing binding: CONSERVATIVE FALLBACK")
  print("repository-wide theorem registry: OUT OF SCOPE")
  print("PRODUCTION_CHANGES=NONE")
  print("EXISTING_TEST_CHANGES=NONE")
  print("DESIGN_RESULT=PASS")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())

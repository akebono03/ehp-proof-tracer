from dataclasses import fields
from pathlib import Path
import inspect

import proof
import toda_group_proof_narrative_semantics as semantics
import toda_proof_dependency as dependency


def field_signature(cls):
  return tuple(
    (field.name, str(field.type), repr(field.default))
    for field in fields(cls)
  )


def public_constructor_count(source_root):
  tests = source_root / "tests"
  counts = {
    "InferenceRule(": 0,
    "ProofStep(": 0,
    "TodaProofEdge(": 0,
    "TodaGroupProofNarrativePremiseSemantic(": 0,
  }
  if not tests.exists():
    return counts
  for path in tests.rglob("*.py"):
    text = path.read_text(encoding="utf-8", errors="ignore")
    for token in counts:
      counts[token] += text.count(token)
  return counts


def candidate_rows(test_counts):
  return (
    {
      "candidate": "ProofStep field",
      "owner": "proof core",
      "edge_specific": False,
      "narrative_specific": False,
      "survives_replay": True,
      "requires_producer_annotation": True,
      "existing_edge_validation": False,
      "api_surface": test_counts["ProofStep("],
      "risk": "HIGH",
      "reason": (
        "Contribution belongs to a premise->consumer edge, but ProofStep is a node. "
        "A tuple aligned with premises would duplicate edge semantics inside the core proof model."
      ),
    },
    {
      "candidate": "InferenceRule premise metadata",
      "owner": "proof rule core",
      "edge_specific": True,
      "narrative_specific": False,
      "survives_replay": True,
      "requires_producer_annotation": True,
      "existing_edge_validation": False,
      "api_surface": test_counts["InferenceRule("],
      "risk": "MEDIUM-HIGH",
      "reason": (
        "Premise index naturally identifies the edge, but rules are reusable proof semantics. "
        "Narrative-only relevance would leak presentation policy into inference rules and require "
        "annotation across a broad existing rule catalog."
      ),
    },
    {
      "candidate": "TodaProofEdge field",
      "owner": "derived provenance graph",
      "edge_specific": True,
      "narrative_specific": False,
      "survives_replay": False,
      "requires_producer_annotation": False,
      "existing_edge_validation": False,
      "api_surface": test_counts["TodaProofEdge("],
      "risk": "MEDIUM",
      "reason": (
        "The location is structurally correct, but TodaProofEdge is reconstructed from ProofStep premises. "
        "A semantic field would need to be inferred during provenance extraction and is not authoritative storage."
      ),
    },
    {
      "candidate": "Narrative premise semantic sidecar",
      "owner": "Narrative semantic layer",
      "edge_specific": True,
      "narrative_specific": True,
      "survives_replay": False,
      "requires_producer_annotation": False,
      "existing_edge_validation": True,
      "api_surface": test_counts["TodaGroupProofNarrativePremiseSemantic("],
      "risk": "LOW",
      "reason": (
        "The existing sidecar already stores semantic data keyed by TodaProofEdge, validates membership "
        "in presentation.edges, rejects duplicate edge semantics, and is consumed only by Narrative layers."
      ),
    },
  )


def main():
  root = Path.cwd()
  counts = public_constructor_count(root)

  print("=" * 118)
  print("Phase 144-6-R5-15L explicit evidence-contribution metadata design audit")
  print("=" * 118)
  print("Audit only. No production code, tests, or project documents are modified.")
  print()

  print("CURRENT CORE DATA MODEL")
  print("-" * 118)
  for cls in (
    proof.InferenceRule,
    proof.ProofStep,
    dependency.TodaProofEdge,
    semantics.TodaGroupProofNarrativePremiseSemantic,
    semantics.TodaGroupProofNarrativeSemanticSidecar,
  ):
    print(cls.__name__)
    for name, annotation, default in field_signature(cls):
      print(f"  {name}: {annotation} default={default}")
  print()

  print("CURRENT NARRATIVE SIDECAR GUARANTEES")
  print("-" * 118)
  sidecar_source = inspect.getsource(
    semantics.TodaGroupProofNarrativeSemanticSidecar.__post_init__
  )
  guarantees = (
    ("presentation-edge membership validation", "allowed_edge_keys" in sidecar_source),
    ("duplicate premise-edge rejection", "seen_premise_keys" in sidecar_source),
    ("step membership validation", "allowed_step_ids" in sidecar_source),
    ("dependency duplicate rejection", "seen_dependency_keys" in sidecar_source),
  )
  for label, present in guarantees:
    print(f"{label}: {'YES' if present else 'NO'}")
  print()

  print("TEST-SURFACE CONSTRUCTOR COUNTS")
  print("-" * 118)
  for token, count in counts.items():
    print(f"{token:<48} {count:5d}")
  print()

  print("CANDIDATE COMPARISON")
  print("-" * 118)
  rows = candidate_rows(counts)
  for row in rows:
    print(row["candidate"])
    print(f"  owner={row['owner']}")
    print(f"  edge_specific={'YES' if row['edge_specific'] else 'NO'}")
    print(f"  narrative_specific={'YES' if row['narrative_specific'] else 'NO'}")
    print(f"  survives_replay={'YES' if row['survives_replay'] else 'NO'}")
    print(f"  requires_producer_annotation={'YES' if row['requires_producer_annotation'] else 'NO'}")
    print(f"  existing_edge_validation={'YES' if row['existing_edge_validation'] else 'NO'}")
    print(f"  test_constructor_surface={row['api_surface']}")
    print(f"  compatibility_risk={row['risk']}")
    print(f"  reason={row['reason']}")
  print()

  print("DESIGN QUESTIONS")
  print("-" * 118)
  print("Q1. Is evidence contribution intrinsic mathematical proof semantics or Narrative selection semantics?")
  print("    15K observed it specifically to decide what a reader-facing Narrative should expose.")
  print("Q2. Is contribution node-specific or edge-specific?")
  print("    Edge-specific: the same premise statement can contribute differently to different consumers.")
  print("Q3. Must metadata exist before replay/presentation construction?")
  print("    Not for the current Phase 144 goal; Narrative is built after presentation edges exist.")
  print("Q4. Which existing abstraction already represents edge-specific Narrative semantics?")
  print("    TodaGroupProofNarrativePremiseSemantic inside TodaGroupProofNarrativeSemanticSidecar.")
  print("Q5. What is still missing?")
  print("    A typed evidence-contribution enum/value and generic builders that populate it without rule-name heuristics.")
  print()

  print("MINIMAL PROTOTYPE SHAPE FOR A FUTURE PHASE")
  print("-" * 118)
  print("This is design output only; it is NOT applied by this audit.")
  print()
  print("class TodaGroupProofNarrativeEvidenceContribution(Enum):")
  print('  ESTABLISH_GROUP = "establish_group"')
  print('  ESTABLISH_MAP = "establish_map"')
  print('  ESTABLISH_ISOMORPHISM = "establish_isomorphism"')
  print('  ESTABLISH_ZERO = "establish_zero"')
  print('  ESTABLISH_ORDER = "establish_order"')
  print('  ESTABLISH_DECOMPOSITION = "establish_decomposition"')
  print('  ESTABLISH_RELATION = "establish_relation"')
  print('  PROVIDE_REFERENCE = "provide_reference"')
  print('  PROVIDE_PRECONDITION = "provide_precondition"')
  print()
  print("TodaGroupProofNarrativePremiseSemantic(")
  print("  edge=<TodaProofEdge>,")
  print("  role=<existing premise role or generalized role>,")
  print("  contribution=<typed evidence contribution>,")
  print(")")
  print()

  print("RECOMMENDATION")
  print("-" * 118)
  print("Preferred storage: Narrative premise semantic sidecar.")
  print("Do not add Narrative relevance fields to ProofStep in the first prototype.")
  print("Do not add Narrative relevance fields to TodaProofEdge; it is a derived graph edge.")
  print("Do not put reader-facing visibility policy directly into InferenceRule.")
  print("If later phases prove that evidence contribution is needed by non-Narrative proof consumers,")
  print("promote only the mathematical contribution type to a proof-core premise annotation then.")
  print()

  print("BOUNDARY TO NEXT PHASE")
  print("-" * 118)
  print("15L stops at storage/design choice.")
  print("The next prototype should add typed contribution metadata only to the Narrative semantic layer,")
  print("populate a minimal subset for the six representative groups, and compare coverage against 15K.")
  print("It must not yet replace the production R4 visibility policy.")
  print()

  print("SUMMARY")
  print("-" * 118)
  print("recommended_owner=NARRATIVE_SEMANTIC_SIDECAR")
  print("recommended_granularity=PREMISE_EDGE")
  print("proof_step_change=NO")
  print("inference_rule_change=NO_FOR_FIRST_PROTOTYPE")
  print("toda_proof_edge_change=NO")
  print("production_visibility_change=NO")
  print("pytest_required=NO")


if __name__ == "__main__":
  main()

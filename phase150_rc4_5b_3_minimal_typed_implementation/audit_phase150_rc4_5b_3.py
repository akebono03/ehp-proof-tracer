from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)


def main():
  presentation, blocks, semantic_sidecar, arguments = _method_evidence_data(3, 3)
  reason_sidecar = build_toda_group_proof_narrative_reason_sidecar(
    presentation,
    semantic_sidecar,
  )
  markdown = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  application = semantic_sidecar.reference_application_semantics[0]
  binding = application.bindings[0]

  print("=" * 78)
  print("Phase 150 / RC4-5B-3 typed reference application audit")
  print("=" * 78)
  print("reference applications:", len(semantic_sidecar.reference_application_semantics))
  print("reference:", application.reference.label)
  print("formal variable:", repr(binding.formal_variable))
  print("instantiated expression:", repr(binding.instantiated_expression))
  print(
    "reason attached:",
    reason_sidecar.reasons[0].reference_application is application,
  )

  needle = "この前提条件を満たすので、Lemma 5.2 を適用できる."
  index = markdown.find(needle)
  if index < 0:
    raise AssertionError("reference-aware prose is not visible")

  print("-" * 78)
  print(markdown[max(0, index - 120):index + 360])
  print("-" * 78)
  print("VISIBLE_REFERENCE_PROSE=PASS")
  print("AUDIT_RESULT=PASS")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())

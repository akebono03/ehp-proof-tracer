from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)


def main():
  presentation, blocks, semantic_sidecar, arguments = _method_evidence_data(3, 3)
  markdown = render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )

  expected = (
    "この前提条件を満たすので、Lemma 5.2 を適用できる.\n"
    "Lemma 5.2 の $\\beta$ を $\\nu'$ と定めると、"
  )

  if markdown.count(expected) != 1:
    raise AssertionError(
      "expected reference-aware beta prose exactly once"
    )

  if "Lemma 5.2 の $β$" in markdown:
    raise AssertionError(
      "raw Unicode beta remains in math prose"
    )

  index = markdown.index(expected)

  print("=" * 78)
  print("Phase 150 / RC4-5B-3-R1 visible repair audit")
  print("=" * 78)
  print(markdown[max(0, index - 120):index + 360])
  print("-" * 78)
  print("REFERENCE_AWARE_PROSE=PASS")
  print("BETA_LATEX=PASS")
  print("AUDIT_RESULT=PASS")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())

from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)


def main():
  presentation, blocks, semantic_sidecar, arguments = _method_evidence_data(3, 3)
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  reason = (
    "この完全性と、左の写像が単射、"
    "右の写像が全射であることより、"
    "次の短完全列を得る."
  )
  old = "この完全性と両端の写像の性質より"
  print(rendered)
  print("=" * 78)
  print("VISIBLE_SHORT_EXACT_REASON=", reason in rendered)
  print("OLD_VAGUE_PROSE_ABSENT=", old not in rendered)
  print(
    "VISIBLE_RESULT=",
    "PASS" if reason in rendered and old not in rendered else "FAIL",
  )


if __name__ == "__main__":
  main()

from expression import HomotopyElement
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_human_readable_renderer import (
  render_toda_expression_latex,
)


def main():
  beta = HomotopyElement(
    name="β",
    dimension=3,
    source=6,
    target=3,
  )
  beta_latex = render_toda_expression_latex(beta)

  if beta_latex != r"\beta":
    raise AssertionError(
      f"unexpected beta LaTeX: {beta_latex!r}"
    )

  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(3, 3)

  markdown = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  expected = (
    "この前提条件を満たすので、"
    "Lemma 5.2 を適用できる.\n"
    "Lemma 5.2 の $\\beta$ を "
    "$\\nu'$ と定めると、"
  )

  if markdown.count(expected) != 1:
    raise AssertionError(
      "reference-aware beta prose is not visible exactly once"
    )

  print("=" * 78)
  print("Phase 150 / RC4-5B-3-R2 test expectation repair audit")
  print("=" * 78)
  print("rendered beta repr:", repr(beta_latex))
  print("expected beta repr:", repr(r"\\beta"))
  print("BETA_EXPECTATION=PASS")
  print("REFERENCE_AWARE_PROSE=PASS")
  print("AUDIT_RESULT=PASS")
  print("PRODUCTION_CHANGES=NONE")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())

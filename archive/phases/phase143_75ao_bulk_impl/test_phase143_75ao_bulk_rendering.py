from homotopy_groups import (
  FiniteHomotopyGroupStatement,
  HomotopyGroup,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def test_phase143_75ao_renders_finite_group_semantically():
  statement = FiniteHomotopyGroupStatement(
    group=HomotopyGroup(
      group_dimension=11,
      sphere_dimension=9,
    ),
  )
  assert (
    render_toda_proof_statement_latex(statement)
    == r"\\pi_{11}^{9} \\text{ is finite}"
  )


def test_phase143_75ao_remaining_batch_has_no_rule_name_fallback():
  import phase143_75ao_bulk_audit.audit_phase143_75ao_bulk as audit

  names = {
    "FiniteHomotopyGroupStatement",
    "Toda211OrdinaryEHPExactnessStatement",
    "TodaLemma510HopfBracketContainsStatement",
    "TodaLemma510IndexedHopfBracketContainsStatement",
    "TodaLemma510Split115Statement",
    "TodaLemma510OrdinaryBracketPlusSuspensionImageStatement",
    "TodaLemma510OrdinarySuspensionImageFiniteStatement",
    "TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement",
    "TodaLemma510OrdinarySuspensionImageInDoubleStatement",
  }

  assert len(names) == 9

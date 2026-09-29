from collections import Counter

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  Sum,
  Suspension,
  WhiteheadProduct,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  Toda58WhiteheadSquareUpToSignStatement,
)


def _target_statements():
  statements = []

  for n in range(2, 16):
    for k in range(0, 8):
      report = build_standard_toda_report(
        n=n,
        k=k,
      )
      group_result = (
        report.candidates[
          0
        ].source_candidate.group_result
      )
      replay = (
        build_toda_group_result_proof_replay(
          group_result,
          max_depth=7,
        )
      )
      presentation = (
        build_toda_group_proof_presentation(
          replay
        )
      )

      for node in presentation.nodes:
        statement = node.proof_step.conclusion

        if (
          type(statement).__name__
          == "Toda58EquationStatement"
        ):
          statements.append(
            statement.whitehead_nu_relation
          )

  return tuple(statements)


def test_phase143_75s_all_aggregate_components_render_semantically():
  statements = _target_statements()

  assert len(statements) == 45

  rendered = tuple(
    render_toda_proof_statement_latex(
      statement
    )
    for statement in statements
  )

  assert all(
    value is not None
    for value in rendered
  )

  assert Counter(
    type(statement).__name__
    for statement in statements
  ) == Counter(
    {
      "Toda58WhiteheadSquareUpToSignStatement":
        45,
    }
  )


def test_phase143_75s_sum_positive_value_is_parenthesized_after_pm():
  iota_4 = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )
  nu_4 = HomotopyElement(
    name="ν₄",
    dimension=4,
    source=7,
    target=4,
    generator=GeneratorSymbol(
      family="ν",
      index=4,
    ),
  )
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  statement = (
    Toda58WhiteheadSquareUpToSignStatement(
      whitehead_square=WhiteheadProduct(
        left=iota_4,
        right=iota_4,
      ),
      positive_value=Sum(
        left=Multiple(
          coefficient=2,
          expression=nu_4,
        ),
        right=Multiple(
          coefficient=-1,
          expression=Suspension(
            expression=nu_prime
          ),
        ),
      ),
    )
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"[\iota_{4}, \iota_{4}]"
      r" = \pm "
      r"\left(2\nu_{4} - E\nu'\right)"
    )
  )


def test_phase143_75s_non_sum_positive_value_has_no_forced_parentheses():
  iota_4 = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )
  nu_4 = HomotopyElement(
    name="ν₄",
    dimension=4,
    source=7,
    target=4,
    generator=GeneratorSymbol(
      family="ν",
      index=4,
    ),
  )

  statement = (
    Toda58WhiteheadSquareUpToSignStatement(
      whitehead_square=WhiteheadProduct(
        left=iota_4,
        right=iota_4,
      ),
      positive_value=nu_4,
    )
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"[\iota_{4}, \iota_{4}]"
      r" = \pm \nu_{4}"
    )
  )

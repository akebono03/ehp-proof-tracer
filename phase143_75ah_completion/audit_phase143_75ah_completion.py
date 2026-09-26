import runpy

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
)
from homotopy_groups import (
  TodaPrimaryGroup,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  TodaLemma57TwoIota5ImageMembershipStatement,
)


def main():
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
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=IteratedSuspension(
        expression=nu_prime,
        exponent=2,
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      ),
    )
  )

  print("=" * 78)
  print("Phase 143-75AH focused semantic rendering")
  print("=" * 78)
  print(
    render_toda_proof_statement_latex(
      statement
    )
  )
  print("")
  print("=" * 78)
  print("Phase 143-75AH completion inventory")
  print("=" * 78)

  runpy.run_path(
    "phase143_75u/"
    "audit_phase143_75u_remaining_fallbacks.py",
    run_name="__main__",
  )


if __name__ == "__main__":
  main()

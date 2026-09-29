import runpy

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Multiple,
  TodaBracket,
)
from homotopy_groups import (
  HomotopyGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  TodaLemma510BracketModuloStatement,
)


def main():
  statement = TodaLemma510BracketModuloStatement(
    element=MapApplication(
      map=EHP_DELTA_MAP,
      expression=HomotopyElement(
        name="ι_13",
        dimension=13,
        generator=GeneratorSymbol(
          family="ι",
          index=13,
        ),
      ),
    ),
    bracket=TodaBracket(
      first=HomotopyElement(
        name="ν_6",
        dimension=6,
        source=9,
        target=6,
        generator=GeneratorSymbol(
          family="ν",
          index=6,
        ),
      ),
      second=HomotopyElement(
        name="η_9",
        dimension=9,
        source=10,
        target=9,
        generator=GeneratorSymbol(
          family="η",
          index=9,
        ),
      ),
      third=Multiple(
        coefficient=2,
        expression=HomotopyElement(
          name="ι_10",
          dimension=10,
          generator=GeneratorSymbol(
            family="ι",
            index=10,
          ),
        ),
      ),
    ),
    ambient_group=HomotopyGroup(
      group_dimension=11,
      sphere_dimension=6,
    ),
    modulus=2,
  )

  print("=" * 78)
  print("Phase 143-75AG focused semantic rendering")
  print("=" * 78)
  print(
    render_toda_proof_statement_latex(
      statement
    )
  )
  print("")
  print("=" * 78)
  print("Phase 143-75AG completion inventory")
  print("=" * 78)

  runpy.run_path(
    "phase143_75u/"
    "audit_phase143_75u_remaining_fallbacks.py",
    run_name="__main__",
  )


if __name__ == "__main__":
  main()

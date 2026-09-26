import runpy

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  TodaProp59DeltaKernelStatement,
)


def main():
  nu_5 = HomotopyElement(
    name="ν_5",
    dimension=5,
    source=8,
    target=5,
    generator=GeneratorSymbol(
      family="ν",
      index=5,
    ),
  )

  statement = TodaProp59DeltaKernelStatement(
    map=TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=2,
      ),
    ),
    kernel_group=FiniteCyclicGroup(
      order=2,
      generator=Multiple(
        coefficient=4,
        expression=nu_5,
      ),
    ),
  )

  print("=" * 78)
  print("Phase 143-75AI focused semantic rendering")
  print("=" * 78)
  print(render_toda_proof_statement_latex(statement))
  print("")
  print("=" * 78)
  print("Phase 143-75AI completion inventory")
  print("=" * 78)

  runpy.run_path(
    "phase143_75u/"
    "audit_phase143_75u_remaining_fallbacks.py",
    run_name="__main__",
  )


if __name__ == "__main__":
  main()

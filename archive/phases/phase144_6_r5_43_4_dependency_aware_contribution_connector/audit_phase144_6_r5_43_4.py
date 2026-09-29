from test_phase144_6_r5_43_4_dependency_aware_contribution_connector import (
  _pi6_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  _contribution_connector_lines,
)


def main():
  (
    presentation,
    base,
    connected,
    ordered,
    contributions,
  ) = _pi6_data()
  connectors = _contribution_connector_lines(
    presentation,
    ordered,
  )

  print("=" * 78)
  print("Phase 144-6-R5-43-4 dependency-aware contribution connector audit")
  print("=" * 78)
  print(
    f"contributions={len(contributions)} "
    f"connectors={len(connectors)}"
  )
  print()

  for index, contribution in enumerate(
    contributions,
    start=1,
  ):
    line = _render_generic_narrative_step(
      contribution.proof_step
    )
    connector = connectors.get(
      id(
        contribution.proof_step
      )
    )
    print(
      f"C{index}: connector_before="
      f"{connector!r}"
    )
    print(
      f"  {line}"
    )
  print()
  print("Connected Narrative")
  print("-" * 78)
  print(
    connected
  )


if __name__ == "__main__":
  main()

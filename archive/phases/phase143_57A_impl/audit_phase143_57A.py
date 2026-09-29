from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_step_transitions import (
  extract_toda_group_proof_narrative_step_transitions,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def main() -> None:
  for n, k in (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ):
    (
      presentation,
      blocks,
      _sidecar,
      _arguments,
    ) = _method_evidence_data(
      n,
      k,
    )
    transitions = (
      extract_toda_group_proof_narrative_step_transitions(
        presentation,
        blocks,
      )
    )

    print(
      "=" * 78
    )
    print(
      f"n={n}, k={k}, "
      f"step_transitions={len(transitions)}"
    )

    for index, transition in enumerate(
      transitions,
      start=1,
    ):
      print(
        f"{index}. "
        f"{transition.role.value}"
      )
      print(
        "   source: "
        + _render_generic_narrative_step(
          transition.source_step
        )
      )
      print(
        "   target: "
        + _render_generic_narrative_step(
          transition.target_step
        )
      )


if __name__ == "__main__":
  main()

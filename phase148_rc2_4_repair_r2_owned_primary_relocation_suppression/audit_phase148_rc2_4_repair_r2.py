from toda_rules import (
  TodaProp42ExactnessStatement,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _normalized(
  step,
):
  rendered = (
    _render_generic_narrative_step(
      step
    )
  )
  suffix = r" \text{ is exact}$"

  if rendered.endswith(
    suffix
  ):
    return (
      rendered[
        :-len(
          suffix
        )
      ]
      + "$ は完全である."
    )

  return rendered


def main():
  presentation, blocks, sidecar, arguments = (
    _method_evidence_data(
      3,
      3,
    )
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  exactness_steps = tuple(
    step
    for block in blocks
    for step in block.steps
    if isinstance(
      step.conclusion,
      TodaProp42ExactnessStatement,
    )
  )
  visible = tuple(
    _normalized(
      step
    )
    for step in exactness_steps
    if _normalized(
      step
    ) in rendered
  )

  print("=" * 78)
  print("Phase 148 RC2-4 Repair R2 post-repair pi_6^3 audit")
  print("=" * 78)
  print(
    f"raw exactness statements={len(exactness_steps)}"
  )
  print(
    f"visible raw exactness statements={len(visible)}"
  )
  for item in visible:
    print(
      "VISIBLE: "
      + item
    )
  short_exact = (
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
  )
  print(
    "owned short exact sequence visible="
    + str(
      short_exact in rendered
    )
  )
  print("=" * 78)
  print("FINAL NARRATIVE")
  print("=" * 78)
  print(
    rendered
  )


if __name__ == "__main__":
  main()

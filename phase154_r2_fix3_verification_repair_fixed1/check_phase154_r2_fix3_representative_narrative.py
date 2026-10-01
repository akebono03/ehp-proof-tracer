from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def main() -> int:
  report = build_standard_toda_report(
    n=4,
    k=7,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  print(rendered)

  assert "まず、[R2]を用いる。" in rendered
  assert "まず、[R2]\n" not in rendered
  assert "Toda Proposition 5.15を用いる。" not in rendered
  assert r"\text{ is injective}" not in rendered
  assert r"\text{ is exact}" not in rendered
  assert "である.を用いる。" not in rendered
  assert (
    r"$\nu_{4}$ の分解写像は同型写像である."
    in rendered
  )
  assert r"\pi_{11}^{4} = 0" in rendered

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

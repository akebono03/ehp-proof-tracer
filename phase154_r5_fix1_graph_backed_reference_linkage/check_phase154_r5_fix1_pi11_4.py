from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


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


def render_group(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
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

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def main() -> int:
  rendered = render_group(
    4,
    7,
  )

  print(
    rendered
  )

  assert (
    r"[R2]より、$\nu_{4}$ の分解写像は同型写像である."
    in rendered
  )
  assert "まず、[R2]を用いる。" not in rendered
  assert (
    rendered.count(
      r"$\nu_{4}$ の分解写像は同型写像である."
    )
    == 1
  )
  assert "[R1]を用いる。" in rendered
  assert r"\pi_{11}^{4} = 0" in rendered

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

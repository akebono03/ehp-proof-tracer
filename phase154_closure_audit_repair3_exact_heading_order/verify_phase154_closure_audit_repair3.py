import sys
from pathlib import Path


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


def _render_group(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def main() -> int:
  for label, n, k in (
    ("pi_8^5", 5, 3),
    ("pi_15^8", 8, 7),
  ):
    rendered = _render_group(
      n,
      k,
    )
    lines = tuple(
      line.strip()
      for line in rendered.splitlines()
    )

    target_index = lines.index(
      "## 証明対象"
    )
    reference_index = lines.index(
      "## 使用する結果"
    )
    proof_index = lines.index(
      "## 証明"
    )

    print(
      label
      + ": proof_target_index="
      + str(
        target_index
      )
      + ", reference_index="
      + str(
        reference_index
      )
      + ", proof_index="
      + str(
        proof_index
      )
    )

    if not (
      target_index
      < reference_index
      < proof_index
    ):
      return 1

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

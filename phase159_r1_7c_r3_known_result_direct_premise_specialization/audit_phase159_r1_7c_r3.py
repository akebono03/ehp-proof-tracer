from pathlib import Path
import sys


REPOSITORY_ROOT = (
  Path(__file__).resolve().parents[1]
)

if str(
  REPOSITORY_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
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


def main() -> None:
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
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  output = (
    Path(__file__).resolve().parent
    / "audit_output"
    / "pi_11^4_after_r3.md"
  )
  output.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  output.write_text(
    rendered,
    encoding="utf-8",
  )
  print(rendered)
  print()
  print(
    "Audit output:",
    output,
  )


if __name__ == "__main__":
  main()

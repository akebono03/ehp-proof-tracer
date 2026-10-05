from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


def main() -> None:
  report = build_standard_toda_report(
    n=2,
    k=1,
  )
  group_result = (
    report.candidates[0]
    .source_candidate
    .group_result
  )
  presentation = (
    build_toda_group_proof_presentation(
      build_toda_group_result_proof_replay(
        group_result,
        max_depth=2,
      )
    )
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  proof_body = rendered.split(
    "## 証明\n\n",
    1,
  )[1]

  exactness_lines = tuple(
    line
    for line in proof_body.splitlines()
    if r"\xrightarrow{" in line
  )

  print(
    "exactness_line_count=",
    len(
      exactness_lines
    ),
    sep="",
  )

  for index, line in enumerate(
    exactness_lines
  ):
    print()
    print(
      "exactness_line_",
      index,
      "=",
      repr(
        line
      ),
      sep="",
    )

  print()
  print("----- FULL PROOF BODY -----")
  print(proof_body)


if __name__ == "__main__":
  main()

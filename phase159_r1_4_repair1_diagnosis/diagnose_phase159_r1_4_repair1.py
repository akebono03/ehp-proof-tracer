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
  _phase159_consolidate_public_exactness_lines,
  _phase159_public_exactness_latex,
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
  lines = proof_body.splitlines()

  exactness = tuple(
    (
      index,
      line,
      _phase159_public_exactness_latex(
        line
      ),
    )
    for index, line in enumerate(
      lines
    )
    if r"\xrightarrow{" in line
  )

  print(
    "exactness_count=",
    len(
      exactness
    ),
    sep="",
  )

  for index, line, normalized in exactness:
    print()
    print(
      "index=",
      index,
      sep="",
    )
    print(
      "raw=",
      repr(
        line
      ),
      sep="",
    )
    print(
      "normalized=",
      repr(
        normalized
      ),
      sep="",
    )

  print()
  print("----- SUBSTRING MATRIX -----")

  for (
    left_index,
    _left_line,
    left_normalized,
  ) in exactness:
    for (
      right_index,
      _right_line,
      right_normalized,
    ) in exactness:
      if left_index == right_index:
        continue

      print(
        left_index,
        "in",
        right_index,
        "=",
        (
          left_normalized in right_normalized
          if (
            left_normalized is not None
            and right_normalized is not None
          )
          else None
        ),
      )

  collapsed = (
    _phase159_consolidate_public_exactness_lines(
      lines
    )
  )

  collapsed_exactness = tuple(
    line
    for line in collapsed
    if r"\xrightarrow{" in line
  )

  print()
  print(
    "collapsed_exactness_count=",
    len(
      collapsed_exactness
    ),
    sep="",
  )

  for index, line in enumerate(
    collapsed_exactness
  ):
    print(
      "collapsed_",
      index,
      "=",
      repr(
        line
      ),
      sep="",
    )

  print()
  print("----- FINAL PUBLIC EXACTNESS -----")

  final_exactness = tuple(
    line
    for line in lines
    if r"\xrightarrow{" in line
  )

  for index, line in enumerate(
    final_exactness
  ):
    print(
      "final_",
      index,
      "=",
      repr(
        line
      ),
      sep="",
    )


if __name__ == "__main__":
  main()

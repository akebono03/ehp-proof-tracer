import re
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


REPRESENTATIVES = (
  ("pi6_3", 3, 3),
  ("pi10_4", 4, 6),
  ("pi11_4", 4, 7),
  ("pi12_5", 5, 7),
  ("pi16_9", 9, 7),
)


def _render_group(
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
  total_period = 0
  total_comma = 0

  for name, n, k in REPRESENTATIVES:
    rendered = _render_group(
      n,
      k,
    )
    ascii_period = 0
    ascii_comma = 0

    for line in rendered.splitlines():
      stripped = line.strip()

      if not stripped:
        continue

      if stripped.startswith(
        "**[R"
      ):
        continue

      prose = re.sub(
        r"\$[^$]*\$",
        "MATH",
        stripped,
      )

      if not re.search(
        r"[ぁ-んァ-ヶ一-龠々]",
        prose,
      ):
        continue

      if prose.endswith(
        "."
      ):
        ascii_period += 1

      if re.search(
        r",(?:\s|$)",
        prose,
      ):
        ascii_comma += 1

    total_period += ascii_period
    total_comma += ascii_comma

    print(
      name
      + ": ascii_period_sentence_endings="
      + str(
        ascii_period
      )
      + ", ascii_comma_prose_lines="
      + str(
        ascii_comma
      )
    )

  print(
    "TOTAL ascii_period_sentence_endings:",
    total_period,
  )
  print(
    "TOTAL ascii_comma_prose_lines:",
    total_comma,
  )

  if total_period != 0:
    return 1

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

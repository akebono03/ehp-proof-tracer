from collections import Counter
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


GROUPS = (
  (3, 3, "pi6_3"),
  (4, 6, "pi10_4"),
  (4, 7, "pi11_4"),
  (5, 7, "pi12_5"),
  (9, 7, "pi16_9"),
)

FINAL_RESULT_SENTENCE = (
  "以上で得た群構造、生成元、および写像に関する結果を合わせると、"
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
  output_dir = (
    Path(__file__).resolve().parent
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  summary = [
    "# Phase 154-R4 Focused Re-audit",
    "",
    "Production target: repeated FINAL_RESULT_DERIVATION prose.",
    "",
  ]

  for n, k, key in GROUPS:
    rendered = render_group(
      n,
      k,
    )
    lines = tuple(
      line.strip()
      for line in rendered.splitlines()
      if line.strip()
    )
    counts = Counter(
      lines
    )
    duplicates = tuple(
      line
      for line, count in counts.items()
      if count > 1
    )

    summary.extend(
      (
        f"## {key}",
        "",
        (
          "final_result_sentence_count: "
          + str(
            rendered.count(
              FINAL_RESULT_SENTENCE
            )
          )
        ),
        (
          "exact_duplicate_line_count: "
          + str(
            len(
              duplicates
            )
          )
        ),
        "",
      )
    )

    (
      output_dir
      / f"{key}.txt"
    ).write_text(
      rendered,
      encoding="utf-8",
    )

  (
    output_dir
    / "phase154_r4_summary.md"
  ).write_text(
    "\n".join(
      summary
    ),
    encoding="utf-8",
  )

  print(
    "\n".join(
      summary
    )
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

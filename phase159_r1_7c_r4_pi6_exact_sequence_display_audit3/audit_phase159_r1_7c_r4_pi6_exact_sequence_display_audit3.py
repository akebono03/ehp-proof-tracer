from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
ROOT_TEXT = str(
  ROOT
)

if ROOT_TEXT not in sys.path:
  sys.path.insert(
    0,
    ROOT_TEXT,
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


def _pi6_3_public_narrative() -> str:
  report = build_standard_toda_report(
    n=3,
    k=3,
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


def _display_math_blocks(
  markdown: str,
) -> tuple[
  str,
  ...,
]:
  blocks = []
  position = 0

  while True:
    start = markdown.find(
      r"\[",
      position,
    )

    if start < 0:
      break

    end = markdown.find(
      r"\]",
      start + 2,
    )

    if end < 0:
      break

    blocks.append(
      markdown[
        start:
        end + 2
      ]
    )
    position = (
      end + 2
    )

  return tuple(
    blocks
  )


def main() -> None:
  rendered = _pi6_3_public_narrative()

  print(
    "=" * 78
  )
  print(
    "pi_6^3 public Narrative display-math audit"
  )
  print(
    "=" * 78
  )

  blocks = _display_math_blocks(
    rendered
  )

  for index, block in enumerate(
    blocks,
    start=1,
  ):
    if (
      r"\xrightarrow{"
      not in block
      and r"\longrightarrow"
      not in block
    ):
      continue

    print()
    print(
      f"[DISPLAY BLOCK {index}]"
    )
    print(
      block
    )
    print()
    print(
      "[NORMALIZED]"
    )
    print(
      " ".join(
        block.split()
      )
    )

  print()
  print(
    "[INLINE / PARAGRAPH LINES WITH ARROWS]"
  )

  for index, paragraph in enumerate(
    rendered.split(
      "\n\n"
    ),
    start=1,
  ):
    if (
      r"\xrightarrow{"
      in paragraph
      or r"\longrightarrow"
      in paragraph
    ):
      print(
        f"{index:03d}: {paragraph.strip()}"
      )


if __name__ == "__main__":
  main()

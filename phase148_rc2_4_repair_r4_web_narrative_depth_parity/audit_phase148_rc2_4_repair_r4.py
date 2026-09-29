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
from web_group_proof import (
  build_standard_web_group_proof_view,
)


def _web_text(
  view,
):
  parts = []
  for line in view.rendered_lines:
    for segment in line.segments:
      if segment.kind in (
        "inline_math",
        "display_math",
      ):
        parts.append(
          "$" + segment.value + "$"
        )
      else:
        parts.append(
          segment.value
        )
    parts.append(
      "\n"
    )
  return "".join(
    parts
  )


def main():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  markdown = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )
  web_text = _web_text(
    view
  )

  print("=" * 78)
  print(
    "Phase 148 RC2-4 Repair R4 "
    "post-repair verification"
  )
  print("=" * 78)
  print(
    "selected depth="
    + str(
      view.max_depth
    )
  )
  print(
    "visible replay steps="
    + str(
      len(
        view.steps
      )
    )
  )
  print(
    "presentation replay nodes="
    + str(
      len(
        presentation.nodes
      )
    )
  )
  print(
    "public depth2 exactness phrases="
    + str(
      markdown.count(
        "は完全である"
      )
      + markdown.count(
        r"\text{ is exact}"
      )
    )
  )
  print(
    "Web exactness phrases="
    + str(
      web_text.count(
        "は完全である"
      )
      + web_text.count(
        r"\text{ is exact}"
      )
    )
  )
  print(
    "short exact sequence visible="
    + str(
      (
        r"0\longrightarrow \pi_{5}^{2}"
        in web_text
      )
      and (
        r"\xrightarrow{E} \pi_{6}^{3}"
        in web_text
      )
      and (
        r"\xrightarrow{H} \pi_{6}^{5}"
        in web_text
      )
      and (
        r"\longrightarrow 0"
        in web_text
      )
    )
  )
  print(
    "group conclusion visible="
    + str(
      r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
      in web_text
    )
  )
  print("=" * 78)
  print("WEB NARRATIVE")
  print("=" * 78)
  print(
    web_text
  )


if __name__ == "__main__":
  main()

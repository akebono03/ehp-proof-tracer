from proof import (
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
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


def _group_result():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  return (
    report.candidates[
      0
    ].source_candidate.group_result
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
  replay = (
    build_toda_group_result_proof_replay(
      _group_result(),
      max_depth=2,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  original_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }
  added = tuple(
    node
    for node in closure.nodes
    if id(
      node.proof_step
    ) not in original_ids
  )
  added_equalities = tuple(
    node
    for node in added
    if (
      isinstance(
        node.proof_step.conclusion,
        Relation,
      )
      and node.proof_step.conclusion.relation_type
      is RelationType.EQUALITY
    )
  )
  rendered = (
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
  web_text = (
    _web_text(
      view
    )
  )

  print("=" * 84)
  print(
    "Phase 148 RC2-4 Repair R4.2 "
    "post-repair audit"
  )
  print("=" * 84)
  print(
    "input replay nodes="
    + str(
      len(
        presentation.nodes
      )
    )
  )
  print(
    "closure nodes="
    + str(
      len(
        closure.nodes
      )
    )
  )
  print(
    "closure max_depth="
    + str(
      closure.max_depth
    )
  )
  print(
    "closure-added steps="
    + str(
      len(
        added
      )
    )
  )
  print(
    "closure-added equality steps="
    + str(
      len(
        added_equalities
      )
    )
  )
  for node in added:
    print(
      "  added depth="
      + str(
        node.depth
      )
      + " role="
      + node.role.value
      + " "
      + _render_generic_narrative_step(
        node.proof_step
      )
    )
  print(
    "public tag1/tag2/tag3="
    + str(
      (
        r"\tag{1}" in rendered,
        r"\tag{2}" in rendered,
        r"\tag{3}" in rendered,
      )
    )
  )
  print(
    "public connector12="
    + str(
      "(1) と (2) より、"
      in rendered
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
    "Web group conclusion="
    + str(
      r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
      in web_text
    )
  )
  print(
    "Web short exact sequence="
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
  print("=" * 84)
  print("WEB NARRATIVE")
  print("=" * 84)
  print(
    web_text
  )


if __name__ == "__main__":
  main()

from collections import Counter

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
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


def _structure(
  replay,
  apply_closure,
):
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  input_nodes = len(
    presentation.nodes
  )
  input_max_depth = (
    presentation.max_depth
  )

  if apply_closure:
    presentation = (
      build_toda_group_proof_narrative_semantic_closure_presentation(
        presentation
      )
    )

  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=sidecar,
    )
  )
  exactness_steps = tuple(
    proof_step
    for block in blocks
    for proof_step in block.steps
    if isinstance(
      proof_step.conclusion,
      TodaProp42ExactnessStatement,
    )
  )
  roles = Counter(
    block.role.value
    for block in blocks
  )
  return {
    "presentation": presentation,
    "sidecar": sidecar,
    "blocks": blocks,
    "arguments": arguments,
    "exactness_steps": exactness_steps,
    "input_nodes": input_nodes,
    "input_max_depth": input_max_depth,
    "roles": roles,
  }


def _exactness_phrase_count(
  markdown,
):
  return (
    markdown.count(
      "は完全である"
    )
    + markdown.count(
      r"\text{ is exact}"
    )
  )


def _print_structure(
  label,
  data,
):
  print(
    f"[{label}]"
  )
  print(
    "input replay nodes="
    + str(
      data[
        "input_nodes"
      ]
    )
  )
  print(
    "input replay max_depth="
    + str(
      data[
        "input_max_depth"
      ]
    )
  )
  print(
    "post-closure nodes="
    + str(
      len(
        data[
          "presentation"
        ].nodes
      )
    )
  )
  print(
    "post-closure max_depth="
    + str(
      data[
        "presentation"
      ].max_depth
    )
  )
  print(
    "blocks="
    + str(
      len(
        data[
          "blocks"
        ]
      )
    )
  )
  print(
    "arguments="
    + str(
      len(
        data[
          "arguments"
        ]
      )
    )
  )
  print(
    "TodaProp42ExactnessStatement count="
    + str(
      len(
        data[
          "exactness_steps"
        ]
      )
    )
  )
  print(
    "block roles="
    + repr(
      dict(
        sorted(
          data[
            "roles"
          ].items()
        )
      )
    )
  )


def _web_lines_text(
  view,
):
  parts = []
  for line in view.rendered_lines:
    if line.segments:
      segment_parts = []
      for segment in line.segments:
        if segment.kind in (
          "inline_math",
          "display_math",
        ):
          segment_parts.append(
            "$"
            + segment.value
            + "$"
          )
        elif segment.kind == "strong":
          segment_parts.append(
            "**"
            + segment.value
            + "**"
          )
        else:
          segment_parts.append(
            segment.value
          )
      parts.append(
        "".join(
          segment_parts
        )
      )
      continue

    parts.append(
      line.prefix
      + (
        ""
        if line.statement_latex is None
        else "$"
        + line.statement_latex
        + "$"
      )
      + line.suffix
    )
  return "\n".join(
    parts
  )


def main():
  group_result = (
    _group_result()
  )
  depth2_replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )
  depth3_replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=3,
    )
  )
  complete_replay = (
    build_complete_toda_group_result_proof_replay(
      group_result
    )
  )

  depth2 = _structure(
    depth2_replay,
    True,
  )
  unit = _structure(
    depth3_replay,
    False,
  )
  complete = _structure(
    complete_replay,
    True,
  )

  unit_markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      unit[
        "presentation"
      ],
      unit[
        "blocks"
      ],
      unit[
        "sidecar"
      ],
      unit[
        "arguments"
      ],
    )
  )

  depth2_base_markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      depth2[
        "presentation"
      ],
      depth2[
        "blocks"
      ],
      depth2[
        "sidecar"
      ],
      depth2[
        "arguments"
      ],
    )
  )
  depth2_contribution_markdown = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      depth2[
        "presentation"
      ],
      depth2[
        "blocks"
      ],
      depth2[
        "sidecar"
      ],
      depth2[
        "arguments"
      ],
    )
  )
  depth2_public_markdown = (
    render_toda_group_proof_narrative_markdown(
      build_toda_group_proof_presentation(
        depth2_replay
      )
    )
  )

  complete_base_markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      complete[
        "presentation"
      ],
      complete[
        "blocks"
      ],
      complete[
        "sidecar"
      ],
      complete[
        "arguments"
      ],
    )
  )
  complete_contribution_markdown = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      complete[
        "presentation"
      ],
      complete[
        "blocks"
      ],
      complete[
        "sidecar"
      ],
      complete[
        "arguments"
      ],
    )
  )
  complete_public_markdown = (
    render_toda_group_proof_narrative_markdown(
      build_toda_group_proof_presentation(
        complete_replay
      )
    )
  )

  web_view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )
  web_text = (
    _web_lines_text(
      web_view
    )
  )

  print("=" * 88)
  print("Phase 148 RC2-4 Repair R3 — Web / unit rendering-path parity audit")
  print("Production changes: none")
  print("=" * 88)
  print()
  print("A. REPLAY / STRUCTURE")
  print("-" * 88)
  _print_structure(
    "UNIT HELPER MODEL: depth=3, no semantic closure",
    unit,
  )
  print()
  _print_structure(
    "DEPTH=2 + semantic closure",
    depth2,
  )
  print()
  _print_structure(
    "COMPLETE REPLAY + semantic closure",
    complete,
  )

  print()
  print("B. RENDERER PATH")
  print("-" * 88)
  print(
    "RC2 unit tests: "
    "render_toda_group_proof_narrative_multi_argument_markdown"
  )
  print(
    "public pi_6^3 renderer: "
    "render_toda_group_proof_narrative_markdown"
  )
  print(
    "public pi_6^3 internal branch: "
    "semantic closure -> blocks -> arguments -> "
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown"
  )
  print(
    "Web narrative replay source: "
    "build_complete_toda_group_result_proof_replay"
  )
  print(
    "Web selected max_depth metadata="
    + str(
      web_view.max_depth
    )
  )
  print(
    "Web visible trace-step count="
    + str(
      len(
        web_view.steps
      )
    )
  )
  print(
    "Complete replay max_depth="
    + str(
      complete_replay.max_depth
    )
  )
  print(
    "Complete replay node count="
    + str(
      len(
        complete_replay.steps
      )
    )
  )

  print()
  print("C. FINAL NARRATIVE EXACTNESS COUNTS")
  print("-" * 88)
  rows = (
    (
      "unit depth3 direct multi_argument",
      unit_markdown,
    ),
    (
      "depth2 closure base multi_argument",
      depth2_base_markdown,
    ),
    (
      "depth2 closure + contributions",
      depth2_contribution_markdown,
    ),
    (
      "depth2 public renderer",
      depth2_public_markdown,
    ),
    (
      "complete closure base multi_argument",
      complete_base_markdown,
    ),
    (
      "complete closure + contributions",
      complete_contribution_markdown,
    ),
    (
      "complete public renderer",
      complete_public_markdown,
    ),
    (
      "actual Web adapter rendered lines",
      web_text,
    ),
  )

  for label, markdown in rows:
    print(
      label
      + ": chars="
      + str(
        len(
          markdown
        )
      )
      + " exactness_phrases="
      + str(
        _exactness_phrase_count(
          markdown
        )
      )
    )

  print()
  print("D. PARITY CHECKS")
  print("-" * 88)
  print(
    "depth2 base == depth2 contributions: "
    + str(
      depth2_base_markdown
      == depth2_contribution_markdown
    )
  )
  print(
    "complete base == complete contributions: "
    + str(
      complete_base_markdown
      == complete_contribution_markdown
    )
  )
  print(
    "complete contributions == complete public: "
    + str(
      complete_contribution_markdown
      == complete_public_markdown
    )
  )
  print(
    "Web text contains same exactness phrase count as complete public: "
    + str(
      _exactness_phrase_count(
        web_text
      )
      == _exactness_phrase_count(
        complete_public_markdown
      )
    )
  )
  print(
    "unit exactness count == Web exactness count: "
    + str(
      _exactness_phrase_count(
        unit_markdown
      )
      == _exactness_phrase_count(
        web_text
      )
    )
  )

  print()
  print("E. CONTRIBUTION-LAYER ADDED TEXT")
  print("-" * 88)
  contribution_added_lines = tuple(
    line
    for line in complete_contribution_markdown.splitlines()
    if (
      line
      and line
      not in complete_base_markdown.splitlines()
    )
  )
  print(
    "unique added nonblank line occurrences="
    + str(
      len(
        contribution_added_lines
      )
    )
  )
  for line in contribution_added_lines:
    print(
      "ADDED: "
      + line
    )

  print()
  print("F. COMPLETE PUBLIC NARRATIVE")
  print("-" * 88)
  print(
    complete_public_markdown
  )


if __name__ == "__main__":
  main()

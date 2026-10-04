from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

import toda_group_proof_narrative_argument_body_renderer as body_renderer

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


TARGET = r"\eta_{3}^{3} = \eta_{3}^{3}"

original_helper = (
  body_renderer
  ._is_toda_group_proof_narrative_rendered_reflexive_equality_step
)
original_relocatable = (
  body_renderer
  ._relocatable_toda_group_proof_narrative_direct_derivation_premises
)
original_insert = (
  body_renderer
  ._insert_toda_group_proof_narrative_relocated_direct_premises
)


def traced_helper(
  proof_step,
):
  result = original_helper(
    proof_step
  )
  rendered = (
    body_renderer
    ._render_generic_narrative_step(
      proof_step
    )
  )

  if (
    result
    or TARGET in rendered
  ):
    print(
      "HELPER",
      "result=",
      result,
      "rendered=",
      rendered,
      "rule=",
      (
        None
        if proof_step.inference_rule is None
        else proof_step.inference_rule.name
      ),
    )

  return result


def traced_relocatable(
  direct_derivation_premises,
  sources_by_target_id,
  conclusion_block,
):
  result = original_relocatable(
    direct_derivation_premises,
    sources_by_target_id,
    conclusion_block,
  )

  matching = tuple(
    step
    for step in result
    if TARGET in (
      body_renderer
      ._render_generic_narrative_step(
        step
      )
    )
  )

  if matching:
    print("")
    print("=" * 88)
    print("RELOCATABLE RESULT CONTAINS TARGET")
    print("=" * 88)

    for step in matching:
      print(
        "rendered=",
        body_renderer
        ._render_generic_narrative_step(
          step
        ),
      )
      print(
        "helper=",
        original_helper(
          step
        ),
      )
      print(
        "rule=",
        (
          None
          if step.inference_rule is None
          else step.inference_rule.name
        ),
      )

  return result


def traced_insert(
  block_lines,
  block,
  conclusion_step,
  direct_derivation_premises,
  relocated_direct_premises,
):
  target_relocated = tuple(
    step
    for step in relocated_direct_premises
    if TARGET in (
      body_renderer
      ._render_generic_narrative_step(
        step
      )
    )
  )

  if target_relocated:
    print("")
    print("=" * 88)
    print("RELOCATED INSERT INPUT CONTAINS TARGET")
    print("=" * 88)

    for step in target_relocated:
      print(
        "rendered=",
        body_renderer
        ._render_generic_narrative_step(
          step
        ),
      )
      print(
        "helper=",
        original_helper(
          step
        ),
      )

  result = original_insert(
    block_lines,
    block,
    conclusion_step,
    direct_derivation_premises,
    relocated_direct_premises,
  )

  if any(
    TARGET in line
    for line in result
  ):
    print("")
    print("=" * 88)
    print("RELOCATED INSERT OUTPUT CONTAINS TARGET")
    print("=" * 88)
    for index, line in enumerate(
      result
    ):
      if TARGET in line:
        print(
          f"[{index}]",
          line,
        )

  return result


def main() -> int:
  body_renderer._is_toda_group_proof_narrative_rendered_reflexive_equality_step = (
    traced_helper
  )
  body_renderer._relocatable_toda_group_proof_narrative_direct_derivation_premises = (
    traced_relocatable
  )
  body_renderer._insert_toda_group_proof_narrative_relocated_direct_premises = (
    traced_insert
  )

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

  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  print("")
  print("=" * 88)
  print("FINAL")
  print("=" * 88)
  print(
    "target present:",
    TARGET in rendered,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

from __future__ import annotations

import inspect

import toda_group_proof_narrative_renderer as renderer
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def main() -> None:
  print(
    "=== public renderer source ==="
  )
  print(
    inspect.getsource(
      renderer.render_toda_group_proof_narrative_markdown
    )
  )

  helper_names = (
    "_phase159_r1_7c_r4_normalize_public_map_property_prose",
    "_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning",
    "_phase159_r1_7c_r4_reorder_public_equation_reference_conclusions",
    "_phase159_r1_6d_finalize_reference_and_linkage",
  )

  for name in helper_names:
    helper = getattr(
      renderer,
      name,
      None,
    )
    print()
    print(
      "=== "
      + name
      + " ==="
    )

    if helper is None:
      print(
        "MISSING"
      )
      continue

    print(
      inspect.getsource(
        helper
      )
    )

  report = build_standard_toda_report(
    n=2,
    k=1,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  baseline = (
    renderer
    ._phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  normalized = (
    renderer
    ._phase158_normalize_public_narrative_contract(
      presentation,
      baseline,
    )
  )

  print()
  print(
    "=== after Phase158 normalization ==="
  )
  print(
    normalized
  )

  map_prose = (
    renderer
    ._phase159_r1_7c_r4_normalize_public_map_property_prose(
      normalized
    )
  )

  print()
  print(
    "=== after map-property prose ==="
  )
  print(
    map_prose
  )

  numbered = (
    renderer
    ._phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      map_prose
    )
  )

  print()
  print(
    "=== after numbered reasoning ==="
  )
  print(
    numbered
  )

  reordered = (
    renderer
    ._phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
      numbered
    )
  )

  print()
  print(
    "=== after equation-reference reorder ==="
  )
  print(
    reordered
  )

  final = (
    renderer.render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  print()
  print(
    "=== actual final public narrative ==="
  )
  print(
    final
  )

  print()
  print(
    "=== checks ==="
  )
  checks = (
    (
      "numbered_stage_has_tag1",
      r"\tag{1}" in numbered,
    ),
    (
      "numbered_stage_has_tag2",
      r"\tag{2}" in numbered,
    ),
    (
      "reordered_stage_has_tag1",
      r"\tag{1}" in reordered,
    ),
    (
      "reordered_stage_has_tag2",
      r"\tag{2}" in reordered,
    ),
    (
      "final_has_tag1",
      r"\tag{1}" in final,
    ),
    (
      "final_has_tag2",
      r"\tag{2}" in final,
    ),
    (
      "final_has_numbered_conclusion",
      (
        r"(1), (2) より, "
        r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
      )
      in final,
    ),
  )

  for label, value in checks:
    print(
      label
      + ": "
      + (
        "YES"
        if value
        else "NO"
      )
    )


if __name__ == "__main__":
  main()

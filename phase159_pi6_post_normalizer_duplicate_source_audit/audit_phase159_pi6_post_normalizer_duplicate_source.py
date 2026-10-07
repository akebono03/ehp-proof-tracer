from __future__ import annotations

from pathlib import Path
import inspect
import sys


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(ROOT),
  )


import toda_group_proof_narrative_renderer as renderer_module
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGET = (
  r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
)


def _fresh_presentation():
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
  return build_toda_group_proof_presentation(
    replay
  )


def _print_stage(
  label: str,
  rendered: str,
) -> None:
  print("")
  print("=" * 78)
  print(label)
  print("=" * 78)
  print(
    "target occurrence count:",
    rendered.count(
      TARGET
    ),
  )

  for index, paragraph in enumerate(
    rendered.split(
      "\n\n"
    )
  ):
    if TARGET not in paragraph:
      continue

    print("")
    print(
      f"[paragraph {index}]"
    )
    print(
      paragraph.strip()
    )


def _print_function_source(
  name: str,
  function,
) -> None:
  print("")
  print("=" * 78)
  print(name)
  print("=" * 78)
  print(
    "source file:",
    inspect.getsourcefile(
      function
    ),
  )
  print(
    "first line:",
    function.__code__.co_firstlineno,
  )
  print("")
  print(
    inspect.getsource(
      function
    )
  )


def main() -> None:
  presentation = _fresh_presentation()

  baseline = (
    renderer_module
    ._phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  _print_stage(
    "1. BASELINE",
    baseline,
  )

  normalized = (
    renderer_module
    ._phase158_normalize_public_narrative_contract(
      presentation,
      baseline,
    )
  )
  _print_stage(
    "2. PHASE158 NORMALIZED",
    normalized,
  )

  map_property_prose = (
    renderer_module
    ._phase159_r1_7c_r4_normalize_public_map_property_prose(
      normalized
    )
  )
  _print_stage(
    "3. MAP PROPERTY PROSE NORMALIZATION",
    map_property_prose,
  )

  numbered_reasoning = (
    renderer_module
    ._phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      map_property_prose
    )
  )
  _print_stage(
    "4. NUMBERED MAP PROPERTY REASONING",
    numbered_reasoning,
  )

  reordered = (
    renderer_module
    ._phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
      numbered_reasoning
    )
  )
  _print_stage(
    "5. EQUATION/REFERENCE CONCLUSION REORDER",
    reordered,
  )

  direct = (
    renderer_module
    .render_toda_group_proof_narrative_markdown(
      _fresh_presentation()
    )
  )
  _print_stage(
    "6. DIRECT PUBLIC",
    direct,
  )

  print("")
  print("=" * 78)
  print("EQUALITY SUMMARY")
  print("=" * 78)
  print(
    "reordered == direct:",
    reordered == direct,
  )

  _print_function_source(
    "_phase159_r1_7c_r4_normalize_public_map_property_prose",
    renderer_module
    ._phase159_r1_7c_r4_normalize_public_map_property_prose,
  )
  _print_function_source(
    "_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning",
    renderer_module
    ._phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning,
  )
  _print_function_source(
    "_phase159_r1_7c_r4_reorder_public_equation_reference_conclusions",
    renderer_module
    ._phase159_r1_7c_r4_reorder_public_equation_reference_conclusions,
  )


if __name__ == "__main__":
  main()

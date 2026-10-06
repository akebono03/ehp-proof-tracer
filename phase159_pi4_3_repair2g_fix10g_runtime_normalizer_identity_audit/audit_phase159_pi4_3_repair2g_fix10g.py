from __future__ import annotations

from pathlib import Path
import inspect
import sys


ROOT = Path(__file__).resolve().parents[1]
RENDERER_PATH = ROOT / "toda_group_proof_narrative_renderer.py"

if str(ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      ROOT
    ),
  )

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


def main() -> int:
  source = RENDERER_PATH.read_text(
    encoding="utf-8"
  )

  function_marker = (
    "def _phase158_normalize_public_equation_numbers("
  )

  print(
    "=== Phase159 fix10g runtime normalizer identity audit ==="
  )
  print(
    "Production code changes: NONE"
  )
  print(
    "Renderer file:",
    renderer.__file__,
  )
  print(
    "Definition count:",
    source.count(
      function_marker
    ),
  )

  runtime_function = (
    renderer
    ._phase158_normalize_public_equation_numbers
  )

  print()
  print(
    "=== runtime function source ==="
  )
  runtime_source = inspect.getsource(
    runtime_function
  )
  print(
    runtime_source
  )

  print()
  print(
    "contains public_number:",
    "public_number" in runtime_source,
  )
  print(
    "contains numbered_map_properties:",
    "numbered_map_properties" in runtime_source,
  )
  print(
    "contains result.extend display conversion:",
    "result.extend" in runtime_source,
  )

  original = runtime_function

  def traced(
    proof_body,
  ):
    print()
    print(
      "=== runtime normalizer INPUT matching lines ==="
    )
    for line in proof_body:
      if (
        r"\tag{" in line
        or "単射" in line
        or "全射" in line
        or "零写像" in line
      ):
        print(
          repr(
            line
          )
        )

    result = original(
      proof_body
    )

    print()
    print(
      "=== runtime normalizer OUTPUT matching lines ==="
    )
    for line in result:
      if (
        r"\tag{" in line
        or "単射" in line
        or "全射" in line
        or "零写像" in line
        or r"\qquad (" in line
      ):
        print(
          repr(
            line
          )
        )

    return result

  renderer._phase158_normalize_public_equation_numbers = (
    traced
  )

  report = build_standard_toda_report(
    n=2,
    k=1,
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
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  print()
  print(
    "=== render pi_3^2 with runtime trace ==="
  )
  rendered = (
    renderer.render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  print()
  print(
    "=== final public Narrative ==="
  )
  print(
    rendered
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

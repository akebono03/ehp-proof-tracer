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


def _describe_function(
  name: str,
  function,
) -> None:
  print("")
  print("=" * 78)
  print(name)
  print("=" * 78)
  print(
    "id:",
    id(
      function
    ),
  )
  print(
    "module:",
    function.__module__,
  )
  print(
    "qualname:",
    function.__qualname__,
  )
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
  print(
    "globals renderer baseline id:",
    id(
      function.__globals__.get(
        "_phase158_baseline_render_toda_group_proof_narrative_markdown"
      )
    ),
  )
  print(
    "globals public normalizer id:",
    id(
      function.__globals__.get(
        "_phase158_normalize_public_narrative_contract"
      )
    ),
  )
  print("")
  print("source:")
  print(
    inspect.getsource(
      function
    )
  )


def _print_target(
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
    print(
      f"[paragraph {index}] "
      + paragraph.strip().replace(
        "\n",
        " / ",
      )
    )


def main() -> None:
  public_function = (
    renderer_module
    .render_toda_group_proof_narrative_markdown
  )
  baseline_function = (
    renderer_module
    ._phase158_baseline_render_toda_group_proof_narrative_markdown
  )
  normalize_function = (
    renderer_module
    ._phase158_normalize_public_narrative_contract
  )

  _describe_function(
    "PUBLIC FUNCTION",
    public_function,
  )
  _describe_function(
    "BASELINE FUNCTION",
    baseline_function,
  )
  _describe_function(
    "NORMALIZER FUNCTION",
    normalize_function,
  )

  module_path = Path(
    inspect.getsourcefile(
      public_function
    )
  )
  module_text = module_path.read_text(
    encoding="utf-8"
  )
  print("")
  print("=" * 78)
  print("SOURCE FILE DEF COUNTS")
  print("=" * 78)
  print(
    "public def count:",
    module_text.count(
      "def render_toda_group_proof_narrative_markdown("
    ),
  )
  print(
    "baseline def count:",
    module_text.count(
      "def _phase158_baseline_render_toda_group_proof_narrative_markdown("
    ),
  )
  print(
    "normalizer def count:",
    module_text.count(
      "def _phase158_normalize_public_narrative_contract("
    ),
  )

  baseline_calls = []
  normalize_calls = []

  original_baseline = baseline_function
  original_normalize = normalize_function

  def traced_baseline(
    presentation,
  ):
    result = original_baseline(
      presentation
    )
    baseline_calls.append(
      result
    )
    _print_target(
      (
        "DIRECT CALL INTERNAL BASELINE "
        f"CALL {len(baseline_calls)}"
      ),
      result,
    )
    return result

  def traced_normalize(
    presentation,
    rendered,
  ):
    _print_target(
      (
        "DIRECT CALL INTERNAL NORMALIZER "
        f"CALL {len(normalize_calls) + 1} INPUT"
      ),
      rendered,
    )
    result = original_normalize(
      presentation,
      rendered,
    )
    normalize_calls.append(
      result
    )
    _print_target(
      (
        "DIRECT CALL INTERNAL NORMALIZER "
        f"CALL {len(normalize_calls)} OUTPUT"
      ),
      result,
    )
    return result

  renderer_module._phase158_baseline_render_toda_group_proof_narrative_markdown = (
    traced_baseline
  )
  renderer_module._phase158_normalize_public_narrative_contract = (
    traced_normalize
  )

  direct = (
    renderer_module
    .render_toda_group_proof_narrative_markdown(
      _fresh_presentation()
    )
  )

  _print_target(
    "DIRECT PUBLIC FINAL",
    direct,
  )

  print("")
  print("=" * 78)
  print("CALL SUMMARY")
  print("=" * 78)
  print(
    "baseline call count:",
    len(
      baseline_calls
    ),
  )
  print(
    "normalizer call count:",
    len(
      normalize_calls
    ),
  )


if __name__ == "__main__":
  main()

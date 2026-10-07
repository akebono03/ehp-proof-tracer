from pathlib import Path
import inspect
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(
  REPO_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


import toda_group_proof_narrative_reason_renderer as reason_renderer


def main() -> int:
  function = (
    reason_renderer
    .order_toda_group_proof_narrative_injective_image_order_reason
  )
  source = inspect.getsource(
    function
  )
  source_path = Path(
    inspect.getsourcefile(
      function
    )
    or ""
  )

  print(
    "=============================================================="
  )
  print(
    "Phase 159 pi3_2 active reason-function audit17"
  )
  print(
    "=============================================================="
  )
  print(
    "source_path="
    + str(
      source_path
    )
  )

  markers = (
    (
      "exactness_kind",
      "EXACTNESS_TO_MAP_PROPERTY",
    ),
    (
      "definition_detection",
      '"を満たす"',
    ),
    (
      "definition_public_prefix",
      '"この同型写像により, "',
    ),
    (
      "math_spans_helper",
      "def math_spans(",
    ),
    (
      "visible_premise_records",
      "visible_premise_records",
    ),
    (
      "definition_spans",
      "definition_spans",
    ),
    (
      "premise_paragraphs",
      "premise_paragraphs",
    ),
  )

  print()
  print(
    "=== Marker presence ==="
  )

  for label, marker in markers:
    print(
      label
      + "="
      + str(
        marker in source
      )
    )

  return_marker = (
    'return "\\n\\n".join('
  )
  return_positions = []
  search_start = 0

  while True:
    index = source.find(
      return_marker,
      search_start,
    )

    if index < 0:
      break

    return_positions.append(
      index
    )
    search_start = (
      index
      + len(
        return_marker
      )
    )

  print()
  print(
    "return_join_positions="
    + repr(
      tuple(
        return_positions
      )
    )
  )

  definition_marker_position = source.find(
    "def math_spans("
  )
  print(
    "definition_marker_position="
    + str(
      definition_marker_position
    )
  )

  print()
  print(
    "=== Active function source ==="
  )
  print(
    source
  )

  output_path = (
    Path(__file__).resolve().parent
    / "active_reason_function_source.py.txt"
  )
  output_path.write_text(
    source,
    encoding="utf-8",
  )

  print()
  print(
    "saved_source="
    + str(
      output_path
    )
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

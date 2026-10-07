from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TARGET_PATH = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
SNAPSHOT_PATH = (
  Path(__file__).resolve().parent
  / "patched_functions_after_apply.py.txt"
)


HELPER_NAME = (
  "normalize_toda_group_proof_narrative_"
  "numbered_map_property_display"
)
RENDER_NAME = (
  "render_toda_group_proof_narrative_"
  "multi_argument_with_contributions_markdown"
)


NEW_HELPER = '''def normalize_toda_group_proof_narrative_numbered_map_property_display(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  normalized_paragraphs = []

  for paragraph in markdown.split(
    "\\n\\n"
  ):
    stripped = paragraph.strip()

    if "は零写像である." in paragraph:
      paragraph = paragraph.replace(
        "は零写像である.",
        "は零写像.",
      )
      stripped = paragraph.strip()

    property_suffixes = (
      (
        " は単射.",
        "は単射",
      ),
      (
        " は全射.",
        "は全射",
      ),
      (
        " は同型.",
        "は同型",
      ),
    )

    for suffix, property_text in property_suffixes:
      if (
        not stripped.startswith(
          "$"
        )
        or not stripped.endswith(
          suffix
        )
      ):
        continue

      math_and_suffix = stripped[
        : -len(
          suffix
        )
      ]

      if not math_and_suffix.endswith(
        "$"
      ):
        continue

      math_content = math_and_suffix[
        1:-1
      ]
      tag_marker = r"\\tag{"
      tag_index = math_content.rfind(
        tag_marker
      )

      if tag_index < 0:
        continue

      closing_brace_index = math_content.find(
        "}",
        tag_index
        + len(
          tag_marker
        ),
      )

      if (
        closing_brace_index < 0
        or closing_brace_index
        != len(
          math_content
        ) - 1
      ):
        continue

      number_text = math_content[
        tag_index
        + len(
          tag_marker
        ):
        closing_brace_index
      ]

      if not number_text.isdigit():
        continue

      map_latex = math_content[
        :tag_index
      ].rstrip()

      paragraph = (
        r"\\["
        + "\\n"
        + map_latex
        + r"\\quad\\text{"
        + property_text
        + r"}. \\qquad ("
        + number_text
        + ")"
        + "\\n"
        + r"\\]"
      )
      break

    normalized_paragraphs.append(
      paragraph
    )

  return "\\n\\n".join(
    normalized_paragraphs
  )


'''


def function_span(
  source: str,
  function_name: str,
) -> tuple[int, int]:
  marker = "def " + function_name + "("
  start = source.find(
    marker
  )

  if start < 0:
    raise RuntimeError(
      f"{function_name}: function not found"
    )

  match = re.search(
    r"\\n(?=def [A-Za-z0-9_]+\\()",
    source[
      start + 1:
    ],
  )

  if match is None:
    return (
      start,
      len(
        source
      ),
    )

  end = (
    start
    + 1
    + match.start()
    + 1
  )

  return (
    start,
    end,
  )


def main() -> int:
  source = TARGET_PATH.read_text(
    encoding="utf-8"
  )

  render_marker = (
    "def "
    + RENDER_NAME
    + "("
  )
  render_start = source.find(
    render_marker
  )

  if render_start < 0:
    raise RuntimeError(
      "target renderer function not found"
    )

  helper_marker = (
    "def "
    + HELPER_NAME
    + "("
  )

  if helper_marker not in source:
    source = (
      source[:render_start]
      + NEW_HELPER
      + source[render_start:]
    )

  render_start, render_end = function_span(
    source,
    RENDER_NAME,
  )
  render_source = source[
    render_start:render_end
  ]

  normalization_call = (
    "  rendered = (\\n"
    "    normalize_toda_group_proof_narrative_"
    "numbered_map_property_display(\\n"
    "      rendered\\n"
    "    )\\n"
    "  )\\n"
    "\\n"
  )

  if normalization_call not in render_source:
    insertion_marker = (
      "  generic_used_step_ids = (\\n"
    )
    insertion_index = render_source.find(
      insertion_marker
    )

    if insertion_index < 0:
      raise RuntimeError(
        "generic_used_step_ids insertion point not found "
        "inside local target renderer"
      )

    render_source = (
      render_source[:insertion_index]
      + normalization_call
      + render_source[insertion_index:]
    )

  if 'if "[R" not in rendered:' in render_source:
    raise RuntimeError(
      "fix10 no-marker Reference clearing unexpectedly returned"
    )

  source = (
    source[:render_start]
    + render_source
    + source[render_end:]
  )

  TARGET_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\\n",
  )

  helper_start, helper_end = function_span(
    source,
    HELPER_NAME,
  )
  render_start, render_end = function_span(
    source,
    RENDER_NAME,
  )

  SNAPSHOT_PATH.write_text(
    source[
      helper_start:helper_end
    ]
    + "\\n\\n"
    + source[
      render_start:render_end
    ],
    encoding="utf-8",
    newline="\\n",
  )

  print(
    "Phase 159 repair2g fix10c applied."
  )
  print(
    "Changed: "
    "toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "Added/retained helper:",
    HELPER_NAME,
  )
  print(
    "Changed function:",
    RENDER_NAME,
  )
  print(
    "Insertion strategy: helper immediately before target renderer."
  )
  print(
    "Normalization call inserted immediately before generic_used_step_ids."
  )
  print(
    "Full changed functions written to:"
  )
  print(
    SNAPSHOT_PATH
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TARGET_PATH = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
SNAPSHOT_PATH = (
  Path(__file__).resolve().parent
  / "patched_normalization_functions_after_apply.py.txt"
)


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
    r"\n(?=def [A-Za-z0-9_]+\()",
    source[start + 1:],
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
    "\\\\n\\\\n"
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
      tag_marker = r"\\\\tag{"
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
        r"\\\\["
        + "\\\\n"
        + map_latex
        + r"\\\\quad\\\\text{"
        + property_text
        + r"}. \\\\qquad ("
        + number_text
        + ")"
        + "\\\\n"
        + r"\\\\]"
      )
      break

    normalized_paragraphs.append(
      paragraph
    )

  return "\\\\n\\\\n".join(
    normalized_paragraphs
  )


'''


def main() -> int:
  source = TARGET_PATH.read_text(
    encoding="utf-8"
  )

  helper_name = (
    "normalize_toda_group_proof_narrative_"
    "numbered_map_property_display"
  )

  if (
    "def "
    + helper_name
    + "("
    not in source
  ):
    insertion_marker = (
      "def normalize_toda_group_proof_narrative_"
      "display_math_periods(\\n"
    )

    insertion_index = source.find(
      insertion_marker
    )

    if insertion_index < 0:
      raise RuntimeError(
        "display-math normalization insertion point not found"
      )

    source = (
      source[:insertion_index]
      + NEW_HELPER
      + source[insertion_index:]
    )

  render_function_name = (
    "render_toda_group_proof_narrative_"
    "multi_argument_with_contributions_markdown"
  )
  start, end = function_span(
    source,
    render_function_name,
  )
  render_function = source[
    start:end
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

  if normalization_call not in render_function:
    insertion_marker = (
      "  generic_used_step_ids = (\\n"
    )
    insertion_index = render_function.find(
      insertion_marker
    )

    if insertion_index < 0:
      raise RuntimeError(
        "generic_used_step_ids insertion point not found"
      )

    render_function = (
      render_function[:insertion_index]
      + normalization_call
      + render_function[insertion_index:]
    )

  source = (
    source[:start]
    + render_function
    + source[end:]
  )

  TARGET_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\\n",
  )

  helper_start, helper_end = function_span(
    source,
    helper_name,
  )
  render_start, render_end = function_span(
    source,
    render_function_name,
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

  if 'if "[R" not in rendered:' in source[
    render_start:render_end
  ]:
    raise RuntimeError(
      "fix10 no-marker Reference clearing unexpectedly returned"
    )

  print(
    "Phase 159 repair2g fix10b applied."
  )
  print(
    "Changed: "
    "toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "Added function: "
    + helper_name
  )
  print(
    "Changed function: "
    + render_function_name
  )
  print(
    "Behavior: numbered map properties are normalized "
    "only at final public-display stage."
  )
  print(
    "Behavior: zero-map wording normalized "
    "'は零写像である.' -> 'は零写像.'."
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

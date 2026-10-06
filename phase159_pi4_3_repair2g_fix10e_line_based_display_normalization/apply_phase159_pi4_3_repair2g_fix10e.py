from __future__ import annotations

from pathlib import Path


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

HELPER_LINES = [
  "def normalize_toda_group_proof_narrative_numbered_map_property_display(\n",
  "  markdown: str,\n",
  ") -> str:\n",
  "  if not isinstance(\n",
  "    markdown,\n",
  "    str,\n",
  "  ):\n",
  "    raise TypeError(\n",
  '      "markdown must be a str"\n',
  "    )\n",
  "\n",
  "  normalized_paragraphs = []\n",
  "\n",
  "  for paragraph in markdown.split(\n",
  '    "\\n\\n"\n',
  "  ):\n",
  "    stripped = paragraph.strip()\n",
  "\n",
  '    if "は零写像である." in paragraph:\n',
  "      paragraph = paragraph.replace(\n",
  '        "は零写像である.",\n',
  '        "は零写像.",\n',
  "      )\n",
  "      stripped = paragraph.strip()\n",
  "\n",
  "    property_suffixes = (\n",
  "      (\n",
  '        " は単射.",\n',
  '        "は単射",\n',
  "      ),\n",
  "      (\n",
  '        " は全射.",\n',
  '        "は全射",\n',
  "      ),\n",
  "      (\n",
  '        " は同型.",\n',
  '        "は同型",\n',
  "      ),\n",
  "    )\n",
  "\n",
  "    for suffix, property_text in property_suffixes:\n",
  "      if (\n",
  "        not stripped.startswith(\n",
  '          "$"\n',
  "        )\n",
  "        or not stripped.endswith(\n",
  "          suffix\n",
  "        )\n",
  "      ):\n",
  "        continue\n",
  "\n",
  "      math_and_suffix = stripped[\n",
  "        : -len(\n",
  "          suffix\n",
  "        )\n",
  "      ]\n",
  "\n",
  "      if not math_and_suffix.endswith(\n",
  '        "$"\n',
  "      ):\n",
  "        continue\n",
  "\n",
  "      math_content = math_and_suffix[\n",
  "        1:-1\n",
  "      ]\n",
  '      tag_marker = r"\\tag{"\n',
  "      tag_index = math_content.rfind(\n",
  "        tag_marker\n",
  "      )\n",
  "\n",
  "      if tag_index < 0:\n",
  "        continue\n",
  "\n",
  "      closing_brace_index = math_content.find(\n",
  '        "}",\n',
  "        tag_index\n",
  "        + len(\n",
  "          tag_marker\n",
  "        ),\n",
  "      )\n",
  "\n",
  "      if (\n",
  "        closing_brace_index < 0\n",
  "        or closing_brace_index\n",
  "        != len(\n",
  "          math_content\n",
  "        ) - 1\n",
  "      ):\n",
  "        continue\n",
  "\n",
  "      number_text = math_content[\n",
  "        tag_index\n",
  "        + len(\n",
  "          tag_marker\n",
  "        ):\n",
  "        closing_brace_index\n",
  "      ]\n",
  "\n",
  "      if not number_text.isdigit():\n",
  "        continue\n",
  "\n",
  "      map_latex = math_content[\n",
  "        :tag_index\n",
  "      ].rstrip()\n",
  "\n",
  "      paragraph = (\n",
  '        r"\\["\n',
  '        + "\\n"\n',
  "        + map_latex\n",
  '        + r"\\quad\\text{"\n',
  "        + property_text\n",
  '        + r"}. \\qquad ("\n',
  "        + number_text\n",
  '        + ")"\n',
  '        + "\\n"\n',
  '        + r"\\]"\n',
  "      )\n",
  "      break\n",
  "\n",
  "    normalized_paragraphs.append(\n",
  "      paragraph\n",
  "    )\n",
  "\n",
  '  return "\\n\\n".join(\n',
  "    normalized_paragraphs\n",
  "  )\n",
  "\n",
  "\n",
]

NORMALIZATION_CALL_LINES = [
  "  rendered = (\n",
  "    normalize_toda_group_proof_narrative_numbered_map_property_display(\n",
  "      rendered\n",
  "    )\n",
  "  )\n",
  "\n",
]


def main() -> int:
  source = TARGET_PATH.read_text(
    encoding="utf-8"
  )
  lines = source.splitlines(
    keepends=True
  )

  render_def_line = (
    "def render_toda_group_proof_narrative_"
    "multi_argument_with_contributions_markdown(\n"
  )
  render_indices = tuple(
    index
    for index, line in enumerate(
      lines
    )
    if line == render_def_line
  )

  if len(
    render_indices
  ) != 1:
    raise RuntimeError(
      "expected exactly one target renderer definition, found "
      + str(
        len(
          render_indices
        )
      )
    )

  render_index = render_indices[
    0
  ]

  helper_def_prefix = (
    "def "
    + HELPER_NAME
    + "(\n"
  )

  helper_indices = tuple(
    index
    for index, line in enumerate(
      lines
    )
    if line == helper_def_prefix
  )

  if not helper_indices:
    lines[
      render_index:render_index
    ] = HELPER_LINES

    render_index += len(
      HELPER_LINES
    )
  elif len(
    helper_indices
  ) != 1:
    raise RuntimeError(
      "expected at most one normalization helper, found "
      + str(
        len(
          helper_indices
        )
      )
    )

  next_top_level_def = next(
    (
      index
      for index in range(
        render_index + 1,
        len(
          lines
        ),
      )
      if lines[
        index
      ].startswith(
        "def "
      )
    ),
    len(
      lines
    ),
  )

  generic_indices = tuple(
    index
    for index in range(
      render_index,
      next_top_level_def,
    )
    if lines[
      index
    ] == "  generic_used_step_ids = (\n"
  )

  if len(
    generic_indices
  ) != 1:
    print(
      "Target renderer lines containing "
      "'generic_used_step_ids':"
    )
    for index in range(
      render_index,
      next_top_level_def,
    ):
      if (
        "generic_used_step_ids"
        in lines[
          index
        ]
      ):
        print(
          repr(
            lines[
              index
            ]
          )
        )

    raise RuntimeError(
      "expected exactly one generic_used_step_ids line "
      "inside target renderer, found "
      + str(
        len(
          generic_indices
        )
      )
    )

  normalization_call_head = (
    "    normalize_toda_group_proof_narrative_"
    "numbered_map_property_display(\n"
  )

  call_already_present = any(
    lines[
      index
    ] == normalization_call_head
    for index in range(
      render_index,
      next_top_level_def,
    )
  )

  if not call_already_present:
    insertion_index = generic_indices[
      0
    ]
    lines[
      insertion_index:insertion_index
    ] = NORMALIZATION_CALL_LINES

  patched_source = "".join(
    lines
  )

  if (
    'if "[R" not in rendered:'
    in patched_source
  ):
    target_start = patched_source.find(
      render_def_line.rstrip(
        "\n"
      )
    )
    target_end = patched_source.find(
      "\ndef ",
      target_start + 1,
    )

    if target_end < 0:
      target_end = len(
        patched_source
      )

    if (
      'if "[R" not in rendered:'
      in patched_source[
        target_start:target_end
      ]
    ):
      raise RuntimeError(
        "fix10 no-marker Reference clearing unexpectedly returned"
      )

  TARGET_PATH.write_text(
    patched_source,
    encoding="utf-8",
    newline="\n",
  )

  final_lines = patched_source.splitlines(
    keepends=True
  )
  helper_start = next(
    index
    for index, line in enumerate(
      final_lines
    )
    if line == helper_def_prefix
  )
  renderer_start = next(
    index
    for index, line in enumerate(
      final_lines
    )
    if line == render_def_line
  )
  renderer_end = next(
    (
      index
      for index in range(
        renderer_start + 1,
        len(
          final_lines
        ),
      )
      if final_lines[
        index
      ].startswith(
        "def "
      )
    ),
    len(
      final_lines
    ),
  )

  SNAPSHOT_PATH.write_text(
    "".join(
      final_lines[
        helper_start:renderer_end
      ]
    ),
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159 repair2g fix10e applied."
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
    "Changed function: "
    "render_toda_group_proof_narrative_"
    "multi_argument_with_contributions_markdown"
  )
  print(
    "Insertion strategy: exact line-based matching."
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

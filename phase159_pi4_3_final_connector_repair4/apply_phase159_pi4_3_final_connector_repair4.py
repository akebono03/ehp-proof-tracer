from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent

RENDERER_PATH = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi4_3_final_connector_repair.py"
)


def replace_function(
  source: str,
) -> str:
  start_marker = (
    "def suppress_toda_group_proof_narrative_dangling_connectors(\n"
  )
  end_marker = (
    "\ndef order_toda_group_proof_narrative_visible_relation_dependencies(\n"
  )

  start = source.find(
    start_marker
  )

  if start < 0:
    raise RuntimeError(
      "dangling-connector function start not found"
    )

  end = source.find(
    end_marker,
    start,
  )

  if end < 0:
    raise RuntimeError(
      "dangling-connector function end not found"
    )

  replacement = 'def suppress_toda_group_proof_narrative_dangling_connectors(\n  markdown: str,\n) -> str:\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  standalone_connectors = {\n    "以上より,",\n    "したがって,",\n    "これより,",\n    "これらより,",\n  }\n\n  def numbered_connector_numbers(\n    line: str,\n  ) -> tuple[\n    int,\n    ...,\n  ] | None:\n    stripped = line.strip()\n\n    if (\n      not stripped.startswith(\n        "("\n      )\n      or not stripped.endswith(\n        "より,"\n      )\n      or "$" in stripped\n      or "[R" in stripped\n    ):\n      return None\n\n    relation_text = stripped[\n      : -len(\n        "より,"\n      )\n    ].strip()\n    parts = tuple(\n      part.strip()\n      for part in relation_text.split(\n        " と "\n      )\n    )\n\n    if not parts:\n      return None\n\n    numbers = []\n\n    for part in parts:\n      if (\n        len(\n          part\n        ) < 3\n        or not part.startswith(\n          "("\n        )\n        or not part.endswith(\n          ")"\n        )\n      ):\n        return None\n\n      number_text = part[\n        1:-1\n      ]\n\n      if not number_text.isdigit():\n        return None\n\n      numbers.append(\n        int(\n          number_text\n        )\n      )\n\n    return tuple(\n      numbers\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n  retained_paragraphs = []\n  pending_connector = None\n\n  for paragraph_index, paragraph in enumerate(\n    paragraphs\n  ):\n    lines = paragraph.splitlines()\n    moved_connector = None\n\n    while lines:\n      stripped = lines[\n        -1\n      ].strip()\n\n      if stripped in standalone_connectors:\n        next_paragraph = next(\n          (\n            candidate.strip()\n            for candidate in paragraphs[\n              paragraph_index + 1:\n            ]\n            if candidate.strip()\n          ),\n          "",\n        )\n        has_following_derivation = (\n          "$" in next_paragraph\n          and not next_paragraph.startswith(\n            "[R"\n          )\n        )\n\n        if has_following_derivation:\n          moved_connector = stripped\n\n        lines.pop()\n        continue\n\n      connector_numbers = (\n        numbered_connector_numbers(\n          stripped\n        )\n      )\n\n      if connector_numbers is None:\n        break\n\n      previous_text = "\\n\\n".join(\n        paragraphs[\n          :paragraph_index\n        ]\n      )\n      referenced_tags_exist = all(\n        (\n          r"\\tag{"\n          + str(\n            number\n          )\n          + "}"\n        )\n        in previous_text\n        for number in connector_numbers\n      )\n\n      next_paragraph = next(\n        (\n          candidate.strip()\n          for candidate in paragraphs[\n            paragraph_index + 1:\n          ]\n          if candidate.strip()\n        ),\n        "",\n      )\n      has_following_derivation = (\n        "$" in next_paragraph\n      )\n\n      if (\n        referenced_tags_exist\n        and has_following_derivation\n      ):\n        break\n\n      lines.pop()\n\n    if lines:\n      normalized = "\\n".join(\n        lines\n      )\n      stripped = normalized.lstrip()\n\n      if pending_connector is not None:\n        leading = len(\n          normalized\n        ) - len(\n          stripped\n        )\n        normalized = (\n          normalized[\n            :leading\n          ]\n          + pending_connector\n          + " "\n          + stripped\n        )\n        pending_connector = None\n\n      stripped = normalized.lstrip()\n\n      for connector in standalone_connectors:\n        prefix = (\n          connector\n          + " "\n        )\n\n        if (\n          stripped.startswith(\n            prefix\n            + "[R"\n          )\n        ):\n          leading = len(\n            normalized\n          ) - len(\n            stripped\n          )\n          normalized = (\n            normalized[\n              :leading\n            ]\n            + stripped[\n              len(\n                prefix\n              ):\n            ]\n          )\n          break\n\n      if normalized.strip():\n        retained_paragraphs.append(\n          normalized\n        )\n\n    if moved_connector is not None:\n      pending_connector = moved_connector\n\n  return "\\n\\n".join(\n    retained_paragraphs\n  )\n'

  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n"
    + source[
      end:
    ]
  )


def main() -> int:
  source = RENDERER_PATH.read_text(
    encoding="utf-8",
  )
  updated = replace_function(
    source
  )

  RENDERER_PATH.write_text(
    updated,
    encoding="utf-8",
  )

  TEST_PATH.write_text(
    (
      PACKAGE_ROOT
      / "test_phase159_pi4_3_final_connector_repair.py"
    ).read_text(
      encoding="utf-8",
    ),
    encoding="utf-8",
  )

  print(
    "Phase 159 final-connector repair4 applied."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent

RENDERER_PATH = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
NEW_TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi4_3_contribution_connector_ownership.py"
)
REPAIR4_TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi4_3_final_connector_repair.py"
)


def replace_function(
  source: str,
  start_marker: str,
  next_marker: str,
  replacement: str,
) -> str:
  start = source.find(
    start_marker
  )

  if start < 0:
    raise RuntimeError(
      "function start not found: "
      + start_marker
    )

  end = source.find(
    next_marker,
    start,
  )

  if end < 0:
    raise RuntimeError(
      "function end not found after: "
      + start_marker
    )

  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n\n"
    + source[
      end:
    ]
  )


def main() -> int:
  source = RENDERER_PATH.read_text(
    encoding="utf-8",
  )

  source = replace_function(
    source,
    "def _contribution_insertion_indices(\n",
    "def _direct_contribution_dependency_pairs(\n",
    'def _contribution_insertion_indices(\n  markdown: str,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  arguments: tuple[\n    TodaGroupProofNarrativeArgument,\n    ...,\n  ],\n  ordered_contributions,\n) -> tuple[\n  tuple[\n    int | None,\n    ...,\n  ],\n  ...,\n]:\n  result = []\n  standalone_conclusion_connectors = {\n    "以上より,",\n    "したがって,",\n    "これより,",\n    "これらより,",\n  }\n\n  for argument_index, contributions in enumerate(\n    ordered_contributions\n  ):\n    if not contributions:\n      result.append(())\n      continue\n\n    argument = arguments[\n      argument_index\n    ]\n    conclusion_step = (\n      extract_toda_group_proof_narrative_argument_conclusion_step(\n        argument\n      )\n    )\n    conclusion_index = None\n\n    if conclusion_step is not None:\n      conclusion_line = (\n        _render_generic_narrative_step(\n          conclusion_step\n        )\n      )\n      candidate_index = markdown.find(\n        conclusion_line\n      )\n\n      if candidate_index >= 0:\n        conclusion_index = candidate_index\n\n        prefix = markdown[\n          :conclusion_index\n        ].rstrip()\n\n        if prefix:\n          previous_paragraph_start = (\n            prefix.rfind(\n              "\\n\\n"\n            )\n            + 2\n          )\n          previous_paragraph = prefix[\n            previous_paragraph_start:\n          ].strip()\n\n          if (\n            previous_paragraph\n            in standalone_conclusion_connectors\n          ):\n            conclusion_index = (\n              previous_paragraph_start\n            )\n\n    if conclusion_index is None:\n      conclusion_index = (\n        _argument_fallback_anchor_index(\n          markdown,\n          blocks,\n          argument,\n          contributions,\n        )\n      )\n\n    if conclusion_index is None:\n      result.append(\n        tuple(\n          None\n          for _ in contributions\n        )\n      )\n      continue\n\n    indices = [\n      None\n      for _ in contributions\n    ]\n\n    for contribution_index, contribution in enumerate(\n      contributions\n    ):\n      if (\n        contribution.placement\n        is TodaGroupProofNarrativeContributionPlacement\n        .AT_PROVIDER_ANCHOR\n      ):\n        anchor_index = _provider_anchor_index(\n          markdown,\n          blocks,\n          contribution.provider_keys,\n        )\n        indices[\n          contribution_index\n        ] = (\n          conclusion_index\n          if anchor_index is None\n          else anchor_index\n        )\n        continue\n\n      if (\n        contribution.placement\n        is TodaGroupProofNarrativeContributionPlacement\n        .BEFORE_ARGUMENT_CONCLUSION\n      ):\n        indices[\n          contribution_index\n        ] = conclusion_index\n\n    for contribution_index in range(\n      len(contributions) - 1,\n      -1,\n      -1,\n    ):\n      contribution = contributions[\n        contribution_index\n      ]\n\n      if (\n        contribution.placement\n        is not TodaGroupProofNarrativeContributionPlacement\n        .BEFORE_DEPENDENT_CONTRIBUTION\n      ):\n        continue\n\n      dependent_index = next(\n        (\n          indices[index]\n          for index in range(\n            contribution_index + 1,\n            len(contributions),\n          )\n          if indices[index] is not None\n        ),\n        conclusion_index,\n      )\n      indices[\n        contribution_index\n      ] = dependent_index\n\n    result.append(\n      tuple(\n        indices\n      )\n    )\n\n  return tuple(\n    result\n  )\n',
  )

  source = replace_function(
    source,
    "def suppress_toda_group_proof_narrative_dangling_connectors(\n",
    "def order_toda_group_proof_narrative_visible_relation_dependencies(\n",
    'def suppress_toda_group_proof_narrative_dangling_connectors(\n  markdown: str,\n) -> str:\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  standalone_connectors = {\n    "以上より,",\n    "したがって,",\n    "これより,",\n    "これらより,",\n  }\n\n  def numbered_connector_numbers(\n    line: str,\n  ) -> tuple[\n    int,\n    ...,\n  ] | None:\n    stripped = line.strip()\n\n    if (\n      not stripped.startswith(\n        "("\n      )\n      or not stripped.endswith(\n        "より,"\n      )\n      or "$" in stripped\n      or "[R" in stripped\n    ):\n      return None\n\n    relation_text = stripped[\n      : -len(\n        "より,"\n      )\n    ].strip()\n    parts = tuple(\n      part.strip()\n      for part in relation_text.split(\n        " と "\n      )\n    )\n\n    if not parts:\n      return None\n\n    numbers = []\n\n    for part in parts:\n      if (\n        len(\n          part\n        ) < 3\n        or not part.startswith(\n          "("\n        )\n        or not part.endswith(\n          ")"\n        )\n      ):\n        return None\n\n      number_text = part[\n        1:-1\n      ]\n\n      if not number_text.isdigit():\n        return None\n\n      numbers.append(\n        int(\n          number_text\n        )\n      )\n\n    return tuple(\n      numbers\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n  retained_paragraphs = []\n\n  for paragraph_index, paragraph in enumerate(\n    paragraphs\n  ):\n    lines = paragraph.splitlines()\n\n    while lines:\n      stripped = lines[\n        -1\n      ].strip()\n\n      if stripped in standalone_connectors:\n        lines.pop()\n        continue\n\n      connector_numbers = (\n        numbered_connector_numbers(\n          stripped\n        )\n      )\n\n      if connector_numbers is None:\n        break\n\n      previous_text = "\\n\\n".join(\n        paragraphs[\n          :paragraph_index\n        ]\n      )\n      referenced_tags_exist = all(\n        (\n          r"\\tag{"\n          + str(\n            number\n          )\n          + "}"\n        )\n        in previous_text\n        for number in connector_numbers\n      )\n\n      next_paragraph = next(\n        (\n          candidate.strip()\n          for candidate in paragraphs[\n            paragraph_index + 1:\n          ]\n          if candidate.strip()\n        ),\n        "",\n      )\n      has_following_derivation = (\n        "$" in next_paragraph\n      )\n\n      if (\n        referenced_tags_exist\n        and has_following_derivation\n      ):\n        break\n\n      lines.pop()\n\n    if not lines:\n      continue\n\n    normalized = "\\n".join(\n      lines\n    )\n    stripped = normalized.lstrip()\n\n    for connector in standalone_connectors:\n      prefix = (\n        connector\n        + " "\n      )\n\n      if (\n        stripped.startswith(\n          prefix\n          + "[R"\n        )\n      ):\n        leading = len(\n          normalized\n        ) - len(\n          stripped\n        )\n        normalized = (\n          normalized[\n            :leading\n          ]\n          + stripped[\n            len(\n              prefix\n            ):\n          ]\n        )\n        break\n\n    if normalized.strip():\n      retained_paragraphs.append(\n        normalized\n      )\n\n  return "\\n\\n".join(\n    retained_paragraphs\n  )\n',
  )

  RENDERER_PATH.write_text(
    source,
    encoding="utf-8",
  )

  NEW_TEST_PATH.write_text(
    (
      PACKAGE_ROOT
      / "test_phase159_pi4_3_contribution_connector_ownership.py"
    ).read_text(
      encoding="utf-8",
    ),
    encoding="utf-8",
  )

  if REPAIR4_TEST_PATH.exists():
    REPAIR4_TEST_PATH.unlink()

  print(
    "Phase 159 contribution-connector ownership repair5 applied."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

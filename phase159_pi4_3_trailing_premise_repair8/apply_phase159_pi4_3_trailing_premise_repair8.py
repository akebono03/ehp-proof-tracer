from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

RENDERER_PATH = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi4_3_trailing_premise_order.py"
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

  updated = replace_function(
    source,
    "def _contribution_insertion_indices(\n",
    "def _direct_contribution_dependency_pairs(\n",
    'def _contribution_insertion_indices(\n  markdown: str,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  arguments: tuple[\n    TodaGroupProofNarrativeArgument,\n    ...,\n  ],\n  ordered_contributions,\n) -> tuple[\n  tuple[\n    int | None,\n    ...,\n  ],\n  ...,\n]:\n  result = []\n\n  for argument_index, contributions in enumerate(\n    ordered_contributions\n  ):\n    if not contributions:\n      result.append(())\n      continue\n\n    argument = arguments[\n      argument_index\n    ]\n    conclusion_step = (\n      extract_toda_group_proof_narrative_argument_conclusion_step(\n        argument\n      )\n    )\n    conclusion_index = None\n\n    if conclusion_step is not None:\n      conclusion_line = (\n        _render_generic_narrative_step(\n          conclusion_step\n        )\n      )\n      candidate_index = markdown.find(\n        conclusion_line\n      )\n\n      if candidate_index >= 0:\n        conclusion_index = candidate_index\n\n        prefix = markdown[\n          :conclusion_index\n        ].rstrip()\n        previous_paragraph_start = (\n          prefix.rfind(\n            "\\n\\n"\n          )\n          + 2\n        )\n        previous_paragraph = prefix[\n          previous_paragraph_start:\n        ].strip()\n        standalone_conclusion_connectors = {\n          "以上より,",\n          "したがって,",\n          "これより,",\n          "これらより,",\n        }\n\n        if (\n          previous_paragraph\n          in standalone_conclusion_connectors\n        ):\n          conclusion_index = (\n            previous_paragraph_start\n          )\n\n    if conclusion_index is None:\n      conclusion_index = (\n        _argument_fallback_anchor_index(\n          markdown,\n          blocks,\n          argument,\n          contributions,\n        )\n      )\n\n    if conclusion_index is None:\n      result.append(\n        tuple(\n          None\n          for _ in contributions\n        )\n      )\n      continue\n\n    indices = [\n      None\n      for _ in contributions\n    ]\n\n    for contribution_index, contribution in enumerate(\n      contributions\n    ):\n      if (\n        contribution.placement\n        is TodaGroupProofNarrativeContributionPlacement\n        .AT_PROVIDER_ANCHOR\n      ):\n        anchor_index = _provider_anchor_index(\n          markdown,\n          blocks,\n          contribution.provider_keys,\n        )\n        indices[\n          contribution_index\n        ] = (\n          conclusion_index\n          if anchor_index is None\n          else min(\n            anchor_index,\n            conclusion_index,\n          )\n        )\n        continue\n\n      if (\n        contribution.placement\n        is TodaGroupProofNarrativeContributionPlacement\n        .BEFORE_ARGUMENT_CONCLUSION\n      ):\n        indices[\n          contribution_index\n        ] = conclusion_index\n\n    for contribution_index in range(\n      len(contributions) - 1,\n      -1,\n      -1,\n    ):\n      contribution = contributions[\n        contribution_index\n      ]\n      if (\n        contribution.placement\n        is not TodaGroupProofNarrativeContributionPlacement\n        .BEFORE_DEPENDENT_CONTRIBUTION\n      ):\n        continue\n\n      dependent_index = next(\n        (\n          indices[index]\n          for index in range(\n            contribution_index + 1,\n            len(contributions),\n          )\n          if indices[index] is not None\n        ),\n        conclusion_index,\n      )\n      indices[\n        contribution_index\n      ] = dependent_index\n\n    result.append(\n      tuple(\n        indices\n      )\n    )\n\n  return tuple(\n    result\n  )\n',
  )

  RENDERER_PATH.write_text(
    updated,
    encoding="utf-8",
  )

  TEST_PATH.write_text(
    (
      Path(__file__).resolve().parent
      / "test_phase159_pi4_3_trailing_premise_order.py"
    ).read_text(
      encoding="utf-8",
    ),
    encoding="utf-8",
  )

  print(
    "Phase 159 pi4_3 trailing-premise repair8 applied."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

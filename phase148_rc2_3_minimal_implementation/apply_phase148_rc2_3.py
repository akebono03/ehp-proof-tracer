from pathlib import Path

ROOT = Path.cwd()
PACKAGE = Path(__file__).resolve().parent


def replace_once(path, old, new):
  text = path.read_text(encoding="utf-8")
  count = text.count(old)
  if count != 1:
    raise SystemExit(
      f"{path}: expected one replacement target, found {count}"
    )
  path.write_text(
    text.replace(old, new, 1),
    encoding="utf-8",
    newline="\n",
  )


def main():
  (ROOT / "toda_group_proof_narrative_exactness_exposure.py").write_text(
    (PACKAGE / "toda_group_proof_narrative_exactness_exposure.py").read_text(
      encoding="utf-8"
    ),
    encoding="utf-8",
    newline="\n",
  )

  path = ROOT / "toda_group_proof_narrative_exactness_contribution_ownership.py"
  replace_once(
    path,
    "from toda_group_proof_narrative_exactness_display_contributions import (\n"
    "  TodaGroupProofNarrativeExactnessDisplayContribution,\n"
    "  TodaGroupProofNarrativeExactnessDisplayContributionKind,\n"
    ")\n",
    "from toda_group_proof_narrative_exactness_display_contributions import (\n"
    "  TodaGroupProofNarrativeExactnessDisplayContribution,\n"
    "  TodaGroupProofNarrativeExactnessDisplayContributionKind,\n"
    ")\n"
    "from toda_group_proof_narrative_exactness_exposure import (\n"
    "  TodaGroupProofNarrativeExactnessExposureClass,\n"
    ")\n",
  )
  replace_once(
    path,
    "  primary_component: (\n"
    "    TodaGroupProofNarrativeExactnessMethodComponent\n"
    "    | None\n"
    "  ),\n"
    ") -> tuple[\n",
    "  primary_component: (\n"
    "    TodaGroupProofNarrativeExactnessMethodComponent\n"
    "    | None\n"
    "  ),\n"
    "  exposure_class: (\n"
    "    TodaGroupProofNarrativeExactnessExposureClass\n"
    "    | None\n"
    "  ) = None,\n"
    ") -> tuple[\n",
  )
  replace_once(
    path,
    "  if primary_component is None:\n"
    "    return contributions\n\n"
    "  is_primary_evidence_block = any(\n",
    "  if (\n"
    "    exposure_class is not None\n"
    "    and not isinstance(\n"
    "      exposure_class,\n"
    "      TodaGroupProofNarrativeExactnessExposureClass,\n"
    "    )\n"
    "  ):\n"
    "    raise TypeError(\n"
    '      "exposure_class must be a "\n'
    '      "TodaGroupProofNarrativeExactnessExposureClass "\n'
    '      "or None"\n'
    "    )\n\n"
    "  if (\n"
    "    exposure_class\n"
    "    is TodaGroupProofNarrativeExactnessExposureClass\n"
    "    .UNOWNED_RECURSIVE\n"
    "  ):\n"
    "    return ()\n\n"
    "  if (\n"
    "    exposure_class\n"
    "    is TodaGroupProofNarrativeExactnessExposureClass\n"
    "    .AMBIGUOUS_RELEVANT\n"
    "  ):\n"
    "    return contributions\n\n"
    "  if primary_component is None:\n"
    "    return contributions\n\n"
    "  is_primary_evidence_block = any(\n",
  )

  path = ROOT / "toda_group_proof_narrative_argument_body_renderer.py"
  replace_once(
    path,
    "from toda_group_proof_narrative_exactness_display_contributions import (\n"
    "  TodaGroupProofNarrativeExactnessDisplayContributionKind,\n"
    "  extract_toda_group_proof_narrative_exactness_display_contributions,\n"
    ")\n",
    "from toda_group_proof_narrative_exactness_display_contributions import (\n"
    "  TodaGroupProofNarrativeExactnessDisplayContributionKind,\n"
    "  extract_toda_group_proof_narrative_exactness_display_contributions,\n"
    ")\n"
    "from toda_group_proof_narrative_exactness_exposure import (\n"
    "  TodaGroupProofNarrativeExactnessExposureClass,\n"
    ")\n",
  )
  replace_once(
    path,
    "  primary_component: (\n"
    "    TodaGroupProofNarrativeExactnessMethodComponent\n"
    "    | None\n"
    "  ),\n"
    "  excluded_exactness_contribution_keys: (\n",
    "  primary_component: (\n"
    "    TodaGroupProofNarrativeExactnessMethodComponent\n"
    "    | None\n"
    "  ),\n"
    "  exposure_class: (\n"
    "    TodaGroupProofNarrativeExactnessExposureClass\n"
    "    | None\n"
    "  ),\n"
    "  excluded_exactness_contribution_keys: (\n",
  )
  replace_once(
    path,
    "      primary_component,\n"
    "    )\n"
    "  )\n\n"
    "  if excluded_exactness_contribution_keys is not None:\n",
    "      primary_component,\n"
    "      exposure_class,\n"
    "    )\n"
    "  )\n\n"
    "  if excluded_exactness_contribution_keys is not None:\n",
  )
  replace_once(
    path,
    "  primary_component: (\n"
    "    TodaGroupProofNarrativeExactnessMethodComponent\n"
    "    | None\n"
    "  ),\n"
    "  excluded_non_exact_block_ids: (\n",
    "  primary_component: (\n"
    "    TodaGroupProofNarrativeExactnessMethodComponent\n"
    "    | None\n"
    "  ),\n"
    "  exactness_exposure_by_block_id: (\n"
    "    dict[\n"
    "      int,\n"
    "      TodaGroupProofNarrativeExactnessExposureClass,\n"
    "    ]\n"
    "    | None\n"
    "  ) = None,\n"
    "  excluded_non_exact_block_ids: (\n",
  )
  replace_once(
    path,
    "  if (\n"
    "    excluded_non_exact_block_ids is not None\n",
    "  if (\n"
    "    exactness_exposure_by_block_id is not None\n"
    "    and not isinstance(\n"
    "      exactness_exposure_by_block_id,\n"
    "      dict,\n"
    "    )\n"
    "  ):\n"
    "    raise TypeError(\n"
    '      "exactness_exposure_by_block_id must be "\n'
    '      "a dict or None"\n'
    "    )\n\n"
    "  if exactness_exposure_by_block_id is not None:\n"
    "    for block_id, exposure_class in exactness_exposure_by_block_id.items():\n"
    "      if not isinstance(block_id, int) or isinstance(block_id, bool):\n"
    "        raise TypeError(\n"
    '          "exactness_exposure_by_block_id keys must be integers"\n'
    "        )\n"
    "      if not isinstance(\n"
    "        exposure_class,\n"
    "        TodaGroupProofNarrativeExactnessExposureClass,\n"
    "      ):\n"
    "        raise TypeError(\n"
    '          "exactness_exposure_by_block_id values must be "\n'
    '          "TodaGroupProofNarrativeExactnessExposureClass objects"\n'
    "        )\n\n"
    "  if (\n"
    "    excluded_non_exact_block_ids is not None\n",
  )
  replace_once(
    path,
    "          primary_component,\n"
    "          excluded_exactness_contribution_keys,\n"
    "        )\n",
    "          primary_component,\n"
    "          (\n"
    "            None\n"
    "            if exactness_exposure_by_block_id is None\n"
    "            else exactness_exposure_by_block_id.get(id(block))\n"
    "          ),\n"
    "          excluded_exactness_contribution_keys,\n"
    "        )\n",
  )

  path = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"
  replace_once(
    path,
    "from toda_group_proof_narrative_exactness_contribution_ownership import (\n",
    "from toda_group_proof_narrative_exactness_components import (\n"
    "  build_toda_group_proof_narrative_exactness_method_components,\n"
    ")\n"
    "from toda_group_proof_narrative_exactness_contribution_ownership import (\n",
  )
  replace_once(
    path,
    "from toda_group_proof_narrative_exactness_selection import (\n",
    "from toda_group_proof_narrative_exactness_exposure import (\n"
    "  TodaGroupProofNarrativeExactnessExposureClass,\n"
    "  classify_toda_group_proof_narrative_exactness_component_exposure,\n"
    ")\n"
    "from toda_group_proof_narrative_exactness_selection import (\n",
  )
  replace_once(
    path,
    "from toda_group_proof_narrative_references import (\n",
    "from toda_group_proof_narrative_relevant_groups import (\n"
    "  extract_toda_group_proof_narrative_argument_relevant_groups,\n"
    ")\n"
    "from toda_group_proof_narrative_references import (\n",
  )
  replace_once(
    path,
    "    primary_component = (\n"
    "      select_toda_group_proof_narrative_argument_primary_exactness_component(\n",
    "    components = (\n"
    "      build_toda_group_proof_narrative_exactness_method_components(\n"
    "        evidence\n"
    "      )\n"
    "    )\n"
    "    relevant_groups = (\n"
    "      extract_toda_group_proof_narrative_argument_relevant_groups(\n"
    "        presentation,\n"
    "        blocks,\n"
    "        argument,\n"
    "      )\n"
    "    )\n"
    "    primary_component = (\n"
    "      select_toda_group_proof_narrative_argument_primary_exactness_component(\n",
  )
  marker = (
    "    local_body_blocks = (\n"
    "      extract_toda_group_proof_narrative_argument_local_body_blocks(\n"
  )
  insertion = (
    "    exactness_exposure_by_block_id = {}\n\n"
    "    for component in components:\n"
    "      exposure_class = (\n"
    "        classify_toda_group_proof_narrative_exactness_component_exposure(\n"
    "          relevant_groups,\n"
    "          components,\n"
    "          component,\n"
    "        )\n"
    "      )\n"
    "      for evidence_block in component.evidence_blocks:\n"
    "        evidence_block_id = id(evidence_block)\n"
    "        existing_exposure = exactness_exposure_by_block_id.get(\n"
    "          evidence_block_id\n"
    "        )\n"
    "        if (\n"
    "          existing_exposure is not None\n"
    "          and existing_exposure is not exposure_class\n"
    "        ):\n"
    "          exactness_exposure_by_block_id[evidence_block_id] = (\n"
    "            TodaGroupProofNarrativeExactnessExposureClass\n"
    "            .AMBIGUOUS_RELEVANT\n"
    "          )\n"
    "          continue\n"
    "        exactness_exposure_by_block_id[evidence_block_id] = exposure_class\n\n"
    + marker
  )
  replace_once(path, marker, insertion)
  replace_once(
    path,
    "        primary_component,\n"
    "        excluded_non_exact_block_ids=frozenset(\n",
    "        primary_component,\n"
    "        exactness_exposure_by_block_id=exactness_exposure_by_block_id,\n"
    "        excluded_non_exact_block_ids=frozenset(\n",
  )
  replace_once(
    path,
    "          primary_component,\n"
    "        )\n"
    "      )\n\n"
    "      for contribution in body_contributions:\n",
    "          primary_component,\n"
    "          exactness_exposure_by_block_id.get(id(block)),\n"
    "        )\n"
    "      )\n\n"
    "      for contribution in body_contributions:\n",
  )

  target = ROOT / "tests" / "test_phase148_rc2_3_exactness_exposure.py"
  target.write_text(
    (PACKAGE / "test_phase148_rc2_3_exactness_exposure.py").read_text(
      encoding="utf-8"
    ),
    encoding="utf-8",
    newline="\n",
  )

  print("Phase 148 RC2-3 minimal implementation applied.")
  print("Production files changed: 4")
  print("Focused test file added: tests/test_phase148_rc2_3_exactness_exposure.py")
  print("RC3 ordering unchanged.")


if __name__ == "__main__":
  main()

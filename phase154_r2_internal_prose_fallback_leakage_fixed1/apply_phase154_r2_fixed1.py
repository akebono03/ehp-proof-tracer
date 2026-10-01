from pathlib import Path
import shutil

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = REPO_ROOT / "toda_group_proof_generic_narrative_renderer.py"
BACKUP = REPO_ROOT / "phase154_r2_internal_prose_fallback_leakage_fixed1" / "backup_before_fixed1" / TARGET.name

IMPORTS = 'from expression import (\n  Composition,\n  HomotopyElement,\n)\nfrom homotopy_groups import (\n  DirectSumGroup,\n  TodaDeltaMap,\n  TodaHopfInvariantMap,\n  TodaIteratedSuspensionMap,\n  TodaPrimaryGroup,\n  TodaSuspensionMap,\n)\nfrom proof import (\n  ProofStep,\n)\nfrom scalar_rules import (\n  ScalarGreaterEqualStatement,\n)\nfrom repository_element_presentation import (\n  render_repository_conclusion_latex,\n)\nfrom toda_group_proof_aggregate_statement_renderer import (\n  render_toda_group_proof_aggregate_statement_prose,\n)\nfrom toda_group_proof_narrative_blocks import (\n  TodaGroupProofNarrativeBlock,\n  TodaGroupProofNarrativeMathematicalBlockRole,\n)\nfrom toda_group_proof_narrative_provenance_catalog import (\n  is_toda_group_proof_narrative_provenance_only_statement,\n)\nfrom toda_group_proof_narrative_semantics import (\n  TodaGroupProofNarrativeSemanticSidecar,\n  build_toda_group_proof_narrative_semantic_sidecar,\n)\nfrom toda_group_proof_presentation import (\n  TodaGroupProofPresentation,\n)\nfrom toda_human_readable_renderer import (\n  _render_scalar_latex,\n  render_toda_expression_latex,\n)\nfrom toda_proof_narrative_renderer import (\n  render_toda_primary_group_latex,\n  render_toda_proof_statement_latex,\n  render_toda_raw_group_structure_latex,\n)\nfrom toda_rules import (\n  Toda36Lemma514SigmaDoublePrimeBridgeStatement,\n  Toda45IsomorphismStatement,\n  Toda52CompositionIsomorphismStatement,\n  Toda53NuPrimeBracketSpecializationStatement,\n  Toda55NuFamilyFiniteDimensionalStatement,\n  Toda56Nu4DecompositionStatement,\n  TodaDeltaInjectiveStatement,\n  TodaDeltaKernelFreeCyclicStatement,\n  TodaDeltaSurjectiveStatement,\n  TodaDeltaZeroStatement,\n  TodaHopfInvariantInjectiveStatement,\n  TodaHopfInvariantIsomorphismStatement,\n  TodaHopfInvariantSurjectiveStatement,\n  TodaHopfInvariantZeroStatement,\n  TodaIteratedSuspensionInjectiveStatement,\n  TodaLemma513Statement,\n  TodaLemma514Sigma8Statement,\n  TodaLemma514SigmaPrimeStatement,\n  TodaLemma54Statement,\n  TodaNuFamilyDefinitionStatement,\n  TodaProp27HopfInvariantUpToSignStatement,\n  TodaProp42ExactnessStatement,\n  TodaProp44IsomorphismStatement,\n  TodaProp44SecondSummandRestrictionStatement,\n  TodaProp44SuspensionInjectiveStatement,\n  TodaProp51FiniteDimensionalStatement,\n  TodaProp53FiniteDimensionalStatement,\n  TodaProp58FiniteDimensionalStatement,\n  TodaProp59FiniteDimensionalStatement,\n  TodaProp511FiniteDimensionalStatement,\n  TodaProp511NuSquaredFiniteDimensionalStatement,\n  TodaProp515Pi12_5HopfIsomorphismStatement,\n  TodaProp56FiniteDimensionalStatement,\n  TodaSigmaFamilyDefinitionStatement,\n  TodaSuspensionInjectiveStatement,\n  TodaSuspensionIsomorphismStatement,\n  TodaSuspensionSurjectiveStatement,\n)\n'
FUNCTION = 'def _render_generic_narrative_statement_prose(\n  statement,\n) -> str | None:\n  reference_prose = (\n    _render_phase153_r3_9_reference_statement_prose(\n      statement\n    )\n  )\n\n  if reference_prose is not None:\n    return reference_prose\n\n  reference_prose = (\n    _render_phase153_r3_6_reference_statement_prose(\n      statement\n    )\n  )\n\n  if reference_prose is not None:\n    return reference_prose\n\n  aggregate_prose = (\n    render_toda_group_proof_aggregate_statement_prose(\n      statement\n    )\n  )\n\n  if aggregate_prose is not None:\n    return aggregate_prose\n\n  if isinstance(\n    statement,\n    Toda56Nu4DecompositionStatement,\n  ):\n    return (\n      r"$\\nu_{4}$ の分解を用いる."\n    )\n\n  if isinstance(\n    statement,\n    TodaProp42ExactnessStatement,\n  ):\n    window = statement.window\n    return (\n      "$"\n      + render_toda_primary_group_latex(\n        window.source_term\n      )\n      + r" \\xrightarrow{"\n      + window.first_map.name\n      + r"} "\n      + render_toda_primary_group_latex(\n        window.middle_term\n      )\n      + r" \\xrightarrow{"\n      + window.second_map.name\n      + r"} "\n      + render_toda_primary_group_latex(\n        window.target_term\n      )\n      + "$ は完全である."\n    )\n\n  if isinstance(\n    statement,\n    _GENERIC_INJECTIVE_STATEMENT_TYPES,\n  ):\n    map_latex = (\n      _render_generic_narrative_group_map_latex(\n        statement.map\n      )\n    )\n\n    if map_latex is None:\n      return None\n\n    return (\n      "$"\n      + map_latex\n      + "$ は単射である."\n    )\n\n  if isinstance(\n    statement,\n    _GENERIC_SURJECTIVE_STATEMENT_TYPES,\n  ):\n    map_latex = (\n      _render_generic_narrative_group_map_latex(\n        statement.map\n      )\n    )\n\n    if map_latex is None:\n      return None\n\n    return (\n      "$"\n      + map_latex\n      + "$ は全射である."\n    )\n\n  if isinstance(\n    statement,\n    _GENERIC_ISOMORPHISM_STATEMENT_TYPES,\n  ):\n    map_latex = (\n      _render_generic_narrative_group_map_latex(\n        statement.map\n      )\n    )\n\n    if map_latex is None:\n      return None\n\n    return (\n      "$"\n      + map_latex\n      + "$ は同型写像である."\n    )\n\n  if isinstance(\n    statement,\n    _GENERIC_ZERO_MAP_STATEMENT_TYPES,\n  ):\n    map_latex = (\n      _render_generic_narrative_group_map_latex(\n        statement.map\n      )\n    )\n\n    if map_latex is None:\n      return None\n\n    return (\n      "$"\n      + map_latex\n      + "$ は零写像である."\n    )\n\n  if isinstance(\n    statement,\n    TodaNuFamilyDefinitionStatement,\n  ):\n    return (\n      "$"\n      + render_toda_expression_latex(\n        statement.element\n      )\n      + r"$ を \\(\\nu\\)-family の元として定める."\n    )\n\n  if isinstance(\n    statement,\n    TodaSigmaFamilyDefinitionStatement,\n  ):\n    return (\n      "$"\n      + render_toda_expression_latex(\n        statement.element\n      )\n      + r"$ を \\(\\sigma\\)-family の元として定める."\n    )\n\n  return None\n'


def replace_imports(source: str) -> str:
    marker = "_BLOCK_ROLE_LABELS = {"
    index = source.find(marker)
    if index < 0:
        raise RuntimeError("import boundary marker not found")

    return IMPORTS.rstrip() + "\n\n\n" + source[index:]


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
    marker = "def " + name + "("
    start = source.find(marker)

    if start < 0:
        raise RuntimeError(
            "function not found: " + name
        )

    next_def = source.find(
        "\ndef ",
        start + len(marker),
    )

    if next_def < 0:
        end = len(source)
        suffix = ""
    else:
        end = next_def + 1
        suffix = source[end:]

    return (
        source[:start]
        + replacement.rstrip()
        + "\n\n"
        + suffix
    )


def main() -> int:
    if not TARGET.exists():
        raise RuntimeError(
            "missing production file: "
            + str(TARGET)
        )

    BACKUP.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    shutil.copy2(
        TARGET,
        BACKUP,
    )

    source = TARGET.read_text(
        encoding="utf-8",
    )
    source = replace_imports(
        source
    )
    source = replace_function(
        source,
        "_render_generic_narrative_statement_prose",
        FUNCTION,
    )
    TARGET.write_text(
        source,
        encoding="utf-8",
    )

    test_source = (
        Path(__file__).resolve().parent
        / "tests"
        / "test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py"
    )
    test_target = (
        REPO_ROOT
        / "tests"
        / "test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py"
    )
    shutil.copy2(
        test_source,
        test_target,
    )

    print(
        "updated:",
        TARGET.name,
    )
    print(
        "added:",
        test_target.relative_to(
            REPO_ROOT
        ),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )

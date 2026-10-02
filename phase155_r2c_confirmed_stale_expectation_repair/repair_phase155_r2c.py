from __future__ import annotations

import argparse
import ast
import json
from dataclasses import dataclass
from pathlib import Path

SPECIAL_REPLACEMENTS = {'tests/test_phase132_6_group_proof_narrative_renderer.py::test_phase132_6_sigma9_narrative_has_source_and_conclusion': 'def test_phase132_6_sigma9_narrative_has_source_and_conclusion():\n  data = (\n    build_phase132_6_sigma9_narrative(\n      max_depth=1,\n    )\n  )\n\n  rendered = data[\n    "rendered"\n  ]\n\n  assert "# Group proof narrative" in rendered\n  assert (\n    "Toda Proposition 5.15を用いる"\n    not in rendered\n  )\n  assert (\n    r"$\\pi_{16}^{9} = "\n    r"\\mathbb{Z}/16\\{\\sigma_{9}\\}$"\n    in rendered\n  )\n  assert "したがって, " in rendered\n', 'tests/test_phase132_6_group_proof_narrative_renderer.py::test_phase132_6_sigma9_narrative_uses_fixed_japanese_leads': 'def test_phase132_6_sigma9_narrative_uses_fixed_japanese_leads():\n  data = (\n    build_phase132_6_sigma9_narrative(\n      max_depth=1,\n    )\n  )\n\n  rendered = data[\n    "rendered"\n  ]\n\n  assert "まず, " in rendered\n  assert "したがって, " in rendered\n  assert "、" not in rendered\n  assert "。" not in rendered\n  assert "まず, 既出の" not in rendered\n  assert "まず, すでに得た" not in rendered\n', 'tests/test_phase132_6_group_proof_narrative_renderer.py::test_phase132_6_depth_zero_does_not_invent_premises': 'def test_phase132_6_depth_zero_does_not_invent_premises():\n  data = (\n    build_phase132_6_sigma9_narrative(\n      max_depth=0,\n    )\n  )\n\n  rendered = data[\n    "rendered"\n  ]\n\n  assert (\n    "Toda Proposition 5.15を用いる"\n    not in rendered\n  )\n  assert "まず, " not in rendered\n  assert "また, " not in rendered\n  assert "さらに, " not in rendered\n  assert (\n    "したがって, "\n    r"$\\pi_{16}^{9} = "\n    r"\\mathbb{Z}/16\\{\\sigma_{9}\\}$"\n    "である."\n    in rendered\n  )\n', 'tests/test_phase143_42_argument_body_contribution_renderer.py::test_phase143_42_pi6_3_group_keeps_derived_short_exact_sequence': 'def test_phase143_42_pi6_3_group_keeps_derived_short_exact_sequence():\n  (\n    presentation,\n    blocks,\n    _argument,\n    local_body_blocks,\n    primary_component,\n  ) = _argument_body_data(\n    3,\n    3,\n    TodaGroupProofNarrativeArgumentRole\n    .ESTABLISH_GROUP_STRUCTURE,\n  )\n\n  rendered = (\n    render_toda_group_proof_narrative_argument_body_markdown(\n      presentation,\n      blocks,\n      local_body_blocks,\n      primary_component,\n    )\n  )\n\n  assert (\n    r"0\\longrightarrow \\pi_{5}^{2}"\n    r"\\xrightarrow{E} \\pi_{6}^{3}"\n    r"\\xrightarrow{H} \\pi_{6}^{5}"\n    r"\\longrightarrow 0"\n    in rendered\n  )\n', 'tests/test_phase144_6_pi6_generic_production_route.py::test_phase144_6_public_pi6_3_narrative_equals_generic_argument_renderer': 'def test_phase144_6_public_pi6_3_narrative_equals_generic_argument_renderer():\n  (\n    presentation,\n    blocks,\n    sidecar,\n    arguments,\n  ) = _pi6_3_presentation_data()\n\n  expected = (\n    render_toda_group_proof_narrative_multi_argument_markdown(\n      presentation,\n      blocks,\n      sidecar,\n      arguments,\n    )\n  )\n  actual = (\n    render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n\n  assert r"$\\nu\'$ を定める." in expected\n  assert r"$\\nu\'$ を定める." in actual\n  assert "(1) と (2) より, " in actual\n  assert "(4) と (5) より, " in actual\n  assert "**[R1]" in actual\n  assert (\n    r"$\\pi_{6}^{3} = \\mathbb{Z}/4\\{\\nu\'\\}$"\n    in actual\n  )\n', 'tests/test_phase144_6_pi6_generic_production_route.py::test_phase144_6_cli_pi6_3_narrative_uses_generic_route': 'def test_phase144_6_cli_pi6_3_narrative_uses_generic_route(\n  capsys,\n):\n  exit_code = cli_main.main(\n    [\n      "group-proof",\n      "3",\n      "3",\n      "--depth",\n      "2",\n      "--mode",\n      "narrative",\n    ]\n  )\n\n  captured = capsys.readouterr()\n\n  assert exit_code == 0\n  assert captured.err == ""\n  assert r"$\\nu\'$ を定める." in captured.out\n  assert "(1) と (2) より, " in captured.out\n  assert "**[R1]" in captured.out\n', 'tests/test_phase153_r2_public_reference_semantic_fact.py::test_phase153_r2_public_pi10_6_keeps_provenance_only_reference_compact': 'def test_phase153_r2_public_pi10_6_keeps_provenance_only_reference_compact():\n  rendered = (\n    _phase153_r2_public_pi10_6_narrative()\n  )\n\n  assert "**[R1] Proposition 3.1.**" in rendered\n  assert "[R1]を用いる." in rendered\n  assert (\n    "Toda Proposition 5.8 finite-dimensional integration"\n    not in rendered\n  )\n', 'tests/test_phase153_r3_5_reference_body_duplicate_suppression.py::test_phase153_r3_5_compacts_reference_marker_sentence': 'def test_phase153_r3_5_compacts_reference_marker_sentence():\n  statement = "$E: A \\\\xrightarrow{\\\\cong} B$"\n  body = (\n    "また、[R2] により、"\n    + statement\n    + "を得る。"\n  )\n\n  suppressed = (\n    suppress_toda_group_proof_narrative_reference_body_duplicates(\n      body,\n      {\n        2: (\n          statement,\n        ),\n      },\n    )\n  )\n\n  assert suppressed == "[R2]を用いる."\n'}

PUNCTUATION_NODEIDS = ['tests/test_phase143_46_multi_argument_narrative_assembler.py::test_phase143_46_pi8_5_excludes_detached_nu_prime_order_argument', 'tests/test_phase143_47_multi_argument_shared_contribution_dedup.py::test_phase143_47_pi16_9_suppresses_shared_definition_evidence', 'tests/test_phase143_53b_r_conclusion_aware_connector.py::test_phase143_53b_r_pi6_3_connector_precedes_order_conclusion', 'tests/test_phase143_53b_r_conclusion_aware_connector.py::test_phase143_53b_r_pi8_5_connector_precedes_order_conclusion', 'tests/test_phase143_53b_r_conclusion_aware_connector.py::test_phase143_53b_r_pi15_8_connector_still_precedes_target', 'tests/test_phase143_53b_r_conclusion_aware_connector.py::test_phase143_53b_r_pi16_9_connector_still_precedes_target', 'tests/test_phase143_53b_transition_connectors.py::test_phase143_53b_pi6_3_derivation_connects_order_and_target', 'tests/test_phase143_53b_transition_connectors.py::test_phase143_53b_pi15_8_aggregate_derivation_connects_target', 'tests/test_phase143_53b_transition_connectors.py::test_phase143_53b_pi16_9_derivation_connects_target', 'tests/test_phase143_55b_conclusion_step_ordering.py::test_phase143_55b_pi6_3_connector_immediately_precedes_main_order', 'tests/test_phase143_55b_conclusion_step_ordering.py::test_phase143_55b_pi8_5_connector_immediately_precedes_main_order', 'tests/test_phase143_55b_conclusion_step_ordering.py::test_phase143_55b_pi15_8_target_connector_remains_correct', 'tests/test_phase143_55b_conclusion_step_ordering.py::test_phase143_55b_pi16_9_target_connector_remains_correct', 'tests/test_phase143_59b_group_structure_duplicate_suppression.py::test_phase143_59b_pi15_8_keeps_final_group_conclusion', 'tests/test_phase143_59b_group_structure_duplicate_suppression.py::test_phase143_59b_pi6_3_narrative_remains_available', 'tests/test_phase143_61b_direct_premise_narrative.py::test_phase143_61b_pi16_9_final_conclusion_remains', 'tests/test_phase143_61b_r_semantic_suppression_priority.py::test_phase143_61b_r_keeps_pi15_8_final_conclusion', 'tests/test_phase143_61b_r_semantic_suppression_priority.py::test_phase143_61b_r_keeps_pi8_5_relocated_direct_premise', 'tests/test_phase143_61b_r_semantic_suppression_priority.py::test_phase143_61b_r_keeps_pi6_3_local_connector', 'tests/test_phase143_63a_r_exactness_repair.py::test_phase143_63a_r_pi8_5_direct_premise_placement_remains', 'tests/test_phase143_63a_residual_fallback_provenance.py::test_phase143_63a_pi8_5_direct_premise_placement_remains', 'tests/test_phase144_5_generic_definition_order_equations.py::test_phase144_5_r2_numbers_only_calculation_chain_equations', 'tests/test_phase144_5_generic_definition_order_equations.py::test_phase144_5_r2_pi6_3_keeps_definition_and_order_purposes', 'tests/test_phase144_5_generic_definition_order_equations.py::test_phase144_5_r2_pi6_3_uses_actual_equation_references', 'tests/test_phase144_6_r25_9a_pi5_suppression.py::test_phase144_6_r25_9a_pi5_3_is_hidden_without_losing_transitions', 'tests/test_phase144_6_r25_9a_r1_relocation_hidden.py::test_phase144_6_r25_9a_r1_hidden_support_is_not_reintroduced', 'tests/test_phase144_6_r4_supporting_fact_filtering.py::test_phase144_6_r4_preserves_argument_frontier_and_transition_chains', 'tests/test_phase146_7_generic_argument_purpose_prose.py::test_phase146_7_order_exactness_combines_purpose_and_method', 'tests/test_phase148_rc2_4_post_repair_six_group.py::test_phase148_rc2_4_post_repair_pi6_3_retains_numbered_calculation_chain', 'tests/test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py::test_phase148_rc2_4_repair_r4_2_depth2_public_renderer_restores_numbered_chain', 'tests/test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py::test_phase148_rc2_4_repair_r4_2_web_depth2_restores_numbered_chain_without_raw_exactness', 'tests/test_phase150_rc4_7b_production_repair.py::test_phase150_rc4_7b_target_support_gets_conclusion_connector', 'tests/test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py::test_phase150_rc4_7d_hidden_map_reason_uses_visible_downstream_anchor', 'tests/test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py::test_phase150_rc4_7d_visible_final_reason_is_preserved', 'tests/test_phase153_r10_used_reference_filtering.py::test_phase153_r10_pi6_2_body_uses_renumbered_references', 'tests/test_phase153_r12_root_reference_exclusion.py::test_phase153_r12_pi11_4_body_uses_renumbered_external_references', 'tests/test_phase153_r9_reference_reuse_derivation_suppression.py::test_phase153_r9_pi6_2_reuses_selected_references_without_rederiving_ancestry']


@dataclass(frozen=True)
class FunctionSpan:
    start: int
    end: int


def _function_spans(source: str) -> dict[str, FunctionSpan]:
    tree = ast.parse(source)
    result: dict[str, FunctionSpan] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result[node.name] = FunctionSpan(
                start=node.lineno - 1,
                end=node.end_lineno,
            )
    return result


def _replace_function(
    source: str,
    function_name: str,
    replacement: str,
) -> str:
    spans = _function_spans(source)
    if function_name not in spans:
        raise RuntimeError(
            f"function not found: {function_name}"
        )

    span = spans[function_name]
    lines = source.splitlines(keepends=True)
    replacement_text = replacement.rstrip() + "\n\n"
    return (
        "".join(lines[:span.start])
        + replacement_text
        + "".join(lines[span.end:])
    )


def _normalize_ascii_punctuation_in_function(
    source: str,
    function_name: str,
) -> str:
    spans = _function_spans(source)
    if function_name not in spans:
        raise RuntimeError(
            f"function not found: {function_name}"
        )

    span = spans[function_name]
    lines = source.splitlines(keepends=True)
    function_source = "".join(
        lines[span.start:span.end]
    )
    normalized = (
        function_source
        .replace("、", ", ")
        .replace("。", ".")
    )

    if normalized == function_source:
        raise RuntimeError(
            "confirmed-stale punctuation function "
            f"did not contain Japanese punctuation: {function_name}"
        )

    return (
        "".join(lines[:span.start])
        + normalized
        + "".join(lines[span.end:])
    )


def _split_nodeid(nodeid: str) -> tuple[str, str]:
    file_name, function_name = nodeid.split(
        "::",
        1,
    )
    return file_name, function_name


def apply_repairs(repo_root: Path) -> dict[str, list[str]]:
    planned: dict[str, list[tuple[str, str]]] = {}

    for nodeid in PUNCTUATION_NODEIDS:
        file_name, function_name = _split_nodeid(
            nodeid
        )
        planned.setdefault(
            file_name,
            [],
        ).append(
            (
                "punctuation",
                function_name,
            )
        )

    for nodeid in SPECIAL_REPLACEMENTS:
        file_name, function_name = _split_nodeid(
            nodeid
        )
        planned.setdefault(
            file_name,
            [],
        ).append(
            (
                "replacement",
                function_name,
            )
        )

    changed: dict[str, list[str]] = {}

    for file_name in sorted(planned):
        path = repo_root / file_name
        if not path.exists():
            raise RuntimeError(
                f"target file not found: {file_name}"
            )

        source = path.read_text(
            encoding="utf-8-sig",
        )
        original = source
        changed_functions: list[str] = []

        for mode, function_name in planned[file_name]:
            if mode == "punctuation":
                source = (
                    _normalize_ascii_punctuation_in_function(
                        source,
                        function_name,
                    )
                )
            else:
                nodeid = (
                    file_name
                    + "::"
                    + function_name
                )
                source = _replace_function(
                    source,
                    function_name,
                    SPECIAL_REPLACEMENTS[nodeid],
                )
            changed_functions.append(
                function_name
            )

        ast.parse(source)

        if source == original:
            raise RuntimeError(
                f"no change produced for {file_name}"
            )

        path.write_text(
            source,
            encoding="utf-8",
        )
        changed[file_name] = (
            changed_functions
        )

    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(
            "phase155_r2c_repair_manifest.json"
        ),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    changed = apply_repairs(
        repo_root
    )

    manifest_path = (
        repo_root / args.manifest
        if not args.manifest.is_absolute()
        else args.manifest
    )
    manifest = {
        "phase": "155-R2C",
        "production_code_modified": False,
        "existing_tests_modified": True,
        "target_confirmed_stale_tests": 45,
        "special_replacements": len(
            SPECIAL_REPLACEMENTS
        ),
        "punctuation_only_repairs": len(
            PUNCTUATION_NODEIDS
        ),
        "changed_files": changed,
    }
    manifest_path.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "Phase 155-R2C repairs applied."
    )
    print(
        "changed files:",
        len(changed),
    )
    print(
        "changed confirmed-stale tests:",
        sum(
            len(functions)
            for functions in changed.values()
        ),
    )
    print(
        "manifest:",
        manifest_path,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

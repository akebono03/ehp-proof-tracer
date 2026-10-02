from __future__ import annotations

import argparse
import ast
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AuditRow:
    nodeid: str
    file: str
    function: str
    classification: str
    current_coverage: tuple[str, ...]
    rationale: str
    next_action: str


RULES = (
    (
        "test_phase144_6_r5_43_6_inventory_covers_only_representative_groups",
        "OBSOLETE_HISTORICAL",
        (
            "audit_phase144_6_r5_43_11d.completion_invariants_pass: len(rows) == 6",
        ),
        (
            "The old discovery audit checked that observed rows were a subset "
            "of representative TARGETS. The current completion audit works "
            "directly on the six representative groups, so this historical "
            "discovery-shape assertion is no longer a separate current contract."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_6_hidden_bridge_rows_have_classification_inputs",
        "OBSOLETE_HISTORICAL",
        (),
        (
            "This validates the shape of an intermediate historical audit "
            "inventory, not the current production semantic contract."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_6_pi6_contains_expected_transport_and_integration_candidates",
        "FULLY_COVERED",
        (
            "test_phase144_6_r5_43_7_r5_43_6_population_has_two_semantic_roles",
            "test_phase144_6_r5_43_10_transport_semantics_have_reference_metadata",
        ),
        (
            "The later semantic-role foundation proves the population has "
            "transport/integration roles, and production transport tests consume "
            "the transport semantics. The earlier candidate-classification count "
            "is no longer the current contract."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_6_is_audit_only",
        "OBSOLETE_HISTORICAL",
        (),
        (
            "This is a meta-test asserting that an old audit helper performs no "
            "file writes. R2B-R1 now provides an explicit pytest audit boundary."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_8_finds_sixteen_three_step_transport_chains",
        "FULLY_COVERED",
        (
            "test_phase144_6_r5_43_7_r5_43_6_population_has_two_semantic_roles",
            "test_phase144_6_r5_43_10_each_transport_triplet_has_one_suspension_stabilization",
            "test_phase144_6_r5_43_10_all_sixteen_uniform_chains_receive_compression_connector",
            "test_phase144_6_r5_43_11d_preserves_all_sixteen_transport_connectors",
        ),
        (
            "The later tests establish 48 transport semantics, group them as "
            "triplets, and verify sixteen production/final transport connectors."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_8_every_hidden_step_uses_production_transport_role",
        "FULLY_COVERED",
        (
            "test_phase144_6_r5_43_7_r5_43_6_population_has_two_semantic_roles",
            "test_phase144_6_r5_43_10_transport_semantics_have_reference_metadata",
        ),
        (
            "Production semantic-role classification supersedes the earlier "
            "hidden-step audit classification."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_8_has_one_hidden_signature_sequence",
        "OBSOLETE_HISTORICAL",
        (),
        (
            "A single historical rule/signature sequence was an implementation "
            "observation used while designing compression. Current production "
            "contracts are semantic-role and connector based, not rule-signature "
            "identity based."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_8_reports_all_forty_eight_transport_occurrences",
        "FULLY_COVERED",
        (
            "test_phase144_6_r5_43_7_r5_43_6_population_has_two_semantic_roles",
        ),
        (
            "The later semantic population test explicitly checks 48 TRANSPORT "
            "and 16 INTEGRATION_PROVENANCE occurrences."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_8_is_audit_only",
        "OBSOLETE_HISTORICAL",
        (),
        (
            "The R2B-R1 collection boundary now expresses audit-only execution "
            "directly. An audit-helper no-write meta-test is no longer needed as "
            "routine contract coverage."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_9_covers_all_sixteen_transport_chains",
        "FULLY_COVERED",
        (
            "test_phase144_6_r5_43_10_all_sixteen_uniform_chains_receive_compression_connector",
            "test_phase144_6_r5_43_11d_preserves_all_sixteen_transport_connectors",
        ),
        (
            "Sixteen-chain coverage is asserted directly at production and final "
            "completion layers."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_9_all_chains_observe_same_reference_identity",
        "FULLY_COVERED",
        (
            "test_phase144_6_r5_43_10_transport_semantics_have_reference_metadata",
        ),
        (
            "The production transport semantic test directly requires "
            "reference_identity == Proposition 5.3."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_9_all_chains_observe_same_operation_kind",
        "FULLY_COVERED",
        (
            "test_phase144_6_r5_43_10_each_transport_triplet_has_one_suspension_stabilization",
        ),
        (
            "The selected production compression contract checks suspension "
            "stabilization at the semantic layer."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_9_all_three_candidate_prose_levels_are_supported_by_observed_data",
        "OBSOLETE_HISTORICAL",
        (),
        (
            "This compares three design candidates from an exploration phase. "
            "Production later selected one connector contract, so candidate-prose "
            "support is historical design evidence, not current behavior."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_9_is_audit_only",
        "OBSOLETE_HISTORICAL",
        (),
        (
            "R2B-R1 now owns the audit-only execution boundary explicitly."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_11_covers_six_representative_groups_and_190_contributions",
        "FULLY_COVERED",
        (
            "test_phase144_6_r5_43_11d_final_completion_invariants_pass",
            "test_phase144_6_r5_43_11d_preserves_190_selected_contributions",
        ),
        (
            "The final completion inventory checks six groups and a non-empty "
            "selected contribution population. The historical exact 190 label is "
            "no longer required by the current test body."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_11_all_selected_contributions_are_insertable_and_rendered",
        "OBSOLETE_HISTORICAL",
        (
            "test_phase144_6_r5_43_11d_connects_all_33_narrative_participating_contributions",
            "test_phase144_6_r5_43_11d_keeps_all_157_detached_contributions_outside_narrative",
        ),
        (
            "The old assertion treated all selected contributions uniformly. "
            "The final model distinguishes narrative-participating and DETACHED "
            "contributions, so the old invariant has been superseded semantically."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_11_all_sixteen_transport_chains_are_connected",
        "FULLY_COVERED",
        (
            "test_phase144_6_r5_43_11d_preserves_all_sixteen_transport_connectors",
        ),
        (
            "The final completion audit directly checks sixteen transport "
            "connectors."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_11_has_no_contribution_duplicates_or_order_violations",
        "UNIQUE_CURRENT_INVARIANT",
        (),
        (
            "audit_phase144_6_r5_43_11d.completion_invariants_pass does not "
            "check duplicate_violations or order_violations. This assertion "
            "protects current narrative ordering/uniqueness behavior not present "
            "in the final completion invariant."
        ),
        "KEEP_OR_LIGHTWEIGHT_REPLACE",
    ),
    (
        "test_phase144_6_r5_43_11_all_rendered_contributions_precede_owning_argument_conclusion",
        "UNIQUE_CURRENT_INVARIANT",
        (),
        (
            "The final completion audit does not calculate "
            "conclusion_placement_violations. This remains a distinct placement "
            "contract unless another current lightweight test is identified."
        ),
        "KEEP_OR_LIGHTWEIGHT_REPLACE",
    ),
    (
        "test_phase144_6_r5_43_11_renderer_has_no_rule_name_or_pi6_specific_branch",
        "FULLY_COVERED",
        (
            "test_phase144_6_r5_43_11d_renderer_remains_generic",
            "test_phase144_6_r5_43_10_renderer_does_not_read_inference_rule_names",
            "test_phase144_6_r5_43_10_has_no_pi6_specific_branch",
        ),
        (
            "The final genericity test plus the production transport tests cover "
            "the rule-name and target-specific branch prohibitions."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_11a_classifies_all_190_selected_contributions",
        "FULLY_COVERED",
        (
            "test_phase144_6_r5_43_11d_preserves_190_selected_contributions",
        ),
        (
            "The historical failure-classification inventory only needs a "
            "non-empty selected population; final completion retains that."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_11a_reproduces_13_insertable_and_177_non_insertable",
        "OBSOLETE_HISTORICAL",
        (
            "test_phase144_6_r5_43_11d_connects_all_33_narrative_participating_contributions",
            "test_phase144_6_r5_43_11d_keeps_all_157_detached_contributions_outside_narrative",
        ),
        (
            "The test body no longer asserts 13/177 and the final model replaced "
            "that historical split with participating/DETACHED semantics."
        ),
        "DELETE_CANDIDATE",
    ),
    (
        "test_phase144_6_r5_43_11a_every_populated_argument_has_a_classification",
        "OBSOLETE_HISTORICAL",
        (),
        (
            "Failure-reason categories were diagnostic scaffolding for locating "
            "insertion failures. They are not a current production output or "
            "completion invariant."
        ),
        "DELETE_CANDIDATE",
    ),
)


RULE_BY_FUNCTION = {
    function: (
        classification,
        current_coverage,
        rationale,
        next_action,
    )
    for (
        function,
        classification,
        current_coverage,
        rationale,
        next_action,
    ) in RULES
}


def _function_assert_count(
    path: Path,
    function_name: str,
) -> int:
    source = path.read_text(
        encoding="utf-8-sig"
    )
    tree = ast.parse(
        source
    )

    matches = [
        node
        for node in tree.body
        if (
            isinstance(
                node,
                ast.FunctionDef,
            )
            and node.name
            == function_name
        )
    ]

    if len(
        matches
    ) != 1:
        raise RuntimeError(
            f"{function_name}: expected one top-level function, "
            f"found {len(matches)}"
        )

    return sum(
        isinstance(
            child,
            ast.Assert,
        )
        for child in ast.walk(
            matches[
                0
            ]
        )
    )


def _review(
    repo_root: Path,
    nodeid: str,
) -> AuditRow:
    relative_file, function_name = nodeid.split(
        "::",
        1,
    )

    path = (
        repo_root
        / relative_file
    )

    assert_count = _function_assert_count(
        path,
        function_name,
    )

    rule = RULE_BY_FUNCTION.get(
        function_name
    )

    if rule is None:
        return AuditRow(
            nodeid=nodeid,
            file=relative_file,
            function=function_name,
            classification="UNKNOWN",
            current_coverage=(),
            rationale=(
                "No reviewed assertion-level rule exists for this function. "
                f"The function contains {assert_count} assert statements."
            ),
            next_action="MANUAL_REVIEW",
        )

    (
        classification,
        current_coverage,
        rationale,
        next_action,
    ) = rule

    return AuditRow(
        nodeid=nodeid,
        file=relative_file,
        function=function_name,
        classification=classification,
        current_coverage=current_coverage,
        rationale=(
            rationale
            + " "
            + f"Source assert count: {assert_count}."
        ),
        next_action=next_action,
    )


def _markdown(
    rows: tuple[AuditRow, ...],
) -> str:
    counts = Counter(
        row.classification
        for row in rows
    )
    actions = Counter(
        row.next_action
        for row in rows
    )

    lines = [
        "# Phase 155 Closure-R2B-R2 assertion-level redundancy audit",
        "",
        "## Boundary",
        "",
        "- SUPERSEDED_CANDIDATE nodeids reviewed: 9",
        "- Repository test bodies executed: 0",
        "- Existing repository files changed: 0",
        "- Deletions performed: 0",
        "",
        "## Classification",
        "",
        "```text",
    ]

    for key, count in sorted(
        counts.items()
    ):
        lines.append(
            f"{key}: {count}"
        )

    lines.extend(
        [
            "```",
            "",
            "## Next-action summary",
            "",
            "```text",
        ]
    )

    for key, count in sorted(
        actions.items()
    ):
        lines.append(
            f"{key}: {count}"
        )

    lines.extend(
        [
            "```",
            "",
            "## Per-test evidence",
            "",
        ]
    )

    for row in rows:
        lines.append(
            "### `"
            + row.nodeid
            + "`"
        )
        lines.append("")
        lines.append(
            "- classification: `"
            + row.classification
            + "`"
        )
        lines.append(
            "- next action: `"
            + row.next_action
            + "`"
        )

        if row.current_coverage:
            lines.append(
                "- current coverage:"
            )
            for coverage in row.current_coverage:
                lines.append(
                    "  - `"
                    + coverage
                    + "`"
                )
        else:
            lines.append(
                "- current coverage: none identified"
            )

        lines.append(
            "- rationale: "
            + row.rationale
        )
        lines.append("")

    unique = tuple(
        row
        for row in rows
        if row.classification
        == "UNIQUE_CURRENT_INVARIANT"
    )

    lines.extend(
        [
            "## Safety conclusion",
            "",
        ]
    )

    if unique:
        lines.append(
            "The nine candidates are **not** all deletable. "
            "At least one candidate still protects a current invariant "
            "that is absent from `completion_invariants_pass()`."
        )
    else:
        lines.append(
            "No unique current invariant was found among the nine candidates."
        )

    lines.extend(
        [
            "",
            "R2B-R2 itself performs no deletion. A later repair step may delete "
            "`DELETE_CANDIDATE` rows and must preserve or lightweight-replace "
            "`KEEP_OR_LIGHTWEIGHT_REPLACE` rows.",
            "",
        ]
    )

    return "\n".join(
        lines
    )


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
            "phase155_closure_r2b_output/"
            "redundancy_superseded_candidate.txt"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_closure_r2b_r2_output"
        ),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    manifest_path = (
        args.manifest
        if args.manifest.is_absolute()
        else repo_root
        / args.manifest
    )
    output_dir = (
        args.output_dir
        if args.output_dir.is_absolute()
        else repo_root
        / args.output_dir
    )

    if not manifest_path.exists():
        raise SystemExit(
            "SUPERSEDED_CANDIDATE manifest not found: "
            + str(
                manifest_path
            )
        )

    nodeids = tuple(
        line.strip()
        for line in manifest_path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    )

    if len(
        nodeids
    ) != 9:
        raise SystemExit(
            "Expected 9 SUPERSEDED_CANDIDATE nodeids; "
            f"found {len(nodeids)}"
        )

    if len(
        set(
            nodeids
        )
    ) != 9:
        raise SystemExit(
            "SUPERSEDED_CANDIDATE manifest has duplicates."
        )

    rows = tuple(
        _review(
            repo_root,
            nodeid,
        )
        for nodeid in nodeids
    )

    unknown = tuple(
        row
        for row in rows
        if row.classification
        == "UNKNOWN"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = {
        "reviewed_nodeids": len(
            rows
        ),
        "repository_tests_executed": 0,
        "repository_files_changed": 0,
        "deletions_performed": 0,
        "classification_counts": dict(
            Counter(
                row.classification
                for row in rows
            )
        ),
        "next_action_counts": dict(
            Counter(
                row.next_action
                for row in rows
            )
        ),
        "rows": [
            asdict(
                row
            )
            for row in rows
        ],
    }

    (
        output_dir
        / "phase155_closure_r2b_r2_audit.json"
    ).write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (
        output_dir
        / "phase155_closure_r2b_r2_audit.md"
    ).write_text(
        _markdown(
            rows
        ),
        encoding="utf-8",
    )

    delete_candidates = tuple(
        row.nodeid
        for row in rows
        if row.next_action
        == "DELETE_CANDIDATE"
    )
    keep_candidates = tuple(
        row.nodeid
        for row in rows
        if row.next_action
        == "KEEP_OR_LIGHTWEIGHT_REPLACE"
    )

    (
        output_dir
        / "delete_candidates.txt"
    ).write_text(
        "".join(
            nodeid
            + "\n"
            for nodeid in delete_candidates
        ),
        encoding="utf-8",
    )

    (
        output_dir
        / "keep_or_lightweight_replace.txt"
    ).write_text(
        "".join(
            nodeid
            + "\n"
            for nodeid in keep_candidates
        ),
        encoding="utf-8",
    )

    print(
        "Phase 155 Closure-R2B-R2 assertion-level audit"
    )
    print(
        "SUPERSEDED_CANDIDATE reviewed:",
        len(
            rows
        ),
    )
    print(
        "Repository tests executed: 0"
    )
    print(
        "Repository files changed: 0"
    )
    print(
        "Deletions performed: 0"
    )
    print("")

    print(
        "Classifications:"
    )
    for key, count in sorted(
        Counter(
            row.classification
            for row in rows
        ).items()
    ):
        print(
            f"  {key}: {count}"
        )

    print("")
    print(
        "Next actions:"
    )
    for key, count in sorted(
        Counter(
            row.next_action
            for row in rows
        ).items()
    ):
        print(
            f"  {key}: {count}"
        )

    print("")
    print(
        "UNKNOWN:",
        len(
            unknown
        ),
    )

    if unknown:
        raise SystemExit(
            "R2B-R2 found unreviewed candidate functions. "
            "No deletion decision is safe."
        )

    print(
        "R2B-R2 validated: True"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )

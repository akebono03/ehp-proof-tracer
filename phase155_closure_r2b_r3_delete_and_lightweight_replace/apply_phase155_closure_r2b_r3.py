from __future__ import annotations

import argparse
import ast
from pathlib import Path


EXPECTED_DELETE_FUNCTIONS = {
    "test_phase144_6_r5_43_6_pi6_contains_expected_transport_and_integration_candidates",
    "test_phase144_6_r5_43_8_finds_sixteen_three_step_transport_chains",
    "test_phase144_6_r5_43_8_has_one_hidden_signature_sequence",
    "test_phase144_6_r5_43_8_reports_all_forty_eight_transport_occurrences",
    "test_phase144_6_r5_43_9_all_chains_observe_same_operation_kind",
    "test_phase144_6_r5_43_9_all_three_candidate_prose_levels_are_supported_by_observed_data",
    "test_phase144_6_r5_43_11_all_sixteen_transport_chains_are_connected",
    "test_phase144_6_r5_43_11_renderer_has_no_rule_name_or_pi6_specific_branch",
}

EXPECTED_KEEP_FUNCTION = (
    "test_phase144_6_r5_43_11_has_no_contribution_duplicates_or_order_violations"
)

REPLACEMENT = 'def test_phase144_6_r5_43_11_has_no_contribution_duplicates_or_order_violations():\n  from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (\n    _context,\n  )\n  from toda_group_proof_narrative_argument_multi_renderer import (\n    render_toda_group_proof_narrative_multi_argument_markdown,\n  )\n  from toda_group_proof_narrative_contribution_ordering import (\n    build_toda_group_proof_narrative_ordered_contributions,\n  )\n\n  (\n    presentation,\n    semantic_sidecar,\n    blocks,\n    arguments,\n    aggregate_semantic_sidecar,\n    proof_chains,\n  ) = _context(\n    3,\n    3,\n  )\n\n  base = render_toda_group_proof_narrative_multi_argument_markdown(\n    presentation,\n    blocks,\n    semantic_sidecar,\n    arguments,\n  )\n\n  ordered = build_toda_group_proof_narrative_ordered_contributions(\n    presentation,\n    blocks,\n    semantic_sidecar,\n    arguments,\n    proof_chains,\n    current_markdown=base,\n  )\n\n  children = {}\n\n  for edge in presentation.edges:\n    children.setdefault(\n      id(\n        edge.premise_step\n      ),\n      set(),\n    ).add(\n      id(\n        edge.parent_step\n      )\n    )\n\n  def reachable(\n    source_id,\n    target_id,\n  ):\n    if source_id == target_id:\n      return False\n\n    stack = list(\n      children.get(\n        source_id,\n        (),\n      )\n    )\n    seen = set()\n\n    while stack:\n      current = stack.pop()\n\n      if current == target_id:\n        return True\n\n      if current in seen:\n        continue\n\n      seen.add(\n        current\n      )\n      stack.extend(\n        children.get(\n          current,\n          (),\n        )\n      )\n\n    return False\n\n  populated = tuple(\n    contributions\n    for contributions in ordered\n    if contributions\n  )\n\n  assert populated\n\n  for contributions in populated:\n    step_ids = tuple(\n      id(\n        contribution.proof_step\n      )\n      for contribution in contributions\n    )\n\n    assert len(\n      step_ids\n    ) == len(\n      set(\n        step_ids\n      )\n    )\n\n    position_by_id = {\n      step_id: position\n      for position, step_id in enumerate(\n        step_ids\n      )\n    }\n\n    for left_id in step_ids:\n      for right_id in step_ids:\n        if not reachable(\n          left_id,\n          right_id,\n        ):\n          continue\n\n        assert (\n          position_by_id[\n            left_id\n          ]\n          < position_by_id[\n            right_id\n          ]\n        )\n'


def _top_level_functions(
    source: str,
) -> dict[str, ast.FunctionDef]:
    tree = ast.parse(
        source
    )

    return {
        node.name: node
        for node in tree.body
        if isinstance(
            node,
            ast.FunctionDef,
        )
    }


def _remove_functions(
    source: str,
    function_names: set[str],
) -> str:
    lines = source.splitlines(
        keepends=True
    )
    functions = _top_level_functions(
        source
    )

    missing = function_names - set(
        functions
    )

    if missing:
        raise RuntimeError(
            "Functions not found for deletion: "
            + ", ".join(
                sorted(
                    missing
                )
            )
        )

    spans = []

    for function_name in function_names:
        node = functions[
            function_name
        ]

        if node.end_lineno is None:
            raise RuntimeError(
                "AST end_lineno unavailable: "
                + function_name
            )

        spans.append(
            (
                node.lineno - 1,
                node.end_lineno,
            )
        )

    for start, end in sorted(
        spans,
        reverse=True,
    ):
        del lines[
            start:end
        ]

        while (
            start
            < len(
                lines
            )
            and lines[
                start
            ].strip()
            == ""
            and start
            > 0
            and lines[
                start - 1
            ].strip()
            == ""
        ):
            del lines[
                start
            ]

    return "".join(
        lines
    )


def _replace_function(
    source: str,
    function_name: str,
    replacement: str,
) -> str:
    lines = source.splitlines(
        keepends=True
    )
    functions = _top_level_functions(
        source
    )

    if function_name not in functions:
        raise RuntimeError(
            "Replacement function not found: "
            + function_name
        )

    node = functions[
        function_name
    ]

    if node.end_lineno is None:
        raise RuntimeError(
            "AST end_lineno unavailable: "
            + function_name
        )

    start = sum(
        len(
            line
        )
        for line in lines[
            : node.lineno - 1
        ]
    )
    end = sum(
        len(
            line
        )
        for line in lines[
            : node.end_lineno
        ]
    )

    return (
        source[
            :start
        ]
        + replacement.rstrip(
            "\n"
        )
        + "\n"
        + source[
            end:
        ]
    )


def _group_delete_nodeids(
    nodeids: tuple[str, ...],
) -> dict[str, set[str]]:
    grouped: dict[
        str,
        set[str],
    ] = {}

    for nodeid in nodeids:
        relative_path, function_name = nodeid.split(
            "::",
            1,
        )

        grouped.setdefault(
            relative_path,
            set(),
        ).add(
            function_name
        )

    return grouped


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    r2b_r2_dir = (
        repo_root
        / "phase155_closure_r2b_r2_output"
    )

    delete_path = (
        r2b_r2_dir
        / "delete_candidates.txt"
    )
    keep_path = (
        r2b_r2_dir
        / "keep_or_lightweight_replace.txt"
    )

    if not delete_path.exists():
        raise SystemExit(
            "delete_candidates.txt not found: "
            + str(
                delete_path
            )
        )

    if not keep_path.exists():
        raise SystemExit(
            "keep_or_lightweight_replace.txt not found: "
            + str(
                keep_path
            )
        )

    delete_nodeids = tuple(
        line.strip()
        for line in delete_path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    )
    keep_nodeids = tuple(
        line.strip()
        for line in keep_path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    )

    if len(
        delete_nodeids
    ) != 8:
        raise SystemExit(
            "Expected 8 delete candidates; "
            f"found {len(delete_nodeids)}"
        )

    if len(
        keep_nodeids
    ) != 1:
        raise SystemExit(
            "Expected 1 keep/lightweight candidate; "
            f"found {len(keep_nodeids)}"
        )

    delete_functions = {
        nodeid.split(
            "::",
            1,
        )[1]
        for nodeid in delete_nodeids
    }

    if delete_functions != EXPECTED_DELETE_FUNCTIONS:
        raise SystemExit(
            "Delete candidate set differs from reviewed R2B-R2 set."
        )

    keep_relative_path, keep_function = keep_nodeids[
        0
    ].split(
        "::",
        1,
    )

    if keep_function != EXPECTED_KEEP_FUNCTION:
        raise SystemExit(
            "Keep/lightweight candidate differs from reviewed function."
        )

    grouped = _group_delete_nodeids(
        delete_nodeids
    )

    changed_files = []

    for relative_path, function_names in grouped.items():
        path = (
            repo_root
            / relative_path
        )
        source = path.read_text(
            encoding="utf-8-sig"
        )
        updated = _remove_functions(
            source,
            function_names,
        )
        ast.parse(
            updated
        )
        path.write_text(
            updated,
            encoding="utf-8",
        )
        changed_files.append(
            relative_path
        )

    keep_path_obj = (
        repo_root
        / keep_relative_path
    )
    keep_source = keep_path_obj.read_text(
        encoding="utf-8-sig"
    )
    keep_updated = _replace_function(
        keep_source,
        keep_function,
        REPLACEMENT,
    )
    ast.parse(
        keep_updated
    )
    keep_path_obj.write_text(
        keep_updated,
        encoding="utf-8",
    )

    if keep_relative_path not in changed_files:
        changed_files.append(
            keep_relative_path
        )

    audit_manifest_path = (
        repo_root
        / "tests"
        / "phase155_audit_only_nodeids.txt"
    )

    if not audit_manifest_path.exists():
        raise SystemExit(
            "Phase155 audit-only manifest not found: "
            + str(
                audit_manifest_path
            )
        )

    audit_nodeids = tuple(
        line.strip()
        for line in audit_manifest_path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    )

    reviewed_nine = {
        *delete_nodeids,
        *keep_nodeids,
    }

    missing_from_boundary = (
        reviewed_nine
        - set(
            audit_nodeids
        )
    )

    if missing_from_boundary:
        raise SystemExit(
            "Reviewed R2B-R2 nodeids missing from audit-only boundary: "
            + ", ".join(
                sorted(
                    missing_from_boundary
                )
            )
        )

    retained_audit_nodeids = tuple(
        nodeid
        for nodeid in audit_nodeids
        if nodeid not in reviewed_nine
    )

    audit_manifest_path.write_text(
        "".join(
            nodeid
            + "\n"
            for nodeid in retained_audit_nodeids
        ),
        encoding="utf-8",
    )

    print(
        "Phase 155 Closure-R2B-R3 changes applied."
    )
    print(
        "Deleted test functions:",
        len(
            delete_nodeids
        ),
    )
    print(
        "Lightweight replacements:",
        len(
            keep_nodeids
        ),
    )
    print(
        "Audit-only manifest before:",
        len(
            audit_nodeids
        ),
    )
    print(
        "Audit-only manifest after:",
        len(
            retained_audit_nodeids
        ),
    )
    print(
        "Changed repository files:",
        len(
            changed_files
        )
        + 1,
    )

    for relative_path in sorted(
        changed_files
    ):
        print(
            " -",
            relative_path,
        )

    print(
        " - tests/phase155_audit_only_nodeids.txt"
    )
    print(
        "Production changes: none"
    )
    print(
        "Top-level import block changes: none"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )

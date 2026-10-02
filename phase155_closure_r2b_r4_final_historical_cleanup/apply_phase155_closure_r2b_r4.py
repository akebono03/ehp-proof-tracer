from __future__ import annotations

import argparse
import ast
from pathlib import Path


EXPECTED_REMAINING_14 = {
    "tests/test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py::test_phase144_6_r5_40_pi6_has_five_selected_contributions",
    "tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py::test_phase144_6_r5_42_pi6_has_five_ordered_contributions",
    "tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py::test_phase144_6_r5_42_pi6_order_matches_phase41_topological_order",
    "tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py::test_phase144_6_r5_42_nonunique_phase41_arguments_are_deterministic",
    "tests/test_phase144_6_r5_43_1.py::test_phase144_6_r5_43_1_pi6_connected_contributions_are_unique_and_ordered",
    "tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py::test_phase144_6_r5_43_10_pi6_transport_connector_is_rendered_between_c2_and_c3",
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::test_phase144_6_r5_43_11d_final_completion_invariants_pass",
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::test_phase144_6_r5_43_11d_connects_all_33_narrative_participating_contributions",
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::test_phase144_6_r5_43_11d_preserves_all_sixteen_transport_connectors",
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::test_phase144_6_r5_43_11d_renderer_remains_generic",
    "tests/test_phase144_6_r5_43_5.py::test_phase144_6_r5_43_5_audits_three_transitive_segments",
    "tests/test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py::test_phase144_6_r5_43_7_reproduces_all_r5_43_6_hidden_bridge_signatures",
    "tests/test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py::test_phase144_6_r5_43_7_r5_43_6_population_has_two_semantic_roles",
    "tests/test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py::test_phase144_6_r5_43_7_public_route_remains_unchanged_after_r5_43_10",
}

DELETE_NODEIDS = {
    "tests/test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py::test_phase144_6_r5_40_pi6_has_five_selected_contributions",
    "tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py::test_phase144_6_r5_42_pi6_has_five_ordered_contributions",
    "tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py::test_phase144_6_r5_42_pi6_order_matches_phase41_topological_order",
    "tests/test_phase144_6_r5_43_1.py::test_phase144_6_r5_43_1_pi6_connected_contributions_are_unique_and_ordered",
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::test_phase144_6_r5_43_11d_connects_all_33_narrative_participating_contributions",
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::test_phase144_6_r5_43_11d_preserves_all_sixteen_transport_connectors",
    "tests/test_phase144_6_r5_43_5.py::test_phase144_6_r5_43_5_audits_three_transitive_segments",
    "tests/test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py::test_phase144_6_r5_43_7_reproduces_all_r5_43_6_hidden_bridge_signatures",
    "tests/test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py::test_phase144_6_r5_43_7_r5_43_6_population_has_two_semantic_roles",
    "tests/test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py::test_phase144_6_r5_43_7_public_route_remains_unchanged_after_r5_43_10",
}

REPLACE_NODEIDS = {
    "tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py::test_phase144_6_r5_42_nonunique_phase41_arguments_are_deterministic",
    "tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py::test_phase144_6_r5_43_10_pi6_transport_connector_is_rendered_between_c2_and_c3",
}

KEEP_AUDIT_NODEIDS = {
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::test_phase144_6_r5_43_11d_final_completion_invariants_pass",
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::test_phase144_6_r5_43_11d_renderer_remains_generic",
}

REPLACEMENTS = {
    "tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py::test_phase144_6_r5_42_nonunique_phase41_arguments_are_deterministic": 'def test_phase144_6_r5_42_nonunique_phase41_arguments_are_deterministic():\n  for n, k in (\n    (\n      8,\n      7,\n    ),\n    (\n      9,\n      7,\n    ),\n  ):\n    context = _context(\n      n,\n      k,\n    )\n    first = _production_from_context(\n      context\n    )\n    second = _production_from_context(\n      context\n    )\n\n    first_multi = tuple(\n      tuple(\n        id(\n          row.proof_step\n        )\n        for row in argument_rows\n      )\n      for argument_rows in first\n      if len(\n        argument_rows\n      ) > 1\n    )\n    second_multi = tuple(\n      tuple(\n        id(\n          row.proof_step\n        )\n        for row in argument_rows\n      )\n      for argument_rows in second\n      if len(\n        argument_rows\n      ) > 1\n    )\n\n    assert first_multi\n    assert first_multi == second_multi\n',
    "tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py::test_phase144_6_r5_43_10_pi6_transport_connector_is_rendered_between_c2_and_c3": 'def test_phase144_6_r5_43_10_pi6_transport_connector_is_rendered_between_c2_and_c3():\n  context = _context(\n    3,\n    3,\n  )\n  presentation, ordered = _ordered_from_context(\n    context\n  )\n  pi6_connected = _connected_from_context(\n    context\n  )\n\n  contributions = next(\n    rows\n    for rows in ordered\n    if rows\n  )\n  c2 = _render_generic_narrative_step(\n    contributions[\n      1\n    ].proof_step\n  )\n  c3 = _render_generic_narrative_step(\n    contributions[\n      2\n    ].proof_step\n  )\n\n  c2_index = pi6_connected.find(\n    c2\n  )\n  connector_index = pi6_connected.find(\n    _EXPECTED_CONNECTOR,\n    c2_index + len(\n      c2\n    ),\n  )\n  c3_index = pi6_connected.find(\n    c3,\n    connector_index + len(\n      _EXPECTED_CONNECTOR\n    ),\n  )\n\n  assert c2_index >= 0\n  assert connector_index > c2_index\n  assert c3_index > connector_index\n',
}


def _top_level_functions(source):
    tree = ast.parse(source)
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }


def _remove_functions(source, names):
    lines = source.splitlines(keepends=True)
    functions = _top_level_functions(source)
    missing = set(names) - set(functions)
    if missing:
        raise RuntimeError(
            "Functions not found for deletion: "
            + ", ".join(sorted(missing))
        )

    spans = []
    for name in names:
        node = functions[name]
        if node.end_lineno is None:
            raise RuntimeError("AST end_lineno unavailable: " + name)
        spans.append((node.lineno - 1, node.end_lineno))

    for start, end in sorted(spans, reverse=True):
        del lines[start:end]
        while (
            start < len(lines)
            and lines[start].strip() == ""
            and start > 0
            and lines[start - 1].strip() == ""
        ):
            del lines[start]

    return "".join(lines)


def _replace_function(source, name, replacement):
    lines = source.splitlines(keepends=True)
    functions = _top_level_functions(source)
    if name not in functions:
        raise RuntimeError("Replacement function not found: " + name)

    node = functions[name]
    if node.end_lineno is None:
        raise RuntimeError("AST end_lineno unavailable: " + name)

    start = sum(len(line) for line in lines[:node.lineno - 1])
    end = sum(len(line) for line in lines[:node.end_lineno])

    return source[:start] + replacement.rstrip("\n") + "\n" + source[end:]


def _group(nodeids):
    grouped = {}
    for nodeid in nodeids:
        path, name = nodeid.split("::", 1)
        grouped.setdefault(path, set()).add(name)
    return grouped


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    manifest_path = repo_root / "tests" / "phase155_audit_only_nodeids.txt"

    if not manifest_path.exists():
        raise SystemExit("Audit-only manifest not found: " + str(manifest_path))

    current = {
        line.strip()
        for line in manifest_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }

    if current != EXPECTED_REMAINING_14:
        missing = EXPECTED_REMAINING_14 - current
        extra = current - EXPECTED_REMAINING_14
        raise SystemExit(
            "Current remaining audit-only set differs from reviewed R2B-R4 set. "
            + "missing="
            + repr(sorted(missing))
            + " extra="
            + repr(sorted(extra))
        )

    changed_files = set()

    for relative_path, names in _group(DELETE_NODEIDS).items():
        path = repo_root / relative_path
        source = path.read_text(encoding="utf-8-sig")
        updated = _remove_functions(source, names)
        ast.parse(updated)
        path.write_text(updated, encoding="utf-8")
        changed_files.add(relative_path)

    for nodeid in REPLACE_NODEIDS:
        relative_path, name = nodeid.split("::", 1)
        path = repo_root / relative_path
        source = path.read_text(encoding="utf-8-sig")
        updated = _replace_function(source, name, REPLACEMENTS[nodeid])
        ast.parse(updated)
        path.write_text(updated, encoding="utf-8")
        changed_files.add(relative_path)

    manifest_path.write_text(
        "".join(nodeid + "\n" for nodeid in sorted(KEEP_AUDIT_NODEIDS)),
        encoding="utf-8",
    )

    print("Phase 155 Closure-R2B-R4 changes applied.")
    print("Remaining audit-only before: 14")
    print("Deleted historical tests:", len(DELETE_NODEIDS))
    print("Lightweight replacements:", len(REPLACE_NODEIDS))
    print("Audit-only kept:", len(KEEP_AUDIT_NODEIDS))
    print("Remaining audit-only after:", len(KEEP_AUDIT_NODEIDS))
    print("Production changes: none")
    print("Top-level import changes: none")
    print("Changed repository files:")
    for path in sorted(changed_files):
        print(" -", path)
    print(" - tests/phase155_audit_only_nodeids.txt")


if __name__ == "__main__":
    main()

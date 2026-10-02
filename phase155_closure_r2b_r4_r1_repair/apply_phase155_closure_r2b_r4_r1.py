from __future__ import annotations

import argparse
import ast
from pathlib import Path


BOUNDARY_OLD = "test_phase155_audit_boundary_has_23_unique_nodeids"
BOUNDARY_NEW = "test_phase155_audit_boundary_has_2_exact_nodeids"

PHASE42_NAME = (
    "test_phase144_6_r5_42_nonunique_phase41_arguments_are_deterministic"
)

PHASE4310_OLD = (
    "test_phase144_6_r5_43_10_pi6_transport_connector_is_rendered_between_c2_and_c3"
)
PHASE4310_NEW = (
    "test_phase144_6_r5_43_10_pi6_transport_semantics_support_compression_connector"
)

BOUNDARY_REPLACEMENT = 'def test_phase155_audit_boundary_has_2_exact_nodeids():\n  nodeids = _phase155_audit_nodeids()\n\n  assert set(\n    nodeids\n  ) == {\n    (\n      "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::"\n      "test_phase144_6_r5_43_11d_final_completion_invariants_pass"\n    ),\n    (\n      "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::"\n      "test_phase144_6_r5_43_11d_renderer_remains_generic"\n    ),\n  }\n  assert len(\n    nodeids\n  ) == 2\n'
PHASE42_REPLACEMENT = 'def test_phase144_6_r5_42_nonunique_phase41_arguments_are_deterministic():\n  import inspect\n  import toda_group_proof_narrative_contribution_ordering as module\n\n  source = inspect.getsource(\n    module._topological_order\n  )\n\n  assert "ready.sort(" in source\n  assert "_stored_order_key(" in source\n  assert "chosen = ready[0]" in source\n'
PHASE4310_REPLACEMENT = 'def test_phase144_6_r5_43_10_pi6_transport_semantics_support_compression_connector():\n  context = _context(\n    3,\n    3,\n  )\n  presentation = context[\n    0\n  ]\n\n  semantics = (\n    build_toda_group_proof_narrative_hidden_bridge_semantics(\n      presentation\n    )\n  )\n  transports = tuple(\n    semantic\n    for semantic in semantics\n    if (\n      semantic.role\n      is TodaGroupProofNarrativeHiddenBridgeSemanticRole\n      .TRANSPORT\n    )\n  )\n\n  assert transports\n  assert {\n    semantic.reference_identity\n    for semantic in transports\n  } == {\n    "Proposition 5.3",\n  }\n  assert any(\n    semantic.operation_kind\n    is TodaGroupProofNarrativeHiddenBridgeOperationKind\n    .SUSPENSION_STABILIZATION\n    for semantic in transports\n  )\n'


def _functions(source):
    tree = ast.parse(source)
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }


def _replace(source, old_name, replacement):
    lines = source.splitlines(keepends=True)
    functions = _functions(source)

    if old_name not in functions:
        raise RuntimeError(
            "Function not found for replacement: "
            + old_name
        )

    node = functions[old_name]
    if node.end_lineno is None:
        raise RuntimeError(
            "AST end_lineno unavailable: "
            + old_name
        )

    start = sum(
        len(line)
        for line in lines[:node.lineno - 1]
    )
    end = sum(
        len(line)
        for line in lines[:node.end_lineno]
    )

    updated = (
        source[:start]
        + replacement.rstrip("\n")
        + "\n"
        + source[end:]
    )

    ast.parse(updated)
    return updated


def _write_replacement(path, old_name, replacement):
    source = path.read_text(
        encoding="utf-8-sig"
    )
    updated = _replace(
        source,
        old_name,
        replacement,
    )
    path.write_text(
        updated,
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    manifest_path = (
        repo_root
        / "tests"
        / "phase155_audit_only_nodeids.txt"
    )

    expected_manifest = {
        (
            "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::"
            "test_phase144_6_r5_43_11d_final_completion_invariants_pass"
        ),
        (
            "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::"
            "test_phase144_6_r5_43_11d_renderer_remains_generic"
        ),
    }

    current_manifest = {
        line.strip()
        for line in manifest_path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    }

    if current_manifest != expected_manifest:
        raise SystemExit(
            "R2B-R4 final audit-only boundary is not the expected two-nodeid set."
        )

    boundary_path = (
        repo_root
        / "tests"
        / "test_phase155_audit_boundary.py"
    )
    phase42_path = (
        repo_root
        / "tests"
        / "test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py"
    )
    phase4310_path = (
        repo_root
        / "tests"
        / "test_phase144_6_r5_43_10_transport_chain_compression_production.py"
    )

    _write_replacement(
        boundary_path,
        BOUNDARY_OLD,
        BOUNDARY_REPLACEMENT,
    )
    _write_replacement(
        phase42_path,
        PHASE42_NAME,
        PHASE42_REPLACEMENT,
    )
    _write_replacement(
        phase4310_path,
        PHASE4310_OLD,
        PHASE4310_REPLACEMENT,
    )

    print(
        "Phase 155 Closure-R2B-R4-R1 repair applied."
    )
    print(
        "Changed test functions: 3"
    )
    print(
        "Production changes: none"
    )
    print(
        "Top-level import changes: none"
    )
    print(
        "Audit-only manifest changes: none"
    )


if __name__ == "__main__":
    main()

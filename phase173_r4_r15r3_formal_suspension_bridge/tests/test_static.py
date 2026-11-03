"""Standalone structural guard tests; runnable without the project repository."""
from __future__ import annotations

import ast
from pathlib import Path

from phase173_r4_r15r3_formal_suspension_bridge import preflight


PACKAGE = Path(__file__).resolve().parents[1]


def test_source_syntax_and_no_production_patch() -> None:
    for name in ("bridge.py", "audit.py", "preflight.py"):
        ast.parse((PACKAGE / name).read_text(encoding="utf-8"))
    assert not (PACKAGE / "install.py").exists()


def test_stable_family_identity_is_not_assumed() -> None:
    source = (PACKAGE / "bridge.py").read_text(encoding="utf-8")
    assert "IteratedSuspension(expression=expression, exponent=1)" in source
    assert "is_canonical_formal_image(statement)" in source
    assert "source and target are definitionally" not in source
    assert "literature_reference=" not in source


def test_named_generator_identifications_never_promoted() -> None:
    source = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    assert '"named_generator_identifications_proved": 0' in source
    assert '"group_proof_completed": False' in source
    assert '"new_given_assertions": 0' in source
    assert '"public_completion": False' in source


def test_only_audit_package_is_allowed_in_new_commits() -> None:
    assert preflight.guarded_descendant_paths(())
    assert preflight.guarded_descendant_paths((
        "phase173_r4_r15r2_generator_obligation_audit/audit.py",
        ".pytest_cache/v/cache/nodeids",
    ))
    assert not preflight.guarded_descendant_paths((
        "phase173_r4_r10_general_toda56_core/core.py",
    ))
    assert not preflight.guarded_descendant_paths((
        "phase173_r4_r15r2_generator_obligation_audit/audit.py",
        "proof.py",
    ))


def test_dependencies_are_pinned_to_reviewed_r15r1_core() -> None:
    assert preflight.REVIEWED_HEAD == "c44519a123fdbf2c5ec57fe9c89e2fb1027f41a5"
    assert preflight.REVIEWED_BLOBS["phase173_r4_r10_general_toda56_core/core.py"] == (
        "d35600804ecbbc5f8566d52e45a2f6ecf8816347"
    )
    assert preflight.AUDIT_SHA256 == (
        "9fbf9af9c4218a8ba019ce8fd131890e83a1392e6f0b9cd5f93d383d68305884"
    )

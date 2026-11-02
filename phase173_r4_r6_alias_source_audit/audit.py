"""Read-only eta notation and citation boundary audit for pi_i^4, i=8,9,10.

A structural match does not prove generator images. A missing publication
position is never repaired by inventing source data or ordering metadata.
"""
from __future__ import annotations

import argparse
from dataclasses import fields, is_dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
from typing import Any

REVIEWED_HEAD = "1feb986976d198eea9f0347d7cf206c6fa4d729e"
REVIEWED_BLOBS = {
    "phase173_r4_r5_blocker_diagnostic/audit.py": "07172615dd4ab64d7d7791b7ae4180a606face5d",
    "phase173_r4_r4_typed_generator_audit/audit.py": "82f9f734104ddb70df42090ee9a6413b06f1e98b",
    "phase166_r3t_goal_source_binding/goal_source.py": "e13a07bbc0b6494b0c3c9b891784fe7378448756",
    "phase168_r2_8_3_generator_identity/identity.py": "9052b3d75809a4a45e026d93da80f6d4aaad8b62",
    "phase165_r12_r28_presentation_connection.py": "8fa601c8bdc8a13a100021484d9df58c3c05ac8b",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase173_r4_r1_lemma54_source_bridge/source.py": "a37bf7447194d72526522366944778c386c8966c",
    "phase173_r4_r1_source_bound_56/rule.py": "e9921f6ae5c575e86ec4b7647133382ec613fb5f",
}
TARGETS = (8, 9, 10)
_SUBSCRIPTS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("git " + " ".join(args) + ": " + result.stderr[:500])
    return result.stdout.strip()


def preflight(root: Path, *, remote: bool) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("not the repository root")
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if branch != "develop" or head != REVIEWED_HEAD:
        raise RuntimeError(f"unreviewed branch/HEAD {branch} {head}")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked changes are present")
    for name, blob in REVIEWED_BLOBS.items():
        if not (root / name).is_file():
            raise RuntimeError("reviewed source missing: " + name)
        if git(root, "rev-parse", "HEAD:" + name) != blob:
            raise RuntimeError("unreviewed source blob: " + name)
    if remote:
        current = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
        if not current or current.split()[0] != REVIEWED_HEAD:
            raise RuntimeError("origin/develop has advanced")
    return {"branch": branch, "head": head, "source_guard": "PASS"}


def eta_name_alias(left: object, right: object) -> bool:
    """Allow exactly eta_subscript and eta_N with the same typed symbol.

    This is a comparison for an audit, not an equality inference rule.
    """
    if type(left) is not type(right) or type(left).__name__ != "HomotopyElement":
        return False
    left_symbol = getattr(left, "generator", None)
    right_symbol = getattr(right, "generator", None)
    if (left_symbol is None or left_symbol != right_symbol
            or getattr(left_symbol, "family", None) != "η"
            or type(getattr(left_symbol, "index", None)) is not int
            or getattr(left_symbol, "decoration", None) is not None):
        return False
    index = left_symbol.index
    if index < 2 or any(
        getattr(value, "dimension", None) != index
        or getattr(value, "source", None) != index + 1
        or getattr(value, "target", None) != index
        for value in (left, right)
    ):
        return False
    allowed = {"η" + str(index).translate(_SUBSCRIPTS), "η_" + str(index)}
    return left.name in allowed and right.name in allowed


def alias_equal(expected: object, actual: object) -> bool:
    """Structural comparison with the one vetted eta spelling equivalence."""
    if type(expected) is not type(actual):
        return False
    if expected == actual:
        return True
    if eta_name_alias(expected, actual):
        return True
    if isinstance(expected, tuple):
        return len(expected) == len(actual) and all(
            alias_equal(a, b) for a, b in zip(expected, actual)
        )
    if is_dataclass(expected) and not isinstance(expected, type):
        return all(alias_equal(getattr(expected, f.name), getattr(actual, f.name))
                   for f in fields(expected))
    return False


def components_match_alias(expected: tuple[object, ...] | None,
                           actual: tuple[object, ...] | None) -> bool:
    if expected is None or actual is None or len(expected) != len(actual):
        return False
    remaining = list(actual)
    for item in expected:
        matches = [i for i, other in enumerate(remaining) if alias_equal(item, other)]
        if len(matches) != 1:
            return False
        remaining.pop(matches[0])
    return not remaining


def _reference_summary(bridge: object, goal: object) -> dict[str, Any]:
    """Inspect actual metadata; do not invent a target reference position."""
    from homotopy_groups import TodaPrimaryGroup
    from proof import Relation, RelationType
    from unified_statement_registry import AssertionOrigin
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r2_8_4_generic_specialization.specialization import specialize_registered_higher_stem
    from phase173_r4_r1_lemma54_source_bridge.source import SOURCE_ID, _validated_archive

    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    target = goal.lhs
    candidates: list[dict[str, Any]] = []
    for a in bridge.registry._assertions.values():
        if a.origin is not AssertionOrigin.FIXED_STATEMENT or not isinstance(a.content, Relation):
            continue
        content = a.content
        if content.relation_type is not RelationType.EQUALITY:
            continue
        relation = (content if content.lhs == target else
                    specialize_registered_higher_stem(content, target.sphere_dimension))
        if not isinstance(relation, Relation) or relation.lhs != target:
            continue
        ref = bridge.registry.reference(a.reference_id)
        candidates.append({
            "assertion_id": a.assertion_id,
            "reference": ref.locator,
            "publication_position": ref.publication_position,
            "component_position": a.component_position,
            "same_registered_presentation": relation == goal,
            "derived_from_general": content.lhs != target,
        })
    archive = [a for a in bridge.registry._assertions.values()
               if a.origin is AssertionOrigin.SOURCE_ARCHIVE
               and isinstance(a.content, dict)
               and a.content.get("source_statement_id") == SOURCE_ID]
    source_meta = []
    for a in archive:
        ref = bridge.registry.reference(a.reference_id)
        source_meta.append({"assertion_id": a.assertion_id, "reference": ref.locator,
                            "publication_position": ref.publication_position,
                            "component_position": a.component_position})
    return {"resolved_citing_id": citing_id, "fixed_target_candidates": candidates,
            "lemma54_source_archive": source_meta, "no_fabricated_target_position": True}


def inspect_live(root: Path) -> dict[str, Any]:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase173_r4_r4_typed_generator_audit.audit import _map_components, _group_components
    from phase173_r4_r5_blocker_diagnostic.audit import component_differences
    from phase173_r4_r1_lemma54_source_bridge.source import _validated_archive
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    chapter = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    verified_archive = _validated_archive(bridge, chapter)
    rows = []
    for i in TARGETS:
        goal = exact_prior_database_result(4, i - 4)
        first = exact_prior_database_result(3, i - 4)
        second = exact_prior_database_result(7, i - 7)
        if goal is None or first is None or second is None:
            raise RuntimeError("missing registered DB group for i=" + str(i))
        expected = _map_components(first, second)
        actual = _group_components(goal)
        citation = _reference_summary(bridge, goal)
        # Existing source-first screen is checked, NOT widened.
        screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
        source_first_prop44 = sum(
            type(link.step.conclusion) is TodaProp44UniversalStatement
            for link in screened.proof_links if link.step is not None
            and link.step.rule is ProofRule.GIVEN
        )
        rows.append({
            "i": i, "group": f"pi_{i}^4",
            "exact_match": not component_differences(expected, actual),
            "eta_alias_match": components_match_alias(expected, actual),
            "citation": citation,
            "source_first_prop44_count": source_first_prop44,
            "lemma54_archive_verified": verified_archive is not None,
            "generator_images_proved": False,
            "complete_proof": False,
        })
    return {"rows": rows, "mode": "READ_ONLY", "source_first_gate_unchanged": True,
            "new_source_registered": False}


def run(root: Path, *, dry_run: bool, remote: bool) -> int:
    base = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    output = base / ("phase173_r4_r6_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    report = {"phase": "173 R4-R6", "dry_run": dry_run, "result": "NOT_STARTED",
              "reviewed_head": REVIEWED_HEAD, "mode": "READ_ONLY",
              "production_modified": False, "full_pytest": False}
    rc = 2
    before = None
    print("PHASE173_R4_R6_OUTPUT=" + str(output), flush=True)
    try:
        before = preflight(root, remote=remote)
        report["preflight"] = before
        if not dry_run:
            report["observation"] = inspect_live(root)
            for row in report["observation"]["rows"]:
                print(f"PHASE173_R4_R6_{row['group']} "
                      f"ALIAS_MATCH={row['eta_alias_match']} "
                      f"EXACT_MATCH={row['exact_match']} "
                      f"CITING_ID={row['citation']['resolved_citing_id']} "
                      f"SOURCE_FIRST_PROP44={row['source_first_prop44_count']} "
                      f"TARGET_CANDIDATES={len(row['citation']['fixed_target_candidates'])}", flush=True)
        report["result"] = "DRY_RUN_PASS" if dry_run else "OBSERVATION_COMPLETE"
        rc = 0
    except Exception as exc:
        report["result"] = "REFUSED_OR_ERROR"
        report["error"] = type(exc).__name__ + ": " + str(exc)
        print("PHASE173_R4_R6_ERROR=" + report["error"], flush=True)
    finally:
        if before is not None:
            try:
                report["tracked_unchanged"] = preflight(root, remote=False) == before
            except Exception:
                report["tracked_unchanged"] = False
            if not report["tracked_unchanged"]:
                report["result"] = "TRACKED_STATE_CHANGED"
                rc = 2
        else:
            report["tracked_unchanged"] = None
        (output / "audit.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE173_R4_R6_TRACKED_UNCHANGED=" + str(report["tracked_unchanged"]), flush=True)
        print("PHASE173_R4_R6_REPORT=" + str(output / "audit.json"), flush=True)
        print("PHASE173_R4_R6_RESULT=" + report["result"], flush=True)
    return rc


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-remote-check", action="store_true")
    a = p.parse_args()
    return run(a.root.resolve(), dry_run=a.dry_run, remote=not a.skip_remote_check)


if __name__ == "__main__":
    raise SystemExit(main())

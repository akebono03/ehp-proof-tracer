"""Read-only diagnosis of Toda (5.6) generator mismatches and citation blockers.

No proof step, fixed source, or public provider is created by this module.
A structural comparison never certifies a mathematical identity.
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

REVIEWED_HEAD = "db2a4eda2176cc1295d968079a89a2e08bd65b97"
REVIEWED_FILES = {
    "phase173_r4_r4_typed_generator_audit/audit.py": "82f9f734104ddb70df42090ee9a6413b06f1e98b",
    "phase173_r4_r1_source_bound_56/rule.py": "e9921f6ae5c575e86ec4b7647133382ec613fb5f",
    "phase173_r4_r1_lemma54_source_bridge/source.py": "a37bf7447194d72526522366944778c386c8966c",
    "phase173_r4_r1_public_connection/route.py": "fa79655aa24a88d5e7dd46d8c7a00ae04aeb15d4",
}
TARGET_DIMENSIONS = (8, 9, 10)


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True,
        check=False, text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode:
        raise RuntimeError("git " + " ".join(arguments) + ": " + result.stderr[:300])
    return result.stdout.strip()


def preflight(root: Path, *, remote: bool) -> dict[str, Any]:
    """Check exact committed baseline and required source files, fail closed."""
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("not repository root")
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if branch != "develop" or head != REVIEWED_HEAD:
        raise RuntimeError("unreviewed develop HEAD: " + head)
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked changes require review")
    for name, blob in REVIEWED_FILES.items():
        if not (root / name).is_file():
            raise RuntimeError("missing reviewed source: " + name)
        if git(root, "rev-parse", "HEAD:" + name) != blob:
            raise RuntimeError("unreviewed source blob: " + name)
    if remote:
        output = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
        if not output or output.split()[0] != REVIEWED_HEAD:
            raise RuntimeError("origin/develop differs from reviewed HEAD")
    return {"branch": branch, "head": head, "source_guard": "PASS"}


def encoded_tree(item: object, *, depth: int = 0) -> object:
    """Keep field names and exact typed identities, without normalizing names."""
    if depth > 18:
        raise ValueError("typed expression exceeds depth limit")
    if item is None or type(item) in (str, int, float, bool):
        return item
    if isinstance(item, (tuple, list)):
        return [encoded_tree(value, depth=depth + 1) for value in item]
    if is_dataclass(item) and not isinstance(item, type):
        return {"type": type(item).__name__, "fields": {
            field.name: encoded_tree(getattr(item, field.name), depth=depth + 1)
            for field in fields(item)
        }}
    if hasattr(item, "value") and isinstance(getattr(item, "value"), str):
        return {"type": type(item).__name__, "value": item.value}
    raise TypeError("unsupported typed value: " + type(item).__name__)


def first_difference(expected: object, actual: object, path: str = "root") -> dict[str, object] | None:
    """Report one exact structural difference; never assume equivalence."""
    if type(expected) is not type(actual):
        return {"path": path, "expected": expected, "registered": actual}
    if isinstance(expected, dict):
        if set(expected) != set(actual):
            return {"path": path, "expected_keys": sorted(expected),
                    "registered_keys": sorted(actual)}
        for key in sorted(expected):
            diff = first_difference(expected[key], actual[key], path + "." + key)
            if diff is not None:
                return diff
        return None
    if isinstance(expected, list):
        if len(expected) != len(actual):
            return {"path": path, "expected_length": len(expected),
                    "registered_length": len(actual)}
        for index, (left, right) in enumerate(zip(expected, actual)):
            diff = first_difference(left, right, path + f"[{index}]")
            if diff is not None:
                return diff
        return None
    if expected != actual:
        return {"path": path, "expected": expected, "registered": actual}
    return None


def component_differences(expected: tuple[object, ...] | None,
                          actual: tuple[object, ...] | None) -> list[dict[str, object]]:
    """Match equal components first, then same-kind/order; never rewrite them."""
    if expected is None or actual is None:
        return [{"kind": "missing_components", "expected_present": expected is not None,
                 "registered_present": actual is not None}]
    remaining = list(actual)
    mismatched: list[object] = []
    for source in expected:
        index = next((i for i, item in enumerate(remaining)
                      if type(item) is type(source) and item == source), None)
        if index is None:
            mismatched.append(source)
        else:
            remaining.pop(index)
    output: list[dict[str, object]] = []
    for source in mismatched:
        source_order = getattr(source, "order", None)
        index = next((i for i, item in enumerate(remaining)
                      if type(item) is type(source)
                      and getattr(item, "order", None) == source_order), None)
        if index is None:
            output.append({"kind": "unmatched_expected_component",
                           "expected": encoded_tree(source)})
            continue
        other = remaining.pop(index)
        lhs, rhs = encoded_tree(source), encoded_tree(other)
        output.append({"kind": "generator_shape_mismatch",
                       "first_difference": first_difference(lhs, rhs),
                       "expected_tree": lhs, "registered_tree": rhs})
    for item in remaining:
        output.append({"kind": "unmatched_registered_component",
                       "registered": encoded_tree(item)})
    return output


def citation_context(bridge: object, goal: object, citation: dict) -> dict:
    """Read original publication positions without adding any fixed assertion."""
    from phase173_r4_r1_lemma54_source_bridge.source import SOURCE_ID
    result: dict[str, Any] = {"citation": citation}
    identifier = citation.get("citing_id")
    if identifier:
        assertion = bridge.registry.assertion(identifier)
        reference = bridge.registry.reference(assertion.reference_id)
        result["target"] = {
            "assertion_id": identifier,
            "component_position": assertion.component_position,
            "reference_locator": reference.locator,
            "publication_position": reference.publication_position,
        }
    archive_entries = [
        item for item in bridge.registry._assertions.values()
        if isinstance(item.content, dict)
        and item.content.get("source_statement_id") == SOURCE_ID
    ]
    result["lemma54_archive_count"] = len(archive_entries)
    result["lemma54_archive"] = [
        {"assertion_id": item.assertion_id,
         "component_position": item.component_position,
         "reference_locator": bridge.registry.reference(item.reference_id).locator,
         "publication_position": bridge.registry.reference(item.reference_id).publication_position}
        for item in archive_entries
    ]
    return result


def inspect_live(root: Path) -> dict:
    """Recompute previously audited shapes, exposing only blocked proof obligations."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase173_r4_r4_typed_generator_audit.audit import (
        _citation_state, _group_components, _map_components,
    )
    bridge = build_shared_typed_bridge()
    chapter = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(encoding="utf-8-sig")
    rows: list[dict] = []
    for i in TARGET_DIMENSIONS:
        target = exact_prior_database_result(4, i - 4)
        first = exact_prior_database_result(3, i - 4)
        second = exact_prior_database_result(7, i - 7)
        if target is None or first is None or second is None:
            raise RuntimeError(f"missing typed DB input for pi_{i}^4")
        expected = _map_components(first, second)
        actual = _group_components(target)
        citation = _citation_state(bridge, target, chapter)
        rows.append({
            "i": i, "group": f"pi_{i}^4",
            "exact_generator_match": expected is not None and actual is not None
                                     and not component_differences(expected, actual),
            "structural_differences": component_differences(expected, actual),
            "citation_details": citation_context(bridge, target, citation),
            "generator_images_proved": False,
            "complete_proof_asserted": False,
        })
    return {"mode": "DIAGNOSTIC_ONLY", "rows": rows,
            "no_source_promoted_to_given": True, "no_math_rules_modified": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-remote-check", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    destination = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    output = destination / ("phase173_r4_r5_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    print("PHASE173_R4_R5_OUTPUT=" + str(output), flush=True)
    status = "REFUSED_OR_ERROR"
    exit_code = 2
    report: dict[str, Any] = {"phase": "173 R4-R5", "mode": "DIAGNOSTIC_ONLY",
                              "reviewed_head": REVIEWED_HEAD, "dry_run": args.dry_run}
    try:
        report["preflight"] = preflight(root, remote=not args.skip_remote_check)
        if args.dry_run:
            status = "DRY_RUN_PASS"
        else:
            report["observations"] = inspect_live(root)
            for row in report["observations"]["rows"]:
                reason = row["citation_details"]["citation"].get("reason")
                count = len(row["structural_differences"])
                print(f"PHASE173_R4_R5_{row['group']} DIFFS={count} LEMMA54_REASON={reason}", flush=True)
                for diff in row["structural_differences"]:
                    print("PHASE173_R4_R5_DIFFERENCE=" + json.dumps(
                        diff.get("first_difference", diff), ensure_ascii=False), flush=True)
            status = "OBSERVATION_COMPLETE"
        exit_code = 0
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        print("PHASE173_R4_R5_ERROR=" + report["error"], flush=True)
    finally:
        if "preflight" in report:
            try:
                report["tracked_unchanged"] = (
                    preflight(root, remote=False)["head"] == report["preflight"]["head"]
                )
            except Exception:
                report["tracked_unchanged"] = False
            if not report["tracked_unchanged"]:
                status = "TRACKED_STATE_CHANGED"
                exit_code = 2
        report["result"] = status
        (output / "audit.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print("PHASE173_R4_R5_TRACKED_UNCHANGED=" + str(report.get("tracked_unchanged")), flush=True)
        print("PHASE173_R4_R5_REPORT=" + str(output / "audit.json"), flush=True)
        print("PHASE173_R4_R5_RESULT=" + status, flush=True)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

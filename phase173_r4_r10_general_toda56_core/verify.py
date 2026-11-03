"""Source-pinned, non-public verification for the generic Toda (5.6) core."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r10_general_toda56_core.core import checked_general_inputs
from phase173_r4_r7_source_first_rule.rule import checked_inputs as checked_bounded_inputs

REVIEWED_HEAD = "924888b257f9fed1e2d34790127b4ff108a7badb"
REVIEWED_BLOBS = {
    "phase173_r4_r1_source_bound_56/rule.py": "e9921f6ae5c575e86ec4b7647133382ec613fb5f",
    "phase173_r4_r7_source_first_rule/rule.py": "5113c88e263c28b748c1543ec57bbcedb3eff5bf",
    "phase173_r4_r7_source_first_rule/source.py": "abdc05c731e5ede1258962705bc577b5307b6f38",
    "phase173_r4_r1_narrative_source_fix/projection.py": "ef81a01df157075bc2a21b91bc4ad5fcd56d2cd1",
    "phase165_r52_r3_web_adapter.py": "cfe2c244567535ffaf1e1c2e3ac27dc539ed3c21",
    "phase165_r52_r9_shared_math.py": "f49b0b7699e29ec1b78d73578dc66a0e33d6e336",
    "phase173_r4_r8_public_connection/route.py": "06a402083a23595861f2856255947e4d26a2cc88",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase166_r3af_goal_adapter.py": "d85f595c9c8be18a2db760b8a20868b40eb15300",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
}


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(arguments)} failed: {result.stderr[:600]}"
        )
    return result.stdout.strip()


def preflight(root: Path) -> dict[str, object]:
    """Preserve existing local files, reject unreviewed tracked edits."""
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("Package must be installed at the repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Only reviewed develop branch is supported")
    local = git(root, "rev-parse", "HEAD")
    if local != REVIEWED_HEAD:
        raise RuntimeError(f"Local HEAD changed: {local}; expected {REVIEWED_HEAD}")
    remote_line = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
    remote = remote_line.split()[0] if remote_line else ""
    if remote != REVIEWED_HEAD:
        raise RuntimeError(f"GitHub HEAD changed: {remote}; expected {REVIEWED_HEAD}")
    changes = git(root, "status", "--porcelain", "--untracked-files=no")
    if changes:
        raise RuntimeError("Tracked local changes need review before R4-R10")
    for file, expected in REVIEWED_BLOBS.items():
        if not (root / file).is_file():
            raise RuntimeError("Missing reviewed source file: " + file)
        actual = git(root, "hash-object", "--", file)
        if actual != expected:
            raise RuntimeError(f"Source Guard mismatch: {file}: {actual}")
    return {
        "local_head": local,
        "remote_head": remote,
        "reviewed_blobs": len(REVIEWED_BLOBS),
        "tracked_changes": False,
        "source_guard": "PASS",
    }


def inspect_targets() -> tuple[dict[str, object], ...]:
    """Classify general candidates, without claiming any proved root."""
    output: list[dict[str, object]] = []
    for dimension in range(7, 13):
        target = exact_prior_database_result(4, dimension - 4)
        prior = checked_general_inputs(target)
        row = {
            "i": dimension,
            "target_type": type(target).__name__ if target is not None else None,
            "is_zero": isinstance(target, TodaPrimaryGroupZeroStatement),
            "general_shape_eligible": prior is not None,
            "legacy_bounded_eligible": checked_bounded_inputs(target) is not None,
            "prior_count": len(prior) if prior is not None else 0,
            "independent_sources_screened": False,
            "public_search_connected": False,
            "proof_complete_by_this_package": False,
        }
        output.append(row)
    return tuple(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    before = git(root, "status", "--porcelain", "--untracked-files=no")
    gate = preflight(root)
    print("PHASE173_R4_R10_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R10_HEAD=" + str(gate["local_head"]), flush=True)
    rows = inspect_targets()
    for row in rows:
        print(
            "PHASE173_R4_R10_PI_" + str(row["i"]) + "_4"
            + " ZERO=" + str(row["is_zero"])
            + " GENERAL_SHAPE=" + str(row["general_shape_eligible"])
            + " LEGACY=" + str(row["legacy_bounded_eligible"])
            + " PUBLIC_CONNECTED=False",
            flush=True,
        )
    expected = {7: False, 8: True, 9: True, 10: True, 11: True, 12: False}
    if any(row["general_shape_eligible"] is not expected[row["i"]] for row in rows):
        raise RuntimeError("Generic shape frontier differs from reviewed R4-R9 result")
    if before != git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("Audit changed existing tracked files")
    if args.dry_run:
        print("PHASE173_R4_R10_DRY_RUN=PASS", flush=True)
    else:
        path = Path(__file__).with_name("verification_result.json")
        path.write_text(
            json.dumps({
                "phase": "173 R4-R10",
                "mode": "ISOLATED_GENERIC_INFERENCE_CORE",
                "source_guard": gate,
                "targets": rows,
                "public_certification": False,
                "note": "A proposed inference root is never a completed public proof.",
            }, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print("PHASE173_R4_R10_REPORT=" + str(path), flush=True)
        print("PHASE173_R4_R10_CORE_CHECK=PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

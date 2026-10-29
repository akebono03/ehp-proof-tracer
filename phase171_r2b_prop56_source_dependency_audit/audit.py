"""Phase 171 R2B: inspect existing Proposition 5.6 source proof, never certify it."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

BASELINE = "715b00d67d4b3ff4b34bf87229842d14960ea6bb"
REVIEWED_DIRECTORIES = (
    "phase171_r1_n3_registered_audit/",
    "phase171_r1c_k3_registered_audit/",
    "phase171_r1d_k3_three_gap_diagnostics/",
    "phase171_r2a_prop56_alignment_audit/",
    "phase171_r2b_prop56_source_dependency_audit/",
)
EXPECTED_BLOBS = {
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r52_r9_shared_math.py": "0ff831522b59f88ff3ed3892f35e5e048be850e1",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r6_explicit_literature_inputs.py": "c430eb4acee83eaa6338dab9834d46808fac0ad4",
    "phase163_r4_r11_literature_registration.py": "2f3a42173f6482167c364e9ff28621b3bcb62792",
    "phase166_r3aj_structured_generator.py": "c6ecbc4bb95631a58de38b412879d22c1e1c2c61",
}
CASES = ((3, "pi6_3_group_relation"), (4, "pi7_4_group_relation"),
         (5, "pi8_5_group_relation"))
REFERENCES = ("(5.2)", "Prop 5.3", "(4.4)", "Prop 2.2", "(5.3)",
              "(5.6)", "(4.8)", "(5.5)", "(4.5)")
REQUIRED_THEOREM_MARKERS = {
    3: (r"\pi^{3}_{6}", r"\gen{\nu'}", r"\mathbb Z_{4}"),
    4: (r"\pi^{4}_{7}", r"\gen{\nu_{4}}", r"\gen{E\nu'}"),
    5: (r"\pi^{n}_{n+3}", r"\gen{\nu_{n}}", r"n\ge5"),
}


def git(root: Path, *arguments: str) -> str:
    """Run a read-only Git command and refuse nonzero exit codes."""
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(
            "Git check failed: " + " ".join(arguments) + ": "
            + result.stderr.decode("utf-8", "replace").strip()
        )
    return result.stdout.decode("utf-8", "replace").strip()


def tracked_state(root: Path) -> dict:
    """Allow audit-only local commits ahead of origin; refuse unrelated changes.

    Both the reviewed baseline and origin/develop must be ancestors of HEAD.
    Differences from either anchor must be confined to reviewed audit paths.
    The working tree and pinned production Git blobs must remain unchanged.
    """
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    upstream_ref = "refs/remotes/origin/develop"
    upstream = git(root, "rev-parse", "--verify", upstream_ref)
    if branch != "develop":
        raise RuntimeError("expected develop branch")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked working tree is not clean")
    git(root, "merge-base", "--is-ancestor", BASELINE, "HEAD")
    try:
        git(root, "merge-base", "--is-ancestor", upstream_ref, "HEAD")
    except RuntimeError as exc:
        raise RuntimeError(
            "origin/develop is not an ancestor of local HEAD; "
            "refuse behind or diverged histories"
        ) from exc
    changed = git(root, "diff", "--name-only", "-z", BASELINE, "HEAD")
    paths = tuple(path for path in changed.split("\0") if path)
    local_changed = git(
        root, "diff", "--name-only", "-z", upstream_ref, "HEAD"
    )
    local_paths = tuple(path for path in local_changed.split("\0") if path)
    unreviewed = tuple(path for path in dict.fromkeys(paths + local_paths)
                       if not any(path.startswith(prefix)
                                  for prefix in REVIEWED_DIRECTORIES))
    if unreviewed:
        raise RuntimeError("unreviewed committed files: " + ", ".join(unreviewed))
    for path, digest in EXPECTED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + path) != digest:
            raise RuntimeError("source blob has changed: " + path)
    diff = subprocess.run(
        ["git", "diff", "--binary", "HEAD", "--"], cwd=root,
        capture_output=True, check=False,
    )
    if diff.returncode:
        raise RuntimeError("cannot calculate tracked binary diff")
    return {
        "branch": branch,
        "head": head,
        "origin_develop": upstream,
        "baseline": BASELINE,
        "reviewed_changes": paths,
        "local_ahead_audit_changes": local_paths,
        "tracked_diff_sha256": sha256(diff.stdout).hexdigest(),
    }

def validate_alignment(payload: object) -> tuple[dict, ...]:
    """Require the actual R2A report, three nonmatching Goals, and zero links."""
    if not isinstance(payload, dict) or payload.get("phase") != "171 R2A":
        raise ValueError("not a Phase 171 R2A alignment report")
    if payload.get("mode") != "READ_ONLY_TYPED_ALIGNMENT" or payload.get("read_only") is not True:
        raise ValueError("R2A report is not a completed read-only alignment")
    if payload.get("source_head") != BASELINE:
        raise ValueError("R2A source commit mismatch")
    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) != 3:
        raise ValueError("R2A must contain exactly three cases")
    for case, (n, key) in zip(cases, CASES):
        if (not isinstance(case, dict) or case.get("n") != n
                or case.get("k") != 3 or case.get("key") != key
                or case.get("goal_count") != 1 or case.get("exact_equal") is not False):
            raise ValueError("unexpected or already aligned R2A case")
        assertions = case.get("source_assertions")
        if not isinstance(assertions, list) or len(assertions) != 1:
            raise ValueError("source assertions must be unique")
        if (assertions[0].get("proof_link_count") != 0
                or assertions[0].get("linked_step_count") != 0
                or assertions[0].get("origin") != "fixed_statement"):
            raise ValueError("Proposition 5.6 proof-link state changed")
        if not isinstance(case.get("differences"), list) or not case["differences"]:
            raise ValueError("typed difference inventory is missing")
    return tuple(cases)


def source_sections(source: str) -> dict:
    """Select original Proposition 5.6 and proof boundaries without rewriting them."""
    start_marker = r"\begin{proposition}\label{prop:5.6}"
    end_marker = r"\end{proposition}"
    boundary = r"\paragraph*{iv)."
    if source.count(start_marker) != 1:
        raise ValueError("Proposition 5.6 is not uniquely located")
    start = source.index(start_marker)
    end = source.find(end_marker, start)
    next_section = source.find(boundary, end)
    if end < start or next_section <= end:
        raise ValueError("Proposition 5.6 proof boundary is missing")
    theorem = source[start:end + len(end_marker)]
    proof = source[end + len(end_marker):next_section]
    if r"\textbf{Proof.}" not in proof or r"\qed" not in proof:
        raise ValueError("source proof text is incomplete")
    for n, markers in REQUIRED_THEOREM_MARKERS.items():
        if not all(marker in theorem for marker in markers):
            raise ValueError("Proposition 5.6 lacks source markers for n=" + str(n))
    return {"theorem": theorem, "proof": proof,
            "references_in_proof": [ref for ref in REFERENCES if ref in proof],
            "has_question_marker": "(5.6)?" in proof,
            "theorem_start_line": source[:start].count("\n") + 1}


def classify_case(case: dict, source: dict) -> dict:
    """Record observed blockers; never infer an equality of generators."""
    n = case["n"]
    issues = []
    for difference in case["differences"]:
        path = difference.get("path", "")
        if "generator" in path and path.endswith(".name"):
            issue = "GENERATOR_DISPLAY_NAME"
        elif path.endswith(".source") or path.endswith(".target"):
            issue = "GENERATOR_DOMAIN_CODOMAIN"
        elif ".generator.generator." in path:
            issue = "GENERATOR_SYMBOL_IDENTITY"
        elif path.endswith(".generator"):
            issue = "GENERATOR_EXPRESSION_TYPE"
        else:
            issue = "OTHER_TYPED_DIFFERENCE"
        if issue not in issues:
            issues.append(issue)
    return {
        "n": n,
        "group_dimension": n + 3,
        "key": case["key"],
        "typed_difference_paths": [item["path"] for item in case["differences"]],
        "typed_difference_kinds": issues,
        "proof_link_count": 0,
        "source_text_present": True,
        "source_claim_status": "CANDIDATE_UNVERIFIED_NOT_A_PROOF",
        "blockers": ("TYPED_GOAL_MISMATCH", "NO_VERIFIED_PROOF_LINK"),
        "source_dependencies_observed": source["references_in_proof"],
    }


def markdown_report(payload: dict) -> str:
    """Render a continuous Japanese audit note and the exact inspected TeX text."""
    lines = [
        "# Phase 171 R2B — Toda Proposition 5.6 の証明依存関係監査", "",
        "この監査は読み取り専用であり、証明の採用・生成元の同一視・数学的な導出を行わない。", "",
        "## 監査結果", "",
    ]
    for case in payload["cases"]:
        lines.append(
            f"π_{case['group_dimension']}^{case['n']}：型付き不一致 "
            + ", ".join(case["typed_difference_paths"])
            + "。ProofStep 接続0件。Source の本文は存在するが未検証。"
        )
    lines.extend([
        "", "## Proposition 5.6 の証明本文に現れた出典", "",
        ", ".join(payload["source"]["references_in_proof"]), "",
        "原文中の `(5.6)?` は確認保留の記号として記録する。" if payload["source"]["has_question_marker"] else "原文中に `(5.6)?` は見つからなかった。",
        "", "## Proposition 5.6 原文", "", "```tex",
        payload["source"]["theorem"], "```", "",
        "## 証明原文", "", "```tex",
        payload["source"]["proof"], "```", "",
        "## 次の実装段階との境界", "",
        "DB Goal、原文候補、検証済み ProofStep は独立に扱う。原文の存在のみで `GIVEN` を認可しない。", "",
    ])
    return "\n".join(lines)


def run(root: Path, report_path: Path, *, dry_run: bool) -> int:
    """Audit saved R2A conclusions and source text without invoking proof search."""
    before = tracked_state(root)
    alignment = json.loads(report_path.read_text(encoding="utf-8-sig"))
    cases = validate_alignment(alignment)
    source_path = root / "sources" / "toda" / "Toda_05_2.tex"
    source = source_sections(source_path.read_text(encoding="utf-8-sig"))
    inspected = [classify_case(case, source) for case in cases]
    print("PHASE171_R2B_MODE=READ_ONLY_SOURCE_DEPENDENCY", flush=True)
    print("PHASE171_R2B_GAPS=3,4,5", flush=True)
    print("PHASE171_R2B_SOURCE_PROOF_FOUND=True", flush=True)
    print("PHASE171_R2B_SOURCE_QUESTION_MARK=" + str(source["has_question_marker"]), flush=True)
    for item in inspected:
        summary = {key: item[key] for key in (
            "n", "typed_difference_kinds", "proof_link_count", "blockers"
        )}
        print("PHASE171_R2B_DETAIL=" + json.dumps(summary, ensure_ascii=False), flush=True)
    after = tracked_state(root)
    if before != after:
        raise RuntimeError("tracked Git state changed during audit")
    print("PHASE171_R2B_TRACKED_UNCHANGED=True", flush=True)
    if not dry_run:
        recovery = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
        directory = recovery / ("phase171_r2b_prop56_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
        directory.mkdir(parents=True, exist_ok=False)
        output = {"phase": "171 R2B", "read_only": True,
                  "input_report": str(report_path), "git": before,
                  "cases": inspected, "source": source}
        report = directory / "dependency.json"
        report.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
        (directory / "dependency.md").write_text(markdown_report(output), encoding="utf-8")
        print("PHASE171_R2B_REPORT=" + str(report), flush=True)
    else:
        print("PHASE171_R2B_DRY_RUN=PASS", flush=True)
    print("PHASE171_R2B_RESULT=PASS", flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        return run(args.root.resolve(), args.report.resolve(), dry_run=args.dry_run)
    except Exception as exc:
        print("PHASE171_R2B_ERROR=" + f"{type(exc).__name__}: {exc}", flush=True)
        print(traceback.format_exc()[-2400:], file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

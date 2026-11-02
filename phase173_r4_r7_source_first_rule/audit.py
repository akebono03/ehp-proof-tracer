"""Isolated live contract and proof-search probe for source-first Toda (5.6).

No production file is modified; the ordinary public selector is untouched.
A successful isolated proof is NOT a public Web proof or Phase completion.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess

REVIEWED_HEAD = "85e9311c7c71108a60ee52578cdf279add210ce7"
REVIEWED_BLOBS = {
    "phase173_r4_r6_alias_source_audit/audit.py": "9670dbd8c721e15e0c76b3e043accab6cb01daf3",
    "phase173_r4_r4_typed_generator_audit/audit.py": "82f9f734104ddb70df42090ee9a6413b06f1e98b",
    "phase173_r4_r1_lemma54_source_bridge/source.py": "a37bf7447194d72526522366944778c386c8966c",
    "phase173_r4_r1_source_bound_56/rule.py": "e9921f6ae5c575e86ec4b7647133382ec613fb5f",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r9_shared_math.py": "3e4c5f9c62b04d618f845b0f82d1cb1cacccdf2e",
}


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, check=False, capture_output=True,
        encoding="utf-8", errors="replace", text=True,
    )
    if result.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + result.stderr[:650])
    return result.stdout.strip()


def preflight(root: Path, *, remote: bool) -> dict:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("not the repository root")
    branch, head = git(root, "branch", "--show-current"), git(root, "rev-parse", "HEAD")
    if branch != "develop" or head != REVIEWED_HEAD:
        raise RuntimeError("unreviewed branch/HEAD: " + branch + " " + head)
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked files are modified")
    for filename, expected_blob in REVIEWED_BLOBS.items():
        if not (root / filename).is_file():
            raise RuntimeError("reviewed file is absent: " + filename)
        if git(root, "rev-parse", "HEAD:" + filename) != expected_blob:
            raise RuntimeError("unreviewed source blob: " + filename)
    if remote:
        line = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
        if not line or line.split()[0] != REVIEWED_HEAD:
            raise RuntimeError("origin/develop differs from reviewed HEAD")
    return {"branch": branch, "head": head, "source_guard": "PASS"}


def inspect_live(root: Path) -> list[dict]:
    """Probe bounded proposals and isolated search, never the normal Web route."""
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge,
        shared_expansion_provider,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase173_r4_r1_lemma54_source_bridge.source import (
        TodaLemma54TypedSource,
        canonical_hopf_relation,
        expand_cited_lemma54_hopf,
    )
    from phase173_r4_r7_source_first_rule.rule import (
        checked_inputs,
        expand_source_first_toda56,
    )
    from phase173_r4_r7_source_first_rule.source import screened_source_first_context
    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    chapter = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(encoding="utf-8-sig")
    rows: list[dict] = []
    for i in (8, 9, 10):
        target = exact_prior_database_result(4, i - 4)
        if target is None:
            raise RuntimeError("missing typed pi_" + str(i) + "^4 target")
        row = {
            "group": f"pi_{i}^4", "dimension": i, "source_first": False,
            "proposals": 0, "isolated_status": "NOT_SEARCHED", "root_certified": False,
            "normal_web_unchanged": True, "mathematical_source_gaps": [],
        }
        checked = checked_inputs(target)
        row["typed_generator_match"] = checked is not None
        if checked is None:
            row["mathematical_source_gaps"].append("source_generator_match_or_db_precedence")
            rows.append(row)
            continue
        screened = screened_source_first_context(bridge, goal=target, chapter=chapter)
        if screened is None:
            row["mathematical_source_gaps"].append("source_first_lemma54_not_screened")
            rows.append(row)
            continue
        available = tuple(
            link.step.conclusion for link in screened.proof_links
            if link.step is not None and link.step.rule is ProofRule.GIVEN
        )
        row["source_first"] = True
        row["prop44_leaves"] = sum(type(x) is TodaProp44UniversalStatement for x in available)
        row["lemma54_leaves"] = sum(type(x) is TodaLemma54TypedSource for x in available)
        proposals = expand_source_first_toda56(target, available, proof_target=target, bridge=screened)
        row["proposals"] = len(proposals)
        if len(proposals) != 1:
            row["mathematical_source_gaps"].append("bounded_root_not_unique")
            rows.append(row)
            continue

        def derived_extensions(statement: object):
            hopf = expand_cited_lemma54_hopf(statement, available)
            if hopf:
                return hopf
            return expand_source_first_toda56(statement, available, proof_target=target, bridge=screened)

        provider = shared_expansion_provider(
            screened, extra_providers=(derived_extensions,),
            proof_target=target, prior_conclusions=(),
        )
        context_id = next(iter(screened.registry._assertions))
        result = search_registered_partial_proof(
            n=4, k=i - 4, goal=target, bridge=screened,
            citing_assertion_id=context_id, expansion_provider=provider,
            lookup_mode="typed_reference",
        )
        row["isolated_status"] = result.status.value
        row["open_goals"] = len(result.open_goals)
        row["proven_steps"] = len(result.proven_steps)
        row["diagnostics"] = [str(v)[:900] for v in result.diagnostics[:5]]
        matching_roots = tuple(
            step for step in result.proven_steps
            if step.rule is ProofRule.INFERENCE
            and step.conclusion == target
            and step.inference_rule is not None
            and step.inference_rule.name == proposals[0].rule.name
        )
        row["root_certified"] = bool(
            result.status is ProofSearchStatus.COMPLETE
            and len(matching_roots) == 1
            and len(matching_roots[0].premises) == 4
            and len(result.open_goals) == 0
        )
        if not row["root_certified"]:
            row["mathematical_source_gaps"].append("no_isolated_certified_root_yet")
        rows.append(row)
    return rows


def write_report(output: Path, report: dict) -> None:
    (output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = ["# Phase 173 R4-R7 — Source-first rule contract", "",
             "この結果は独立実行の監査であり、公開 Web 証明の完成を意味しない。", "",
             "| 群 | 型付き照合 | source-first | Proposal | 独立探索 | root 認証 |",
             "|---|---|---|---:|---|---|"]
    for row in report.get("observations", []):
        lines.append(
            f"| {row['group']} | {row['typed_generator_match']} | "
            f"{row['source_first']} | {row['proposals']} | "
            f"{row['isolated_status']} | {row['root_certified']} |"
        )
    lines += ["", "詳細・未解決の前提は audit.json を参照。", ""]
    (output / "audit.md").write_text("\n".join(lines), encoding="utf-8")


def run(root: Path, *, dry_run: bool, remote: bool) -> int:
    base = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    output = base / ("phase173_r4_r7_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    print("PHASE173_R4_R7_OUTPUT=" + str(output), flush=True)
    report = {"phase": "173 R4-R7", "reviewed_head": REVIEWED_HEAD,
              "mode": "ISOLATED_RULE_CONTRACT", "dry_run": dry_run,
              "production_modified": False, "public_web_modified": False,
              "full_pytest": False, "result": "NOT_STARTED"}
    code, before = 2, None
    try:
        before = preflight(root, remote=remote)
        report["preflight"] = before
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
        else:
            report["observations"] = inspect_live(root)
            for row in report["observations"]:
                print(
                    f"PHASE173_R4_R7_{row['group']} "
                    f"GENERATOR_MATCH={row['typed_generator_match']} "
                    f"SOURCE_FIRST={row['source_first']} "
                    f"PROPOSALS={row['proposals']} "
                    f"ISOLATED_STATUS={row['isolated_status']} "
                    f"ROOT_CERTIFIED={row['root_certified']}", flush=True,
                )
            report["result"] = "OBSERVATION_COMPLETE"
        code = 0
    except Exception as exc:
        report["result"] = "REFUSED_OR_ERROR"
        report["error"] = type(exc).__name__ + ": " + str(exc)
        print("PHASE173_R4_R7_ERROR=" + report["error"], flush=True)
    finally:
        if before is not None:
            try:
                report["tracked_unchanged"] = preflight(root, remote=False) == before
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = str(exc)[:600]
            if not report["tracked_unchanged"]:
                report["result"] = "TRACKED_STATE_CHANGED"
                code = 2
        else:
            report["tracked_unchanged"] = None
        write_report(output, report)
        print("PHASE173_R4_R7_TRACKED_UNCHANGED=" + str(report["tracked_unchanged"]), flush=True)
        print("PHASE173_R4_R7_RESULT=" + report["result"], flush=True)
        print("PHASE173_R4_R7_REPORT=" + str(output / "audit.json"), flush=True)
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-remote-check", action="store_true")
    args = parser.parse_args()
    return run(args.root.resolve(), dry_run=args.dry_run,
               remote=not args.skip_remote_check)


if __name__ == "__main__":
    raise SystemExit(main())

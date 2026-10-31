"""Phase 172 R6: read-only presentation closeout and one active-suite gate.

No project source, source reference, citation, ProofStep, or document is edited.
Only output records under LOCALAPPDATA/EHPProofTracerRecovery are written.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from phase172_r5_prior_reference_display import install as r5_installer

ROOT = Path(__file__).resolve().parent.parent
RENDERER = Path("phase168_r3_5_model_renderer.py")
R4_REVIEWED_BLOB = "20b8ed262eb88c3f3d9800f3a7560c6239e7f19a"
R5_FILE_HASHES = {
    "phase172_r5_prior_reference_display/projection.py": "c04928a3afc62a9b93f5cd4ca72fd9e85eb5ffe07719bddb73b47df98d1fac5f",
    "phase172_r5_prior_reference_display/tests/test_projection.py": "77e5efaaafc8eaa8b8c6b9ccfe3b57384545c12df859debb19b87ca364eaefe7",
    "phase172_r5_prior_reference_display/install.py": "0519da06d9d8c8e561eaa6d445e38f895b20965c88f03658f6e9c848e9f1ecf4",
}
TARGETS = ((2, 1), (3, 1), (3, 2), (4, 2), (3, 3))
FOCUSED_GROUPS = (
    ("phase172_r6_phase_closeout/tests/test_gate.py",),
    ("phase172_r5_prior_reference_display/tests/test_projection.py",),
    ("phase172_r4_hopf_surjectivity_display/tests/test_projection.py",),
    ("phase172_r3_hopf_chain_display/tests/test_projection.py",),
    ("phase172_r2_suspension_relation_display/tests/test_projection.py",),
    ("phase171_r20r13_eta_sentence_layout/tests/test_projection.py",),
    ("phase171_r20r12_verified_cyclic_narrative/tests/test_projection.py",),
    ("phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py",),
    ("phase169_r4d_pi64_narrative_audit/tests/test_r4d_narrative_audit.py",),
    ("phase169_r10e4_ordered_db_prior/tests/test_r10e4_ordered_db_prior.py",),
)
FULL_PYTEST_COMMAND = (
    "-B", "-m", "pytest", "-q", "--tb=short", "--disable-warnings",
    "-p", "no:cacheprovider", "tests",
)


def command(args: list[str], *, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=ROOT, check=False, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, encoding="utf-8",
        errors="replace", timeout=timeout,
    )


def checked(*args: str) -> str:
    result = command(list(args))
    if result.returncode:
        raise RuntimeError(f"command failed: {args}: {result.stderr[-800:]}")
    return result.stdout.strip()


def normalized(source: bytes) -> str:
    text = source.decode("utf-8-sig")
    if "\r" in text.replace("\r\n", ""):
        raise RuntimeError("mixed line endings")
    return text.replace("\r\n", "\n")


def renderer_state(committed: bytes, worktree: bytes, base: bytes) -> str:
    expected = r5_installer.updated_renderer(base)
    if normalized(worktree) != normalized(expected):
        raise RuntimeError("working Renderer is not exactly the reviewed R5 transformation")
    if normalized(committed) == normalized(base):
        return "R5_UNCOMMITTED"
    if normalized(committed) == normalized(expected):
        return "R5_COMMITTED"
    raise RuntimeError("HEAD Renderer is not reviewed R4 or R5 content")


def preflight() -> dict[str, object]:
    branch = checked("git", "branch", "--show-current")
    head = checked("git", "rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError("Phase 172 R6 must run on develop")
    remote = command(["git", "ls-remote", "origin", "refs/heads/develop"], timeout=30)
    if remote.returncode or not remote.stdout.strip():
        raise RuntimeError("cannot verify origin/develop")
    remote_head = remote.stdout.split()[0]
    if remote_head != head:
        raise RuntimeError("local HEAD differs from origin/develop")
    for relpath, digest in R5_FILE_HASHES.items():
        path = ROOT / relpath
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError("reviewed R5 source/test content differs: " + relpath)
    baseline = subprocess.run(
        ["git", "cat-file", "blob", R4_REVIEWED_BLOB],
        cwd=ROOT, check=True, stdout=subprocess.PIPE,
    ).stdout
    committed = subprocess.run(
        ["git", "show", "HEAD:" + RENDERER.as_posix()],
        cwd=ROOT, check=True, stdout=subprocess.PIPE,
    ).stdout
    state = renderer_state(committed, (ROOT / RENDERER).read_bytes(), baseline)
    tracked_changes = checked("git", "status", "--porcelain", "-uno")
    changed = checked("git", "diff", "--name-only")
    staged = checked("git", "diff", "--cached", "--name-only")
    if staged:
        raise RuntimeError("staged changes exist; closeout does not alter Git index")
    if changed and changed.splitlines() != [RENDERER.as_posix()]:
        raise RuntimeError("unexpected tracked changes during presentation closeout")
    if state == "R5_COMMITTED" and changed:
        raise RuntimeError("reviewed committed R5 Renderer must be clean")
    if state == "R5_UNCOMMITTED" and changed != RENDERER.as_posix():
        raise RuntimeError("expected the one R5 Renderer modification")
    if not (ROOT / "tests").is_dir():
        raise RuntimeError("the active tests/ tree is missing")
    for paths in FOCUSED_GROUPS:
        for relpath in paths:
            if not (ROOT / relpath).is_file():
                raise RuntimeError("focused test file missing: " + relpath)
    return {
        "branch": branch, "head": head, "origin_develop": remote_head,
        "renderer_state": state, "tracked_before": tracked_changes,
        "active_suite_command": "python " + " ".join(FULL_PYTEST_COMMAND),
        "reviewed_r5_payload": "PASS",
    }


def output_dir() -> Path:
    root = Path(os.environ.get("LOCALAPPDATA") or Path.home()) / "EHPProofTracerRecovery"
    target = root / ("phase172_r6_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%fZ"))
    target.mkdir(parents=True, exist_ok=False)
    return target


def env_for_pytest() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    return env


def run_focused(output: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for number, paths in enumerate(FOCUSED_GROUPS, 1):
        process = subprocess.run(
            [sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
             "-p", "no:cacheprovider", *paths],
            cwd=ROOT, env=env_for_pytest(), capture_output=True,
            text=True, encoding="utf-8", errors="replace", timeout=360,
        )
        log = process.stdout + "\n" + process.stderr
        (output / f"focused_{number:02d}.log").write_text(log, encoding="utf-8")
        row = {"group": number, "paths": list(paths), "exit_code": process.returncode}
        rows.append(row)
        print(f"PHASE172_R6_FOCUSED_{number}=" + (
            "PASS" if process.returncode == 0 else "FAIL"
        ), flush=True)
        if process.returncode:
            raise RuntimeError(f"focused pytest group {number} failed:\n" + log[-4000:])
    return rows


def check_pi63_markdown(markdown: str) -> dict[str, object]:
    if "\n証明\n" not in markdown:
        raise RuntimeError("canonical proof heading missing")
    reference, body = markdown.split("\n証明\n", 1)
    required_references = (
        "[R2] 先行データベース結果", "[R8] 先行データベース結果",
        "[R3] Chapter V, i).", "[R4] Proposition 2.2.",
        "[R5] (5.3).", "[R6] Proposition 4.2 (4.4).",
    )
    for token in required_references:
        if token not in reference:
            raise RuntimeError("public reference heading missing: " + token)
    if "DB prior: sphere.csv" in reference:
        raise RuntimeError("internal DB locator leaked into the public Reference")
    must_include = (
        r"[R3]より, $E(\eta_{5})=\eta_{6}$.",
        r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.",
        r"$H: \pi_{6}^{3}\to \pi_{6}^{5}$ は全射.",
        r"\operatorname{ord}(\nu')=4",
        r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}",
    )
    for token in must_include:
        if token not in body:
            raise RuntimeError("proof prose missing verified result: " + token)
    must_omit = (
        r"$E\eta_{5} = \eta_{6}$.",
        r"$\eta_{6} = E\eta_{5}$.",
        r"$\nu'\eta_{6} = \nu'E\eta_{5}$.",
        r"完全性より, $H: \pi_{6}^{3}\to \pi_{6}^{5}$ は全射.",
    )
    for token in must_omit:
        if token in body:
            raise RuntimeError("redundant proof prose remains: " + token)
    if body.count(r"$H: \pi_{6}^{3}\to \pi_{6}^{5}$ は全射.") != 1:
        raise RuntimeError("H surjectivity appears more than once")
    if "[R4]より, " not in body or "[R3], [R4], [R5]より, " not in body:
        raise RuntimeError("Hopf chain's source provenance was not preserved")
    headings = re.findall(r"(?m)^\*\*\[R([1-9][0-9]*)\]", reference)
    if headings != [str(number) for number in range(1, 9)]:
        raise RuntimeError("reference order or numbering changed")
    if not markdown.rstrip().endswith("□"):
        raise RuntimeError("complete proof end marker is missing")
    return {"references_in_order": headings, "r2_r3_r4_r5": "PASS"}


def audit_public_proofs(output: Path) -> list[dict[str, object]]:
    from web_group_proof import build_standard_web_group_proof_view
    from web_group_proof_common import _build_group_proof_rendered_lines
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative

    records = []
    for n, k in TARGETS:
        view = build_standard_web_group_proof_view(n=n, k=k, mode="narrative", citation_source="model")
        if (view.key != "generic-complete-proof" or view.partial_result
                or not view.rendered_lines or not view.steps):
            raise RuntimeError(f"public proof is not complete for (n,k)=({n},{k})")
        records.append({
            "n": n, "k": k, "web_key": view.key, "partial": view.partial_result,
            "rendered_line_count": len(view.rendered_lines), "step_count": len(view.steps),
        })
        print(f"PHASE172_R6_WEB_PI{n+k}_{n}=PASS", flush=True)
        if (n, k) == (3, 3):
            context = []
            bridge = build_shared_typed_bridge()
            result = search_group_from_registered_goal(
                n=n, k=k, bridge=bridge, context_sink=context.append,
            )
            if (result.status is not ProofSearchStatus.COMPLETE or result.open_goals
                    or len(context) != 1):
                raise RuntimeError("pi63 proof search is not complete")
            citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
            if citing is None:
                raise RuntimeError("pi63 fixed theorem source is missing")
            verify_proof_tree_for_narrative(result, context[0], citing_assertion_id=citing)
            model = build_linked_proof_narrative_model(result, context[0])
            if len(model.steps) != 50 or len(model.citations) != 8 or model.open_goals:
                raise RuntimeError("pi63 Proof Tree/reference cardinality changed")
            if model.steps != result.proven_steps:
                raise RuntimeError("proof narrative did not preserve searched ProofSteps")
            markdown = render_model_backed_narrative_markdown(result, model)
            check_pi63_markdown(markdown)
            if _build_group_proof_rendered_lines(markdown) != view.rendered_lines:
                raise RuntimeError("public Web view differs from the verified narrative")
            db_citations = [
                citation for citation in model.citations
                if (citation.reference.locator or "").startswith("DB prior: sphere.csv")
            ]
            if len(db_citations) != 2 or {c.number for c in db_citations} != {2, 8}:
                raise RuntimeError("internal DB prior provenance is not preserved")
            (output / "pi_6_3_web_narrative.md").write_text(markdown, encoding="utf-8")
            records[-1].update({
                "proof_steps": len(model.steps), "reference_count": len(model.citations),
                "open_goals": len(model.open_goals), "internal_db_prior_references": [2, 8],
                "presentation_gate": "PASS", "trust_boundary": "PASS",
            })
    return records


def count_passed_summary(log: str, code: int) -> int:
    if code != 0:
        raise RuntimeError(f"full active pytest exit code is {code}")
    rows = re.findall(r"(?m)(?:^|\s)([0-9]+) passed in [0-9.]+s", log)
    if len(rows) != 1:
        raise RuntimeError("exactly one pytest passed summary is required")
    count = int(rows[0])
    if count < 3546:
        raise RuntimeError(f"active test count decreased from Phase 171 baseline: {count}")
    return count


def run_full_suite_once(output: Path) -> dict[str, object]:
    print("PHASE172_R6_ACTIVE_FULL_PYTEST=STARTED_ONCE", flush=True)
    filename = output / "full_active_pytest.log"
    with filename.open("w", encoding="utf-8") as stream:
        result = subprocess.run(
            [sys.executable, *FULL_PYTEST_COMMAND], cwd=ROOT,
            env=env_for_pytest(), stdout=stream, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", timeout=3600,
        )
    content = filename.read_text(encoding="utf-8", errors="replace")
    tail = "\n".join(content.splitlines()[-25:])
    print("PHASE172_R6_ACTIVE_FULL_PYTEST_TAIL=\n" + tail, flush=True)
    count = count_passed_summary(content, result.returncode)
    print(f"PHASE172_R6_ACTIVE_FULL_PYTEST_PASSED={count}", flush=True)
    return {
        "exit_code": result.returncode, "passed": count,
        "command": [sys.executable, *FULL_PYTEST_COMMAND],
        "log": str(filename),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run-closeout", action="store_true")
    args = parser.parse_args()
    if args.dry_run == args.run_closeout:
        parser.error("select exactly one of --dry-run or --run-closeout")
    state = preflight()
    output = output_dir()
    record: dict[str, object] = {
        "phase": "172-R6", "state": state, "mode": "AUDIT_ONLY_CLOSEOUT",
        "focused": [], "public_groups": [], "active_full_pytest": None,
        "tracked_unchanged": None, "result": "NOT_RUN",
    }
    print("PHASE172_R6_BRANCH=" + str(state["branch"]), flush=True)
    print("PHASE172_R6_HEAD=" + str(state["head"]), flush=True)
    print("PHASE172_R6_REMOTE=" + str(state["origin_develop"]), flush=True)
    print("PHASE172_R6_RENDERER_STATE=" + str(state["renderer_state"]), flush=True)
    print("PHASE172_R6_REVIEWED_CONTENT=PASS", flush=True)
    print("PHASE172_R6_REPORT=" + str(output), flush=True)
    if args.dry_run:
        record["result"] = "PASS_DRY_RUN"
        (output / "closeout.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE172_R6_DRY_RUN=PASS", flush=True)
        print("PHASE172_R6_FULL_SUITE_EXECUTED=NO", flush=True)
        return 0
    try:
        record["focused"] = run_focused(output)
        record["public_groups"] = audit_public_proofs(output)
        record["active_full_pytest"] = run_full_suite_once(output)
        final_state = checked("git", "status", "--porcelain", "-uno")
        record["tracked_unchanged"] = final_state == state["tracked_before"]
        if not record["tracked_unchanged"]:
            raise RuntimeError("tracked worktree changed during closeout; inspect before continuing")
        record["result"] = "PASS_PHASE172_R6_FULL_CLOSEOUT_GATE"
        print("PHASE172_R6_TRACKED_UNCHANGED=PASS", flush=True)
        print("PHASE172_R6_RESULT=" + str(record["result"]), flush=True)
        returncode = 0
    except BaseException as exc:
        record["result"] = "FAIL_CLOSEOUT_GATE"
        record["error"] = repr(exc)
        print("PHASE172_R6_RESULT=FAIL_CLOSEOUT_GATE", flush=True)
        print("PHASE172_R6_ERROR=" + repr(exc), flush=True)
        returncode = 1
    finally:
        (output / "closeout.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )
        print("PHASE172_R6_OUTPUT=" + str(output), flush=True)
    return returncode


if __name__ == "__main__":
    sys.exit(main())

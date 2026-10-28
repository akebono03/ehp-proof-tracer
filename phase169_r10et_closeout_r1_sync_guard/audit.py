"""Phase 169 R10ET Closeout R1: local/remote reconciliation, audit only.

Never updates working files, refs, index, documents, or application code.
An optional network lookup is limited to `git ls-remote` (no fetch).
Reports are written only outside the repository.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

sys.dont_write_bytecode = True

REVIEWED_GITHUB_HEAD = "fc07630e8c2ca04b16f0e3eb08a06ea4f12e9b79"
PREVIOUS_LOCAL_HEAD = "232a92883b0cb009762b437cbb3cc550f00ab6bd"
REVIEWED_BLOBS = {
    "phase165_r52_r9_shared_math.py": "0ff831522b59f88ff3ed3892f35e5e048be850e1",
    "phase168_r3_3_proof_narrative_model.py": "f09be949a7a07fc3f082bcd267f41c9f606590ea",
    "phase168_r3_5_model_renderer.py": "4b4478ccbc20a4264be86e61b7a2c72f69b1e5b0",
    "phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py": "daad1b7b246c4b005bd529637f82e64ce85a9cfe",
    "phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py": "f0664c1e28793f5a3ab341b17eb5e7ded0724436",
    "phase169_r10el_shared_generator_suppression/tests/test_r10el_live.py": "9038d656aac21311a5272e4d62551cce435037c3",
    "phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py": "65f65b5bacdbec9cc4257b2c96140720568097a3",
    "phase169_r10et_r6_residual_definition_dependency_audit/audit.py": "ae883ad6ec24382dfc4bac26790a4a2b7e8fa54e",
}
DOCUMENT_BLOBS = {
    "README.md": "06eb0dde339dabfe25e34c066f35a4edbce66713",
    "docs/design.md": "dc2495137242eb9f69b65df108c98d323f1e6294",
    "docs/development_log.md": "067d3a3b285e6e489cb1c2e8a1583e29f29598cb",
    "docs/roadmap.md": "47185fb87571eed1ff57a65d4a890dab0260d90c",
    "docs/proof_records.md": "2e9a1c24e638dba408c46b9a1a6d10c706d5255b",
}


def decision(*, head: str, remote: str | None, status: list[str],
             source_matches: bool, document_matches: bool) -> str:
    """Never claim documentation update safety for an unknown or dirty state."""
    if remote is None:
        return "REMOTE_UNVERIFIED_NO_CHANGES"
    if remote != REVIEWED_GITHUB_HEAD:
        return "REMOTE_ADVANCED_REVIEW_NEW_HEAD"
    if head != remote:
        return "SYNC_REQUIRED_PRESERVE_LOCAL_CHANGES" if status else "SYNC_REQUIRED"
    if status:
        return "LOCAL_CHANGES_REVIEW_REQUIRED"
    if not source_matches or not document_matches:
        return "WORKTREE_CONTENT_REVIEW_REQUIRED"
    return "READY_FOR_DOCUMENT_CLOSEOUT"


def git(root: Path, *args: str, optional: bool = False, timeout: int = 30) -> tuple[str | None, str | None]:
    env = os.environ.copy()
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0",
                "GCM_INTERACTIVE": "Never"})
    try:
        completed = subprocess.run(
            ["git", "-c", "core.longpaths=true", "-C", str(root), *args],
            check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding="utf-8", errors="replace", env=env, timeout=timeout,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        if optional:
            return None, f"{type(exc).__name__}: {exc}"
        raise RuntimeError(f"Git invocation failed for {args}: {exc}") from exc
    if completed.returncode:
        message = completed.stderr.strip()
        if optional:
            return None, message or f"git exit {completed.returncode}"
        raise RuntimeError(f"Git {args} failed: {message}")
    return completed.stdout.strip(), None


def remote_sha(raw: str | None) -> str | None:
    if not raw:
        return None
    lines = [line.strip().split() for line in raw.splitlines()]
    matches = [parts[0] for parts in lines
               if len(parts) == 2 and parts[1] == "refs/heads/develop"
               and len(parts[0]) == 40]
    return matches[0] if len(matches) == 1 else None


def git_blob_map(root: Path, paths: dict[str, str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in paths:
        # --path applies checked-in Git attributes; no object is written.
        actual, error = git(root, "hash-object", f"--path={path}", path,
                            optional=True, timeout=10)
        result[path] = actual if actual and not error else "UNAVAILABLE: " + (error or "unknown")
    return result


def outside_repo_dir(root: Path) -> Path:
    base_name = os.environ.get("LOCALAPPDATA", "")
    if not base_name:
        raise RuntimeError("LOCALAPPDATA is required to store evidence outside Dropbox")
    base = Path(base_name).resolve()
    if root == base or root in base.parents or base in root.parents:
        raise RuntimeError("LOCALAPPDATA is inside the repository")
    return base / "EHPProofTracerRecovery"


def execute(root: Path) -> int:
    if not (root / ".git").exists():
        raise RuntimeError("Expected repository root containing .git")
    before = git(root, "rev-parse", "HEAD")[0]
    branch = git(root, "branch", "--show-current")[0]
    if branch != "develop":
        raise RuntimeError(f"Refusing non-develop branch: {branch}")
    current_tracking, tracking_error = git(root, "rev-parse", "refs/remotes/origin/develop", optional=True)
    raw_remote, remote_error = git(root, "ls-remote", "origin", "refs/heads/develop", optional=True, timeout=20)
    current_remote = remote_sha(raw_remote)
    if not current_remote and not remote_error:
        remote_error = "origin/develop not returned by ls-remote"
    tracked, _ = git(root, "diff", "--name-only")
    staged, _ = git(root, "diff", "--cached", "--name-only")
    status_text, _ = git(root, "status", "--porcelain=v1", "--untracked-files=normal")
    tracked_names = [p for p in tracked.splitlines() if p]
    staged_names = [p for p in staged.splitlines() if p]
    status = [p for p in status_text.splitlines() if p]
    untracked = [p for p in status if p.startswith("?? ")]
    # Untracked audit bundles are not tracked edits and must not prevent a safe
    # documentation-only closeout. They are still fully reported.
    tracked_edits = [p for p in status if not p.startswith("?? ")]
    source_blobs = git_blob_map(root, REVIEWED_BLOBS)
    document_blobs = git_blob_map(root, DOCUMENT_BLOBS)
    source_matches = all(source_blobs.get(path) == sha for path, sha in REVIEWED_BLOBS.items())
    document_matches = all(document_blobs.get(path) == sha for path, sha in DOCUMENT_BLOBS.items())
    after = git(root, "rev-parse", "HEAD")[0]
    if before != after:
        raise RuntimeError("Concurrent HEAD change during audit: state not stable")
    verdict = decision(head=before or "", remote=current_remote, status=tracked_edits,
                       source_matches=source_matches, document_matches=document_matches)
    output_root = outside_repo_dir(root)
    output_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    folder = output_root / ("r10et_closeout_r1_" + stamp)
    folder.mkdir(parents=False, exist_ok=False)
    payload = {
        "mode": "AUDIT_ONLY", "phase": "169 R10ET Closeout R1",
        "github_reviewed_head": REVIEWED_GITHUB_HEAD, "previous_local_head": PREVIOUS_LOCAL_HEAD,
        "local_head": before, "branch": branch, "tracking_ref": current_tracking,
        "tracking_error": tracking_error, "live_remote_head": current_remote,
        "remote_probe_error": remote_error, "tracked_unstaged": tracked_names,
        "tracked_staged": staged_names, "status_lines": status,
        "untracked_status_lines": untracked,
        "source_expected_blobs": REVIEWED_BLOBS, "source_actual_blobs": source_blobs,
        "source_matches_reviewed_github": source_matches,
        "document_expected_blobs": DOCUMENT_BLOBS, "document_actual_blobs": document_blobs,
        "documents_match_reviewed_github": document_matches,
        "verdict": verdict, "repo_files_modified": False, "full_pytest_run": False,
    }
    (folder / "audit.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = [
        "# Phase 169 R10ET Closeout R1 — Git 同期・文書更新前監査", "",
        "状態：AUDIT_ONLY（作業ツリー・Git index・refs・文書の変更なし）。", "",
        f"- GitHub 確認時 HEAD: `{REVIEWED_GITHUB_HEAD}`",
        f"- ローカル HEAD: `{before}`", f"- Live remote HEAD: `{current_remote or 'UNVERIFIED'}`",
        f"- origin/develop tracking: `{current_tracking or 'UNAVAILABLE'}`",
        f"- 作業ツリーの変更項目数: `{len(status)}`（未追跡ディレクトリを含む）",
        f"- 未ステージの tracked 変更: `{len(tracked_names)}`",
        f"- 未追跡項目: `{len(untracked)}`（文書更新の阻害条件にしない）",
        f"- ステージ済み変更: `{len(staged_names)}`",
        f"- GitHub と本体8ファイル一致: `{source_matches}`",
        f"- GitHub と文書5ファイル一致: `{document_matches}`",
        f"- 判定: `{verdict}`", "",
        "## 方針", "",
        "結果にかかわらず、この監査は pull / fetch / reset / checkout / clean / add を実行しない。",
        "同期・競合解消前に README.md 等を上書きしない。", "",
        "## 未ステージの tracked 差分", "",
    ]
    summary.extend(f"- `{p}`" for p in tracked_names)
    summary.extend(["", "## ステージ済み差分", ""])
    summary.extend(f"- `{p}`" for p in staged_names)
    summary.extend(["", "## GitHub と一致しない本体ファイル", ""])
    summary.extend(f"- `{p}`" for p, sha in REVIEWED_BLOBS.items() if source_blobs.get(p) != sha)
    summary.extend(["", "## GitHub と一致しない文書ファイル", ""])
    summary.extend(f"- `{p}`" for p, sha in DOCUMENT_BLOBS.items() if document_blobs.get(p) != sha)
    summary.append("")
    (folder / "audit.md").write_text("\n".join(summary), encoding="utf-8")
    print("R10ET_CLOSEOUT_R1_MODE=AUDIT_ONLY", flush=True)
    print("R10ET_CLOSEOUT_R1_REVIEWED_GITHUB_HEAD=" + REVIEWED_GITHUB_HEAD, flush=True)
    print("R10ET_CLOSEOUT_R1_LOCAL_HEAD=" + str(before), flush=True)
    print("R10ET_CLOSEOUT_R1_TRACKING_HEAD=" + str(current_tracking or "UNAVAILABLE"), flush=True)
    print("R10ET_CLOSEOUT_R1_REMOTE_HEAD=" + str(current_remote or "UNVERIFIED"), flush=True)
    if remote_error:
        print("R10ET_CLOSEOUT_R1_REMOTE_ERROR=" + remote_error, flush=True)
    print(f"R10ET_CLOSEOUT_R1_TRACKED_UNSTAGED={len(tracked_names)}", flush=True)
    print(f"R10ET_CLOSEOUT_R1_TRACKED_STAGED={len(staged_names)}", flush=True)
    print(f"R10ET_CLOSEOUT_R1_STATUS_LINES={len(status)}", flush=True)
    print(f"R10ET_CLOSEOUT_R1_UNTRACKED={len(untracked)}", flush=True)
    print(f"R10ET_CLOSEOUT_R1_SOURCE_MATCH_GITHUB={source_matches}", flush=True)
    print(f"R10ET_CLOSEOUT_R1_DOCUMENTS_MATCH_GITHUB={document_matches}", flush=True)
    print("R10ET_CLOSEOUT_R1_DECISION=" + verdict, flush=True)
    print("R10ET_CLOSEOUT_R1_REPORT=" + str(folder / "audit.md"), flush=True)
    print("R10ET_CLOSEOUT_R1_NO_REPOSITORY_CHANGES=True", flush=True)
    print("R10ET_CLOSEOUT_R1_EXIT=0", flush=True)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        return execute(args.repo.resolve())
    except BaseException:
        print("R10ET_CLOSEOUT_R1_ERROR=" + traceback.format_exc(), flush=True)
        print("R10ET_CLOSEOUT_R1_EXIT=1", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

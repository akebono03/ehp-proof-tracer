"""Inspect Git environment issues without changing repository files or index."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def git_read(root: Path, *arguments: str) -> dict:
    env = dict(os.environ)
    env["GIT_OPTIONAL_LOCKS"] = "0"
    command = ["git", "--no-optional-locks", "-C", str(root), *arguments]
    try:
        process = subprocess.run(command, text=True, encoding="utf-8", errors="replace", capture_output=True, env=env, timeout=40, check=False)
        return {"arguments": list(arguments), "exit_code": process.returncode,
                "stdout": process.stdout.strip(), "stderr": process.stderr.strip()}
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return {"arguments": list(arguments), "exit_code": None,
                "stdout": "", "stderr": f"{type(exc).__name__}: {exc}"}


def conflict_copy_files(root: Path) -> list[dict]:
    gitdir = root / ".git"
    results: list[dict] = []
    for relative in ("refs", "logs"):
        base = gitdir / relative
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if "競合コピー" not in path.name and "conflicted copy" not in path.name.lower():
                continue
            results.append({"path": path.relative_to(root).as_posix(),
                            "size_bytes": path.stat().st_size,
                            "sample": path.read_text(encoding="utf-8", errors="replace")[:200]})
    return sorted(results, key=lambda row: row["path"])


def longest_audit_files(root: Path, limit: int = 12) -> list[dict]:
    base = root / "phase169_r10et_r5d_staged_audit_guard" / "output"
    if not base.is_dir():
        return []
    found = []
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        found.append({"path": path.relative_to(root).as_posix(),
                      "absolute_path_length": len(str(path)),
                      "greater_than_259": len(str(path)) > 259})
    return sorted(found, key=lambda row: row["absolute_path_length"], reverse=True)[:limit]


def collect(root: Path) -> dict:
    if not (root / ".git").is_dir():
        raise RuntimeError("Repository .git directory is missing or not a directory")
    return {
        "mode": "AUDIT_ONLY", "root": str(root),
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
        "git": {
            "version": git_read(root, "--version"),
            "branch": git_read(root, "branch", "--show-current"),
            "head": git_read(root, "rev-parse", "--verify", "HEAD"),
            "origin_develop": git_read(root, "rev-parse", "--verify", "refs/remotes/origin/develop"),
            "local_longpaths": git_read(root, "config", "--local", "--get", "core.longpaths"),
            "tracked_status": git_read(root, "-c", "core.longpaths=true", "status", "--short", "-uno"),
            "staged_changes": git_read(root, "diff", "--cached", "--name-status"),
            "working_changes": git_read(root, "diff", "--name-status"),
        },
        "dropbox_conflict_copies": conflict_copy_files(root),
        "long_generated_paths": longest_audit_files(root),
        "does_not_modify_repository": True,
    }


def markdown_report(data: dict) -> str:
    lines = [
        "# EHP Proof Tracer — Git 作業環境の読み取り専用監査", "",
        f"- 作業ディレクトリ: `{data['root']}`",
        f"- 実行時刻: `{data['recorded_at']}`",
        "- **Git の設定・ファイル・ステージ領域は変更していない。**", "",
        "## Git の読み取り結果", "",
    ]
    for key, value in data["git"].items():
        lines.extend((f"### {key}", "", f"終了コード: `{value['exit_code']}`", "",
                      "```text", value["stdout"] or "(no output)", value["stderr"] or "", "```", ""))
    lines.extend(("## Dropbox の競合コピー", "", f"件数: {len(data['dropbox_conflict_copies'])}", ""))
    for row in data["dropbox_conflict_copies"]:
        lines.append(f"- `{row['path']}` ({row['size_bytes']} bytes)")
    lines.extend(("", "## R5D の生成ファイルの長いパス（上位12件）", ""))
    for row in data["long_generated_paths"]:
        lines.append(f"- {row['absolute_path_length']}文字: `{row['path']}`")
    lines.extend(("", "## 安全上の注意", "",
                  "VS Code を閉じ、Dropbox の同時同期を止めてから、別途保全して復旧手順を検討する。",
                  "この監査では `.git` 内の競合ファイルを削除・改名していない。",
                  "R5D output のファイルを削除していない。全体 pytest は未実行。", ""))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    data = collect(root)
    (output / "audit.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "audit.md").write_text(markdown_report(data), encoding="utf-8")
    print("GIT_ENV_MODE=AUDIT_ONLY")
    print(f"GIT_ENV_CONFLICT_REFLOG_FILES={len(data['dropbox_conflict_copies'])}")
    print(f"GIT_ENV_LONGEST_PATH={max((r['absolute_path_length'] for r in data['long_generated_paths']), default=0)}")
    print("GIT_ENV_GIT_HEAD=" + data["git"]["head"]["stdout"])
    print("GIT_ENV_STAGED_PATHS_PRESERVED=True")
    print(f"GIT_ENV_REPORT={output / 'audit.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

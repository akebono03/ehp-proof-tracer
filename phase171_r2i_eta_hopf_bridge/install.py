"""Install one additive shared-provider hook; preserve local R2H work."""
from __future__ import annotations

import argparse
import ast
import subprocess
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
ANCHOR = (
    "        options.extend(expand_cited_prop22_right_formula(goal, tuple(available)))\n"
)
ADDITION = (
    "        from phase171_r2i_eta_hopf_bridge.source import (\n"
    "            expand_cited_eta_hopf_power,\n"
    "        )\n"
    "        options.extend(expand_cited_eta_hopf_power(goal, tuple(available)))\n"
)


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True,
    )
    return result.stdout.strip()


def _decode_baseline(raw: bytes) -> tuple[str, bytes]:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("unexpected UTF-8 BOM in shared_math; refusing conversion")
    text = raw.decode("utf-8")
    if b"\r\n" in raw and raw.count(b"\r\n") == raw.count(b"\n"):
        newline = b"\r\n"
    elif b"\r\n" not in raw:
        newline = b"\n"
    else:
        raise RuntimeError("mixed CRLF/LF newlines in shared_math")
    return text.replace("\r\n", "\n"), newline


def _full_function_source(text: str) -> str:
    tree = ast.parse(text)
    functions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "shared_expansion_provider"
    ]
    if len(functions) != 1:
        raise RuntimeError("cannot isolate exactly one shared_expansion_provider")
    lines = text.splitlines(keepends=True)
    return "".join(lines[functions[0].lineno - 1: functions[0].end_lineno])


def _report(text: str) -> str:
    originals = (ROOT / "phase171_r2i_eta_hopf_bridge" / "source.py").read_text(encoding="utf-8")
    test = (ROOT / "phase171_r2i_eta_hopf_bridge" / "tests" / "test_cited_eta_hopf.py").read_text(encoding="utf-8")
    return (
        "# Phase 171 R2I — 全文コード記録\n\n"
        "## 変更対象\n\n"
        "- `phase165_r52_r9_shared_math.py` — `shared_expansion_provider` 全体（下記）\n"
        "- 新規 `phase171_r2i_eta_hopf_bridge/source.py` — 全関数・クラス（下記）\n"
        "- 新規 `phase171_r2i_eta_hopf_bridge/tests/test_cited_eta_hopf.py` — テスト全文（下記）\n"
        "- 新規 `phase171_r2i_eta_hopf_bridge/audit.py`、`install.py`、`run.ps1`（ZIP 内の全文）\n\n"
        "モジュール先頭の import は変更なし。変更関数内部に R2I の import を追加。\n"
        "新規ファイルはパッケージの先頭から末尾までが実装全文。\n\n"
        "## `shared_expansion_provider` 変更後全文\n\n```python\n"
        + _full_function_source(text)
        + "\n```\n\n## 新規 `source.py` 全文\n\n```python\n"
        + originals + "\n```\n\n## 新規テスト全文\n\n```python\n"
        + test + "\n```\n"
    )


def install(*, dry_run: bool) -> None:
    if not (ROOT / ".git").is_dir():
        raise RuntimeError("unzip the package directly inside the existing Git repository")
    branch = _git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("expected develop, got " + branch)
    head = _git("rev-parse", "HEAD")
    print("PHASE171_R2I_BRANCH=" + branch, flush=True)
    print("PHASE171_R2I_HEAD=" + head, flush=True)
    if not TARGET.is_file():
        raise RuntimeError("shared_math missing")
    if not (ROOT / "phase171_r2h_prop22_cited_hopf" / "source.py").is_file():
        raise RuntimeError("R2H missing; do not attempt to replace its uncommitted code")
    raw = TARGET.read_bytes()
    before, newline = _decode_baseline(raw)
    if before.count(ANCHOR) != 1:
        raise RuntimeError("R2H hook missing or ambiguous; not writing anything")
    if before.count(ADDITION) > 1:
        raise RuntimeError("duplicate R2I hook")
    already = ADDITION in before
    changed = before if already else before.replace(ANCHOR, ANCHOR + ADDITION, 1)
    ast.parse(changed)
    if changed.count(ADDITION) != 1:
        raise RuntimeError("R2I hook insertion failed")
    _full_function_source(changed)
    print("PHASE171_R2I_PREFLIGHT=PASS", flush=True)
    print("PHASE171_R2I_R2H_PRESERVED=PASS", flush=True)
    print("PHASE171_R2I_EXISTING_HOOK=" + str(already), flush=True)
    if dry_run:
        print("PHASE171_R2I_RESULT=PASS_DRY_RUN", flush=True)
        return
    output = PACKAGE / "output"
    output.mkdir(exist_ok=True)
    if not already:
        backup = output / "phase165_r52_r9_shared_math.py.before_r2i"
        if backup.exists() and backup.read_bytes() != raw:
            raise RuntimeError("existing backup differs; not overwriting it")
        if not backup.exists():
            backup.write_bytes(raw)
        current = TARGET.read_bytes()
        if current != raw:
            raise RuntimeError("shared_math changed during preflight")
        rewritten = changed.encode("utf-8").replace(b"\n", newline)
        TARGET.write_bytes(rewritten)
        if TARGET.read_bytes() != rewritten:
            raise RuntimeError("shared_math write verification failed")
        print("PHASE171_R2I_PATCHED=phase165_r52_r9_shared_math.py", flush=True)
        print("PHASE171_R2I_BACKUP=" + str(backup), flush=True)
    full = output / "CHANGED_CODE_FULL_JA.md"
    full.write_text(_report(changed), encoding="utf-8")
    print("PHASE171_R2I_CHANGED_CODE=" + str(full), flush=True)
    print("PHASE171_R2I_RESULT=PASS_APPLY", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    install(dry_run=arguments.dry_run)


if __name__ == "__main__":
    main()

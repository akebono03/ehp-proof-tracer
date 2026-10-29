"""Conservative R2J-R2 installer; preserves CRLF and unrelated changes."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
OUTPUT = HERE / "output"
BACKUP = OUTPUT / "phase165_r52_r9_shared_math.py.before_r2j_r2"
STATE = OUTPUT / "state.json"
HOOK = "expand_cited_cyclic_hopf_surjectivity"
ANCHOR = "        options.extend(expand_cited_eta_hopf_power(goal, tuple(available)))\n"
ADDITION = (
    "        from phase171_r2j_r2_cyclic_hopf_surjective.source import (\n"
    "            expand_cited_cyclic_hopf_surjectivity,\n"
    "        )\n"
    "        options.extend(expand_cited_cyclic_hopf_surjectivity(\n"
    "            goal, tuple(available), proof_target=proof_target,\n"
    "        ))\n"
)
EXPECTED_BASE_HEADS = (
    "176766a70841853039b8efaac0a8661eac22686d",
    "d172a8a7b0d50f56509f30287aded1b304c7d6a2",
)
EXPECTED_SHARED_BLOB = "be8824391358d9295ab950e42b7dee5cf34d15a8"


def _git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args,
        cwd=ROOT, check=True, capture_output=True,
        encoding="utf-8", errors="replace",
    ).stdout.strip()


def _digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def _render_source_with_hook(original: bytes) -> bytes:
    raw = original.decode("utf-8-sig")
    normalized = raw.replace("\r\n", "\n")
    if normalized.count(ANCHOR) != 1:
        raise RuntimeError("R2I shared hook not found exactly once")
    if HOOK in normalized:
        raise RuntimeError("R2J-R2 hook already present")
    modified = normalized.replace(ANCHOR, ANCHOR + ADDITION)
    ast.parse(modified)
    eol = "\r\n" if b"\r\n" in original else "\n"
    return (b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b"") + modified.replace("\n", eol).encode("utf-8")


def _full_function(source: str, function: str) -> str:
    tree = ast.parse(source)
    found = [node for node in tree.body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
             and node.name == function]
    if len(found) != 1:
        raise RuntimeError("changed full function not uniquely found: " + function)
    lines = source.splitlines()
    node = found[0]
    return "\n".join(lines[node.lineno - 1:node.end_lineno]) + "\n"


def _changed_code_document(shared: str) -> str:
    source = (HERE / "source.py").read_text(encoding="utf-8")
    audit = (HERE / "audit.py").read_text(encoding="utf-8")
    tests = (HERE / "tests" / "test_cited_cyclic_hopf.py").read_text(encoding="utf-8")
    import_part = shared[:shared.index("def build_shared_typed_bridge(")]
    return (
        "# Phase 171 R2J-R2 変更コード全文\n\n"
        "## 変更対象\n\n"
        "- 既存ファイル `phase165_r52_r9_shared_math.py`\n"
        "- 関数 `shared_expansion_provider`（全体を以下に提示）\n"
        "- 追加位置：R2I `expand_cited_eta_hopf_power` の直後\n"
        "- 新規 `phase171_r2j_r2_cyclic_hopf_surjective/source.py`（全文）\n"
        "- 新規 `audit.py`（全文）と `tests/test_cited_cyclic_hopf.py`（全文）\n"
        "- 既存ファイルのトップレベル import 変更なし\n\n"
        "## 既存ファイル import 全文（モジュールドキュメントも含む）\n\n```python\n"
        + import_part + "```\n\n"
        "## `shared_expansion_provider` 関数全文\n\n```python\n"
        + _full_function(shared, "shared_expansion_provider") + "```\n\n"
        "## 新規 source.py 全文\n\n```python\n" + source + "\n```\n\n"
        "## 新規 audit.py 全文\n\n```python\n" + audit + "\n```\n\n"
        "## 新規テスト全文\n\n```python\n" + tests + "\n```\n"
    )


def preflight() -> tuple[bytes, bool]:
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    print("PHASE171_R2J_R2_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R2_HEAD=" + head, flush=True)
    if branch != "develop":
        raise RuntimeError("develop branch required; checkout/reset forbidden")
    if not TARGET.is_file():
        raise RuntimeError("shared production module missing")
    raw = TARGET.read_bytes()
    normalized = raw.decode("utf-8-sig").replace("\r\n", "\n")
    installed = HOOK in normalized
    if not installed and head not in EXPECTED_BASE_HEADS:
        raise RuntimeError("unexpected HEAD; re-audit GitHub before applying")
    if (not installed and _git(
            "rev-parse", "HEAD:phase165_r52_r9_shared_math.py"
    ) != EXPECTED_SHARED_BLOB):
        raise RuntimeError("shared production blob differs from audited GitHub version")
    if not installed and _git("diff", "--", str(TARGET.relative_to(ROOT))):
        raise RuntimeError("existing tracked edit to shared module: preserve and audit first")
    if normalized.count(ANCHOR) != 1:
        raise RuntimeError("R2I hook missing or changed")
    if installed and normalized.count(HOOK) != 2:
        raise RuntimeError("incomplete or ambiguous R2J-R2 installation")
    if not installed:
        _render_source_with_hook(raw)
    print("PHASE171_R2J_R2_R2I_PRESERVED=PASS", flush=True)
    print("PHASE171_R2J_R2_PREFLIGHT=PASS", flush=True)
    print("PHASE171_R2J_R2_ALREADY_INSTALLED=" + str(installed), flush=True)
    return raw, installed


def apply(dry_run: bool) -> None:
    raw, installed = preflight()
    if dry_run:
        print("PHASE171_R2J_R2_RESULT=PASS_DRY_RUN", flush=True)
        return
    if installed:
        print("PHASE171_R2J_R2_RESULT=PASS_ALREADY_APPLIED", flush=True)
        return
    altered = _render_source_with_hook(raw)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if BACKUP.exists() or STATE.exists():
        raise RuntimeError("existing installer backup/state: review before applying")
    BACKUP.write_bytes(raw)
    try:
        TARGET.write_bytes(altered)
        edited_text = altered.decode("utf-8-sig").replace("\r\n", "\n")
        (OUTPUT / "phase165_r52_r9_shared_math.py.FULL").write_bytes(altered)
        (OUTPUT / "CHANGED_CODE_FULL_JA.md").write_text(
            _changed_code_document(edited_text), encoding="utf-8",
        )
        STATE.write_text(json.dumps({
            "before_sha256": _digest(raw),
            "after_sha256": _digest(altered),
        }, indent=2) + "\n", encoding="utf-8")
    except Exception:
        if TARGET.read_bytes() == altered:
            TARGET.write_bytes(raw)
        raise
    print("PHASE171_R2J_R2_PATCHED=" + TARGET.name, flush=True)
    print("PHASE171_R2J_R2_BACKUP=" + str(BACKUP), flush=True)
    print("PHASE171_R2J_R2_CHANGED_CODE=" + str(OUTPUT / "CHANGED_CODE_FULL_JA.md"), flush=True)
    print("PHASE171_R2J_R2_RESULT=PASS_APPLY", flush=True)


def restore() -> None:
    if not BACKUP.is_file() or not STATE.is_file():
        raise RuntimeError("no verified R2J-R2 backup")
    record = json.loads(STATE.read_text(encoding="utf-8"))
    original = BACKUP.read_bytes()
    if _digest(original) != record["before_sha256"]:
        raise RuntimeError("backup hash changed")
    if _digest(TARGET.read_bytes()) != record["after_sha256"]:
        raise RuntimeError("target has changed; refusing unsafe restore")
    TARGET.write_bytes(original)
    STATE.unlink()
    print("PHASE171_R2J_R2_RESULT=PASS_RESTORE", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--dry-run", action="store_true")
    actions.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    if args.restore:
        restore()
    else:
        apply(args.dry_run)


if __name__ == "__main__":
    main()

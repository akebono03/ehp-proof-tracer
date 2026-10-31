# Phase 172 R1：追加コード全文

変更対象の既存ファイル・既存クラス・既存関数はありません。
新規の各ファイルはリポジトリ直下の `phase172_r1_renderer_audit/` に追加します。新規 import は下記コードの先頭に全文含まれています。コード中の省略はありません。

## audit.py（全文）

```python
"""Phase 172 R1: read-only, proof-step-linked canonical pi_6^3 display audit.

No proof, reference, renderer, registry, or test data are altered. All output
is outside the Git worktree. A completed public proof is searched afresh.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import traceback
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
PACKAGE_NAME = "phase172_r1_renderer_audit"
BASELINE_COMMIT = "a64edd93e0df561b0970d482c6b2bd0ec72b2344"
REVIEWED_GITHUB_BLOBS = {
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
    "phase165_r52_r4_flask_bridge.py": "aec7615671ea0b472d4f6093c06fc0f857632db7",
    "phase165_r52_r3_web_adapter.py": "aefdc5527aeec7bcb7ffe77f69b754a39f3a242b",
    "phase168_r3_3_proof_narrative_model.py": "f09be949a7a07fc3f082bcd267f41c9f606590ea",
    "phase168_r3_4_link_bridge.py": "c3a6233a57c41e61e6649ee33c7a336d7aa1c664",
    "phase168_r3_5_model_renderer.py": "94996b403f1c01f81319824565db422463714f02",
    "phase168_r3_12_body_binding.py": "ac7d387158b0af8ead4b07f623c216ed1dd561dd",
    "phase171_r20r12_verified_cyclic_narrative/projection.py": "73babd53daf6ec088e12b723a905ba40523f8120",
    "phase171_r20r13_eta_sentence_layout/projection.py": "4c1ef57ed0a20d551ae24c80d4b7ddbbb7df9c31",
    "phase171_r20r13_eta_sentence_layout/tests/test_projection.py": "6031f6a1b396d040181f04b792bc5c5caf2c5530",
    "phase171_r20r12_verified_cyclic_narrative/tests/test_projection.py": "512e67c66f5a36a30b40b06d974f537fd08ca6f7",
    "phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py": "881d5a5cdc77220be42615236ed99ff3ec6ee164",
}
FOCUSED_TESTS = (
    "phase171_r20r13_eta_sentence_layout/tests/test_projection.py",
    "phase171_r20r12_verified_cyclic_narrative/tests/test_projection.py",
    "phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py",
)
RELEVANT_SYMBOLS = {
    "web_group_proof.py": ["build_standard_web_group_proof_view"],
    "phase168_r3_5_model_renderer.py": ["render_model_backed_narrative_markdown"],
    "phase168_r3_3_proof_narrative_model.py": ["build_proof_narrative_model", "root_ancestor_step_indices"],
    "phase168_r3_4_link_bridge.py": ["build_linked_proof_narrative_model"],
    "phase168_r3_12_body_binding.py": ["build_narrative_body_lines"],
    "phase171_r20r12_verified_cyclic_narrative/projection.py": ["verified_order_four_summary", "suppress_exact_duplicate_body_lines"],
    "phase171_r20r13_eta_sentence_layout/projection.py": ["verified_eta_display_sentences", "combine_adjacent_verified_eta_sentences", "format_complete_proof_sentences"],
}
MATH_RE = re.compile(r"\$([^$\n]+)\$")
INTERNAL_RE = re.compile(r"DB[ _-]?prior|prior[_ -]?result|source[_ -]?id|internal[_ -]?rule|GIVEN", re.IGNORECASE)


def git(*args: str, timeout: int = 15) -> dict[str, Any]:
    """Observe Git state without updating refs, index, or worktree."""
    try:
        p = subprocess.run(
            ["git", *args], cwd=ROOT, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, encoding="utf-8", errors="replace",
            timeout=timeout, check=False,
        )
        return {"exit_code": p.returncode, "stdout": p.stdout.strip(),
                "stderr": p.stderr.strip()}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"exit_code": -1, "stdout": "", "stderr": str(exc)}


def get_git_value(*args: str) -> str:
    result = git(*args)
    if result["exit_code"] != 0:
        raise RuntimeError(f"git {args!r}: {result['stderr']}")
    return str(result["stdout"])


def preflight() -> dict[str, Any]:
    """Require reviewed GitHub content, no edits to watched files, develop."""
    branch = get_git_value("branch", "--show-current")
    head = get_git_value("rev-parse", "HEAD")
    status = get_git_value("status", "--porcelain=v1", "--untracked-files=no")
    remote = git("ls-remote", "origin", "refs/heads/develop", timeout=15)
    remote_sha = remote["stdout"].split()[0] if remote["exit_code"] == 0 and remote["stdout"] else None
    blobs: dict[str, Any] = {}
    for relative_path, expected in REVIEWED_GITHUB_BLOBS.items():
        path = ROOT / relative_path
        committed = git("rev-parse", "HEAD:" + relative_path)
        tracked = committed["stdout"] if committed["exit_code"] == 0 else None
        worktree = git("hash-object", "--", relative_path) if path.is_file() else {
            "exit_code": 2, "stdout": "", "stderr": "missing worktree file",
        }
        # Git's working tree may use CRLF while the index retains the same blob.
        # A tracked change to a watched file is disallowed by the status below.
        blobs[relative_path] = {
            "reviewed_sha": expected,
            "committed_sha": tracked,
            "working_sha": worktree["stdout"] if worktree["exit_code"] == 0 else None,
            "committed_matches": tracked == expected,
            "file_exists": path.is_file(),
        }
    tracked_paths = [line[3:].replace("\\", "/") for line in status.splitlines() if len(line) >= 4]
    changed_watched = sorted(set(tracked_paths) & set(REVIEWED_GITHUB_BLOBS))
    check = {
        "branch": branch,
        "local_head": head,
        "phase171_baseline_commit": BASELINE_COMMIT,
        "remote_develop_head": remote_sha,
        "remote_check": "REACHABLE" if remote_sha else "UNAVAILABLE",
        "remote_error": remote["stderr"] if remote_sha is None else "",
        "tracked_status_before": status,
        "changed_watched_paths": changed_watched,
        "source_blobs": blobs,
        "full_pytest": False,
    }
    if branch != "develop":
        raise RuntimeError("Preflight failed: branch must be develop")
    if changed_watched:
        raise RuntimeError("Preflight failed: reviewed files have local edits: " + ", ".join(changed_watched))
    mismatches = [name for name, item in blobs.items()
                  if not item["committed_matches"] or not item["file_exists"]]
    if mismatches:
        raise RuntimeError("Preflight failed: GitHub-reviewed file content differs: " + ", ".join(mismatches))
    if remote_sha is not None and remote_sha != head:
        raise RuntimeError("Preflight failed: local HEAD differs from origin/develop. No pull is attempted. "
                           f"local={head}, remote={remote_sha}")
    return check


def safe_repr(obj: Any, length: int = 1200) -> str:
    value = repr(obj)
    if len(value) > length:
        return value[:length] + " [truncated]"
    return value


def math_fragments(line: str) -> tuple[str, ...]:
    """Extract display-only matching candidates, never infer mathematics."""
    return tuple(fragment.strip() for fragment in MATH_RE.findall(line)
                 if len(fragment.strip()) >= 6)


def display_categories(line: str) -> list[str]:
    """Keyword flags for an audit, not claims about duplicate mathematical facts."""
    categories: list[str] = []
    if (r"\eta_" in line or "η" in line) and ("E(" in line or r"E\eta" in line or r"\xrightarrow{E}" in line):
        categories.append("ETA_SUSPENSION")
    if ("H(" in line or r"H\left" in line or "H:" in line or r"\xrightarrow{H}" in line or "Hopf" in line) and (
        r"\nu" in line or "ν" in line or "Hopf" in line or "全射" in line
    ):
        categories.append("HOPF_DESCRIPTION")
    if "全射" in line or "surject" in line.lower():
        categories.append("SURJECTIVITY")
    if INTERNAL_RE.search(line):
        categories.append("INTERNAL_REFERENCE_TEXT")
    if r"\operatorname{ord}" in line or "短完全列" in line:
        categories.append("ORDER_FOUR_SUMMARY")
    return categories


def locate_premises(steps: tuple[Any, ...], step: Any) -> list[int | None]:
    result: list[int | None] = []
    for premise in step.premises:
        found = [i for i, node in enumerate(steps) if node is premise]
        if not found:
            found = [i for i, node in enumerate(steps) if node == premise]
        result.append(found[0] if len(found) == 1 else None)
    return result


def build_step_inventory(model: Any) -> list[dict[str, Any]]:
    from web_group_proof_common import _group_proof_statement_latex
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    inventory: list[dict[str, Any]] = []
    for i, step in enumerate(model.steps):
        latex, fallback = _group_proof_statement_latex(step.conclusion)
        sentence = typed_sentence(step.conclusion, step)
        inference = getattr(step, "inference_rule", None)
        inventory.append({
            "step_index": i,
            "in_root_ancestry": i in scope,
            "is_root": i == model.root_index,
            "proof_rule": getattr(step.rule, "value", str(step.rule)),
            "statement_type": type(step.conclusion).__name__,
            "statement_repr": safe_repr(step.conclusion),
            "latex": latex,
            "fallback_type": fallback,
            "typed_sentence": sentence,
            "inference_rule_for_audit_only": getattr(inference, "name", None),
            "premise_step_indices": locate_premises(model.steps, step),
            "citation_numbers": list(model.step_citation_numbers[i]),
        })
    return inventory


def align_body_lines(markdown: str, inventory: list[dict[str, Any]], model: Any) -> list[dict[str, Any]]:
    """Return candidate correspondence; never assert unique attribution from TeX."""
    _, separator, body = markdown.partition("\n証明\n")
    if not separator:
        raise RuntimeError("Web narrative has no '証明' section")
    from phase171_r20r12_verified_cyclic_narrative.projection import verified_order_four_summary
    summary = verified_order_four_summary(model)
    result: list[dict[str, Any]] = []
    for number, line in enumerate(body.splitlines(), start=1):
        if not line.strip():
            continue
        fragments = math_fragments(line)
        exact: list[int] = []
        math_matches: list[int] = []
        for item in inventory:
            if not item["in_root_ancestry"]:
                continue
            sentence = item["typed_sentence"]
            if sentence and (sentence.strip() == line.strip() or sentence.strip() in line):
                exact.append(item["step_index"])
            candidate_fragments = set(math_fragments(sentence or ""))
            if item["latex"]:
                candidate_fragments.add(item["latex"])
            if fragments and any(value in candidate_fragments for value in fragments):
                math_matches.append(item["step_index"])
        is_summary = summary is not None and line in summary or (summary is not None and summary in line)
        result.append({
            "proof_body_line_number": number,
            "printed_text": line,
            "categories": display_categories(line),
            "exact_typed_sentence_step_candidates": sorted(set(exact)),
            "math_match_step_candidates": sorted(set(math_matches)),
            "root_supported_summary": bool(is_summary),
            "summary_root_step_index": model.root_index if is_summary else None,
            "attribution_note": "候補対応のみ。特に合成文は複数の ProofStep に依存する。",
        })
    return result


def duplicate_inventory(lines: list[dict[str, Any]]) -> dict[str, Any]:
    """Observe repetitions without conflating distinct source/proof assertions."""
    exact_groups: dict[str, list[int]] = defaultdict(list)
    formula_groups: dict[str, list[int]] = defaultdict(list)
    for row in lines:
        line = row["printed_text"].strip()
        exact_groups[line].append(row["proof_body_line_number"])
        for f in set(math_fragments(line)):
            formula_groups[f].append(row["proof_body_line_number"])
    return {
        "byte_identical_nonempty_lines": [
            {"text": text, "line_numbers": numbers}
            for text, numbers in exact_groups.items() if len(numbers) > 1
        ],
        "shared_tex_fragments": [
            {"latex": latex, "line_numbers": numbers}
            for latex, numbers in formula_groups.items() if len(numbers) > 1
        ],
        "warning": "同一 TeX の複数回登場だけでは意味的な重複とは判定しない。",
    }


def capture_canonical_proof() -> dict[str, Any]:
    """Follow the exact searched/verified/model-backed production route."""
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase171_r20r13_eta_sentence_layout.projection import verified_eta_display_sentences

    bridge = build_shared_typed_bridge()
    contexts: list[Any] = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or result.open_goals or len(contexts) != 1:
        raise RuntimeError("The real pi_6^3 search is not complete, or lacks a single context")
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing is None:
        raise RuntimeError("Expected registered proof-source publication binding is absent")
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    if model.root_index is None or not model.steps:
        raise RuntimeError("Verified complete model has no root step")
    ancestry = root_ancestor_step_indices(model.steps, model.root_index)
    markdown = render_model_backed_narrative_markdown(result, model)
    view = build_partial_web_group_proof_view(
        result, max_depth=2, mode="narrative", narrative_model=model,
    )
    if (view.key != "generic-complete-proof" or view.partial_result
            or not view.steps or not view.rendered_lines):
        raise RuntimeError("Verified Web adapter did not return a complete proof")
    inventory = build_step_inventory(model)
    lines = align_body_lines(markdown, inventory, model)
    references = [{
        "number": c.number,
        "locator": c.reference.locator or c.reference.label,
        "step_indices": list(c.step_indices),
        "assertion_ids": list(c.assertion_ids),
        "reference_ids": list(c.reference_ids),
        "statement_bodies": list(c.statement_bodies),
        "internal_term_hits": [x for x in (c.reference.locator or c.reference.label, *c.statement_bodies) if INTERNAL_RE.search(x)],
    } for c in model.citations]
    web = [{
        "kind": x.kind,
        "indent_level": x.indent_level,
        "prefix": x.prefix,
        "statement_latex": x.statement_latex,
        "suffix": x.suffix,
        "segments": [{"kind": seg.kind, "value": seg.value} for seg in x.segments],
    } for x in view.rendered_lines]
    by_category = {
        category: [row for row in lines if category in row["categories"]]
        for category in ("ETA_SUSPENSION", "HOPF_DESCRIPTION", "SURJECTIVITY", "INTERNAL_REFERENCE_TEXT", "ORDER_FOUR_SUMMARY")
    }
    return {
        "public_status": result.status.value,
        "web_key": view.key,
        "web_partial": view.partial_result,
        "root_index": model.root_index,
        "proven_step_count": len(result.proven_steps),
        "root_ancestry_count": len(ancestry),
        "open_goals_count": len(result.open_goals),
        "reference_count": len(model.citations),
        "verified_eta_sentence_count": len(verified_eta_display_sentences(model)),
        "proof_tree_verified": True,
        "new_given_added": 0,
        "markdown": markdown,
        "proof_steps": inventory,
        "references": references,
        "web_rendered_lines": web,
        "body_lines_with_step_candidates": lines,
        "category_evidence": by_category,
        "duplicate_observations": duplicate_inventory(lines),
    }


def report_directory() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or os.environ.get("TEMP") or str(Path.home()))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%fZ")
    path = base / "EHPProofTracerRecovery" / ("phase172_r1_" + stamp)
    path.mkdir(parents=True, exist_ok=False)
    return path


def save_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")


def formatted_findings(proof: dict[str, Any], pre: dict[str, Any]) -> str:
    findings = [
        "# Phase 172 R1 — π₆³ 表示監査（実行結果）", "",
        f"- ブランチ：`{pre['branch']}`",
        f"- HEAD：`{pre['local_head']}`",
        f"- Web：`{proof['web_key']}`、未解決 Goal：{proof['open_goals_count']}",
        f"- ProofStep：{proof['proven_step_count']} 件（根の祖先：{proof['root_ancestry_count']} 件）",
        f"- Reference：{proof['reference_count']} 件、η 検証済み式：{proof['verified_eta_sentence_count']} 件", "",
        "## 重複候補（表示上の観測のみ）", "",
    ]
    dupe = proof["duplicate_observations"]
    for item in dupe["byte_identical_nonempty_lines"]:
        findings.append(f"- 同一行 {item['line_numbers']}：`{item['text']}`")
    if not dupe["byte_identical_nonempty_lines"]:
        findings.append("- 完全一致の非空行は検出されませんでした。")
    findings.extend(("", "## Reference の内部表記", ""))
    for ref in proof["references"]:
        if ref["internal_term_hits"]:
            findings.append(f"- [R{ref['number']}] {ref['locator']}：ProofStep {ref['step_indices']}")
    findings.extend(("", "## 監査重点箇所と ProofStep 候補", ""))
    labels = {
        "ETA_SUSPENSION": "R2：懸垂 η 関係",
        "HOPF_DESCRIPTION": "R3：Hopf 関係",
        "SURJECTIVITY": "R4：全射性",
        "INTERNAL_REFERENCE_TEXT": "R5：内部的な出典表記",
        "ORDER_FOUR_SUMMARY": "根に依拠する位数4の説明",
    }
    for category, title in labels.items():
        rows = proof["category_evidence"][category]
        findings.extend((f"### {title}（{len(rows)} 行）", ""))
        if not rows:
            findings.append("- キーワードに該当する本文行は検出されませんでした。")
        for row in rows:
            ids = sorted(set(row["exact_typed_sentence_step_candidates"])
                         | set(row["math_match_step_candidates"]))
            indices = ",".join(str(i) for i in ids) if ids else "未対応（合成文の可能性）"
            findings.append(f"- 本文 {row['proof_body_line_number']} 行／ProofStep 候補 {indices}：{row['printed_text']}")
        findings.append("")
    findings.extend((
        "## 判定上の注意", "",
        "- ProofStep 候補は数式・型付き文の照合による診断で、数学的な同一性や唯一性を断言しない。",
        "- 完成証明中の長い要約文は複数の証明済み前提に依拠するため、単一 ProofStep へ帰属させない。",
        "- `web_narrative.md` が共通 Renderer の全文、`proof_steps.json` が Proof Tree の根拠、`references.json` が引用の登録根拠。",
        "- この R1 は既存コードを変更せず、R2〜R5 の修正方針を決定しない。",
        "",
    ))
    return "\n".join(findings)


def run_focused_tests(output: Path) -> list[dict[str, Any]]:
    """Run each existing focused file separately to avoid module-name collisions."""
    outcomes: list[dict[str, Any]] = []
    for index, target in enumerate(FOCUSED_TESTS, 1):
        args = [sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
                "-p", "no:cacheprovider", target]
        command = subprocess.run(
            args, cwd=ROOT, encoding="utf-8", errors="replace",
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        log = output / (f"focused_pytest_{index}.txt")
        log.write_text(command.stdout, encoding="utf-8")
        outcomes.append({"test_path": target, "exit_code": command.returncode,
                         "log_path": str(log)})
        print(f"PHASE172_R1_FOCUSED_{index}=" + ("PASS" if command.returncode == 0 else "FAIL"), flush=True)
    return outcomes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run-focused-tests", action="store_true")
    args = parser.parse_args()
    try:
        pre = preflight()
        print("PHASE172_R1_BRANCH=" + pre["branch"], flush=True)
        print("PHASE172_R1_LOCAL_HEAD=" + pre["local_head"], flush=True)
        print("PHASE172_R1_REMOTE_DEVELOP_HEAD=" + str(pre["remote_develop_head"]), flush=True)
        print("PHASE172_R1_REMOTE_CHECK=" + pre["remote_check"], flush=True)
        print("PHASE172_R1_REVIEWED_CONTENT=PASS", flush=True)
        if args.dry_run:
            print("PHASE172_R1_DRY_RUN=PASS", flush=True)
            print("PHASE172_R1_SOURCE_CHANGES=0", flush=True)
            return 0
        proof = capture_canonical_proof()
        if proof["reference_count"] != 8:
            raise RuntimeError("Phase 171 expected 8 references; observed " + str(proof["reference_count"]))
        if pre["tracked_status_before"] != get_git_value("status", "--porcelain=v1", "--untracked-files=no"):
            raise RuntimeError("Tracked worktree changed during read-only audit")
        output = report_directory()
        (output / "web_narrative.md").write_text(proof.pop("markdown"), encoding="utf-8")
        for key, path in (
            ("proof_steps", "proof_steps.json"),
            ("references", "references.json"),
            ("web_rendered_lines", "web_rendered_lines.json"),
            ("body_lines_with_step_candidates", "line_alignment.json"),
        ):
            save_json(output / path, proof[key])
        tests: list[dict[str, Any]] = []
        if args.run_focused_tests:
            tests = run_focused_tests(output)
        audit = {"phase": "172-R1", "mode": "AUDIT_ONLY", "git": pre,
                 "proof": proof, "focused_tests": tests,
                 "full_pytest_executed": False,
                 "existing_source_modified_by_audit": False}
        save_json(output / "audit.json", audit)
        (output / "AUDIT_FINDINGS_JA.md").write_text(formatted_findings(proof, pre), encoding="utf-8")
        print("PHASE172_R1_PUBLIC_STATUS=" + str(proof["public_status"]), flush=True)
        print("PHASE172_R1_WEB_KEY=" + str(proof["web_key"]), flush=True)
        print("PHASE172_R1_OPEN_GOALS=" + str(proof["open_goals_count"]), flush=True)
        print("PHASE172_R1_REFERENCES=" + str(proof["reference_count"]), flush=True)
        print("PHASE172_R1_STEPS=" + str(proof["proven_step_count"]), flush=True)
        print("PHASE172_R1_REPORT=" + str(output), flush=True)
        if any(item["exit_code"] != 0 for item in tests):
            print("PHASE172_R1_RESULT=FOCUSED_PYTEST_FAILED", flush=True)
            return 1
        if pre["tracked_status_before"] != get_git_value("status", "--porcelain=v1", "--untracked-files=no"):
            print("PHASE172_R1_RESULT=TRACKED_WORKTREE_CHANGED", flush=True)
            return 1
        print("PHASE172_R1_SOURCE_CHANGES=0", flush=True)
        print("PHASE172_R1_RESULT=PASS_AUDIT_ONLY", flush=True)
        return 0
    except Exception as exc:
        print("PHASE172_R1_RESULT=FAILED", flush=True)
        print(f"PHASE172_R1_ERROR={type(exc).__name__}: {exc}", flush=True)
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## run.ps1（全文）

```powershell
param(
    [switch]$DryRun,
    [switch]$RunFocusedTests
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldLocation = (Get-Location).Path
$OldPythonPath = $env:PYTHONPATH
$OldPythonUtf8 = $env:PYTHONUTF8
$OldPythonEncoding = $env:PYTHONIOENCODING
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE
$OldNoCache = $env:PYTEST_ADDOPTS
try {
    Set-Location $Root
    $env:PYTHONPATH = "$Root;$OldPythonPath"
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_ADDOPTS = ''
    $PythonArguments = @('-B', '-m', 'phase172_r1_renderer_audit.audit')
    if ($DryRun) { $PythonArguments += '--dry-run' }
    if ($RunFocusedTests) { $PythonArguments += '--run-focused-tests' }
    & python @PythonArguments
    $ExitCode = $LASTEXITCODE
    if ($ExitCode -ne 0) { throw "Phase 172 R1 audit failed: exit $ExitCode" }
}
finally {
    Set-Location $OldLocation
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONUTF8 = $OldPythonUtf8
    $env:PYTHONIOENCODING = $OldPythonEncoding
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
    $env:PYTEST_ADDOPTS = $OldNoCache
}
```

## tests/test_audit.py（全文）

```python
"""Pure diagnosis tests; no production imports or search mocks."""
from __future__ import annotations

from phase172_r1_renderer_audit.audit import (
    display_categories,
    duplicate_inventory,
    math_fragments,
)


def test_two_different_provenance_lines_are_not_exact_duplicates():
    lines = [
        {"proof_body_line_number": 1, "printed_text": r"[R1]より, $E(\eta_{5})=\eta_{6}$."},
        {"proof_body_line_number": 2, "printed_text": r"[R2]より, $E(\eta_{5})=\eta_{6}$."},
    ]
    observed = duplicate_inventory(lines)
    assert observed["byte_identical_nonempty_lines"] == []
    assert observed["shared_tex_fragments"] == [
        {"latex": r"E(\eta_{5})=\eta_{6}", "line_numbers": [1, 2]},
    ]


def test_exact_repetition_is_reported_without_inference():
    lines = [
        {"proof_body_line_number": 1, "printed_text": "全射である."},
        {"proof_body_line_number": 3, "printed_text": "全射である."},
    ]
    observed = duplicate_inventory(lines)
    assert observed["byte_identical_nonempty_lines"] == [
        {"text": "全射である.", "line_numbers": [1, 3]},
    ]


def test_math_extractor_requires_closed_inline_formula():
    assert math_fragments(r"$E(\eta_{5})=\eta_{6}$. $x$") == (
        r"E(\eta_{5})=\eta_{6}",
    )


def test_categories_are_non_authoritative_observations():
    assert "SURJECTIVITY" in display_categories("H の全射性を証明した.")
    assert "INTERNAL_REFERENCE_TEXT" in display_categories("DB prior")
    assert "ETA_SUSPENSION" in display_categories(r"$E(\eta_{5})=\eta_{6}$.")
```

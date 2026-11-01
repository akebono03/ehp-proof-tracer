# Phase 173 R3 portable — 全コード

変更は新規追加のみ。以下は各ファイルの全文。

## __init__.py

```python
"""Phase 173 R3 read-only source and backward-route audit."""
```

## audit.py

```python
"""Review Phase 173 R3 root expansions without changing mathematical proofs.

Accept a descendant of the reviewed baseline only when every committed change
since that baseline is an added Phase 173 audit file, and the reviewed source
blobs remain identical. R1 history is optional across Windows profiles.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
from typing import Any

BASELINE = "11ea331f322883e2f2cf34b9e865dea2134f5058"
REVIEWED_BLOBS = {
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r52_r9_shared_math.py": "2718c55789af7f442ac2c086d016d3d6f7ca3133",
    "phase165_r52_r16_web_citation_gate.py": "d1138c0450f234b6da761902ed7358b6038a19c8",
    "phase166_r3t_goal_source_binding/goal_source.py": "e13a07bbc0b6494b0c3c9b891784fe7378448756",
    "phase169_r3m_prior_result_catalog/prior_results.py": "c522cbaf924b3a9aa500d453b8eb6a1a66c42611",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}
TARGETS = ((4, 3), (5, 3))


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, text=True, encoding="utf-8",
        capture_output=True, check=True,
    )
    return result.stdout.strip()


def verify_committed_changes(diff_text: str) -> tuple[str, ...]:
    """Accept only newly added files below Phase 173 audit directories."""
    paths = []
    for line in diff_text.splitlines():
        fields = line.split("\t")
        if len(fields) != 2:
            raise RuntimeError("Unrecognized Git name-status entry: " + repr(line))
        status, name = fields
        if status != "A" or not name.startswith("phase173_") or "/" not in name:
            raise RuntimeError("Reviewed production scope changed: " + repr(line))
        if ".." in Path(name).parts or "\\" in name:
            raise RuntimeError("Invalid audit path: " + repr(name))
        paths.append(name)
    return tuple(paths)


def preflight(root: Path) -> dict[str, Any]:
    """Validate lineage, reviewed content, publication source, and clean files."""
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R3 requires develop")
    head = git(root, "rev-parse", "HEAD")
    if git(root, "rev-parse", "origin/develop") != head:
        raise RuntimeError("Local HEAD is not origin/develop; inspect git status")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASELINE, head],
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("Reviewed baseline is not an ancestor of HEAD")
    changes = verify_committed_changes(
        git(root, "diff", "--name-status", "--no-renames", BASELINE, head)
    )
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("Tracked worktree must be clean")
    for name, sha in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + name) != sha:
            raise RuntimeError("Reviewed source content changed: " + name)
    source = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(
        encoding="utf-8-sig"
    )
    anchor = r"\begin{proposition}\label{prop:5.6}"
    begin = source.index(anchor)
    finish = source.index(r"\end{proposition}", begin)
    excerpt = source[begin:finish]
    for fragment in (r"\pi^{4}_{7}", r"\pi^{n}_{n+3}", r"\nu'"):
        if fragment not in excerpt:
            raise RuntimeError("Proposition 5.6 source text differs")
    return {"head": head, "reviewed_baseline": BASELINE,
            "committed_audit_additions": list(changes),
            "reviewed_source_blobs": dict(REVIEWED_BLOBS)}


def r1_baseline_status(local_appdata: Path) -> str:
    """Cross-check locally available R1 reports; absence is not a proof fact."""
    directory = local_appdata / "EHPProofTracerRecovery"
    reports = sorted(
        directory.glob("phase173_r1_*/audit.json"),
        key=lambda path: path.stat().st_mtime, reverse=True,
    ) if directory.is_dir() else []
    for path in reports:
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            continue
        rows = data.get("rows")
        if not isinstance(rows, list):
            continue
        observed = {(row.get("n"), row.get("k")): row for row in rows
                    if isinstance(row, dict)}
        if all(pair in observed for pair in TARGETS):
            for pair in TARGETS:
                if observed[pair].get("audit_result") != "PROOF_UNFINISHED":
                    raise RuntimeError("R1 local baseline disagrees: " + str(pair))
            return "MATCHED:" + str(path)
    return "NOT_AVAILABLE_IN_THIS_PROFILE"


def inspect_roots() -> list[dict[str, Any]]:
    """Inspect already registered proof proposals, never certify them."""
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase166_r3t_goal_source_binding.goal_source import (
        resolve_specialized_goal_citing_id,
    )
    from phase169_r3m_prior_result_catalog.prior_results import (
        resolve_prior_group_result,
    )
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    rows = []
    for n, k in TARGETS:
        goals = registered_group_goal_candidates(bridge, n=n, k=k)
        if len(goals) != 1:
            raise RuntimeError(f"n={n} k={k}: expected one typed goal, found {len(goals)}")
        goal = goals[0]
        citing = resolve_specialized_goal_citing_id(bridge, goal)
        if citing is None:
            raise RuntimeError(f"n={n} k={k}: source position missing")
        assertion = bridge.registry.assertion(citing)
        locator = bridge.registry.reference(assertion.reference_id).locator
        screened = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=citing,
            explicit_publication_target=True,
        )
        screened = prefer_universal_prop42_derivation(screened)
        given = tuple(
            link.step.conclusion for link in screened.proof_links
            if link.step is not None and link.step.rule is ProofRule.GIVEN
        )
        if any(type(statement) is type(goal) and statement == goal for statement in given):
            raise RuntimeError("Target was admitted as GIVEN")
        provider = shared_expansion_provider(screened, proof_target=goal)
        options = provider(goal)
        roots = []
        memo: list[object] = []
        for option in options:
            children = []
            for child in option.subgoals:
                item = {"type": type(child).__name__, "repr": repr(child)[:1600]}
                is_new = not any(type(old) is type(child) and old == child for old in memo)
                if is_new:
                    memo.append(child)
                    item["exact_screened_given"] = any(
                        type(source) is type(child) and source == child for source in given
                    )
                    try:
                        proposals = provider(child)
                        item["child_proposal_count"] = len(proposals)
                        item["child_proposal_rules"] = [p.rule.name for p in proposals]
                    except Exception as exc:
                        item["child_probe_error"] = type(exc).__name__ + ": " + str(exc)
                else:
                    item["duplicate_subgoal"] = True
                children.append(item)
            roots.append({"rule": option.rule.name, "children": children})
        prior = []
        for earlier_n in range(3, n):
            source = resolve_prior_group_result(
                screened, source_n=earlier_n, source_k=k,
                citing_assertion_id=citing,
            )
            prior.append({"n": earlier_n, "k": k, "eligible": source.eligible,
                          "reason": source.reason, "stable_source": earlier_n >= k + 2})
        rows.append({"n": n, "k": k, "source_locator": locator,
                     "citing_assertion_id": citing,
                     "screened_given_count": len(given),
                     "target_direct_given_count": 0,
                     "root_candidate_count": len(roots),
                     "roots": roots, "prior_sources": prior})
    return rows


def format_report(rows: list[dict[str, Any]]) -> str:
    output = ["PHASE173_R3_PORTABLE_FRONTIER=AUDIT_ONLY"]
    for row in rows:
        output.append("R3 n=%d k=%d locator=%s GIVEN=%d roots=%d" % (
            row["n"], row["k"], row["source_locator"],
            row["screened_given_count"], row["root_candidate_count"],
        ))
        for index, root in enumerate(row["roots"], start=1):
            output.append("  ROOT %d rule=%s" % (index, root["rule"]))
            for child in root["children"]:
                output.append("    SUBGOAL %s proposals=%s exact_given=%s" % (
                    child["type"], child.get("child_proposal_count", "DUPLICATE"),
                    child.get("exact_screened_given", "DUPLICATE"),
                ))
                for name in child.get("child_proposal_rules", []):
                    output.append("      CANDIDATE_RULE " + name)
                if "child_probe_error" in child:
                    output.append("      PROBE_ERROR " + child["child_probe_error"])
                output.append("      STATEMENT " + child["repr"][:650])
        for prior in row["prior_sources"]:
            output.append("  PRIOR n=%d eligible=%s reason=%s" % (
                prior["n"], prior["eligible"], prior["reason"],
            ))
    output.append("PHASE173_R3_PORTABLE_FRONTIER=PASS")
    output.append("OBSERVATION_IS_NOT_A_PROOF=True")
    return "\n".join(output)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only R3 source and root audit")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    state = preflight(root)
    print("PHASE173_R3_HEAD_REVIEW=PASS")
    print("PHASE173_R3_REVIEWED_SOURCE_BLOBS=PASS")
    print("PHASE173_R3_CURRENT_HEAD=" + state["head"])
    if args.dry_run:
        print("PHASE173_R3_DRY_RUN=PASS")
        return 0
    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        raise RuntimeError("LOCALAPPDATA not set")
    baseline_state = r1_baseline_status(Path(local_appdata))
    print("PHASE173_R3_R1_LOCAL_BASELINE=" + baseline_state)
    rows = inspect_roots()
    report = {"phase": "173-R3", "mode": "AUDIT_ONLY",
              "observations_are_not_proofs": True,
              "r1_local_baseline": baseline_state, **state, "rows": rows}
    out = Path(local_appdata) / "EHPProofTracerRecovery" / "phase173_r3_portable"
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "audit.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
    markdown = format_report(rows)
    (out / "audit.md").write_text(markdown + "\n", encoding="utf-8")
    print(markdown)
    print("PHASE173_R3_REPORT=" + str(json_path))
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("Tracked files changed during R3")
    print("PHASE173_R3_TRACKED_UNCHANGED=True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$env:PYTHONPATH = $Root
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
Write-Output 'PHASE173_R3_PORTABLE_FOCUSED_PYTEST_START'
python -B -m pytest -q -p no:cacheprovider '.\phase173_r3_portable\tests\test_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'Phase 173 R3 focused pytest failed' }
Write-Output 'PHASE173_R3_PORTABLE_FOCUSED_PYTEST=PASS'
if ($DryRun) {
    python -B -m phase173_r3_portable.audit --dry-run
} else {
    python -B -m phase173_r3_portable.audit
}
if ($LASTEXITCODE -ne 0) { throw 'Phase 173 R3 audit failed' }
git status -sb
```

## tests/test_audit.py

```python
"""Offline tests for Phase 173 R3 portable, read-only report inspection."""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_r3_portable import audit


def test_added_phase173_paths_are_allowed() -> None:
    assert audit.verify_committed_changes(
        "A\tphase173_r1_nge3_audit/audit.py\n"
        "A\tphase173_r3_head_guard_fix/audit.py\n"
    ) == ("phase173_r1_nge3_audit/audit.py", "phase173_r3_head_guard_fix/audit.py")


@pytest.mark.parametrize("entry", [
    "M\tphase165_r52_r9_shared_math.py",
    "A\tsources/toda/new.tex",
    "D\tphase173_r1_nge3_audit/audit.py",
    "R100\tphase173_r1_nge3_audit/old.py\tphase173_r1_nge3_audit/new.py",
    "A\tdocs/development_log.md",
    "A\tphase173_invalid/../bad.py",
])
def test_other_changes_are_rejected(entry: str) -> None:
    with pytest.raises(RuntimeError):
        audit.verify_committed_changes(entry)


def test_preflight_accepts_new_head_with_only_reviewed_additions(monkeypatch, tmp_path: Path) -> None:
    source = tmp_path / "sources" / "toda" / "Toda_05_2.tex"
    source.parent.mkdir(parents=True)
    source.write_text(
        r"\begin{proposition}\label{prop:5.6}\pi^{4}_{7}\pi^{n}_{n+3}\nu'\end{proposition}",
        encoding="utf-8",
    )
    current = "new-head"
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args in (("rev-parse", "HEAD"), ("rev-parse", "origin/develop")):
            return current
        if args[:3] == ("diff", "--name-status", "--no-renames"):
            return "A\tphase173_r1_nge3_audit/audit.py"
        if args == ("status", "--porcelain", "--untracked-files=no"):
            return ""
        if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return audit.REVIEWED_BLOBS[args[1][5:]]
        raise AssertionError(args)
    monkeypatch.setattr(audit, "git", fake_git)
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0))
    result = audit.preflight(tmp_path)
    assert result["head"] == current
    assert len(result["reviewed_source_blobs"]) == 6


def test_preflight_rejects_changed_reviewed_blob(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "git", lambda root, *args: (
        "bad" if args[0] == "rev-parse" and args[1].startswith("HEAD:")
        else "develop" if args[0] == "branch"
        else "head" if args[0] == "rev-parse"
        else ""
    ))
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0))
    with pytest.raises(RuntimeError, match="Reviewed source content changed"):
        audit.preflight(tmp_path)


def test_missing_r1_profile_is_not_fabricated(tmp_path: Path) -> None:
    assert audit.r1_baseline_status(tmp_path) == "NOT_AVAILABLE_IN_THIS_PROFILE"


def test_valid_r1_baseline_detected(tmp_path: Path) -> None:
    directory = tmp_path / "EHPProofTracerRecovery" / "phase173_r1_example"
    directory.mkdir(parents=True)
    (directory / "audit.json").write_text(json.dumps({"rows": [
        {"n": n, "k": k, "audit_result": "PROOF_UNFINISHED"}
        for n, k in audit.TARGETS
    ]}), encoding="utf-8")
    assert audit.r1_baseline_status(tmp_path).startswith("MATCHED:")


def test_inconsistent_r1_baseline_is_rejected(tmp_path: Path) -> None:
    directory = tmp_path / "EHPProofTracerRecovery" / "phase173_r1_example"
    directory.mkdir(parents=True)
    (directory / "audit.json").write_text(json.dumps({"rows": [
        {"n": 4, "k": 3, "audit_result": "COMPLETE_AND_WEB_VERIFIED"},
        {"n": 5, "k": 3, "audit_result": "PROOF_UNFINISHED"},
    ]}), encoding="utf-8")
    with pytest.raises(RuntimeError, match="disagrees"):
        audit.r1_baseline_status(tmp_path)


def test_format_reports_roots_and_subgoals() -> None:
    rows = [{"n": 4, "k": 3, "source_locator": "Proposition 5.6",
             "screened_given_count": 26, "root_candidate_count": 1,
             "roots": [{"rule": "mock source rule", "children": [{
                 "type": "Relation", "repr": "target", "child_proposal_count": 0,
                 "exact_screened_given": False, "child_proposal_rules": [],
             }]}], "prior_sources": [
                 {"n": 3, "eligible": True, "reason": "prior_fixed_source"}
             ]}]
    output = audit.format_report(rows)
    assert "ROOT 1" in output
    assert "SUBGOAL Relation proposals=0 exact_given=False" in output
    assert "PRIOR n=3 eligible=True" in output
    assert "OBSERVATION_IS_NOT_A_PROOF=True" in output


def test_duplicate_goal_is_not_probed() -> None:
    text = audit.format_report([{"n": 5, "k": 3,
        "source_locator": "Proposition 5.6", "screened_given_count": 27,
        "root_candidate_count": 1, "roots": [{"rule": "r", "children": [
            {"type": "Relation", "repr": "test", "duplicate_subgoal": True}
        ]}], "prior_sources": []}])
    assert "proposals=DUPLICATE" in text
```

## README.md

```markdown
# Phase 173 R3: Portable Read-Only Audit

This package audits the typed root proposals of the two priority groups without changing production source code or promoting registered DB goals to proofs.

It addresses two previous execution failures: a hard-coded Git commit guard and the R1 audit path belonging to another Windows user profile.

From the repository root, unpack the ZIP and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r3_portable\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r3_portable\run.ps1'
```

The run checks the reviewed baseline lineage and exact source blob hashes. Only newly added files under `phase173_*` may have been committed since the baseline. If production source files have been modified, the audit refuses to run until those changes are reviewed.

Reports are written to `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_r3_portable`. A missing local R1 report is explicitly marked as unavailable, not silently treated as evidence. The full pytest suite is not run.
```

## AUDIT_PLAN_JA.md

```markdown
# Phase 173 R3 — プロファイル・コミット変動への対応

## 対象

- 新規 `phase173_r3_portable/__init__.py`
- 新規 `phase173_r3_portable/audit.py`：`git`, `verify_committed_changes`, `preflight`, `r1_baseline_status`, `inspect_roots`, `format_report`, `main` の全関数
- 新規 `phase173_r3_portable/run.ps1`
- 新規 `phase173_r3_portable/tests/test_audit.py`
- 新規 `phase173_r3_portable/README.md`, `CODE_FULL_JA.md`, この文書

既存の本番コード、既存テスト、五つの正式ドキュメントは変更しない。

## 検査方法

- `develop` かつローカル `origin/develop` と HEAD が一致し、追跡済みファイルがクリーンである。
- `11ea331f` が HEAD の祖先で、基準以後のコミット差分は `phase173_*` 内の**新規追加**だけである。既存ファイルの変更・削除は禁止する。
- 重要な六つの source blob が GitHub でレビューした SHA と一致する。
- Toda Proposition 5.6 の原文が確認できる。
- R1 レポートが現在の Windows プロファイルにない場合、`NOT_AVAILABLE_IN_THIS_PROFILE` として報告し、過去の成功結果を捏造しない。
- 公開の検索器と同一の screened context を用い、根の候補・直下 Subgoal の候補だけを調査する。型付き候補を ProofStep とみなさない。

## 完了条件

- `run.ps1 -DryRun` と限定 pytest が PASS。
- 本実行が二群の候補、既存 GIVEN、先行結果を出力。
- `%LOCALAPPDATA%/EHPProofTracerRecovery/phase173_r3_portable/audit.json` と `audit.md` を出力。
- tracked files 不変、全体 pytest 未実行。

Phase 173 R4 は本レポートの診断後に検討する。新しい数学的規則・GIVEN の追加は本パッケージで実施しない。
```


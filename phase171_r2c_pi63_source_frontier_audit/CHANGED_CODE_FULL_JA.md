# Phase 171 R2C — 変更・新規コード全文（省略なし）

## 変更対象

既存ファイル・既存 API・既存クラス・既存テストは変更しない。以下をリポジトリ直下の `phase171_r2c_pi63_source_frontier_audit/` に新規追加する。

`audit.py`（全 import・全関数）、`run.ps1`、`__init__.py`、`tests/test_audit.py`（全 import・全テスト・テスト用クラス）、`README.md`（英語全文）、`監査仕様.md`（日本語全文）。

## 対象となる全関数

`git`, `tracked_state`, `validate_r2b`, `locator_inventory`, `summarize_pi63`, `markdown_report`, `run`, `main`。

## 追加位置

全ファイルは新規パッケージ配下に、ZIP の相対パスどおり追加する。既存ファイル内の挿入は行わない。

## 限定 pytest・完了条件・次段階との境界

`python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider phase171_r2c_pi63_source_frontier_audit/tests/test_audit.py` を実行する。全体 pytest は Phase 171 の終了時のみ。

DryRun と通常監査が PASS、出典別集計と `PHASE171_R2C_TRACKED_UNCHANGED=True` が出力されること。未検証候補や DB Goal を証明済みに変更する行為はこの Phase に含めない。

---
## `audit.py` — 全文

```python
"""Phase 171 R2C: read-only audit of existing typed premises for pi_6^3.

Never promotes candidate literature statements into ProofSteps, modifies a
proof registry, or equates differently typed generator expressions.
"""
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
    "phase171_r2c_pi63_source_frontier_audit/",
)
EXPECTED_BLOBS = {
    "phase165_r52_r9_shared_math.py": "0ff831522b59f88ff3ed3892f35e5e048be850e1",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r6_explicit_literature_inputs.py": "c430eb4acee83eaa6338dab9834d46808fac0ad4",
    "phase169_r3h_source_registry.py": "1829e3ac1381e10270dac73a196bfd4983540ea4",
    "phase163_r4_r11_literature_registration.py": "2f3a42173f6482167c364e9ff28621b3bcb62792",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}
LOCATORS = (
    "(5.3)", "Proposition 5.3", "Proposition 2.2", "(4.4)",
    "Proposition 5.6", "(5.6)",
)
TARGET_N = 3
TARGET_K = 3


def git(root: Path, *args: str) -> str:
    """Execute a read-only Git command with explicit failure handling."""
    proc = subprocess.run(["git", *args], cwd=root, capture_output=True, check=False)
    if proc.returncode:
        raise RuntimeError(
            "git " + " ".join(args) + ": " + proc.stderr.decode("utf-8", "replace").strip()
        )
    return proc.stdout.decode("utf-8", "replace").strip()


def tracked_state(root: Path) -> dict:
    """Allow only audited-path commits ahead of upstream and unchanged source blobs."""
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    upstream_ref = "refs/remotes/origin/develop"
    upstream = git(root, "rev-parse", "--verify", upstream_ref)
    if branch != "develop":
        raise RuntimeError("expected develop branch")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked files are modified")
    git(root, "merge-base", "--is-ancestor", BASELINE, "HEAD")
    try:
        git(root, "merge-base", "--is-ancestor", upstream_ref, "HEAD")
    except RuntimeError as exc:
        raise RuntimeError("origin/develop is behind local HEAD or has diverged") from exc
    committed = git(root, "diff", "--name-only", "-z", BASELINE, "HEAD")
    changed = tuple(path for path in committed.split("\0") if path)
    unknown = tuple(path for path in changed
                    if not any(path.startswith(prefix) for prefix in REVIEWED_DIRECTORIES))
    if unknown:
        raise RuntimeError("non-audit committed changes: " + ", ".join(unknown))
    for path, digest in EXPECTED_BLOBS.items():
        if digest and git(root, "rev-parse", "HEAD:" + path) != digest:
            raise RuntimeError("source blob changed: " + path)
    diff = subprocess.run(["git", "diff", "--binary", "HEAD", "--"],
                          cwd=root, capture_output=True, check=False)
    if diff.returncode:
        raise RuntimeError("cannot inspect tracked binary diff")
    return {
        "branch": branch, "head": head, "origin_develop": upstream,
        "baseline": BASELINE, "reviewed_changes": list(changed),
        "tracked_diff_sha256": sha256(diff.stdout).hexdigest(),
    }


def validate_r2b(report: object) -> dict:
    """Require exactly the saved, successful three-gap R2B scope and provenance."""
    if not isinstance(report, dict) or report.get("phase") != "171 R2B":
        raise ValueError("R2B report required")
    if report.get("read_only") is not True:
        raise ValueError("R2B must be read-only")
    cases = report.get("cases")
    if not isinstance(cases, list) or len(cases) != 3:
        raise ValueError("R2B must contain exactly three cases")
    for expected_n, case in zip((3, 4, 5), cases):
        if not isinstance(case, dict) or case.get("n") != expected_n or case.get("proof_link_count") != 0:
            raise ValueError("R2B gap case or proof-link state differs")
        if case.get("blockers") != ["TYPED_GOAL_MISMATCH", "NO_VERIFIED_PROOF_LINK"]:
            raise ValueError("R2B blocker inventory differs")
    source = report.get("source")
    if not isinstance(source, dict) or not source.get("has_question_marker"):
        raise ValueError("R2B unresolved source reference is missing")
    if "(5.3)" not in source.get("references_in_proof", []):
        raise ValueError("R2B source proof lacks (5.3)")
    return cases[0]


def locator_inventory(bridge: object, *, locators: tuple[str, ...] = LOCATORS) -> list[dict]:
    """Inspect exact registered source provenance; a candidate is not a proof."""
    registry = bridge.registry
    assertions = tuple(registry._assertions.values())
    links = tuple(bridge.proof_links)
    items = []
    for locator in locators:
        matches = []
        for assertion in assertions:
            reference = registry.reference(assertion.reference_id)
            if reference.locator != locator:
                continue
            associated = tuple(link for link in links if link.assertion_id == assertion.assertion_id)
            exact_given = sum(
                link.step is not None
                and getattr(getattr(link.step, "rule", None), "name", None) == "GIVEN"
                and getattr(assertion.origin, "value", None) == "fixed_statement"
                and link.step.conclusion == assertion.content
                for link in associated
            )
            matches.append({
                "assertion_id": assertion.assertion_id,
                "origin": getattr(assertion.origin, "value", str(assertion.origin)),
                "statement_type": type(assertion.content).__name__,
                "statement_repr": repr(assertion.content)[:1500],
                "link_count": len(associated),
                "matching_given_count": exact_given,
                "scope_repr": repr(getattr(assertion, "scope", None))[:350],
            })
        items.append({"locator": locator, "assertion_count": len(matches),
                      "matching_given_total": sum(m["matching_given_count"] for m in matches),
                      "assertions": matches})
    return items


def summarize_pi63(bridge: object, goal: object, inventory: list[dict]) -> dict:
    """Compare registered target and citation provenance without making a derivation."""
    target_id = "shared:0:boundary:Proposition 5.6:pi6_3_group_relation"
    candidate = bridge.registry._assertions.get(target_id)
    if candidate is None:
        raise ValueError("Proposition 5.6 pi6_3 candidate absent")
    links = tuple(link for link in bridge.proof_links if link.assertion_id == target_id)
    if links:
        raise ValueError("Proposition 5.6 target unexpectedly has proof links")
    source53 = next(item for item in inventory if item["locator"] == "(5.3)")
    adopted_hopf = [entry for entry in source53["assertions"]
                    if "nu_prime_hopf_relation" in entry["assertion_id"]]
    return {
        "target": "pi_6^3", "goal_repr": repr(goal)[:2300],
        "candidate_repr": repr(candidate.content)[:2300],
        "typed_equal": type(goal) is type(candidate.content) and goal == candidate.content,
        "candidate_link_count": len(links),
        "toda53_hopf_assertion_count": len(adopted_hopf),
        "toda53_hopf_link_count": sum(item["matching_given_count"] for item in adopted_hopf),
        "toda53_hopf_assertions": adopted_hopf,
        "not_established": [
            "Equality of the DB generator and the literature generator",
            "Verified derivation of the target cyclic group structure",
            "Evidence chain for the order-four relation and generator property",
        ],
    }


def markdown_report(payload: dict) -> str:
    """Document observed and unproved facts without TeX tables."""
    summary = payload["pi63"]
    lines = [
        "# Phase 171 R2C — π₆³ の型付き前提監査", "",
        "R2B が確定した型付き不一致と証明リンク欠落を前提に、現行台帳の出典と型付き命題を監査した。", "",
        "この監査は証明木を変更せず、文献候補を GIVEN に昇格させない。", "",
        "## π₆³ の状態", "",
        f"DB Goal と Proposition 5.6 候補の完全一致：{summary['typed_equal']}。", "",
        f"Proposition 5.6 結論の ProofStep リンク：{summary['candidate_link_count']}件。", "",
        f"(5.3) Hopf 関係の候補：{summary['toda53_hopf_assertion_count']}件。", "",
        f"同関係の照合可能な GIVEN：{summary['toda53_hopf_link_count']}件。", "",
        "## 文献位置別の監査", "",
    ]
    for item in payload["inventory"]:
        lines.append(f"{item['locator']}：登録{item['assertion_count']}件、照合可能な GIVEN {item['matching_given_total']}件。")
        for statement in item["assertions"][:12]:
            lines.append("  - " + statement["assertion_id"] + "（" + statement["origin"] + "）")
    lines.extend([
        "", "## 次の実装との境界", "",
        "(5.3) の Hopf 関係が登録済みであっても、その事実だけでは ν′ の位数や群構造は証明されない。", "",
        "出典を確認できない (5.6)? は採用しない。π₇⁴、π₈⁵ の構成は本監査に含めない。", "",
    ])
    return "\n".join(lines)


def run(root: Path, report_path: Path, *, dry_run: bool) -> int:
    """Validate saved evidence and inspect the real typed registry read-only."""
    before = tracked_state(root)
    report = json.loads(report_path.read_text(encoding="utf-8-sig"))
    validate_r2b(report)
    print("PHASE171_R2C_MODE=READ_ONLY_PI63_FRONTIER", flush=True)
    print("PHASE171_R2C_TARGET=3,3", flush=True)
    if dry_run:
        after = tracked_state(root)
        if before != after:
            raise RuntimeError("Git state changed during DryRun")
        print("PHASE171_R2C_DRY_RUN=PASS", flush=True)
        print("PHASE171_R2C_TRACKED_UNCHANGED=True", flush=True)
        print("PHASE171_R2C_RESULT=PASS", flush=True)
        return 0

    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import registered_group_goal_candidates

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=TARGET_N, k=TARGET_K)
    if len(goals) != 1:
        raise RuntimeError("expected one registered typed pi_6^3 Goal")
    inventory = locator_inventory(bridge)
    summary = summarize_pi63(bridge, goals[0], inventory)
    output = {
        "phase": "171 R2C", "mode": "READ_ONLY_PI63_FRONTIER", "read_only": True,
        "source_report": str(report_path), "git": before,
        "pi63": summary, "inventory": inventory,
    }
    for item in inventory:
        print("PHASE171_R2C_SOURCE=" + json.dumps({
            "locator": item["locator"], "assertion_count": item["assertion_count"],
            "matching_given_total": item["matching_given_total"],
        }, ensure_ascii=False), flush=True)
    print("PHASE171_R2C_DETAIL=" + json.dumps({
        "n": 3, "k": 3, "typed_equal": summary["typed_equal"],
        "candidate_link_count": summary["candidate_link_count"],
        "toda53_hopf_assertion_count": summary["toda53_hopf_assertion_count"],
        "toda53_hopf_link_count": summary["toda53_hopf_link_count"],
    }, ensure_ascii=False), flush=True)
    after = tracked_state(root)
    if before != after:
        raise RuntimeError("Git state changed during audit")
    output["tracked_unchanged"] = True
    base = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    directory = base / ("phase171_r2c_pi63_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    directory.mkdir(parents=True, exist_ok=False)
    path = directory / "frontier.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    (directory / "frontier.md").write_text(markdown_report(output), encoding="utf-8")
    print("PHASE171_R2C_REPORT=" + str(path), flush=True)
    print("PHASE171_R2C_TRACKED_UNCHANGED=True", flush=True)
    print("PHASE171_R2C_RESULT=PASS", flush=True)
    return 0


def main() -> int:
    """Provide a safe CLI for Windows PowerShell module execution."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        return run(args.root.resolve(), args.report.resolve(), dry_run=args.dry_run)
    except Exception as exc:
        print("PHASE171_R2C_ERROR=" + f"{type(exc).__name__}: {exc}", flush=True)
        print(traceback.format_exc()[-2400:], file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1` — 全文

```powershell
param(
    [Parameter(Mandatory = $true)]
    [string] $ReportPath,
    [switch] $DryRun
)
$ErrorActionPreference = 'Stop'
$packageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = (Resolve-Path (Join-Path $packageRoot '..')).Path
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location $repoRoot
try {
    python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider phase171_r2c_pi63_source_frontier_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw "PHASE171_R2C_FOCUSED_PYTEST_EXIT=$LASTEXITCODE" }
    Write-Host 'PHASE171_R2C_FOCUSED_PYTEST=PASS'
    $arguments = @('-B', '-m', 'phase171_r2c_pi63_source_frontier_audit.audit', '--root', $repoRoot, '--report', $ReportPath)
    if ($DryRun.IsPresent) { $arguments += '--dry-run' }
    & python @arguments
    if ($LASTEXITCODE -ne 0) { throw "PHASE171_R2C_AUDIT_EXIT=$LASTEXITCODE" }
    Write-Host 'PHASE171_R2C=PASS'
}
finally {
    Pop-Location
}
```

## `__init__.py` — 全文

```python
"""Phase 171 R2C read-only source-frontier audit."""
```

## `tests/test_audit.py` — 全文

```python
"""Focused R2C source-frontier and trust-boundary regression tests."""
from __future__ import annotations

from enum import Enum
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace

import pytest

from phase171_r2c_pi63_source_frontier_audit import audit


class Origin(Enum):
    FIXED_STATEMENT = "fixed_statement"


class Rule(Enum):
    GIVEN = "given"


def example_r2b() -> dict:
    return {
        "phase": "171 R2B", "read_only": True,
        "cases": [{
            "n": n, "proof_link_count": 0,
            "blockers": ["TYPED_GOAL_MISMATCH", "NO_VERIFIED_PROOF_LINK"],
        } for n in (3, 4, 5)],
        "source": {"has_question_marker": True,
                   "references_in_proof": ["(5.3)", "(5.6)"]},
    }


def fake_registry():
    hopf = SimpleNamespace(
        assertion_id="shared:9:toda:adopted:eq5.3:nu_prime_hopf_relation",
        reference_id="h", content=("H(nu')", "eta5"),
        origin=Origin.FIXED_STATEMENT, scope=None,
    )
    proposition = SimpleNamespace(
        assertion_id="shared:0:boundary:Proposition 5.6:pi6_3_group_relation",
        reference_id="p", content=("pi63", "Z4:literature"),
        origin=Origin.FIXED_STATEMENT, scope=None,
    )
    match_step = SimpleNamespace(rule=Rule.GIVEN, conclusion=hopf.content)
    link = SimpleNamespace(assertion_id=hopf.assertion_id, step=match_step)
    entries = {"h": SimpleNamespace(locator="(5.3)"),
               "p": SimpleNamespace(locator="Proposition 5.6")}
    registry = SimpleNamespace(
        _assertions={hopf.assertion_id: hopf, proposition.assertion_id: proposition},
        reference=lambda key: entries[key],
    )
    bridge = SimpleNamespace(registry=registry, proof_links=(link,))
    return bridge


def test_r2b_accepts_expected_scope():
    assert audit.validate_r2b(example_r2b())["n"] == 3


def test_r2b_rejects_wrong_phase():
    report = example_r2b()
    report["phase"] = "171 R2A"
    with pytest.raises(ValueError, match="R2B"):
        audit.validate_r2b(report)


def test_r2b_rejects_wrong_number_of_cases():
    report = example_r2b()
    report["cases"] = report["cases"][:2]
    with pytest.raises(ValueError, match="three"):
        audit.validate_r2b(report)


def test_r2b_rejects_nonzero_proof_links():
    report = example_r2b()
    report["cases"][0]["proof_link_count"] = 1
    with pytest.raises(ValueError, match="gap case"):
        audit.validate_r2b(report)


def test_r2b_rejects_missing_uncertainty_marker():
    report = example_r2b()
    report["source"]["has_question_marker"] = False
    with pytest.raises(ValueError, match="unresolved"):
        audit.validate_r2b(report)


def test_r2b_rejects_unreviewed_dependency_list():
    report = example_r2b()
    report["source"]["references_in_proof"] = []
    with pytest.raises(ValueError, match="lacks"):
        audit.validate_r2b(report)


def test_locator_inventory_counts_only_matching_verified_given():
    bridge = fake_registry()
    inventory = audit.locator_inventory(bridge)
    hopf = next(x for x in inventory if x["locator"] == "(5.3)")
    prop = next(x for x in inventory if x["locator"] == "Proposition 5.6")
    assert hopf["assertion_count"] == 1
    assert hopf["matching_given_total"] == 1
    assert prop["assertion_count"] == 1
    assert prop["matching_given_total"] == 0


def test_locator_inventory_rejects_mismatched_given_conclusion():
    bridge = fake_registry()
    bridge.proof_links[0].step.conclusion = "unrelated"
    row = next(x for x in audit.locator_inventory(bridge) if x["locator"] == "(5.3)")
    assert row["matching_given_total"] == 0


def test_locator_inventory_rejects_inference_as_given():
    bridge = fake_registry()
    bridge.proof_links[0].step.rule = SimpleNamespace(name="INFERENCE")
    row = next(x for x in audit.locator_inventory(bridge) if x["locator"] == "(5.3)")
    assert row["matching_given_total"] == 0


def test_pi63_summary_never_equates_goal_and_candidate():
    bridge = fake_registry()
    inventory = audit.locator_inventory(bridge)
    output = audit.summarize_pi63(bridge, ("pi63", "Z4:DB"), inventory)
    assert output["typed_equal"] is False
    assert output["candidate_link_count"] == 0
    assert output["toda53_hopf_assertion_count"] == 1
    assert output["toda53_hopf_link_count"] == 1


def test_pi63_summary_refuses_target_proof_link():
    bridge = fake_registry()
    bridge.proof_links += (SimpleNamespace(
        assertion_id="shared:0:boundary:Proposition 5.6:pi6_3_group_relation",
        step=None,
    ),)
    with pytest.raises(ValueError, match="proof links"):
        audit.summarize_pi63(bridge, object(), audit.locator_inventory(bridge))


def test_markdown_does_not_claim_proof():
    bridge = fake_registry()
    inventory = audit.locator_inventory(bridge)
    output = audit.markdown_report({
        "inventory": inventory,
        "pi63": audit.summarize_pi63(bridge, ("pi63", "Z4:DB"), inventory),
    })
    assert "GIVEN に昇格させない" in output
    assert "(5.6)?" in output
    assert "ProofStep リンク：0件" in output


def test_git_guard_rejects_changed_production(monkeypatch, tmp_path):
    def fake(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("diff", "--name-only", "-z", audit.BASELINE, "HEAD"):
            return "phase165_r52_r9_shared_math.py\0"
        return ""
    monkeypatch.setattr(audit, "git", fake)
    with pytest.raises(RuntimeError, match="non-audit"):
        audit.tracked_state(tmp_path)


def test_git_guard_rejects_tracked_diff(monkeypatch, tmp_path):
    def fake(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("status", "--porcelain", "--untracked-files=no"):
            return " M data/sphere.csv"
        return ""
    monkeypatch.setattr(audit, "git", fake)
    with pytest.raises(RuntimeError, match="modified"):
        audit.tracked_state(tmp_path)


def test_git_guard_allows_ahead_audit_only_commit(monkeypatch, tmp_path):
    def fake(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "local-head"
        if args == ("rev-parse", "--verify", "refs/remotes/origin/develop"):
            return "remote-base"
        if args == ("diff", "--name-only", "-z", audit.BASELINE, "HEAD"):
            return "phase171_r2b_prop56_source_dependency_audit/audit.py\0"
        if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return audit.EXPECTED_BLOBS[args[1][5:]]
        return ""
    monkeypatch.setattr(audit, "git", fake)
    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kw: SimpleNamespace(
        returncode=0, stdout=b"", stderr=b"",
    ))
    output = audit.tracked_state(tmp_path)
    assert output["head"] == "local-head"
    assert output["origin_develop"] == "remote-base"


def test_git_guard_rejects_diverged_upstream(monkeypatch, tmp_path):
    def fake(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("merge-base", "--is-ancestor", "refs/remotes/origin/develop", "HEAD"):
            raise RuntimeError("not an ancestor")
        return ""
    monkeypatch.setattr(audit, "git", fake)
    with pytest.raises(RuntimeError, match="diverged"):
        audit.tracked_state(tmp_path)


def test_run_dry_run_does_not_import_production(monkeypatch, tmp_path, capsys):
    report_path = tmp_path / "r2b.json"
    report_path.write_text(json.dumps(example_r2b()), encoding="utf-8")
    monkeypatch.setattr(audit, "tracked_state", lambda root: {"head": "fixed"})
    assert audit.run(tmp_path, report_path, dry_run=True) == 0
    text = capsys.readouterr().out
    assert "PHASE171_R2C_DRY_RUN=PASS" in text
    assert "PHASE171_R2C_RESULT=PASS" in text


def test_module_entrypoint_works_with_sibling_module(tmp_path):
    root = tmp_path / "isolated"
    (root / "package").mkdir(parents=True)
    (root / "package" / "__init__.py").write_text("", encoding="utf-8")
    (root / "sibling.py").write_text("VALUE = 11\n", encoding="utf-8")
    (root / "package" / "run.py").write_text(
        "from sibling import VALUE\nprint(VALUE)\n", encoding="utf-8",
    )
    import sys
    result = subprocess.run(
        [sys.executable, "-B", "-m", "package.run"], cwd=root,
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "11"


def test_locator_inventory_does_not_adopt_nonfixed_statement():
    bridge = fake_registry()
    assertion = next(item for item in bridge.registry._assertions.values()
                     if item.reference_id == "h")
    assertion.origin = SimpleNamespace(value="source_archive")
    row = next(x for x in audit.locator_inventory(bridge) if x["locator"] == "(5.3)")
    assert row["matching_given_total"] == 0


def test_run_normal_records_read_only_inventory(monkeypatch, tmp_path, capsys):
    import sys
    import types

    report_path = tmp_path / "r2b.json"
    report_path.write_text(json.dumps(example_r2b()), encoding="utf-8")
    bridge = fake_registry()
    maths = types.ModuleType("phase165_r52_r9_shared_math")
    maths.build_shared_typed_bridge = lambda: bridge
    goals = types.ModuleType("phase165_r55_nk_only_goal")
    goals.registered_group_goal_candidates = lambda bridge, n, k: (("pi63", "DB"),)
    monkeypatch.setitem(sys.modules, maths.__name__, maths)
    monkeypatch.setitem(sys.modules, goals.__name__, goals)
    monkeypatch.setattr(audit, "tracked_state", lambda root: {"head": "fixed"})
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))

    assert audit.run(tmp_path, report_path, dry_run=False) == 0
    output = capsys.readouterr().out
    assert "PHASE171_R2C_DETAIL=" in output
    assert "PHASE171_R2C_TRACKED_UNCHANGED=True" in output
    report = list((tmp_path / "EHPProofTracerRecovery").glob("*/frontier.json"))
    assert len(report) == 1
    payload = json.loads(report[0].read_text(encoding="utf-8"))
    assert payload["pi63"]["typed_equal"] is False
    assert payload["pi63"]["toda53_hopf_link_count"] == 1
    assert payload["tracked_unchanged"] is True
```

## `README.md` — 全文

```markdown
# Phase 171 R2C: pi_6^3 source-frontier audit

This read-only package inspects current, typed literature assertions relevant to the unresolved 3-stem goal pi_6^3. It starts from the completed R2B report, examines the actual shared statement registry and source-linked `GIVEN` steps, and **does not create proofs, alter application code, equate generator aliases, or certify Toda Proposition 5.6**.

Run from the repository root with Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2C.zip" -DestinationPath "." -Force
$Report = Join-Path $env:LOCALAPPDATA "EHPProofTracerRecovery\phase171_r2b_prop56_20261029_073131_311779\dependency.json"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2c_pi63_source_frontier_audit\run.ps1" -ReportPath $Report -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2c_pi63_source_frontier_audit\run.ps1" -ReportPath $Report
git status -sb
```

The dry run checks the R2B report and Git safety boundary. The normal run imports the existing registry through `python -m`, inventories exact literature locators, and reports source assertions and their actual links. Artifacts are saved under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2c_pi63_*` as `frontier.json` and `frontier.md`.

A `matching_given_count` means only that a source-linked `GIVEN` matches its registered assertion. It **does not** establish the target group theorem, the printed source's edition, or correctness of a new inference. The original text's uncertain `(5.6)?` reference remains unverified. Only focused tests run; no entire-suite test is performed.
```

## `監査仕様.md` — 全文

```markdown
# Phase 171 R2C — π₆³ の型付き前提監査

## 目的

R2B で未完成の三群に、生成元の厳密な型付き不一致と証明リンク欠落が確認された。R2C は最初の π₆³ に限定し、既存の出典登録の状態を明らかにする。

## 監査する範囲

既存の R2B 結果、`build_shared_typed_bridge()` の登録済み命題、各命題の `ProofStepLink`、(5.3) Hopf 関係、Proposition 5.3、Proposition 2.2、EHP 完全列 (4.4)、Proposition 5.6 の候補を確認する。文献のラベルは既存台帳の `locator` に厳密一致した場合のみ集計する。

(5.3) の Hopf 等式の登録は、同じ出典中の他の等式まで登録済みであることを意味しない。また `GIVEN` は登録先の出典に紐づく証拠であり、群構造の完成証明ではない。DB Goal と Proposition 5.6 の型付き生成元を勝手に同一視しない。

## Git 安全性

基準コミットから、確認済みの Phase 171 監査用ディレクトリの追加以外を拒否する。`origin/develop` が HEAD の祖先であること、追跡ファイルが未変更であること、所定の production ソースの blob が同一であることを必須とする。Git の checkout、reset、push は実行しない。

## 完了条件・次段階との境界

限定 pytest 成功、DryRun 成功、π₆³ の出典別の登録件数と照合可能な GIVEN 件数の出力、Git 追跡ファイルの非変更が条件。Phase 171 の完成条件とは区別する。次の段階で不足する証明規則・原典照合とその順序を検討し、未検証の文献候補を証明済みにしない。
```


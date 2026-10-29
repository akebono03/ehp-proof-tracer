# Phase 171 R2D — 変更対象・コード全文

本 Phase は新規の読み取り専用監査パッケージだけを追加する。既存 Production モジュール・既存テスト・正式文書は変更しない。

## 新規ファイルと追加位置

リポジトリ直下に `phase171_r2d_pi63_root_expansion_audit/` ディレクトリを追加する。

新規クラスの追加はない。新規関数は `audit.py` 内の定数宣言後に順に配置する。変更される関数はない。

`audit.py`：`git`、`tracked_state`、`validate_r2c`、`eligible_source_inventory`、`root_expansion_inventory`、`markdown_report`、`run`、`main`。

`tests/test_audit.py`：全28テストと関係する helper・import を全文掲載。

下記は `import` を含む各ファイル全文であり、コード中の省略はない。

## audit.py

```python
"""Inspect the real screened backward-search frontier for pi_6^3, read-only.

A proposed GoalExpansion, a fixed statement, or an archive text is not a
completed ProofStep. This diagnostic never promotes any of them into proof.
"""
from __future__ import annotations

import argparse
from collections import Counter
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
    "phase171_r2d_pi63_root_expansion_audit/",
)
EXPECTED_BLOBS = {
    "phase165_r52_r9_shared_math.py": "0ff831522b59f88ff3ed3892f35e5e048be850e1",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r6_explicit_literature_inputs.py": "c430eb4acee83eaa6338dab9834d46808fac0ad4",
    "phase169_r3h_source_registry.py": "1829e3ac1381e10270dac73a196bfd4983540ea4",
    "phase163_r4_r11_literature_registration.py": "2f3a42173f6482167c364e9ff28621b3bcb62792",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase165_r52_r16_web_citation_gate.py": "d1138c0450f234b6da761902ed7358b6038a19c8",
    "phase166_r3t_goal_source_binding/goal_source.py": "e13a07bbc0b6494b0c3c9b891784fe7378448756",
    "phase165_r3_recursive_search.py": "9c424f61a2b4a2d7789777017ad4f91292b0ad30",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}
LOCATORS = (
    "(5.3)", "Proposition 5.3", "Proposition 2.2",
    "Proposition 4.2 (4.4)", "(4.4)",
    "Proposition 5.6", "(5.6)",
)
MAX_PREVIEW = 30


def git(root: Path, *args: str) -> str:
    """Run read-only Git commands with a checked return code."""
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(
            "git " + " ".join(args) + ": "
            + result.stderr.decode("utf-8", "replace").strip()
        )
    return result.stdout.decode("utf-8", "replace").strip()


def tracked_state(root: Path) -> dict:
    """Allow committed audit-only additions, never unscreened source edits."""
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
        raise RuntimeError("origin/develop is ahead of or diverged from local HEAD") from exc
    changed = tuple(path for path in git(
        root, "diff", "--name-only", "-z", BASELINE, "HEAD"
    ).split("\0") if path)
    outside = tuple(path for path in changed if not any(
        path.startswith(prefix) for prefix in REVIEWED_DIRECTORIES
    ))
    if outside:
        raise RuntimeError("unreviewed committed changes: " + ", ".join(outside))
    for path, expected in EXPECTED_BLOBS.items():
        if expected and git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("source blob changed: " + path)
    changes = subprocess.run(
        ["git", "diff", "--binary", "HEAD", "--"],
        cwd=root, capture_output=True, check=False,
    )
    if changes.returncode:
        raise RuntimeError("cannot inspect tracked diff")
    return {
        "branch": branch, "head": head, "upstream": upstream,
        "baseline": BASELINE, "reviewed_changes": list(changed),
        "tracked_diff_sha256": sha256(changes.stdout).hexdigest(),
    }


def validate_r2c(payload: object) -> dict:
    """Reject any report other than the successful recorded pi_6^3 frontier."""
    if not isinstance(payload, dict) or payload.get("phase") != "171 R2C":
        raise ValueError("R2C report required")
    if payload.get("read_only") is not True:
        raise ValueError("R2C source report must be read-only")
    if payload.get("tracked_unchanged") is not True:
        raise ValueError("R2C tracked verification missing")
    case = payload.get("pi63")
    if not isinstance(case, dict) or case.get("target") != "pi_6^3":
        raise ValueError("R2C pi_6^3 report missing")
    if case.get("typed_equal") is not False or case.get("candidate_link_count") != 0:
        raise ValueError("R2C source goal/proof state differs")
    if case.get("toda53_hopf_link_count") != 1:
        raise ValueError("R2C (5.3) Hopf premise inventory differs")
    return case


def eligible_source_inventory(complete_bridge: object, screened_bridge: object) -> list[dict]:
    """Count screened eligible GIVENs per exact source locator, not aliases."""
    registry = complete_bridge.registry
    fixed = tuple(registry._assertions.values())
    steps = tuple(screened_bridge.proof_links)
    inventory = []
    for locator in LOCATORS:
        registered = []
        available = []
        for assertion in fixed:
            reference = registry.reference(assertion.reference_id)
            if reference.locator != locator:
                continue
            registered.append(assertion.assertion_id)
            for link in steps:
                step = link.step
                if (link.assertion_id == assertion.assertion_id
                        and step is not None
                        and getattr(getattr(step, "rule", None), "name", "") == "GIVEN"
                        and not getattr(step, "premises", ())
                        and type(step.conclusion) is type(assertion.content)
                        and step.conclusion == assertion.content):
                    available.append(assertion.assertion_id)
        inventory.append({
            "locator": locator,
            "registered_assertions": len(registered),
            "screened_given_links": len(available),
            "screened_ids": available,
        })
    return inventory


def root_expansion_inventory(goal: object, provider: object, screened_bridge: object) -> dict:
    """Summarize genuine backward proposals; never treat proposals as proofs."""
    if not callable(provider):
        raise TypeError("provider must be callable")
    options = provider(goal)
    if not isinstance(options, tuple):
        raise TypeError("provider must return a tuple")
    names = Counter()
    examples = []
    linked = tuple(screened_bridge.proof_links)
    for index, option in enumerate(options):
        premises = getattr(option, "subgoals", None)
        rule = getattr(option, "rule", None)
        if not isinstance(premises, tuple) or rule is None:
            raise TypeError("invalid typed backward expansion")
        name = str(getattr(rule, "name", type(rule).__name__))
        names[name] += 1
        if index >= MAX_PREVIEW:
            continue
        children = []
        for child in premises[:12]:
            source_count = sum(
                link.step is not None
                and type(link.step.conclusion) is type(child)
                and link.step.conclusion == child
                for link in linked
            )
            children.append({
                "goal_type": type(child).__name__,
                "goal_repr": repr(child)[:900],
                "screened_exact_step_count": source_count,
            })
        examples.append({
            "rule": name, "subgoal_count": len(premises),
            "subgoals": children, "truncated_subgoals": len(premises) > 12,
        })
    return {
        "root_expansions": len(options),
        "distinct_rule_names": len(names),
        "rule_counts": dict(sorted(names.items())),
        "preview_count": len(examples),
        "preview": examples,
        "truncated_expansions": len(options) > MAX_PREVIEW,
        "root_is_verified_proof": False,
    }


def markdown_report(payload: dict) -> str:
    """Report observed source availability and proof-search proposals in Japanese."""
    lines = [
        "# Phase 171 R2D — π₆³ backward expansion frontier", "",
        "このレポートは source screening（出典の選別）と backward expansion（逆向き推論候補）の診断である。", "",
        "推論候補数は完成済み ProofStep 数ではない。", "",
        "## Screened Sources", "",
    ]
    for entry in payload["screened_sources"]:
        lines.append(
            f"{entry['locator']}：登録 {entry['registered_assertions']}件、"
            f"使用可能な照合済み GIVEN {entry['screened_given_links']}件。"
        )
    frontier = payload["frontier"]
    lines += [
        "", "## Root Goal", "",
        "引用の付いた Goal assertion：" + str(payload["citing_assertion_id"]),
        "選別した ProofStepLink 件数：" + str(payload["screened_link_total"]),
        "Root の逆向き推論候補：" + str(frontier["root_expansions"]),
        "候補の規則別件数：" + repr(frontier["rule_counts"]),
        "", "## 保留", "",
        "R2C の型付き不一致と Proposition 5.6 の root ProofStep 欠落は解決していない。",
        "原典の (5.6)? は未確認のままとする。DB の群構造を前提として採用しない。",
        "", "## 次 Phase との境界", "",
        "R2E 以降の導出規則の実装は、本監査で現れた不足前提の出典確認後に別途判断する。",
    ]
    return "\n".join(lines) + "\n"


def run(root: Path, report_path: Path, *, dry_run: bool) -> int:
    """Read saved R2C evidence, then inspect the actual screened search path."""
    before = tracked_state(root)
    source = json.loads(report_path.read_text(encoding="utf-8-sig"))
    validate_r2c(source)
    print("PHASE171_R2D_MODE=READ_ONLY_ROOT_EXPANSION", flush=True)
    print("PHASE171_R2D_TARGET=3,3", flush=True)
    if dry_run:
        if tracked_state(root) != before:
            raise RuntimeError("Git state changed during DryRun")
        print("PHASE171_R2D_DRY_RUN=PASS", flush=True)
        print("PHASE171_R2D_TRACKED_UNCHANGED=True", flush=True)
        print("PHASE171_R2D_RESULT=PASS", flush=True)
        return 0

    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import (
        resolve_specialized_goal_citing_id,
    )
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=3)
    if len(goals) != 1:
        raise RuntimeError("expected exactly one typed pi_6^3 DB Goal")
    goal = goals[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    else:
        screened = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=citing_id,
            explicit_publication_target=True,
        )
    screened = prefer_universal_prop42_derivation(screened)
    inventory = eligible_source_inventory(bridge, screened)
    provider = shared_expansion_provider(screened, proof_target=goal)
    frontier = root_expansion_inventory(goal, provider, screened)
    payload = {
        "phase": "171 R2D", "mode": "READ_ONLY_ROOT_EXPANSION", "read_only": True,
        "source_report": str(report_path), "git": before,
        "citing_assertion_id": citing_id,
        "target_repr": repr(goal)[:2400],
        "screened_link_total": len(screened.proof_links),
        "screened_sources": inventory,
        "frontier": frontier,
    }
    for item in inventory:
        print("PHASE171_R2D_SOURCE=" + json.dumps(item, ensure_ascii=False), flush=True)
    print("PHASE171_R2D_ROOT=" + json.dumps({
        "citing_assertion_id": citing_id,
        "screened_link_total": len(screened.proof_links),
        "root_expansions": frontier["root_expansions"],
        "distinct_rule_names": frontier["distinct_rule_names"],
        "rule_counts": frontier["rule_counts"],
        "preview_count": frontier["preview_count"],
    }, ensure_ascii=False), flush=True)
    for option in frontier["preview"][:8]:
        print("PHASE171_R2D_DETAIL=" + json.dumps(option, ensure_ascii=False), flush=True)
    if tracked_state(root) != before:
        raise RuntimeError("Git state changed during audit")
    payload["tracked_unchanged"] = True
    base = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    directory = base / ("phase171_r2d_pi63_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    directory.mkdir(parents=True, exist_ok=False)
    output = directory / "frontier.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (directory / "frontier.md").write_text(markdown_report(payload), encoding="utf-8")
    print("PHASE171_R2D_REPORT=" + str(output), flush=True)
    print("PHASE171_R2D_TRACKED_UNCHANGED=True", flush=True)
    print("PHASE171_R2D_RESULT=PASS", flush=True)
    return 0


def main() -> int:
    """Run this audit from a module invocation at the repository root."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        return run(args.root.resolve(), args.report.resolve(), dry_run=args.dry_run)
    except Exception as exc:
        print("PHASE171_R2D_ERROR=" + f"{type(exc).__name__}: {exc}", flush=True)
        print(traceback.format_exc()[-2800:], file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## run.ps1

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
    python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider phase171_r2d_pi63_root_expansion_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw "PHASE171_R2D_FOCUSED_PYTEST_EXIT=$LASTEXITCODE" }
    Write-Host 'PHASE171_R2D_FOCUSED_PYTEST=PASS'
    $arguments = @('-B', '-m', 'phase171_r2d_pi63_root_expansion_audit.audit', '--root', $repoRoot, '--report', $ReportPath)
    if ($DryRun.IsPresent) { $arguments += '--dry-run' }
    & python @arguments
    if ($LASTEXITCODE -ne 0) { throw "PHASE171_R2D_AUDIT_EXIT=$LASTEXITCODE" }
    Write-Host 'PHASE171_R2D=PASS'
}
finally {
    Pop-Location
}
```

## tests/test_audit.py

```python
"""Focused tests for the pi_6^3 read-only root-expansion audit."""
from __future__ import annotations

from enum import Enum
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

from phase171_r2d_pi63_root_expansion_audit import audit


class Rule(Enum):
    GIVEN = "given"
    INFERENCE = "inference"


def saved_r2c() -> dict:
    return {
        "phase": "171 R2C",
        "read_only": True,
        "tracked_unchanged": True,
        "pi63": {
            "target": "pi_6^3", "typed_equal": False,
            "candidate_link_count": 0,
            "toda53_hopf_link_count": 1,
        },
    }


def fake_bridge():
    records = (
        ("p42", "Proposition 4.2 (4.4)", ("EHP", "schema")),
        ("h53", "(5.3)", ("H(nu')", "eta5")),
        ("p56", "Proposition 5.6", ("pi63", "Z4")),
    )
    refs = {}
    assertions = {}
    links = []
    for id_, locator, content in records:
        refs[id_] = SimpleNamespace(locator=locator)
        assertions[id_] = SimpleNamespace(
            assertion_id=id_, reference_id=id_, content=content,
        )
        if id_ != "p56":
            links.append(SimpleNamespace(
                assertion_id=id_,
                step=SimpleNamespace(
                    rule=Rule.GIVEN, premises=(), conclusion=content,
                ),
            ))
    registry = SimpleNamespace(
        _assertions=assertions,
        reference=lambda id_: refs[id_],
    )
    complete = SimpleNamespace(registry=registry)
    screened = SimpleNamespace(proof_links=tuple(links))
    return complete, screened


def fake_expansion(name="exactness rule", children=("EHP", "H(nu')")):
    return SimpleNamespace(
        rule=SimpleNamespace(name=name), subgoals=tuple(children),
    )


def test_saved_r2c_accepted():
    assert audit.validate_r2c(saved_r2c())["target"] == "pi_6^3"


@pytest.mark.parametrize("wrong", [None, [], "str", 123])
def test_saved_r2c_rejects_invalid_payload(wrong):
    with pytest.raises(ValueError, match="R2C"):
        audit.validate_r2c(wrong)


def test_saved_r2c_rejects_wrong_phase():
    payload = saved_r2c()
    payload["phase"] = "171 R2B"
    with pytest.raises(ValueError, match="R2C"):
        audit.validate_r2c(payload)


def test_saved_r2c_rejects_missing_readonly():
    payload = saved_r2c()
    payload["read_only"] = False
    with pytest.raises(ValueError, match="read-only"):
        audit.validate_r2c(payload)


def test_saved_r2c_rejects_tracked_modifications():
    payload = saved_r2c()
    payload["tracked_unchanged"] = False
    with pytest.raises(ValueError, match="tracked"):
        audit.validate_r2c(payload)


def test_saved_r2c_rejects_wrong_target():
    payload = saved_r2c()
    payload["pi63"]["target"] = "pi_7^4"
    with pytest.raises(ValueError, match="pi_6"):
        audit.validate_r2c(payload)


def test_saved_r2c_rejects_unexpected_existing_link():
    payload = saved_r2c()
    payload["pi63"]["candidate_link_count"] = 1
    with pytest.raises(ValueError, match="state differs"):
        audit.validate_r2c(payload)


def test_saved_r2c_rejects_hopf_missing():
    payload = saved_r2c()
    payload["pi63"]["toda53_hopf_link_count"] = 0
    with pytest.raises(ValueError, match="Hopf"):
        audit.validate_r2c(payload)


def test_locator_alias_is_separate_from_exact_4_4():
    complete, screened = fake_bridge()
    results = {r["locator"]: r for r in audit.eligible_source_inventory(complete, screened)}
    assert results["Proposition 4.2 (4.4)"]["screened_given_links"] == 1
    assert results["(4.4)"]["registered_assertions"] == 0


def test_given_hopf_is_counted_but_target_candidate_is_not():
    complete, screened = fake_bridge()
    results = {r["locator"]: r for r in audit.eligible_source_inventory(complete, screened)}
    assert results["(5.3)"]["screened_given_links"] == 1
    assert results["Proposition 5.6"]["screened_given_links"] == 0


def test_screened_source_not_counted_when_conclusion_mismatches():
    complete, screened = fake_bridge()
    screened.proof_links[1].step.conclusion = ("wrong", "data")
    results = {r["locator"]: r for r in audit.eligible_source_inventory(complete, screened)}
    assert results["(5.3)"]["screened_given_links"] == 0


def test_screened_source_not_counted_when_rule_is_inference():
    complete, screened = fake_bridge()
    screened.proof_links[0].step.rule = Rule.INFERENCE
    results = {r["locator"]: r for r in audit.eligible_source_inventory(complete, screened)}
    assert results["Proposition 4.2 (4.4)"]["screened_given_links"] == 0


def test_screened_source_not_counted_when_premises_nonempty():
    complete, screened = fake_bridge()
    screened.proof_links[0].step.premises = ("fake",)
    results = {r["locator"]: r for r in audit.eligible_source_inventory(complete, screened)}
    assert results["Proposition 4.2 (4.4)"]["screened_given_links"] == 0


def test_no_root_expansions_is_not_a_proof():
    _, screened = fake_bridge()
    frontier = audit.root_expansion_inventory("goal", lambda goal: (), screened)
    assert frontier["root_expansions"] == 0
    assert frontier["root_is_verified_proof"] is False


def test_root_expansion_counts_distinct_rules():
    _, screened = fake_bridge()
    expansions = (
        fake_expansion(), fake_expansion(),
        fake_expansion("cyclic relation", ("H(nu')",)),
    )
    frontier = audit.root_expansion_inventory("goal", lambda goal: expansions, screened)
    assert frontier["root_expansions"] == 3
    assert frontier["rule_counts"] == {
        "cyclic relation": 1, "exactness rule": 2,
    }
    assert len(frontier["preview"]) == 3
    assert frontier["root_is_verified_proof"] is False


def test_expansion_subgoals_count_screened_evidence_only():
    _, screened = fake_bridge()
    candidates = (fake_expansion(children=(("H(nu')", "eta5"), ("unknown",))),)
    frontier = audit.root_expansion_inventory("goal", lambda goal: candidates, screened)
    subgoals = frontier["preview"][0]["subgoals"]
    assert subgoals[0]["screened_exact_step_count"] == 1
    assert subgoals[1]["screened_exact_step_count"] == 0


def test_provider_must_be_callable():
    _, screened = fake_bridge()
    with pytest.raises(TypeError, match="callable"):
        audit.root_expansion_inventory("goal", object(), screened)


def test_provider_must_return_tuple():
    _, screened = fake_bridge()
    with pytest.raises(TypeError, match="tuple"):
        audit.root_expansion_inventory("goal", lambda goal: [], screened)


def test_provider_rejects_invalid_expansion():
    _, screened = fake_bridge()
    with pytest.raises(TypeError, match="typed"):
        audit.root_expansion_inventory("goal", lambda goal: (object(),), screened)


def test_truncated_expansion_preview():
    _, screened = fake_bridge()
    options = tuple(fake_expansion() for _ in range(audit.MAX_PREVIEW + 1))
    result = audit.root_expansion_inventory("goal", lambda goal: options, screened)
    assert result["root_expansions"] == audit.MAX_PREVIEW + 1
    assert result["preview_count"] == audit.MAX_PREVIEW
    assert result["truncated_expansions"] is True


def test_markdown_warns_proposals_are_not_proofs():
    _, screened = fake_bridge()
    payload = {
        "screened_sources": [{"locator": "(5.3)", "registered_assertions": 1,
                              "screened_given_links": 1}],
        "frontier": audit.root_expansion_inventory("goal", lambda goal: (), screened),
        "citing_assertion_id": None,
        "screened_link_total": 1,
    }
    result = audit.markdown_report(payload)
    assert "ProofStep" in result
    assert "Proposition 5.6" in result
    assert "(5.6)?" in result


def test_git_guard_blocks_unknown_committed_file(monkeypatch, tmp_path):
    def fake_git(root, *args):
        if args[:3] == ("diff", "--name-only", "-z"):
            return "phase165_r52_r9_shared_math.py"
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return audit.BASELINE
        if args == ("rev-parse", "--verify", "refs/remotes/origin/develop"):
            return audit.BASELINE
        return ""
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="unreviewed committed"):
        audit.tracked_state(tmp_path)


def test_git_guard_blocks_modified_tracked(monkeypatch, tmp_path):
    def fake_git(root, *args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return audit.BASELINE
        if args == ("rev-parse", "--verify", "refs/remotes/origin/develop"):
            return audit.BASELINE
        if args == ("status", "--porcelain", "--untracked-files=no"):
            return " M proof.py"
        return ""
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="tracked"):
        audit.tracked_state(tmp_path)


def test_cli_imports_as_module_from_repository_root():
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "-B", "-m", "phase171_r2d_pi63_root_expansion_audit.audit", "--help"],
        cwd=root, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "--report" in result.stdout


def test_dry_run_does_not_import_proof_engine(monkeypatch, tmp_path, capsys):
    report = tmp_path / "frontier.json"
    report.write_text(json.dumps(saved_r2c()), encoding="utf-8")
    state = {"head": audit.BASELINE, "diff": "clean"}
    monkeypatch.setattr(audit, "tracked_state", lambda root: state.copy())
    result = audit.run(tmp_path, report, dry_run=True)
    assert result == 0
    output = capsys.readouterr().out
    assert "PHASE171_R2D_DRY_RUN=PASS" in output
    assert "PHASE171_R2D_TRACKED_UNCHANGED=True" in output
```

## tests/__init__.py

```python
"""Focused Phase 171 R2D tests."""
```

## __init__.py

```python
"""Phase 171 R2D read-only proof-search frontier audit."""
```

## README.md

```markdown
# Phase 171 R2D: pi_6^3 screened backward-frontier audit

This read-only package inspects **the exact typed proof-search context** for the registered `(n=3,k=3)` goal. It reports eligible literature GIVEN steps and root-level backward inference candidates, not completed proofs.

The saved Phase 171 R2C `frontier.json` is required. The run neither installs changes nor edits the production source, registry, database, renderer, existing tests, or official documents. The reviewed Git preflight allows local commits ahead of `origin/develop` only when all changes since the frozen Phase 170 baseline are confined to known Phase 171 audit directories. It rejects divergent/behind remotes and tracked modifications and verifies the previously reviewed source blobs.

The R2C `(4.4)` literal-locator count was zero because the registered source is actually named `Proposition 4.2 (4.4)`. R2D checks both exact locators and counts the GIVEN steps **after** the same citation screening performed by production search.

## Windows PowerShell

Extract `EHP_Phase171_R2D.zip` into the repository root, then run:

```powershell
$Report = Join-Path $env:LOCALAPPDATA "EHPProofTracerRecovery\phase171_r2c_pi63_20261029_074152_618884\frontier.json"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2d_pi63_root_expansion_audit\run.ps1" -ReportPath $Report -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2d_pi63_root_expansion_audit\run.ps1" -ReportPath $Report
git status -sb
```

The focused tests run first. The full pytest suite is deliberately excluded until the end of Phase 171. The diagnostic report is saved under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2d_pi63_*`.

No root expansion is promoted into a verified proof, and unverified source statements remain unverified. R2E (or later) must establish the mathematical derivation separately.
```

## 監査仕様.md

```markdown
# Phase 171 R2D — π₆³ の逆向き推論候補・出典選別監査

## 対象

3-stem の未完成3群のうち、最初の π₆³（n=3, k=3）に限定する。R2C の保存済み `frontier.json` を検証する。R2B で確認された Toda Proposition 5.6 の結論を、ProofStep として自動採用しない。

## 監査項目

`build_shared_typed_bridge()` と DB の `registered_group_goal_candidates()` により現行の型付き Goal を取得する。`resolve_specialized_goal_citing_id()` と既存の citation screening を利用し、Proof Search と同じ順序で出典を選別する。`prefer_universal_prop42_derivation()` を適用し、続けて `shared_expansion_provider()` が Root Goal に提案する逆向き推論候補を集計する。

R2C の `(4.4)` 登録数0は完全列の未登録を意味しない。既存の一般 EHP 完全列は `Proposition 4.2 (4.4)` の locator で登録されている。本監査では両方を正確に区別し、選別後の `GIVEN` 数を表示する。

出典として `GIVEN` が選別されても、数学的な Root Goal の導出が証明されるわけではない。候補の推論規則と subgoal を実際に検証していないため、候補数と ProofStep 数を混同しない。とくに Toda (5.3) から ν′ の位数4および生成元性を自動認定しない。

## 安全条件と境界

Git `develop` の履歴、対象コードとデータの blob、追跡済みファイル変更の有無を実行前後に確認する。追加された監査ディレクトリ以外への変更は拒否する。ファイルの書き込み先は `%LOCALAPPDATA%` の監査報告のみとする。

限定 pytest だけを実行する。全体 pytest、Production の変更、PDF 文献の原典照合、π₇⁴／π₈⁵ の証明完成化は R2D の範囲外とする。次段階では不足前提を一つずつ出典・型・推論規則に基づいて追加する。
```

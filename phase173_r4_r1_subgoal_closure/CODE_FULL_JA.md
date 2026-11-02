# Phase 173 R4-R1 — 新規コード全文

## 変更対象と実装境界

- 既存の Production（実行本体）ファイル・クラス・関数・import は変更しない。
- 新規ディレクトリ `phase173_r4_r1_subgoal_closure/` のみ追加。
- `audit.py` 新規関数（先頭から順）：`git()`、`guard_sources()`、`validate_lemma_source()`、`classify_step()`、`lemma54_archive_metadata()`、`describe_progress()`、`inspect_runtime()`、`main()`。
- `tests/test_audit.py` 新規関数はコードに記載した順に追加する。
- 新規関数は `audit.py` の import 群直後に記載した順で追加し、テストは import 群直後に記載した順で追加。
- `README.md` は英文、`AUDIT_PLAN_JA.md` は日本語。既存公式ドキュメント5件は変更しない。

## `phase173_r4_r1_subgoal_closure/audit.py`

```python
"""Inspect four Toda (5.6) subgoals in the exact screened publication context.

This audit does not register a statement, create a GIVEN, or modify production.
A source-archive entry is metadata, never a ProofStep.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
from typing import Any

REVIEWED_ANCESTOR = "84f7c3f892d50889e9e2a8a8426213c7964605eb"
REVIEWED_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "sources/toda/Toda_04_2.tex": "4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7",
    "phase165_r52_r9_shared_math.py": "2718c55789af7f442ac2c086d016d3d6f7ca3133",
    "phase165_r52_r16_web_citation_gate.py": "d1138c0450f234b6da761902ed7358b6038a19c8",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r52_r27_r5_literature.py": "c9bfe2788f4cf043db6dada98a437afea6accf75",
    "phase169_r3m_prior_result_catalog/prior_results.py": "c522cbaf924b3a9aa500d453b8eb6a1a66c42611",
    "phase166_r3t_goal_source_binding/goal_source.py": "e13a07bbc0b6494b0c3c9b891784fe7378448756",
    "toda_rules.py": "77f4159644f10eff65a79f6e528cf7b471c6ddc9",
}
LEMMA54_ARCHIVE_ID = "toda:tex:ch5:0007"


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(("git", *arguments), cwd=root, capture_output=True,
                            text=True, encoding="utf-8", check=True)
    return result.stdout.strip()


def guard_sources(root: Path) -> dict[str, Any]:
    """Refuse unknown production blobs and local source modifications."""
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Phase 173 R4-R1 requires develop")
    head = git(root, "rev-parse", "HEAD")
    ancestor = subprocess.run(("git", "merge-base", "--is-ancestor",
                              REVIEWED_ANCESTOR, head), cwd=root, check=False,
                             capture_output=True)
    if ancestor.returncode != 0:
        raise RuntimeError("Reviewed R4-R1 commit is not an ancestor")
    if git(root, "rev-parse", "origin/develop") != head:
        raise RuntimeError("Local HEAD differs from origin/develop")
    for name, expected in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + name) != expected:
            raise RuntimeError("Reviewed production source changed: " + name)
        for args in (("diff", "--quiet", "--", name),
                     ("diff", "--cached", "--quiet", "--", name)):
            result = subprocess.run(("git", *args), cwd=root, capture_output=True,
                                    check=False)
            if result.returncode != 0:
                raise RuntimeError("Source modified or unreadable: " + name)
    chapter = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(
        encoding="utf-8-sig")
    validate_lemma_source(chapter)
    return {"head": head, "production_blobs_verified": list(REVIEWED_BLOBS),
            "no_git_mutation": True}


def validate_lemma_source(source: str) -> None:
    """Require both exact Lemma 5.4 identities in the cited lemma environment."""
    marker = r"\begin{lemma}[]" + "\n" + r"\label{lem:5.4}"
    start = source.find(marker)
    if start < 0:
        raise RuntimeError("Reviewed Lemma 5.4 start is absent")
    end = source.find(r"\end{lemma}", start)
    if end < 0 or source.find(marker, start + 1) >= 0:
        raise RuntimeError("Lemma 5.4 source is missing or ambiguous")
    excerpt = source[start:end]
    for token in (r"\nu_{4}\in \pi^{4}_{7}",
                  r"H(\nu_{4})=\iota_7",
                  r"2E \nu_{4}=E^{2}\nu'"):
        if token not in excerpt:
            raise RuntimeError("Toda Lemma 5.4 lacks reviewed clause: " + token)


def classify_step(step: object, expected: object, *, required_rule: str | None = None) -> str:
    """Distinguish a verified conclusion from a proposal or wrong proof rule."""
    if getattr(step, "conclusion", None) != expected:
        return "WRONG_CONCLUSION"
    rule = getattr(getattr(step, "rule", None), "value", None)
    if rule is None:
        rule = str(getattr(step, "rule", "MISSING"))
    if required_rule is not None and rule != required_rule:
        return "WRONG_RULE:" + str(rule)
    return "PROVED:" + str(rule)


def lemma54_archive_metadata(bridge: object, screened: object) -> dict[str, Any]:
    from unified_statement_registry import AssertionOrigin
    rows = [a for a in bridge.registry._assertions.values()
            if a.origin is AssertionOrigin.SOURCE_ARCHIVE
            and isinstance(a.content, dict)
            and a.content.get("source_statement_id") == LEMMA54_ARCHIVE_ID]
    hashed = [isinstance(row.content.get("source_text"), str)
              and row.content.get("source_sha256") == sha256(
                  row.content.get("source_text", "").encode("utf-8")
              ).hexdigest() for row in rows]
    # Do not confuse the SOURCE_ARCHIVE dict with a screened source ProofStep.
    fixed_count = sum(
        1 for link in screened.proof_links if link.step is not None
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
        and getattr(screened.registry.reference(
            screened.registry.assertion(link.assertion_id).reference_id),
            "locator", None) == "Lemma 5.4"
    )
    return {"archived_rows": len(rows), "archive_sha256_verified": hashed,
            "screened_lemma54_fixed_steps": fixed_count,
            "archive_is_proof": False}


def describe_progress(events: list[tuple[str, str]]) -> dict[str, Any]:
    unresolved = [v for kind, v in events if kind == "unresolved"]
    proved = [v for kind, v in events if kind == "proved"]
    return {"event_count": len(events), "proved_count": len(proved),
            "unresolved_count": len(unresolved),
            "first_unresolved": unresolved[:5], "last_unresolved": unresolved[-5:]}


def inspect_runtime(root: Path) -> dict[str, Any]:
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r3_recursive_search import (
        RegisteredGoalUnresolved, reconstruct_registered_goal,
    )
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase173_r4_r1_source_bound_56.rule import expand_source_bound_toda56
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=4, k=3)
    if len(goals) != 1:
        raise RuntimeError("Expected exact one pi_7^4 target")
    goal = goals[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        raise RuntimeError("Missing positioned pi_7^4 citation")
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    ))
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN
                      and screened.registry.assertion(link.assertion_id).origin
                      is AssertionOrigin.FIXED_STATEMENT)

    def extra(statement: object):
        return expand_source_bound_toda56(
            statement, available, screened, proof_target=goal,
        )

    roots = extra(goal)
    if len(roots) != 1 or len(roots[0].subgoals) != 4:
        raise RuntimeError("Expected one exact four-premise Toda root")
    provider = shared_expansion_provider(
        screened, extra_providers=(extra,), proof_target=goal,
    )
    labels = ("CITED_PROP44", "PRIOR_PI63", "DIAGONAL_PI77", "HOPF_NU4")
    rows = []
    for index, (label, subgoal) in enumerate(zip(labels, roots[0].subgoals), 1):
        screened_exact = [x for x in available if type(x) is type(subgoal) and x == subgoal]
        proposals = provider(subgoal)
        # No source, no proposal: the reconstruction cannot invent a proof.
        row: dict[str, Any] = {
            "index": index, "label": label, "statement_type": type(subgoal).__name__,
            "statement": repr(subgoal), "screened_exact_given": len(screened_exact),
            "proposal_count": len(proposals),
            "proposal_rules": [p.rule.name for p in proposals],
            "certified": False, "status": "NOT_CHECKED",
        }
        if not screened_exact and not proposals:
            row["status"] = "NO_SCREENED_LEAF_OR_PROPOSAL"
            rows.append(row)
            continue
        events: list[tuple[str, str]] = []
        def observer(kind: str, target: object, step: object) -> None:
            if len(events) < 500:
                events.append((kind, repr(target)[:450]))
        try:
            step = reconstruct_registered_goal(
                subgoal, screened, citing_assertion_id=citing_id,
                expansion_provider=provider, lookup_mode="typed_reference_publication",
                progress_observer=observer,
            )
        except RegisteredGoalUnresolved as exc:
            row["status"] = "UNRESOLVED"
            row["error"] = str(exc)[:1500]
        else:
            required_rule = "inference" if label in ("DIAGONAL_PI77", "HOPF_NU4") else None
            status = classify_step(step, subgoal, required_rule=required_rule)
            row["status"] = status
            row["certified"] = status.startswith("PROVED:")
            row["proof_rule"] = getattr(step.rule, "value", str(step.rule))
        row["progress"] = describe_progress(events)
        rows.append(row)
    return {
        "goal": repr(goal), "citing_assertion_id": citing_id,
        "root_rule": roots[0].rule.name,
        "lemma54_source": lemma54_archive_metadata(bridge, screened),
        "subgoals": rows,
        "all_four_premises_proved": all(x["certified"] for x in rows),
        "complete_root_certified": False,
        "no_proof_promotion": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    preflight = guard_sources(root)
    print("PHASE173_R4_R1_CLOSURE_SOURCE_GUARD=PASS")
    if args.dry_run:
        print("PHASE173_R4_R1_CLOSURE_DRY_RUN=PASS")
        return 0
    runtime = inspect_runtime(root)
    destination = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / (
        "EHPProofTracerRecovery/phase173_r4_r1_subgoal_closure/audit.json"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps({
        "phase": "173-R4-R1", "scope": "AUDIT_ONLY",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "preflight": preflight, "runtime": runtime, "production_changes": [],
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PHASE173_R4_R1_CLOSURE_AUDIT=PASS")
    source = runtime["lemma54_source"]
    print("LEMMA54_ARCHIVED_ROWS=" + str(source["archived_rows"]))
    print("LEMMA54_ARCHIVE_HASH_VALID=" + str(source["archive_sha256_verified"]))
    print("LEMMA54_SCREENED_FIXED_STEPS=" + str(source["screened_lemma54_fixed_steps"]))
    for item in runtime["subgoals"]:
        prefix = "SUBGOAL_" + str(item["index"])
        print(prefix + "=" + item["label"])
        print(prefix + "_STATUS=" + item["status"])
        print(prefix + "_PROPOSALS=" + str(item["proposal_count"]))
        print(prefix + "_RULES=" + repr(item["proposal_rules"]))
        if "error" in item:
            print(prefix + "_ERROR=" + item["error"])
        if "progress" in item:
            print(prefix + "_FIRST_UNRESOLVED=" + repr(item["progress"]["first_unresolved"]))
    print("ALL_FOUR_PREMISES_PROVED=" + str(runtime["all_four_premises_proved"]))
    print("COMPLETE_ROOT_CERTIFIED=False")
    print("NO_PROOF_PROMOTION=True")
    print("AUDIT_JSON=" + str(destination))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `phase173_r4_r1_subgoal_closure/run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = (Resolve-Path (Join-Path $Here '..')).Path
Push-Location $Root
try {
    Write-Output 'PHASE173_R4_R1_CLOSURE_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider '.\phase173_r4_r1_subgoal_closure\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 closure focused pytest failed' }
    Write-Output 'PHASE173_R4_R1_CLOSURE_FOCUSED_PYTEST=PASS'
    $Arguments = @('-m', 'phase173_r4_r1_subgoal_closure.audit', '--root', $Root)
    if ($DryRun) { $Arguments += '--dry-run' }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 closure audit failed' }
}
finally {
    Pop-Location
}
```

## `phase173_r4_r1_subgoal_closure/tests/test_audit.py`

```python
"""Focused tests: source immutability, proof status and report integrity."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_r4_r1_subgoal_closure.audit import (
    classify_step,
    describe_progress,
    validate_lemma_source,
)


def lemma_fixture() -> str:
    return (
        "prefix\n"
        "\\begin{lemma}[]\n\\label{lem:5.4}\n"
        "\\nu_{4}\\in \\pi^{4}_{7}\n"
        "H(\\nu_{4})=\\iota_7,\\qquad 2E \\nu_{4}=E^{2}\\nu' .\n"
        "\\end{lemma}\n"
    )


def test_accepts_verified_lemma_environment() -> None:
    validate_lemma_source(lemma_fixture())


@pytest.mark.parametrize("needle", [
    "\\label{lem:5.4}",
    "\\nu_{4}\\in \\pi^{4}_{7}",
    "H(\\nu_{4})=\\iota_7",
    "2E \\nu_{4}=E^{2}\\nu'",
])
def test_rejects_missing_lemma_clause(needle: str) -> None:
    with pytest.raises(RuntimeError):
        validate_lemma_source(lemma_fixture().replace(needle, "MISSING"))


def test_rejects_duplicate_lemma() -> None:
    with pytest.raises(RuntimeError):
        validate_lemma_source(lemma_fixture() + lemma_fixture())


def test_proof_classification_correct_inference() -> None:
    expected = object()
    step = SimpleNamespace(conclusion=expected, rule=SimpleNamespace(value="inference"))
    assert classify_step(step, expected, required_rule="inference") == "PROVED:inference"


def test_rejects_given_instead_of_inference() -> None:
    expected = object()
    step = SimpleNamespace(conclusion=expected, rule=SimpleNamespace(value="given"))
    assert classify_step(step, expected, required_rule="inference") == "WRONG_RULE:given"


def test_rejects_other_conclusion() -> None:
    step = SimpleNamespace(conclusion=object(), rule=SimpleNamespace(value="inference"))
    assert classify_step(step, object()) == "WRONG_CONCLUSION"


def test_progress_reports_unresolved_and_proved() -> None:
    value = describe_progress([
        ("proved", "p"), ("unresolved", "a"), ("unresolved", "b"),
    ])
    assert value["proved_count"] == 1
    assert value["first_unresolved"] == ["a", "b"]
    assert value["last_unresolved"] == ["a", "b"]


def test_no_production_import_at_module_level() -> None:
    source = Path(__file__).resolve().parents[1].joinpath("audit.py").read_text(encoding="utf-8")
    before = source.split("def inspect_runtime(", 1)[0]
    assert "from phase165_" not in before
    assert "from phase173_r4_r1_source_bound_56" not in before
```

## `phase173_r4_r1_subgoal_closure/__init__.py`

```python
"""Phase 173 R4-R1: isolated prerequisite closure audit."""
```

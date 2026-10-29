# Phase 171 R2F-R1 — 変更コード全文

## 変更ファイル・関数・クラス

- `phase171_r2f_pi63_extension_gap_audit/audit.py`：既存関数 `run()` のみ変更。import は不変。
- `phase171_r2f_pi63_extension_gap_audit/tests/test_audit.py`：末尾に新規 `test_normal_run_preserves_path_after_root_frontier()` を追加。既存7テスト、トップレベル import は不変。
- `phase171_r2f_r1_root_shadow_fix/install.py`：新規 `PatchSpec`, `digest`, `preflight`, `atomic_replace`, `apply`, `main`。
- `phase171_r2f_r1_root_shadow_fix/tests/test_install.py`：新規 `fixture_paths` と4テスト。
- `phase171_r2f_r1_root_shadow_fix/run.ps1`：新規。

変更前後の `audit.py` の唯一の変更は `root`（辞書）を `root_frontier` に改名し、参照2か所を修正すること。既存の `root: Path` は変更しない。

次の各ファイルはそのまま置換できる**全文**である。

## 既存 audit.py の変更後全文

```python
"""Read-only audit for the typed order-four extension of pi_6^3.

This code neither adds a ProofStep nor changes any inference rule or source.
A mathematical argument is not reported as a completed machine proof.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import fields, is_dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

EXPECTED_TARGET = "shared:0:boundary:Proposition 5.6:pi6_3_group_relation"
EXPECTED_DOUBLE_SUFFIX = "toda:adopted:eq5.3:nu_prime_double_relation"
EXPECTED_HOPF_SUFFIX = "toda:adopted:eq5.3:nu_prime_hopf_relation"
LOCATORS = (
    "Proposition 2.2", "Proposition 4.2 (4.4)", "(5.2)",
    "Proposition 5.3", "(5.3)", "Proposition 5.6",
)


def git_read(root: Path, *arguments: str) -> bytes:
    """Execute only listed read-only Git invocations and require success."""
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("rev-parse", "--verify", "refs/remotes/origin/develop"),
        ("status", "--porcelain=v1", "--untracked-files=all"),
        ("diff", "--binary", "HEAD", "--"),
    }
    if arguments not in allowed:
        raise ValueError("Git operation not authorized for R2F audit")
    process = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True, check=False,
    )
    if process.returncode:
        raise RuntimeError(
            "git " + " ".join(arguments) + ": "
            + process.stderr.decode("utf-8", errors="replace")
        )
    return process.stdout


def snapshot(root: Path) -> dict:
    """Record committed identity and exact tracked/untracked worktree state."""
    branch = git_read(root, "branch", "--show-current").decode().strip()
    if branch != "develop":
        raise RuntimeError("R2F requires develop but never switches branches")
    head = git_read(root, "rev-parse", "HEAD").decode().strip()
    try:
        upstream = git_read(root, "rev-parse", "--verify", "refs/remotes/origin/develop").decode().strip()
    except RuntimeError:
        upstream = None
    return {
        "branch": branch,
        "head": head,
        "origin_develop_local_ref": upstream,
        "head_equals_local_origin_ref": head == upstream,
        "status": git_read(root, "status", "--porcelain=v1", "--untracked-files=all").decode(
            "utf-8", errors="replace"
        ).splitlines(),
        "tracked_diff_sha256": sha256(git_read(root, "diff", "--binary", "HEAD", "--")).hexdigest(),
    }


def typed_differences(left: object, right: object, *, limit: int = 20) -> list[dict]:
    """Compare dataclass fields exactly; never accept name-only generator aliases."""
    differences: list[dict] = []

    def visit(a: object, b: object, path: str, depth: int) -> None:
        if len(differences) >= limit:
            return
        if type(a) is not type(b):
            differences.append({
                "path": path, "reason": "type_mismatch",
                "left": type(a).__name__, "right": type(b).__name__,
            })
            return
        if depth >= 12:
            if a != b:
                differences.append({"path": path, "reason": "depth_limit"})
            return
        if is_dataclass(a) and not isinstance(a, type):
            for field in fields(a):
                visit(getattr(a, field.name), getattr(b, field.name), path + "." + field.name, depth + 1)
            return
        if a != b:
            differences.append({
                "path": path, "reason": "value_mismatch",
                "left": repr(a)[:250], "right": repr(b)[:250],
            })

    visit(left, right, "generator", 0)
    return differences


def matching_cited_steps(bridge: object, suffix: str) -> tuple:
    """Require screened, no-premise, registered fixed GIVENs with exact identity."""
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    matches = []
    for link in bridge.proof_links:
        step = link.step
        if not link.assertion_id.endswith(suffix) or step is None:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and step.rule is ProofRule.GIVEN
                and not step.premises
                and step.conclusion == assertion.content):
            matches.append((link.assertion_id, step.conclusion))
    return tuple(matches)


def source_inventory(bridge: object) -> dict:
    """Count screened assertions, never count unscreened archive metadata as proof."""
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    output = {}
    for locator in LOCATORS:
        entries = []
        for link in bridge.proof_links:
            step = link.step
            if step is None:
                continue
            assertion = bridge.registry.assertion(link.assertion_id)
            reference = bridge.registry.reference(assertion.reference_id)
            if reference.locator != locator:
                continue
            if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                    or step.rule is not ProofRule.GIVEN
                    or step.premises or step.conclusion != assertion.content):
                continue
            entries.append({
                "id": link.assertion_id,
                "type": type(step.conclusion).__name__,
                "text": repr(step.conclusion)[:1200],
                "position": reference.publication_position,
            })
        output[locator] = {"count": len(entries), "steps": entries[:16]}
    return output


def expansion_inventory(goal: object, provider: object, bridge: object) -> dict:
    """Observe first-level proposals without treating a proposed premise as known."""
    from proof import ProofRule

    options = provider(goal)
    if not isinstance(options, tuple):
        raise TypeError("provider must return a tuple")
    counter = Counter()
    details = []
    for option in options:
        name = str(getattr(option.rule, "name", type(option.rule).__name__))
        counter[name] += 1
        if len(details) >= 16:
            continue
        children = []
        for child in option.subgoals[:10]:
            cited_matches = tuple(
                link.assertion_id for link in bridge.proof_links
                if link.step is not None
                and link.step.rule is ProofRule.GIVEN
                and not link.step.premises
                and link.step.conclusion == child
            )
            children.append({
                "type": type(child).__name__,
                "goal": repr(child)[:1200],
                "exact_screened_given_ids": cited_matches,
            })
        details.append({"rule": name, "subgoals": children})
    return {"count": len(options), "rules": dict(sorted(counter.items())), "examples": details}


def requirement_assessment(inventory: dict, *, double_present: bool, hopf_present: bool,
                           cyclic_expansions: int) -> list[dict]:
    """List known evidence and unproved obligations without asserting impossibility."""
    evidence = (
        ("prop22_hopf_composition", "Proposition 2.2",
         "H(nu' o eta_6)=eta_5^2 の型付き導出"),
        ("prop53_eta_squared", "Proposition 5.3",
         "pi_7^5 および pi_5^3 の位数2・生成性の特殊化"),
        ("toda52_pi52", "(5.2)",
         "pi_5^2 の群構造と生成元 eta_2^3 の輸送"),
        ("ehp_exact_window", "Proposition 4.2 (4.4)",
         "pi_7^3→pi_7^5→pi_5^2→pi_6^3→pi_6^5 の完全性"),
    )
    rows = [{
        "key": key,
        "screened_fixed_given_count": inventory[locator]["count"],
        "obligation": obligation,
        "certified_as_completed_inference": False,
    } for key, locator, obligation in evidence]
    rows.extend((
        {"key": "nu_prime_hopf", "screened_fixed_given_count": int(hopf_present),
         "obligation": "H(nu')=eta_5 と H の全射性を区別", "certified_as_completed_inference": False},
        {"key": "nu_prime_double", "screened_fixed_given_count": int(double_present),
         "obligation": "2nu'=eta_3 eta_4 eta_5 と E(eta_2^3) を同一視する証明",
         "certified_as_completed_inference": False},
        {"key": "finite_extension_structure", "screened_fixed_given_count": 0,
         "obligation": "E の単射・H の全射・完全性と Z/2×Z/2 から |pi_6^3|=4 を導く",
         "certified_as_completed_inference": False},
        {"key": "order_and_generator", "screened_fixed_given_count": 0,
         "obligation": "非零の 2nu' と位数4の群から位数4・生成性を導く",
         "certified_as_completed_inference": False},
    ))
    if cyclic_expansions:
        rows[-1]["note"] = "既存の巡回群構造への候補は存在するが証明ではない"
    return rows


def run(root: Path, *, dry_run: bool, search: bool) -> int:
    """Audit the current local worktree without modifying repository files."""
    before = snapshot(root)
    print("PHASE171_R2F_BRANCH=" + before["branch"], flush=True)
    print("PHASE171_R2F_HEAD=" + before["head"], flush=True)
    print("PHASE171_R2F_TRACKED_DIFF_SHA256=" + before["tracked_diff_sha256"], flush=True)
    if dry_run:
        if snapshot(root) != before:
            raise RuntimeError("worktree changed during DryRun")
        print("PHASE171_R2F_DRY_RUN=PASS", flush=True)
        print("PHASE171_R2F_RESULT=PASS_AUDIT_ONLY", flush=True)
        return 0

    from expression import Multiple
    from homotopy_groups import FiniteCyclicGroup
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase166_r3c_publication_order import precedes_citing_assertion
    from proof import ProofRule

    complete = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(complete, n=3, k=3)
    if len(candidates) != 1:
        raise RuntimeError("expected one typed pi_6^3 DB goal")
    goal = candidates[0]
    if not isinstance(goal.rhs, FiniteCyclicGroup) or goal.rhs.order != 4:
        raise RuntimeError("unexpected pi_6^3 target group")
    citing = resolve_specialized_goal_citing_id(complete, goal)
    if citing != EXPECTED_TARGET:
        raise RuntimeError("unexpected source identity for pi_6^3 goal: " + repr(citing))
    screened = screen_shared_proof_context(
        complete, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    screened = prefer_universal_prop42_derivation(screened)
    doubles = matching_cited_steps(screened, EXPECTED_DOUBLE_SUFFIX)
    hopfs = matching_cited_steps(screened, EXPECTED_HOPF_SUFFIX)
    if len(doubles) != 1 or len(hopfs) != 1:
        raise RuntimeError("R2E double and R3H Hopf must each be uniquely screened GIVENs")
    double_assertion = screened.registry.assertion(doubles[0][0])
    double_reference = screened.registry.reference(double_assertion.reference_id)
    if (double_reference.locator != "(5.3)"
            or double_reference.publication_position != 8100
            or not precedes_citing_assertion(screened, doubles[0][0], citing)):
        raise RuntimeError("R2E source does not precede the target at the reviewed position")
    relation = doubles[0][1]
    if not isinstance(relation.lhs, Multiple) or relation.lhs.coefficient != 2:
        raise RuntimeError("R2E conclusion is not a typed 2*generator equality")
    if any(link.step is not None and link.step.conclusion == goal
           for link in screened.proof_links):
        raise RuntimeError("forbidden direct target proof link was found")

    cyclic = CyclicStructureStatement(goal.lhs, goal.rhs.generator, 4)
    provider = shared_expansion_provider(screened, proof_target=goal)
    root_frontier = expansion_inventory(goal, provider, screened)
    cyclic_frontier = expansion_inventory(cyclic, provider, screened)
    sources = source_inventory(screened)
    assessment = requirement_assessment(
        sources, double_present=True, hopf_present=True,
        cyclic_expansions=cyclic_frontier["count"],
    )
    runtime_search = None
    if search:
        from phase165_r55_nk_only_goal import search_group_from_registered_goal
        result = search_group_from_registered_goal(n=3, k=3, bridge=complete)
        runtime_search = {
            "status": str(result.status),
            "conclusion_is_goal": result.conclusion == goal,
            "inference_step_count": sum(step.rule is ProofRule.INFERENCE
                                        for step in result.proven_steps),
            "given_step_count": sum(step.rule is ProofRule.GIVEN
                                    for step in result.proven_steps),
            "open_goals": [repr(x)[:1000] for x in result.open_goals[:16]],
        }
    report = {
        "phase": "171 R2F", "mode": "READ_ONLY_TYPED_GAP", "read_only": True,
        "git_before": before,
        "target": repr(goal), "citing_id": citing,
        "double_given_id": doubles[0][0], "hopf_given_id": hopfs[0][0],
        "double_publication_position": double_reference.publication_position,
        "double_precedes_target": True,
        "double_relation": repr(relation),
        "db_generator": repr(goal.rhs.generator),
        "nu_prime_from_double": repr(relation.lhs.expression),
        "generator_typed_equal": goal.rhs.generator == relation.lhs.expression,
        "generator_differences": typed_differences(goal.rhs.generator, relation.lhs.expression),
        "sources": sources,
        "root_expansions": root_frontier, "cyclic_expansions": cyclic_frontier,
        "remaining_obligations": assessment,
        "runtime_search": runtime_search,
        "root_proof_certified_by_this_audit": False,
    }
    if snapshot(root) != before:
        raise RuntimeError("worktree changed during source inspection")
    report["git_after_identical"] = True
    report_dir = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    report_dir = report_dir / ("phase171_r2f_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    report_dir.mkdir(parents=True, exist_ok=False)
    report_path = report_dir / "audit.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PHASE171_R2F_DOUBLE_SOURCE=PASS", flush=True)
    print("PHASE171_R2F_HOPF_SOURCE=PASS", flush=True)
    print("PHASE171_R2F_DB_GENERATOR_TYPED_EQUAL=" + str(report["generator_typed_equal"]), flush=True)
    print("PHASE171_R2F_ROOT_RULES=" + json.dumps(root_frontier["rules"], ensure_ascii=False), flush=True)
    print("PHASE171_R2F_CYCLIC_RULES=" + json.dumps(cyclic_frontier["rules"], ensure_ascii=False), flush=True)
    for row in assessment:
        print("PHASE171_R2F_OBLIGATION=" + json.dumps(row, ensure_ascii=False), flush=True)
    if runtime_search is not None:
        print("PHASE171_R2F_SEARCH=" + json.dumps(runtime_search, ensure_ascii=False), flush=True)
    print("PHASE171_R2F_REPORT=" + str(report_path), flush=True)
    print("PHASE171_R2F_WORKTREE_UNCHANGED=True", flush=True)
    print("PHASE171_R2F_RESULT=PASS_AUDIT_ONLY", flush=True)
    return 0


def main() -> int:
    """Run the audit in dry-run, frontier, or optional existing-search mode."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--search", action="store_true")
    args = parser.parse_args()
    try:
        return run(args.root.resolve(), dry_run=args.dry_run, search=args.search)
    except Exception as exc:
        print("PHASE171_R2F_ERROR=" + f"{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        print(traceback.format_exc()[-3000:], file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## 既存 tests/test_audit.py の変更後全文

```python
"""Source-independent, narrow tests for Phase 171 R2F read-only audit."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase171_r2f_pi63_extension_gap_audit import audit


def test_git_read_blocks_mutating_commands(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="not authorized"):
        audit.git_read(tmp_path, "reset", "--hard")
    with pytest.raises(ValueError, match="not authorized"):
        audit.git_read(tmp_path, "checkout", "--", "proof.py")


def test_typed_differences_rejects_same_text_with_different_types() -> None:
    left = SimpleNamespace(name="nu-prime", source=6)
    right = {"name": "nu-prime", "source": 6}
    result = audit.typed_differences(left, right)
    assert result == [{
        "path": "generator", "reason": "type_mismatch",
        "left": "SimpleNamespace", "right": "dict",
    }]


def test_typed_differences_detects_dataclass_field_mismatch() -> None:
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class Generator:
        family: str
        decoration: str

    differences = audit.typed_differences(Generator("nu", "prime"), Generator("nu", "apostrophe"))
    assert len(differences) == 1
    assert differences[0]["path"] == "generator.decoration"


def test_assessment_keeps_sources_separate_from_proven_inference() -> None:
    sample = {locator: {"count": 1} for locator in audit.LOCATORS}
    rows = audit.requirement_assessment(
        sample, double_present=True, hopf_present=True, cyclic_expansions=0,
    )
    assert len(rows) == 8
    assert rows[4]["key"] == "nu_prime_hopf"
    assert rows[5]["key"] == "nu_prime_double"
    assert all(row["certified_as_completed_inference"] is False for row in rows)
    assert rows[-1]["screened_fixed_given_count"] == 0


def test_assessment_reports_absent_prop22_source_without_claiming_proof() -> None:
    sample = {locator: {"count": 0} for locator in audit.LOCATORS}
    rows = audit.requirement_assessment(
        sample, double_present=True, hopf_present=True, cyclic_expansions=2,
    )
    assert rows[0]["key"] == "prop22_hopf_composition"
    assert rows[0]["screened_fixed_given_count"] == 0
    assert "候補" in rows[-1]["note"]


def test_dry_run_preserves_snapshot_and_does_not_load_proof_engine(monkeypatch, tmp_path: Path, capsys) -> None:
    before = {"branch": "develop", "head": "dummy", "tracked_diff_sha256": "hash", "status": [" M source.py"]}
    monkeypatch.setattr(audit, "snapshot", lambda root: before.copy())
    assert audit.run(tmp_path, dry_run=True, search=False) == 0
    output = capsys.readouterr().out
    assert "PHASE171_R2F_RESULT=PASS_AUDIT_ONLY" in output
    assert "PHASE171_R2F_DRY_RUN=PASS" in output


def test_dry_run_fails_closed_when_snapshot_changes(monkeypatch, tmp_path: Path) -> None:
    calls = iter((
        {"branch": "develop", "head": "a", "tracked_diff_sha256": "one"},
        {"branch": "develop", "head": "a", "tracked_diff_sha256": "two"},
    ))
    monkeypatch.setattr(audit, "snapshot", lambda root: next(calls))
    with pytest.raises(RuntimeError, match="worktree changed"):
        audit.run(tmp_path, dry_run=True, search=False)


@pytest.mark.parametrize("search", (False, True))
def test_normal_run_preserves_path_after_root_frontier(monkeypatch, tmp_path: Path, search: bool) -> None:
    """Exercise the actual non-DryRun branch and reject a dict in snapshot(root)."""
    import json
    import sys
    from dataclasses import dataclass
    from types import ModuleType

    original_root = tmp_path / "repository"
    original_root.mkdir()
    recovery = tmp_path / "recovery"
    monkeypatch.setenv("LOCALAPPDATA", str(recovery))
    state = {"branch": "develop", "head": "test-head", "tracked_diff_sha256": "test-diff", "status": []}
    observed_roots = []

    def guarded_snapshot(path: Path) -> dict:
        assert isinstance(path, Path), "repository root must remain a Path, not an expansion dict"
        assert path == original_root
        observed_roots.append(path)
        return state.copy()

    monkeypatch.setattr(audit, "snapshot", guarded_snapshot)

    @dataclass(frozen=True)
    class FakeMultiple:
        coefficient: int
        expression: object

    @dataclass(frozen=True)
    class FakeFiniteCyclic:
        order: int
        generator: object

    @dataclass(frozen=True)
    class FakeCyclic:
        group: object
        generator: object
        order: int

    target_generator = object()
    target_group = object()
    goal = SimpleNamespace(
        lhs=target_group,
        rhs=FakeFiniteCyclic(order=4, generator=target_generator),
    )
    double = SimpleNamespace(lhs=FakeMultiple(2, target_generator), rhs="eta-composite")
    source_id = "shared:12:" + audit.EXPECTED_DOUBLE_SUFFIX
    hopf_id = "shared:8:" + audit.EXPECTED_HOPF_SUFFIX
    reference = SimpleNamespace(locator="(5.3)", publication_position=8100)
    registry = SimpleNamespace(
        assertion=lambda assertion_id: SimpleNamespace(reference_id="adopted53"),
        reference=lambda reference_id: reference,
    )
    complete = SimpleNamespace(registry=registry)
    screened = SimpleNamespace(registry=registry, proof_links=())

    class FakeProofRule:
        GIVEN = object()
        INFERENCE = object()

    # Only the externally imported collaborators are stubbed. The real
    # audit.run(), including its final snapshot and JSON write, executes.
    def stub(name: str, **attributes: object) -> None:
        module = ModuleType(name)
        for attribute, value in attributes.items():
            setattr(module, attribute, value)
        monkeypatch.setitem(sys.modules, name, module)

    parent = ModuleType("phase166_r3t_goal_source_binding")
    parent.__path__ = []
    monkeypatch.setitem(sys.modules, parent.__name__, parent)
    stub("expression", Multiple=FakeMultiple)
    stub("homotopy_groups", FiniteCyclicGroup=FakeFiniteCyclic)
    stub("phase165_r12_r2_quotient_rules", CyclicStructureStatement=FakeCyclic)
    stub("phase165_r12_r11_prop42_unified", prefer_universal_prop42_derivation=lambda bridge: bridge)
    stub("phase165_r52_r16_web_citation_gate", screen_shared_proof_context=lambda *args, **kwargs: screened)
    stub(
        "phase165_r52_r9_shared_math",
        build_shared_typed_bridge=lambda: complete,
        shared_expansion_provider=lambda *args, **kwargs: (lambda goal_value: ()),
    )
    search_result = SimpleNamespace(
        status="search_failed", conclusion=None,
        proven_steps=(), open_goals=(goal,),
    )
    stub(
        "phase165_r55_nk_only_goal",
        registered_group_goal_candidates=lambda *args, **kwargs: (goal,),
        search_group_from_registered_goal=lambda *args, **kwargs: search_result,
    )
    stub(
        "phase166_r3t_goal_source_binding.goal_source",
        resolve_specialized_goal_citing_id=lambda *args, **kwargs: audit.EXPECTED_TARGET,
    )
    stub("phase166_r3c_publication_order", precedes_citing_assertion=lambda *args: True)
    stub("proof", ProofRule=FakeProofRule)

    monkeypatch.setattr(
        audit, "matching_cited_steps",
        lambda bridge, suffix: ((source_id, double),)
        if suffix == audit.EXPECTED_DOUBLE_SUFFIX else ((hopf_id, "hopf"),),
    )
    monkeypatch.setattr(
        audit, "expansion_inventory",
        lambda goal_value, provider, bridge: {
            "count": 2, "rules": {"audited candidate": 2}, "examples": [],
        },
    )
    monkeypatch.setattr(
        audit, "source_inventory",
        lambda bridge: {locator: {"count": 0} for locator in audit.LOCATORS},
    )
    assert audit.run(original_root, dry_run=False, search=search) == 0
    assert observed_roots == [original_root, original_root]
    reports = list((recovery / "EHPProofTracerRecovery").glob("phase171_r2f_*/audit.json"))
    assert len(reports) == 1
    report = json.loads(reports[0].read_text(encoding="utf-8"))
    assert report["git_after_identical"] is True
    assert report["root_expansions"]["rules"] == {"audited candidate": 2}
    assert (report["runtime_search"] is not None) is search
```

## 新規 install.py 全文

```python
"""Guarded, idempotent two-file repair of the R2F audit's root variable.

This installer never invokes checkout/reset or changes application proof code.
Only pre-reviewed original R2F audit files or already-repaired files are accepted.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import os
from pathlib import Path
import sys
import tempfile
import traceback


REPO = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class PatchSpec:
    relative_target: str
    full_source_name: str
    original_sha256: str
    updated_sha256: str


PATCHES = (
    PatchSpec(
        "phase171_r2f_pi63_extension_gap_audit/audit.py",
        "audit_FULL.py",
        "350e32844dd24b73ccde87e2a7ca2da8060e62f8ded794759e05737c66320ae4",
        "6ad8575297dcb7689a3f19f1fedf0992dae3c106cd7502d74062b56e466d3756",
    ),
    PatchSpec(
        "phase171_r2f_pi63_extension_gap_audit/tests/test_audit.py",
        "test_audit_FULL.py",
        "aa55bfee677b65f65a03514d747c449524dcf096069da6157e686e2720a51044",
        "f8fff0efd46771ff4e6cd09eb86a62dc981e56e2ff615a134641d3a4f0330e64",
    ),
)


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def preflight(repo: Path = REPO, package: Path = PACKAGE) -> tuple[dict, ...]:
    """Reject modified user files and invalid bundle templates before any write."""
    reviewed = []
    for spec in PATCHES:
        target = repo / spec.relative_target
        source = package / spec.full_source_name
        if not target.is_file() or not source.is_file():
            raise RuntimeError("required R2F audit/repair file missing: " + spec.relative_target)
        payload = source.read_bytes()
        if digest(payload) != spec.updated_sha256:
            raise RuntimeError("repair template checksum mismatch: " + spec.relative_target)
        previous = target.read_bytes()
        current_hash = digest(previous)
        if current_hash == spec.original_sha256:
            state = "NEEDS_REPAIR"
        elif current_hash == spec.updated_sha256:
            state = "ALREADY_REPAIRED"
        else:
            raise RuntimeError(
                "unrecognized local edits; refusing to overwrite: " + spec.relative_target
            )
        reviewed.append({
            "target": target,
            "source": source,
            "previous": previous,
            "updated": payload,
            "original_sha256": current_hash,
            "spec": spec,
            "state": state,
        })
    return tuple(reviewed)


def atomic_replace(path: Path, payload: bytes) -> None:
    """Write one verified template atomically; preserve existing content on failure."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".r2f_r1_", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def apply(repo: Path = REPO, package: Path = PACKAGE) -> None:
    """Backup exact originals outside the repo and repair only matching audit files."""
    reviewed = preflight(repo, package)
    changes = [entry for entry in reviewed if entry["state"] == "NEEDS_REPAIR"]
    if not changes:
        print("PHASE171_R2F_R1_ALREADY_REPAIRED=True", flush=True)
        return
    backup_parent = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    backup = backup_parent / (
        "phase171_r2f_r1_fix_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    )
    backup.mkdir(parents=True, exist_ok=False)
    # Finish backups before touching any target.
    for entry in changes:
        name = str(entry["spec"].relative_target).replace("/", "__")
        path = backup / (name + ".before")
        path.write_bytes(entry["previous"])
        if digest(path.read_bytes()) != entry["original_sha256"]:
            raise RuntimeError("failed to verify backup: " + str(path))
    written = []
    try:
        for entry in changes:
            target = entry["target"]
            if digest(target.read_bytes()) != entry["original_sha256"]:
                raise RuntimeError("concurrent edit detected; refusing to replace: " + str(target))
            atomic_replace(target, entry["updated"])
            if digest(target.read_bytes()) != entry["spec"].updated_sha256:
                raise RuntimeError("repair write verification failed: " + str(target))
            written.append(entry)
    except Exception:
        # Restore only files still matching the bytes we just installed.
        for entry in reversed(written):
            target = entry["target"]
            if digest(target.read_bytes()) == entry["spec"].updated_sha256:
                atomic_replace(target, entry["previous"])
        raise
    print("PHASE171_R2F_R1_BACKUP=" + str(backup), flush=True)
    for entry in changes:
        print("PHASE171_R2F_R1_PATCHED=" + entry["spec"].relative_target, flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "apply"))
    args = parser.parse_args()
    try:
        reviewed = preflight()
        for entry in reviewed:
            print("PHASE171_R2F_R1_PREFLIGHT=" + entry["spec"].relative_target
                  + ":" + entry["state"], flush=True)
        if args.action == "apply":
            apply()
        print("PHASE171_R2F_R1_RESULT=PASS_" + args.action.upper(), flush=True)
        return 0
    except Exception as exc:
        print("PHASE171_R2F_R1_ERROR=" + f"{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        print(traceback.format_exc()[-2200:], file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規インストーラー単体テスト全文

```python
"""Unit tests for guarded and repeatable R2F root-collision repair."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

from phase171_r2f_r1_root_shadow_fix import install


def fixture_paths(monkeypatch, tmp_path: Path):
    repo = tmp_path / "repo"
    package = tmp_path / "package"
    repo.mkdir()
    package.mkdir()
    target = repo / "audit.py"
    source = package / "audit_FULL.py"
    original = b"old verified audit\n"
    updated = b"new verified audit\n"
    target.write_bytes(original)
    source.write_bytes(updated)
    monkeypatch.setattr(install, "PATCHES", (
        install.PatchSpec(
            "audit.py", "audit_FULL.py",
            sha256(original).hexdigest(), sha256(updated).hexdigest(),
        ),
    ))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "recovery"))
    return repo, package, target, original, updated


def test_check_never_modifies_existing_files(monkeypatch, tmp_path: Path) -> None:
    repo, package, target, original, updated = fixture_paths(monkeypatch, tmp_path)
    result = install.preflight(repo, package)
    assert len(result) == 1
    assert result[0]["state"] == "NEEDS_REPAIR"
    assert target.read_bytes() == original


def test_apply_is_idempotent_and_backs_up_original(monkeypatch, tmp_path: Path) -> None:
    repo, package, target, original, updated = fixture_paths(monkeypatch, tmp_path)
    install.apply(repo, package)
    assert target.read_bytes() == updated
    backups = list((tmp_path / "recovery" / "EHPProofTracerRecovery").glob(
        "phase171_r2f_r1_fix_*/audit.py.before"
    ))
    assert len(backups) == 1
    assert backups[0].read_bytes() == original
    install.apply(repo, package)
    assert target.read_bytes() == updated
    assert len(list((tmp_path / "recovery" / "EHPProofTracerRecovery").glob(
        "phase171_r2f_r1_fix_*/audit.py.before"
    ))) == 1


def test_unrecognized_edit_is_rejected_without_overwrite(monkeypatch, tmp_path: Path) -> None:
    repo, package, target, original, updated = fixture_paths(monkeypatch, tmp_path)
    target.write_bytes(b"user-customized audit\n")
    with pytest.raises(RuntimeError, match="refusing to overwrite"):
        install.apply(repo, package)
    assert target.read_bytes() == b"user-customized audit\n"
    assert not (tmp_path / "recovery").exists()


def test_bundle_corruption_is_rejected_without_overwrite(monkeypatch, tmp_path: Path) -> None:
    repo, package, target, original, updated = fixture_paths(monkeypatch, tmp_path)
    (package / "audit_FULL.py").write_bytes(b"corrupted bundle\n")
    with pytest.raises(RuntimeError, match="checksum mismatch"):
        install.apply(repo, package)
    assert target.read_bytes() == original
```

## 新規 run.ps1 全文

```powershell
param(
    [switch] $DryRun,
    [switch] $Search
)
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = (Resolve-Path (Join-Path $package '..')).Path
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location $repo
try {
    python -B -m phase171_r2f_r1_root_shadow_fix.install check
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2F_R1_PREFLIGHT_FAILED' }

    if ($DryRun.IsPresent) {
        python -B -m phase171_r2f_pi63_extension_gap_audit.audit --root $repo --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2F_R1_AUDIT_DRY_RUN_FAILED' }
        Write-Host 'PHASE171_R2F_R1_RESULT=PASS_DRY_RUN'
        return
    }

    python -B -m phase171_r2f_r1_root_shadow_fix.install apply
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2F_R1_INSTALL_FAILED' }

    $tests = @(
        'phase171_r2f_pi63_extension_gap_audit/tests/test_audit.py',
        'phase171_r2f_r1_root_shadow_fix/tests/test_install.py',
        'phase171_r2e_toda53_double_source/tests/test_source.py',
        'phase169_r3h_toda53_hopf_source/tests/test_phase169_r3h_toda53_hopf_source.py',
        'test_phase165_r52_r9_shared_math.py'
    )
    python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider @tests
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2F_R1_FOCUSED_PYTEST_FAILED' }
    Write-Host 'PHASE171_R2F_R1_FOCUSED_PYTEST=PASS'

    $auditArgs = @('-B', '-m', 'phase171_r2f_pi63_extension_gap_audit.audit', '--root', $repo)
    if ($Search.IsPresent) { $auditArgs += '--search' }
    & python @auditArgs
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2F_R1_AUDIT_FAILED' }
    Write-Host 'PHASE171_R2F_R1_RESULT=PASS'
}
finally {
    Pop-Location
}
```

## 新規 README.md 英語全文

```markdown
# Phase 171 R2F-R1 — Root Variable Collision Fix

This narrow corrective package fixes a local-variable collision in the existing read-only Phase 171 R2F audit. The audit's `run(root: Path, ...)` function previously reused `root` to store a dictionary of backward expansions, which then caused `snapshot(root)` to raise `TypeError` after the focused tests passed.

Only two previously created R2F audit files are changed: `phase171_r2f_pi63_extension_gap_audit/audit.py` and `phase171_r2f_pi63_extension_gap_audit/tests/test_audit.py`. In `run()`, the expansion result is renamed `root_frontier`; a parameterized regression test covers normal and optional-search execution. No application code, EHP rule, proof step, registered mathematical source, or existing R2E file is changed.

`run.ps1 -DryRun` verifies that both original audit files have the exact reviewed SHA-256 hashes and runs the existing audit's Git-state dry-run. `run.ps1` applies the guarded, idempotent repair, runs only focused tests, and executes the ordinary R2F audit. `run.ps1 -Search` additionally executes the existing registered group search. Unrecognized local edits are rejected without modification.

The installer backs up each original file outside the repository under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2f_r1_fix_*`. The existing audit continues writing its report under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2f_*\audit.json`. No Git checkout, reset, pull, or synchronization is performed.

This repair addresses audit execution only; it does **not** establish a completed proof of the group structure of pi_6(S^3). Run the complete test suite only at Phase 171 closeout.
```

## 新規 監査仕様.md 日本語全文

```markdown
# Phase 171 R2F-R1 — 監査終了時の変数衝突修正

## 判明した原因

`audit.py` の `run(root: Path, *, dry_run: bool, search: bool)` の内部で、入力 `root`（リポジトリの `Path`）へ `expansion_inventory()` の結果である辞書を再代入した。最後の `snapshot(root)` が辞書を `subprocess.run(..., cwd=root)` に渡したため `TypeError` となった。乾式監査と限定 pytest が通過し、通常監査だけが失敗した理由もこれに一致する。

## 変更対象と境界

- 既存 `phase171_r2f_pi63_extension_gap_audit/audit.py`：`run()` のみを全文置換。監査結果を `root_frontier` に保持し、`Path` の `root` は維持する。
- 既存 `phase171_r2f_pi63_extension_gap_audit/tests/test_audit.py`：`test_normal_run_preserves_path_after_root_frontier` を末尾に追加。通常監査と `-Search` の両方を検証する。
- 新規 `phase171_r2f_r1_root_shadow_fix/`：監査用の全文ソース、厳格なハッシュ検査付きインストーラー、PowerShell 実行スクリプト、その単体テストと説明文書。

トップレベル import は変更しない。既存の数学的ルール、Proof Tree、Reference、DB、R2E のソースは変更しない。

## 保護方針

取り込み前に変更対象の全ファイルが配布元 R2F の元ハッシュまたは本修正済みハッシュと一致することを確認する。独自編集を検出した場合は上書きしない。更新前に元ファイルをリポジトリ外へ保存する。再実行時に修正済みファイルは変更しない。Git の reset、checkout、pull は行わない。

## 検証

修正前に新しい回帰テスト2ケースが失敗し、修正後に同じ2ケースが成功することを確認する。監査用テスト9件と保護インストーラーテスト4件を限定実行する。ユーザーのローカルで `run.ps1` を実行した際には、R2E および既存 shared math の限定 pytest も再実行し、監査終了と JSON 出力を確認する。

全体 pytest は実行しない。最終的な `CyclicStructureStatement(\pi_6^3,\nu',4)` の証明は未完了として扱う。
```

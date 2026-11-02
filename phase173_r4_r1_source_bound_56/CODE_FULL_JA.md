# Phase 173 R4-R1：追加コード・テスト全文

変更対象は新規の `phase173_r4_r1_source_bound_56/` 内のファイルのみ。既存ファイル・クラス・関数の変更はありません。次 Phase の処理は先取りしません。

### __init__.py（全文）

```python
"""Phase 173 R4-R1: guarded Toda (5.6) proposal, without production mutation."""
```

### rule.py（全文）

```python
"""Source-bound pi_7^4 decomposition: only a backward proposal, never a GIVEN.

The general Toda Proposition 4.4 source is a mandatory screened leaf.
The pi_6^3 prior must pass the published-prior source ordering rule.
The diagonal pi_7^7 relation and H(nu_4)=iota_7 must be independently
proved INFERENCE steps. A DB goal or candidate generator is not evidence.
"""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, MapApplication
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3m_prior_result_catalog.prior_results import resolve_prior_group_result
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import EHP_H_MAP


def _target_generators(goal: object) -> tuple[HomotopyElement, HomotopyElement] | None:
    """Match the exact current typed target; do not repair symbolic mismatches."""
    if not (
        isinstance(goal, Relation)
        and goal.relation_type is RelationType.EQUALITY
        and goal.lhs == TodaPrimaryGroup(7, 4)
        and isinstance(goal.rhs, DirectSumGroup)
        and len(goal.rhs.summands) == 2
    ):
        return None
    free, torsion = goal.rhs.summands
    if not (
        isinstance(free, FreeCyclicGroup)
        and isinstance(torsion, FiniteCyclicGroup)
        and type(torsion.order) is int and torsion.order == 4
        and isinstance(free.generator, HomotopyElement)
        and isinstance(torsion.generator, IteratedSuspension)
        and type(torsion.generator.exponent) is int
        and torsion.generator.exponent == 1
        and isinstance(torsion.generator.expression, HomotopyElement)
    ):
        return None
    nu4 = free.generator
    prime = torsion.generator.expression
    if not (
        nu4.dimension == 4 and nu4.source == 7 and nu4.target == 4
        and isinstance(nu4.generator, GeneratorSymbol)
        and nu4.generator.family == "ν" and nu4.generator.index == 4
        and prime.dimension == 3 and prime.source == 6 and prime.target == 3
        and isinstance(prime.generator, GeneratorSymbol)
        and prime.generator.family in ("\\nu'", "ν")
        and (prime.generator.family == "\\nu'" or prime.generator.decoration == "′")
    ):
        return None
    return nu4, prime


def _diagonal_goal(bridge: object) -> Relation | None:
    """Require the independently registered pi_7^7 goal with its identity."""
    candidates = registered_group_goal_candidates(bridge, n=7, k=0)
    if len(candidates) != 1:
        return None
    relation = candidates[0]
    if not (
        isinstance(relation, Relation)
        and relation.relation_type is RelationType.EQUALITY
        and relation.lhs == TodaPrimaryGroup(7, 7)
        and isinstance(relation.rhs, FreeCyclicGroup)
        and isinstance(relation.rhs.generator, HomotopyElement)
    ):
        return None
    iota = relation.rhs.generator
    if not (
        isinstance(iota.generator, GeneratorSymbol)
        and iota.generator.family == "ι" and iota.generator.index == 7
        and iota.dimension == 7
    ):
        return None
    return relation


def source_bound_toda56_rule(
    goal: Relation, prior_relation: Relation, diagonal: Relation, hopf: Relation,
) -> InferenceRule:
    """Derive the exact presentation only after four proved typed premises."""
    generators = _target_generators(goal)
    if generators is None or not isinstance(prior_relation, Relation):
        raise ValueError("Exact pi_7^4 target and typed prior relation required")
    nu4, prime = generators
    expected_prior = Relation(
        TodaPrimaryGroup(6, 3), FiniteCyclicGroup(4, prime), RelationType.EQUALITY,
    )
    if prior_relation != expected_prior:
        raise ValueError("The pi_6^3 generator is not the target's suspended generator")
    if not (
        isinstance(diagonal, Relation)
        and diagonal.relation_type is RelationType.EQUALITY
        and diagonal.lhs == TodaPrimaryGroup(7, 7)
        and isinstance(diagonal.rhs, FreeCyclicGroup)
        and isinstance(diagonal.rhs.generator, HomotopyElement)
        and diagonal.rhs.generator.generator is not None
        and diagonal.rhs.generator.generator.family == "ι"
        and diagonal.rhs.generator.generator.index == 7
    ):
        raise ValueError("An independently typed diagonal generator is required")
    exact_hopf = Relation(
        MapApplication(map=EHP_H_MAP, expression=nu4),
        diagonal.rhs.generator,
        RelationType.EQUALITY,
    )
    if hopf != exact_hopf:
        raise ValueError("The independent n=4 Hopf-invariant premise differs")
    universal = TodaProp44UniversalStatement()
    expected = (universal, expected_prior, diagonal, exact_hopf)

    def guard(premises, bindings):
        return (
            len(premises) == 4
            and tuple(step.conclusion for step in premises) == expected
            and premises[0].rule is ProofRule.GIVEN
            and premises[2].rule is ProofRule.INFERENCE
            and premises[3].rule is ProofRule.INFERENCE
        )

    return InferenceRule(
        name="Toda (5.6) pi_7^4 source-bound direct-sum presentation",
        description=(
            "Specialize cited Toda Proposition 4.4 at n=4, i=7 using the "
            "independently proved Hopf invariant H(nu_4)=iota_7. Its map "
            "(alpha,beta) -> E(alpha)+nu_4 composed with beta sends "
            "nu-prime to E nu-prime and identity iota_7 to nu_4. "
            "Transport the independently proved pi_6^3 and pi_7^7 "
            "presentations along this isomorphism; no DB result is an axiom."
        ),
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.GIVEN,
                           statement_type=TodaProp44UniversalStatement,
                           statement_pattern=universal),
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=expected_prior),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=diagonal),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=exact_hopf),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Proposition 4.4", locator="Proposition 4.4",
        ),
    )


def expand_source_bound_toda56(
    goal: object, available: tuple[object, ...], bridge: object, *, proof_target: object,
) -> tuple[GoalExpansion, ...]:
    """Offer one sound root; proof search must discharge all four subgoals."""
    if not isinstance(available, tuple):
        raise TypeError("screened available claims must be a tuple")
    generators = _target_generators(goal)
    if generators is None or goal != proof_target:
        return ()
    if sum(type(x) is TodaProp44UniversalStatement and x == TodaProp44UniversalStatement()
           for x in available) != 1:
        return ()
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        return ()
    prior = resolve_prior_group_result(
        bridge, source_n=3, source_k=3, citing_assertion_id=citing_id,
    )
    if not prior.eligible or prior.relation is None:
        return ()
    diagonal = _diagonal_goal(bridge)
    if diagonal is None:
        return ()
    nu4, _ = generators
    hopf = Relation(
        MapApplication(map=EHP_H_MAP, expression=nu4),
        diagonal.rhs.generator,
        RelationType.EQUALITY,
    )
    try:
        rule = source_bound_toda56_rule(goal, prior.relation, diagonal, hopf)
    except ValueError:
        return ()
    return (GoalExpansion(
        rule, (TodaProp44UniversalStatement(), prior.relation, diagonal, hopf),
    ),)
```

### audit.py（全文）

```python
"""Opt-in, read-only check of a source-bound Toda (5.6) root provider."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
from typing import Any

REVIEWED_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "sources/toda/Toda_04_2.tex": "4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7",
    "phase165_r52_r9_shared_math.py": "2718c55789af7f442ac2c086d016d3d6f7ca3133",
    "phase165_r52_r27_r5_literature.py": "c9bfe2788f4cf043db6dada98a437afea6accf75",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase169_r3m_prior_result_catalog/prior_results.py": "c522cbaf924b3a9aa500d453b8eb6a1a66c42611",
    "toda_rules.py": "77f4159644f10eff65a79f6e528cf7b471c6ddc9",
    "phase165_r52_r16_web_citation_gate.py": "d1138c0450f234b6da761902ed7358b6038a19c8",
    "phase166_r3t_goal_source_binding/goal_source.py": "e13a07bbc0b6494b0c3c9b891784fe7378448756",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "phase165_r57_r11_proof_order_gate.py": "1ad9dfe8bb3da061cbee0dbd7a11c196f3f50604",
}


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=root, text=True, encoding="utf-8",
        capture_output=True, check=True,
    )
    return result.stdout.strip()


def preflight(root: Path) -> dict[str, Any]:
    """Allow audit-only HEAD advances, never production source drift."""
    if _git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Only reviewed develop is supported")
    head = _git(root, "rev-parse", "HEAD")
    checked = []
    for path, expected in REVIEWED_BLOBS.items():
        actual = _git(root, "rev-parse", "HEAD:" + path)
        if actual != expected:
            raise RuntimeError("Reviewed production blob changed: " + path)
        diff = subprocess.run(
            ("git", "diff", "--quiet", "HEAD", "--", path),
            cwd=root, capture_output=True, check=False,
        )
        if diff.returncode != 0:
            raise RuntimeError("Reviewed production working file changed: " + path)
        checked.append(path)
    return {"head": head, "verified_files": checked, "tracked_file_changes": []}


def inspect_runtime() -> dict[str, Any]:
    """Use the existing source-screening and first-success search with one extra provider."""
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, search_shared_group_goal, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin
    from phase173_r4_r1_source_bound_56.rule import expand_source_bound_toda56

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=4, k=3)
    if len(goals) != 1:
        raise RuntimeError("Expected one independently registered pi_7^4 goal")
    goal = goals[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        raise RuntimeError("Pi_7^4 has no uniquely positioned citing assertion")
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    )
    screened = prefer_universal_prop42_derivation(screened)
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )

    def local_provider(statement: object):
        return expand_source_bound_toda56(
            statement, available, screened, proof_target=goal,
        )

    proposed = local_provider(goal)
    if len(proposed) > 1:
        raise RuntimeError("Ambiguous Toda (5.6) root proposals")
    combined = shared_expansion_provider(
        screened, extra_providers=(local_provider,), proof_target=goal,
    )
    root_rules = [option.rule.name for option in combined(goal)]
    result = search_shared_group_goal(
        n=4, k=3, group_structure=goal.rhs,
        bridge=bridge, citing_assertion_id=citing_id,
        expansion_provider=combined,
    )
    status = getattr(result.status, "value", str(result.status))
    complete = status == "complete"
    if complete and result.conclusion != goal:
        raise RuntimeError("A completed proof has an unexpected conclusion")
    return {
        "goal": repr(goal), "citing_assertion_id": citing_id,
        "source_bound_root_count": len(proposed),
        "source_bound_subgoals": [
            {"type": type(p).__name__, "statement": repr(p)}
            for option in proposed for p in option.subgoals
        ],
        "combined_root_rule_names": root_rules,
        "proof_search_status": status,
        "complete": complete,
        "open_goals": [repr(item) for item in getattr(result, "open_goals", ())],
        "diagnostics": [str(item) for item in getattr(result, "diagnostics", ())],
        "production_provider_changed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    pre = preflight(root)
    print("PHASE173_R4_R1_SOURCE_BOUND_SOURCE_GUARD=PASS")
    if args.dry_run:
        print("PHASE173_R4_R1_SOURCE_BOUND_DRY_RUN=PASS")
        return 0
    runtime = inspect_runtime()
    report = {
        "phase": "173-R4-R1", "scope": "ISOLATED_PROOF_PROPOSAL",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "preflight": pre,
        "runtime": runtime,
        "production_changes": [],
    }
    path = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / (
        "EHPProofTracerRecovery/phase173_r4_r1_source_bound_56/audit.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PHASE173_R4_R1_SOURCE_BOUND_ROOTS=" + str(runtime["source_bound_root_count"]))
    for index, subgoal in enumerate(runtime["source_bound_subgoals"], 1):
        print("PHASE173_R4_R1_SUBGOAL_" + str(index) + "=" + subgoal["type"] + " " + subgoal["statement"])
    print("PHASE173_R4_R1_SEARCH_STATUS=" + str(runtime["proof_search_status"]))
    print("PHASE173_R4_R1_COMPLETE=" + str(runtime["complete"]))
    print("PHASE173_R4_R1_REPORT=" + str(path))
    print("PHASE173_R4_R1_NO_PRODUCTION_CHANGES=True")
    print("PHASE173_R4_R1_SOURCE_BOUND_AUDIT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### tests/test_rule.py（全文）

```python
"""Focused proof-contract tests using actual EHP Proof Tracer types."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, MapApplication
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase173_r4_r1_source_bound_56.rule import (
    _target_generators, source_bound_toda56_rule,
    expand_source_bound_toda56,
)
from proof import ProofRule, Relation, RelationType
from toda_rules import EHP_H_MAP


def fixture_relations():
    nu4 = HomotopyElement(
        name="ν₄", dimension=4, source=7, target=4,
        generator=GeneratorSymbol(family="ν", index=4),
    )
    prime = HomotopyElement(
        name="ν'", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="\\nu'", index=None),
    )
    iota = HomotopyElement(
        name="ι_7", dimension=7, generator=GeneratorSymbol(family="ι", index=7),
    )
    goal = Relation(
        TodaPrimaryGroup(7, 4),
        DirectSumGroup((FreeCyclicGroup(nu4),
                        FiniteCyclicGroup(4, IteratedSuspension(prime, 1)))),
        RelationType.EQUALITY,
    )
    prior = Relation(TodaPrimaryGroup(6, 3), FiniteCyclicGroup(4, prime), RelationType.EQUALITY)
    diagonal = Relation(TodaPrimaryGroup(7, 7), FreeCyclicGroup(iota), RelationType.EQUALITY)
    hopf = Relation(MapApplication(EHP_H_MAP, nu4), iota, RelationType.EQUALITY)
    return goal, prior, diagonal, hopf


def test_exact_target_is_typed() -> None:
    goal, prior, diagonal, hopf = fixture_relations()
    assert _target_generators(goal) is not None
    assert source_bound_toda56_rule(goal, prior, diagonal, hopf).conclusion_pattern == goal


def test_wrong_prime_generator_is_rejected() -> None:
    goal, prior, diagonal, hopf = fixture_relations()
    wrong = Relation(prior.lhs, FiniteCyclicGroup(4, goal.rhs.summands[0].generator), RelationType.EQUALITY)
    with pytest.raises(ValueError):
        source_bound_toda56_rule(goal, wrong, diagonal, hopf)


def test_wrong_hopf_image_is_rejected() -> None:
    goal, prior, diagonal, hopf = fixture_relations()
    wrong = Relation(hopf.lhs, goal.rhs.summands[0].generator, RelationType.EQUALITY)
    with pytest.raises(ValueError):
        source_bound_toda56_rule(goal, prior, diagonal, wrong)


def test_rule_requires_given_source_and_derived_hopf() -> None:
    goal, prior, diagonal, hopf = fixture_relations()
    rule = source_bound_toda56_rule(goal, prior, diagonal, hopf)
    steps = (
        SimpleNamespace(conclusion=TodaProp44UniversalStatement(), rule=ProofRule.GIVEN),
        SimpleNamespace(conclusion=prior, rule=ProofRule.INFERENCE),
        SimpleNamespace(conclusion=diagonal, rule=ProofRule.INFERENCE),
        SimpleNamespace(conclusion=hopf, rule=ProofRule.INFERENCE),
    )
    assert rule.match_guard(steps, {}) is True
    replaced = (*steps[:3], SimpleNamespace(conclusion=hopf, rule=ProofRule.GIVEN))
    assert rule.match_guard(replaced, {}) is False


def test_no_citation_means_no_root(monkeypatch) -> None:
    goal, prior, diagonal, hopf = fixture_relations()
    assert expand_source_bound_toda56(
        goal, (), object(), proof_target=goal,
    ) == ()


def test_no_root_for_other_group() -> None:
    goal, prior, diagonal, hopf = fixture_relations()
    other = Relation(TodaPrimaryGroup(8, 5), goal.rhs, RelationType.EQUALITY)
    assert _target_generators(other) is None
```

### tests/test_preflight.py（全文）

```python
"""Offline-focused protection tests; no production imports or Git writes."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_r4_r1_source_bound_56 import audit


def test_preflight_accepts_only_exact_reviewed_blobs(monkeypatch, tmp_path: Path) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "audit-only-new-head"
        if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return audit.REVIEWED_BLOBS[args[1][5:]]
        raise AssertionError(args)

    monkeypatch.setattr(audit, "_git", fake_git)
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0))
    result = audit.preflight(tmp_path)
    assert result["head"] == "audit-only-new-head"
    assert len(result["verified_files"]) == len(audit.REVIEWED_BLOBS)


def test_preflight_rejects_modified_source_blob(monkeypatch, tmp_path: Path) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "audit-only-new-head"
        if args == ("rev-parse", "HEAD:sources/toda/Toda_05_2.tex"):
            return "tampered"
        if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return audit.REVIEWED_BLOBS[args[1][5:]]
        raise AssertionError(args)

    monkeypatch.setattr(audit, "_git", fake_git)
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0))
    with pytest.raises(RuntimeError, match="Reviewed production blob changed"):
        audit.preflight(tmp_path)


def test_preflight_rejects_modified_worktree_source(monkeypatch, tmp_path: Path) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "audit-only-new-head"
        if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return audit.REVIEWED_BLOBS[args[1][5:]]
        raise AssertionError(args)

    monkeypatch.setattr(audit, "_git", fake_git)
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=1))
    with pytest.raises(RuntimeError, match="production working file changed"):
        audit.preflight(tmp_path)


def test_preflight_rejects_wrong_branch(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "_git", lambda *a: "main")
    with pytest.raises(RuntimeError, match="develop"):
        audit.preflight(tmp_path)


def test_reviewed_manifest_contains_original_source_and_provider() -> None:
    assert "sources/toda/Toda_04_2.tex" in audit.REVIEWED_BLOBS
    assert "phase165_r52_r9_shared_math.py" in audit.REVIEWED_BLOBS
    assert "toda_rules.py" in audit.REVIEWED_BLOBS
```

### run.ps1（全文）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
    Write-Output 'PHASE173_R4_R1_SOURCE_BOUND_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider '.\phase173_r4_r1_source_bound_56\tests'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 source-bound focused tests failed' }
    Write-Output 'PHASE173_R4_R1_SOURCE_BOUND_FOCUSED_PYTEST=PASS'
    if ($DryRun) {
        python -m phase173_r4_r1_source_bound_56.audit --root $Root --dry-run
    } else {
        python -m phase173_r4_r1_source_bound_56.audit --root $Root
    }
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 source-bound run failed' }
} finally {
    Pop-Location
}
```

### README.md（全文）

```markdown
# Phase 173 R4-R1: Source-Bound Toda (5.6) Proof Candidate

This package provides a bounded, typed backward proof proposal for the
pi_7(S^4) direct-sum presentation. It does **not** mutate the production
provider or any existing tracked source file.

The rule requires an independently screened Toda Proposition 4.4 universal
reference, a publication-eligible prior pi_6(S^3) presentation, a proven
pi_7(S^7) diagonal presentation, and an independently derived Hopf-invariant
relation H(nu_4) = iota_7. In particular, a database goal or a literal
source string never counts as a proof step.

Run `run.ps1 -DryRun` before `run.ps1`. The standard shared backward search
is run with the new provider injected for this isolated process only. A new
root proposal does not constitute a completed proof. Inspect the reported
search status and open goals before considering production integration.

Only focused tests are run. No whole-suite pytest is executed.
```

### AUDIT_PLAN_JA.md（全文）

```markdown
# Phase 173 R4-R1：Toda (5.6) 出典付き候補の限定実装

## 対象

- 新規 `phase173_r4_r1_source_bound_56/rule.py`：`_target_generators`、`_diagonal_goal`、`source_bound_toda56_rule`、`expand_source_bound_toda56`。
- 新規 `phase173_r4_r1_source_bound_56/audit.py`：`_git`、`preflight`、`inspect_runtime`、`main`。
- 新規 `run.ps1`、限定テスト `tests/test_rule.py`、`README.md`、`__init__.py`。

既存クラス・既存関数・公式5文書は変更しない。全体 pytest は Phase 173 の終わりまで行わない。

## 数学的条件

Toda Proposition 4.4 の引用済み一般命題、先行する $\pi_6^3=\mathbb Z/4\{\nu'\}$、導出済み $\pi_7^7=\mathbb Z\{\iota_7\}$、独立に導出した $H(\nu_4)=\iota_7$ が4前提。H の関係は `ProofRule.INFERENCE` を必須とする。これが無ければルート候補は未完成のまま残す。

$$
(\alpha,\beta)\mapsto E\alpha+\nu_4\circ\beta
$$

により生成元 $\nu'$ は $E\nu'$ に、$\iota_7$ は $\nu_4$ に写る。DB Goal、出典テキスト、提案そのものを GIVEN にしない。

## 完了条件

1. 既存の reviewed blob が Git HEAD と作業ツリーで変わっていない。
2. 限定 pytest が PASS。
3. ソースの固定引用が1件で、Root が1件以下。
4. SearchStatus と OpenGoals を audit.json に記録する。
5. `COMPLETE=False` なら証明完成と宣言しない。

## 次の境界

今回の孤立した提案実装が数学的に成立することを確認してから、公開経路への常設接続を判断する。$\pi_8^5$ の位数8導出は R4-R2 の範囲とする。
```

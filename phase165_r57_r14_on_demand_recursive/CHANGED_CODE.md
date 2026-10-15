# R57-R14 変更コード全文

変更対象：`phase165_r52_r9_shared_math.py` の `search_shared_group_goal()`、新規 `phase165_r57_r14_recursive_search.py` の `search_recursively_in_proof_order()`、新規テスト6件、インストーラー。既存 import は変更しません。

## 変更後の `search_shared_group_goal()` 全文

```python
def search_shared_group_goal(*, n: int, k: int, group_structure: object,
                              bridge: RegistryBridgeResult | None = None,
                              expansion_provider=None,
                              citing_assertion_id: str | None = None,
                              verified_assertion_ids: tuple[str, ...] = (), completed_internal_proofs: tuple = (), proof_use_order=None,
                              ordered_completed_proofs: tuple = (), target_order: int | None = None,
                              proof_order_catalog=None, recursive_proof_order_catalog=None):
    """Run canonical search under a screened Reference context.

    Older calls retain their signature. R15 ordering is applied to sources
    outside the explicitly adopted-Tex policy; no IDs are auto-verified.
    """
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r57_r12_ordered_proofs import validate_prior_internal_proofs

    goal = Relation(TodaPrimaryGroup(n + k, n), group_structure)
    if recursive_proof_order_catalog is not None:
        from phase165_r57_r14_recursive_search import search_recursively_in_proof_order
        if (proof_order_catalog is not None or ordered_completed_proofs
                or completed_internal_proofs or target_order is not None):
            raise ValueError("recursive proof order cannot mix with saved or caller-supplied proofs")

        def search_one(statement, earlier, order):
            if (not isinstance(statement, Relation)
                    or not isinstance(statement.lhs, TodaPrimaryGroup)
                    or statement.relation_type is not RelationType.EQUALITY):
                raise TypeError("recursive catalog targets must be typed group relations")
            target = statement.lhs
            if (not isinstance(target.group_dimension, int)
                    or not isinstance(target.sphere_dimension, int)
                    or target.sphere_dimension < 2
                    or target.group_dimension < target.sphere_dimension):
                raise ValueError("recursive target must have concrete dimensions")
            return search_shared_group_goal(
                n=target.sphere_dimension,
                k=target.group_dimension - target.sphere_dimension,
                group_structure=statement.rhs,
                bridge=bridge,
                expansion_provider=expansion_provider,
                citing_assertion_id=citing_assertion_id,
                verified_assertion_ids=verified_assertion_ids,
                completed_internal_proofs=(),
                proof_use_order=proof_use_order,
                ordered_completed_proofs=earlier,
                target_order=order,
            )

        return search_recursively_in_proof_order(
            recursive_proof_order_catalog, goal, search_one,
        )
    if proof_order_catalog is not None:
        from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog
        if not isinstance(proof_order_catalog, ProofOrderCatalog):
            raise TypeError("proof_order_catalog must be ProofOrderCatalog")
        if ordered_completed_proofs or completed_internal_proofs or target_order is not None:
            raise ValueError("catalog proof order cannot be mixed with caller order")
        prior, target_order = proof_order_catalog.select_prior(goal)
    else:
        prior = validate_prior_internal_proofs(
            ordered_completed_proofs, target_order, completed_internal_proofs
        )
    if bridge is None:
        bridge = build_shared_typed_bridge()
    assertions = tuple(bridge.registry._assertions.values())
    if not assertions:
        raise ValueError("shared typed registry is empty")
    context_id = citing_assertion_id or assertions[0].assertion_id
    proof_context = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=context_id,
        verified_assertion_ids=verified_assertion_ids,
    )
    if proof_use_order == "registered":
        from phase165_r52_r19_prop51_binding import resolve_registered_proof_use_order
        proof_use_order = resolve_registered_proof_use_order(proof_context, goal)
    if proof_use_order is not None:
        from phase165_r52_r18_proof_order import restrict_by_proof_use_order
        proof_context = restrict_by_proof_use_order(
            proof_context, goal=goal, policy=proof_use_order,
        )
    if expansion_provider is None:
        expansion_provider = shared_expansion_provider(
            proof_context, proof_target=goal,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
    return search_registered_partial_proof(
        n=n, k=k, goal=goal, bridge=proof_context,
        citing_assertion_id=context_id,
        expansion_provider=expansion_provider,
        lookup_mode="typed_reference",
        structure_status=GroupStructureStatus.UNKNOWN,
        completed_internal_proofs=prior,
    )

```

## 新規モジュール全文（ファイル先頭に追加）

```python
"""R57-R14: recompute earlier proofs on demand; never store finished ProofSteps.

The catalog contains only independently reviewed positions and typed targets.
Every invocation has its own local cache and rejects cached/persisted roots.
"""
from __future__ import annotations

from collections.abc import Callable

from phase165_r52_r17_internal_dependency import CompletedInternalProof, same_statement
from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase165_r57_r12_ordered_proofs import OrderedCompletedProof
from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog
from proof import ProofRule, ProofStep


def search_recursively_in_proof_order(
    catalog: ProofOrderCatalog,
    goal: object,
    search_one: Callable[[object, tuple[OrderedCompletedProof, ...], int], PartialProofResult],
) -> PartialProofResult:
    """Run earlier searches afresh, then search the goal using proven earlier roots.

    Incomplete earlier results are never promoted. Only this invocation's local
    memoization is used; the catalog is not modified. A root must be an inferred
    step whose conclusion matches its registered target exactly.
    """
    if not isinstance(catalog, ProofOrderCatalog):
        raise TypeError("catalog must be ProofOrderCatalog")
    if not callable(search_one):
        raise TypeError("search_one must be callable")
    records = tuple(catalog._records)
    if any(record.completed is not None for record in records):
        raise ValueError("on-demand mode forbids registered completed proofs")
    matching = tuple(record for record in records if same_statement(record.statement, goal))
    if len(matching) != 1:
        raise ValueError("target has no unique registered proof order")
    ordered = tuple(sorted(records, key=lambda record: record.position))
    cache: dict[int, PartialProofResult] = {}
    completed: dict[int, CompletedInternalProof] = {}

    def resolve(position: int) -> PartialProofResult:
        if position in cache:
            return cache[position]
        record = next((item for item in ordered if item.position == position), None)
        if record is None:
            raise ValueError("unregistered proof position")
        for predecessor in ordered:
            if predecessor.position >= position:
                break
            resolve(predecessor.position)
        available = tuple(
            OrderedCompletedProof(completed[item.position], item.position)
            for item in ordered
            if item.position < position and item.position in completed
        )
        result = search_one(record.statement, available, position)
        if not isinstance(result, PartialProofResult):
            raise TypeError("search_one must return PartialProofResult")
        if result.status is ProofSearchStatus.COMPLETE:
            if not same_statement(result.conclusion, record.statement):
                raise ValueError("completed conclusion differs from registered target")
            roots = tuple(
                step for step in result.proven_steps
                if isinstance(step, ProofStep)
                and same_statement(step.conclusion, record.statement)
            )
            if len(roots) != 1 or roots[0].rule is not ProofRule.INFERENCE:
                raise ValueError("completed proof requires exactly one inferred root")
            completed[position] = CompletedInternalProof(roots[0])
        cache[position] = result
        return result

    return resolve(matching[0].position)

```

## テスト全文

```python
"""R57-R14: actual on-demand recursion, not stored proof replay."""
import pytest

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog, ProofOrderRecord
from phase165_r57_r14_recursive_search import search_recursively_in_proof_order
from proof import InferenceRule, PremisePattern, ProofRule, ProofStep, Relation, RelationType


def _target(n):
    return Relation(TodaPrimaryGroup(n + 1, n), FreeCyclicGroup(generator="formal-generator-" + str(n)), RelationType.EQUALITY)


def _catalog():
    catalog = ProofOrderCatalog()
    catalog.register(ProofOrderRecord(_target(2), 1))
    catalog.register(ProofOrderRecord(_target(3), 2))
    catalog.register(ProofOrderRecord(_target(4), 3))
    return catalog


def _result(statement, complete):
    n = statement.lhs.sphere_dimension
    if not complete:
        return make_partial_proof_result(n=n, k=1, status=ProofSearchStatus.SEARCH_FAILED,
                                         open_goals=(statement,), diagnostics=("not proved",))
    premise = ProofStep(conclusion="independent-source-" + str(n), premises=(), rule=ProofRule.GIVEN)
    rule = InferenceRule(name="test inference", premise_patterns=(PremisePattern(statement_type=str),),
                         conclusion_builder=lambda steps: statement)
    root = ProofStep(conclusion=statement, premises=(premise,), rule=ProofRule.INFERENCE,
                     inference_rule=rule)
    return make_partial_proof_result(n=n, k=1, status=ProofSearchStatus.COMPLETE,
                                     proven_steps=(premise, root), conclusion=statement)


def test_r14_generates_all_earlier_goals_before_target_without_persisting():
    catalog = _catalog()
    seen = []

    def search(goal, prior, position):
        seen.append((position, tuple(item.order for item in prior)))
        return _result(goal, True)

    result = search_recursively_in_proof_order(catalog, _target(4), search)
    assert result.status is ProofSearchStatus.COMPLETE
    assert seen == [(1, ()), (2, (1,)), (3, (1, 2))]
    assert all(record.completed is None for record in catalog._records)


def test_r14_does_not_reuse_failed_predecessor():
    seen = []

    def search(goal, prior, position):
        seen.append((position, tuple(item.order for item in prior)))
        return _result(goal, position != 2)

    search_recursively_in_proof_order(_catalog(), _target(4), search)
    assert seen == [(1, ()), (2, (1,)), (3, (1,))]


def test_r14_recomputes_proofs_for_each_request():
    calls = []

    def search(goal, prior, position):
        calls.append(position)
        return _result(goal, True)

    catalog = _catalog()
    search_recursively_in_proof_order(catalog, _target(4), search)
    search_recursively_in_proof_order(catalog, _target(4), search)
    assert calls == [1, 2, 3, 1, 2, 3]


def test_r14_rejects_persisted_roots_and_unknown_order():
    from phase165_r52_r17_internal_dependency import CompletedInternalProof
    previously = _result(_target(2), True)
    catalog = ProofOrderCatalog()
    catalog.register(ProofOrderRecord(_target(2), 1, CompletedInternalProof(previously.proven_steps[-1])))
    catalog.register(ProofOrderRecord(_target(3), 2))
    with pytest.raises(ValueError, match="forbids registered completed proofs"):
        search_recursively_in_proof_order(catalog, _target(3), lambda goal, prior, order: _result(goal, True))
    with pytest.raises(ValueError, match="registered proof order"):
        search_recursively_in_proof_order(_catalog(), _target(9), lambda goal, prior, order: _result(goal, True))


def test_r14_rejects_fake_completed_root():
    def fake(goal, prior, position):
        n = goal.lhs.sphere_dimension
        leaf = ProofStep(conclusion=goal, premises=(), rule=ProofRule.GIVEN)
        return make_partial_proof_result(n=n, k=1, status=ProofSearchStatus.COMPLETE,
                                         proven_steps=(leaf,), conclusion=goal)

    with pytest.raises(ValueError, match="inferred root"):
        search_recursively_in_proof_order(_catalog(), _target(4), fake)


def test_r14_shared_entry_exposes_on_demand_mode():
    from inspect import signature
    from phase165_r52_r9_shared_math import search_shared_group_goal
    assert "recursive_proof_order_catalog" in signature(search_shared_group_goal).parameters

```

## インストーラー全文

```python
"""Fail-closed, idempotent R57-R14 installer on top of R57-R13."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def install(root: Path, package: Path) -> str:
    destination = root / "phase165_r52_r9_shared_math.py"
    helper = root / "phase165_r57_r14_recursive_search.py"
    new_helper = (package / helper.name).read_bytes()
    if helper.exists() and helper.read_bytes() != new_helper:
        raise RuntimeError("conflicting recursive search helper")
    source = destination.read_text(encoding="utf-8")
    nodes = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)
             and node.name == "search_shared_group_goal"]
    if len(nodes) != 1:
        raise RuntimeError("shared group search must have one definition")
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    existing = "".join(lines[node.lineno - 1:node.end_lineno]).strip()
    expected = (package / "search_shared_group_goal.py.txt").read_text(encoding="utf-8").strip()
    if existing == expected:
        if not helper.exists():
            shutil.copy2(package / helper.name, helper)
        return "ALREADY_INSTALLED"
    prior = (package.parent / "phase165_r57_r13_proof_order_catalog" / "search_shared_group_goal.py.txt")
    if not prior.exists() or prior.read_text(encoding="utf-8").strip() != existing:
        raise RuntimeError("unexpected R57-R13 shared search; abort without changes")
    replacement = "".join(lines[:node.lineno - 1]) + expected + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(replacement)
    backup = destination.with_name(destination.name + ".r57_r14_before.bak")
    if not backup.exists():
        shutil.copy2(destination, backup)
    if not helper.exists():
        shutil.copy2(package / helper.name, helper)
    destination.write_text(replacement, encoding="utf-8")
    return "INSTALLED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("R57-R14:", install(package.parent, package))
    print("On-demand earlier-proof recursion; no ProofStep persisted; full pytest NOT run")

```

## PowerShell 実行コード全文

```powershell
$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
try {
  python "$package\install.py"
  if ($LASTEXITCODE -ne 0) { throw "R57-R14 install failed" }
  $tests = @(
    "$package\test_phase165_r57_r14_on_demand_recursive.py",
    "$root\phase165_r57_r13_proof_order_catalog\test_phase165_r57_r13_proof_order_catalog.py",
    "$root\phase165_r57_r12_ordered_internal_transport\test_phase165_r57_r12_ordered_internal_transport.py"
  )
  foreach ($test in $tests) {
    Write-Host "Running focused pytest: $test"
    python -m pytest -q "$test"
    if ($LASTEXITCODE -ne 0) { throw "Targeted pytest failed: $test" }
  }
  Write-Host "R57-R14 targeted tests passed; full pytest NOT run."
} finally {
  Pop-Location
}

```

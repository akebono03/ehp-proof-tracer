# R57-R15 変更コード全文

## 変更ファイル・関数

- `phase165_r52_r9_shared_math.py`: `search_shared_group_goal` 全文を置換。import 部は変更なし。
- `phase165_r55_nk_only_goal.py`: `search_group_from_registered_goal` 全文を置換。import 部は変更なし。
- `phase165_r57_r15_ordinary_recursive_connection/`: installer とテストを追加。

## `search_shared_group_goal` 全文

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
    if proof_order_catalog is not None and recursive_proof_order_catalog is None:
        from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog
        if not isinstance(proof_order_catalog, ProofOrderCatalog):
            raise TypeError("proof_order_catalog must be ProofOrderCatalog")
        if ordered_completed_proofs or completed_internal_proofs or target_order is not None:
            raise ValueError("catalog proof order cannot mix with caller-supplied proofs")
        if any(record.completed is not None for record in proof_order_catalog._records):
            raise ValueError("on-demand mode forbids registered completed proofs")
        recursive_proof_order_catalog = proof_order_catalog
        proof_order_catalog = None
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

## `search_group_from_registered_goal` 全文

```python
def search_group_from_registered_goal(*, n: int, k: int, bridge=None, proof_order_catalog=None):
    """Resolve a unique sourced target and run the existing screened backward search."""
    make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.NOT_SEARCHED)
    if bridge is None:
        bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=n, k=k)
    if len(candidates) != 1:
        explanation = (
            "群構造・生成元の型付き証明目標が文献命題台帳に未登録"
            if not candidates else
            "群構造の型付き候補が複数あり、証明目標を一意に選択できない"
        )
        return make_partial_proof_result(
            n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
            open_goals=(TodaPrimaryGroup(n + k, n),),
            diagnostics=(explanation,),
        )
    candidate = candidates[0]
    # The candidate is a requested conclusion, NEVER a GIVEN proof premise.
    # search_shared_group_goal screens exact-root fixed assertions.
    result = search_shared_group_goal(
        n=n, k=k, group_structure=candidate.rhs, bridge=bridge,
        proof_order_catalog=proof_order_catalog,
    )
    if (result.status is ProofSearchStatus.COMPLETE and result.conclusion == candidate):
        return replace(result, structure_status=GroupStructureStatus.KNOWN)
    return result
```

## 新規テスト全文

```python
"""R57-R15 focused integration and installer tests."""
import ast
from pathlib import Path

import pytest

from install import replace_function


def test_new_shared_search_has_automatic_catalog_recursion():
    text = (Path(__file__).parent / "search_shared_group_goal.py.txt").read_text(encoding="utf8")
    tree = ast.parse(text)
    assert len([n for n in tree.body if isinstance(n, ast.FunctionDef)]) == 1
    assert "recursive_proof_order_catalog = proof_order_catalog" in text
    assert "on-demand mode forbids registered completed proofs" in text
    assert "search_recursively_in_proof_order" in text


def test_selector_preserves_original_nk_contract():
    text = (Path(__file__).parent / "search_group_from_registered_goal.py.txt").read_text(encoding="utf8")
    node = ast.parse(text).body[0]
    assert node.name == "search_group_from_registered_goal"
    assert [v.arg for v in node.args.kwonlyargs] == ["n", "k", "bridge", "proof_order_catalog"]
    assert "proof_order_catalog=proof_order_catalog" in text


def test_installer_is_idempotent_and_fail_closed():
    old = "def f(x):\n    return x\n"
    new = "def f(x):\n    return x + 1\n"
    updated, changed = replace_function(old, "f", old, new)
    assert changed and "return x + 1" in updated
    same, changed = replace_function(updated, "f", old, new)
    assert not changed and same == updated
    with pytest.raises(RuntimeError, match="unexpected predecessor"):
        replace_function("def f(x):\n    return None\n", "f", old, new)


def test_reuses_existing_recursive_engine_not_saved_proofs():
    source = (Path(__file__).parent / "search_shared_group_goal.py.txt").read_text(encoding="utf8")
    assert "completed_internal_proofs=()" in source
    assert "ordered_completed_proofs=earlier" in source
    assert "target_order=order" in source


def test_no_new_given_or_group_specific_answers():
    source = (Path(__file__).parent / "search_shared_group_goal.py.txt").read_text(encoding="utf8")
    assert "ProofRule.GIVEN" not in source
    assert "\\pi_5^4" not in source
```

## インストーラー全文

```python
"""R57-R15 fail-closed installer. Preserve all unrelated R55/R14 code."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def replace_function(source: str, name: str, expected: str, desired: str) -> tuple[str, bool]:
    nodes = [n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(nodes) != 1:
        raise RuntimeError("expected exactly one function: " + name)
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    current = "".join(lines[node.lineno - 1:node.end_lineno]).strip()
    if current == desired.strip():
        return source, False
    if current != expected.strip():
        raise RuntimeError("unexpected predecessor function: " + name)
    result = "".join(lines[:node.lineno - 1]) + desired.rstrip("\n") + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(result)
    return result, True


def install(root: Path, package: Path) -> str:
    shared = root / "phase165_r52_r9_shared_math.py"
    selector = root / "phase165_r55_nk_only_goal.py"
    r14 = package.parent / "phase165_r57_r14_on_demand_recursive" / "search_shared_group_goal.py.txt"
    r55 = package.parent / "phase165_r55_nk_only_web" / "phase165_r55_nk_only_goal.py"
    if not r14.is_file() or not r55.is_file():
        raise RuntimeError("R57-R14 and R55 local source bundles are required")
    existing_shared = shared.read_text(encoding="utf8")
    existing_selector = selector.read_text(encoding="utf8")
    oldsel_tree = ast.parse(r55.read_text(encoding="utf8"))
    oldsel_node = next(n for n in oldsel_tree.body if isinstance(n, ast.FunctionDef) and n.name == "search_group_from_registered_goal")
    oldsel_lines = r55.read_text(encoding="utf8").splitlines(keepends=True)
    oldsel = "".join(oldsel_lines[oldsel_node.lineno - 1:oldsel_node.end_lineno])
    changes = []
    for path, current, name, expected, desired in (
        (shared, existing_shared, "search_shared_group_goal", r14.read_text(encoding="utf8"), (package / "search_shared_group_goal.py.txt").read_text(encoding="utf8")),
        (selector, existing_selector, "search_group_from_registered_goal", oldsel, (package / "search_group_from_registered_goal.py.txt").read_text(encoding="utf8")),
    ):
        updated, changed = replace_function(current, name, expected, desired)
        if changed:
            changes.append((path, updated))
    for path, updated in changes:
        backup = path.with_name(path.name + ".r57_r15_before.bak")
        if not backup.exists():
            shutil.copy2(path, backup)
        path.write_text(updated, encoding="utf8")
    return "INSTALLED" if changes else "ALREADY_INSTALLED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("R57-R15:", install(package.parent, package))
    print("Ordinary group search accepts on-demand proof-order catalog; no finished ProofStep persisted")
    print("Full pytest NOT run")
```

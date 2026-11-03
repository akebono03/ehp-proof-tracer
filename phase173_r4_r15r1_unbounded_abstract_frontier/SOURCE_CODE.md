# Phase 173 R4-R15R1 — 全コード提示

## 変更ファイル・クラス・関数

- 既存 `phase173_r4_r10_general_toda56_core/core.py`：`homotopy_groups` の import、`checked_general_inputs()` 全体。
- 同ファイル：`_abstract_group_signature()`、`checked_abstract_inputs()` を `checked_general_inputs()` の直前に新規追加。
- 変更対象のクラスはなし。
- 新規パッケージ：監査・インストール・限定テスト・実行スクリプト。

## 既存コードの変更後 import（全文）

```python
"""General, source-first Toda Proposition 4.4 inference proposals for n=4."""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step,
    exact_prior_database_result,
    group_coordinates,
    verified_db_step,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
)
from phase173_r4_r4_typed_generator_audit.audit import (
    _group_components,
    _map_components,
)
from phase173_r4_r6_alias_source_audit.audit import components_match_alias
from proof import (
    InferenceRule,
    LiteratureReference,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)
```

## 既存ファイルへ追加・置換する関数（全文）

```python
def _abstract_group_signature(statement: object) -> tuple[tuple[str, int], ...] | None:
    """Read structural cyclic orders only; no generator equality is inferred."""
    components = _group_components(statement)
    if components is None:
        return None
    signature: list[tuple[str, int]] = []
    for component in components:
        if isinstance(component, FreeCyclicGroup):
            signature.append(("free", 0))
        elif (isinstance(component, FiniteCyclicGroup)
              and type(component.order) is int and component.order >= 2):
            signature.append(("finite", component.order))
        else:
            return None
    return tuple(sorted(signature))


def checked_abstract_inputs(goal: object) -> tuple[object, object] | None:
    """Identify general Toda 4.4 prior-group shapes for every registered k.

    This is a necessary abstract compatibility check, NOT a ProofStep,
    not a source citation and not evidence for named generator identities.
    The actual n=4 target and both adopted prior CSV rows must be verified.
    """
    coordinates = group_coordinates(goal)
    if coordinates is None:
        return None
    n, k = coordinates
    if n != 4 or type(k) is not int:
        return None
    dimension = n + k
    if dimension < 7:
        return None
    group = (
        goal.group if hasattr(goal, "group") else
        goal.lhs if isinstance(goal, Relation) and goal.relation_type is RelationType.EQUALITY
        else None
    )
    if group != TodaPrimaryGroup(dimension, 4):
        return None
    registered = exact_prior_database_result(4, k)
    if type(registered) is not type(goal) or registered != goal:
        return None
    first = exact_prior_database_result(3, k)
    second = exact_prior_database_result(7, dimension - 7)
    if first is None or second is None:
        return None
    if (admitted_db_step(first, proof_target=goal) is None
            or admitted_db_step(second, proof_target=goal) is None):
        return None
    target_signature = _abstract_group_signature(goal)
    first_signature = _abstract_group_signature(first)
    second_signature = _abstract_group_signature(second)
    if (target_signature is None or first_signature is None
            or second_signature is None):
        return None
    if tuple(sorted(first_signature + second_signature)) != target_signature:
        return None
    return first, second


def checked_general_inputs(goal: object) -> tuple[object, object] | None:
    """Require both abstract compatibility and certified generator presentation.

    The general structural gate is k-unbounded, but an unverified generator
    mapping never becomes a complete result. Existing public rules stay strict.
    """
    pair = checked_abstract_inputs(goal)
    if pair is None:
        return None
    first, second = pair
    mapped = _map_components(first, second)
    actual = _group_components(goal)
    if mapped is None or actual is None or not components_match_alias(mapped, actual):
        return None
    return first, second
```

## 新規ファイル全文：`phase173_r4_r15r1_unbounded_abstract_frontier/__init__.py`

```python
"""Phase 173 R4-R15R1: unbounded abstract source-prior frontier."""
```

## 新規ファイル全文：`phase173_r4_r15r1_unbounded_abstract_frontier/patch_source.py`

```python
"""One-file, reviewed-source transformation for generic abstract prior frontiers.

The candidate is not a proof and never bypasses named-generator guards.
"""
from __future__ import annotations

import ast
from pathlib import Path

ORIGINAL_BLOB = "cd4b8feb29fbe95a4aedb355514a0267146935ee"
TARGET = "phase173_r4_r10_general_toda56_core/core.py"

UPDATED_IMPORT = "from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup"
ORIGINAL_IMPORT = "from homotopy_groups import TodaPrimaryGroup"

REPLACEMENT = '''def _abstract_group_signature(statement: object) -> tuple[tuple[str, int], ...] | None:
    """Read structural cyclic orders only; no generator equality is inferred."""
    components = _group_components(statement)
    if components is None:
        return None
    signature: list[tuple[str, int]] = []
    for component in components:
        if isinstance(component, FreeCyclicGroup):
            signature.append(("free", 0))
        elif (isinstance(component, FiniteCyclicGroup)
              and type(component.order) is int and component.order >= 2):
            signature.append(("finite", component.order))
        else:
            return None
    return tuple(sorted(signature))


def checked_abstract_inputs(goal: object) -> tuple[object, object] | None:
    """Identify general Toda 4.4 prior-group shapes for every registered k.

    This is a necessary abstract compatibility check, NOT a ProofStep,
    not a source citation and not evidence for named generator identities.
    The actual n=4 target and both adopted prior CSV rows must be verified.
    """
    coordinates = group_coordinates(goal)
    if coordinates is None:
        return None
    n, k = coordinates
    if n != 4 or type(k) is not int:
        return None
    dimension = n + k
    if dimension < 7:
        return None
    group = (
        goal.group if hasattr(goal, "group") else
        goal.lhs if isinstance(goal, Relation) and goal.relation_type is RelationType.EQUALITY
        else None
    )
    if group != TodaPrimaryGroup(dimension, 4):
        return None
    registered = exact_prior_database_result(4, k)
    if type(registered) is not type(goal) or registered != goal:
        return None
    first = exact_prior_database_result(3, k)
    second = exact_prior_database_result(7, dimension - 7)
    if first is None or second is None:
        return None
    if (admitted_db_step(first, proof_target=goal) is None
            or admitted_db_step(second, proof_target=goal) is None):
        return None
    target_signature = _abstract_group_signature(goal)
    first_signature = _abstract_group_signature(first)
    second_signature = _abstract_group_signature(second)
    if (target_signature is None or first_signature is None
            or second_signature is None):
        return None
    if tuple(sorted(first_signature + second_signature)) != target_signature:
        return None
    return first, second


def checked_general_inputs(goal: object) -> tuple[object, object] | None:
    """Require both abstract compatibility and certified generator presentation.

    The general structural gate is k-unbounded, but an unverified generator
    mapping never becomes a complete result. Existing public rules stay strict.
    """
    pair = checked_abstract_inputs(goal)
    if pair is None:
        return None
    first, second = pair
    mapped = _map_components(first, second)
    actual = _group_components(goal)
    if mapped is None or actual is None or not components_match_alias(mapped, actual):
        return None
    return first, second
'''


def transform(source: bytes) -> bytes:
    """Replace complete function and complete import atomically; retain EOL."""
    newline = b"\r\n" if b"\r\n" in source else b"\n"
    if b"\r\n" in source and source.replace(b"\r\n", b"").find(b"\n") != -1:
        raise RuntimeError("Mixed EOL requires separate review")
    decoded = source.decode("utf-8-sig").replace("\r\n", "\n")
    tree = ast.parse(decoded)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    names = {node.name for node in functions}
    if "checked_abstract_inputs" in names:
        raise RuntimeError("Previously generalized core requires separate review")
    target = [node for node in functions if node.name == "checked_general_inputs"]
    subsequent = [node for node in functions if node.name == "general_toda56_rule"]
    if len(target) != 1 or len(subsequent) != 1:
        raise RuntimeError("Reviewed function anchors are missing")
    if subsequent[0].lineno <= target[0].end_lineno:
        raise RuntimeError("Reviewed function ordering changed")
    if decoded.count(ORIGINAL_IMPORT) != 1 or UPDATED_IMPORT in decoded:
        raise RuntimeError("Reviewed import anchor missing or duplicated")
    if decoded.count("def checked_general_inputs(") != 1:
        raise RuntimeError("Reviewed function name is ambiguous")
    source_lines = decoded.splitlines(keepends=True)
    before = "".join(source_lines[:target[0].lineno - 1])
    after = "".join(source_lines[subsequent[0].lineno - 1:])
    if any(line.strip() for line in source_lines[target[0].end_lineno:subsequent[0].lineno - 1]):
        raise RuntimeError("Unexpected code between reviewed functions")
    original = "".join(source_lines[target[0].lineno - 1:target[0].end_lineno])
    required = (
        "def checked_general_inputs(goal: object)",
        "exact_prior_database_result(4, k)",
        "admitted_db_step(first, proof_target=goal)",
        "admitted_db_step(second, proof_target=goal)",
        "_map_components(first, second)",
        "components_match_alias(mapped, actual)",
    )
    if not all(value in original for value in required):
        raise RuntimeError("Reviewed generator guard differs")
    updated = (before + REPLACEMENT + "\n" + after).replace(ORIGINAL_IMPORT, UPDATED_IMPORT)
    ast.parse(updated)
    output = updated.encode("utf-8")
    return output.replace(b"\n", newline) if newline == b"\r\n" else output


def find_module(root: Path) -> Path:
    return root / TARGET
```

## 新規ファイル全文：`phase173_r4_r15r1_unbounded_abstract_frontier/install.py`

```python
"""Guarded, reversible one-module change for unbounded abstract prior matching."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

from phase173_r4_r15r1_unbounded_abstract_frontier.patch_source import (
    ORIGINAL_BLOB,
    TARGET,
    transform,
)

REVIEWED_ANCESTOR = "382cef8b866351b14fe1e717a283e50dc6f24555"
DEPENDENCIES = {
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase173_r4_r4_typed_generator_audit/audit.py": "82f9f734104ddb70df42090ee9a6413b06f1e98b",
    "phase173_r4_r6_alias_source_audit/audit.py": "9670dbd8c721e15e0c76b3e043accab6cb01daf3",
}
ALLOWED_TRACKED = {
    ".pytest_cache/v/cache/nodeids",
    "phase165_r52_r3_web_adapter.py",
    "phase173_r4_r13_narrative_audit/audit.py",
    "phase173_r4_r13_narrative_audit/tests/test_audit.py",
    "phase168_r3_5_model_renderer.py",
    TARGET,
}


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if completed.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + completed.stderr[:600])
    return completed.stdout.strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def package_path(root: Path) -> Path:
    return root / "phase173_r4_r15r1_unbounded_abstract_frontier"


def preflight(root: Path) -> tuple[bytes, bytes, bool]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("Run from the repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Only develop is supported")
    local = git(root, "rev-parse", "HEAD")
    remote = git(root, "rev-parse", "origin/develop")
    if local != remote:
        raise RuntimeError(f"GitHub/local HEAD mismatch: local={local} remote={remote}")
    git(root, "merge-base", "--is-ancestor", REVIEWED_ANCESTOR, local)
    if git(root, "rev-parse", "HEAD:" + TARGET) != ORIGINAL_BLOB:
        raise RuntimeError("Production base core differs from the reviewed Git blob")
    for path, expected in DEPENDENCIES.items():
        if git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("Committed dependency changed: " + path)
        committed = subprocess.run(
            ("git", "show", "HEAD:" + path), cwd=root,
            capture_output=True, check=True,
        ).stdout
        working = (root / path).read_bytes()
        if working.replace(b"\r\n", b"\n") != committed.replace(b"\r\n", b"\n"):
            raise RuntimeError("Local dependency changed: " + path)
    changed = set(filter(None, git(root, "diff", "--name-only").splitlines()))
    staged = git(root, "diff", "--cached", "--name-only")
    if staged:
        raise RuntimeError("Review staged changes before running")
    unexpected = changed - ALLOWED_TRACKED
    if unexpected:
        raise RuntimeError("Unexpected tracked changes: " + ", ".join(sorted(unexpected)))
    actual = (root / TARGET).read_bytes()
    baseline = subprocess.run(
        ("git", "show", "HEAD:" + TARGET), cwd=root, check=True,
        capture_output=True,
    ).stdout
    expected = transform(baseline)
    normalized = lambda value: value.replace(b"\r\n", b"\n")
    if normalized(actual) == normalized(baseline):
        candidate = transform(actual)
        installed = False
    elif normalized(actual) == normalized(expected):
        candidate = actual
        installed = True
    else:
        raise RuntimeError("Target has unexpected local edits")
    print("PHASE173_R4_R15R1_LOCAL_HEAD=" + local, flush=True)
    print("PHASE173_R4_R15R1_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R1_PREFLIGHT=PASS", flush=True)
    print("PHASE173_R4_R15R1_PREVIOUS_WORKTREE_PRESERVED=True", flush=True)
    return baseline, candidate, installed


def write_preview(root: Path, candidate: bytes) -> None:
    folder = package_path(root) / "reviewed_full_source"
    folder.mkdir(exist_ok=True)
    (folder / "phase173_r4_r10_core_FULL.py.txt").write_bytes(candidate)
    print("PHASE173_R4_R15R1_FULL_SOURCE=" + str(folder / "phase173_r4_r10_core_FULL.py.txt"), flush=True)


def apply(root: Path, *, dry_run: bool) -> None:
    baseline, candidate, installed = preflight(root)
    write_preview(root, candidate)
    if dry_run:
        print("PHASE173_R4_R15R1_DRY_RUN=PASS", flush=True)
        print("PHASE173_R4_R15R1_PRODUCTION_EDIT=NONE", flush=True)
        return
    if installed:
        print("PHASE173_R4_R15R1_ALREADY_INSTALLED=True", flush=True)
        return
    package = package_path(root)
    backup = package / "reviewed_full_source" / "original_core.py.bak"
    state = package / "reviewed_full_source" / "installed_state.json"
    if backup.exists() or state.exists():
        raise RuntimeError("Unreviewed existing backup/state requires inspection")
    backup.write_bytes(baseline)
    state.write_text(json.dumps({
        "original_sha256": sha256(baseline),
        "candidate_sha256": sha256(candidate),
        "target": TARGET,
    }, indent=2) + "\n", encoding="utf-8")
    temp = (root / TARGET).with_suffix(".phase173.tmp")
    try:
        temp.write_bytes(candidate)
        os.replace(temp, root / TARGET)
    finally:
        if temp.exists():
            temp.unlink()
    print("PHASE173_R4_R15R1_PATCHED=" + TARGET, flush=True)


def rollback(root: Path) -> None:
    package = package_path(root)
    state_path = package / "reviewed_full_source" / "installed_state.json"
    backup_path = package / "reviewed_full_source" / "original_core.py.bak"
    if not state_path.is_file() or not backup_path.is_file():
        raise RuntimeError("No reviewed backup available for rollback")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    target_path = root / TARGET
    actual = target_path.read_bytes()
    baseline = backup_path.read_bytes()
    if (sha256(baseline) != state["original_sha256"]
            or sha256(actual) != state["candidate_sha256"]):
        raise RuntimeError("Refusing rollback: source changed after installation")
    temp = target_path.with_suffix(".phase173.tmp")
    try:
        temp.write_bytes(baseline)
        os.replace(temp, target_path)
    finally:
        if temp.exists():
            temp.unlink()
    state_path.unlink()
    backup_path.unlink()
    print("PHASE173_R4_R15R1_ROLLBACK=PASS", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.rollback:
        rollback(root)
    else:
        apply(root, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規ファイル全文：`phase173_r4_r15r1_unbounded_abstract_frontier/frontier.py`

```python
"""Read-only comparison of k-unbounded abstract and named-generator gates."""
from __future__ import annotations

import json
from pathlib import Path

from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r10_general_toda56_core.core import (
    _abstract_group_signature,
    checked_abstract_inputs,
    checked_general_inputs,
)
from phase173_r4_r4_typed_generator_audit.audit import (
    _group_components,
    _map_components,
    _nu4_composed_image,
    _suspend_verified_shape,
)


def inspect_k(k: int) -> dict[str, object]:
    """Describe actual DB and typed frontier, without creating a proof leaf."""
    if type(k) is not int or k < 3:
        raise ValueError("This n=4 split requires integer k>=3")
    dimension = k + 4
    goal = exact_prior_database_result(4, k)
    first = exact_prior_database_result(3, k)
    second = exact_prior_database_result(7, dimension - 7)
    abstract = checked_abstract_inputs(goal) if goal is not None else None
    named = checked_general_inputs(goal) if goal is not None else None
    images = _map_components(*abstract) if abstract is not None else None
    target_components = _group_components(goal) if goal is not None else None
    left_components = _group_components(first) if first is not None else None
    right_components = _group_components(second) if second is not None else None
    left_pending = tuple(
        index for index, component in enumerate(left_components)
        if _suspend_verified_shape(component.generator) is None
    ) if left_components is not None else ()
    right_pending = tuple(
        index for index, component in enumerate(right_components)
        if _nu4_composed_image(component.generator) is None
    ) if right_components is not None else ()
    row = {
        "k": k,
        "group": f"pi_{dimension}^4",
        "registered": goal is not None,
        "first_prior": first is not None,
        "second_prior": second is not None,
        "target_signature": _abstract_group_signature(goal) if goal is not None else None,
        "first_signature": _abstract_group_signature(first) if first is not None else None,
        "second_signature": _abstract_group_signature(second) if second is not None else None,
        "abstract_inputs_eligible": abstract is not None,
        "named_generator_inputs_eligible": named is not None,
        "mapped_generator_components": len(images) if images is not None else None,
        "left_component_count": len(left_components) if left_components is not None else None,
        "right_component_count": len(right_components) if right_components is not None else None,
        "left_suspension_shape_pending_indices": left_pending,
        "right_nu4_composition_shape_pending_indices": right_pending,
        "target_generator_components": len(target_components) if target_components is not None else None,
        "public_proof_complete_by_this_change": False,
    }
    row["frontier"] = (
        "MISSING_REGISTERED_SOURCE" if (goal is None or first is None or second is None)
        else "ABSTRACT_PRIOR_MISMATCH" if abstract is None
        else "NAMED_IMAGE_MATCH" if named is not None
        else "GENERATOR_IMAGE_PROOF_PENDING"
    )
    return row


def write_report(root: Path, output: Path) -> tuple[dict[str, object], ...]:
    rows = tuple(inspect_k(k) for k in (3, 4, 5, 6, 7, 8, 31))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({
        "phase": "173-R4-R15R1",
        "mode": "ABSTRACT_STRUCTURE_ONLY",
        "rows": rows,
        "all_named_generator_claims_require_separate_proof": True,
        "no_proof_steps_created": True,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print("PHASE173_R4_R15R1_K=" + str(row["k"])
              + " ABSTRACT=" + str(row["abstract_inputs_eligible"])
              + " GENERATORS=" + str(row["named_generator_inputs_eligible"])
              + " FRONTIER=" + str(row["frontier"]), flush=True)
    print("PHASE173_R4_R15R1_REPORT=" + str(output), flush=True)
    return rows


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    report = Path(__file__).with_name("frontier_result.json")
    rows = write_report(root, report)
    selected = next(row for row in rows if row["k"] == 31)
    if not selected["registered"]:
        print("PHASE173_R4_R15R1_K31_REGISTERED=False", flush=True)
        return 2
    print("PHASE173_R4_R15R1_K31_ABSTRACT="
          + str(selected["abstract_inputs_eligible"]), flush=True)
    print("PHASE173_R4_R15R1_PUBLIC_COMPLETION=False", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規ファイル全文：`phase173_r4_r15r1_unbounded_abstract_frontier/tests/test_patch_source.py`

```python
"""Standalone tests of the one-function patch boundary."""
from __future__ import annotations

import ast

import pytest

from phase173_r4_r15r1_unbounded_abstract_frontier.patch_source import (
    ORIGINAL_IMPORT,
    UPDATED_IMPORT,
    transform,
)


def fixture_source(eol: str = "\n") -> bytes:
    text = (
        "from __future__ import annotations\n"
        + ORIGINAL_IMPORT + "\n"
        + "from phase173_r4_r4_typed_generator_audit.audit import _group_components, _map_components\n"
        + "def checked_general_inputs(goal: object):\n"
        + "    registered = exact_prior_database_result(4, k)\n"
        + "    first = admitted_db_step(first, proof_target=goal)\n"
        + "    second = admitted_db_step(second, proof_target=goal)\n"
        + "    mapped = _map_components(first, second)\n"
        + "    actual = _group_components(goal)\n"
        + "    if not components_match_alias(mapped, actual):\n"
        + "        return None\n"
        + "    return first, second\n\n\n"
        + "def general_toda56_rule(goal: object):\n"
        + "    return goal\n"
    )
    return text.replace("\n", eol).encode("utf-8")


@pytest.mark.parametrize("eol", ("\n", "\r\n"))
def test_transform_preserves_end_of_lines_and_unrelated_function(eol: str) -> None:
    source = fixture_source(eol)
    result = transform(source)
    assert UPDATED_IMPORT.encode() in result
    assert ORIGINAL_IMPORT.encode() not in result
    assert result.count(b"def checked_abstract_inputs(") == 1
    assert result.count(b"def checked_general_inputs(") == 1
    assert result.endswith(f"def general_toda56_rule(goal: object):{eol}    return goal{eol}".encode())
    assert (b"\r\n" in result) == (eol == "\r\n")
    ast.parse(result.decode())


def test_transform_refuses_missing_guard() -> None:
    source = fixture_source().replace(b"components_match_alias(mapped, actual)", b"True")
    with pytest.raises(RuntimeError, match="Reviewed generator guard"):
        transform(source)


def test_transform_refuses_duplicate_general_implementation() -> None:
    source = fixture_source().replace(b"def general_toda56_rule", b"def checked_abstract_inputs(x):\n    pass\n\ndef general_toda56_rule")
    with pytest.raises(RuntimeError, match="Previously generalized"):
        transform(source)


def test_transform_refuses_mixed_endings() -> None:
    source = fixture_source("\r\n") + b"# stray\n"
    with pytest.raises(RuntimeError, match="Mixed EOL"):
        transform(source)
```

## 新規ファイル全文：`phase173_r4_r15r1_unbounded_abstract_frontier/tests/test_frontier.py`

```python
"""Focused repository-backed, mathematical-structure-only tests."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r10_general_toda56_core.core import (
    checked_abstract_inputs,
    checked_general_inputs,
)
from phase173_r4_r15r1_unbounded_abstract_frontier.frontier import inspect_k


@pytest.mark.parametrize("k", (3, 4, 5, 6, 7))
def test_prior_signature_previously_proven_dimensions(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    assert goal is not None
    assert checked_abstract_inputs(goal) is not None


def test_k31_abstract_prior_gate_is_generic_but_named_generator_is_not_certified() -> None:
    goal = exact_prior_database_result(4, 31)
    assert goal is not None
    prior = checked_abstract_inputs(goal)
    assert prior is not None
    assert prior[0] == exact_prior_database_result(3, 31)
    assert prior[1] == exact_prior_database_result(7, 28)
    assert checked_general_inputs(goal) is None
    row = inspect_k(31)
    assert row["target_signature"] == (("finite", 2),) * 8
    assert row["first_signature"] == (("finite", 2),) * 4
    assert row["second_signature"] == (("finite", 2),) * 4
    assert row["frontier"] == "GENERATOR_IMAGE_PROOF_PENDING"
    assert row["public_proof_complete_by_this_change"] is False


def test_existing_strict_generator_guards_retained() -> None:
    for k in (4, 5, 6, 7):
        goal = exact_prior_database_result(4, k)
        assert checked_general_inputs(goal) is not None
    goal12 = exact_prior_database_result(4, 8)
    assert goal12 is not None
    assert checked_general_inputs(goal12) is None
    legacy = exact_prior_database_result(4, 3)
    assert checked_general_inputs(legacy) is None


def test_forged_registered_group_is_not_admitted() -> None:
    goal = exact_prior_database_result(4, 31)
    assert goal is not None
    altered = replace(goal, rhs=exact_prior_database_result(4, 4).rhs)
    assert checked_abstract_inputs(altered) is None


def test_invalid_k_rejected_before_reading_database() -> None:
    with pytest.raises(ValueError):
        inspect_k(2)
    with pytest.raises(ValueError):
        inspect_k(True)
```

## 新規ファイル全文：`phase173_r4_r15r1_unbounded_abstract_frontier/run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'GitHub fetch failed' }

    $Options = @('--root', $Root)
    if ($DryRun) { $Options += '--dry-run' }
    python -m phase173_r4_r15r1_unbounded_abstract_frontier.install @Options
    if ($LASTEXITCODE -ne 0) { throw 'R4-R15R1 preflight/apply failed' }

    python -m pytest -q -p no:cacheprovider `
      phase173_r4_r15r1_unbounded_abstract_frontier/tests/test_patch_source.py
    if ($LASTEXITCODE -ne 0) { throw 'R4-R15R1 patch safety tests failed' }
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R1_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R1_PRODUCTION_EDIT=NONE'
        exit 0
    }

    python -m pytest -q -p no:cacheprovider `
      phase173_r4_r15r1_unbounded_abstract_frontier/tests/test_frontier.py `
      phase173_r4_r10_general_toda56_core/tests/test_core.py
    if ($LASTEXITCODE -ne 0) {
        python -m phase173_r4_r15r1_unbounded_abstract_frontier.install --root $Root --rollback
        throw 'R4-R15R1 focused mathematical tests failed; rollback requested'
    }

    python -m phase173_r4_r15r1_unbounded_abstract_frontier.frontier
    if ($LASTEXITCODE -ne 0) {
        python -m phase173_r4_r15r1_unbounded_abstract_frontier.install --root $Root --rollback
        throw 'R4-R15R1 frontier audit failed; rollback requested'
    }
    Write-Output 'PHASE173_R4_R15R1_FOCUSED_PYTEST=PASS'
    Write-Output 'PHASE173_R4_R15R1_PRODUCTION_CORE=ABSTRACT_PRIORS_K_UNBOUNDED'
    Write-Output 'PHASE173_R4_R15R1_NAMED_GENERATOR_CERTIFICATION=PENDING'
    Write-Output 'PHASE173_R4_R15R1_PHASE_COMPLETED=False'
}
finally {
    Pop-Location
}
```


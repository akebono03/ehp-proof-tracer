# Phase 171 R2J-R4-R9-R9 — 完全実装コード

## 変更対象・配置

- 既存: `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` 内部 `expand()` の R8 hook 直後に4行追加。既存トップレベル import は無変更。
- 新規: `phase171_r2j_r4_r9_r9_public_cyclic_structure/source.py`, `install.py`, `audit.py`, `tests/test_audit.py`, `run.ps1`。それぞれ既存同名ファイルを置換しない。
- インストール後の **置換可能な既存関数全文** と既存ファイル全文は `output/shared_expansion_provider_FULL.py` および `output/phase165_r52_r9_shared_math.FULL.py` に自動保存する。

## 既存関数内で挿入する4行（R8 呼出しの直後）

```python
        from phase171_r2j_r4_r9_r9_public_cyclic_structure.source import (
            expand_cited_full_order_cyclic_structure,
        )
        options.extend(expand_cited_full_order_cyclic_structure(goal, tuple(available)))
```

## source.py

```python
"""Source-screened finite cyclic structure from independently proved orders.

Only proof obligations are proposed. The named element is identified through
an earlier screened typed double relation, not through a database group answer.
The existing order-four root proposer supplies the identical, checked pair of
subgoals; this stage does not attempt to prove either premise.
"""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase171_r2j_r4_r7_nonzero_nu_order.source import FiniteElementOrder
from phase171_r2j_r4_r8_cyclic_structure.source import cyclic_group_from_generator_order
from phase171_r2j_r4_r9_r7_public_cyclic_root.source import expand_cited_double_cyclic_root
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


def finite_cyclic_structure_from_full_order_rule(
    goal: CyclicStructureStatement,
) -> InferenceRule:
    """Infer the cyclic structure if an element has the full group order.

    ProofStep premises must both be INFERENCE; a database row, a nominal
    source relation, or an unproved requested group cannot discharge either.
    """
    if (
        not isinstance(goal, CyclicStructureStatement)
        or not isinstance(goal.group, TodaPrimaryGroup)
        or type(goal.order) is not int
        or goal.order < 2
    ):
        raise ValueError("a positive finite cyclic-structure goal is required")
    requested = Relation(
        goal.group,
        FiniteCyclicGroup(goal.order, goal.generator),
        RelationType.EQUALITY,
    )

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and cyclic_group_from_generator_order(
                premises[0].conclusion,
                premises[1].conclusion,
                requested=requested,
            ) == requested
        )

    return InferenceRule(
        name="proved finite cardinality and full element order imply cyclic structure",
        description=(
            "A finite group of order m with an element of order m is cyclic; "
            "the generator is checked against the typed registered identity."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=FiniteGroupCardinality,
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=FiniteElementOrder,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_full_order_cyclic_structure(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Reuse R7's checked source-witness candidate, without importing proof.

    This phase supports only the order-four source shape that R7 already
    exposes, while the mathematical InferenceRule works for any order >= 2.
    Future generic order inference must be independently established.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be screened fixed statements in a tuple")
    if (
        not isinstance(goal, CyclicStructureStatement)
        or not isinstance(goal.group, TodaPrimaryGroup)
        or type(goal.order) is not int
        or goal.order < 2
    ):
        return ()
    requested = Relation(
        goal.group,
        FiniteCyclicGroup(goal.order, goal.generator),
        RelationType.EQUALITY,
    )
    routes = expand_cited_double_cyclic_root(requested, available)
    if len(routes) != 1 or len(routes[0].subgoals) != 2:
        return ()
    cardinality, element_order = routes[0].subgoals
    if cyclic_group_from_generator_order(
        cardinality, element_order, requested=requested,
    ) != requested:
        return ()
    return (GoalExpansion(
        finite_cyclic_structure_from_full_order_rule(goal),
        (cardinality, element_order),
    ),)
```

## install.py

```python
"""Guarded single-function patch; preserve reviewed R7 and R8 hooks."""
from __future__ import annotations

import argparse
import ast
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
PATH_IN_GIT = "phase165_r52_r9_shared_math.py"
REVIEWED_ORIGINAL_BLOB_SHA = "68846671215c38e3e0a572932b8ed955a7880edc"
R7_HOOK = (
    "        from phase171_r2j_r4_r9_r7_public_cyclic_root.source import (\n"
    "            expand_cited_double_cyclic_root,\n"
    "        )\n"
    "        options.extend(expand_cited_double_cyclic_root(goal, tuple(available)))\n"
)
R8_HOOK = (
    "        from phase171_r2j_r4_r9_r8_public_cardinality.source import (\n"
    "            expand_cited_ehp_middle_cardinality,\n"
    "        )\n"
    "        options.extend(expand_cited_ehp_middle_cardinality(goal, tuple(available)))\n"
)
R9_HOOK = (
    "        from phase171_r2j_r4_r9_r9_public_cyclic_structure.source import (\n"
    "            expand_cited_full_order_cyclic_structure,\n"
    "        )\n"
    "        options.extend(expand_cited_full_order_cyclic_structure(goal, tuple(available)))\n"
)


def _git(*args: str) -> bytes:
    permitted = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("show", f"HEAD:{PATH_IN_GIT}"),
    }
    if args not in permitted:
        raise ValueError("read-only reviewed Git operations only")
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=True,
    ).stdout


def _clean_text(blob: bytes) -> str:
    return blob.decode("utf-8-sig").replace("\r\n", "\n")


def _git_blob_sha(blob: bytes) -> str:
    return hashlib.sha1(f"blob {len(blob)}\0".encode() + blob).hexdigest()


def _function_text(source: str) -> str:
    tree = ast.parse(source)
    selected = [
        item for item in tree.body
        if isinstance(item, ast.FunctionDef)
        and item.name == "shared_expansion_provider"
    ]
    if len(selected) != 1:
        raise RuntimeError("expected exactly one existing shared provider function")
    node = selected[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def install(*, dry_run: bool) -> bool:
    """Check exact reviewed baseline and in-worktree R7/R8 before insertion."""
    if _git("branch", "--show-current").decode().strip() != "develop":
        raise RuntimeError("develop branch required")
    if not TARGET.is_file():
        raise RuntimeError("shared provider is missing")
    head_bytes = _git("show", f"HEAD:{PATH_IN_GIT}")
    head_text = _clean_text(head_bytes)
    # HEAD may contain R7 and R8 if committed; do not accept unrelated edits.
    if any(head_text.count(hook) > 1 for hook in (R7_HOOK, R8_HOOK, R9_HOOK)):
        raise RuntimeError("duplicate previously committed provider hook")
    head_newline = "\r\n" if b"\r\n" in head_bytes else "\n"
    baseline_bytes = head_bytes
    for hook in (R7_HOOK, R8_HOOK, R9_HOOK):
        baseline_bytes = baseline_bytes.replace(
            hook.replace("\n", head_newline).encode("utf-8"), b"",
        )
    if _git_blob_sha(baseline_bytes) != REVIEWED_ORIGINAL_BLOB_SHA:
        raise RuntimeError("HEAD provider differs from reviewed GitHub source")
    original_bytes = TARGET.read_bytes()
    current = _clean_text(original_bytes)
    expected = head_text
    anchor = "        options.extend(expand_finite_cyclic_relation(goal))\n"
    if R7_HOOK not in expected:
        if expected.count(anchor) != 1:
            raise RuntimeError("R7 insertion anchor is not unique")
        expected = expected.replace(anchor, anchor + R7_HOOK, 1)
    if R8_HOOK not in expected:
        if expected.count(R7_HOOK) != 1:
            raise RuntimeError("R7 prerequisite is ambiguous")
        expected = expected.replace(R7_HOOK, R7_HOOK + R8_HOOK, 1)
    if any(expected.count(hook) != 1 for hook in (R7_HOOK, R8_HOOK)):
        raise RuntimeError("R7/R8 prerequisite is absent")
    if R9_HOOK not in expected:
        expected_with_r9 = expected.replace(R8_HOOK, R8_HOOK + R9_HOOK, 1)
    else:
        expected_with_r9 = expected
    if current == expected and R9_HOOK not in expected:
        state = "READY_TO_PATCH"
    elif current == expected_with_r9:
        state = "ALREADY_INSTALLED"
    else:
        raise RuntimeError("unknown tracked provider changes; refusing overwrite")
    next_text = expected_with_r9
    if any(next_text.count(hook) != 1 for hook in (R7_HOOK, R8_HOOK, R9_HOOK)):
        raise RuntimeError("required hook is missing or duplicated")
    function = _function_text(next_text)
    if any(hook not in function for hook in (R7_HOOK, R8_HOOK, R9_HOOK)):
        raise RuntimeError("patch escaped the shared provider function")
    ast.parse(next_text)
    print("PHASE171_R2J_R4_R9_R9_HEAD=" + _git("rev-parse", "HEAD").decode().strip(), flush=True)
    print("PHASE171_R2J_R4_R9_R9_PATCH_STATE=" + state, flush=True)
    if dry_run:
        print("PHASE171_R2J_R4_R9_R9_RESULT=PASS_DRY_RUN", flush=True)
        return False
    OUTPUT.mkdir(exist_ok=True)
    if state == "READY_TO_PATCH":
        (OUTPUT / "phase165_r52_r9_shared_math.BEFORE.py").write_bytes(original_bytes)
        newline = "\r\n" if b"\r\n" in original_bytes else "\n"
        bom = b"\xef\xbb\xbf" if original_bytes.startswith(b"\xef\xbb\xbf") else b""
        TARGET.write_bytes(bom + next_text.replace("\n", newline).encode("utf-8"))
        print("PHASE171_R2J_R4_R9_R9_PATCHED=phase165_r52_r9_shared_math.py", flush=True)
    (OUTPUT / "shared_expansion_provider_FULL.py").write_text(function + "\n", encoding="utf-8")
    (OUTPUT / "phase165_r52_r9_shared_math.FULL.py").write_bytes(TARGET.read_bytes())
    print("PHASE171_R2J_R4_R9_R9_FULL_FUNCTION=" + str(OUTPUT / "shared_expansion_provider_FULL.py"), flush=True)
    print("PHASE171_R2J_R4_R9_R9_FULL_FILE=" + str(OUTPUT / "phase165_r52_r9_shared_math.FULL.py"), flush=True)
    return state == "READY_TO_PATCH"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    install(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
```

## audit.py

```python
"""Audit public finite-cyclic-structure expansion using genuine R4-R8 sources."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r9_public_cyclic_structure.source import (
    expand_cited_full_order_cyclic_structure,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*args: str) -> str:
    if args not in {("branch", "--show-current"), ("rev-parse", "HEAD")}:
        raise ValueError("only read-only Git commands permitted")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True,
    ).stdout.strip()


def matching_cyclic_route(options: tuple, parents: tuple[ProofStep, ...]) -> bool:
    """Require exactly one reconstructed route for the original two hypotheses."""
    return sum(
        proposal.rule.name
        == "proved finite cardinality and full element order imply cyclic structure"
        and proposal.subgoals == tuple(parent.conclusion for parent in parents)
        for proposal in options
    ) == 1


def inspect_public_cyclic_structure() -> dict:
    screened, target, _ = _screened_context()
    original, _, original_report = build_cyclic_pi63_proof()
    if (
        original.rule is not ProofRule.INFERENCE
        or original.conclusion != target
        or len(original.premises) != 2
        or original_report["new_given_added"] != 0
    ):
        raise RuntimeError("source R4-R8 proof must be genuine inference")
    goal = CyclicStructureStatement(
        target.lhs, target.rhs.generator, target.rhs.order,
    )
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    proposed = expand_cited_full_order_cyclic_structure(goal, available)
    if not matching_cyclic_route(proposed, original.premises):
        raise RuntimeError("screened source lacks exact cyclic structure route")
    shared = shared_expansion_provider(screened, proof_target=target)(goal)
    if not matching_cyclic_route(shared, original.premises):
        raise RuntimeError("public provider lacks cyclic structure obligation")
    matches = tuple(
        item for item in find_inference_matches_for_rule(
            proposed[0].rule, original.premises,
        )
        if item.premises == original.premises
    )
    if len(matches) != 1:
        raise RuntimeError("full-order structure does not match genuine premises")
    structure_step = derive_inference_proof_step(matches[0])
    if (
        structure_step.conclusion != goal
        or structure_step.rule is not ProofRule.INFERENCE
        or structure_step.premises != original.premises
    ):
        raise RuntimeError("cyclic structure was not a real typed inference")
    public = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(), goal=target,
    )
    return {
        "phase": "171-R2J-R4-R9-R9",
        "mode": "PUBLIC_CYCLIC_STRUCTURE_PROPOSAL_ONLY",
        "registered_target": repr(target),
        "cyclic_structure_goal": repr(goal),
        "structure_inference_matched": True,
        "screened_structure_routes": len(proposed),
        "shared_structure_connected": True,
        "shared_structure_routes": len(shared),
        "structure_subgoals": [repr(item) for item in proposed[0].subgoals],
        "public_search_status": public.status.value,
        "public_complete": public.status.value == "complete" and public.conclusion == target,
        "public_open_goals": [repr(item)[:1200] for item in public.open_goals[:15]],
        "public_diagnostics": list(public.diagnostics[:15]),
        "new_given_added": 0,
        "completed_proof_imported": False,
        "web_modified": False,
        "trust_boundary_modified": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch, head = _git("branch", "--show-current"), _git("rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError("develop branch required")
    print("PHASE171_R2J_R4_R9_R9_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R9_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R9_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = inspect_public_cyclic_structure()
    report["git_head"] = head
    OUTPUT.mkdir(exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R9_R9_STRUCTURE_INFERENCE=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R9_R9_SHARED_STRUCTURE_CONNECTED=True", flush=True)
    print("PHASE171_R2J_R4_R9_R9_PUBLIC_SEARCH=" + report["public_search_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R9_PUBLIC_COMPLETE=" + str(report["public_complete"]), flush=True)
    if report["public_open_goals"]:
        print("PHASE171_R2J_R4_R9_R9_FIRST_OPEN_GOAL=" + report["public_open_goals"][0], flush=True)
    print("PHASE171_R2J_R4_R9_R9_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R9_REPORT=" + str(destination), flush=True)
    print("PHASE171_R2J_R4_R9_R9_RESULT=PASS_STRUCTURE_INTEGRATION", flush=True)


if __name__ == "__main__":
    main()
```

## tests/test_audit.py

```python
"""Focused cyclic-structure source, type, rule and public-path regressions."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement, Multiple
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase171_r2j_r4_r7_nonzero_nu_order.source import FiniteElementOrder
from phase171_r2j_r4_r9_r9_public_cyclic_structure.source import (
    expand_cited_full_order_cyclic_structure,
    finite_cyclic_structure_from_full_order_rule,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def _case():
    nu = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    db_nu = HomotopyElement(
        name="ν'", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family=r"\nu'"),
    )
    group = TodaPrimaryGroup(6, 3)
    source = Relation(Multiple(2, nu), "typed cited RHS", RelationType.EQUALITY)
    goal = CyclicStructureStatement(group, db_nu, 4)
    return source, goal, nu


def test_source_anchored_structure_is_only_two_unproved_subgoals():
    source, goal, nu = _case()
    routes = expand_cited_full_order_cyclic_structure(goal, (source,))
    assert len(routes) == 1
    assert routes[0].subgoals == (
        FiniteGroupCardinality(goal.group, 4),
        FiniteElementOrder(goal.group, nu, 4),
    )
    assert not any(isinstance(item, ProofStep) for item in routes[0].subgoals)


def test_matched_order_and_group_derive_one_real_cyclic_structure():
    source, goal, _ = _case()
    route, = expand_cited_full_order_cyclic_structure(goal, (source,))
    parents = tuple(ProofStep(value, (), ProofRule.INFERENCE) for value in route.subgoals)
    matches = find_inference_matches_for_rule(route.rule, parents)
    assert len(matches) == 1
    result = derive_inference_proof_step(matches[0])
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == goal
    assert result.premises == parents


def test_givens_cannot_replace_proved_orders():
    source, goal, _ = _case()
    route, = expand_cited_full_order_cyclic_structure(goal, (source,))
    left, right = route.subgoals
    rule = finite_cyclic_structure_from_full_order_rule(goal)
    for parents in (
        (ProofStep(left, (), ProofRule.GIVEN), ProofStep(right, (), ProofRule.INFERENCE)),
        (ProofStep(left, (), ProofRule.INFERENCE), ProofStep(right, (), ProofRule.GIVEN)),
    ):
        assert find_inference_matches_for_rule(rule, parents) == ()


def test_missing_screened_source_or_bad_generator_fails_closed():
    source, goal, nu = _case()
    assert expand_cited_full_order_cyclic_structure(goal, ()) == ()
    bad = replace(nu, generator=GeneratorSymbol(family="σ", index=3))
    assert expand_cited_full_order_cyclic_structure(
        goal, (replace(source, lhs=Multiple(2, bad)),),
    ) == ()


def test_cited_relation_must_be_typed_and_double():
    source, goal, nu = _case()
    assert expand_cited_full_order_cyclic_structure(
        goal, (replace(source, relation_type=RelationType.INEQUALITY),),
    ) == ()
    assert expand_cited_full_order_cyclic_structure(
        goal, (replace(source, lhs=Multiple(3, nu)),),
    ) == ()
    assert expand_cited_full_order_cyclic_structure(
        goal, (replace(source, lhs=Multiple(2, replace(nu, source=7))),),
    ) == ()


def test_invalid_goal_and_bad_container_are_rejected():
    source, goal, _ = _case()
    with pytest.raises(TypeError):
        expand_cited_full_order_cyclic_structure(goal, [source])
    assert expand_cited_full_order_cyclic_structure("invalid", (source,)) == ()
    with pytest.raises(ValueError):
        finite_cyclic_structure_from_full_order_rule(
            replace(goal, order=0),
        )


def test_other_cardinality_does_not_become_asserted_order():
    source, goal, _ = _case()
    # R7 currently provides only source-anchored order-four proposals.
    assert expand_cited_full_order_cyclic_structure(
        replace(goal, order=8), (source,),
    ) == ()
    assert expand_cited_full_order_cyclic_structure(
        replace(goal, order=2), (source,),
    ) == ()


def test_duplicate_source_does_not_duplicate_proposals():
    source, goal, _ = _case()
    assert len(expand_cited_full_order_cyclic_structure(goal, (source, source))) == 1


def test_public_provider_matches_existing_r4_r8_verified_parents():
    from phase171_r2j_r4_r9_r9_public_cyclic_structure.audit import (
        inspect_public_cyclic_structure,
    )
    report = inspect_public_cyclic_structure()
    assert report["shared_structure_connected"] is True
    assert report["structure_inference_matched"] is True
    assert report["new_given_added"] == 0
    assert report["completed_proof_imported"] is False


def test_prior_scoped_search_and_trust_boundary_remain_complete():
    from phase171_r2j_r4_r9_r6_source_bound_cited_hopf.audit import (
        audit_second_source_bound_hopf,
    )
    report = audit_second_source_bound_hopf()
    assert report["scoped_search_complete"] is True
    assert report["trust_boundary_accepted"] is True
    assert report["new_given_added"] == 0
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'EHP Git repository root required' }
    python -B -m phase171_r2j_r4_r9_r9_public_cyclic_structure.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R9 guarded preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R9_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m phase171_r2j_r4_r9_r9_public_cyclic_structure.install
    if ($LASTEXITCODE -ne 0) { throw 'R9-R9 guarded patch failed' }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r9_public_cyclic_structure\tests\test_audit.py' `
        '.\phase171_r2j_r4_r9_r8_public_cardinality\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R9 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R9_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r9_public_cyclic_structure.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R9 cyclic-structure audit failed' }
} finally {
    Pop-Location
}
```

## README.md

```markdown
# EHP Proof Tracer — Phase 171 R2J-R4-R9-R9

This package connects a source-screened finite cyclic-structure backward obligation to the ordinary shared Proof Search provider. The rule says a finite group of order `m` with a proved element of order `m` is cyclic, and a registered generator identity must agree with the requested presentation.

## Changes

The installer modifies only the existing `shared_expansion_provider()` function in `phase165_r52_r9_shared_math.py`, inserting four statements immediately after the reviewed R9-R8 provider hook. Top-level imports are unchanged. The package adds `source.py` with the full typed inference rule and backward provider, `install.py`, `audit.py`, focused tests, and this documentation.

The backward provider reuses the reviewed R9-R7 typed source-witness proposer, which currently supports order four. It never uses that source as proof of nonzeroness, cardinality, or element order. All new cyclic-structure premises must be independently reconstructed by the existing recursive proof search. No prior complete `ProofStep` is injected.

## Preconditions and protected patch

Use branch `develop`, with R9-R7 and R9-R8 already installed. The installer accepts only GitHub-reviewed baseline `phase165_r52_r9_shared_math.py` with the exact three reviewed hooks (R7, R8, and optional already-installed R9). It refuses unknown local edits, does not reset or pull, and is idempotent. The reviewed original Git blob is `68846671215c38e3e0a572932b8ed955a7880edc`.

## Windows PowerShell

Extract the ZIP in the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r9_public_cyclic_structure\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r9_public_cyclic_structure\run.ps1"
git status -sb
git diff --stat
```

The run executes 10 new tests and 8 focused R9-R8 tests, not the full suite. It then writes `output/audit.json`. The installer also writes the **entire final** `shared_expansion_provider()` and `phase165_r52_r9_shared_math.py` into its output folder, along with the original file backup if a patch is applied.

## Completion boundary

Success requires exactly one generic cyclic-structure proposal in the public provider, a valid independent inference match, 0 new `GIVEN`, and passing focused tests. Public Proof Search and Web completion are reported as observed; this package does not claim those are complete. Remaining full-order, short-exact or cited-source proof paths belong to later iterations. The public Trust Boundary and Web renderer are not modified.
```

## 監査仕様.md

```markdown
# Phase 171 R2J-R4-R9-R9 監査仕様

## 目的

R9-R8 までに共通 Provider から得られる群の位数に関する目標と、先行 R4-R8 の型付き証明木で実証した生成元の位数を結び付け、`CyclicStructureStatement` の逆方向推論を共通探索で利用できるようにする。

数学的には、有限群 $G$ と $x\in G$ に対して、$|G|=m$ かつ $\operatorname{ord}(x)=m$ から $G=\langle x\rangle$ を導く。今回の接続対象は、R9-R7 が対応済みの位数4の出典付き生成元候補である。

## 変更ファイル・関数

- 既存 `phase165_r52_r9_shared_math.py`：`shared_expansion_provider()` の内部 `expand()` に Provider 呼出し4行のみを追加。トップレベル import と他の関数を変更しない。実行後、関数全文・ファイル全文を `output/` に出力する。
- 新規 `phase171_r2j_r4_r9_r9_public_cyclic_structure/source.py`：`finite_cyclic_structure_from_full_order_rule()`、`expand_cited_full_order_cyclic_structure()` を追加する。ファイルの先頭に追加し、既存コードを置換しない。
- 新規 `install.py`：レビュー済み Git blob と R7/R8 の4行 hook を厳密に検査する。`install()`、`main()` とその補助関数を追加する。
- 新規 `audit.py`：`inspect_public_cyclic_structure()`、`matching_cyclic_route()`、`main()` と補助関数を追加する。
- 新規 `tests/test_audit.py`：10件の限定テストを追加する。
- 新規 `run.ps1`、`README.md`、`CODE_FULL_JA.md`、本ファイル。

## 根拠・信頼境界

R4-R8 の完成済み `ProofStep` は監査中の期待値比較に限って利用する。共通 Provider には `GoalExpansion`（推論規則と前提目標）だけを登録し、証明済みの `ProofStep` を直接挿入しない。

出典選別済みの式 $2\nu'=\cdots$ は生成元の候補を識別する目的だけで使い、$\operatorname{ord}(\nu')=4$ や $|\pi_6^3|=4$ を仮定しない。生成元の型付き同一性は既存 `same_registered_group_presentation()` の判定を再利用する。

照合規則は `FiniteGroupCardinality` と `FiniteElementOrder` がともに `INFERENCE` である場合に限って成立する。DB の `GIVEN` と偽の未証明前提を拒否する。

## 実行・完了条件

先に `-DryRun` を実行し、既存コードの検査結果が `READY_TO_PATCH` または `ALREADY_INSTALLED` であることを確認する。続いて実行用 ZIP に同梱した `run.ps1` で新規10件と R9-R8 の既存8件の限定 pytest、実際の出典を使う公開 Provider の監査を実行する。

- `STRUCTURE_INFERENCE=INFERRED`
- `SHARED_STRUCTURE_CONNECTED=True`
- `NEW_GIVEN=0`
- `RESULT=PASS_STRUCTURE_INTEGRATION`

公開 Proof Search と Web 表示の完成は別の判定とし、`partial` を `complete` とみなさない。

## 次 Phase との境界

R9-R9 では `FiniteElementOrder`、短完全列、Hopf 全射性、非零性の全依存経路を本番 Provider に接続しない。表示文章の修正、公開 Trust Boundary の変更、既存全体 pytest は Phase の後続または終了時のみ行う。
```


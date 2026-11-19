# Phase 175 R4R14R6 — 新規コード全文

## `rule.py`

```python
"""Derive a zero codomain from a proved surjection with zero image.

This mathematical rule is independent of the Toda (5.9) source and of
any particular (n, k). The backward candidate uses the canonical E map
ending in a typed Toda zero-group goal; both premises must be proved.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule

RULE_NAME = "surjective suspension with zero image has zero codomain"


def surjective_zero_codomain_inputs(
    goal: object,
) -> tuple[MapSurjective, ImageZeroStatement] | None:
    """Choose only a well-typed canonical suspension into the target group."""
    if not isinstance(goal, TodaPrimaryGroupZeroStatement):
        return None
    target = goal.group
    if not isinstance(target, TodaPrimaryGroup):
        return None
    q, n = target.group_dimension, target.sphere_dimension
    if (type(q) is not int or type(n) is not int
            or n < 3 or q < n):
        return None
    source = TodaPrimaryGroup(q - 1, n - 1)
    mapping = TodaSuspensionMap(source, target)
    return MapSurjective(mapping), ImageZeroStatement(mapping)


def surjective_zero_codomain_rule(
    goal: TodaPrimaryGroupZeroStatement,
) -> InferenceRule:
    """Require independently inferred surjectivity and zero-image proofs."""
    required = surjective_zero_codomain_inputs(goal)
    if required is None:
        raise ValueError("a typed suspension zero-codomain goal is required")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and surjective_zero_codomain_inputs(goal) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "If a proved surjective homomorphism E:A->B has proved image zero, "
            "then B=im(E)=0. The map properties are separate inferred premises."
        ),
        premise_patterns=(
            PremisePattern(
                statement_type=MapSurjective,
                statement_pattern=required[0],
                proof_rule=ProofRule.INFERENCE,
            ),
            PremisePattern(
                statement_type=ImageZeroStatement,
                statement_pattern=required[1],
                proof_rule=ProofRule.INFERENCE,
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_surjective_zero_codomain(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Supply one unproved root branch, without making any source leaf."""
    required = surjective_zero_codomain_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(surjective_zero_codomain_rule(goal), required),)

```

## `installer.py`

```python
"""Guarded and idempotent addition of one generic root expansion provider."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess
import sys

TARGET = "phase165_r52_r9_shared_math.py"
R5_PIN = "f103bd9ca787542bf41a8b9ab1d1d96668ba63b7"
ANCHOR = "        options.extend(expand_ehp_zero_from_delta_surjectivity(goal))"
INSERT = (
    "        # Phase 175 R4R14R6: generic surjective-zero-image root branch.\n"
    "        # All subgoals remain ordinary source-first proof obligations.\n"
    "        from phase175_r4r14r6_surjective_zero_codomain.rule import (\n"
    "            expand_surjective_zero_codomain,\n"
    "        )\n"
    "        options.extend(expand_surjective_zero_codomain(goal))\n"
)


def git(root: Path, *args: str, data: bytes | None = None) -> str:
    proc = subprocess.run(
        ("git",) + args, cwd=root, input=data, capture_output=True, check=False,
    )
    if proc.returncode:
        raise RuntimeError("GIT_FAILURE: " + " ".join(args) + " " + proc.stderr.decode(errors="replace")[:300])
    return proc.stdout.decode("ascii", errors="replace").strip()


def source_hash(root: Path, contents: str) -> str:
    return git(root, "hash-object", "--stdin", data=contents.encode("utf-8"))


def next_source(source: str) -> str:
    if source.count(ANCHOR) != 1:
        raise RuntimeError("EXPECTED_EHP_ROOT_ANCHOR_MISSING")
    if source.count("build_public_composite_zero_transport_provider(bridge)") != 1:
        raise RuntimeError("R4R14R5_SOURCE_WIRING_MISSING")
    if INSERT in source:
        return source
    updated = source.replace(ANCHOR, INSERT + ANCHOR, 1)
    tree = ast.parse(updated)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef)
               and node.name == "shared_expansion_provider"]
    if len(matches) != 1:
        raise RuntimeError("SHARED_PROVIDER_DEFINITION_CHANGED")
    return updated


def verify_and_apply(root: Path, dry_run: bool) -> str:
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("STAGED_FILES_PRESENT")
    f = root / TARGET
    raw = f.read_bytes()
    if b"\r" in raw.replace(b"\r\n", b""):
        raise RuntimeError("MIXED_OR_INVALID_EOL")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    source = raw.decode("utf-8").replace("\r\n", "\n")
    updated = next_source(source)
    if INSERT in source:
        before = source.replace(INSERT, "", 1)
        if source_hash(root, before) != R5_PIN:
            raise RuntimeError("UNREVIEWED_MODIFIED_SHARED_SOURCE")
        status = "ALREADY_APPLIED"
    else:
        if source_hash(root, source) != R5_PIN:
            raise RuntimeError("R5_SOURCE_BLOB_MISMATCH")
        status = "PATCH_REQUIRED"
        if not dry_run:
            f.write_bytes(updated.replace("\n", newline).encode("utf-8"))
    if not dry_run:
        tree = ast.parse(updated)
        fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                  and node.name == "shared_expansion_provider")
        complete = "\n".join(updated.splitlines()[fn.lineno - 1:fn.end_lineno])
        report = root / "phase175_r4r14r6_surjective_zero_codomain" / "SHARED_FUNCTION_FULL_JA.md"
        report.write_text(
            "# 更新後の共有関数全文\n\n"
            "`phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` 全文。\n\n"
            "```python\n" + complete + "\n```\n", encoding="utf-8",
        )
    return status


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    status = verify_and_apply(args.root, dry_run=args.dry_run)
    print("PHASE175_R4R14R6_PATCH_STATUS=" + status)
    print("PHASE175_R4R14R6_GATE=" + (
        "PASS_R4R14R6_DRYRUN_SOURCE_GUARD" if args.dry_run
        else "PASS_R4R14R6_SHARED_ROOT_PROVIDER_CONNECTED"
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())

```

## `audit.py`

```python
"""Actual search observation; a connected rule is not a completed proof."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase175_r4r14r6_surjective_zero_codomain.rule import RULE_NAME


def inspect_public_search() -> dict[str, object]:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 6))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    options = tuple(shared_expansion_provider(bridge, proof_target=root)(root))
    matches = tuple(option for option in options if option.rule.name == RULE_NAME)
    if len(matches) != 1:
        raise RuntimeError("SHARED_ROOT_ZERO_BRANCH_MISSING_OR_DUPLICATE")
    result = search_group_from_registered_goal(n=6, k=4)
    return {
        "target": "pi_10^6",
        "new_root_expansion": RULE_NAME,
        "new_root_subgoals": [str(x) for x in matches[0].subgoals],
        "root_proposal_count": len(options),
        "search_status": getattr(result.status, "value", str(result.status)),
        "proven_steps": len(result.proven_steps),
        "references": len(result.references),
        "open_goals": [str(x) for x in result.open_goals],
        "root_conclusion": str(result.conclusion) if result.conclusion is not None else None,
        "new_given": 0,
        "full_pytest": False,
    }


def main() -> int:
    report = inspect_public_search()
    path = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "EHP_Phase175_R4R14R6_search.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R4R14R6_NEW_ROOT_OPTIONS=1")
    print("PHASE175_R4R14R6_SEARCH_STATUS=" + report["search_status"])
    print("PHASE175_R4R14R6_PROVEN_STEPS=" + str(report["proven_steps"]))
    print("PHASE175_R4R14R6_OPEN_GOALS=" + str(len(report["open_goals"])))
    print("PHASE175_R4R14R6_REPORT=" + str(path))
    print("PHASE175_R4R14R6_COMPLETE_CLAIMED=False")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## `tests/test_rule.py`

```python
"""General surjective-and-zero-image zero-codomain proof contract."""
from __future__ import annotations

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import MapSurjective
from phase175_r4r14r6_surjective_zero_codomain.rule import (
    RULE_NAME, expand_surjective_zero_codomain,
    surjective_zero_codomain_inputs, surjective_zero_codomain_rule,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule


def root(i: int, n: int) -> TodaPrimaryGroupZeroStatement:
    return TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(i, n))


def test_pi106_has_typed_surjectivity_and_zero_image_goals() -> None:
    claim = root(10, 6)
    mapping = TodaSuspensionMap(TodaPrimaryGroup(9, 5), TodaPrimaryGroup(10, 6))
    required = surjective_zero_codomain_inputs(claim)
    assert required == (MapSurjective(mapping), ImageZeroStatement(mapping))
    options = expand_surjective_zero_codomain(claim)
    assert len(options) == 1
    assert options[0].subgoals == required
    assert options[0].rule.name == RULE_NAME


@pytest.mark.parametrize("i,n", [(9, 5), (10, 6), (12, 7), (15, 8)])
def test_root_candidate_is_not_stem_specific(i: int, n: int) -> None:
    claim = root(i, n)
    required = surjective_zero_codomain_inputs(claim)
    assert required is not None
    assert required[0].map == required[1].map
    assert required[0].map.target_group == claim.group


@pytest.mark.parametrize("invalid", [root(1, 2), root(3, 2), root(2, 3), root(5, 7), "zero", None])
def test_invalid_or_below_diagonal_goals_fail_closed(invalid: object) -> None:
    assert surjective_zero_codomain_inputs(invalid) is None
    assert expand_surjective_zero_codomain(invalid) == ()


def test_rule_needs_two_independently_inferred_premises() -> None:
    claim = root(10, 6)
    required = surjective_zero_codomain_inputs(claim)
    assert required is not None
    rule = surjective_zero_codomain_rule(claim)
    parents = tuple(ProofStep(x, (), ProofRule.INFERENCE) for x in required)
    matches = find_inference_matches_for_rule(rule, parents)
    assert len(matches) == 1
    derived = derive_inference_proof_step(matches[0])
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == claim
    assert derived.premises == parents
    assert find_inference_matches_for_rule(rule, parents[:1]) == ()
    assert find_inference_matches_for_rule(rule, (ProofStep(required[0], (), ProofRule.GIVEN), parents[1])) == ()
    assert find_inference_matches_for_rule(rule, (parents[0], ProofStep(required[1], (), ProofRule.GIVEN))) == ()


def test_wrong_map_cannot_close_zero_group() -> None:
    claim = root(10, 6)
    required = surjective_zero_codomain_inputs(claim)
    assert required is not None
    wrong = TodaSuspensionMap(TodaPrimaryGroup(10, 6), TodaPrimaryGroup(11, 7))
    rule = surjective_zero_codomain_rule(claim)
    assert find_inference_matches_for_rule(rule, (
        ProofStep(MapSurjective(wrong), (), ProofRule.INFERENCE),
        ProofStep(required[1], (), ProofRule.INFERENCE),
    )) == ()


def test_backward_expansion_creates_no_given_or_proof_step() -> None:
    options = expand_surjective_zero_codomain(root(10, 6))
    assert len(options) == 1
    assert all(not isinstance(x, ProofStep) for x in options[0].subgoals)

```

## `tests/test_installer.py`

```python
"""No repeat patch, no unreviewed source, no premature completion."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase175_r4r14r6_surjective_zero_codomain.installer import (
    ANCHOR, INSERT, next_source,
)


def test_anchor_adds_once_and_retains_old_delta_route() -> None:
    before = (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        "        build_public_composite_zero_transport_provider(bridge)\n"
        + ANCHOR + "\n"
        "        return ()\n"
        "    return expand\n"
    )
    after = next_source(before)
    assert after.count(INSERT) == 1
    assert ANCHOR in after
    ast.parse(after)
    assert next_source(after) == after


def test_changed_anchor_fails_closed() -> None:
    with pytest.raises(RuntimeError, match="EXPECTED_EHP_ROOT_ANCHOR_MISSING"):
        next_source("def unrelated():\n    return None\n")


def test_no_source_or_group_given_is_inserted() -> None:
    assert "GIVEN" not in INSERT
    assert "Toda (5.9)" not in INSERT
    assert "pi_10" not in INSERT
    assert "expand_surjective_zero_codomain(goal)" in INSERT

```

## `tests/test_public.py`

```python
"""Real shared provider proposal, not a claimed completed group proof."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase175_r4r14r6_surjective_zero_codomain.rule import (
    RULE_NAME, surjective_zero_codomain_inputs,
)


def test_live_root_has_exactly_one_generic_zero_codomain_option() -> None:
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 6))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=goal)
    options = tuple(shared_expansion_provider(bridge, proof_target=goal)(goal))
    matches = tuple(option for option in options if option.rule.name == RULE_NAME)
    assert len(matches) == 1
    assert matches[0].subgoals == surjective_zero_codomain_inputs(goal)

```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $argsList = @('-m', 'phase175_r4r14r6_surjective_zero_codomain.installer', '--root', $root)
    if ($DryRun) { $argsList += '--dry-run' }
    python @argsList
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R6 source guard or install failed' }
    if ($DryRun) { exit 0 }

    python -m pytest -q --import-mode=importlib -p no:cacheprovider `
        phase175_r4r14r6_surjective_zero_codomain/tests/test_rule.py `
        phase175_r4r14r6_surjective_zero_codomain/tests/test_installer.py `
        phase175_r4r14r6_surjective_zero_codomain/tests/test_public.py `
        phase175_r4r14r5_public_zero_transport/tests/test_provider.py `
        phase174_r3_r7_r3_ehp_zero_rule/tests/test_rule.py
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R6 focused tests failed' }
    Write-Output 'PHASE175_R4R14R6_FOCUSED_TESTS=PASS'

    python -m phase175_r4r14r6_surjective_zero_codomain.audit
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R6 public search audit failed' }
    Write-Output 'PHASE175_R4R14R6_NEW_GIVEN=0'
    Write-Output 'PHASE175_R4R14R6_GATE=PASS_R4R14R6_GENERIC_ROOT_AND_SEARCH_AUDITED'
} finally {
    Pop-Location
}

```

変更後の既存関数全文は `run.ps1` の本実行で `SHARED_FUNCTION_FULL_JA.md` に保存される。

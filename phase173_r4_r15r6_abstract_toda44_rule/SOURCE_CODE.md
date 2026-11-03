# Phase 173 R4-R15R6 — 新規コード・テスト全文

変更対象は以下の全て新規ファイル。既存ファイル・クラス・関数・import の変更なし。

- `abstract_rule.py`（追加位置: `phase173_r4_r15r6_abstract_toda44_rule/abstract_rule.py`）
- `audit.py`（追加位置: `phase173_r4_r15r6_abstract_toda44_rule/audit.py`）
- `preflight.py`（追加位置: `phase173_r4_r15r6_abstract_toda44_rule/preflight.py`）
- `run.ps1`（追加位置: `phase173_r4_r15r6_abstract_toda44_rule/run.ps1`）
- `tests/test_static.py`（追加位置: `phase173_r4_r15r6_abstract_toda44_rule/tests/test_static.py`）
- `tests/test_integration.py`（追加位置: `phase173_r4_r15r6_abstract_toda44_rule/tests/test_integration.py`）
- `__init__.py`（追加位置: `phase173_r4_r15r6_abstract_toda44_rule/__init__.py`）
- `tests/__init__.py`（追加位置: `phase173_r4_r15r6_abstract_toda44_rule/tests/__init__.py`）

各ファイルをそのまま追加できる。`...` による省略は行っていない。

## `abstract_rule.py`

```python
"""A generator-independent typed consequence of Toda Proposition 4.4.

A source-screened Proposition 4.4, cited Hopf identity and two independently
admitted earlier DB groups are REQUIRED. Only the abstract group structure is
concluded. This never identifies a named generator or installs a Web route.
"""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase169_r10e4_ordered_db_prior.db_prior import (
    group_coordinates,
    verified_db_step,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
)
from phase173_r4_r10_general_toda56_core.core import (
    HOPF_ROOT_NAME,
    _abstract_group_signature,
    checked_abstract_inputs,
)
from proof import (
    InferenceRule,
    LiteratureReference,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)


ABSTRACT_RULE_NAME = "Toda Proposition 4.4 source-first abstract direct-sum result"


@dataclass(frozen=True)
class TodaProp44AbstractGroupResult:
    """Abstract cyclic invariants, never a labelled generator presentation.

    A ('free', 0) entry denotes one infinite cyclic summand. Each
    ('finite', m) entry denotes an abstract cyclic summand of order m.
    """

    group: TodaPrimaryGroup
    invariant_summands: tuple[tuple[str, int], ...]


def canonical_abstract_result(proof_target: object) -> TodaProp44AbstractGroupResult | None:
    """Construct only a DB-screened n=4, k-unbounded abstract consequence."""
    pair = checked_abstract_inputs(proof_target)
    coords = group_coordinates(proof_target)
    if pair is None or coords is None:
        return None
    n, k = coords
    if n != 4 or type(k) is not int or k < 3:
        return None
    signatures = tuple(_abstract_group_signature(item) for item in pair)
    if any(signature is None for signature in signatures):
        return None
    invariants = tuple(sorted(signatures[0] + signatures[1]))
    return TodaProp44AbstractGroupResult(
        group=TodaPrimaryGroup(n + k, n),
        invariant_summands=invariants,
    )


def abstract_toda44_rule(
    statement: TodaProp44AbstractGroupResult, *,
    proof_target: object, bridge: object = None,
) -> InferenceRule:
    """Require the exact cited theorem, two verified DB priors and Hopf inference.

    This is an inference-rule candidate only; it NEVER manufactures a GIVEN
    statement or automatically adds a source to a proof context.
    """
    expected_result = canonical_abstract_result(proof_target)
    if expected_result is None or statement != expected_result:
        raise ValueError("Unreviewed or noncanonical abstract Proposition 4.4 target")
    first, second = checked_abstract_inputs(proof_target)
    theorem = TodaProp44UniversalStatement()
    hopf = canonical_hopf_relation()
    expected = (theorem, first, second, hopf)

    def guard(premises, bindings):
        if len(premises) != 4 or bindings:
            return False
        if tuple(step.conclusion for step in premises) != expected:
            return False
        theorem_step, first_step, second_step, hopf_step = premises
        if (theorem_step.rule is not ProofRule.GIVEN
                or not verified_db_step(first_step, proof_target=proof_target, bridge=bridge)
                or not verified_db_step(second_step, proof_target=proof_target, bridge=bridge)):
            return False
        if (hopf_step.rule is not ProofRule.INFERENCE
                or hopf_step.inference_rule is None
                or hopf_step.inference_rule.name != HOPF_ROOT_NAME
                or hopf_step.inference_rule.conclusion_pattern != hopf
                or len(hopf_step.premises) != 1):
            return False
        original = hopf_step.premises[0]
        if (original.rule is not ProofRule.GIVEN
                or original.conclusion != TodaLemma54TypedSource()
                or not hopf_step.inference_rule.match_guard((original,), ())):
            return False
        return (canonical_abstract_result(proof_target) == statement
                and checked_abstract_inputs(proof_target) == (first, second))

    return InferenceRule(
        name=ABSTRACT_RULE_NAME,
        description=(
            "Derive abstract free and 2-primary cyclic invariants by the "
            "source-verified Toda Proposition 4.4 splitting using "
            "H(nu_4)=iota_7 from Lemma 5.4 and two independently adopted "
            "earlier database groups. No individual generator transport is asserted."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=TodaProp44UniversalStatement,
                statement_pattern=theorem,
            ),
            PremisePattern(statement_type=type(first), statement_pattern=first),
            PremisePattern(statement_type=type(second), statement_pattern=second),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=hopf,
            ),
        ),
        conclusion_pattern=statement,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Proposition 4.4", locator="Proposition 4.4",
        ),
    )


def expand_abstract_toda44(
    statement: object, available: tuple[object, ...], *,
    proof_target: object, bridge: object = None,
) -> tuple[GoalExpansion, ...]:
    """Offer an abstract root only in an independently source-screened context."""
    if not isinstance(available, tuple):
        raise TypeError("Source-screened context must be a tuple")
    if not isinstance(statement, TodaProp44AbstractGroupResult):
        return ()
    if canonical_abstract_result(proof_target) != statement:
        return ()
    for source in (TodaProp44UniversalStatement(), TodaLemma54TypedSource()):
        if sum(type(item) is type(source) and item == source for item in available) != 1:
            return ()
    first, second = checked_abstract_inputs(proof_target)
    return (GoalExpansion(
        abstract_toda44_rule(statement, proof_target=proof_target, bridge=bridge),
        (TodaProp44UniversalStatement(), first, second, canonical_hopf_relation()),
    ),)
```

## `audit.py`

```python
"""Report k-unbounded abstract roots, without promoting named/public proof."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource
from phase173_r4_r10_general_toda56_core.core import checked_general_inputs
from phase173_r4_r15r6_abstract_toda44_rule.abstract_rule import (
    canonical_abstract_result,
    expand_abstract_toda44,
)


def inspect_k(k: int) -> dict[str, object]:
    """Read registered group and abstract proposal for any permitted k."""
    if type(k) is not int or k < 3:
        raise ValueError("k must be an integer >= 3")
    goal = exact_prior_database_result(4, k)
    statement = canonical_abstract_result(goal)
    sources = (TodaProp44UniversalStatement(), TodaLemma54TypedSource())
    expansions = (
        expand_abstract_toda44(statement, sources, proof_target=goal)
        if statement is not None else ()
    )
    return {
        "k": k,
        "group": f"pi_{k + 4}^4",
        "registered_target": goal is not None,
        "abstract_result": statement is not None,
        "invariant_summands": (
            [list(item) for item in statement.invariant_summands]
            if statement is not None else []
        ),
        "source_screened_rule_proposals": len(expansions),
        "strict_named_generator_guard": (
            checked_general_inputs(goal) is not None if goal is not None else False
        ),
        "theorem_citation_screening_performed_here": False,
        "proof_step_replayed_in_this_audit": False,
        "new_given_created": False,
        "public_completion": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not (args.root / "data" / "sphere.csv").is_file():
        raise RuntimeError("Expected repository root")
    rows = [inspect_k(k) for k in (3, 4, 7, 8, 31)]
    report = {
        "phase": "173-R4-R15R6",
        "mode": "ABSTRACT_TODA44_TYPED_ROOT_NOT_PUBLIC_PROOF",
        "rows": rows,
        "new_named_generator_equalities": 0,
        "new_given": 0,
        "public_completion": False,
        "full_pytest_performed": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(
            "PHASE173_R4_R15R6_K=" + str(row["k"])
            + " ABSTRACT=" + str(row["abstract_result"])
            + " ROOT_CANDIDATE=" + str(row["source_screened_rule_proposals"])
            + " NAMED_GUARD=" + str(row["strict_named_generator_guard"]),
            flush=True,
        )
    k31 = rows[-1]
    passed = (
        k31["abstract_result"] is True
        and k31["source_screened_rule_proposals"] == 1
        and k31["invariant_summands"] == [["finite", 2]] * 8
        and k31["strict_named_generator_guard"] is False
        and k31["public_completion"] is False
    )
    print("PHASE173_R4_R15R6_K31_ABSTRACT_RULE=" + ("PASS" if passed else "FAIL"), flush=True)
    print("PHASE173_R4_R15R6_PUBLIC_COMPLETION=False", flush=True)
    print("PHASE173_R4_R15R6_REPORT=" + str(args.output), flush=True)
    print("PHASE173_R4_R15R6_AUDIT=" + ("PASS" if passed else "FAIL"), flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## `preflight.py`

```python
"""Review-pinned Git lineage and source content checks for R15R6."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

REVIEWED_HEAD = "1f46799f0673df0de880830b37bea7071cba64b8"
REVIEWED_BLOBS = {'phase173_r4_r10_general_toda56_core/core.py': 'd35600804ecbbc5f8566d52e45a2f6ecf8816347', 'phase169_r10e4_ordered_db_prior/db_prior.py': 'ed8c6a1f0f6f130005d42a2edba4ab40991e879b', 'phase173_r4_r1_lemma54_source_bridge/source.py': 'a37bf7447194d72526522366944778c386c8966c', 'phase165_r52_r27_r5_literature.py': 'c9bfe2788f4cf043db6dada98a437afea6accf75', 'phase173_r4_r10_general_toda56_core/tests/test_core.py': '68205bf2840688a7b5d7277875c513323be7a5fc', 'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395', 'data/HyoujiGen.csv': '26f33db0c83ba7f151433583fe861598399cbe6a'}
REVIEWED_PREVIOUS_PACKAGE = {'phase173_r4_r15r5_family_source_frontier/audit.py': '46cb627981db32b930a316b329a6cf8c37b4ddba93cfde6f1d4ca6febbd9e83a', 'phase173_r4_r15r5_family_source_frontier/source_scan.py': 'df73926f4bd2b4b33d13fa582e4bb1da252b0c1373f2f8cd3062314d617e4523', 'phase173_r4_r15r5_family_source_frontier/preflight.py': '036498cae089b1f211c4e2d4981a8bdccaaff662a1ffd36c03032a2e303aa1ff'}
ALLOWED_COMMITTED_PREFIX = "phase173_r4_r15r5_family_source_frontier/"
ALLOWED_CACHE = ".pytest_cache/v/cache/nodeids"


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if completed.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + completed.stderr[:600])
    return completed.stdout.strip()


def is_allowed_committed(path: str) -> bool:
    return path == ALLOWED_CACHE or path.startswith(ALLOWED_COMMITTED_PREFIX)


def sha256_normalized(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def preflight(root: Path) -> None:
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Expected repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    head = git(root, "rev-parse", "HEAD")
    if git(root, "rev-parse", "origin/develop") != head:
        raise RuntimeError("GitHub develop HEAD and local HEAD differ")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head),
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode:
        raise RuntimeError("Unreviewed HEAD lineage")
    committed = tuple(filter(None, git(root, "diff", "--name-only", REVIEWED_HEAD, head).splitlines()))
    if any(not is_allowed_committed(path) for path in committed):
        raise RuntimeError("Unreviewed committed files: " + repr(committed))
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    dirty = tuple(filter(None, git(root, "diff", "--name-only").splitlines()))
    if any(path != ALLOWED_CACHE for path in dirty):
        raise RuntimeError("Unreviewed tracked changes: " + repr(dirty))
    for relative, expected in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + relative) != expected:
            raise RuntimeError("Reviewed Git blob differs: " + relative)
        if git(root, "hash-object", "--", relative) != expected:
            raise RuntimeError("Reviewed worktree differs: " + relative)
    for relative, expected in REVIEWED_PREVIOUS_PACKAGE.items():
        path = root / relative
        if not path.is_file() or sha256_normalized(path) != expected:
            raise RuntimeError("R15R5 previous source changed: " + relative)
    print("PHASE173_R4_R15R6_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R6_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R6_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R6_PRODUCTION_EDIT=NONE", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    preflight(args.root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R6 Git fetch failed' }

    python -m phase173_r4_r15r6_abstract_toda44_rule.preflight --root "$Root"
    if ($LASTEXITCODE -ne 0) { throw 'R15R6 source preflight failed' }

    python -m pytest -q `
        phase173_r4_r15r6_abstract_toda44_rule/tests/test_static.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R6 static tests failed' }

    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R6_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R6_PRODUCTION_EDIT=NONE'
        exit 0
    }

    python -m pytest -q `
        phase173_r4_r15r6_abstract_toda44_rule/tests/test_integration.py `
        phase173_r4_r15r5_family_source_frontier/tests/test_integration.py `
        phase173_r4_r15r1_unbounded_abstract_frontier/tests/test_frontier.py `
        phase173_r4_r10_general_toda56_core/tests/test_core.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R6 focused pytest failed' }
    Write-Output 'PHASE173_R4_R15R6_FOCUSED_PYTEST=PASS'

    python -m phase173_r4_r15r6_abstract_toda44_rule.audit `
        --root "$Root" `
        --output (Join-Path $PSScriptRoot 'abstract_toda44_report.json')
    if ($LASTEXITCODE -ne 0) { throw 'R15R6 abstract root audit failed' }
    Write-Output 'PHASE173_R4_R15R6_PHASE_COMPLETED=False'
} finally {
    Pop-Location
}
```

## `tests/test_static.py`

```python
"""Standalone regression and fail-closed content constraints."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r15r6_abstract_toda44_rule.preflight import (
    is_allowed_committed,
    sha256_normalized,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("filename", ("abstract_rule.py", "audit.py", "preflight.py"))
def test_source_is_parsable_and_has_no_ellipsis(filename: str) -> None:
    source = (ROOT / filename).read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert not any(isinstance(node, ast.Expr)
                   and isinstance(node.value, ast.Constant)
                   and node.value.value is Ellipsis
                   for node in ast.walk(tree))
    assert "eval(" not in source
    assert "exec(" not in source


def test_only_prior_audit_commit_paths_allowed() -> None:
    assert is_allowed_committed("phase173_r4_r15r5_family_source_frontier/audit.py")
    assert is_allowed_committed(".pytest_cache/v/cache/nodeids")
    assert not is_allowed_committed("phase173_r4_r10_general_toda56_core/core.py")
    assert not is_allowed_committed("sources/toda/Toda_06_2.tex")
    assert not is_allowed_committed("phase173_r4_r15r6_abstract_toda44_rule/audit.py")


def test_source_identity_is_line_ending_tolerant_only(tmp_path: Path) -> None:
    path = tmp_path / "test.py"
    path.write_bytes(b"a=1\nb=2\n")
    digest = sha256_normalized(path)
    path.write_bytes(b"a=1\r\nb=2\r\n")
    assert sha256_normalized(path) == digest
    path.write_bytes(b"a=1\r\nb=3\r\n")
    assert sha256_normalized(path) != digest


def test_no_public_proof_or_given_is_created() -> None:
    source = (ROOT / "audit.py").read_text(encoding="utf-8")
    assert '"public_completion": False' in source
    assert '"new_given": 0' in source
    rule = (ROOT / "abstract_rule.py").read_text(encoding="utf-8")
    assert "conclusion_pattern=statement" in rule
    assert "verified_db_step(first_step" in rule
    assert "verified_db_step(second_step" in rule
    assert "checked_abstract_inputs(proof_target)" in rule


def test_runner_uses_only_focused_pytest() -> None:
    s = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "-DryRun" not in s
    assert "pytest -q" in s
    assert "phase173_r4_r10_general_toda56_core/tests/test_core.py" in s
    assert "git reset" not in s
    assert "git checkout" not in s
```

## `tests/test_integration.py`

```python
"""Focused real-repository typed abstract inference contracts."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step,
    exact_prior_database_result,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
    lemma54_hopf_inference_rule,
)
from phase173_r4_r10_general_toda56_core.core import checked_general_inputs
from phase173_r4_r15r6_abstract_toda44_rule.abstract_rule import (
    ABSTRACT_RULE_NAME,
    canonical_abstract_result,
    abstract_toda44_rule,
    expand_abstract_toda44,
)
from proof import (
    ProofRule,
    ProofStep,
    apply_inference_match,
    find_inference_matches_for_rule,
)


@pytest.mark.parametrize("k", (3, 4, 7, 8, 31))
def test_canonical_abstract_result_is_k_unbounded(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    statement = canonical_abstract_result(goal)
    assert statement is not None
    assert statement.group == TodaPrimaryGroup(4 + k, 4)
    assert statement.invariant_summands is not None
    proposals = expand_abstract_toda44(
        statement, (TodaProp44UniversalStatement(), TodaLemma54TypedSource()),
        proof_target=goal,
    )
    assert len(proposals) == 1
    assert proposals[0].rule.name == ABSTRACT_RULE_NAME


def test_k31_abstract_result_is_eight_order_two_factors_not_named() -> None:
    goal = exact_prior_database_result(4, 31)
    statement = canonical_abstract_result(goal)
    assert statement is not None
    assert statement.invariant_summands == (("finite", 2),) * 8
    assert checked_general_inputs(goal) is None
    assert not hasattr(statement, "generator")


def test_k31_source_screen_rejects_missing_duplicate_and_wrong_target() -> None:
    goal = exact_prior_database_result(4, 31)
    statement = canonical_abstract_result(goal)
    theorem = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    assert expand_abstract_toda44(statement, (), proof_target=goal) == ()
    assert expand_abstract_toda44(statement, (theorem,), proof_target=goal) == ()
    assert expand_abstract_toda44(statement, (theorem, lemma, lemma), proof_target=goal) == ()
    assert expand_abstract_toda44(
        statement, (theorem, lemma),
        proof_target=exact_prior_database_result(4, 8),
    ) == ()
    forged = replace(statement, invariant_summands=(("finite", 4),) * 4)
    assert expand_abstract_toda44(forged, (theorem, lemma), proof_target=goal) == ()


def test_k31_proof_engine_rule_replay_rejects_unadmitted_priors() -> None:
    goal = exact_prior_database_result(4, 31)
    statement = canonical_abstract_result(goal)
    source = (TodaProp44UniversalStatement(), TodaLemma54TypedSource())
    rule = expand_abstract_toda44(statement, source, proof_target=goal)[0].rule
    from phase173_r4_r10_general_toda56_core.core import checked_abstract_inputs
    first, second = checked_abstract_inputs(goal)
    lemma = ProofStep(TodaLemma54TypedSource(), (), ProofRule.GIVEN)
    hopf_goal = canonical_hopf_relation()
    hopf = ProofStep(
        hopf_goal, (lemma,), ProofRule.INFERENCE,
        inference_rule=lemma54_hopf_inference_rule(hopf_goal),
    )
    steps = (
        ProofStep(TodaProp44UniversalStatement(), (), ProofRule.GIVEN),
        admitted_db_step(first, proof_target=goal),
        admitted_db_step(second, proof_target=goal),
        hopf,
    )
    assert all(step is not None for step in steps)
    matches = find_inference_matches_for_rule(rule, steps)
    assert len(matches) == 1
    derived = apply_inference_match(matches[0])
    assert derived.conclusion == statement
    assert derived.rule is ProofRule.INFERENCE
    assert rule.match_guard((steps[0], steps[2], steps[1], steps[3]), ()) is False
    forged = ProofStep(first, (), ProofRule.GIVEN)
    assert rule.match_guard((steps[0], forged, steps[2], steps[3]), ()) is False
    wrong_hopf = ProofStep(hopf_goal, (), ProofRule.GIVEN)
    assert rule.match_guard((steps[0], steps[1], steps[2], wrong_hopf), ()) is False
    # These are isolated contract-test leaves, not an audited public source tree.


def test_existing_named_generator_root_is_unchanged() -> None:
    goal = exact_prior_database_result(4, 8)
    assert checked_general_inputs(goal) is None
    goal31 = exact_prior_database_result(4, 31)
    assert checked_general_inputs(goal31) is None
    assert canonical_abstract_result(goal31) is not None
```

## `__init__.py`

```python
"""Phase 173 R4-R15R6 typed abstract Proposition 4.4 candidates."""
```

## `tests/__init__.py`

```python

```

# Phase 175 R4R5R3 — 変更コード全文

## 変更対象

- 既存 `phase165_r52_r9_shared_math.py`：`shared_expansion_provider()` の関数全体。トップレベル import の変更なし。
- 新規 `phase175_r4r5r3_public_order_zero/provider.py`：一般規則の公開 Provider。
- 新規 `phase175_r4r5r3_public_order_zero/installer.py`：固定 blob の確認・AST 単位の関数置換。
- 新規監査・限定テスト・文書。R4R5R2 の `rule.py` はバイト単位で変更なし。

## 既存関数全文の出力

DryRun または本実行で、現行コードと一致する全関数を `EHPProofTracerAudit/phase175_r4r5r3_public_order_zero/<UTC-stamp>/shared_expansion_provider_FULL.py` に出力する。入力コードは Git BLOB `ee1efa2d91df479168b7b964d24e814e0f516449` との完全一致が必要。実装時は関数全体を AST で抽出・置換し、他の関数と既存 module import は変更しない。

本書には新規・変更した全ファイルの import と関数全文をそのまま収録する。

## 新規 Provider（全 import・関数全文）

`provider.py`

```python
"""General backward provider: a proved finite cyclic summand has order m.

Every proposal is conditional on proving its complete group presentation.
Only an earlier, explicit DB prior or a source-screened/previously completed
presentation may be proposed. This provider never creates ProofSteps or GIVEN.
"""
from __future__ import annotations

from collections.abc import Callable

from homotopy_groups import TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import (
    exact_prior_database_result, group_coordinates, precedes_db_goal,
)
from phase175_r4r5_eta7_annihilator_isolated.rule import (
    expand_finite_cyclic_order_zero, order_zero_premise,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def eligible_order_zero_sources(
    goal: object, *, bridge: object, proof_target: object,
    prior_conclusions: tuple = (),
) -> tuple[Relation, ...]:
    """Find source-bound candidates; their ProofSteps remain search obligations.

    The root's original typed group statement is the only proof-use order
    anchor. DB rows for the source group are re-read; stable fallback and
    unscreened citations are never accepted as evidence.
    """
    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be a tuple")
    root = group_coordinates(proof_target)
    requested = order_zero_premise(goal)
    if root is None or requested is None:
        return ()
    source = group_coordinates(requested)
    if source is None or not precedes_db_goal(*source, *root):
        return ()

    candidates: list[Relation] = []

    def include(statement: object) -> None:
        if (isinstance(statement, Relation)
                and statement.relation_type is RelationType.EQUALITY
                and group_coordinates(statement) == source
                and order_zero_premise(goal, statement) == statement
                and statement not in candidates):
            candidates.append(statement)

    # These are completed, ordered internal proof conclusions, never created here.
    for statement in prior_conclusions:
        include(statement)

    # Only citation-screened fixed source statements may be used as candidates.
    registry = getattr(bridge, "registry", None)
    links = getattr(bridge, "proof_links", ())
    if registry is not None:
        for link in links:
            step = getattr(link, "step", None)
            if step is None or step.rule is not ProofRule.GIVEN:
                continue
            assertion = registry.assertion(link.assertion_id)
            if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                    and assertion.content == step.conclusion):
                include(step.conclusion)

    # The original exact-DB prior rule verifies/adopts this source in the
    # ordinary resolver; merely discovering the row is never a ProofStep.
    include(exact_prior_database_result(*source))
    return tuple(candidates)


def build_public_order_zero_provider(
    *, bridge: object, proof_target: object, prior_conclusions: tuple = (),
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Expose one generic inference to every shared backward-search root.

    The canonical resolver rechecks an actual earlier DB row or accepted source
    ProofStep, then applies the R4R5R2 InferenceRule. No target-specific branch.
    """
    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be a tuple")

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        candidates = eligible_order_zero_sources(
            goal, bridge=bridge, proof_target=proof_target,
            prior_conclusions=prior_conclusions,
        )
        if not candidates:
            return ()
        return expand_finite_cyclic_order_zero(goal, candidates)

    return expand
```

## 既存関数の丸ごと置換装置（全 import・関数全文）

`installer.py`

```python
"""Pinned whole-function replacement for shared_expansion_provider only.

No regex-based partial edits or changes to the module-level imports.
The full replacement function is emitted to output/ on actual installation.
"""
from __future__ import annotations

import ast
from pathlib import Path
import subprocess
import tempfile

TARGET_RELATIVE = Path("phase165_r52_r9_shared_math.py")
TARGET_FUNCTION = "shared_expansion_provider"
PINNED_GIT_BLOB = "ee1efa2d91df479168b7b964d24e814e0f516449"
INSERTION = '''
    # Phase 175 R4R5R3: reusable finite-cyclic summand order-to-zero rule.
    # All proof steps are resolved by the ordinary citation/DB-prior gate.
    from phase175_r4r5r3_public_order_zero.provider import (
        build_public_order_zero_provider,
    )
    extra_providers = (
        build_public_order_zero_provider(
            bridge=bridge, proof_target=proof_target,
            prior_conclusions=prior_conclusions,
        ),
    ) + tuple(extra_providers)
'''
ANCHOR = '''    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be a tuple")
'''


def git_blob(root: Path, reference: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", reference], cwd=root, text=True,
        capture_output=True, check=True,
    )
    return result.stdout.strip()


def function_replacement(original: str) -> tuple[str, str]:
    """Replace a complete AST-defined function while keeping other bytes.

    Both the existing and new source parse as Python. Reject unusual source
    shapes or multiple anchors rather than silently patching another function.
    """
    syntax = ast.parse(original)
    functions = [node for node in syntax.body if isinstance(node, ast.FunctionDef)
                 and node.name == TARGET_FUNCTION]
    if len(functions) != 1:
        raise RuntimeError("R4R5R3_FUNCTION_NOT_UNIQUE")
    function = functions[0]
    lines = original.splitlines(keepends=True)
    start, end = function.lineno - 1, function.end_lineno
    before = "".join(lines[start:end])
    if before.count(ANCHOR) != 1 or INSERTION.strip() in before:
        raise RuntimeError("R4R5R3_INSERTION_ANCHOR_CHANGED")
    after = before.replace(ANCHOR, ANCHOR + INSERTION, 1)
    whole = "".join(lines[:start]) + after + "".join(lines[end:])
    ast.parse(whole)
    return whole, after


def plan(root: Path) -> tuple[Path, bytes, bytes, str]:
    """Return a full-file, full-function replacement guarded by Git blob SHA."""
    path = root / TARGET_RELATIVE
    data = path.read_bytes()
    if b"\r\n" in data:
        normalized = data.decode("utf-8").replace("\r\n", "\n")
        eol = "\r\n"
    else:
        normalized = data.decode("utf-8")
        eol = "\n"
    committed = git_blob(root, "HEAD:" + TARGET_RELATIVE.as_posix())
    if committed != PINNED_GIT_BLOB:
        raise RuntimeError("R4R5R3_PRODUCTION_SOURCE_BLOB_CHANGED")
    # --path applies Git's checkout clean filters (including Windows CRLF).
    working = subprocess.run(
        ["git", "hash-object", "--path", TARGET_RELATIVE.as_posix(), str(path)],
        cwd=root, text=True, check=True, capture_output=True,
    ).stdout.strip()
    if working != PINNED_GIT_BLOB:
        raise RuntimeError("R4R5R3_PRODUCTION_SOURCE_BLOB_CHANGED")
    replaced, full_function = function_replacement(normalized)
    return path, data, replaced.replace("\n", eol).encode("utf-8"), full_function


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    path, old, new, full_function = plan(root)
    output.mkdir(parents=True, exist_ok=True)
    # Whole function, not a diff. This is the exact post-install replacement.
    (output / "shared_expansion_provider_FULL.py").write_text(
        full_function, encoding="utf-8",
    )
    if not dry_run:
        with tempfile.NamedTemporaryFile(mode="wb", delete=False,
                                         dir=path.parent, prefix=".r4r5r3_") as stream:
            temporary = Path(stream.name)
            stream.write(new)
        try:
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
        if path.read_bytes() != new:
            raise RuntimeError("R4R5R3_REPLACEMENT_MISMATCH")
    return {
        "target": TARGET_RELATIVE.as_posix(),
        "class_changes": [],
        "changed_function": TARGET_FUNCTION,
        "module_imports_changed": False,
        "other_functions_unchanged": True,
        "dry_run": dry_run,
        "full_replacement_path": str(output / "shared_expansion_provider_FULL.py"),
        "original_size": len(old),
        "replacement_size": len(new),
    }
```

## 監査（全 import・関数全文）

`audit.py`

```python
"""Phase 175 R4R5R3: source-guarded general public order-zero wiring.

One shared backward provider is added; previous isolated R4R5R2 results
are revalidated as audit provenance and NEVER inserted as proof certificates.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback

from phase175_r4r5r3_public_order_zero import installer

EXPECTED_HEAD = "2789fb6297efaa35962695b95300063feb6e2ea2"
PRIOR_GATE = "PASS_R4R5R2_DIRECT_SUM_ORDER_ZERO_ISOLATED_NOT_PUBLIC"
PRIOR_PACKAGE = "phase175_r4r5_eta7_annihilator_isolated"
PRIOR_RULE_SHA256 = "228a856bb4aa535edf4243885dee8472b8789c7d85c3507fc5eb1aace8a42bcd"
DRY_GATE = "PASS_R4R5R3_PUBLIC_PROVIDER_DRYRUN"
FINAL_GATE = "PASS_R4R5R3_SHARED_PROVIDER_CONNECTED_NOT_COMPLETE"


def latest_prior(explicit: Path | None) -> Path:
    if explicit is not None:
        path = explicit.resolve()
        if not path.is_file():
            raise RuntimeError("R4R5R3_PRIOR_REPORT_NOT_FOUND")
        return path
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PRIOR_PACKAGE
    for candidate in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            content = json.loads(candidate.read_text(encoding="utf-8"))
        except (ValueError, OSError, UnicodeError):
            continue
        if isinstance(content, dict) and content.get("gate") == PRIOR_GATE:
            return candidate
    raise RuntimeError("R4R5R3_SUCCESSFUL_R4R5R2_REPORT_MISSING")


def validate_prior(prior: object) -> dict[str, object]:
    if not isinstance(prior, dict):
        raise RuntimeError("R4R5R3_PRIOR_REPORT_INVALID")
    expected = {
        "phase": "175-R4R5R2", "gate": PRIOR_GATE,
        "dry_run": False, "production_changes": [], "new_given": 0,
        "new_mathematical_rules": 1, "rule_connected_to_public": False,
        "pi95_proof_complete": False, "full_pytest_executed": False,
    }
    if any(prior.get(k) != v for k, v in expected.items()):
        raise RuntimeError("R4R5R3_PRIOR_SCOPE_INVALID")
    pre = prior.get("preflight", {})
    eta = prior.get("eta7", {})
    direct = prior.get("direct_sum", {})
    if (not isinstance(pre, dict) or pre.get("head") != EXPECTED_HEAD
            or not isinstance(eta, dict) or not isinstance(direct, dict)
            or eta.get("derived_rule_proof_step") is not True
            or eta.get("prior_proof_search_executed") is not False
            or eta.get("prior_status") != "ADOPTED_DATABASE_PRIOR"
            or direct.get("inferred_zero_steps") != 2
            or direct.get("prior_proof_search_executed") is not False):
        raise RuntimeError("R4R5R3_PRIOR_EVIDENCE_INVALID")
    return {
        "prior_head": pre["head"], "isolated_eta7_verified": True,
        "isolated_direct_sum_inferences": 2,
        "prior_report_is_not_public_proof": True,
    }


def source_guard(root: Path) -> dict[str, str]:
    if installer.git_blob(root, "HEAD") != EXPECTED_HEAD:
        raise RuntimeError("R4R5R3_UNREVIEWED_HEAD")
    path = root / PRIOR_PACKAGE / "rule.py"
    if not path.is_file():
        raise RuntimeError("R4R5R3_R4R5R2_RULE_MISSING")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != PRIOR_RULE_SHA256:
        raise RuntimeError("R4R5R3_R4R5R2_RULE_DRIFT")
    return {
        "reviewed_head": EXPECTED_HEAD,
        "production_blob": installer.PINNED_GIT_BLOB,
        "isolated_rule_sha256": actual,
    }


def public_order_zero_evidence() -> dict[str, object]:
    """Verify real accepted DB-prior parent ProofSteps without prior search.

    This checks the public provider's source-first proposals against R4R5R2's
    exact two source groups and checks ordinary inference replay separately.
    It does not claim that pi_9^5 has a completed root proof tree.
    """
    from expression import Multiple, Zero
    from homotopy_groups import DirectSumGroup
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, verified_db_step,
    )
    from phase175_r4r5_eta7_annihilator_isolated.rule import RULE_NAME
    from phase175_r4r5r3_public_order_zero.provider import build_public_order_zero_provider
    from proof import (
        ProofRule, Relation, apply_inference_match, find_inference_matches_for_rule,
    )

    root = exact_prior_database_result(5, 4)
    eta = exact_prior_database_result(7, 1)
    direct = exact_prior_database_result(4, 4)
    if (not isinstance(root, Relation) or not isinstance(eta, Relation)
            or not isinstance(direct, Relation)
            or not isinstance(direct.rhs, DirectSumGroup)
            or len(direct.rhs.summands) != 2):
        raise RuntimeError("R4R5R3_SOURCE_ROWS_NOT_TYPED")
    bridge = object()
    expand = build_public_order_zero_provider(bridge=bridge, proof_target=root)
    counted = []
    sources = [eta] + [direct] * len(direct.rhs.summands)
    components = [eta.rhs] + list(direct.rhs.summands)
    for source, item in zip(sources, components):
        target = Relation(Multiple(item.order, item.generator), Zero())
        found = expand(target)
        if len(found) != 1 or found[0].subgoals != (source,) or found[0].rule.name != RULE_NAME:
            raise RuntimeError("R4R5R3_SHARED_SOURCE_FIRST_PROPOSAL_INVALID")
        admitted = admitted_db_step(source, proof_target=root)
        if admitted is None or not verified_db_step(admitted, proof_target=root):
            raise RuntimeError("R4R5R3_PARENT_DB_PRIOR_NOT_AUTHENTICATED")
        matches = find_inference_matches_for_rule(found[0].rule, (admitted,))
        if len(matches) != 1:
            raise RuntimeError("R4R5R3_INFERENCE_MATCH_FAILED")
        step = apply_inference_match(matches[0])
        if (step.rule is not ProofRule.INFERENCE
                or step.conclusion != target
                or step.premises != (admitted,)):
            raise RuntimeError("R4R5R3_INFERENCE_REPLAY_FAILED")
        counted.append(repr(target))
    return {
        "public_provider_proposals_with_verified_parent": len(counted),
        "source_groups": ["pi_8^7", "pi_8^4", "pi_8^4"],
        "conclusions": counted, "new_given": 0,
        "previous_proof_search_executed": False,
        "target_pi95_completed": False,
    }


def run(root: Path, *, dry_run: bool, prior_file: Path | None) -> int:
    folder = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / "phase175_r4r5r3_public_order_zero" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    folder.mkdir(parents=True, exist_ok=False)
    record: dict[str, object] = {
        "phase": "175-R4R5R3", "dry_run": dry_run,
        "new_given": 0, "new_mathematical_rules": 0,
        "connected_previously_isolated_general_rules": 1,
        "public_pi95_complete": False, "full_pytest_executed": False,
        "gate": "FAIL_R4R5R3_SOURCE_FIRST_PUBLIC_PROVIDER",
    }
    try:
        prior_path = latest_prior(prior_file)
        record["prior_report"] = str(prior_path)
        record["prior"] = validate_prior(json.loads(prior_path.read_text(encoding="utf-8")))
        record["source_guard"] = source_guard(root)
        # Check git clean before mutating. Untracked isolated packages are allowed.
        import subprocess
        changed = subprocess.run(
            ["git", "diff", "--name-only"], cwd=root, text=True,
            capture_output=True, check=True,
        ).stdout.strip().splitlines()
        changed += subprocess.run(
            ["git", "diff", "--cached", "--name-only"], cwd=root, text=True,
            capture_output=True, check=True,
        ).stdout.strip().splitlines()
        if any(name.strip() for name in changed):
            raise RuntimeError("R4R5R3_UNREVIEWED_TRACKED_CHANGES")
        record["install"] = installer.install(root, dry_run=dry_run, output=folder)
        if not dry_run:
            record["general_rule"] = public_order_zero_evidence()
            result = subprocess.run(
                [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
                 "--import-mode=importlib",
                 "phase175_r4r5r3_public_order_zero/tests/test_real_integration.py"],
                cwd=root, text=True, capture_output=True,
            )
            record["real_integration_pytest"] = {
                "exit_code": result.returncode,
                "stdout": result.stdout[-4000:],
                "stderr": result.stderr[-2000:],
            }
            if result.returncode != 0:
                raise RuntimeError("R4R5R3_REAL_INTEGRATION_PYTEST_FAILED")
        record["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as error:
        record["error"] = f"{type(error).__name__}: {error}"
        record["traceback"] = traceback.format_exc()[-6000:]
    (folder / "report.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (folder / "report.md").write_text(
        "# Phase 175 R4R5R3 — 一般零関係の共有探索接続\n\n"
        + "Gate: `" + str(record["gate"]) + "`\n\n"
        + "先行 DB 結果を再証明せず、既存の一般規則を共有 Provider に接続。\n"
        + "Proposition 2.5 と (5.8) は本段階の対象外。\n"
        + "π₉⁵ の完成証明は依然として未完成。\n",
        encoding="utf-8",
    )
    print("PHASE175_R4R5R3_HEAD=" + str(record.get("source_guard", {}).get("reviewed_head", "UNKNOWN")))
    print("PHASE175_R4R5R3_NEW_GIVEN=0")
    print("PHASE175_R4R5R3_NEW_MATHEMATICAL_RULES=0")
    print("PHASE175_R4R5R3_SHARED_RULE_CONNECTED=" + str(not dry_run and "error" not in record))
    print("PHASE175_R4R5R3_VERIFIED_PUBLIC_PROVIDER_EXAMPLES=" + str(record.get("general_rule", {}).get("public_provider_proposals_with_verified_parent", 0)))
    print("PHASE175_R4R5R3_PRIOR_PROOF_SEARCH_EXECUTED=False")
    print("PHASE175_R4R5R3_REAL_INTEGRATION_PYTEST=" + (
        "NOT_RUN" if dry_run else "PASS" if "error" not in record else "FAIL"
    ))
    print("PHASE175_R4R5R3_PI95_PROOF=NOT_COMPLETE")
    print("PHASE175_R4R5R3_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R5R3_FULL_FUNCTION=" + str(folder / "shared_expansion_provider_FULL.py"))
    print("PHASE175_R4R5R3_REPORT=" + str(folder / "report.json"))
    print("PHASE175_R4R5R3_GATE=" + str(record["gate"]))
    if "error" in record:
        print("PHASE175_R4R5R3_ERROR=" + str(record["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4r5r2-report", type=Path)
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run, prior_file=args.r4r5r2_report)


if __name__ == "__main__":
    sys.exit(main())
```

## PowerShell 全文

`run.ps1`

```powershell
param(
    [switch] $DryRun,
    [string] $R4R5R2Report = ""
)
$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$target = Join-Path $root 'phase165_r52_r9_shared_math.py'
$original = $null
Push-Location $root
try {
    $tests = @(
        'phase175_r4r5r3_public_order_zero/tests/test_provider.py',
        'phase175_r4r5r3_public_order_zero/tests/test_installer.py',
        'phase175_r4r5_eta7_annihilator_isolated/tests/test_rule.py',
        'phase175_r4r5_eta7_annihilator_isolated/tests/test_audit.py',
        'phase175_r4r4_pi95_premise_frontier/tests/test_audit.py',
        'phase175_r4r3_two_summand_quotient/tests/test_rule.py',
        'phase175_r4r3_two_summand_quotient/tests/test_audit.py',
        'phase175_r4_pi95_audit/tests/test_audit.py'
    )
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib @tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R5R3 focused baseline pytest failed' }
    Write-Output 'PHASE175_R4R5R3_FOCUSED_BASELINE_PYTEST=PASS'

    if (-not $DryRun) {
        $original = [System.IO.File]::ReadAllBytes($target)
    }
    $command = @('-B', '-m', 'phase175_r4r5r3_public_order_zero.audit', '--root', $root)
    if ($DryRun) { $command += '--dry-run' }
    if ($R4R5R2Report -ne '') { $command += @('--r4r5r2-report', $R4R5R2Report) }
    & python @command
    if ($LASTEXITCODE -ne 0) { throw 'R4R5R3 source guard or public wiring failed' }

    if (-not $DryRun) {
        Write-Output 'PHASE175_R4R5R3_PRODUCTION_PATCH=APPLIED'
    }
    Write-Output 'PHASE175_R4R5R3_EXIT_CODE=0'
    exit 0
} catch {
    if ($null -ne $original) {
        [System.IO.File]::WriteAllBytes($target, $original)
        Write-Output 'PHASE175_R4R5R3_PRODUCTION_PATCH=ROLLED_BACK'
    }
    Write-Output ('PHASE175_R4R5R3_ERROR=' + $_.Exception.Message)
    Write-Output 'PHASE175_R4R5R3_EXIT_CODE=1'
    exit 1
} finally {
    Pop-Location
}
```

## Provider テスト（全 import・関数全文）

`tests/test_provider.py`

```python
"""R4R5R3 general source-first backward-provider contracts (test shapes only)."""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from expression import GeneratorSymbol, HomotopyElement, Multiple, Zero
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase175_r4r5r3_public_order_zero import provider
from phase175_r4r5_eta7_annihilator_isolated.rule import RULE_NAME
from proof import InferenceRule, ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def component(n: int, k: int = 1, label: str = "a") -> HomotopyElement:
    return HomotopyElement(label, n, source=n+k, target=n,
                           generator=GeneratorSymbol(label, index=n))


def sample_goal(generator: HomotopyElement, order: int) -> Relation:
    return Relation(Multiple(order, generator), Zero(), RelationType.EQUALITY)


def prior_root() -> Relation:
    return Relation(TodaPrimaryGroup(9, 5), FiniteCyclicGroup(2, component(5, 4)))


@dataclass(frozen=True)
class FakeAssertion:
    origin: object
    content: object


@dataclass(frozen=True)
class FakeLink:
    assertion_id: str
    step: object


class FakeRegistry:
    def __init__(self, source: Relation, origin=AssertionOrigin.FIXED_STATEMENT):
        self.record = FakeAssertion(origin, source)

    def assertion(self, ident: str) -> FakeAssertion:
        assert ident == "fixed"
        return self.record


class FakeBridge:
    def __init__(self, source: Relation, *, origin=AssertionOrigin.FIXED_STATEMENT,
                 proof_rule=ProofRule.GIVEN):
        self.registry = FakeRegistry(source, origin)
        self.proof_links = (FakeLink("fixed", ProofStep(source, (), proof_rule)),)


def test_public_provider_uses_direct_sum_actual_component(monkeypatch) -> None:
    a, b = component(4, 4, "a"), component(4, 4, "b")
    source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((
        FiniteCyclicGroup(2, a), FiniteCyclicGroup(4, b),
    )))
    monkeypatch.setattr(provider, "exact_prior_database_result", lambda n, k: None)
    expand = provider.build_public_order_zero_provider(
        bridge=FakeBridge(source), proof_target=prior_root(),
    )
    for g, order in ((a, 2), (b, 4)):
        options = expand(sample_goal(g, order))
        assert len(options) == 1
        assert options[0].subgoals == (source,)
        assert options[0].rule.name == RULE_NAME
    assert expand(sample_goal(a, 4)) == ()
    assert expand(sample_goal(component(4, 4, "unrelated"), 2)) == ()


def test_public_provider_prior_conclusions_have_same_general_semantics(monkeypatch) -> None:
    a = component(4, 4)
    source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((
        FreeCyclicGroup(component(4, 4, "free")),
        FiniteCyclicGroup(6, a),
    )))
    monkeypatch.setattr(provider, "exact_prior_database_result", lambda n, k: None)
    expand = provider.build_public_order_zero_provider(
        bridge=object(), proof_target=prior_root(), prior_conclusions=(source,),
    )
    proposals = expand(sample_goal(a, 6))
    assert len(proposals) == 1 and proposals[0].subgoals == (source,)


def test_public_provider_db_only_never_returns_a_proof_step(monkeypatch) -> None:
    a = component(7)
    source = Relation(TodaPrimaryGroup(8, 7), FiniteCyclicGroup(2, a))
    monkeypatch.setattr(provider, "exact_prior_database_result", lambda n, k: source)
    expand = provider.build_public_order_zero_provider(
        bridge=object(), proof_target=prior_root(),
    )
    options = expand(sample_goal(a, 2))
    assert len(options) == 1
    assert options[0].subgoals == (source,)
    assert options[0].rule.premise_patterns[0].statement_pattern == source
    assert options[0].rule.premise_patterns[0].proof_rule is None


def test_unverified_or_unordered_source_is_not_proposed(monkeypatch) -> None:
    a = component(4, 4)
    source = Relation(TodaPrimaryGroup(8, 4), FiniteCyclicGroup(2, a))
    monkeypatch.setattr(provider, "exact_prior_database_result", lambda n, k: None)
    for bridge in (FakeBridge(source, origin=object()),
                   FakeBridge(source, proof_rule=ProofRule.RELATION)):
        expand = provider.build_public_order_zero_provider(
            bridge=bridge, proof_target=prior_root(),
        )
        assert expand(sample_goal(a, 2)) == ()
    earlier_root = Relation(TodaPrimaryGroup(7, 3), FiniteCyclicGroup(2, component(3, 4)))
    expand = provider.build_public_order_zero_provider(
        bridge=FakeBridge(source), proof_target=earlier_root,
    )
    assert expand(sample_goal(a, 2)) == ()


def test_wrong_root_goal_and_wrong_goal_type_are_inert(monkeypatch) -> None:
    a = component(7)
    source = Relation(TodaPrimaryGroup(8, 7), FiniteCyclicGroup(2, a))
    monkeypatch.setattr(provider, "exact_prior_database_result", lambda n, k: source)
    for root in (None, "pi_9^5", Relation(Multiple(2, a), Zero())):
        assert provider.build_public_order_zero_provider(
            bridge=object(), proof_target=root,
        )(sample_goal(a, 2)) == ()
    expand = provider.build_public_order_zero_provider(
        bridge=object(), proof_target=prior_root(),
    )
    assert expand(Relation(Multiple(2, a), a)) == ()
    assert expand(Relation(Multiple(2, a), Zero(), RelationType.ORDER)) == ()


def test_candidate_mismatch_not_sufficient(monkeypatch) -> None:
    a = component(4, 4)
    bad = Relation(TodaPrimaryGroup(8, 4), FiniteCyclicGroup(4, a))
    monkeypatch.setattr(provider, "exact_prior_database_result", lambda n, k: bad)
    expand = provider.build_public_order_zero_provider(
        bridge=object(), proof_target=prior_root(),
    )
    assert expand(sample_goal(a, 2)) == ()


def test_duplicate_concrete_sources_are_deduplicated(monkeypatch) -> None:
    a = component(4, 4)
    source = Relation(TodaPrimaryGroup(8, 4), FiniteCyclicGroup(2, a))
    monkeypatch.setattr(provider, "exact_prior_database_result", lambda n, k: source)
    expand = provider.build_public_order_zero_provider(
        bridge=FakeBridge(source), proof_target=prior_root(),
        prior_conclusions=(source,),
    )
    assert len(expand(sample_goal(a, 2))) == 1


def test_empty_prior_conclusions_is_tuple_only() -> None:
    with pytest.raises(TypeError, match="must be a tuple"):
        provider.build_public_order_zero_provider(
            bridge=object(), proof_target=prior_root(), prior_conclusions=[],
        )
```

## インストール テスト（全 import・関数全文）

`tests/test_installer.py`

```python
"""Pinned whole-function installation contracts."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase175_r4r5r3_public_order_zero import installer


SOURCE = '''from collections import namedtuple


def shared_expansion_provider(bridge, prior_conclusions=()):
    value = (1,)
    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be a tuple")
    return value


def unaffected():
    return "unchanged"
'''


def test_whole_function_replacement_is_exact_and_has_no_other_changes() -> None:
    changed, whole = installer.function_replacement(SOURCE)
    assert changed.count("build_public_order_zero_provider") == 2
    assert "return value" in whole
    assert ast.parse(changed)
    assert changed.split("\ndef unaffected()", 1)[1] == SOURCE.split("\ndef unaffected()", 1)[1]
    assert changed[:changed.index("def shared_expansion_provider")] == SOURCE[:SOURCE.index("def shared_expansion_provider")]
    assert installer.INSERTION.strip() in whole


@pytest.mark.parametrize("invalid", [
    SOURCE.replace("if not isinstance(prior_conclusions, tuple):", "if prior_conclusions is None:"),
    SOURCE.replace("def shared_expansion_provider", "def another_provider"),
    SOURCE + SOURCE,
])
def test_fail_closed_for_changed_function_or_duplicate(invalid: str) -> None:
    with pytest.raises(RuntimeError):
        installer.function_replacement(invalid)


def test_source_pin_guard_rejects_modified_original(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / installer.TARGET_RELATIVE
    path.write_text(SOURCE, encoding="utf-8")
    monkeypatch.setattr(installer, "git_blob", lambda root, ref: "unreviewed")
    with pytest.raises(RuntimeError, match="PRODUCTION_SOURCE_BLOB_CHANGED"):
        installer.plan(tmp_path)


def test_plan_never_fabricates_a_goal() -> None:
    assert "eta_7" not in installer.INSERTION
    assert "pi_9^5" not in installer.INSERTION
    assert "GIVEN" not in installer.INSERTION


def test_full_install_replaces_only_function_in_temporary_git_repo(
    tmp_path: Path, monkeypatch,
) -> None:
    import subprocess

    target = tmp_path / installer.TARGET_RELATIVE
    target.write_text(SOURCE, encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", installer.TARGET_RELATIVE.as_posix()],
                   cwd=tmp_path, check=True)
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.com",
                    "commit", "-qm", "synthetic fixture"], cwd=tmp_path, check=True)
    synthetic_blob = installer.git_blob(
        tmp_path, "HEAD:" + installer.TARGET_RELATIVE.as_posix(),
    )
    monkeypatch.setattr(installer, "PINNED_GIT_BLOB", synthetic_blob)
    output = tmp_path / "audit-output"
    dry = installer.install(tmp_path, dry_run=True, output=output)
    assert target.read_text(encoding="utf-8") == SOURCE
    assert Path(dry["full_replacement_path"]).is_file()
    installed = installer.install(tmp_path, dry_run=False, output=output)
    assert installed["dry_run"] is False
    changed = target.read_text(encoding="utf-8")
    assert "build_public_order_zero_provider" in changed
    assert changed.split("def unaffected():", 1)[1] == SOURCE.split("def unaffected():", 1)[1]
    assert "build_public_order_zero_provider" in Path(
        installed["full_replacement_path"],
    ).read_text(encoding="utf-8")
```

## 実環境テスト（全 import・関数全文）

`tests/test_real_integration.py`

```python
"""Real-repository integration, intentionally no prior-proof replay.

Runs only in the real repository, never in the mock-only authoring runner.
"""
from __future__ import annotations

import pytest

from expression import Multiple, Zero
from homotopy_groups import DirectSumGroup
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step, exact_prior_database_result, verified_db_step,
)
from phase175_r4r5_eta7_annihilator_isolated.rule import RULE_NAME
from phase175_r4r5r3_public_order_zero.provider import build_public_order_zero_provider
from proof import (
    ProofRule, Relation, RelationType, apply_inference_match,
    find_inference_matches_for_rule,
)


def test_real_ordered_db_prior_generator_and_both_summands_public_proposals() -> None:
    root = exact_prior_database_result(5, 4)
    eta = exact_prior_database_result(7, 1)
    direct = exact_prior_database_result(4, 4)
    assert isinstance(root, Relation)
    assert isinstance(eta, Relation)
    assert isinstance(direct, Relation)
    assert isinstance(direct.rhs, DirectSumGroup)
    sources = [eta] + [direct for _ in direct.rhs.summands]
    generators = [(eta.rhs.order, eta.rhs.generator)] + [
        (part.order, part.generator) for part in direct.rhs.summands
    ]
    for source, (m, generator) in zip(sources, generators):
        prior = admitted_db_step(source, proof_target=root)
        assert prior is not None and verified_db_step(prior, proof_target=root)
        goal = Relation(Multiple(m, generator), Zero(), RelationType.EQUALITY)
        proposals = build_public_order_zero_provider(
            bridge=object(), proof_target=root,
        )(goal)
        assert len(proposals) == 1
        assert proposals[0].rule.name == RULE_NAME
        assert proposals[0].subgoals == (source,)
        match = find_inference_matches_for_rule(proposals[0].rule, (prior,))
        assert len(match) == 1
        inferred = apply_inference_match(match[0])
        assert inferred.rule is ProofRule.INFERENCE
        assert inferred.conclusion == goal
        assert inferred.premises == (prior,)


def test_real_shared_expansion_provider_has_installed_general_rule() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase175_r4r5r3_public_order_zero.installer import INSERTION
    import inspect

    assert "build_public_order_zero_provider" in inspect.getsource(shared_expansion_provider)
    root = exact_prior_database_result(5, 4)
    eta = exact_prior_database_result(7, 1)
    assert root is not None and eta is not None
    goal = Relation(Multiple(2, eta.rhs.generator), Zero())
    bridge = build_shared_typed_bridge()
    providers = shared_expansion_provider(bridge, proof_target=root)
    options = providers(goal)
    relevant = [o for o in options if o.rule.name == RULE_NAME]
    assert len(relevant) >= 1
    assert all(o.subgoals == (eta,) for o in relevant)
```



## R4R5R3R1 追補 — HEAD 履歴修正

変更ファイル：`phase175_r4r5r3_public_order_zero/audit.py`（新規 `reviewed_head_lineage` は `source_guard` 直前に配置、変更 `source_guard` 全体）、`run.ps1` 全体、`tests/test_head_lineage.py` 新規、README/監査計画/テスト記録全文を ZIP に収録。クラス変更なし。既存の数学規則・共有関数の変更内容は R4R5R3 と同一。

変更後 `audit.py` の import 全文：

```python
"""Phase 175 R4R5R3: source-guarded general public order-zero wiring.

One shared backward provider is added; previous isolated R4R5R2 results
are revalidated as audit provenance and NEVER inserted as proof certificates.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback

from phase175_r4r5r3_public_order_zero import installer
```

変更・追加関数全文：

```python
def reviewed_head_lineage(root: Path) -> dict[str, object]:
    """Accept the reviewed HEAD or descendants changing only the R4R5R2 package.

    The source is still independently guarded by its committed Git blob, and
    the prior inference rule by its byte-level SHA256. Other committed changes
    must receive a separate source review; no arbitrary later HEAD is trusted.
    """
    import subprocess

    current = installer.git_blob(root, "HEAD")
    if current == EXPECTED_HEAD:
        return {"current_head": current, "intervening_paths": []}
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", EXPECTED_HEAD, current],
        cwd=root, text=True, capture_output=True,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("R4R5R3_UNREVIEWED_HEAD")
    changed = subprocess.run(
        ["git", "diff", "--name-only", EXPECTED_HEAD, current],
        cwd=root, text=True, capture_output=True, check=True,
    ).stdout.splitlines()
    paths = sorted(set(name.strip() for name in changed if name.strip()))
    prefix = PRIOR_PACKAGE + "/"
    if any(not name.startswith(prefix) or name == prefix for name in paths):
        raise RuntimeError("R4R5R3_UNREVIEWED_HEAD_CHANGES")
    return {"current_head": current, "intervening_paths": paths}

def source_guard(root: Path) -> dict[str, object]:
    lineage = reviewed_head_lineage(root)
    path = root / PRIOR_PACKAGE / "rule.py"
    if not path.is_file():
        raise RuntimeError("R4R5R3_R4R5R2_RULE_MISSING")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != PRIOR_RULE_SHA256:
        raise RuntimeError("R4R5R3_R4R5R2_RULE_DRIFT")
    return {
        "reviewed_head": str(lineage["current_head"]),
        "reviewed_base_head": EXPECTED_HEAD,
        "reviewed_intervening_paths": list(lineage["intervening_paths"]),
        "production_blob": installer.PINNED_GIT_BLOB,
        "isolated_rule_sha256": actual,
    }
```

追加テストの import・関数全文：

```python
"""R4R5R3R1: only reviewed R4R5R2 lineage may advance the pinned HEAD."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

import pytest

from phase175_r4r5r3_public_order_zero import audit


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=True,
    ).stdout.strip()


def commit(root: Path, message: str) -> None:
    git(root, "add", ".")
    git(root, "-c", "user.name=Test", "-c", "user.email=test@example.com",
        "commit", "-qm", message)


def prepared_repository(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, str]:
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    (root / "baseline.txt").write_text("reviewed baseline\n", encoding="utf-8")
    commit(root, "reviewed source")
    old_head = git(root, "rev-parse", "HEAD")
    monkeypatch.setattr(audit, "EXPECTED_HEAD", old_head)
    return root, old_head


def reviewed_rule(root: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = root / audit.PRIOR_PACKAGE / "rule.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = b"original reviewed general rule\n"
    path.write_bytes(payload)
    monkeypatch.setattr(audit, "PRIOR_RULE_SHA256", hashlib.sha256(payload).hexdigest())
    return path


def test_exact_reviewed_head_does_not_require_new_commit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, old_head = prepared_repository(tmp_path, monkeypatch)
    assert audit.reviewed_head_lineage(root) == {
        "current_head": old_head, "intervening_paths": [],
    }


def test_reviewed_r4r5r2_commit_is_accepted_and_recorded(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, old_head = prepared_repository(tmp_path, monkeypatch)
    rule = reviewed_rule(root, monkeypatch)
    (rule.parent / "README.md").write_text("audit\n", encoding="utf-8")
    commit(root, "175-4-5")
    current = git(root, "rev-parse", "HEAD")
    assert current != old_head
    result = audit.source_guard(root)
    assert result["reviewed_head"] == current
    assert result["reviewed_base_head"] == old_head
    assert result["reviewed_intervening_paths"] == [
        audit.PRIOR_PACKAGE + "/README.md", audit.PRIOR_PACKAGE + "/rule.py",
    ]


@pytest.mark.parametrize("stray", [
    "phase165_r52_r9_shared_math.py",
    "phase175_r4r5_eta7_annihilator_isolated_fake/rule.py",
    "other/README.md",
])
def test_unrelated_committed_change_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, stray: str,
) -> None:
    root, _ = prepared_repository(tmp_path, monkeypatch)
    reviewed_rule(root, monkeypatch)
    path = root / stray
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("changed\n", encoding="utf-8")
    commit(root, "unauthorized unrelated edit")
    with pytest.raises(RuntimeError, match="R4R5R3_UNREVIEWED_HEAD_CHANGES"):
        audit.source_guard(root)


def test_unrelated_non_descendant_head_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, old_head = prepared_repository(tmp_path, monkeypatch)
    rule = reviewed_rule(root, monkeypatch)
    commit(root, "new reviewed package")
    monkeypatch.setattr(audit, "EXPECTED_HEAD", "0" * 40)
    with pytest.raises(RuntimeError, match="R4R5R3_UNREVIEWED_HEAD"):
        audit.source_guard(root)
    assert old_head != "0" * 40


def test_reviewed_package_rule_byte_drift_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, _ = prepared_repository(tmp_path, monkeypatch)
    rule = reviewed_rule(root, monkeypatch)
    commit(root, "reviewed package")
    rule.write_bytes(b"tampered rule\n")
    with pytest.raises(RuntimeError, match="R4R5R3_R4R5R2_RULE_DRIFT"):
        audit.source_guard(root)


def test_inherited_reviewed_commit_does_not_waive_production_blob_pin() -> None:
    from phase175_r4r5r3_public_order_zero import installer
    assert installer.TARGET_RELATIVE.as_posix() == "phase165_r52_r9_shared_math.py"
    assert len(installer.PINNED_GIT_BLOB) == 40
    assert "R4R5R3_PRODUCTION_SOURCE_BLOB_CHANGED" in (
        installer.plan.__code__.co_consts
    )

```

変更後 `run.ps1` 全文：

```powershell
param(
    [switch] $DryRun,
    [string] $R4R5R2Report = ""
)
$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$target = Join-Path $root 'phase165_r52_r9_shared_math.py'
$original = $null
Push-Location $root
try {
    $tests = @(
        'phase175_r4r5r3_public_order_zero/tests/test_provider.py',
        'phase175_r4r5r3_public_order_zero/tests/test_installer.py',
        'phase175_r4r5r3_public_order_zero/tests/test_head_lineage.py',
        'phase175_r4r5_eta7_annihilator_isolated/tests/test_rule.py',
        'phase175_r4r5_eta7_annihilator_isolated/tests/test_audit.py',
        'phase175_r4r4_pi95_premise_frontier/tests/test_audit.py',
        'phase175_r4r3_two_summand_quotient/tests/test_rule.py',
        'phase175_r4r3_two_summand_quotient/tests/test_audit.py',
        'phase175_r4_pi95_audit/tests/test_audit.py'
    )
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib @tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R5R3 focused baseline pytest failed' }
    Write-Output 'PHASE175_R4R5R3_FOCUSED_BASELINE_PYTEST=PASS'

    if (-not $DryRun) {
        $original = [System.IO.File]::ReadAllBytes($target)
    }
    $command = @('-B', '-m', 'phase175_r4r5r3_public_order_zero.audit', '--root', $root)
    if ($DryRun) { $command += '--dry-run' }
    if ($R4R5R2Report -ne '') { $command += @('--r4r5r2-report', $R4R5R2Report) }
    & python @command
    if ($LASTEXITCODE -ne 0) { throw 'R4R5R3 source guard or public wiring failed' }

    if (-not $DryRun) {
        Write-Output 'PHASE175_R4R5R3_PRODUCTION_PATCH=APPLIED'
    }
    Write-Output 'PHASE175_R4R5R3_EXIT_CODE=0'
    exit 0
} catch {
    if ($null -ne $original) {
        [System.IO.File]::WriteAllBytes($target, $original)
        Write-Output 'PHASE175_R4R5R3_PRODUCTION_PATCH=ROLLED_BACK'
    }
    Write-Output ('PHASE175_R4R5R3_ERROR=' + $_.Exception.Message)
    Write-Output 'PHASE175_R4R5R3_EXIT_CODE=1'
    exit 1
} finally {
    Pop-Location
}

```

作成環境での新規・既存模擬依存テストは90件 PASS。実環境での結果は未確認。

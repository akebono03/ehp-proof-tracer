# Phase 173 R4-R15R7: Source code and complete tests

The complete imports, functions, class definitions, tests and PowerShell runner are reproduced below. All files are new and are added under `phase173_r4_r15r7_source_first_abstract_certificate/` at the repository root; there are no existing-file changes.

## `__init__.py`

```python
"""Phase 173 R4-R15R7: source-first abstract certificate without Web promotion."""
```

## `source.py`

```python
"""Build a source-screened n=4 context for an abstract Toda 4.4 consequence.

The registered target is used solely to choose and validate earlier database
priors. It is never inserted as a source or inferred named-group conclusion.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step
from phase173_r4_r10_general_toda56_core.core import checked_abstract_inputs
from phase173_r4_r1_lemma54_source_bridge.source import (
    ADOPTED_ASSERTION_ID,
    TodaLemma54TypedSource,
    _validated_archive,
)
from proof import ProofRule
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    UnifiedStatementRegistry,
)


def screened_abstract_context(
    bridge: RegistryBridgeResult, *, proof_target: object, chapter: str,
) -> RegistryBridgeResult | None:
    """Reuse the exact original Lemma 5.4 archive and source-first screening.

    A directly cited predecessor is removed ONLY if its separately admitted
    database counterpart can be verified. This avoids a direct literature leaf
    taking the place of the required adopted-DB hypothesis.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("A typed source registry is required")
    inputs = checked_abstract_inputs(proof_target)
    if inputs is None or ADOPTED_ASSERTION_ID in bridge.registry._assertions:
        return None
    archive = _validated_archive(bridge, chapter)
    reference = bridge.registry.reference(archive.reference_id)
    if (type(reference.publication_position) is not int
            or reference.publication_position < 1):
        return None

    registry = UnifiedStatementRegistry()
    for item in bridge.registry._references.values():
        registry.add_reference(item)
    for item in bridge.registry._assertions.values():
        registry.add_assertion(item)
    registry.add_assertion(AssertionEntry(
        assertion_id=ADOPTED_ASSERTION_ID,
        reference_id=archive.reference_id,
        kind=AssertionKind.STATEMENT,
        content=TodaLemma54TypedSource(),
        origin=AssertionOrigin.FIXED_STATEMENT,
        component_position=archive.component_position,
        scope=("source-first: independently registered Lemma 5.4",),
    ))
    augmented = RegistryBridgeResult(registry, bridge.records, bridge.proof_links)
    screened = screen_independent_sources_for_derived_goal(
        augmented, goal=proof_target,
    )
    for prior in inputs:
        matches = tuple(
            link for link in screened.proof_links
            if link.step is not None and link.step.conclusion == prior
        )
        if len(matches) > 1:
            return None
        if matches:
            if admitted_db_step(prior, proof_target=proof_target, bridge=screened) is None:
                return None
            link = matches[0]
            assertion = screened.registry.assertion(link.assertion_id)
            if (link.step.rule is not ProofRule.GIVEN
                    or link.step.premises
                    or assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                    or assertion.content != prior):
                return None
            screened = RegistryBridgeResult(
                screened.registry, screened.records,
                tuple(item for item in screened.proof_links
                      if item.assertion_id != link.assertion_id),
            )

    theorem = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    for expected in (theorem, lemma):
        links = tuple(
            item for item in screened.proof_links
            if item.step is not None
            and type(item.step.conclusion) is type(expected)
            and item.step.conclusion == expected
            and item.step.rule is ProofRule.GIVEN
            and not item.step.premises
            and screened.registry.assertion(item.assertion_id).origin
            is AssertionOrigin.FIXED_STATEMENT
        )
        if len(links) != 1:
            return None
    if any(
        item.step is not None
        and (item.step.conclusion == proof_target
             or item.step.conclusion in inputs)
        for item in screened.proof_links
    ):
        return None
    return screened
```

## `search.py`

```python
"""Reconstruct a source-first abstract certificate using existing proof checks.

This is a separate abstract certificate, not a COMPLETE result for the named
registered group and not a new alternative to the canonical Web query API.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step,
    exact_prior_database_result,
    verified_db_step,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
    expand_cited_lemma54_hopf,
)
from phase173_r4_r10_general_toda56_core.core import (
    checked_abstract_inputs,
    checked_general_inputs,
)
from phase173_r4_r15r6_abstract_toda44_rule.abstract_rule import (
    TodaProp44AbstractGroupResult,
    canonical_abstract_result,
    expand_abstract_toda44,
)
from phase173_r4_r15r7_source_first_abstract_certificate.source import (
    screened_abstract_context,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin


@dataclass(frozen=True)
class AbstractSearchCertificate:
    """One verified abstract inference, explicitly separate from named proof."""

    proof_target: object
    conclusion: TodaProp44AbstractGroupResult
    root_step: ProofStep
    source_context: RegistryBridgeResult
    named_generator_shape_matched: bool

    @property
    def public_group_complete(self) -> bool:
        """This certificate never establishes the registered named group."""
        return False


def _screened_given_conclusions(screened: RegistryBridgeResult) -> tuple[object, ...]:
    """Obtain only exact fixed claims from screened proof links."""
    return tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and not link.step.premises
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
        and link.step.conclusion
        == screened.registry.assertion(link.assertion_id).content
    )


def search_source_first_abstract(
    *, k: int, bridge: RegistryBridgeResult | None = None,
) -> AbstractSearchCertificate | None:
    """Derive one checked abstract root for any eligible k; never name its basis.

    The common registered backward solver resolves only original literature
    source and Hopf subgoals. Two DB hypotheses are separately admitted and
    rechecked by the existing R10E4 API. The standard inference matcher then
    reconstructs the Proposition 4.4 root from those four proven steps.
    """
    if type(k) is not int or k < 3:
        return None
    target = exact_prior_database_result(4, k)
    conclusion = canonical_abstract_result(target)
    if conclusion is None:
        return None
    inputs = checked_abstract_inputs(target)
    if inputs is None:
        return None
    if bridge is None:
        bridge = build_shared_typed_bridge()
    root = Path(__file__).resolve().parents[1]
    chapter = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(
        encoding="utf-8-sig",
    )
    screened = screened_abstract_context(
        bridge, proof_target=target, chapter=chapter,
    )
    if screened is None:
        return None
    available = _screened_given_conclusions(screened)
    theorem = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    if available.count(theorem) != 1 or available.count(lemma) != 1:
        return None

    def source_provider(goal: object):
        return expand_cited_lemma54_hopf(goal, available)

    context_id = next(iter(screened.registry._assertions))
    theorem_step = reconstruct_registered_goal(
        theorem, screened, context_id, source_provider,
        lookup_mode="typed_reference",
    )
    hopf_goal = canonical_hopf_relation()
    hopf_step = reconstruct_registered_goal(
        hopf_goal, screened, context_id, source_provider,
        lookup_mode="typed_reference",
    )
    first_step = admitted_db_step(
        inputs[0], proof_target=target, bridge=screened,
    )
    second_step = admitted_db_step(
        inputs[1], proof_target=target, bridge=screened,
    )
    if (first_step is None or second_step is None
            or not verified_db_step(first_step, proof_target=target, bridge=screened)
            or not verified_db_step(second_step, proof_target=target, bridge=screened)):
        return None
    if (theorem_step.rule is not ProofRule.GIVEN
            or hopf_step.rule is not ProofRule.INFERENCE):
        return None
    proposals = expand_abstract_toda44(
        conclusion, available, proof_target=target, bridge=screened,
    )
    if len(proposals) != 1:
        return None
    proposal = proposals[0]
    if proposal.subgoals != (
        theorem, inputs[0], inputs[1], hopf_goal,
    ):
        return None
    premises = (theorem_step, first_step, second_step, hopf_step)
    matches = tuple(
        match for match in find_inference_matches_for_rule(
            proposal.rule, premises,
        )
        if match.premises == premises
    )
    if len(matches) != 1:
        return None
    root_step = derive_inference_proof_step(matches[0])
    if (root_step.rule is not ProofRule.INFERENCE
            or root_step.conclusion != conclusion
            or root_step.premises != premises
            or not proposal.rule.match_guard(root_step.premises, ())):
        return None
    return AbstractSearchCertificate(
        proof_target=target,
        conclusion=conclusion,
        root_step=root_step,
        source_context=screened,
        named_generator_shape_matched=checked_general_inputs(target) is not None,
    )
```

## `audit.py`

```python
"""Validate source-first abstract certificates, not named-group Web completion."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e4_ordered_db_prior.db_prior import verified_db_step
from phase173_r4_r15r7_source_first_abstract_certificate.search import (
    search_source_first_abstract,
)
from proof import ProofRule


def inspect_k(k: int, bridge: object) -> dict[str, object]:
    """Inspect actual checked root and premise ancestry under one shared bridge."""
    result = search_source_first_abstract(k=k, bridge=bridge)
    if result is None:
        return {
            "k": k,
            "abstract_certified": False,
            "named_generator_shape_matched": False,
            "public_group_complete": False,
            "reason": "SOURCE_FIRST_ABSTRACT_PROOF_UNRESOLVED",
        }
    root = result.root_step
    premises = root.premises
    valid = (
        root.rule is ProofRule.INFERENCE
        and root.conclusion == result.conclusion
        and len(premises) == 4
        and root.inference_rule is not None
        and root.inference_rule.match_guard(premises, ())
        and premises[0].rule is ProofRule.GIVEN
        and verified_db_step(
            premises[1], proof_target=result.proof_target,
            bridge=result.source_context,
        )
        and verified_db_step(
            premises[2], proof_target=result.proof_target,
            bridge=result.source_context,
        )
        and premises[3].rule is ProofRule.INFERENCE
        and len(premises[3].premises) == 1
        and premises[3].premises[0].rule is ProofRule.GIVEN
        and result.public_group_complete is False
    )
    return {
        "k": k,
        "abstract_certified": bool(valid),
        "invariant_summands": [list(x) for x in result.conclusion.invariant_summands],
        "premise_count": len(premises),
        "hopf_inferred": premises[3].rule is ProofRule.INFERENCE,
        "prior_db_reverified": bool(valid),
        "named_generator_shape_matched": result.named_generator_shape_matched,
        "public_group_complete": result.public_group_complete,
        "source_context_links": len(result.source_context.proof_links),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "data" / "sphere.csv").is_file():
        raise RuntimeError("Expected repository root")
    bridge = build_shared_typed_bridge()
    rows = [inspect_k(k, bridge) for k in (4, 7, 8, 31)]
    report = {
        "phase": "173-R4-R15R7",
        "mode": "SOURCE_FIRST_ABSTRACT_CERTIFICATE_SEPARATE_FROM_NAMED_WEB_GROUP",
        "rows": rows,
        "public_route_changed": False,
        "new_given": 0,
        "named_generator_equalities_added": 0,
        "full_pytest_performed": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    for row in rows:
        print(
            "PHASE173_R4_R15R7_K=" + str(row["k"])
            + " ABSTRACT_CERTIFIED=" + str(row["abstract_certified"])
            + " NAMED_SHAPE=" + str(row["named_generator_shape_matched"])
            + " PUBLIC_COMPLETE=" + str(row["public_group_complete"]),
            flush=True,
        )
    k31 = rows[-1]
    passed = (
        all(row["abstract_certified"] for row in rows)
        and k31.get("invariant_summands") == [["finite", 2]] * 8
        and k31["named_generator_shape_matched"] is False
        and k31["public_group_complete"] is False
    )
    print("PHASE173_R4_R15R7_K31_SOURCE_FIRST_ABSTRACT=" + ("PASS" if passed else "FAIL"), flush=True)
    print("PHASE173_R4_R15R7_PUBLIC_COMPLETION=False", flush=True)
    print("PHASE173_R4_R15R7_REPORT=" + str(args.output), flush=True)
    print("PHASE173_R4_R15R7_AUDIT=" + ("PASS" if passed else "FAIL"), flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## `preflight.py`

```python
"""Content-pinned Git/source preflight for the non-invasive R15R7 package."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

REVIEWED_HEAD = "3e3dfecec3c6972a1a2bb19f00372b66314492e2"
REVIEWED_BLOBS = {
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase173_r4_r11_zero_public_connection/source.py": "d18a52b87ca258fdabea46f3523cbd09ace65833",
    "phase165_r52_r9_shared_math.py": "f49b0b7699e29ec1b78d73578dc66a0e33d6e336",
    "phase164_r8_proofstep_factory.py": "d314def19ab4e3e77f57af0ca9da18d7837efdda",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r27_r5_literature.py": "c9bfe2788f4cf043db6dada98a437afea6accf75",
    "phase173_r4_r1_lemma54_source_bridge/source.py": "a37bf7447194d72526522366944778c386c8966c",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase173_r4_r10_general_toda56_core/core.py": "d35600804ecbbc5f8566d52e45a2f6ecf8816347",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase173_r4_r10_general_toda56_core/tests/test_core.py": "68205bf2840688a7b5d7277875c513323be7a5fc",
}
PREVIOUS_R6_HASHES = {
    "phase173_r4_r15r6_abstract_toda44_rule/abstract_rule.py": "fceab3505977b741e0756221b8c7c7abb70339ca75527e55f1924f23f7b54444",
    "phase173_r4_r15r6_abstract_toda44_rule/audit.py": "490044d7d5e5513b3fb46b4c876a36b4ffd36aa7fb6b6f63926641c00d48decd",
    "phase173_r4_r15r6_abstract_toda44_rule/preflight.py": "6d50cc42879bf2178b6ed554aa7207df7f28280e50efbe0f7f361ff796c71041",
}
ALLOWED_PREVIOUS_PREFIX = "phase173_r4_r15r6_abstract_toda44_rule/"
ALLOWED_CACHE = ".pytest_cache/v/cache/nodeids"


def git(root: Path, *args: str) -> str:
    """Run one read-only Git query, refusing failure."""
    result = subprocess.run(
        ("git", *args), cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + result.stderr[:600])
    return result.stdout.strip()


def allowed_committed(path: str) -> bool:
    """Permit only the immediate previous phase package's commit."""
    return path == ALLOWED_CACHE or path.startswith(ALLOWED_PREVIOUS_PREFIX)


def normalized_sha256(path: Path) -> str:
    """Recognize identical text under either Windows or Unix line endings."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def preflight(root: Path) -> None:
    """Require a pristine reviewed math core and same upstream/local HEAD."""
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Expected repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    head = git(root, "rev-parse", "HEAD")
    if git(root, "rev-parse", "origin/develop") != head:
        raise RuntimeError("Local HEAD and GitHub develop differ")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head),
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode:
        raise RuntimeError("Unreviewed HEAD lineage")
    committed = tuple(filter(None, git(
        root, "diff", "--name-only", REVIEWED_HEAD, head,
    ).splitlines()))
    if any(not allowed_committed(path) for path in committed):
        raise RuntimeError("Unreviewed committed source: " + repr(committed))
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    dirty = tuple(filter(None, git(root, "diff", "--name-only").splitlines()))
    if any(path != ALLOWED_CACHE for path in dirty):
        raise RuntimeError("Unreviewed tracked modifications: " + repr(dirty))
    for relative, expected_blob in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + relative) != expected_blob:
            raise RuntimeError("Reviewed Git blob changed: " + relative)
        if git(root, "hash-object", "--", relative) != expected_blob:
            raise RuntimeError("Reviewed worktree content changed: " + relative)
    for relative, expected_hash in PREVIOUS_R6_HASHES.items():
        source = root / relative
        if not source.is_file() or normalized_sha256(source) != expected_hash:
            raise RuntimeError("R15R6 source not reviewed: " + relative)
    print("PHASE173_R4_R15R7_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R7_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R7_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R7_PRODUCTION_EDIT=NONE", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
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
    if ($LASTEXITCODE -ne 0) { throw 'R15R7 Git fetch failed' }

    python -m phase173_r4_r15r7_source_first_abstract_certificate.preflight --root "$Root"
    if ($LASTEXITCODE -ne 0) { throw 'R15R7 source preflight failed' }

    python -m pytest -q phase173_r4_r15r7_source_first_abstract_certificate/tests/test_static.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R7 static tests failed' }

    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R7_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R7_PRODUCTION_EDIT=NONE'
    } else {
        python -m pytest -q `
            phase173_r4_r15r7_source_first_abstract_certificate/tests/test_integration.py `
            phase173_r4_r15r6_abstract_toda44_rule/tests/test_integration.py `
            phase173_r4_r10_general_toda56_core/tests/test_core.py `
            phase173_r4_r11_zero_public_connection/tests/test_route.py
        if ($LASTEXITCODE -ne 0) { throw 'R15R7 focused pytest failed' }
        Write-Output 'PHASE173_R4_R15R7_FOCUSED_PYTEST=PASS'

        python -m phase173_r4_r15r7_source_first_abstract_certificate.audit `
            --root "$Root" `
            --output (Join-Path $PSScriptRoot 'abstract_certificate_report.json')
        if ($LASTEXITCODE -ne 0) { throw 'R15R7 source-first abstract audit failed' }
        Write-Output 'PHASE173_R4_R15R7_PHASE_COMPLETED=False'
    }
} finally {
    Pop-Location
}
```

## `tests/__init__.py`

```python
"""Focused tests for independent abstract source-first proof certificates."""
```

## `tests/test_static.py`

```python
"""Standalone fail-closed/static tests; no live repository source required."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r15r7_source_first_abstract_certificate.preflight import (
    allowed_committed,
    normalized_sha256,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    "filename", ("source.py", "search.py", "audit.py", "preflight.py"),
)
def test_new_source_is_valid_python_without_ellipsis(filename: str) -> None:
    text = (ROOT / filename).read_text(encoding="utf-8")
    tree = ast.parse(text)
    assert not any(
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and node.value.value is Ellipsis
        for node in ast.walk(tree)
    )
    assert "eval(" not in text
    assert "exec(" not in text


def test_only_prior_package_commits_permitted() -> None:
    assert allowed_committed("phase173_r4_r15r6_abstract_toda44_rule/audit.py")
    assert allowed_committed(".pytest_cache/v/cache/nodeids")
    assert not allowed_committed("phase173_r4_r10_general_toda56_core/core.py")
    assert not allowed_committed("phase173_r4_r15r7_source_first_abstract_certificate/search.py")


def test_previous_package_is_content_pinned(tmp_path: Path) -> None:
    path = tmp_path / "source.py"
    path.write_bytes(b"key = 10\n")
    digest = normalized_sha256(path)
    path.write_bytes(b"key = 10\r\n")
    assert normalized_sha256(path) == digest
    path.write_bytes(b"key = 11\r\n")
    assert normalized_sha256(path) != digest


def test_named_web_promotion_is_explicitly_forbidden() -> None:
    text = (ROOT / "search.py").read_text(encoding="utf-8")
    assert "def public_group_complete(self) -> bool:" in text
    assert "return False" in text
    assert "named_generator_shape_matched" in text
    assert "verified_db_step" in text
    assert "reconstruct_registered_goal" in text
    assert "derive_inference_proof_step" in text


def test_runner_only_runs_focused_tests_and_keeps_production_sources() -> None:
    script = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "pytest -q" in script
    assert "phase173_r4_r10_general_toda56_core/tests/test_core.py" in script
    assert "git reset" not in script
    assert "git checkout" not in script
    assert "PHASE173_R4_R15R7_PHASE_COMPLETED=False" in script
```

## `tests/test_integration.py`

```python
"""Source-verified integration contracts for n=4 abstract Toda 4.4 proofs."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e4_ordered_db_prior.db_prior import (
    exact_prior_database_result,
    verified_db_step,
)
from phase173_r4_r10_general_toda56_core.core import checked_general_inputs
from phase173_r4_r15r6_abstract_toda44_rule.abstract_rule import (
    canonical_abstract_result,
)
from phase173_r4_r15r7_source_first_abstract_certificate.search import (
    search_source_first_abstract,
)
from phase173_r4_r15r7_source_first_abstract_certificate.source import (
    screened_abstract_context,
)
from proof import ProofRule


@pytest.fixture(scope="module")
def bridge():
    return build_shared_typed_bridge()


@pytest.mark.parametrize("k", (4, 7, 8, 31))
def test_abstract_root_reconstructed_from_real_sources(bridge, k: int) -> None:
    result = search_source_first_abstract(k=k, bridge=bridge)
    assert result is not None
    assert result.root_step.conclusion == canonical_abstract_result(result.proof_target)
    assert result.root_step.rule is ProofRule.INFERENCE
    assert result.root_step.inference_rule.match_guard(result.root_step.premises, ())
    assert len(result.root_step.premises) == 4
    assert result.root_step.premises[0].rule is ProofRule.GIVEN
    assert result.root_step.premises[3].rule is ProofRule.INFERENCE
    for prior in result.root_step.premises[1:3]:
        assert verified_db_step(
            prior, proof_target=result.proof_target,
            bridge=result.source_context,
        )
    assert result.public_group_complete is False


def test_k31_is_abstract_eight_2_summands_without_named_certificate(bridge) -> None:
    result = search_source_first_abstract(k=31, bridge=bridge)
    assert result is not None
    assert result.conclusion.invariant_summands == (("finite", 2),) * 8
    assert not result.named_generator_shape_matched
    assert checked_general_inputs(result.proof_target) is None
    assert result.public_group_complete is False


def test_k8_original_epsilon_named_goal_still_requires_generator_proof(bridge) -> None:
    result = search_source_first_abstract(k=8, bridge=bridge)
    assert result is not None
    assert not result.named_generator_shape_matched
    assert checked_general_inputs(result.proof_target) is None


def test_forged_target_and_missing_source_fail_closed(bridge) -> None:
    target = exact_prior_database_result(4, 31)
    invalid = replace(target, rhs=exact_prior_database_result(4, 4).rhs)
    source = (Path(__file__).resolve().parents[2] / "sources" / "toda" /
              "Toda_05_2.tex").read_text(encoding="utf-8-sig")
    assert screened_abstract_context(
        bridge, proof_target=invalid, chapter=source,
    ) is None
    with pytest.raises(ValueError):
        screened_abstract_context(
            bridge, proof_target=target, chapter="not the original source",
        )


def test_non_eligible_stems_rejected() -> None:
    for stem in (True, 0, 1, 2, -1, 3.0):
        assert search_source_first_abstract(k=stem) is None
```


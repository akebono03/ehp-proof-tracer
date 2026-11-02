# Phase 173 R4-R1 追加コード全文

既存ソースは変更しない。以下は新規ファイルの全文であり、import と関数・テストの省略はない。

## `source.py`

```python
"""Derive the typed Hopf clause of Toda Lemma 5.4 from its verified source.

This module does not reclassify an archive row or DB goal as a proof. It
introduces one explicit fixed literature assertion only after source-hash,
exact-clause and existing publication-order verification. Its Hopf equality
is concluded by INFERENCE, not adopted directly as a GIVEN.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement, MapApplication
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from proof import (
    InferenceRule,
    LiteratureReference,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)
from map_facts import EHP_H_MAP

SOURCE_ID = "toda:tex:ch5:0007"
ADOPTED_ASSERTION_ID = "phase173:r4r1:lemma54:typed_hopf_source"
HOPF_TEXT = r"H(\nu_{4})=\iota_7"
MEMBERSHIP_TEXT = r"\nu_{4}\in \pi^{4}_{7}"
DOUBLE_TEXT = r"2E \nu_{4}=E^{2}\nu'"


@dataclass(frozen=True)
class TodaLemma54TypedSource:
    """One exact source-verified, cited clause, never a DB group result."""
    source_id: str = SOURCE_ID
    hopf_formula: str = HOPF_TEXT
    membership_formula: str = MEMBERSHIP_TEXT
    double_formula: str = DOUBLE_TEXT


def canonical_hopf_relation() -> Relation:
    """Build the concrete Hopf relation independently of the requested goal."""
    nu4 = HomotopyElement(
        name="ν₄", dimension=4, source=7, target=4,
        generator=GeneratorSymbol(family="ν", index=4),
    )
    iota = HomotopyElement(
        name="ι_7", dimension=7, source=7, target=7,
        generator=GeneratorSymbol(family="ι", index=7),
    )
    return Relation(
        MapApplication(map=EHP_H_MAP, expression=nu4),
        iota,
        RelationType.EQUALITY,
    )


def validate_lemma54_text(text: str) -> None:
    """Require a unique original lemma environment with all three clauses."""
    if not isinstance(text, str):
        raise TypeError("Lemma 5.4 archived text must be a string")
    if text.count(r"\label{lem:5.4}") != 1:
        raise ValueError("Lemma 5.4 archive must contain one lemma label")
    start = text.find(r"\label{lem:5.4}")
    end = text.find(r"\end{lemma}", start)
    if end < 0:
        raise ValueError("Lemma 5.4 environment is incomplete")
    opening = text.rfind(r"\begin{lemma}", 0, start)
    if opening < 0:
        raise ValueError("Lemma 5.4 environment opening is absent")
    passage = text[opening:end]
    if any(token not in passage for token in (HOPF_TEXT, MEMBERSHIP_TEXT, DOUBLE_TEXT)):
        raise ValueError("Lemma 5.4 verified claims differ")


def _validated_archive(bridge: RegistryBridgeResult, chapter: str):
    """Match the archived row and the frozen full TeX text, not a DB goal."""
    validate_lemma54_text(chapter)
    candidates = tuple(
        assertion for assertion in bridge.registry._assertions.values()
        if assertion.origin is AssertionOrigin.SOURCE_ARCHIVE
        and isinstance(assertion.content, dict)
        and assertion.content.get("source_statement_id") == SOURCE_ID
    )
    if len(candidates) != 1:
        raise ValueError("Expected a unique original Lemma 5.4 archive row")
    archive = candidates[0]
    content = archive.content
    source = content.get("source_text")
    if not isinstance(source, str) or not source:
        raise ValueError("Lemma 5.4 archive lacks source text")
    if content.get("source_sha256") != sha256(source.encode("utf-8")).hexdigest():
        raise ValueError("Lemma 5.4 archived SHA-256 does not match text")
    # Archive format may hold a shorter extracted block. It must belong to the
    # exactly checked chapter; never accept merely matching generic tokens.
    normalized = chapter.replace("\r\n", "\n")
    extracted = source.replace("\r\n", "\n")
    if extracted not in normalized:
        raise ValueError("Lemma 5.4 archive is not a literal source passage")
    if not all(token in extracted for token in (HOPF_TEXT, MEMBERSHIP_TEXT, DOUBLE_TEXT)):
        raise ValueError("Lemma 5.4 archive does not contain the complete lemma")
    reference = bridge.registry.reference(archive.reference_id)
    if reference.locator != "Lemma 5.4" or reference.kind is not ReferenceKind.LEMMA:
        raise ValueError("Lemma 5.4 archive has an incorrect reference")
    return archive


def add_verified_lemma54_source(
    bridge: RegistryBridgeResult, *, citing_assertion_id: str, chapter: str,
) -> RegistryBridgeResult:
    """Add one explicitly cited typed literature statement to an isolated bridge.

    Reuse the original referenced publication position, not a fabricated rank.
    No source-archive row itself becomes a GIVEN; the new source statement is
    checked before registration and must precede the actual citing assertion.
    """
    from phase166_r3c_publication_order import precedes_citing_assertion

    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("An existing typed reference bridge is required")
    archive = _validated_archive(bridge, chapter)
    if ADOPTED_ASSERTION_ID in bridge.registry._assertions:
        raise ValueError("Lemma 5.4 typed source already registered")
    registry = UnifiedStatementRegistry()
    for entry in bridge.registry._references.values():
        registry.add_reference(entry)
    for entry in bridge.registry._assertions.values():
        registry.add_assertion(entry)
    registry.add_assertion(AssertionEntry(
        assertion_id=ADOPTED_ASSERTION_ID,
        reference_id=archive.reference_id,
        kind=AssertionKind.STATEMENT,
        content=TodaLemma54TypedSource(),
        origin=AssertionOrigin.FIXED_STATEMENT,
        component_position=archive.component_position,
        scope=("adopted source-verified Lemma 5.4 exact clause",),
    ))
    result = RegistryBridgeResult(registry, bridge.records, bridge.proof_links)
    if not precedes_citing_assertion(result, ADOPTED_ASSERTION_ID, citing_assertion_id):
        raise ValueError("Lemma 5.4 has no proven earlier publication position")
    return result


def lemma54_hopf_inference_rule(goal: Relation) -> InferenceRule:
    """Extract only the uniquely typed Hopf clause as a derived ProofStep."""
    if goal != canonical_hopf_relation():
        raise ValueError("Only the concrete verified Lemma 5.4 Hopf fact is supported")
    claim = TodaLemma54TypedSource()

    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].rule is ProofRule.GIVEN
                and type(premises[0].conclusion) is TodaLemma54TypedSource
                and premises[0].conclusion == claim)

    return InferenceRule(
        name="Toda Lemma 5.4 cited Hopf identity consequence",
        description=(
            "Extract H(nu_4)=iota_7 from the fully source-verified and "
            "publication-screened Toda Lemma 5.4 typed literature statement."
        ),
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=TodaLemma54TypedSource,
            statement_pattern=claim,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Lemma 5.4", locator="Lemma 5.4",
        ),
    )


def expand_cited_lemma54_hopf(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """No source-verified screened claim means no proposal whatsoever."""
    if not isinstance(available, tuple):
        raise TypeError("available must be the screened source tuple")
    if goal != canonical_hopf_relation():
        return ()
    claim = TodaLemma54TypedSource()
    if sum(type(source) is TodaLemma54TypedSource and source == claim
           for source in available) != 1:
        return ()
    return (GoalExpansion(lemma54_hopf_inference_rule(goal), (claim,)),)
```

## `audit.py`

```python
"""Isolated publication-screened proof search for Toda Lemma 5.4 -> (5.6)."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
from typing import Any

REVIEWED_ANCESTOR = "cc1b206f787986dccc659cc9a5982bea3bb05d50"
REVIEWED_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "sources/toda/Toda_04_2.tex": "4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7",
    "phase165_r52_r9_shared_math.py": "2718c55789af7f442ac2c086d016d3d6f7ca3133",
    "phase165_r52_r27_r5_literature.py": "c9bfe2788f4cf043db6dada98a437afea6accf75",
    "phase165_r52_r16_web_citation_gate.py": "d1138c0450f234b6da761902ed7358b6038a19c8",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase169_r3m_prior_result_catalog/prior_results.py": "c522cbaf924b3a9aa500d453b8eb6a1a66c42611",
    "phase166_r3t_goal_source_binding/goal_source.py": "e13a07bbc0b6494b0c3c9b891784fe7378448756",
    "phase173_r4_r1_source_bound_56/rule.py": "e05ada41cbcf53e8b755428afd245ba2da619fa8",
}


def git(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ("git", *arguments), cwd=root,
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    return completed.stdout.strip()


def validate_audit_additions(changes: str) -> tuple[str, ...]:
    """Reject modifications to any committed file after reviewed ancestor."""
    paths = []
    for record in changes.splitlines():
        fields = record.split("\t")
        if len(fields) != 2:
            raise RuntimeError("Unexpected commit status: " + repr(record))
        status, path = fields
        if (status != "A" or not path.startswith("phase173_")
                or "/" not in path or "\\" in path or ".." in Path(path).parts):
            raise RuntimeError("Non-audit committed change: " + repr(record))
        paths.append(path)
    return tuple(paths)


def guard_sources(root: Path) -> dict[str, Any]:
    """Check reviewed production content and require audit-only intervening commits."""
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Only the reviewed develop branch is supported")
    head = git(root, "rev-parse", "HEAD")
    if head != git(root, "rev-parse", "origin/develop"):
        raise RuntimeError("Local develop differs from origin/develop")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_ANCESTOR, head),
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("Unreviewed Git history")
    additions = validate_audit_additions(
        git(root, "diff", "--name-status", "--no-renames", REVIEWED_ANCESTOR, head)
    )
    for path, expected in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("Reviewed blob changed: " + path)
        for arguments in (("diff", "--quiet", "--", path),
                          ("diff", "--cached", "--quiet", "--", path)):
            checked = subprocess.run(("git", *arguments), cwd=root,
                                     capture_output=True, check=False)
            if checked.returncode != 0:
                raise RuntimeError("Reviewed working source changed: " + path)
    return {"head": head, "added_audit_files": list(additions),
            "reviewed_sources": sorted(REVIEWED_BLOBS), "no_git_mutation": True}


def collect_ancestry(root: object) -> tuple[object, ...]:
    """Flatten only real ProofStep ancestry, avoiding repeated shared nodes."""
    from proof import ProofStep
    if not isinstance(root, ProofStep):
        return ()
    visited: set[int] = set()
    sequence: list[ProofStep] = []

    def visit(node: ProofStep) -> None:
        if id(node) in visited:
            return
        visited.add(id(node))
        sequence.append(node)
        for parent in node.premises:
            visit(parent)

    visit(root)
    return tuple(sequence)


def inspect_runtime(root: Path) -> dict[str, Any]:
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, search_shared_group_goal, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3c_publication_order import precedes_citing_assertion
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase173_r4_r1_source_bound_56.rule import expand_source_bound_toda56
    from phase173_r4_r1_lemma54_source_bridge.source import (
        ADOPTED_ASSERTION_ID, TodaLemma54TypedSource,
        add_verified_lemma54_source, canonical_hopf_relation,
        expand_cited_lemma54_hopf,
    )
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    original = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(original, n=4, k=3)
    if len(candidates) != 1:
        raise RuntimeError("pi_7^4 requires exactly one typed target goal")
    goal = candidates[0]
    citing_id = resolve_specialized_goal_citing_id(original, goal)
    if citing_id is None:
        raise RuntimeError("pi_7^4 lacks a unique source publication position")
    chapter = (root / "sources" / "toda" / "Toda_05_2.tex").read_text(
        encoding="utf-8-sig"
    )
    augmented = add_verified_lemma54_source(
        original, citing_assertion_id=citing_id, chapter=chapter,
    )
    if not precedes_citing_assertion(augmented, ADOPTED_ASSERTION_ID, citing_id):
        raise RuntimeError("Lemma 5.4 is not positioned before the goal")
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        augmented, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    ))
    matching_links = tuple(
        link for link in screened.proof_links
        if link.assertion_id == ADOPTED_ASSERTION_ID
        and link.step is not None and link.step.rule is ProofRule.GIVEN
        and type(link.step.conclusion) is TodaLemma54TypedSource
    )
    if len(matching_links) != 1:
        raise RuntimeError("Lemma 5.4 is not uniquely citation-screened")
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )

    def extra(statement: object):
        candidates = expand_cited_lemma54_hopf(statement, available)
        if candidates:
            return candidates
        return expand_source_bound_toda56(
            statement, available, screened, proof_target=goal,
        )

    provider = shared_expansion_provider(
        screened, extra_providers=(extra,), proof_target=goal,
    )
    hopf = canonical_hopf_relation()
    hopf_candidates = provider(hopf)
    goal_candidates = provider(goal)
    result = search_shared_group_goal(
        n=4, k=3, group_structure=goal.rhs,
        bridge=augmented, citing_assertion_id=citing_id,
        expansion_provider=provider,
    )
    status = getattr(result.status, "value", str(result.status))
    final_steps = [
        step for step in result.proven_steps
        if step.conclusion == goal and step.rule is ProofRule.INFERENCE
    ]
    if status == "complete" and (result.conclusion != goal or not final_steps):
        raise RuntimeError("Uncertified completion must not be accepted")
    final = final_steps[-1] if final_steps else None
    ancestry = collect_ancestry(final)
    source_present = any(
        step.rule is ProofRule.GIVEN and type(step.conclusion) is TodaLemma54TypedSource
        for step in ancestry
    )
    hopf_present = any(
        step.rule is ProofRule.INFERENCE and step.conclusion == hopf
        for step in ancestry
    )
    certified = status == "complete" and source_present and hopf_present
    if status == "complete" and not certified:
        raise RuntimeError("Complete result lacks cited Lemma 5.4 Hopf ancestry")
    return {
        "goal": repr(goal), "citing_id": citing_id,
        "citation_screened_lemma54_count": len(matching_links),
        "direct_hopf_given_count": sum(
            type(x) is type(hopf) and x == hopf for x in available
        ),
        "hopf_proposal_names": [x.rule.name for x in hopf_candidates],
        "root_proposal_names": [x.rule.name for x in goal_candidates],
        "status": status, "complete": status == "complete",
        "complete_and_source_certified": certified,
        "source_in_final_proof_ancestry": source_present,
        "hopf_in_final_proof_ancestry": hopf_present,
        "proven_step_count": len(result.proven_steps),
        "open_goals": [repr(x)[:700] for x in result.open_goals[:15]],
        "diagnostics": [str(x)[:700] for x in result.diagnostics[:15]],
        "publication_position_preserved": True,
        "production_changes": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase173 R4-R1 isolated cited Lemma 5.4 proof")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    check = guard_sources(root)
    print("PHASE173_R4_R1_LEMMA54_SOURCE_GUARD=PASS")
    if args.dry_run:
        print("PHASE173_R4_R1_LEMMA54_DRY_RUN=PASS")
        return 0
    result = inspect_runtime(root)
    destination = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / (
        "EHPProofTracerRecovery/phase173_r4_r1_lemma54_source_bridge/audit.json"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps({
        "phase": "173-R4-R1", "scope": "ISOLATED_TYPED_CITED_LEMMA54",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "preflight": check, "runtime": result, "production_changes": [],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("LEMMA54_SCREENED_SOURCE=" + str(result["citation_screened_lemma54_count"]))
    print("LEMMA54_DIRECT_HOPF_GIVEN=" + str(result["direct_hopf_given_count"]))
    print("LEMMA54_HOPF_PROPOSALS=" + repr(result["hopf_proposal_names"]))
    print("TODA56_ROOT_PROPOSALS=" + repr(result["root_proposal_names"]))
    print("PHASE173_R4_R1_PROOF_STATUS=" + str(result["status"]))
    print("PHASE173_R4_R1_COMPLETE=" + str(result["complete"]))
    print("PHASE173_R4_R1_SOURCE_CERTIFIED=" + str(result["complete_and_source_certified"]))
    print("PHASE173_R4_R1_OPEN_GOALS=" + repr(result["open_goals"]))
    print("PHASE173_R4_R1_REPORT=" + str(destination))
    print("PHASE173_R4_R1_NO_PRODUCTION_CHANGES=True")
    print("PHASE173_R4_R1_LEMMA54_AUDIT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = (Resolve-Path (Join-Path $Here '..')).Path
Push-Location $Root
try {
    Write-Output 'PHASE173_R4_R1_LEMMA54_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider '.\phase173_r4_r1_lemma54_source_bridge\tests'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 Lemma54 focused pytest failed' }
    Write-Output 'PHASE173_R4_R1_LEMMA54_FOCUSED_PYTEST=PASS'
    $Arguments = @('-m', 'phase173_r4_r1_lemma54_source_bridge.audit', '--root', $Root)
    if ($DryRun) { $Arguments += '--dry-run' }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 Lemma54 audit failed' }
}
finally {
    Pop-Location
}
```

## `tests/test_source.py`

```python
"""Focused tests for source-gated Toda Lemma 5.4 and inferred Hopf claim."""
from __future__ import annotations

from hashlib import sha256
from types import SimpleNamespace

import pytest

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase173_r4_r1_lemma54_source_bridge.source import (
    ADOPTED_ASSERTION_ID,
    SOURCE_ID,
    TodaLemma54TypedSource,
    add_verified_lemma54_source,
    canonical_hopf_relation,
    expand_cited_lemma54_hopf,
    lemma54_hopf_inference_rule,
    validate_lemma54_text,
)
from proof import ProofRule
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def source_text() -> str:
    return (
        "chapter prefix\n"
        "\\begin{lemma}[]\n\\label{lem:5.4}\n"
        "\\nu_{4}\\in \\pi^{4}_{7}\n"
        "H(\\nu_{4})=\\iota_7,\\qquad 2E \\nu_{4}=E^{2}\\nu' .\n"
        "\\end{lemma}\nchapter suffix\n"
    )


def archive_bridge(*, modified_text: str | None = None,
                   wrong_hash: bool = False,
                   source_position: int | None = 3,
                   goal_position: int | None = 5) -> RegistryBridgeResult:
    text = source_text() if modified_text is None else modified_text
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id="archive:lemma54", kind=ReferenceKind.LEMMA,
        locator="Lemma 5.4", source_id=SOURCE_ID,
        publication_position=source_position,
    ))
    registry.add_reference(LiteratureEntry(
        reference_id="goal:prop56", kind=ReferenceKind.PROPOSITION,
        locator="Proposition 5.6", publication_position=goal_position,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="source:archive", reference_id="archive:lemma54",
        kind=AssertionKind.STATEMENT,
        content={
            "source_statement_id": SOURCE_ID,
            "source_text": text,
            "source_sha256": "bad" if wrong_hash else sha256(text.encode("utf-8")).hexdigest(),
        },
        origin=AssertionOrigin.SOURCE_ARCHIVE,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="target:goal", reference_id="goal:prop56",
        kind=AssertionKind.STATEMENT, content="independent proof goal",
        origin=AssertionOrigin.FIXED_STATEMENT,
    ))
    return RegistryBridgeResult(registry, (), ())


def test_verified_toda_lemma54_text() -> None:
    validate_lemma54_text(source_text())


@pytest.mark.parametrize("missing", [
    r"\label{lem:5.4}", r"\nu_{4}\in \pi^{4}_{7}",
    r"H(\nu_{4})=\iota_7", r"2E \nu_{4}=E^{2}\nu'",
])
def test_missing_source_fragment_is_rejected(missing: str) -> None:
    with pytest.raises(ValueError):
        validate_lemma54_text(source_text().replace(missing, "REMOVED"))


def test_register_source_only_after_exact_hash_and_position() -> None:
    bridge = archive_bridge()
    updated = add_verified_lemma54_source(
        bridge, citing_assertion_id="target:goal", chapter=source_text(),
    )
    assert ADOPTED_ASSERTION_ID not in bridge.registry._assertions
    registered = updated.registry.assertion(ADOPTED_ASSERTION_ID)
    assert registered.origin is AssertionOrigin.FIXED_STATEMENT
    assert registered.content == TodaLemma54TypedSource()
    assert registered.reference_id == "archive:lemma54"
    assert updated.proof_links == ()


def test_modified_archive_hash_is_rejected() -> None:
    with pytest.raises(ValueError, match="SHA-256"):
        add_verified_lemma54_source(
            archive_bridge(wrong_hash=True),
            citing_assertion_id="target:goal", chapter=source_text(),
        )


def test_archive_must_be_literal_chapter_passage() -> None:
    text = source_text().replace("chapter prefix", "different prefix")
    with pytest.raises(ValueError, match="literal source passage"):
        add_verified_lemma54_source(
            archive_bridge(modified_text=text),
            citing_assertion_id="target:goal", chapter=source_text(),
        )


def test_citation_after_target_is_rejected() -> None:
    with pytest.raises(ValueError, match="earlier publication"):
        add_verified_lemma54_source(
            archive_bridge(source_position=9),
            citing_assertion_id="target:goal", chapter=source_text(),
        )


def test_missing_position_is_rejected() -> None:
    with pytest.raises(ValueError, match="earlier publication"):
        add_verified_lemma54_source(
            archive_bridge(source_position=None),
            citing_assertion_id="target:goal", chapter=source_text(),
        )


def test_derived_hopf_requires_one_screened_typed_source() -> None:
    goal = canonical_hopf_relation()
    assert expand_cited_lemma54_hopf(goal, ()) == ()
    source = TodaLemma54TypedSource()
    result = expand_cited_lemma54_hopf(goal, (source,))
    assert len(result) == 1
    assert result[0].subgoals == (source,)
    assert result[0].rule.conclusion_pattern == goal
    assert expand_cited_lemma54_hopf(goal, (source, source)) == ()


def test_inference_refuses_given_hopf_as_inference_source() -> None:
    goal = canonical_hopf_relation()
    rule = lemma54_hopf_inference_rule(goal)
    source = TodaLemma54TypedSource()
    good = SimpleNamespace(conclusion=source, rule=ProofRule.GIVEN)
    wrong = SimpleNamespace(conclusion=source, rule=ProofRule.INFERENCE)
    assert rule.match_guard((good,), {}) is True
    assert rule.match_guard((wrong,), {}) is False


def test_wrong_goal_is_not_inferred() -> None:
    with pytest.raises(ValueError):
        lemma54_hopf_inference_rule(object())
    assert expand_cited_lemma54_hopf(object(), (TodaLemma54TypedSource(),)) == ()
```

## `tests/test_audit.py`

```python
"""Offline checks for source immutability and review scope."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_r4_r1_lemma54_source_bridge.audit import validate_audit_additions


def test_empty_delta_is_allowed() -> None:
    assert validate_audit_additions("") == ()


def test_only_added_phase173_files_are_allowed() -> None:
    assert validate_audit_additions(
        "A\tphase173_r4_r1_subgoal_closure/audit.py\n"
    ) == ("phase173_r4_r1_subgoal_closure/audit.py",)


@pytest.mark.parametrize("record", [
    "M\tphase173_r4_r1_subgoal_closure/audit.py",
    "A\tphase165_r52_r9_shared_math.py",
    "D\tphase173_r4_r1_subgoal_closure/audit.py",
    "A\tphase173_r4_r1_subgoal_closure/../bad.py",
    "R100\tphase173_r4_r1_subgoal_closure/x.py\tphase173_r4_r1_subgoal_closure/y.py",
])
def test_unauthorized_commit_diff_is_rejected(record: str) -> None:
    with pytest.raises(RuntimeError):
        validate_audit_additions(record)


def test_no_production_changes_in_auditor() -> None:
    path = Path(__file__).resolve().parents[1] / "audit.py"
    source = path.read_text(encoding="utf-8")
    assert "git reset" not in source
    assert "os.replace" not in source
    assert "production_changes" in source
```

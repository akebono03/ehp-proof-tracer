# Phase 173 R4-R15R4 — 変更・追加コード全文

対象: 全ファイル新規追加。既存ファイルのクラス・関数・import 変更なし。コード中の省略なし。

## `bridge.py`

```python
"""Compose separately verified suspension images with a source-neutral rule.

Never assume an atomic generator identity from matching database labels.
Every composite proof has two strictly smaller GeneratorImage premises.
"""
from __future__ import annotations

from expression import Composition
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span
from proof import InferenceRule, PremisePattern, ProofRule


COMPOSITION_IMAGE_RULE = "suspension image of composition from verified factor images"


def generator_image(source: object, target: object) -> GeneratorImage | None:
    """Form the unique typed one-suspension GeneratorImage for two expressions."""
    source_span = typed_element_span(source)
    target_span = typed_element_span(target)
    if source_span is None or target_span is None:
        return None
    if target_span != (source_span[0] + 1, source_span[1] + 1):
        return None
    q, n = source_span
    if q < n or n < 2:
        return None
    return GeneratorImage(
        map=TodaSuspensionMap(
            source_group=TodaPrimaryGroup(q, n),
            target_group=TodaPrimaryGroup(q + 1, n + 1),
        ),
        source_generator=source,
        target_generator=target,
    )


def factor_image_goals(goal: object) -> tuple[GeneratorImage, GeneratorImage] | None:
    """Split a typed composite image without deciding either atomic identity."""
    if not isinstance(goal, GeneratorImage):
        return None
    source = goal.source_generator
    target = goal.target_generator
    if not isinstance(source, Composition) or not isinstance(target, Composition):
        return None
    if generator_image(source, target) != goal:
        return None
    left = generator_image(source.left, target.left)
    right = generator_image(source.right, target.right)
    if left is None or right is None:
        return None
    return (left, right)


def expand_composed_generator_image(goal: object) -> tuple[GoalExpansion, ...]:
    """Propose the functorial image with *required* inferred factor premises."""
    factors = factor_image_goals(goal)
    if factors is None:
        return ()

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(p.rule is ProofRule.INFERENCE for p in premises)
            and tuple(p.conclusion for p in premises) == factors
            and factor_image_goals(goal) == factors
        )

    rule = InferenceRule(
        name=COMPOSITION_IMAGE_RULE,
        description=(
            "The suspension of a typed composition is the composition "
            "of the separately proved factor images. No unproved named "
            "generator identity is inferred from group or order metadata."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=GeneratorImage,
                statement_pattern=factors[0],
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=GeneratorImage,
                statement_pattern=factors[1],
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )
    return (GoalExpansion(rule, factors),)
```

## `replay.py`

```python
"""Replay a source-backed composite image in the existing proof engine.

Only actual cited Chapter V stable-family GIVEN steps are allowed as leaves.
The R15R3 canonical formal image inference is a separate, premise-free
inference; the proof construction adds no new GIVEN or direct DB leaf.
"""
from __future__ import annotations

from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10e8_hyoujigen_generic_suspension.chapter_vi_reference import (
    build_cited_chapter_vi_family_definitions,
)
from phase169_r10d2_general_family_definition.family_citation import (
    build_cited_stable_family_definitions,
    expand_cited_stable_family,
)
from phase173_r4_r15r3_formal_suspension_bridge.bridge import (
    expand_canonical_formal_image,
)
from phase173_r4_r15r4_cited_composition_image.bridge import (
    expand_composed_generator_image,
    generator_image,
)
from proof import (
    ProofRule,
    ProofStep,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from unified_statement_registry import AssertionOrigin


def cited_source_steps() -> tuple[ProofStep, ...]:
    """Fetch the existing Chapter V source-verified GIVENs, not CSV assertions."""
    result: list[ProofStep] = []
    for cited in (
        build_cited_stable_family_definitions(),
        build_cited_chapter_vi_family_definitions(),
    ):
        for link in cited.proof_links:
            assertion = cited.registry.assertion(link.assertion_id)
            step = link.step
            if (
                assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and step is not None
                and step.rule is ProofRule.GIVEN
                and step.conclusion == assertion.content
                and not step.premises
            ):
                result.append(step)
    return tuple(result)


def replay_cited_image(goal: object, sources: tuple[ProofStep, ...]) -> ProofStep | None:
    """Derive an image only if every leaf and inference matches an existing rule.

    Return None on missing cited definitions or missing atomic image rules.
    Does not modify the public expansion registry or Web proof results.
    """
    if not isinstance(goal, GeneratorImage) or not isinstance(sources, tuple):
        return None
    if any(step.rule is not ProofRule.GIVEN or step.premises for step in sources):
        return None
    available = tuple(step.conclusion for step in sources)
    if len(set(available)) != len(available):
        return None
    memo: dict[object, ProofStep | None] = {}
    in_progress: set[object] = set()

    def prove(statement: object) -> ProofStep | None:
        if statement in memo:
            return memo[statement]
        if statement in in_progress:
            return None
        for original in sources:
            if statement == original.conclusion and type(statement) is type(original.conclusion):
                memo[statement] = original
                return original
        in_progress.add(statement)
        proposals = (
            expand_canonical_formal_image(statement)
            + expand_cited_stable_family(statement, available)
            + expand_composed_generator_image(statement)
        )
        valid: list[ProofStep] = []
        for proposal in proposals:
            premises = tuple(prove(subgoal) for subgoal in proposal.subgoals)
            if any(premise is None for premise in premises):
                continue
            for match in find_inference_matches_for_rule(proposal.rule, premises):
                candidate = apply_inference_match(match)
                if (
                    candidate.rule is ProofRule.INFERENCE
                    and candidate.conclusion == statement
                    and candidate.premises == premises
                ):
                    valid.append(candidate)
        in_progress.remove(statement)
        # First Successful Proof Search: the first independently replayable
        # derivation is enough. No unnecessary uniqueness requirement.
        result = valid[0] if valid else None
        memo[statement] = result
        return result

    return prove(goal)


def replay_named_image(
    source: object, target: object, sources: tuple[ProofStep, ...]
) -> ProofStep | None:
    """Prove E(source)=target only through checked independent atom images."""
    goal = generator_image(source, target)
    return replay_cited_image(goal, sources) if goal is not None else None


def proof_tree_steps(root: ProofStep) -> tuple[ProofStep, ...]:
    """Traverse the proof premises in postorder without claiming completeness."""
    result: list[ProofStep] = []
    visited: set[int] = set()

    def visit(step: ProofStep) -> None:
        if id(step) in visited:
            return
        visited.add(id(step))
        for premise in step.premises:
            visit(premise)
        result.append(step)

    visit(root)
    return tuple(result)
```

## `audit.py`

```python
"""Audit source-cited named images without modifying the public proof tree."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from expression import Composition, IteratedSuspension
from phase169_r10b_registered_stable_family_binding.family_registry import (
    registered_stable_family_pair,
)
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r4_typed_generator_audit.audit import _group_components
from phase173_r4_r15r2_generator_obligation_audit.audit import inspect_k as previous_inspect_k
from phase173_r4_r15r4_cited_composition_image.replay import (
    cited_source_steps,
    proof_tree_steps,
    replay_named_image,
)
from proof import ProofRule


def expression_atoms(expression: object) -> tuple[object, ...]:
    """Flatten a structurally typed composition; never conflate generator IDs."""
    if isinstance(expression, Composition):
        return expression_atoms(expression.left) + expression_atoms(expression.right)
    return (expression,)


def atom_evidence(
    source: object, target: object, cited_family_ids: frozenset[int],
) -> dict[str, object]:
    """Distinguish cited family identities, formal suspension and missing source."""
    from phase173_r4_r15r4_cited_composition_image.bridge import generator_image

    goal = generator_image(source, target)
    row: dict[str, object] = {
        "source": str(source),
        "target": str(target),
        "well_typed": goal is not None,
        "status": "UNSUPPORTED_ATOMIC_IMAGE",
        "family_id": None,
    }
    if goal is None:
        row["status"] = "INCORRECT_ATOMIC_IMAGE_TYPING"
        return row
    if isinstance(target, IteratedSuspension) and target.exponent == 1 and target.expression == source:
        row["status"] = "CANONICAL_FORMAL_IMAGE"
        return row
    family = registered_stable_family_pair(source, target)
    if family is None:
        return row
    row["family_id"] = family.family_id
    row["status"] = (
        "CITED_FAMILY_IMAGE_PROPOSAL"
        if family.family_id in cited_family_ids
        else "FAMILY_ID_KNOWN_BUT_SOURCE_NOT_CITED"
    )
    return row


def inspect_k(k: int) -> dict[str, object]:
    """Replay every plausible named image from all existing earlier DB factors."""
    base = previous_inspect_k(k)
    target = exact_prior_database_result(4, k)
    left = exact_prior_database_result(3, k)
    if not base.get("abstract_compatible") or target is None or left is None:
        return {
            "k": k, "status": "ABSTRACT_PREMISES_UNAVAILABLE", "candidate_pairs": [],
            "proved_named_images": 0, "public_completion": False,
        }
    source_steps = cited_source_steps()
    cited_ids = frozenset(
        step.conclusion.family_id
        for step in source_steps
        if isinstance(step.conclusion, CitedStableFamilyDefinition)
    )
    sources = _group_components(left)
    targets = _group_components(target)
    if sources is None or targets is None:
        raise RuntimeError("Reviewed abstract premises are not typed cyclic groups")
    candidates: list[dict[str, object]] = []
    certified_pairs: list[tuple[int, int]] = []
    for i, source in enumerate(sources):
        for j in base["residual_target_indices"]:
            proposed = targets[j]
            if type(source) is not type(proposed):
                continue
            if getattr(source, "order", None) != getattr(proposed, "order", None):
                continue
            from_atoms = expression_atoms(source.generator)
            to_atoms = expression_atoms(proposed.generator)
            if len(from_atoms) != len(to_atoms):
                continue
            factors = tuple(
                atom_evidence(x, y, cited_ids)
                for x, y in zip(from_atoms, to_atoms)
            )
            if not all(factor["well_typed"] for factor in factors):
                continue
            # Actual derivation may exist only if every factor has cited or
            # canonical-formal evidence; no shape match can grant a proof.
            step = replay_named_image(source.generator, proposed.generator, source_steps)
            if step is not None:
                certified_pairs.append((i, j))
            steps = proof_tree_steps(step) if step is not None else ()
            candidates.append({
                "source_index": i,
                "target_index": j,
                "source_generator": str(source.generator),
                "target_generator": str(proposed.generator),
                "factors": factors,
                "proof_engine_replayed": step is not None,
                "proof_step_count": len(steps),
                "cited_references": sorted({
                    proof.inference_rule.literature_reference.locator
                    for proof in steps
                    if proof.rule is ProofRule.GIVEN
                    and proof.inference_rule is not None
                    and proof.inference_rule.literature_reference is not None
                }),
                "missing_family_ids": sorted({
                    factor["family_id"] for factor in factors
                    if factor["status"] == "FAMILY_ID_KNOWN_BUT_SOURCE_NOT_CITED"
                    and type(factor["family_id"]) is int
                }),
            })
    return {
        "k": k,
        "status": "SOURCE_BACKED_IMAGE_AUDIT",
        "cited_stable_family_ids": sorted(cited_ids),
        "right_named_image_shape_matches": len(base["right_matched_target_indices"]),
        "left_source_count": len(sources),
        "residual_target_count": len(base["residual_target_indices"]),
        "candidate_pairs": candidates,
        "proved_named_images": len(certified_pairs),
        "certified_pairs": [list(value) for value in certified_pairs],
        "new_source_given": False,
        "public_completion": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "data" / "sphere.csv").is_file():
        raise RuntimeError("Expected EHP Proof Tracer repository root")
    observations = tuple(inspect_k(k) for k in (4, 7, 8, 31))
    report = {
        "phase": "173-R4-R15R4",
        "mode": "READ_ONLY_SOURCE_CITED_COMPOSITE_GENERATOR_IMAGE",
        "observations": observations,
        "proof_promoted_to_public": False,
        "full_pytest_performed": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in observations:
        print(
            "PHASE173_R4_R15R4_K=" + str(row["k"])
            + " LEFT=" + str(row.get("left_source_count", 0))
            + " NAMED_REPLAYED=" + str(row["proved_named_images"])
            + " CANDIDATES=" + str(len(row["candidate_pairs"])),
            flush=True,
        )
    last = observations[-1]
    blockers = sorted({
        fid for candidate in last["candidate_pairs"]
        for fid in candidate["missing_family_ids"]
    })
    print("PHASE173_R4_R15R4_K31_MISSING_FAMILY_SOURCE_IDS=" + ",".join(map(str, blockers)), flush=True)
    print("PHASE173_R4_R15R4_K31_NAMED_REPLAYED=" + str(last["proved_named_images"]), flush=True)
    passed = bool(
        last["left_source_count"] == 4
        and last["right_named_image_shape_matches"] == 4
        and last["residual_target_count"] == 4
        and last["public_completion"] is False
        and last["new_source_given"] is False
    )
    print("PHASE173_R4_R15R4_PRODUCTION_EDIT=NONE", flush=True)
    print("PHASE173_R4_R15R4_PUBLIC_COMPLETION=False", flush=True)
    print("PHASE173_R4_R15R4_REPORT=" + str(args.output), flush=True)
    print("PHASE173_R4_R15R4_AUDIT=" + ("PASS" if passed else "FAIL"), flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## `preflight.py`

```python
"""Fail-closed source guard with allowance for committed prior R15R3 package."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess


REVIEWED_BASE_HEAD = "3901da80ac4af7226b41246353b700708a33c085"
REVIEWED_BLOBS = {
    "phase169_r10d2_general_family_definition/family_citation.py": "b4b0c65e3eee85b557d5cfe7fa66a38a5386c3f8",
    "phase169_r10e8_hyoujigen_generic_suspension/source_records.py": "bb54cc49092c6b16c4b83b113b325e028a42f50c",
    "phase169_r10b_registered_stable_family_binding/family_registry.py": "4e461795954cc3e7a34fe9e3b47f77d00e5faeda",
    "phase169_r10e8_hyoujigen_generic_suspension/chapter_vi_reference.py": "e3b2f167428ba6b230acd8505b976eea189d39ff",
    "phase169_r10eq_r1_universal_stable_definition/definition.py": "0c74d121419b6755e947a367d7de465d81193174",
    "phase173_r4_r10_general_toda56_core/core.py": "d35600804ecbbc5f8566d52e45a2f6ecf8816347",
    "phase173_r4_r4_typed_generator_audit/audit.py": "82f9f734104ddb70df42090ee9a6413b06f1e98b",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
}
LOCAL_PINNED = {
    "phase173_r4_r15r2_generator_obligation_audit/audit.py": "9fbf9af9c4218a8ba019ce8fd131890e83a1392e6f0b9cd5f93d383d68305884",
    "phase173_r4_r15r3_formal_suspension_bridge/bridge.py": "0e2a44e97ae8d87aca02559cda5d0b8e14c1c2a161a966b5f34bb36140459adf",
}
ALLOWED_COMMITTED = "phase173_r4_r15r3_formal_suspension_bridge/"
ALLOWED_DIRTY = frozenset({".pytest_cache/v/cache/nodeids"})


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=root, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + result.stderr[:500])
    return result.stdout.strip()


def verify_source_head(root: Path) -> None:
    """Accept only the inspected HEAD lineage with intact pinned dependencies."""
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Not the EHP Proof Tracer repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    head = git(root, "rev-parse", "HEAD")
    remote = git(root, "rev-parse", "origin/develop")
    if head != remote:
        raise RuntimeError("Local develop and origin/develop differ")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_BASE_HEAD, head),
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode:
        raise RuntimeError("Unreviewed HEAD lineage")
    changed = tuple(filter(None, git(
        root, "diff", "--name-only", REVIEWED_BASE_HEAD, head,
    ).splitlines()))
    if any(
        path != ".pytest_cache/v/cache/nodeids"
        and not path.startswith(ALLOWED_COMMITTED)
        for path in changed
    ):
        raise RuntimeError("Unreviewed committed dependencies: " + repr(changed))
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    dirty = set(filter(None, git(root, "diff", "--name-only").splitlines()))
    if dirty - ALLOWED_DIRTY:
        raise RuntimeError("Unreviewed tracked local source modifications")
    for path, expected in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("Unexpected Git blob for " + path)
        if git(root, "hash-object", "--", path) != expected:
            raise RuntimeError("Modified working tree dependency: " + path)
    for path, expected in LOCAL_PINNED.items():
        target = root / path
        if not target.is_file():
            raise RuntimeError("Required previous phase source missing: " + path)
        actual = hashlib.sha256(
            target.read_bytes().replace(b"\r\n", b"\n")
        ).hexdigest()
        if actual != expected:
            raise RuntimeError("Previous phase source changed: " + path)
    print("PHASE173_R4_R15R4_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R4_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R4_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R4_PRODUCTION_EDIT=NONE", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    verify_source_head(args.root)
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
    if ($LASTEXITCODE -ne 0) { throw 'R15R4 Git fetch failed' }
    python -m phase173_r4_r15r4_cited_composition_image.preflight --root "$Root"
    if ($LASTEXITCODE -ne 0) { throw 'R15R4 Preflight failed' }
    python -m pytest -q `
        phase173_r4_r15r4_cited_composition_image/tests/test_static.py `
        phase173_r4_r15r4_cited_composition_image/tests/test_isolated.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R4 isolated tests failed' }
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R4_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R4_PRODUCTION_EDIT=NONE'
        exit 0
    }
    python -m pytest -q `
        phase173_r4_r15r4_cited_composition_image/tests/test_integration.py `
        phase173_r4_r15r3_formal_suspension_bridge/tests/test_bridge.py `
        phase173_r4_r15r2_generator_obligation_audit/tests/test_audit.py `
        phase173_r4_r15r1_unbounded_abstract_frontier/tests/test_frontier.py `
        phase173_r4_r10_general_toda56_core/tests/test_core.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R4 focused pytest failed' }
    Write-Output 'PHASE173_R4_R15R4_FOCUSED_PYTEST=PASS'
    python -m phase173_r4_r15r4_cited_composition_image.audit `
        --root "$Root" `
        --output (Join-Path $PSScriptRoot 'source_cited_image_report.json')
    if ($LASTEXITCODE -ne 0) { throw 'R15R4 cited-image audit failed' }
    Write-Output 'PHASE173_R4_R15R4_PHASE_COMPLETED=False'
} finally {
    Pop-Location
}
```

## `tests/test_static.py`

```python
"""Source boundary and structural security assertions; no live repo needed."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("name", ("bridge.py", "replay.py", "audit.py", "preflight.py"))
def test_syntax_and_no_ellipsis(name: str) -> None:
    source = (ROOT / name).read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert not any(
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and node.value.value is Ellipsis
        for node in ast.walk(tree)
    )
    assert "eval(" not in source
    assert "exec(" not in source


def test_no_old_production_code_or_public_completion_change() -> None:
    assert (ROOT / "run.ps1").is_file()
    source = (ROOT / "audit.py").read_text(encoding="utf-8")
    assert '"public_completion": False' in source
    assert '"new_source_given": False' in source
    assert "replay_named_image" in source
    assert "proof_tree_steps" in source


def test_generic_composition_has_required_premises() -> None:
    source = (ROOT / "bridge.py").read_text(encoding="utf-8")
    assert "PremisePattern(" in source
    assert "proof_rule=ProofRule.INFERENCE" in source
    assert "return (GoalExpansion(rule, factors),)" in source
    assert "factor_image_goals(goal) == factors" in source


def test_replay_requires_checked_cited_fixed_sources() -> None:
    source = (ROOT / "replay.py").read_text(encoding="utf-8")
    assert "build_cited_stable_family_definitions()" in source
    assert "build_cited_chapter_vi_family_definitions()" in source
    assert "assertion.origin is AssertionOrigin.FIXED_STATEMENT" in source
    assert "find_inference_matches_for_rule" in source
    assert "apply_inference_match" in source


def test_commit_lineage_guard_is_not_blanket_disabled() -> None:
    source = (ROOT / "preflight.py").read_text(encoding="utf-8")
    assert "merge-base" in source
    assert "REVIEWED_BLOBS" in source
    assert "LOCAL_PINNED" in source
    assert "ALLOWED_COMMITTED" in source
    assert "head != remote" in source
```

## `tests/test_isolated.py`

```python
"""Standalone typed inference tests using deliberately minimal dependency doubles."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

import pytest


@dataclass(frozen=True)
class Component:
    source: int
    target: int


@dataclass(frozen=True)
class Composition:
    left: object
    right: object


@dataclass(frozen=True)
class TodaPrimaryGroup:
    group_dimension: int
    sphere_dimension: int


@dataclass(frozen=True)
class TodaSuspensionMap:
    source_group: object
    target_group: object


@dataclass(frozen=True)
class GeneratorImage:
    map: object
    source_generator: object
    target_generator: object


@dataclass(frozen=True)
class GoalExpansion:
    rule: object
    subgoals: tuple


@dataclass(frozen=True)
class PremisePattern:
    proof_rule: object = None
    statement_type: object = None
    statement_pattern: object = None


@dataclass(frozen=True)
class InferenceRule:
    name: str
    description: str
    premise_patterns: tuple
    conclusion_pattern: object
    match_guard: object


class ProofRule(Enum):
    GIVEN = "given"
    INFERENCE = "inference"


def typed_element_span(expression: object) -> tuple[int, int] | None:
    if isinstance(expression, Component):
        return expression.source, expression.target
    if isinstance(expression, Composition):
        left = typed_element_span(expression.left)
        right = typed_element_span(expression.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return right[0], left[1]
    return None


@pytest.fixture
def isolated_bridge(monkeypatch: pytest.MonkeyPatch):
    modules = {
        "expression": {"Composition": Composition},
        "homotopy_groups": {"TodaPrimaryGroup": TodaPrimaryGroup, "TodaSuspensionMap": TodaSuspensionMap},
        "phase165_r14_r6_generic_iso": {"GeneratorImage": GeneratorImage},
        "phase165_r3_recursive_search": {"GoalExpansion": GoalExpansion},
        "phase169_r10eq_r1_universal_stable_definition.definition": {
            "typed_element_span": typed_element_span,
        },
        "proof": {"InferenceRule": InferenceRule, "PremisePattern": PremisePattern, "ProofRule": ProofRule},
    }
    for name, contents in modules.items():
        fake = ModuleType(name)
        for key, value in contents.items():
            setattr(fake, key, value)
        monkeypatch.setitem(sys.modules, name, fake)
    path = Path(__file__).resolve().parents[1] / "bridge.py"
    spec = importlib.util.spec_from_file_location("_isolated_r15r4_bridge", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _example():
    a = Component(7, 3)
    b = Component(34, 7)
    suspended_a = Component(8, 4)
    suspended_b = Component(35, 8)
    return a, b, suspended_a, suspended_b


def test_generic_compound_image_proposes_two_unproved_factor_goals(isolated_bridge) -> None:
    bridge = isolated_bridge
    a, b, ea, eb = _example()
    goal = bridge.generator_image(Composition(a, b), Composition(ea, eb))
    assert goal is not None
    parts = bridge.factor_image_goals(goal)
    assert parts == (bridge.generator_image(a, ea), bridge.generator_image(b, eb))
    proposals = bridge.expand_composed_generator_image(goal)
    assert len(proposals) == 1
    assert proposals[0].subgoals == parts
    assert proposals[0].rule.conclusion_pattern == goal
    assert len(proposals[0].rule.premise_patterns) == 2


def test_compound_guard_requires_both_inferred_atomic_premises(isolated_bridge) -> None:
    bridge = isolated_bridge
    a, b, ea, eb = _example()
    goal = bridge.generator_image(Composition(a, b), Composition(ea, eb))
    proposal = bridge.expand_composed_generator_image(goal)[0]
    left, right = proposal.subgoals
    first = SimpleNamespace(rule=ProofRule.INFERENCE, conclusion=left)
    second = SimpleNamespace(rule=ProofRule.INFERENCE, conclusion=right)
    forged = SimpleNamespace(rule=ProofRule.GIVEN, conclusion=right)
    assert proposal.rule.match_guard((first, second), {})
    assert not proposal.rule.match_guard((first,), {})
    assert not proposal.rule.match_guard((first, forged), {})
    assert not proposal.rule.match_guard((second, first), {})
    assert not proposal.rule.match_guard((), {})


def test_wrong_types_and_unproved_named_atoms_do_not_become_rules(isolated_bridge) -> None:
    bridge = isolated_bridge
    a, b, ea, eb = _example()
    wrong = Component(35, 7)
    assert bridge.generator_image(a, wrong) is None
    assert bridge.generator_image(Composition(a, b), Composition(ea, wrong)) is None
    atomic = bridge.generator_image(a, ea)
    assert atomic is not None
    assert bridge.expand_composed_generator_image(atomic) == ()
    incompatible = Composition(a, Component(35, 6))
    assert bridge.generator_image(incompatible, Composition(ea, eb)) is None


def test_forged_map_cannot_be_composed(isolated_bridge) -> None:
    bridge = isolated_bridge
    a, b, ea, eb = _example()
    goal = bridge.generator_image(Composition(a, b), Composition(ea, eb))
    forged = GeneratorImage(
        map=TodaSuspensionMap(TodaPrimaryGroup(34, 3), TodaPrimaryGroup(99, 4)),
        source_generator=goal.source_generator,
        target_generator=goal.target_generator,
    )
    assert bridge.factor_image_goals(forged) is None
    assert bridge.expand_composed_generator_image(forged) == ()
```

## `tests/test_integration.py`

```python
"""Repository-backed focused mathematical trust-boundary regression tests."""
from __future__ import annotations

from expression import Composition
from phase169_r10d2_general_family_definition.family_citation import CitedStableFamilyDefinition
from phase173_r4_r15r4_cited_composition_image.audit import (
    atom_evidence,
    expression_atoms,
    inspect_k,
)
from phase173_r4_r15r4_cited_composition_image.replay import (
    cited_source_steps,
    replay_named_image,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r4_typed_generator_audit.audit import _group_components


def test_real_chapter_definitions_are_only_given_leaves() -> None:
    sources = cited_source_steps()
    ids = {
        step.conclusion.family_id for step in sources
        if isinstance(step.conclusion, CitedStableFamilyDefinition)
    }
    assert {4, 9, 10, 11, 12}.issubset(ids)
    assert 56 not in ids
    assert 88 not in ids
    assert all(not step.premises for step in sources)


def test_k31_composition_images_require_independent_family_sources() -> None:
    row = inspect_k(31)
    assert row["left_source_count"] == 4
    assert row["right_named_image_shape_matches"] == 4
    assert row["residual_target_count"] == 4
    assert row["public_completion"] is False
    assert row["new_source_given"] is False
    assert row["proved_named_images"] <= 4
    blockers = {
        fid for candidate in row["candidate_pairs"]
        for fid in candidate["missing_family_ids"]
    }
    assert 56 in blockers or 88 in blockers


def test_cited_phi_prime_nu_square_image_is_replayable_when_registered() -> None:
    # The proof engine must establish every atomic image; textual matching is
    # insufficient. This is a source-backed, nonpublic regression target.
    row = inspect_k(31)
    matches = [x for x in row["candidate_pairs"] if x["proof_engine_replayed"]]
    assert any(x["source_index"] == 3 for x in matches)
    assert all(x["proof_step_count"] > 0 for x in matches)
    assert all(x["cited_references"] for x in matches)


def test_no_citation_means_no_nu_named_composite_proof() -> None:
    left = _group_components(exact_prior_database_result(3, 31))
    target = _group_components(exact_prior_database_result(4, 31))
    assert left is not None and target is not None
    # No cited ν-family GIVEN: E(phi' nu_28^2) cannot be identified with ν_29^2.
    assert replay_named_image(left[3].generator, target[7].generator, ()) is None


def test_generic_flattening_preserves_all_composition_atoms() -> None:
    left = _group_components(exact_prior_database_result(3, 31))
    assert left is not None
    for component in left:
        atoms = expression_atoms(component.generator)
        assert len(atoms) >= 2
        assert not any(isinstance(x, Composition) for x in atoms)
```

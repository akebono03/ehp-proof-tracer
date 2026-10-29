# Phase 171 R2J-R4-R2 — コード全文

## 変更対象

- 既存ファイル、既存クラス、既存関数、既存テスト：**変更なし**。
- 新規 `audit.py`：全文（import を含む）。
- 新規 `tests/test_audit.py`：全文（import を含む）。
- 新規 `run.ps1`：全文。
- 新規パッケージ初期化ファイル2件：全文。

各ファイルはリポジトリ直下の `phase171_r2j_r4_r2_generator_image_replay/` に追加する。


## audit.py

```python
"""Read-only replay of E(eta_2^3)=eta_3 eta_4 eta_5.

No database group structure or Toda (5.3) double equality is used as a
proof premise. All generator identities are typed, and the cited general eta
definition must be available before the pi_6^3 publication target.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from expression import Composition
from phase165_r12_r20_eta_definition import (
    TodaEtaFamilyGeneralDefinition,
    expand_cited_eta_definition,
)
from phase165_r12_r21_eta_generator_chain import expand_cited_eta_generator
from phase165_r3_recursive_search import (
    RegisteredGoalUnresolved,
    reconstruct_registered_goal,
)
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from phase166_r3c_publication_order import precedes_citing_assertion
from phase169_r10e5_composite_generator_image.rule import (
    component_image_obligations,
    expand_composite_generator_image,
)
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r1_extension_frontier_audit.audit import (
    DOUBLE_SUFFIX,
    _generator_image_goal,
    _matching_screened_relation,
)
from phase165_r14_r6_generic_iso import GeneratorImage
from proof import ProofRule, ProofStep
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*args: str) -> str:
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if args not in allowed:
        raise ValueError("read-only Git operation required")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def prepare_image_obligation():
    """Build only a goal from DB coordinates and a separately screened (5.3).

    The proposed pi_5^2 group presentation is not admitted as evidence.
    """
    screened, pi63_goal, citing = _screened_context()
    source = database_structured_group_goal_candidates(n=2, k=3)
    if len(source) != 1:
        raise RuntimeError("expected exactly one pi_5^2 database goal candidate")
    double = _matching_screened_relation(screened, citing, DOUBLE_SUFFIX)
    if double is None:
        raise RuntimeError("Toda (5.3) double equality not citation-screened")
    image = _generator_image_goal(source[0], double)
    if not isinstance(image, GeneratorImage):
        raise RuntimeError("the proposed E-image is not a typed generator image")
    if not isinstance(image.source_generator, Composition):
        raise RuntimeError("pi_5^2 candidate generator must be an actual composite")
    if not isinstance(image.target_generator, Composition):
        raise RuntimeError("the Toda (5.3) right side must be an actual composite")
    return screened, pi63_goal, citing, image


def _screened_eta_definition(screened, citing):
    """Require one earlier source, not a manufactured GIVEN or a DB row."""
    matched = []
    for link in screened.proof_links:
        step = link.step
        assertion = screened.registry.assertion(link.assertion_id)
        if (
            step is not None
            and step.rule is ProofRule.GIVEN
            and not step.premises
            and step.conclusion == TodaEtaFamilyGeneralDefinition()
            and assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and step.conclusion == assertion.content
            and precedes_citing_assertion(screened, link.assertion_id, citing)
        ):
            matched.append((link.assertion_id, step.conclusion))
    if len(matched) != 1:
        raise RuntimeError("expected one earlier, screened Chapter V eta definition")
    return matched[0]


def scoped_provider(available: tuple[object, ...]):
    """Use three existing general rules; never offer a group result as GIVEN."""
    if available != (TodaEtaFamilyGeneralDefinition(),):
        raise ValueError("only the cited general eta definition may enter this scope")

    def expand(goal: object):
        return (
            expand_composite_generator_image(goal)
            + expand_cited_eta_generator(goal)
            + expand_cited_eta_definition(goal, available)
        )

    return expand


def proof_ancestry(root: ProofStep) -> tuple[ProofStep, ...]:
    """Traverse unique typed ProofSteps without trusting rendered text."""
    found: list[ProofStep] = []
    visited: set[int] = set()

    def visit(step: ProofStep) -> None:
        if id(step) in visited:
            return
        visited.add(id(step))
        found.append(step)
        for parent in step.premises:
            visit(parent)

    visit(root)
    return tuple(found)


def replay_image() -> dict:
    """Attempt a real inference replay, reporting unresolved subgoals separately."""
    screened, pi63_goal, citing, image = prepare_image_obligation()
    source_id, general = _screened_eta_definition(screened, citing)
    scoped = scoped_provider((general,))
    existing = shared_expansion_provider(screened, proof_target=pi63_goal)
    root_options = existing(image)
    if not any(option.subgoals == component_image_obligations(image)
               for option in root_options):
        raise RuntimeError("existing shared provider lacks the observed composite image")

    progress = []

    def observe(kind: str, goal: object, step: ProofStep | None) -> None:
        if kind == "unresolved":
            value = repr(goal)[:650]
            if value not in progress:
                progress.append(value)

    try:
        root = reconstruct_registered_goal(
            image, screened, citing, scoped,
            lookup_mode="typed_reference_publication",
            progress_observer=observe,
        )
    except RegisteredGoalUnresolved as exc:
        return {
            "status": "UNFINISHED",
            "reason": str(exc)[:1200],
            "open_goals": progress[:25],
            "proof_inferences": 0,
            "proof_given_leaves": 0,
            "source_id": source_id,
            "image_goal": repr(image),
            "group_pi63_proven": False,
            "new_given_added": 0,
        }

    ancestry = proof_ancestry(root)
    given = tuple(node for node in ancestry if node.rule is ProofRule.GIVEN)
    inferred = tuple(node for node in ancestry if node.rule is ProofRule.INFERENCE)
    if root.conclusion != image or root.rule is not ProofRule.INFERENCE:
        raise RuntimeError("a generator image result must have an inferred root")
    if not given or any(node.conclusion != general or node.premises for node in given):
        raise RuntimeError("untrusted GIVEN was used in the image proof")
    if any(node.conclusion == pi63_goal for node in ancestry):
        raise RuntimeError("the requested pi_6^3 presentation was assumed")
    if not all(node.rule in (ProofRule.GIVEN, ProofRule.INFERENCE) for node in ancestry):
        raise RuntimeError("unexpected proof-step class")
    return {
        "status": "INFERRED",
        "reason": None,
        "open_goals": [],
        "proof_inferences": len(inferred),
        "proof_given_leaves": len(given),
        "source_id": source_id,
        "image_goal": repr(image),
        "inference_rule_names": [
            node.inference_rule.name if node.inference_rule else "unnamed"
            for node in inferred
        ],
        "group_pi63_proven": False,
        "new_given_added": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R2J-R4-R2 requires develop; no branch changes are made")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    print("PHASE171_R2J_R4_R2_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R2_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R2_RESULT=PASS_DRY_RUN", flush=True)
        return

    report = replay_image()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked Git state changed during read-only replay")
    OUTPUT.mkdir(exist_ok=True)
    report.update({
        "phase": "171-R2J-R4-R2",
        "mode": "READ_ONLY_INFERENCE_REPLAY",
        "git_head": head,
        "tracked_status_unchanged": True,
        "production_modified": False,
        "full_pytest": False,
    })
    outfile = OUTPUT / "audit.json"
    outfile.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R2_IMAGE_REPLAY=" + report["status"], flush=True)
    print("PHASE171_R2J_R4_R2_GIVEN_ADDED=0", flush=True)
    print("PHASE171_R2J_R4_R2_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R2_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R2_REPORT=" + str(outfile), flush=True)
    print("PHASE171_R2J_R4_R2_RUN=PASS", flush=True)


if __name__ == "__main__":
    main()
```

## tests/test_audit.py

```python
"""Focused replay and negative tests for the typed triple eta suspension."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10e5_composite_generator_image.rule import (
    component_image_obligations,
    expand_composite_generator_image,
)
from phase171_r2j_r4_r2_generator_image_replay.audit import (
    proof_ancestry,
    scoped_provider,
)
from proof import ProofRule, ProofStep


def _eta(n: int) -> HomotopyElement:
    return HomotopyElement(
        name="η" + str(n), dimension=n, source=n + 1, target=n,
        generator=GeneratorSymbol(family="η", index=n),
    )


def _triple(n: int) -> Composition:
    return Composition(_eta(n), Composition(_eta(n + 1), _eta(n + 2)))


def _image(source: object, target: object) -> GeneratorImage:
    return GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 3)),
        source, target,
    )


def test_general_composition_rule_decomposes_triple_eta_suspension():
    goal = _image(_triple(2), _triple(3))
    obligations = component_image_obligations(goal)
    assert obligations is not None and len(obligations) == 2
    first, rest = obligations
    assert first.source_generator == _eta(2)
    assert first.target_generator == _eta(3)
    next_pair = component_image_obligations(rest)
    assert next_pair is not None and len(next_pair) == 2
    assert tuple(node.source_generator for node in next_pair) == (_eta(3), _eta(4))
    assert tuple(node.target_generator for node in next_pair) == (_eta(4), _eta(5))
    assert len(expand_composite_generator_image(goal)) == 1


def test_invalid_composition_or_map_is_rejected():
    goal = _image(_triple(2), _triple(3))
    bad_target = Composition(_eta(3), Composition(_eta(5), _eta(4)))
    assert component_image_obligations(replace(goal, target_generator=bad_target)) is None
    assert component_image_obligations(replace(
        goal,
        map=TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3)),
    )) is None
    assert component_image_obligations(replace(goal, target_generator=_triple(2))) is None


def test_scoped_provider_requires_only_exact_general_definition():
    general = TodaEtaFamilyGeneralDefinition()
    provider = scoped_provider((general,))
    assert callable(provider)
    with pytest.raises(ValueError):
        scoped_provider(())
    with pytest.raises(ValueError):
        scoped_provider((general, general))
    with pytest.raises(ValueError):
        scoped_provider((general, object()))


def test_cyclic_root_cannot_be_conjured_from_composite_rule():
    from homotopy_groups import FiniteCyclicGroup
    from proof import Relation, RelationType
    goal = Relation(
        TodaPrimaryGroup(6, 3), FiniteCyclicGroup(4, _eta(3)),
        RelationType.EQUALITY,
    )
    provider = scoped_provider((TodaEtaFamilyGeneralDefinition(),))
    assert provider(goal) == ()


def test_proof_ancestry_preserves_real_rule_tags():
    leaf = ProofStep(TodaEtaFamilyGeneralDefinition(), (), ProofRule.GIVEN)
    root = ProofStep("inferred consequence", (leaf,), ProofRule.INFERENCE)
    assert proof_ancestry(root) == (root, leaf)
    assert all(step.rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
               for step in proof_ancestry(root))
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    python -B -m phase171_r2j_r4_r2_generator_image_replay.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R2 preflight failed" }
    if ($DryRun) {
        Write-Output "PHASE171_R2J_R4_R2_RUN=PASS_DRY_RUN"
        exit 0
    }
    python -B -m pytest -q -p no:cacheprovider phase171_r2j_r4_r2_generator_image_replay/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R2 focused pytest failed" }
    Write-Output "PHASE171_R2J_R4_R2_FOCUSED_PYTEST=PASS"
    python -B -m phase171_r2j_r4_r2_generator_image_replay.audit
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R2 proof replay failed" }
    Write-Output "PHASE171_R2J_R4_R2_RESULT=PASS_AUDIT_ONLY"
}
finally {
    Pop-Location
}
```

## __init__.py

```python
"""Phase 171 R2J-R4-R2: read-only generator suspension proof replay."""
```

## tests/__init__.py

```python
"""Focused tests for R2J-R4-R2."""
```


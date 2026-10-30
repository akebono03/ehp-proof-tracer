# Phase 171 R2J-R4-R3 — コード全文

新規ファイルのみを追加します。既存の本番コード・既存テスト・R4-R2 のローカル変更は変更しません。

## 変更対象一覧

- `phase171_r2j_r4_r3_double_image_bridge/source.py`（新規ファイルとして追加）

- `phase171_r2j_r4_r3_double_image_bridge/audit.py`（新規ファイルとして追加）

- `phase171_r2j_r4_r3_double_image_bridge/tests/test_audit.py`（新規ファイルとして追加）

- `phase171_r2j_r4_r3_double_image_bridge/run.ps1`（新規ファイルとして追加）


## 追加ファイルとその全文

### `source.py`

```python
"""Typed equality substitution from a cited relation and a proved E-image.

This module defines an inference schema, not an additional literature axiom.
Neither its constructor nor its expansion certifies a database group goal.
"""
from __future__ import annotations

from expression import MapApplication, Multiple
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from map_facts import EHP_E_MAP
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10e5_composite_generator_image.rule import _endpoints
from proof import (
    InferenceRule,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)


def typed_double_image_conclusion(
    relation: object, image: object,
) -> Relation | None:
    """Return a typed substitution, but only for a matching suspension image.

    For a cited equality m*a=b and an inferred E(x)=b this constructs
    m*a=E(x). The object equality of b includes its full composition tree;
    display text and aliases alone are not accepted.
    """
    if (
        not isinstance(relation, Relation)
        or relation.relation_type is not RelationType.EQUALITY
        or not isinstance(relation.lhs, Multiple)
        or type(relation.lhs.coefficient) is not int
        or relation.lhs.coefficient <= 0
        or not isinstance(image, GeneratorImage)
        or not isinstance(image.map, TodaSuspensionMap)
        or relation.rhs != image.target_generator
    ):
        return None
    src = _endpoints(image.source_generator)
    dst = _endpoints(image.target_generator)
    left = _endpoints(relation.lhs.expression)
    if (
        src is None
        or dst is None
        or left is None
        or left != dst
        or dst != (src[0] + 1, src[1] + 1)
        or image.map.source_group != TodaPrimaryGroup(*src)
        or image.map.target_group != TodaPrimaryGroup(*dst)
    ):
        return None
    return Relation(
        lhs=relation.lhs,
        rhs=MapApplication(EHP_E_MAP, image.source_generator),
        relation_type=RelationType.EQUALITY,
    )


def typed_double_image_rule(
    relation: Relation, image: GeneratorImage,
) -> InferenceRule:
    """Require exactly one cited GIVEN and one independently inferred image."""
    target = typed_double_image_conclusion(relation, image)
    if target is None:
        raise ValueError("source equality and inferred generator image are not type-compatible")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.GIVEN
            and not premises[0].premises
            and premises[1].rule is ProofRule.INFERENCE
            and premises[0].conclusion == relation
            and premises[1].conclusion == image
            and typed_double_image_conclusion(relation, image) == target
        )

    return InferenceRule(
        name="substitute independently proved typed suspension image into cited equality",
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=relation,
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=GeneratorImage,
                statement_pattern=image,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=target,
    )
```

### `audit.py`

```python
"""Read-only Phase 171 R2J-R4-R3 replay of 2 nu' = E(eta_2^3).

The cited Toda (5.3) double relation and the inferred R4-R2 image are
combined by a checked InferenceRule. No cyclic group structure is asserted.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase166_r3c_publication_order import precedes_citing_assertion
from phase171_r2j_r4_r1_extension_frontier_audit.audit import DOUBLE_SUFFIX
from phase171_r2j_r4_r2_generator_image_replay.audit import (
    _screened_eta_definition,
    prepare_image_obligation,
    proof_ancestry,
    scoped_provider,
)
from phase171_r2j_r4_r3_double_image_bridge.source import (
    typed_double_image_conclusion,
    typed_double_image_rule,
)
from proof import ProofRule, ProofStep, Relation, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    if arguments not in {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("read-only Git operation required")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def screened_double_proof_step(screened, citing: str) -> tuple[str, ProofStep]:
    """Read a unique earlier fixed, typed and actually linked source leaf."""
    matches: list[tuple[str, ProofStep]] = []
    for link in screened.proof_links:
        if not link.assertion_id.endswith(DOUBLE_SUFFIX):
            continue
        step = link.step
        assertion = screened.registry.assertion(link.assertion_id)
        reference = screened.registry.reference(assertion.reference_id)
        if (
            isinstance(step, ProofStep)
            and step.rule is ProofRule.GIVEN
            and not step.premises
            and isinstance(step.conclusion, Relation)
            and step.conclusion == assertion.content
            and assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and reference.locator == "(5.3)"
            and precedes_citing_assertion(screened, link.assertion_id, citing)
        ):
            matches.append((link.assertion_id, step))
    if len(matches) != 1:
        raise RuntimeError("expected exactly one earlier Toda (5.3) double-relation GIVEN")
    return matches[0]


def build_double_image_proof() -> tuple[ProofStep, tuple[ProofStep, ...], dict]:
    """Reconstruct the R4-R2 tree and connect it to the screened Toda leaf."""
    screened, pi63_goal, citing, image = prepare_image_obligation()
    eta_assertion_id, general = _screened_eta_definition(screened, citing)
    double_assertion_id, cited_double = screened_double_proof_step(screened, citing)
    target = typed_double_image_conclusion(cited_double.conclusion, image)
    if target is None:
        raise RuntimeError("typed Toda relation and image are structurally incompatible")
    image_root = reconstruct_registered_goal(
        image,
        screened,
        citing,
        scoped_provider((general,)),
        lookup_mode="typed_reference_publication",
    )
    if image_root.rule is not ProofRule.INFERENCE or image_root.conclusion != image:
        raise RuntimeError("R4-R2 generator image was not inferred")
    image_ancestors = proof_ancestry(image_root)
    image_leaves = tuple(
        step for step in image_ancestors if step.rule is ProofRule.GIVEN
    )
    if (
        len(image_leaves) != 1
        or image_leaves[0].conclusion != general
        or image_leaves[0].premises
        or any(step.conclusion == pi63_goal for step in image_ancestors)
    ):
        raise RuntimeError("R4-R2 image replay imported an unapproved premise")

    rule = typed_double_image_rule(cited_double.conclusion, image)
    matches = tuple(
        match for match in find_inference_matches_for_rule(
            rule, (cited_double, image_root),
        )
        if len(match.premises) == 2
        and match.premises[0] is cited_double
        and match.premises[1] is image_root
    )
    if len(matches) != 1:
        raise RuntimeError("exactly one genuine typed substitution match required")
    root = derive_inference_proof_step(matches[0])
    ancestors = proof_ancestry(root)
    if (
        root.rule is not ProofRule.INFERENCE
        or root.conclusion != target
        or root.premises != (cited_double, image_root)
        or any(step.conclusion == pi63_goal for step in ancestors)
        or any(step.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE) for step in ancestors)
    ):
        raise RuntimeError("invalid proof root or cyclic-group result admitted")
    given = tuple(step for step in ancestors if step.rule is ProofRule.GIVEN)
    if (
        len(given) != 2
        or not any(step is cited_double for step in given)
        or not any(step is image_leaves[0] for step in given)
        or any(step.premises for step in given)
    ):
        raise RuntimeError("uncited or additional GIVEN leaf in the combined proof")
    report = {
        "phase": "171-R2J-R4-R3",
        "mode": "READ_ONLY_TYPED_INFERENCE_REPLAY",
        "status": "INFERRED",
        "double_source_id": double_assertion_id,
        "eta_definition_source_id": eta_assertion_id,
        "double_source": repr(cited_double.conclusion),
        "generator_image": repr(image_root.conclusion),
        "derived_relation": repr(root.conclusion),
        "root_inference_rule": root.inference_rule.name,
        "inferences": sum(step.rule is ProofRule.INFERENCE for step in ancestors),
        "given_leaves": len(given),
        "new_given_added": 0,
        "pi63_group_proven": False,
        "production_modified": False,
        "full_pytest": False,
    }
    return root, ancestors, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R2J-R4-R3 requires develop; branch is not changed")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    if not (ROOT / "phase171_r2j_r4_r2_generator_image_replay" / "audit.py").is_file():
        raise RuntimeError("R4-R2 audit is required in the local worktree")
    print("PHASE171_R2J_R4_R3_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R3_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R3_RESULT=PASS_DRY_RUN", flush=True)
        return
    root, ancestors, report = build_double_image_proof()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked worktree changed during inference replay")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R2J_R4_R3_DOUBLE_IMAGE=" + report["status"], flush=True)
    print("PHASE171_R2J_R4_R3_INFERENCES=" + str(report["inferences"]), flush=True)
    print("PHASE171_R2J_R4_R3_GIVEN_LEAVES=" + str(report["given_leaves"]), flush=True)
    print("PHASE171_R2J_R4_R3_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R3_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R3_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R3_REPORT=" + str(destination), flush=True)
    print("PHASE171_R2J_R4_R3_RUN=PASS", flush=True)


if __name__ == "__main__":
    main()
```

### `tests/test_audit.py`

```python
"""Focused typed-double substitution, source-screening and live replay tests."""
from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

import pytest

from expression import (
    Composition,
    GeneratorSymbol,
    HomotopyElement,
    MapApplication,
    Multiple,
)
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from map_facts import EHP_E_MAP
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import GeneratorImage
from phase171_r2j_r4_r3_double_image_bridge.audit import (
    build_double_image_proof,
    screened_double_proof_step,
)
from phase171_r2j_r4_r3_double_image_bridge.source import (
    typed_double_image_conclusion,
    typed_double_image_rule,
)
from proof import (
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    find_inference_matches_for_rule,
)


def _eta(n: int) -> HomotopyElement:
    return HomotopyElement(
        name="η" + str(n),
        dimension=n,
        source=n + 1,
        target=n,
        generator=GeneratorSymbol(family="η", index=n),
    )


def _triple(n: int) -> Composition:
    return Composition(_eta(n), Composition(_eta(n + 1), _eta(n + 2)))


def _inputs() -> tuple[Relation, GeneratorImage]:
    nu = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    double = Relation(Multiple(2, nu), _triple(3), RelationType.EQUALITY)
    image = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 3)),
        _triple(2), _triple(3),
    )
    return double, image


def test_type_checked_double_image_has_exact_expected_structure():
    double, image = _inputs()
    target = typed_double_image_conclusion(double, image)
    assert target == Relation(
        double.lhs, MapApplication(EHP_E_MAP, image.source_generator),
        RelationType.EQUALITY,
    )
    assert target.lhs.coefficient == 2
    assert target.rhs.expression == _triple(2)


def test_actual_matcher_builds_inference_step_with_both_ancestors():
    double, image = _inputs()
    cited_fixture = ProofStep(double, (), ProofRule.GIVEN)
    inferred_fixture = ProofStep(image, (), ProofRule.INFERENCE)
    rule = typed_double_image_rule(double, image)
    matches = find_inference_matches_for_rule(rule, (cited_fixture, inferred_fixture))
    assert len(matches) == 1
    step = derive_inference_proof_step(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.premises == (cited_fixture, inferred_fixture)
    assert step.conclusion == typed_double_image_conclusion(double, image)


def test_wrong_target_composition_is_rejected_not_string_matched():
    double, image = _inputs()
    wrongly_ordered = Composition(_eta(3), Composition(_eta(5), _eta(4)))
    assert typed_double_image_conclusion(
        double, replace(image, target_generator=wrongly_ordered),
    ) is None
    assert typed_double_image_conclusion(
        replace(double, rhs=wrongly_ordered), image,
    ) is None


def test_wrong_map_domain_and_codomain_are_rejected():
    double, image = _inputs()
    wrong_source = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    wrong_target = TodaSuspensionMap(TodaPrimaryGroup(5, 2), TodaPrimaryGroup(7, 3))
    assert typed_double_image_conclusion(double, replace(image, map=wrong_source)) is None
    assert typed_double_image_conclusion(double, replace(image, map=wrong_target)) is None


def test_wrong_nu_degree_is_rejected():
    double, image = _inputs()
    bad_nu = replace(double.lhs.expression, source=7)
    assert typed_double_image_conclusion(
        replace(double, lhs=Multiple(2, bad_nu)), image,
    ) is None


def test_nonpositive_or_boolean_multiple_cannot_produce_relation():
    double, image = _inputs()
    for coefficient in (0, -2, True):
        assert typed_double_image_conclusion(
            replace(double, lhs=Multiple(coefficient, double.lhs.expression)), image,
        ) is None


def test_rule_does_not_accept_noninferred_image_or_uncited_relation_fixture():
    double, image = _inputs()
    rule = typed_double_image_rule(double, image)
    given_double = ProofStep(double, (), ProofRule.GIVEN)
    inferred_image = ProofStep(image, (), ProofRule.INFERENCE)
    assert find_inference_matches_for_rule(
        rule, (given_double, ProofStep(image, (), ProofRule.GIVEN)),
    ) == ()
    assert find_inference_matches_for_rule(
        rule, (ProofStep(double, (), ProofRule.INFERENCE), inferred_image),
    ) == ()
    assert find_inference_matches_for_rule(
        rule, (given_double, ProofStep(replace(image, source_generator=_eta(2)), (), ProofRule.INFERENCE)),
    ) == ()


def test_no_unregistered_double_relation_can_be_screened():
    empty = SimpleNamespace(proof_links=())
    with pytest.raises(RuntimeError):
        screened_double_proof_step(empty, "unused")


def test_real_source_bound_tree_builds_double_image_without_group_theorem():
    root, ancestry, report = build_double_image_proof()
    assert root.rule is ProofRule.INFERENCE
    assert report["status"] == "INFERRED"
    assert report["given_leaves"] == 2
    assert report["new_given_added"] == 0
    assert report["pi63_group_proven"] is False
    assert sum(step.rule is ProofRule.INFERENCE for step in ancestry) >= 2
    assert len(root.premises) == 2
```

### `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    python -B -m phase171_r2j_r4_r3_double_image_bridge.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R3 preflight failed" }
    if ($DryRun) {
        Write-Output "PHASE171_R2J_R4_R3_RESULT=PASS_DRY_RUN"
        return
    }
    python -B -m pytest -q -p no:cacheprovider `
        phase171_r2j_r4_r2_generator_image_replay/tests/test_audit.py `
        phase171_r2j_r4_r3_double_image_bridge/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R3 focused pytest failed" }
    Write-Output "PHASE171_R2J_R4_R3_FOCUSED_PYTEST=PASS"
    python -B -m phase171_r2j_r4_r3_double_image_bridge.audit
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R3 typed replay failed" }
    Write-Output "PHASE171_R2J_R4_R3_RESULT=PASS_AUDIT_ONLY"
}
finally {
    Pop-Location
}
```

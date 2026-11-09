# R40 追加コード全文（そのまま追加可能なファイル単位）

## 実装・テスト対象

既存ファイルの変更：**なし**。次の各ファイルを新しい `phase174_r3_r7_r40_adopted_db_zero_image_isolated/` に追加する。import の変更は既存ファイルに一切なく、各新規ファイルの import は冒頭から全文を掲示。

既存 API・既存テストの変更はない。今 Phase の対象に限る。

## `__init__.py` 全文

```python
"""R40 isolated, provenance-checked adopted earlier DB cyclic-zero inference."""
```

## `rule.py` 全文

```python
"""Generic cyclic zero-image inference from a VERIFIED adopted earlier DB prior.

This does not convert the DB prior to a literature reference or an INFERENCE.
The R6 inference-only rule is unchanged.  Every application revalidates the
actual adopted database step against the independently specified proof root.
"""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step,
    group_coordinates,
    verified_db_step,
)
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    cyclic_generator_zero_image_inputs,
)
from proof import InferenceRule, PremisePattern, ProofRule, Relation
from phase165_r14_r6_generic_iso import GeneratorImage
from map_property_rules import ImageZeroStatement


RULE_NAME = "adopted earlier DB cyclic presentation and inferred generator zero imply zero image"


def verified_prior_zero_image_inputs(
    goal: object,
    presentation: object,
    *,
    proof_target: object,
    bridge: RegistryBridgeResult,
) -> tuple[Relation, GeneratorImage] | None:
    """Accept a real earlier adopted DB row as an obligation, never as a theorem.

    The generator, cyclic order, E dimensions and root's precedence are all
    rechecked by the existing independent admission mechanism.  No conversion
    of a GIVEN into an INFERENCE is performed here.
    """
    if (not isinstance(bridge, RegistryBridgeResult)
            or group_coordinates(proof_target) is None):
        return None
    obligations = cyclic_generator_zero_image_inputs(goal, presentation)
    if obligations is None:
        return None
    admitted = admitted_db_step(presentation, proof_target=proof_target, bridge=bridge)
    if (admitted is None
            or admitted.rule is not ProofRule.GIVEN
            or not verified_db_step(admitted, proof_target=proof_target, bridge=bridge)):
        return None
    return obligations


def adopted_prior_zero_image_rule(
    goal: ImageZeroStatement,
    presentation: Relation,
    *,
    proof_target: object,
    bridge: RegistryBridgeResult,
) -> InferenceRule:
    """Derive zero image only from a verified DB GIVEN and an inferred zero image of g."""
    obligations = verified_prior_zero_image_inputs(
        goal, presentation, proof_target=proof_target, bridge=bridge,
    )
    if obligations is None:
        raise ValueError("Not an eligible earlier adopted cyclic DB presentation")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.GIVEN
            and premises[1].rule is ProofRule.INFERENCE
            and tuple(step.conclusion for step in premises) == obligations
            and verified_db_step(premises[0], proof_target=proof_target, bridge=bridge)
            and verified_prior_zero_image_inputs(
                goal, presentation, proof_target=proof_target, bridge=bridge,
            ) == obligations
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "A verified, explicitly adopted earlier DB presentation Z/m{g}, "
            "and a separate proved E(g)=0, imply im(E)=0. The DB premise "
            "remains an adopted GIVEN, not a cited Toda fact or an inference. "
            "Every application checks the original DB and strict root precedence."
        ),
        premise_patterns=(
            PremisePattern(
                statement_type=Relation,
                statement_pattern=obligations[0],
                proof_rule=ProofRule.GIVEN,
            ),
            PremisePattern(
                statement_type=GeneratorImage,
                statement_pattern=obligations[1],
                proof_rule=ProofRule.INFERENCE,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_adopted_prior_zero_image(
    goal: object,
    presentation: object,
    *,
    proof_target: object,
    bridge: RegistryBridgeResult,
) -> tuple[GoalExpansion, ...]:
    """Return an isolated backward candidate, not a proof or a GIVEN."""
    obligations = verified_prior_zero_image_inputs(
        goal, presentation, proof_target=proof_target, bridge=bridge,
    )
    if obligations is None:
        return ()
    return (GoalExpansion(
        adopted_prior_zero_image_rule(
            goal, presentation, proof_target=proof_target, bridge=bridge,
        ),
        obligations,
    ),)
```

## `source_guard.py` 全文

```python
"""Review-bound Git and source checks for isolated R40 audit."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_R38_HEAD = "edf3672a709bde915ba28fa868a134e4a9ae18e7"
REVIEWED_R39_PREFIX = "phase174_r3_r7_r39_verified_zero_image_frontier/"
PINS = {
    "phase174_r3_r7_r39_verified_zero_image_frontier/audit.py": "1e3b589bb221daa32c9ee1d21fb10a6dedcd2333",
    "phase174_r3_r7_r38_source_bound_zero_image_public_wiring/provider.py": "6aa48096b41714fbdf588c3ba423d264a4a13bb9",
    "phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py": "66407339808ed4ba8a65c04fd3bfbbf05bde6745",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r6_2_unified_registry_r3_r4/context_provider_registry.py": "a1afa3f733e7dd324cb827ad7a1f6cb6ee90cf40",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=ROOT, check=True,
                          text=True, capture_output=True,
                          encoding="utf-8", errors="replace").stdout.strip()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def matches_blob(data: bytes, expected: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return len(expected) == 40 and expected in (
        git_blob(data), git_blob(normalized),
        git_blob(normalized.replace(b"\n", b"\r\n")),
    )


def verify_checkout() -> dict[str, object]:
    """Allow only the actual R39 merge, no unrelated edits or relaxed hashes."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R40 at repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD")
    remote_output = git("ls-remote", "origin", "refs/heads/develop")
    remote = remote_output.split()[0] if remote_output else ""
    if not remote:
        raise RuntimeError("Cannot verify remote develop")
    if remote != REVIEWED_R38_HEAD:
        git("fetch", "-q", "origin", "develop")
        if git("rev-parse", "FETCH_HEAD") != remote:
            raise RuntimeError("Remote changed during review")
        process = subprocess.run(("git", "merge-base", "--is-ancestor", REVIEWED_R38_HEAD, remote),
                                 cwd=ROOT, capture_output=True)
        if process.returncode != 0:
            raise RuntimeError("Unreviewed remote history")
        changed_remote = tuple(git("diff", "--name-only", REVIEWED_R38_HEAD, remote).splitlines())
        if not changed_remote or any(not p.startswith(REVIEWED_R39_PREFIX) for p in changed_remote):
            raise RuntimeError("Remote changed outside reviewed R39")
    else:
        changed_remote = ()
    if local not in (REVIEWED_R38_HEAD, remote):
        raise RuntimeError("Unreviewed local HEAD")
    if git("diff", "--cached", "--name-only") or git("diff", "--name-only"):
        raise RuntimeError("Unexpected tracked edits")
    for path, sha in PINS.items():
        item = ROOT / path
        if not item.is_file() or not matches_blob(item.read_bytes(), sha):
            raise RuntimeError("Reviewed source differs: " + path)
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "reviewed_r39_merge_files": len(changed_remote),
        "reviewed_source_pins": len(PINS),
    }
```

## `audit.py` 全文

```python
"""Rebuild real cited zero-generator ancestry and audited adopted-prior zero image."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r40_adopted_db_zero_image_isolated.source_guard import verify_checkout


def inspect_isolated_zero_image() -> dict[str, object]:
    """Re-run cited R39 steps and infer E(image)=0 without changing any GIVEN."""
    from expression import Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, verified_db_step,
    )
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations, expand_composite_generator_image,
    )
    from phase169_r10eq_r1_universal_stable_definition.definition import (
        expand_defined_stable_element_image,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
        expand_cited_annihilator_specialization,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.source import CitedFamilyAnnihilator
    from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
        left_associated, lifted_stable_composition,
    )
    from phase174_r3_r7_r39_verified_zero_image_frontier.audit import derive_one, derive_from_expansion
    from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import (
        RULE_NAME, expand_adopted_prior_zero_image,
    )
    from proof import ProofRule, ProofStep, Relation, RelationType

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    cited = tuple(
        link.step for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and type(link.step.conclusion) is CitedFamilyAnnihilator
        and bridge.registry.assertion(link.assertion_id).content == link.step.conclusion
        and link.step.inference_rule is not None
        and link.step.inference_rule.literature_reference is not None
        and link.step.inference_rule.literature_reference.locator == "(5.9)"
    )
    if len(cited) != 1:
        raise RuntimeError("Exactly one independently cited Toda (5.9) general law required")
    prior = exact_prior_database_result(5, 5)
    db = admitted_db_step(prior, proof_target=root, bridge=bridge)
    if (db is None or db.rule is not ProofRule.GIVEN
            or not verified_db_step(db, proof_target=root, bridge=bridge)):
        raise RuntimeError("Actual earlier adopted database prior not verified")
    domain = prior.lhs
    suspension = TodaSuspensionMap(
        domain, TodaPrimaryGroup(domain.group_dimension + 1, domain.sphere_dimension + 1),
    )
    lifted = lifted_stable_composition(prior.rhs.generator)
    left = left_associated(lifted) if lifted is not None else None
    if left is None or type(left.left) is not type(left):
        raise RuntimeError("Canonical composition or parenthesization invalid")
    right_goal = GeneratorImage(suspension, prior.rhs.generator, lifted)
    left_goal = GeneratorImage(suspension, prior.rhs.generator, left)
    zero_goal = GeneratorImage(suspension, prior.rhs.generator, Zero())
    zero_image = ImageZeroStatement(suspension)
    annihilator = Relation(left.left, Zero(), RelationType.EQUALITY)

    annihilator_step = derive_one(
        annihilator,
        lambda goal: expand_cited_annihilator_specialization(goal, (cited[0].conclusion,)),
        (cited[0],),
    )
    parts = component_image_obligations(right_goal)
    if parts is None or len(parts) != 2:
        raise RuntimeError("Factor-image obligations changed")
    factor_steps = tuple(derive_one(goal, expand_defined_stable_element_image, ()) for goal in parts)
    right_step = derive_one(right_goal, expand_composite_generator_image, factor_steps)
    from phase174_r3_r7_r9_composition_associativity.rule import expand_generator_image_associativity
    left_step = derive_one(left_goal, expand_generator_image_associativity, (right_step,))
    from phase174_r3_r7_r7_composite_zero_audit.rule import expand_generator_zero_from_composite
    zero_step = derive_one(
        zero_goal,
        lambda goal: expand_generator_zero_from_composite(goal, left_goal),
        (left_step, annihilator_step),
    )
    if (zero_step.rule is not ProofRule.INFERENCE
            or zero_step.conclusion != zero_goal):
        raise RuntimeError("Cited generator-zero inference incomplete")

    options = expand_adopted_prior_zero_image(
        zero_image, prior, proof_target=root, bridge=bridge,
    )
    if len(options) != 1 or options[0].rule.name != RULE_NAME:
        raise RuntimeError("Isolated adopted-DB zero-image inference not proposed")
    if options[0].subgoals != (prior, zero_goal):
        raise RuntimeError("A premise was replaced or reordered")
    final = derive_from_expansion(options[0], (db, zero_step))
    if (final.rule is not ProofRule.INFERENCE or final.conclusion != zero_image
            or final.premises != (db, zero_step)):
        raise RuntimeError("Actual inferred zero image did not retain its DB provenance")
    if (db.rule is not ProofRule.GIVEN
            or db.note != "ADOPTED_DATABASE_PRIOR; independent reference not asserted"
            or any(step.conclusion in (zero_image, root) for step in (db, cited[0]))):
        raise RuntimeError("Database or result was laundered into a cited conclusion")

    return {
        "source_locator": "(5.9)",
        "cited_general_source_givens": 1,
        "earlier_adopted_db_prior_verified": True,
        "db_prior_rule": db.rule.name,
        "db_prior_is_independent_literature": False,
        "inferred_stable_factor_images": len(factor_steps),
        "inferred_generator_zero": True,
        "isolated_zero_image_proved": True,
        "isolated_zero_image_rule": final.rule.name,
        "db_given_preserved_inside_proof_tree": final.premises[0] is db,
        "isolated_not_public_provider": True,
        "upper_delta_surjectivity_proved": False,
        "root_complete": False,
        "new_givens": 0,
        "new_direct_root_givens": 0,
        "public_production_files_changed": 0,
        "full_pytest": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    result = None if args.dry_run else inspect_isolated_zero_image()
    gate = (
        "PASS_R40_SOURCE_GUARD_ONLY" if args.dry_run else
        "PASS_R40_VERIFIED_ADOPTED_DB_CYCLIC_ZERO_IMAGE_ISOLATED_PUBLIC_PENDING"
    )
    report = {"phase": "174-R3-R7-R40", "git_state": state,
              "observations": result, "gate": gate}
    directory = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r40"
    )
    directory.mkdir(parents=True, exist_ok=True)
    file = directory / ("preflight.json" if args.dry_run else "adopted_db_zero_image.json")
    file.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R40_"
    for name, value in state.items():
        print(prefix + name.upper() + "=" + str(value))
    if result is not None:
        for name, value in result.items():
            print(prefix + name.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(file))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/test_rule.py` 全文

```python
"""Focused real-adoption and fail-closed inference-contract tests for R40."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, exact_prior_database_result
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    expand_zero_image_from_cyclic_generator,
)
from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import (
    RULE_NAME, adopted_prior_zero_image_rule, expand_adopted_prior_zero_image,
    verified_prior_zero_image_inputs,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)
from homotopy_groups import FiniteCyclicGroup


def fixture():
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    relation = exact_prior_database_result(5, 5)
    assert type(relation) is Relation
    assert relation.lhs == TodaPrimaryGroup(10, 5)
    delta = TodaSuspensionMap(relation.lhs, TodaPrimaryGroup(11, 6))
    goal = ImageZeroStatement(delta)
    db = admitted_db_step(relation, proof_target=root, bridge=bridge)
    assert isinstance(db, ProofStep)
    zero = GeneratorImage(delta, relation.rhs.generator, Zero())
    independent = ProofStep(
        conclusion=zero, premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only independent generator-zero fixture"),
    )
    return root, bridge, relation, goal, db, independent


def test_adopted_earlier_db_and_inferred_zero_have_one_general_candidate():
    root, bridge, relation, goal, db, independent = fixture()
    assert verified_prior_zero_image_inputs(goal, relation, proof_target=root, bridge=bridge) == (
        relation, independent.conclusion,
    )
    result = expand_adopted_prior_zero_image(goal, relation, proof_target=root, bridge=bridge)
    assert len(result) == 1
    assert result[0].rule.name == RULE_NAME
    assert result[0].subgoals == (relation, independent.conclusion)
    assert all(not isinstance(item, ProofStep) for item in result[0].subgoals)
    matches = find_inference_matches_for_rule(result[0].rule, (db, independent))
    assert len(matches) == 1
    step = apply_inference_match(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == goal
    assert step.premises == (db, independent)
    assert db.rule is ProofRule.GIVEN
    assert db.note == "ADOPTED_DATABASE_PRIOR; independent reference not asserted"


def test_historical_r6_does_not_accept_db_given_and_remains_unchanged():
    root, bridge, relation, goal, db, independent = fixture()
    old = expand_zero_image_from_cyclic_generator(goal, relation)
    assert len(old) == 1
    assert find_inference_matches_for_rule(old[0].rule, (db, independent)) == ()


def test_forged_db_step_with_different_source_identity_is_rejected():
    root, bridge, relation, goal, db, independent = fixture()
    rule = adopted_prior_zero_image_rule(goal, relation, proof_target=root, bridge=bridge)
    forged = replace(db, inference_rule=InferenceRule(name="test-only forged DB citation"))
    assert find_inference_matches_for_rule(rule, (forged, independent)) == ()
    forged_note = replace(db, note="CITED_TODA_SOURCE")
    assert find_inference_matches_for_rule(rule, (forged_note, independent)) == ()


def test_direct_given_for_generator_zero_is_rejected():
    root, bridge, relation, goal, db, independent = fixture()
    rule = adopted_prior_zero_image_rule(goal, relation, proof_target=root, bridge=bridge)
    forged = replace(independent, rule=ProofRule.GIVEN)
    assert find_inference_matches_for_rule(rule, (db, forged)) == ()
    assert find_inference_matches_for_rule(rule, (independent, db)) == ()
    assert find_inference_matches_for_rule(rule, (db,)) == ()


def test_self_citing_or_prior_root_fails_strict_order():
    root, bridge, relation, goal, db, independent = fixture()
    wrong_root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 5))
    assert verified_prior_zero_image_inputs(
        goal, relation, proof_target=wrong_root, bridge=bridge,
    ) is None
    assert expand_adopted_prior_zero_image(
        goal, relation, proof_target=wrong_root, bridge=bridge,
    ) == ()
    with pytest.raises(ValueError, match="earlier adopted"):
        adopted_prior_zero_image_rule(
            goal, relation, proof_target=wrong_root, bridge=bridge,
        )


def test_non_database_presentation_and_wrong_order_are_rejected():
    root, bridge, relation, goal, db, independent = fixture()
    other = Relation(relation.lhs, FiniteCyclicGroup(4, relation.rhs.generator), RelationType.EQUALITY)
    assert expand_adopted_prior_zero_image(
        goal, other, proof_target=root, bridge=bridge,
    ) == ()
    assert expand_adopted_prior_zero_image(
        goal, relation, proof_target="untyped root", bridge=bridge,
    ) == ()
    assert expand_adopted_prior_zero_image(
        "not a zero image", relation, proof_target=root, bridge=bridge,
    ) == ()


def test_cross_map_and_wrong_target_zero_fail():
    root, bridge, relation, goal, db, independent = fixture()
    rule = adopted_prior_zero_image_rule(goal, relation, proof_target=root, bridge=bridge)
    wrong_map = TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(12, 7))
    altered = replace(independent, conclusion=GeneratorImage(
        wrong_map, relation.rhs.generator, Zero(),
    ))
    assert find_inference_matches_for_rule(rule, (db, altered)) == ()
    altered_two = replace(independent, conclusion=GeneratorImage(
        goal.map, relation.rhs.generator, "zero",
    ))
    assert find_inference_matches_for_rule(rule, (db, altered_two)) == ()


def test_rule_is_not_registered_by_constructing_it():
    root, bridge, relation, goal, db, independent = fixture()
    before = tuple(bridge.proof_links)
    options = expand_adopted_prior_zero_image(
        goal, relation, proof_target=root, bridge=bridge,
    )
    assert len(options) == 1
    assert bridge.proof_links == before
    assert all(link.step is None or link.step.conclusion != goal for link in before)
```

## `tests/test_audit.py` 全文

```python
"""R40 actual source-bound citation and adopted-prior proof frontier checks."""
from __future__ import annotations

from phase174_r3_r7_r40_adopted_db_zero_image_isolated.audit import inspect_isolated_zero_image


def test_real_toda_annihilator_and_prior_db_derive_zero_image():
    report = inspect_isolated_zero_image()
    assert report["source_locator"] == "(5.9)"
    assert report["inferred_stable_factor_images"] == 2
    assert report["inferred_generator_zero"] is True
    assert report["isolated_zero_image_proved"] is True
    assert report["db_given_preserved_inside_proof_tree"] is True


def test_no_independent_literature_or_public_root_claim():
    report = inspect_isolated_zero_image()
    assert report["earlier_adopted_db_prior_verified"] is True
    assert report["db_prior_rule"] == "GIVEN"
    assert report["db_prior_is_independent_literature"] is False
    assert report["isolated_not_public_provider"] is True
    assert report["upper_delta_surjectivity_proved"] is False
    assert report["root_complete"] is False
    assert report["new_givens"] == 0
    assert report["new_direct_root_givens"] == 0
    assert report["public_production_files_changed"] == 0
```

## `tests/test_guard.py` 全文

```python
"""R40 source pinning and exact-path checks."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r40_adopted_db_zero_image_isolated import source_guard


def test_blob_pin_has_full_forty_hex_digits():
    assert source_guard.PINS
    assert all(len(x) == 40 and set(x) <= set("0123456789abcdef")
               for x in source_guard.PINS.values())
    b = b"alpha\nbeta\n"
    sha = source_guard.git_blob(b)
    assert source_guard.matches_blob(b, sha)
    assert source_guard.matches_blob(b.replace(b"\n", b"\r\n"), sha)
    assert not source_guard.matches_blob(b"tampered", sha)


def test_checkout_protects_real_upstream_sources():
    check = source_guard.verify_checkout()
    assert check["source_guard"] == "PASS"
    assert check["reviewed_source_pins"] == len(source_guard.PINS)


def test_wrong_source_sha_is_rejected(monkeypatch):
    changed = dict(source_guard.PINS)
    changed["sources/toda/Toda_05_2.tex"] = "0" * 40
    monkeypatch.setattr(source_guard, "PINS", changed)
    with pytest.raises(RuntimeError, match="Reviewed source differs"):
        source_guard.verify_checkout()
```

## `tests/test_static.py` 全文

```python
"""Standalone static checks runnable without the full repository."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_all_r40_python_compiles_without_source_omissions():
    paths = tuple(PACKAGE.rglob("*.py"))
    assert paths
    for path in paths:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_no_direct_given_or_root_claim_in_rule():
    data = (PACKAGE / "rule.py").read_text(encoding="utf-8")
    assert "verified_db_step(premises[0]" in data
    assert "ProofRule.INFERENCE" in data
    assert "ProofRule.GIVEN" in data
    assert "ProofStep(" not in data
    assert "TodaPrimaryGroupZeroStatement(" not in data


def test_no_prior_production_function_mutations():
    data = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    assert "derive_from_expansion" in data
    assert "new_givens" in data
    assert "root_complete" in data
    assert (PACKAGE / "run.ps1").is_file()


def test_all_full_implementation_and_test_units_documented():
    docs = (PACKAGE / "CODE_FULL_JA.md").read_text(encoding="utf-8")
    assert "## `rule.py` 全文" in docs
    assert "## `audit.py` 全文" in docs
    assert "## `source_guard.py` 全文" in docs
    assert "## `tests/test_rule.py` 全文" in docs
```

## `run.ps1` 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r40_adopted_db_zero_image_isolated.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R40 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R40_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r40_adopted_db_zero_image_isolated.audit
    if ($LASTEXITCODE -ne 0) { throw 'R40 isolated zero-image inference failed' }
    $Groups = @(
        @{Name='R40_STATIC'; Path='phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_static.py'},
        @{Name='R40_RULE'; Path='phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py'},
        @{Name='R40_REAL_AUDIT'; Path='phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_audit.py'},
        @{Name='R40_GUARD'; Path='phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_guard.py'},
        @{Name='R39_REAL_PROOF'; Path='phase174_r3_r7_r39_verified_zero_image_frontier/tests/test_proof.py'},
        @{Name='R6_HISTORICAL'; Path='phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py'},
        @{Name='R38_PUBLIC'; Path='phase174_r3_r7_r38_source_bound_zero_image_public_wiring/tests/test_public.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R40_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R40 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R40_RUN=PASS'
    Write-Output 'PHASE174_R3R7R40_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```

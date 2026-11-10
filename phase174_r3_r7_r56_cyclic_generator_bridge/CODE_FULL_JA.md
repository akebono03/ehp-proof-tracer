# R56 コード全文（新規・変更対象）

変更した既存関数 `shared_expansion_provider()` と `search_shared_group_goal()` の全文は、run.ps1 の本実行後に `output/CHANGED_FUNCTIONS_FULL_JA.md` に自動出力されます。既存の import 部分は変更していません。新規関数・クラスは `rule.py` に追加し、いずれもこのパッケージが新規追加される位置に置きます。

## `rule.py` 全文

```python
"""Shared cyclic-generator lifting and generator-image surjectivity in EHP.

The first rule separates the cyclic generator conclusion from the already
certified four-premise R37 Hopf argument. The second uses that conclusion and
an independently proved typed Hopf-Delta formula to establish surjectivity.
Neither rule creates a source leaf, trusts a database name as evidence, nor
special-cases a fixed group/stem. R37's original public rule is retained.
"""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27TypedHopfDeltaStatement,
    typed_specialization,
)
from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
    upper_delta_surjectivity_inputs,
)
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


CYCLIC_RULE_NAME = "injective Hopf generated image lifts a free cyclic generator"
SURJECTIVE_RULE_NAME = "generator of Delta codomain is Delta image implies surjectivity"


def canonical_typed_delta_generator(
    witness: object,
) -> HomotopyElement | None:
    """Project a *typed* Delta(iota) witness to the existing DB goal notation.

    This is a canonical representation constructor, not a proof step. In
    particular, an arbitrary HomotopyElement whose printed name resembles
    Delta(iota) cannot supply the witness. The sourced R25 theorem and its
    independently verified prerequisites remain mandatory in the rules.
    """
    if type(witness) is not Prop27TypedHopfDeltaStatement:
        return None
    n = witness.n
    if type(n) is not int or n < 4 or n % 2 != 0:
        return None
    if witness != typed_specialization(n):
        return None
    delta = witness.delta
    target = delta.target_group
    if (type(delta) is not TodaDeltaMap
            or type(target) is not TodaPrimaryGroup
            or target.sphere_dimension != n
            or target.group_dimension != 2 * n - 1
            or witness.source_iota_dimension != 2 * n + 1):
        return None
    index = witness.source_iota_dimension
    return HomotopyElement(
        name=f"Δ(ι{index})",
        dimension=target.sphere_dimension,
        source=target.group_dimension,
        target=target.sphere_dimension,
        generator=GeneratorSymbol(family=rf"\Delta(\iota_{{{index}}})"),
    )


def cyclic_generator_inputs(goal: object) -> tuple[object, ...] | None:
    """Only the already checked R37 four-premise typed EHP geometry qualifies."""
    if (type(goal) is not Relation
            or goal.relation_type is not RelationType.EQUALITY
            or type(goal.lhs) is not TodaPrimaryGroup
            or type(goal.rhs) is not FreeCyclicGroup):
        return None
    target = goal.lhs
    n = target.sphere_dimension
    if type(n) is not int or n < 4 or n % 2:
        return None
    witness = typed_specialization(n)
    if (witness.delta.target_group != target
            or canonical_typed_delta_generator(witness) != goal.rhs.generator):
        return None
    required = upper_delta_surjectivity_inputs(MapSurjective(witness.delta))
    if (required is None or len(required) != 4 or required[3] != witness):
        return None
    return required


def cyclic_generator_rule(goal: Relation) -> InferenceRule:
    """H injective and im(H)=<H(g)> imply A=<g>, with four certified facts."""
    required = cyclic_generator_inputs(goal)
    if required is None:
        raise ValueError("not an exact typed cyclic-generator EHP goal")

    def guard(premises, bindings):
        return (
            len(premises) == 4
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and cyclic_generator_inputs(goal) == required
        )

    return InferenceRule(
        name=CYCLIC_RULE_NAME,
        description=(
            "For an injective H with im(H)=<2*iota> and an independently "
            "proved H(Delta(iota))=+/-2*iota, the typed Delta(iota) generates "
            "its source group. Every antecedent is an ordinary inferred "
            "ProofStep; a database generator label is never an axiom."
        ),
        premise_patterns=tuple(
            PremisePattern(
                statement_type=type(item),
                statement_pattern=item,
                proof_rule=ProofRule.INFERENCE,
            )
            for item in required
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_cyclic_generator_from_hopf(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Offer the proved-generator root for any matching even EHP dimension."""
    required = cyclic_generator_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(cyclic_generator_rule(goal), required),)


def delta_surjectivity_generator_inputs(
    goal: object,
) -> tuple[Relation, Prop27TypedHopfDeltaStatement] | None:
    """Separate cyclic target presentation from typed Delta(iota) provenance."""
    if type(goal) is not MapSurjective or type(goal.map) is not TodaDeltaMap:
        return None
    delta = goal.map
    if type(delta.target_group) is not TodaPrimaryGroup:
        return None
    n = delta.target_group.sphere_dimension
    if type(n) is not int or n < 4 or n % 2:
        return None
    witness = typed_specialization(n)
    generator = canonical_typed_delta_generator(witness)
    if generator is None or witness.delta != delta:
        return None
    return (
        Relation(delta.target_group, FreeCyclicGroup(generator), RelationType.EQUALITY),
        witness,
    )


def delta_surjectivity_from_generator_rule(goal: MapSurjective) -> InferenceRule:
    """A=<Delta(iota)> and sourced typed Delta(iota) imply Delta is onto.

    A prior DB result is allowed as a group premise only when the existing
    source-first search itself admits it; this function never admits a DB row.
    """
    required = delta_surjectivity_generator_inputs(goal)
    if required is None:
        raise ValueError("not an exact typed Delta cyclic surjectivity goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and premises[1].rule is ProofRule.INFERENCE
            and tuple(step.conclusion for step in premises) == required
            and delta_surjectivity_generator_inputs(goal) == required
        )

    return InferenceRule(
        name=SURJECTIVE_RULE_NAME,
        description=(
            "An element written as the typed Delta of the canonical identity "
            "generates the target group; the proved typed Delta application "
            "witness therefore makes Delta surjective. An earlier admitted "
            "database presentation or an inferred cyclic group can be used."
        ),
        premise_patterns=(
            PremisePattern(
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=required[0],
            ),
            PremisePattern(
                statement_type=Prop27TypedHopfDeltaStatement,
                statement_pattern=required[1],
                proof_rule=ProofRule.INFERENCE,
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_delta_surjectivity_from_generator(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Generic reverse candidate; no source, GIVEN or proof result is created."""
    required = delta_surjectivity_generator_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(delta_surjectivity_from_generator_rule(goal), required),)

```

## `install.py` 全文

```python
"""Source-guarded R56 installer; only common provider wiring is edited.

Git object bytes are pinned. All local file edits and EOL styles are preserved
unless they exactly match the reviewed baseline, and an idempotent re-run is
allowed. Existing mathematical and presentation modules are not rewritten.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
SHARED = "phase165_r52_r9_shared_math.py"
PINNED_SHA = "534b552856fefc8315b243fecc3170ee5792ebc7"
REVIEWED_ANCESTOR = "d923ff2a34b6ba9d4c23d3da0221402f0b815f46"
REVIEWED_GITHUB_HEAD = "0a5be29a4458cdffaa8a7ad4ad31c2e91f6941f9"

PROVIDER_BEFORE = '''    extra_providers = (
        expand_hopf_injective_from_zero_image,
        expand_upper_delta_surjectivity,
    ) + tuple(extra_providers)
'''
PROVIDER_AFTER = '''    extra_providers = (
        expand_hopf_injective_from_zero_image,
        expand_upper_delta_surjectivity,
    ) + tuple(extra_providers)
    # R56: two ordinary typed EHP consequences, shared by every root query.
    # Prefer the two-step generator route while preserving the old R37 rule.
    from phase174_r3_r7_r56_cyclic_generator_bridge.rule import (
        expand_cyclic_generator_from_hopf,
        expand_delta_surjectivity_from_generator,
    )
    extra_providers = (
        expand_delta_surjectivity_from_generator,
        expand_cyclic_generator_from_hopf,
    ) + tuple(extra_providers)
'''
SHARED_SEARCH_BEFORE = '''    if expansion_provider is None:
        expansion_provider = shared_expansion_provider(
            proof_context, proof_target=goal,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
    return search_registered_partial_proof(
'''
SHARED_SEARCH_AFTER = '''    if expansion_provider is None:
        expansion_provider = shared_expansion_provider(
            proof_context, proof_target=goal,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
        # Every ordinary (nonzero) group search needs the same cited R53
        # source-bound kernel candidate already used by the zero-group route.
        # This is a candidate ordering wrapper, not a new premise or GIVEN.
        from phase174_r3_r7_r53_public_source_bound_kernel.provider import (
            build_public_source_bound_kernel_provider,
        )
        expansion_provider = build_public_source_bound_kernel_provider(
            expansion_provider, proof_context,
        )
    return search_registered_partial_proof(
'''


def _git(*args: str, binary: bool = False):
    cmd = subprocess.run(("git",) + args, cwd=ROOT, check=False,
                         capture_output=True)
    if cmd.returncode:
        raise RuntimeError("git " + " ".join(args) + " failed: "
                           + cmd.stderr.decode("utf-8", "replace").strip())
    return cmd.stdout if binary else cmd.stdout.decode("utf-8", "replace").strip()


def _git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def _normalize(raw: bytes) -> tuple[str, bytes, str]:
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    data = raw[len(bom):]
    if b"\r" in data.replace(b"\r\n", b""):
        raise RuntimeError("unsupported CR-only or mixed EOL")
    return data.decode("utf-8").replace("\r\n", "\n"), bom, ("\r\n" if b"\r\n" in data else "\n")


def _write_style(text: str, bom: bytes, eol: str) -> bytes:
    return bom + text.replace("\n", eol).encode("utf-8")


def _replace_once(text: str, before: str, after: str, name: str) -> str:
    if text.count(before) != 1:
        raise RuntimeError("missing or ambiguous reviewed patch anchor: " + name)
    return text.replace(before, after, 1)


def patch_shared(source: str) -> str:
    result = _replace_once(source, PROVIDER_BEFORE, PROVIDER_AFTER, "common provider")
    result = _replace_once(result, SHARED_SEARCH_BEFORE, SHARED_SEARCH_AFTER,
                           "ordinary group source-bound provider")
    ast.parse(result, filename=SHARED)
    return result


def _whole_function(source: str, name: str) -> str:
    tree = ast.parse(source)
    functions = [item for item in tree.body
                 if isinstance(item, ast.FunctionDef) and item.name == name]
    if len(functions) != 1:
        raise RuntimeError("cannot extract unique full function " + name)
    node = functions[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def review() -> dict[str, object]:
    if _git("branch", "--show-current") != "develop":
        raise RuntimeError("expected develop branch")
    if (_git("rev-parse", "--show-toplevel").replace("\\", "/").lower()
            != str(ROOT).replace("\\", "/").lower()):
        raise RuntimeError("extract the ZIP into repository root")
    status = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_ANCESTOR, "HEAD"),
        cwd=ROOT, check=False,
    )
    if status.returncode:
        raise RuntimeError("HEAD does not descend from reviewed R55 baseline")
    committed_sha = _git("rev-parse", "HEAD:" + SHARED)
    if committed_sha != PINNED_SHA:
        raise RuntimeError("unreviewed committed provider module")
    raw_git = _git("show", "HEAD:" + SHARED, binary=True)
    if _git_blob(raw_git) != PINNED_SHA:
        raise RuntimeError("committed Git object byte check failed")
    base = _normalize(raw_git)[0]
    intended = patch_shared(base)
    local_path = ROOT / SHARED
    local = local_path.read_bytes()
    current, bom, eol = _normalize(local)
    if current not in (base, intended):
        raise RuntimeError("unreviewed user changes in provider module: " + SHARED)
    staged = _git("diff", "--cached", "--name-only", "--", SHARED)
    if staged:
        raise RuntimeError("provider file has staged modifications")
    code = (PACKAGE / "rule.py").read_text(encoding="utf-8")
    if "GIVEN" in code and "ProofRule.GIVEN" not in code:
        raise RuntimeError("unexpected rule source")
    ast.parse(code, filename="rule.py")
    return {
        "local_head": _git("rev-parse", "HEAD"),
        "github_reviewed_head": REVIEWED_GITHUB_HEAD,
        "source_guard": "PASS",
        "provider": SHARED,
        "current": current,
        "proposed": intended,
        "existing_bytes": local,
        "future_bytes": _write_style(intended, bom, eol),
        "new_givens": 0,
        "new_general_rules": 2,
        "changed_production_files": [SHARED],
    }


def install(*, dry_run: bool) -> dict[str, object]:
    state = review()
    changed = state["existing_bytes"] != state["future_bytes"]
    if not dry_run:
        if changed:
            (ROOT / SHARED).write_bytes(state["future_bytes"])
        new_source = _normalize((ROOT / SHARED).read_bytes())[0]
        if new_source != state["proposed"]:
            raise RuntimeError("post-install source mismatch")
        folder = PACKAGE / "output"
        folder.mkdir(exist_ok=True)
        (folder / "phase165_r52_r9_shared_math.FULL.py").write_text(
            new_source, encoding="utf-8")
        full = (
            "# R56 変更後の関数全文\n\n"
            "## phase165_r52_r9_shared_math.py : shared_expansion_provider\n\n"
            "```python\n" + _whole_function(new_source, "shared_expansion_provider")
            + "\n```\n\n"
            "## phase165_r52_r9_shared_math.py : search_shared_group_goal\n\n"
            "```python\n" + _whole_function(new_source, "search_shared_group_goal")
            + "\n```\n"
        )
        (folder / "CHANGED_FUNCTIONS_FULL_JA.md").write_text(full, encoding="utf-8")
    result = {key: value for key, value in state.items()
              if key not in ("current", "proposed", "existing_bytes", "future_bytes")}
    result["would_change" if dry_run else "changed"] = changed
    result["gate"] = "PASS_PREFLIGHT_ONLY" if dry_run else "PASS_R56_SHARED_PROVIDER_CONNECTED"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = install(dry_run=args.dry_run)
    print("PHASE174_R56_LOCAL_HEAD=" + str(report["local_head"]))
    print("PHASE174_R56_SOURCE_GUARD=" + str(report["source_guard"]))
    print("PHASE174_R56_NEW_GIVENS=0")
    print("PHASE174_R56_NEW_GENERAL_RULES=2")
    print("PHASE174_R56_GATE=" + str(report["gate"]))
    if not args.dry_run:
        print("PHASE174_R56_FUNCTIONS_FULL=" + str(
            PACKAGE / "output" / "CHANGED_FUNCTIONS_FULL_JA.md"
        ))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## `audit.py` 全文

```python
"""Real source-first Group query audit for the two general R56 inferences."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r56_cyclic_generator_bridge.install import review


PACKAGE = Path(__file__).resolve().parent


def _search_with_model(n: int, k: int, bridge):
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative

    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or result.open_goals:
        raise RuntimeError(f"pi_{n+k}^{n} is not independently completed")
    if len(contexts) != 1:
        raise RuntimeError("public screened source context is missing or duplicated")
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=None,
        derived_target_without_citing_id=True,
    )
    return result, build_linked_proof_narrative_model(result, contexts[0])


def inspect_public() -> dict[str, object]:
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r56_cyclic_generator_bridge.rule import (
        CYCLIC_RULE_NAME, SURJECTIVE_RULE_NAME,
    )
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    first, model1 = _search_with_model(6, 5, bridge)
    expected = exact_prior_database_result(6, 5)
    if expected is None or first.conclusion != expected:
        raise RuntimeError("pi_11^6 goal mismatches exact registered database structure")
    cyclic_roots = [step for step in model1.steps
                    if step.rule is ProofRule.INFERENCE
                    and step.conclusion == expected
                    and getattr(step.inference_rule, "name", None) == CYCLIC_RULE_NAME]
    if len(cyclic_roots) != 1:
        raise RuntimeError("pi_11^6 has no inferred, general four-premise cyclic root")
    if len(cyclic_roots[0].premises) != 4:
        raise RuntimeError("pi_11^6 cyclic source contract was weakened")

    second, model2 = _search_with_model(7, 5, bridge)
    if (not isinstance(second.conclusion, TodaPrimaryGroupZeroStatement)
            or second.conclusion.group != TodaPrimaryGroup(12, 7)):
        raise RuntimeError("pi_12^7 zero root changed")
    full = tuple(model2.steps)
    two_step = [step for step in full if step.rule is ProofRule.INFERENCE
                and getattr(step.inference_rule, "name", None) == SURJECTIVE_RULE_NAME]
    prior_used = [step for step in full if step.rule is ProofRule.GIVEN
                  and step.conclusion == expected
                  and "ADOPTED_DATABASE_PRIOR" in (step.note or "")]
    if not two_step:
        raise RuntimeError("pi_12^7 did not select the shared generator-to-surjectivity rule")
    if len(prior_used) != 1:
        raise RuntimeError("pi_12^7 did not reuse the ordered prior DB result")
    if any(item.conclusion == expected and item.rule is ProofRule.INFERENCE for item in full):
        raise RuntimeError("pi_12^7 unnecessarily reproved its admitted prior group")

    return {
        "pi11_6_complete": True,
        "pi11_6_group_root_rule": CYCLIC_RULE_NAME,
        "pi11_6_group_root_premise_count": len(cyclic_roots[0].premises),
        "pi11_6_steps": len(model1.steps),
        "pi11_6_citation_count": len(model1.citations),
        "pi12_7_complete": True,
        "pi12_7_surjectivity_rule": SURJECTIVE_RULE_NAME,
        "pi12_7_prior_db_adopted_once": True,
        "pi12_7_prior_group_reproved": False,
        "pi12_7_steps": len(model2.steps),
        "pi12_7_citation_count": len(model2.citations),
        "new_given": 0,
        "new_math_rules": 2,
        "full_pytest": False,
        "gate": "PASS_R56_TWO_GENERAL_RULES_SOURCE_FIRST_PUBLIC",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = review()
    data = None if args.dry_run else inspect_public()
    report = {
        "phase": "174-R3-R7-R56",
        "local_head": state["local_head"],
        "source_guard": state["source_guard"],
        "inspection": data,
        "gate": "PASS_PREFLIGHT_ONLY" if args.dry_run else data["gate"],
    }
    destination = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    destination /= "EHPProofTracerAudit" / "phase174_r3_r7_r56"
    destination.mkdir(parents=True, exist_ok=True)
    output = destination / ("preflight.json" if args.dry_run else "public_proofs.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE174_R56_SOURCE_GUARD=" + str(report["source_guard"]))
    if data is not None:
        for key, value in data.items():
            if key != "gate":
                print("PHASE174_R56_" + key.upper() + "=" + str(value))
    print("PHASE174_R56_REPORT=" + str(output))
    print("PHASE174_R56_GATE=" + str(report["gate"]))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## `tests/test_rule.py` 全文

```python
"""Focused algebraic EHP bridge tests; hypothetical steps never count as evidence."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapSurjective
from phase174_r3_r7_r25_prop27_isolated_inference.rule import typed_specialization
from phase174_r3_r7_r56_cyclic_generator_bridge.rule import (
    CYCLIC_RULE_NAME,
    SURJECTIVE_RULE_NAME,
    canonical_typed_delta_generator,
    cyclic_generator_inputs,
    cyclic_generator_rule,
    delta_surjectivity_generator_inputs,
    delta_surjectivity_from_generator_rule,
    expand_cyclic_generator_from_hopf,
    expand_delta_surjectivity_from_generator,
)
from proof import (
    InferenceRule,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    apply_inference_match,
    find_inference_matches_for_rule,
)


def _goal(n: int) -> Relation:
    theorem = typed_specialization(n)
    return Relation(
        theorem.delta.target_group,
        FreeCyclicGroup(canonical_typed_delta_generator(theorem)),
        RelationType.EQUALITY,
    )


def _test_step(statement: object, rule: ProofRule = ProofRule.INFERENCE) -> ProofStep:
    return ProofStep(
        statement, (), rule,
        inference_rule=InferenceRule(name="hypothetical-test-only"),
    )


@pytest.mark.parametrize("n", (4, 6, 8, 10))
def test_four_certified_inputs_propose_generator_relation(n: int) -> None:
    goal = _goal(n)
    required = cyclic_generator_inputs(goal)
    assert required is not None and len(required) == 4
    assert required == tuple(
        expand_cyclic_generator_from_hopf(goal)[0].subgoals
    )
    options = expand_cyclic_generator_from_hopf(goal)
    assert len(options) == 1
    assert options[0].rule.name == CYCLIC_RULE_NAME
    facts = tuple(_test_step(item) for item in required)
    matches = find_inference_matches_for_rule(cyclic_generator_rule(goal), facts)
    assert len(matches) == 1
    proof = apply_inference_match(matches[0])
    assert proof.rule is ProofRule.INFERENCE
    assert proof.conclusion == goal
    assert proof.premises == facts


def test_real_db_goal_generator_representation_is_canonical() -> None:
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result

    assert exact_prior_database_result(6, 5) == _goal(6)
    assert _goal(6).lhs == TodaPrimaryGroup(11, 6)
    element = _goal(6).rhs.generator
    assert element == HomotopyElement(
        name="Δ(ι13)", dimension=6, source=11, target=6,
        generator=GeneratorSymbol(family=r"\Delta(\iota_{13})"),
    )


@pytest.mark.parametrize("missing", range(4))
def test_missing_a_proved_hopf_premise_blocks_group_rule(missing: int) -> None:
    goal = _goal(6)
    facts = tuple(
        _test_step(item)
        for i, item in enumerate(cyclic_generator_inputs(goal))
        if i != missing
    )
    assert not find_inference_matches_for_rule(cyclic_generator_rule(goal), facts)


def test_proposed_group_cannot_be_discharged_by_direct_given_premises() -> None:
    goal = _goal(6)
    required = cyclic_generator_inputs(goal)
    for index in range(4):
        facts = tuple(
            _test_step(item, ProofRule.GIVEN if i == index else ProofRule.INFERENCE)
            for i, item in enumerate(required)
        )
        assert not find_inference_matches_for_rule(cyclic_generator_rule(goal), facts)


def test_mismatched_generator_or_dimension_is_rejected() -> None:
    goal = _goal(6)
    current = goal.rhs.generator
    bad = replace(current, name="Δ(ι15)")
    assert cyclic_generator_inputs(Relation(goal.lhs, FreeCyclicGroup(bad))) is None
    assert cyclic_generator_inputs(Relation(
        TodaPrimaryGroup(11, 7), goal.rhs
    )) is None
    assert cyclic_generator_inputs("pi11-6") is None
    assert canonical_typed_delta_generator(replace(
        typed_specialization(6), sign_undetermined=False
    )) is None


@pytest.mark.parametrize("n", (4, 6, 8, 10))
def test_generator_and_typed_delta_prove_surjectivity(n: int) -> None:
    theorem = typed_specialization(n)
    goal = MapSurjective(theorem.delta)
    required = delta_surjectivity_generator_inputs(goal)
    assert required == (_goal(n), theorem)
    candidates = expand_delta_surjectivity_from_generator(goal)
    assert len(candidates) == 1
    assert candidates[0].rule.name == SURJECTIVE_RULE_NAME
    facts = (_test_step(required[0]), _test_step(required[1]))
    matches = find_inference_matches_for_rule(
        delta_surjectivity_from_generator_rule(goal), facts
    )
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == goal


def test_admitted_prior_relation_is_permitted_but_theorem_must_be_inferred() -> None:
    theorem = typed_specialization(6)
    goal = MapSurjective(theorem.delta)
    relation, witness = delta_surjectivity_generator_inputs(goal)
    valid = (_test_step(relation, ProofRule.GIVEN), _test_step(witness))
    assert len(find_inference_matches_for_rule(
        delta_surjectivity_from_generator_rule(goal), valid
    )) == 1
    invalid = (_test_step(relation, ProofRule.GIVEN),
               _test_step(witness, ProofRule.GIVEN))
    assert not find_inference_matches_for_rule(
        delta_surjectivity_from_generator_rule(goal), invalid
    )


def test_unproved_or_mismatched_delta_witness_blocks_surjectivity() -> None:
    theorem = typed_specialization(6)
    goal = MapSurjective(theorem.delta)
    relation, witness = delta_surjectivity_generator_inputs(goal)
    for facts in (
        (_test_step(relation),),
        (_test_step(relation), _test_step(typed_specialization(8))),
        (_test_step(relation), _test_step(replace(witness, absolute_coefficient=4))),
    ):
        assert not find_inference_matches_for_rule(
            delta_surjectivity_from_generator_rule(goal), facts
        )


def test_unrelated_goals_and_odd_instances_have_no_proposals() -> None:
    assert expand_cyclic_generator_from_hopf(object()) == ()
    assert expand_delta_surjectivity_from_generator(object()) == ()
    theorem = typed_specialization(6)
    assert expand_delta_surjectivity_from_generator(
        MapSurjective(theorem.hopf)
    ) == ()


def test_providers_only_propose_subgoals_not_proofs_or_givens() -> None:
    candidates = (
        expand_cyclic_generator_from_hopf(_goal(6))
        + expand_delta_surjectivity_from_generator(
            MapSurjective(typed_specialization(6).delta)
        )
    )
    assert len(candidates) == 2
    for option in candidates:
        assert not any(isinstance(p, ProofStep) for p in option.subgoals)
        assert option.rule.conclusion_pattern is not None

```

## `tests/test_public.py` 全文

```python
"""Verify independent source-first proof searches under real production sources."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroupZeroStatement, TodaPrimaryGroup
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from proof import ProofRule


def _public_search(*, n: int, k: int, bridge):
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=None,
        derived_target_without_citing_id=True,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    return result, model


def test_pi11_6_is_independently_proved_with_certified_generator() -> None:
    bridge = build_shared_typed_bridge()
    result, model = _public_search(n=6, k=5, bridge=bridge)
    expected = exact_prior_database_result(6, 5)
    assert expected is not None
    assert result.conclusion == expected
    assert result.proven_steps
    assert model.steps[model.root_index].rule is ProofRule.INFERENCE
    assert model.steps[model.root_index].conclusion == expected
    assert any(item.reference.locator == "Proposition 2.7"
               for item in model.citations)


def test_pi12_7_remains_source_first_complete() -> None:
    bridge = build_shared_typed_bridge()
    result, model = _public_search(n=7, k=5, bridge=bridge)
    assert isinstance(result.conclusion, TodaPrimaryGroupZeroStatement)
    assert result.conclusion.group == TodaPrimaryGroup(12, 7)
    assert model.steps[model.root_index].rule is ProofRule.INFERENCE
    assert any(item.reference.locator == "Proposition 4.2 (4.4)"
               for item in model.citations)


def test_earlier_db_result_is_not_promoted_as_same_group_given() -> None:
    from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step

    prior = exact_prior_database_result(6, 5)
    assert prior is not None
    assert admitted_db_step(prior, proof_target=prior) is None
    from homotopy_groups import TodaPrimaryGroupZeroStatement, TodaPrimaryGroup
    later = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    adopted = admitted_db_step(prior, proof_target=later)
    assert adopted is not None
    assert adopted.rule is ProofRule.GIVEN
    assert adopted.conclusion == prior

```

## `tests/test_installer.py` 全文

```python
"""Reviewed patch scope, idempotence, fail-closed guards, and syntax tests."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r56_cyclic_generator_bridge.install import (
    PINNED_SHA,
    PROVIDER_AFTER,
    PROVIDER_BEFORE,
    SHARED_SEARCH_AFTER,
    SHARED_SEARCH_BEFORE,
    _git_blob,
    _normalize,
    _replace_once,
    patch_shared,
)


def _fixture_source() -> str:
    return (
        "def shared_expansion_provider():\n"
        + PROVIDER_BEFORE
        + "    return extra_providers\n\n"
        + "def search_shared_group_goal():\n"
        + SHARED_SEARCH_BEFORE
        + "    )\n"
    )


def test_common_patch_adds_both_rules_and_nonzero_source_bound_provider() -> None:
    updated = patch_shared(_fixture_source())
    ast.parse(updated)
    assert "expand_cyclic_generator_from_hopf" in updated
    assert "expand_delta_surjectivity_from_generator" in updated
    assert "build_public_source_bound_kernel_provider" in updated
    assert updated.count("expand_upper_delta_surjectivity") == 1


def test_patch_rejects_missing_or_repeated_anchor() -> None:
    with pytest.raises(RuntimeError):
        patch_shared("def nothing():\n    return None\n")
    with pytest.raises(RuntimeError):
        _replace_once("same same", "same", "new", "duplicate")


def test_file_eol_preserved_with_no_sha_normalization() -> None:
    raw = b"first\r\nsecond\r\n"
    content, bom, style = _normalize(raw)
    assert content == "first\nsecond\n"
    assert bom == b""
    assert style == "\r\n"
    assert _git_blob(raw) != _git_blob(raw.replace(b"\r\n", b"\n"))
    assert len(PINNED_SHA) == 40


def test_no_group_specific_narrative_or_direct_given_added() -> None:
    root = Path(__file__).resolve().parents[1]
    source = (root / "rule.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert "ProofRule.GIVEN" in source
    assert "GIVEN" not in {x.id for x in ast.walk(tree) if isinstance(x, ast.Name)}
    assert "render_" not in source
    assert "n == 6" not in source
    assert "k == 5" not in source
    assert "ProofStep(" not in source


def test_only_shared_provider_is_existing_production_patch_target() -> None:
    root = Path(__file__).resolve().parents[1]
    installer = (root / "install.py").read_text(encoding="utf-8")
    assert 'SHARED = "phase165_r52_r9_shared_math.py"' in installer
    assert "git reset" not in installer
    assert "git checkout" not in installer

```

## `run.ps1` 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r56_cyclic_generator_bridge.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R56 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R56_DRYRUN=PASS'
        Write-Output '(END)'
        exit 0
    }

    python -B -m phase174_r3_r7_r56_cyclic_generator_bridge.install
    if ($LASTEXITCODE -ne 0) { throw 'R56 shared rule connection failed' }

    $Tests = @(
        '.\phase174_r3_r7_r56_cyclic_generator_bridge\tests\test_installer.py',
        '.\phase174_r3_r7_r56_cyclic_generator_bridge\tests\test_rule.py',
        '.\phase174_r3_r7_r37_upper_delta_surjectivity_isolated\tests\test_rule.py',
        '.\phase174_r3_r7_r35_isolated_cyclic_delta_kernel\tests\test_rule.py',
        '.\phase174_r3_r7_r56_cyclic_generator_bridge\tests\test_public.py'
    )
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Tests
    if ($LASTEXITCODE -ne 0) { throw 'R56 focused pytest failed' }

    python -B -m phase174_r3_r7_r56_cyclic_generator_bridge.audit
    if ($LASTEXITCODE -ne 0) { throw 'R56 public proof certification failed' }

    Write-Output 'PHASE174_R56_FOCUSED_TESTS=PASS'
    Write-Output 'PHASE174_R56_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}

```


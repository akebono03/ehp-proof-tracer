# Phase 171 R2J-R2 — 新規コード全文

既存 `shared_expansion_provider()` の変更後全文と import 全文は適用時 `output/CHANGED_CODE_FULL_JA.md` へ保存する。変更後のファイル全体は `output/phase165_r52_r9_shared_math.py.FULL` に保存する。

## source.py（全文）

```python
"""Source-bound cyclic-generator surjectivity, without recycled complete proofs.

The printed group theorem is specialized as an INFERENCE from a screened
fixed general statement.  H(x)=g is separately reconstructed from its own
cited premises; neither is admitted as a new GIVEN.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, IteratedSuspension, MapApplication, Suspension
from homotopy_groups import FiniteCyclicGroup, TodaHopfInvariantMap, TodaPrimaryGroup
from map_facts import EHP_H_MAP
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase168_r2_8_4_generic_specialization.specialization import specialize_registered_higher_stem
from phase171_r2i_eta_hopf_bridge.source import eligible_eta_hopf_chains
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


def _coordinates(value: object) -> tuple[int, int] | None:
    """Return (source, target) of a well-typed concrete homotopy element."""
    if isinstance(value, HomotopyElement):
        s, t = value.source, value.target
        if (type(s) is int and type(t) is int
                and type(value.dimension) is int
                and value.dimension == t and s >= t >= 2):
            return s, t
        return None
    if isinstance(value, Composition):
        left = _coordinates(value.left)
        right = _coordinates(value.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return right[0], left[1]
    if isinstance(value, Suspension):
        inner = _coordinates(value.expression)
        return None if inner is None else (inner[0] + 1, inner[1] + 1)
    if isinstance(value, IteratedSuspension):
        inner = _coordinates(value.expression)
        k = value.exponent
        return (inner[0] + k, inner[1] + k) if inner is not None and type(k) is int and k >= 0 else None
    return None


def _same_generator(left: object, right: object, order: int) -> bool:
    """Use exact typed equality or the pre-existing, ID-checked name alias."""
    if left == right:
        return True
    if type(order) is not int or order <= 1:
        return False
    return same_registered_group_presentation(
        FiniteCyclicGroup(order, left), FiniteCyclicGroup(order, right),
    )


def _eligible_group_instance(source: object, group: Relation) -> bool:
    """Recognize one existing positioned higher-stem group theorem.

    The general source provides the mathematics. HyoujiGen supplies only
    the spelling/degree identity of its concrete named generator.
    """
    if (not isinstance(source, Relation)
            or not isinstance(group, Relation)
            or group.relation_type is not RelationType.EQUALITY
            or not isinstance(group.lhs, TodaPrimaryGroup)
            or not isinstance(group.rhs, FiniteCyclicGroup)):
        return False
    n = group.lhs.sphere_dimension
    if type(n) is not int:
        return False
    specialized = specialize_registered_higher_stem(source, n)
    return (specialized is not None
            and specialized == group
            and type(group.rhs.order) is int
            and group.rhs.order > 1)


def cyclic_group_from_cited_general_rule(goal: Relation, source: Relation) -> InferenceRule:
    """Specialize the screened general fixed theorem, never the DB result."""
    if not _eligible_group_instance(source, goal):
        raise ValueError("source does not specialize to this typed cyclic group")

    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].rule is ProofRule.GIVEN
                and premises[0].conclusion == source
                and _eligible_group_instance(source, goal))

    return InferenceRule(
        name="specialize earlier cited cyclic group schema",
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=Relation,
            relation_type=RelationType.EQUALITY,
        ),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def _valid_surjective_pair(
    goal: MapSurjective, group: Relation, image: Relation,
) -> bool:
    """Check the exact H-domain, codomain and generating image."""
    if not isinstance(goal, MapSurjective) or not isinstance(goal.map, TodaHopfInvariantMap):
        return False
    mapping = goal.map
    if (not isinstance(mapping.source_group, TodaPrimaryGroup)
            or not isinstance(mapping.target_group, TodaPrimaryGroup)
            or not isinstance(group, Relation)
            or group.relation_type is not RelationType.EQUALITY
            or group.lhs != mapping.target_group
            or not isinstance(group.rhs, FiniteCyclicGroup)
            or type(group.rhs.order) is not int or group.rhs.order <= 1
            or not isinstance(image, Relation)
            or image.relation_type is not RelationType.EQUALITY
            or not isinstance(image.lhs, MapApplication)
            or image.lhs.map != EHP_H_MAP):
        return False
    src = _coordinates(image.lhs.expression)
    dst = _coordinates(image.rhs)
    generator = _coordinates(group.rhs.generator)
    if src is None or dst is None or generator is None:
        return False
    q, n = src
    if (q < n or mapping.source_group != TodaPrimaryGroup(q, n)
            or mapping.target_group != TodaPrimaryGroup(q, 2 * n - 1)
            or dst != (q, 2 * n - 1)
            or generator != dst):
        return False
    return _same_generator(group.rhs.generator, image.rhs, group.rhs.order)


def cyclic_generator_image_surjectivity_rule(
    goal: MapSurjective, group: Relation, image: Relation,
) -> InferenceRule:
    """A homomorphism hitting a certified cyclic generator is surjective."""
    if not _valid_surjective_pair(goal, group, image):
        raise ValueError("cyclic group and Hopf generator image do not match")

    def guard(premises, bindings):
        return (len(premises) == 2
                and all(step.rule is ProofRule.INFERENCE for step in premises)
                and premises[0].conclusion == group
                and premises[1].conclusion == image
                and _valid_surjective_pair(goal, group, image))

    return InferenceRule(
        name="cyclic codomain generator in image implies Hopf surjectivity",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=Relation,
                           relation_type=RelationType.EQUALITY),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=Relation,
                           relation_type=RelationType.EQUALITY),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_cyclic_hopf_surjectivity(
    goal: object, available: tuple[object, ...], *, proof_target: object = None,
) -> tuple[GoalExpansion, ...]:
    """Propose only backed-up group specializations and R2I Hopf chains.

    Do not duplicate the group root's independent existing proof search.
    In subgoals of another proof, the specialized group schema remains a
    separate inference obligation; it is never inserted as a GIVEN.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    sources = tuple(value for value in available if isinstance(value, Relation))
    if isinstance(goal, Relation):
        if proof_target is None or goal == proof_target:
            return ()
        proposals = []
        for source in sources:
            if _eligible_group_instance(source, goal):
                proposals.append(GoalExpansion(
                    cyclic_group_from_cited_general_rule(goal, source),
                    (source,),
                ))
        return tuple(proposals)
    if not isinstance(goal, MapSurjective) or not isinstance(goal.map, TodaHopfInvariantMap):
        return ()
    proposals = []
    for chain in eligible_eta_hopf_chains(available):
        for source in sources:
            target = goal.map.target_group
            if not isinstance(target, TodaPrimaryGroup):
                continue
            n = target.sphere_dimension
            if type(n) is not int:
                continue
            group = specialize_registered_higher_stem(source, n)
            if group is None or not _valid_surjective_pair(goal, group, chain.conclusion):
                continue
            candidate = GoalExpansion(
                cyclic_generator_image_surjectivity_rule(goal, group, chain.conclusion),
                (group, chain.conclusion),
            )
            if not any(x.subgoals == candidate.subgoals for x in proposals):
                proposals.append(candidate)
    return tuple(proposals)

```

## audit.py（全文）

```python
"""R2J-R2: prove H surjective from a cited cyclic group generator image.

R2I is reconstructed inside this proof, not imported as a completed proof
or inserted as a leaf. This audit does not assert Delta=0 or pi_6^3.
"""
from __future__ import annotations

import json
from pathlib import Path

from expression import Composition, MapApplication
from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
from map_facts import EHP_H_MAP
from phase165_r12_r20_eta_definition import expand_cited_eta_definition
from phase165_r12_r21_eta_generator_chain import expand_cited_eta_generator
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase166_r3c_publication_order import precedes_citing_assertion
from phase168_r2_8_4_generic_specialization.specialization import specialize_registered_higher_stem
from phase171_r2h_prop22_cited_hopf.source import expand_cited_prop22_right_formula
from phase171_r2i_eta_hopf_bridge.audit import _available, _checked_chain, _screened_context
from phase171_r2i_eta_hopf_bridge.source import expand_cited_eta_hopf_power
from phase171_r2j_r2_cyclic_hopf_surjective.source import (
    _valid_surjective_pair,
    expand_cited_cyclic_hopf_surjectivity,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin

OUTPUT = Path(__file__).resolve().parent / "output"
SOURCE = Path(__file__).resolve().parent.parent / "sources" / "toda" / "Toda_05_2.tex"


def _verify_adopted_prop53_text() -> None:
    """Check the reviewed transcription; do not claim original-edition verification."""
    text = SOURCE.read_text(encoding="utf-8-sig")
    begin = text.find(r"\begin{proposition}\label{prop:5.3}")
    end = text.find(r"\end{proposition}", begin)
    if begin < 0 or end <= begin:
        raise RuntimeError("adopted Proposition 5.3 source block missing")
    clause = text[begin:end]
    if any(piece not in clause for piece in (
        r"\pi^{n}_{n+2}", r"\eta_n^{2}", r"\mathbb Z_2", r"n\ge2",
    )):
        raise RuntimeError("adopted Proposition 5.3 theorem text is incomplete")


def _scoped_provider(available: tuple[object, ...], goal: MapSurjective):
    """Exact known obligations; no historical completed-proof import."""
    def expand(current: object):
        return (
            expand_cited_cyclic_hopf_surjectivity(
                current, available, proof_target=goal,
            )
            + expand_cited_eta_hopf_power(current, available)
            + expand_cited_prop22_right_formula(current, available)
            + expand_cited_eta_definition(current, available)
            + expand_cited_eta_generator(current)
        )
    return expand


def build_cited_r2j_r2_proof():
    """Reconstruct the proof tree from four screened, earlier cited leaves."""
    _verify_adopted_prop53_text()
    screened, group_goal, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    hopf = TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    )
    goal = MapSurjective(hopf)
    expected_image = chain.conclusion
    if (expected_image.lhs != MapApplication(
            EHP_H_MAP, Composition(chain.alpha, chain.eta_next),
        ) or not isinstance(expected_image.rhs, Composition)):
        raise RuntimeError("R2I Hopf image has the wrong type")
    proposals = expand_cited_cyclic_hopf_surjectivity(
        goal, available, proof_target=group_goal,
    )
    if len(proposals) != 1 or proposals[0].subgoals[1] != expected_image:
        raise RuntimeError("generator-in-image proposal not uniquely screened")
    prior_group = proposals[0].subgoals[0]
    if not _valid_surjective_pair(goal, prior_group, expected_image):
        raise RuntimeError("cyclic generator/element identity mismatch")
    source_links = []
    for link in screened.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        if not isinstance(link.step.conclusion, Relation):
            continue
        specialized = specialize_registered_higher_stem(
            link.step.conclusion, 5,
        )
        if specialized != prior_group:
            continue
        assertion = screened.registry.assertion(link.assertion_id)
        ref = screened.registry.reference(assertion.reference_id)
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or ref.locator != "Proposition 5.3"
                or not precedes_citing_assertion(
                    screened, link.assertion_id, citing,
                )):
            raise RuntimeError("Proposition 5.3 is not an earlier fixed source")
        source_links.append(link)
    if len(source_links) != 1:
        raise RuntimeError("exactly one screened Proposition 5.3 source required")
    public_options = shared_expansion_provider(
        screened, proof_target=group_goal,
    )(goal)
    if not any(
        option.subgoals == proposals[0].subgoals
        and option.rule.name == proposals[0].rule.name
        for option in public_options
    ):
        raise RuntimeError("R2J rule not connected to shared provider")
    proof = reconstruct_registered_goal(
        goal, screened, citing, _scoped_provider(available, goal),
        lookup_mode="typed_reference_publication",
    )
    if (proof.rule is not ProofRule.INFERENCE
            or proof.conclusion != goal
            or len(proof.premises) != 2
            or any(p.rule is not ProofRule.INFERENCE for p in proof.premises)
            or proof.premises[0].conclusion != prior_group
            or proof.premises[1].conclusion != expected_image):
        raise RuntimeError("H surjectivity was not reconstructed from two inferences")
    nodes = []
    seen = set()

    def visit(step):
        if id(step) in seen:
            return
        seen.add(id(step))
        nodes.append(step)
        for parent in step.premises:
            visit(parent)

    visit(proof)
    leaves = [step for step in nodes if step.rule is ProofRule.GIVEN]
    sources = tuple(link.step.conclusion for link in screened.proof_links
                    if link.step is not None and link.step.rule is ProofRule.GIVEN)
    if (len(leaves) != 4
            or any(leaf.premises for leaf in leaves)
            or any(leaf.conclusion not in sources for leaf in leaves)
            or sum(leaf.conclusion == source_links[0].step.conclusion
                   for leaf in leaves) != 1):
        raise RuntimeError("unexpected or fabricated GIVEN in H surjectivity proof")
    if any(step.conclusion == group_goal for step in nodes):
        raise RuntimeError("pi_6^3 group structure improperly inserted")
    if any(step.rule is ProofRule.GIVEN
           and step.conclusion in (prior_group, expected_image, goal)
           for step in nodes):
        raise RuntimeError("derived group/Hopf/map fact promoted to GIVEN")
    return proof, prior_group, chain, tuple(nodes), source_links[0]


def run() -> None:
    proof, group, chain, nodes, link = build_cited_r2j_r2_proof()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = {
        "result": "PASS_CITED_H_SURJECTIVE_ONLY",
        "hopf_map": repr(proof.conclusion.map),
        "group": repr(group),
        "r2i_image": repr(chain.conclusion),
        "prop53_assertion_id": link.assertion_id,
        "inferences": sum(step.rule is ProofRule.INFERENCE for step in nodes),
        "given_leaves": sum(step.rule is ProofRule.GIVEN for step in nodes),
        "given_conclusions": [repr(step.conclusion) for step in nodes
                              if step.rule is ProofRule.GIVEN],
        "delta_zero_proven": False,
        "pi63_proven": False,
        "adopted_prop53_text_matched": True,
        "original_edition_verified": False,
        "registration_status_not_upgraded": True,
        "full_pytest": False,
    }
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R2J_R2_PROP53_SPECIALIZATION=PASS", flush=True)
    print("PHASE171_R2J_R2_R2I_INFERRED_ANCESTRY=PASS", flush=True)
    print("PHASE171_R2J_R2_CYCLIC_GENERATOR_IN_IMAGE=PASS", flush=True)
    print("PHASE171_R2J_R2_H_SURJECTIVE=PASS", flush=True)
    print("PHASE171_R2J_R2_GIVEN_LEAVES=" + str(report["given_leaves"]), flush=True)
    print("PHASE171_R2J_R2_INFERENCES=" + str(report["inferences"]), flush=True)
    print("PHASE171_R2J_R2_DELTA_ZERO_PROVEN=False", flush=True)
    print("PHASE171_R2J_R2_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R2_RESULT=PASS_CITED_H_SURJECTIVE_ONLY", flush=True)
    print("PHASE171_R2J_R2_REPORT=" + str(OUTPUT / "audit.json"), flush=True)


if __name__ == "__main__":
    run()

```

## tests/test_cited_cyclic_hopf.py（全文）

```python
"""R2J-R2 regression: valid cited derivation and rejected counterfeit premises."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
from homotopy_groups import FiniteCyclicGroup, TodaHopfInvariantMap, TodaPrimaryGroup
from map_facts import EHP_H_MAP
from phase165_r14_r6_generic_iso import MapSurjective
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase171_r2i_eta_hopf_bridge.audit import _available, _checked_chain, _screened_context
from phase171_r2j_r2_cyclic_hopf_surjective.audit import build_cited_r2j_r2_proof
from phase171_r2j_r2_cyclic_hopf_surjective.source import (
    _coordinates,
    _eligible_group_instance,
    _valid_surjective_pair,
    cyclic_generator_image_surjectivity_rule,
    cyclic_group_from_cited_general_rule,
    expand_cited_cyclic_hopf_surjectivity,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def _case():
    screened, group_goal, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    goal = MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    ))
    return chain, available, group_goal, goal


def test_cited_proof_of_h_surjectivity_contains_both_inferred_premises():
    proof, group, chain, nodes, source_link = build_cited_r2j_r2_proof()
    assert proof.rule is ProofRule.INFERENCE
    assert len(proof.premises) == 2
    assert all(step.rule is ProofRule.INFERENCE for step in proof.premises)
    assert proof.premises[0].conclusion == group
    assert proof.premises[1].conclusion == chain.conclusion
    assert sum(step.rule is ProofRule.GIVEN for step in nodes) == 4
    assert sum(step.conclusion == source_link.step.conclusion
               for step in nodes if step.rule is ProofRule.GIVEN) == 1


def test_cyclic_group_specialization_requires_screened_general_statement():
    chain, available, root, goal = _case()
    offered = expand_cited_cyclic_hopf_surjectivity(goal, available, proof_target=root)
    assert len(offered) == 1
    group = offered[0].subgoals[0]
    assert _valid_surjective_pair(goal, group, chain.conclusion)
    group_options = expand_cited_cyclic_hopf_surjectivity(group, available, proof_target=root)
    assert len(group_options) == 1
    assert group_options[0].subgoals[0] in available
    assert _eligible_group_instance(group_options[0].subgoals[0], group)
    assert expand_cited_cyclic_hopf_surjectivity(group, available, proof_target=group) == ()
    assert expand_cited_cyclic_hopf_surjectivity(goal, (), proof_target=root) == ()


def test_rejects_wrong_hopf_degree_and_wrong_generator():
    chain, available, root, goal = _case()
    group = expand_cited_cyclic_hopf_surjectivity(goal, available, proof_target=root)[0].subgoals[0]
    bad_map = MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 6),
    ))
    assert not _valid_surjective_pair(bad_map, group, chain.conclusion)
    assert expand_cited_cyclic_hopf_surjectivity(bad_map, available, proof_target=root) == ()
    unrelated = HomotopyElement(
        "η₇", 7, source=8, target=7, generator=GeneratorSymbol("η", index=7),
    )
    bad_group = replace(group, rhs=FiniteCyclicGroup(2, unrelated))
    assert not _valid_surjective_pair(goal, bad_group, chain.conclusion)
    assert _coordinates(Composition(chain.alpha, chain.eta_next)) == (7, 3)
    assert _coordinates(Composition(chain.beta, chain.eta_next)) == (7, 5)


def test_rejects_forged_given_group_or_hopf_result():
    chain, available, root, goal = _case()
    group = expand_cited_cyclic_hopf_surjectivity(goal, available, proof_target=root)[0].subgoals[0]
    rule = cyclic_generator_image_surjectivity_rule(goal, group, chain.conclusion)
    forged_group = ProofStep(group, (), ProofRule.GIVEN)
    forged_image = ProofStep(chain.conclusion, (), ProofRule.GIVEN)
    assert find_inference_matches_for_rule(rule, (forged_group, forged_image)) == ()
    source = expand_cited_cyclic_hopf_surjectivity(group, available, proof_target=root)[0].subgoals[0]
    group_rule = cyclic_group_from_cited_general_rule(group, source)
    assert find_inference_matches_for_rule(
        group_rule, (ProofStep(source, (), ProofRule.INFERENCE),)
    ) == ()


def test_cited_generator_alias_is_typed_not_textual():
    chain, available, root, goal = _case()
    group = expand_cited_cyclic_hopf_surjectivity(goal, available, proof_target=root)[0].subgoals[0]
    assert group.rhs.generator != chain.conclusion.rhs or _valid_surjective_pair(
        goal, group, chain.conclusion,
    )
    assert same_registered_group_presentation(
        FiniteCyclicGroup(2, group.rhs.generator),
        FiniteCyclicGroup(2, chain.conclusion.rhs),
    )
    wrong = replace(chain.eta_next, source=80)
    false_image = Relation(
        MapApplication(EHP_H_MAP, Composition(chain.alpha, wrong)),
        chain.conclusion.rhs, RelationType.EQUALITY,
    )
    assert not _valid_surjective_pair(goal, group, false_image)


def test_without_cited_prop53_or_r2i_sources_cannot_propose_surjectivity():
    chain, available, root, goal = _case()
    offered = expand_cited_cyclic_hopf_surjectivity(goal, available, proof_target=root)
    assert len(offered) == 1
    group_source = expand_cited_cyclic_hopf_surjectivity(
        offered[0].subgoals[0], available, proof_target=root,
    )[0].subgoals[0]
    without_prop53 = tuple(item for item in available if item != group_source)
    assert expand_cited_cyclic_hopf_surjectivity(goal, without_prop53, proof_target=root) == ()
    hopf_source = Relation(MapApplication(EHP_H_MAP, chain.alpha), chain.beta, RelationType.EQUALITY)
    without_hopf = tuple(item for item in available if item != hopf_source)
    assert expand_cited_cyclic_hopf_surjectivity(goal, without_hopf, proof_target=root) == ()

```

## install.py（全文）

```python
"""Conservative R2J-R2 installer; preserves CRLF and unrelated changes."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
OUTPUT = HERE / "output"
BACKUP = OUTPUT / "phase165_r52_r9_shared_math.py.before_r2j_r2"
STATE = OUTPUT / "state.json"
HOOK = "expand_cited_cyclic_hopf_surjectivity"
ANCHOR = "        options.extend(expand_cited_eta_hopf_power(goal, tuple(available)))\n"
ADDITION = (
    "        from phase171_r2j_r2_cyclic_hopf_surjective.source import (\n"
    "            expand_cited_cyclic_hopf_surjectivity,\n"
    "        )\n"
    "        options.extend(expand_cited_cyclic_hopf_surjectivity(\n"
    "            goal, tuple(available), proof_target=proof_target,\n"
    "        ))\n"
)
EXPECTED_BASE_HEAD = "176766a70841853039b8efaac0a8661eac22686d"


def _git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args,
        cwd=ROOT, check=True, capture_output=True,
        encoding="utf-8", errors="replace",
    ).stdout.strip()


def _digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def _render_source_with_hook(original: bytes) -> bytes:
    raw = original.decode("utf-8-sig")
    normalized = raw.replace("\r\n", "\n")
    if normalized.count(ANCHOR) != 1:
        raise RuntimeError("R2I shared hook not found exactly once")
    if HOOK in normalized:
        raise RuntimeError("R2J-R2 hook already present")
    modified = normalized.replace(ANCHOR, ANCHOR + ADDITION)
    ast.parse(modified)
    eol = "\r\n" if b"\r\n" in original else "\n"
    return (b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b"") + modified.replace("\n", eol).encode("utf-8")


def _full_function(source: str, function: str) -> str:
    tree = ast.parse(source)
    found = [node for node in tree.body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
             and node.name == function]
    if len(found) != 1:
        raise RuntimeError("changed full function not uniquely found: " + function)
    lines = source.splitlines()
    node = found[0]
    return "\n".join(lines[node.lineno - 1:node.end_lineno]) + "\n"


def _changed_code_document(shared: str) -> str:
    source = (HERE / "source.py").read_text(encoding="utf-8")
    audit = (HERE / "audit.py").read_text(encoding="utf-8")
    tests = (HERE / "tests" / "test_cited_cyclic_hopf.py").read_text(encoding="utf-8")
    import_part = shared[:shared.index("def build_shared_typed_bridge(")]
    return (
        "# Phase 171 R2J-R2 変更コード全文\n\n"
        "## 変更対象\n\n"
        "- 既存ファイル `phase165_r52_r9_shared_math.py`\n"
        "- 関数 `shared_expansion_provider`（全体を以下に提示）\n"
        "- 追加位置：R2I `expand_cited_eta_hopf_power` の直後\n"
        "- 新規 `phase171_r2j_r2_cyclic_hopf_surjective/source.py`（全文）\n"
        "- 新規 `audit.py`（全文）と `tests/test_cited_cyclic_hopf.py`（全文）\n"
        "- 既存ファイルのトップレベル import 変更なし\n\n"
        "## 既存ファイル import 全文（モジュールドキュメントも含む）\n\n```python\n"
        + import_part + "```\n\n"
        "## `shared_expansion_provider` 関数全文\n\n```python\n"
        + _full_function(shared, "shared_expansion_provider") + "```\n\n"
        "## 新規 source.py 全文\n\n```python\n" + source + "\n```\n\n"
        "## 新規 audit.py 全文\n\n```python\n" + audit + "\n```\n\n"
        "## 新規テスト全文\n\n```python\n" + tests + "\n```\n"
    )


def preflight() -> tuple[bytes, bool]:
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    print("PHASE171_R2J_R2_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R2_HEAD=" + head, flush=True)
    if branch != "develop":
        raise RuntimeError("develop branch required; checkout/reset forbidden")
    if not TARGET.is_file():
        raise RuntimeError("shared production module missing")
    raw = TARGET.read_bytes()
    normalized = raw.decode("utf-8-sig").replace("\r\n", "\n")
    installed = HOOK in normalized
    if not installed and head != EXPECTED_BASE_HEAD:
        raise RuntimeError("unexpected HEAD; re-audit GitHub before applying")
    if not installed and _git("diff", "--", str(TARGET.relative_to(ROOT))):
        raise RuntimeError("existing tracked edit to shared module: preserve and audit first")
    if normalized.count(ANCHOR) != 1:
        raise RuntimeError("R2I hook missing or changed")
    if installed and normalized.count(HOOK) != 2:
        raise RuntimeError("incomplete or ambiguous R2J-R2 installation")
    if not installed:
        _render_source_with_hook(raw)
    print("PHASE171_R2J_R2_R2I_PRESERVED=PASS", flush=True)
    print("PHASE171_R2J_R2_PREFLIGHT=PASS", flush=True)
    print("PHASE171_R2J_R2_ALREADY_INSTALLED=" + str(installed), flush=True)
    return raw, installed


def apply(dry_run: bool) -> None:
    raw, installed = preflight()
    if dry_run:
        print("PHASE171_R2J_R2_RESULT=PASS_DRY_RUN", flush=True)
        return
    if installed:
        print("PHASE171_R2J_R2_RESULT=PASS_ALREADY_APPLIED", flush=True)
        return
    altered = _render_source_with_hook(raw)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if BACKUP.exists() or STATE.exists():
        raise RuntimeError("existing installer backup/state: review before applying")
    BACKUP.write_bytes(raw)
    try:
        TARGET.write_bytes(altered)
        edited_text = altered.decode("utf-8-sig").replace("\r\n", "\n")
        (OUTPUT / "phase165_r52_r9_shared_math.py.FULL").write_bytes(altered)
        (OUTPUT / "CHANGED_CODE_FULL_JA.md").write_text(
            _changed_code_document(edited_text), encoding="utf-8",
        )
        STATE.write_text(json.dumps({
            "before_sha256": _digest(raw),
            "after_sha256": _digest(altered),
        }, indent=2) + "\n", encoding="utf-8")
    except Exception:
        if TARGET.read_bytes() == altered:
            TARGET.write_bytes(raw)
        raise
    print("PHASE171_R2J_R2_PATCHED=" + TARGET.name, flush=True)
    print("PHASE171_R2J_R2_BACKUP=" + str(BACKUP), flush=True)
    print("PHASE171_R2J_R2_CHANGED_CODE=" + str(OUTPUT / "CHANGED_CODE_FULL_JA.md"), flush=True)
    print("PHASE171_R2J_R2_RESULT=PASS_APPLY", flush=True)


def restore() -> None:
    if not BACKUP.is_file() or not STATE.is_file():
        raise RuntimeError("no verified R2J-R2 backup")
    record = json.loads(STATE.read_text(encoding="utf-8"))
    original = BACKUP.read_bytes()
    if _digest(original) != record["before_sha256"]:
        raise RuntimeError("backup hash changed")
    if _digest(TARGET.read_bytes()) != record["after_sha256"]:
        raise RuntimeError("target has changed; refusing unsafe restore")
    TARGET.write_bytes(original)
    STATE.unlink()
    print("PHASE171_R2J_R2_RESULT=PASS_RESTORE", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--dry-run", action="store_true")
    actions.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    if args.restore:
        restore()
    else:
        apply(args.dry_run)


if __name__ == "__main__":
    main()

```

## run.ps1（全文）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $Root
try {
    if ($DryRun) {
        & python ".\phase171_r2j_r2_cyclic_hopf_surjective\install.py" --dry-run
        if ($LASTEXITCODE -ne 0) { throw "R2J-R2 DryRun preflight failed" }
        Write-Output "PHASE171_R2J_R2_RUN=PASS_DRY_RUN"
        return
    }
    & python ".\phase171_r2j_r2_cyclic_hopf_surjective\install.py" --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R2J-R2 initial preflight failed" }
    $Target = Join-Path $Root "phase165_r52_r9_shared_math.py"
    $wasInstalled = [bool](Select-String -Path $Target -Pattern "expand_cited_cyclic_hopf_surjectivity" -Quiet)
    & python ".\phase171_r2j_r2_cyclic_hopf_surjective\install.py"
    if ($LASTEXITCODE -ne 0) { throw "R2J-R2 patch failed" }
    try {
        & python -m pytest -q `
            ".\phase171_r2j_r2_cyclic_hopf_surjective\tests\test_cited_cyclic_hopf.py" `
            ".\phase171_r2i_eta_hopf_bridge\tests\test_cited_eta_hopf.py"
        if ($LASTEXITCODE -ne 0) { throw "R2J-R2 focused pytest failed" }
        Write-Output "PHASE171_R2J_R2_FOCUSED_PYTEST=PASS"
        & python -m phase171_r2j_r2_cyclic_hopf_surjective.audit
        if ($LASTEXITCODE -ne 0) { throw "R2J-R2 proof ancestry audit failed" }
    } catch {
        if (-not $wasInstalled) {
            & python ".\phase171_r2j_r2_cyclic_hopf_surjective\install.py" --restore
            if ($LASTEXITCODE -ne 0) { throw "R2J-R2 failed AND automatic restore failed; inspect original backup" }
        }
        throw
    }
    Write-Output "PHASE171_R2J_R2_RUN=PASS"
} finally {
    Pop-Location
}

```


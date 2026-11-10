# R57R3 コード全文

## 変更対象の一覧

- `phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py`：既存 `test_missing_or_wrong_group_generator_blocks_surjectivity()` の関数全体を置換。既存 import は変更しない。
- `phase174_r3_r7_r57_narrative_source_cleanup/install.py`：定数 `NEW_TEST3` と `AFTER_SHA256` のテスト用ピンを置換。既存 import、クラス、関数の変更はない。

R57R3 インストーラーはこれらの変更後のファイル全文を Source Guard 付きで安全に配置する。下記は変更後のファイル全文で、コード内に省略記号は使用していない。

## R56 テストファイル全文（変更後）

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
def test_generator_relation_alone_proves_delta_surjectivity(n: int) -> None:
    theorem = typed_specialization(n)
    goal = MapSurjective(theorem.delta)
    required = delta_surjectivity_generator_inputs(goal)
    assert required == (_goal(n),)
    proposals = expand_delta_surjectivity_from_generator(goal)
    assert len(proposals) == 1
    assert proposals[0].rule.name == SURJECTIVE_RULE_NAME
    assert proposals[0].subgoals == required
    for proof_kind in (ProofRule.GIVEN, ProofRule.INFERENCE):
        facts = (_test_step(required[0], proof_kind),)
        matches = find_inference_matches_for_rule(
            delta_surjectivity_from_generator_rule(goal), facts
        )
        assert len(matches) == 1
        assert apply_inference_match(matches[0]).conclusion == goal

def test_prior_relation_needs_no_prop27_reproof() -> None:
    goal = MapSurjective(typed_specialization(6).delta)
    relation, = delta_surjectivity_generator_inputs(goal)
    facts = (_test_step(relation, ProofRule.GIVEN),)
    assert len(find_inference_matches_for_rule(
        delta_surjectivity_from_generator_rule(goal), facts
    )) == 1
    assert all(type(x) is Relation for x in delta_surjectivity_generator_inputs(goal))

def test_missing_or_wrong_group_generator_blocks_surjectivity() -> None:
    theorem = typed_specialization(6)
    goal = MapSurjective(theorem.delta)
    relation, = delta_surjectivity_generator_inputs(goal)
    wrong = Relation(relation.lhs, FreeCyclicGroup(
        replace(relation.rhs.generator, name="Delta of wrong identity")
    ))
    rule = delta_surjectivity_from_generator_rule(goal)
    assert find_inference_matches_for_rule(rule, ()) == ()
    assert find_inference_matches_for_rule(rule, (_test_step(wrong),)) == ()
    assert find_inference_matches_for_rule(rule, (_test_step(theorem),)) == ()
    valid_relation = _test_step(relation)
    unrelated_theorem = _test_step(theorem)
    matches = find_inference_matches_for_rule(
        rule, (valid_relation, unrelated_theorem)
    )
    assert len(matches) == 1
    assert matches[0].premises == (valid_relation,)
    derived = apply_inference_match(matches[0])
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == goal
    assert derived.premises == (valid_relation,)

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

## R57 インストーラーファイル全文（変更後）

```python
"""R57 audited source-first correction of the R56 dependency and common display."""
from __future__ import annotations
import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
HEAD = '0a5be29a4458cdffaa8a7ad4ad31c2e91f6941f9'
PINS = {
    'phase168_r3_27_typed_statement_projection.py': '8dc8d676c8dbc401e0428fa57316d1b05caf2d49',
    'phase168_r3_5_model_renderer.py': '913a7030e209a689f58a5215013d3708140052e7',
    'phase168_r3_37c_reference_projection.py': '36f0b84857257b21b2573a7a77ef82d2baa6935d',
}
R56_RULE = 'phase174_r3_r7_r56_cyclic_generator_bridge/rule.py'
R56_TEST = 'phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py'
AFTER_SHA256 = {
    'phase174_r3_r7_r56_cyclic_generator_bridge/rule.py': 'f1bbcf7cc07d7221799d8d04e164366ec976d1a9b9c11cbf686097792aba86c2',
    'phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py': 'b13d03c5877d9b24d40a6c2e11d65120465f699b89f9719cde68586522c7b719',
}
LOCAL_SHA256 = {
    R56_RULE: '2dc98a014225a6a6df9e03b4894c290e279be2926ea2804337b6f1a85943826c',
    R56_TEST: 'c7e9df7894af23654e02aba264fe957655d5afe4fb3f3d166cf30b641e3dfa9a',
}

def git(*args: str, binary=False):
    p = subprocess.run(('git',)+args, cwd=ROOT, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError('git failed: '+' '.join(args)+' '+p.stderr.decode(errors='replace'))
    return p.stdout if binary else p.stdout.decode('utf-8', 'replace').strip()

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def normalize(raw: bytes):
    bom=b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''
    data=raw[len(bom):]
    if b'\r' in data.replace(b'\r\n',b''):
        raise RuntimeError('unexpected CR-only/mixed EOL')
    return data.decode('utf-8').replace('\r\n','\n'), bom, ('\r\n' if b'\r\n' in data else '\n')

def replace_once(s, old, new, label):
    if s.count(old)!=1:
        raise RuntimeError('unreviewed or ambiguous edit anchor: '+label+' count '+str(s.count(old)))
    return s.replace(old,new,1)

def replace_function(source: str, name: str, replacement: str) -> str:
    tree=ast.parse(source)
    found=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name==name]
    if len(found)!=1:
        raise RuntimeError('function not unique '+name)
    node=found[0]
    lines=source.splitlines(keepends=True)
    return ''.join(lines[:node.lineno-1])+replacement.rstrip()+'\n\n'+''.join(lines[node.end_lineno:]).lstrip('\n')

NEW_INPUTS='''def delta_surjectivity_generator_inputs(
    goal: object,
) -> tuple[Relation] | None:
    """A canonical typed Delta-identity generator is already a Delta image.

    A group presentation is an ordinary independently proved or admitted
    premise; Proposition 2.7 is NOT needed to establish this definitional
    image membership. No printed name can pass without matching the complete
    typed EHP Delta source, target and identity index.
    """
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
    )
'''
NEW_RULE='''def delta_surjectivity_from_generator_rule(goal: MapSurjective) -> InferenceRule:
    """A=<Delta(iota)> makes Delta onto; no Hopf-Delta formula is required.

    The group relation must be admitted as a prior DB statement or independently
    inferred by the proof search. A target-group DB entry cannot be assumed
    as its own proof; the existing admission gate controls all GIVEN steps.
    """
    required = delta_surjectivity_generator_inputs(goal)
    if required is None:
        raise ValueError("not an exact typed Delta cyclic surjectivity goal")

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and premises[0].conclusion == required[0]
            and delta_surjectivity_generator_inputs(goal) == required
        )

    return InferenceRule(
        name=SURJECTIVE_RULE_NAME,
        description=(
            "If the cyclic codomain is generated by the canonical typed "
            "Delta(identity), Delta is onto by the definition of its image. "
            "The source of the cyclic presentation is independently checked; "
            "the Proposition 2.7 Hopf-Delta formula is not a premise."
        ),
        premise_patterns=(
            PremisePattern(
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=required[0],
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )
'''

NEW_TEST1='''def test_generator_relation_alone_proves_delta_surjectivity(n: int) -> None:
    theorem = typed_specialization(n)
    goal = MapSurjective(theorem.delta)
    required = delta_surjectivity_generator_inputs(goal)
    assert required == (_goal(n),)
    proposals = expand_delta_surjectivity_from_generator(goal)
    assert len(proposals) == 1
    assert proposals[0].rule.name == SURJECTIVE_RULE_NAME
    assert proposals[0].subgoals == required
    for proof_kind in (ProofRule.GIVEN, ProofRule.INFERENCE):
        facts = (_test_step(required[0], proof_kind),)
        matches = find_inference_matches_for_rule(
            delta_surjectivity_from_generator_rule(goal), facts
        )
        assert len(matches) == 1
        assert apply_inference_match(matches[0]).conclusion == goal
'''
NEW_TEST2='''def test_prior_relation_needs_no_prop27_reproof() -> None:
    goal = MapSurjective(typed_specialization(6).delta)
    relation, = delta_surjectivity_generator_inputs(goal)
    facts = (_test_step(relation, ProofRule.GIVEN),)
    assert len(find_inference_matches_for_rule(
        delta_surjectivity_from_generator_rule(goal), facts
    )) == 1
    assert all(type(x) is Relation for x in delta_surjectivity_generator_inputs(goal))
'''
NEW_TEST3='''def test_missing_or_wrong_group_generator_blocks_surjectivity() -> None:
    theorem = typed_specialization(6)
    goal = MapSurjective(theorem.delta)
    relation, = delta_surjectivity_generator_inputs(goal)
    wrong = Relation(relation.lhs, FreeCyclicGroup(
        replace(relation.rhs.generator, name="Delta of wrong identity")
    ))
    rule = delta_surjectivity_from_generator_rule(goal)
    assert find_inference_matches_for_rule(rule, ()) == ()
    assert find_inference_matches_for_rule(rule, (_test_step(wrong),)) == ()
    assert find_inference_matches_for_rule(rule, (_test_step(theorem),)) == ()
    valid_relation = _test_step(relation)
    unrelated_theorem = _test_step(theorem)
    matches = find_inference_matches_for_rule(
        rule, (valid_relation, unrelated_theorem)
    )
    assert len(matches) == 1
    assert matches[0].premises == (valid_relation,)
    derived = apply_inference_match(matches[0])
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == goal
    assert derived.premises == (valid_relation,)
'''

def patch_rule(s):
    s=replace_function(s,'delta_surjectivity_generator_inputs',NEW_INPUTS)
    s=replace_function(s,'delta_surjectivity_from_generator_rule',NEW_RULE)
    s=replace_once(s,'an independently proved typed Hopf-Delta formula to establish surjectivity.',
                      'no additional Hopf-Delta premise to establish surjectivity.',
                      'rule module docstring')
    return s

def patch_test(s):
    s=replace_function(s,'test_generator_and_typed_delta_prove_surjectivity',NEW_TEST1)
    s=replace_function(s,'test_admitted_prior_relation_is_permitted_but_theorem_must_be_inferred',NEW_TEST2)
    s=replace_function(s,'test_unproved_or_mismatched_delta_witness_blocks_surjectivity',NEW_TEST3)
    return s

def patch_typed(s):
    old='''    if type(statement) is KernelMultipleStatement:
'''
    new=r'''    from map_property_rules import ImageZeroStatement
    if type(statement) is ImageZeroStatement:
        mapping = statement.map
        source = group_tex(getattr(mapping, "source_group", None))
        target = group_tex(getattr(mapping, "target_group", None))
        symbol = map_symbol_tex(mapping)
        if source is not None and target is not None and symbol is not None:
            return rf"${symbol}:{source}\\to {target}$ は零写像."
        return None
    if type(statement) is KernelMultipleStatement:
'''
    s=replace_once(s,old,new,'typed zero image')
    old='''                rf"{statement.multiple}\\mathbb{{Z}}\\{{{generator}\\}}$."
'''
    new='''                rf"\\mathbb{{Z}}\\{{{statement.multiple}{generator}\\}}$."
'''
    s=replace_once(s,old,new,'ker multiple equals generator')
    return s

RENDER_HELPER='''    def single_source_ancestor_numbers(step):
        """Cite only a unique verified GIVEN ancestor, not every tree source."""
        sources = set()
        pending = [step]
        seen = set()
        while pending:
            ancestor = pending.pop()
            if id(ancestor) in seen:
                continue
            seen.add(id(ancestor))
            if ancestor.rule is ProofRule.GIVEN:
                for idx, candidate in enumerate(model.steps):
                    if candidate is ancestor or candidate == ancestor:
                        sources.update(model.step_citation_numbers[idx])
                        break
            pending.extend(ancestor.premises)
        return tuple(sorted(sources)) if len(sources) == 1 else ()

'''
RENDER_SIGN='''        # -g=g in a verified order-two cyclic target; remove the redundant
        # sign only when its exact typed group structure is already proved.
        from toda_rules import TodaDeltaImageUpToSignStatement
        if isinstance(statement, TodaDeltaImageUpToSignStatement):
            from homotopy_groups import FiniteCyclicGroup
            target_order_two = any(
                isinstance(candidate.conclusion, Relation)
                and candidate.conclusion.relation_type is RelationType.EQUALITY
                and candidate.conclusion.lhs == statement.map.target_group
                and isinstance(candidate.conclusion.rhs, FiniteCyclicGroup)
                and candidate.conclusion.rhs.order == 2
                and candidate.conclusion.rhs.generator == statement.positive_value
                for candidate in model.steps
            )
            if target_order_two:
                from toda_proof_narrative_renderer import render_toda_expression_latex
                lhs = render_toda_expression_latex(statement.element)
                rhs = render_toda_expression_latex(statement.positive_value)
                sentence = rf"$\\Delta({lhs})={rhs}$."
'''

def patch_renderer(s):
    s=replace_once(s,'    if model.abstract_structure is not result.abstract_structure:\n',
                   RENDER_HELPER+'    if model.abstract_structure is not result.abstract_structure:\n',
                   'common source ancestor helper')
    s=replace_once(s,'        sentence = typed_sentence(step.conclusion, step)\n',
                   '        sentence = typed_sentence(step.conclusion, step)\n'+RENDER_SIGN,
                   'common sign normalization')
    before='''                    if eta_numbers:
                        source_tags = ", ".join(
                            f"[R{number}]" for number in eta_numbers
                        )
                        sentence = f"{source_tags}より, " + sentence
'''
    after=before+'''                    elif not sourced_numbers:
                        unique_source = single_source_ancestor_numbers(step)
                        if unique_source:
                            source_tags = ", ".join(
                                f"[R{number}]" for number in unique_source
                            )
                            sentence = f"{source_tags}より, " + sentence
'''
    return replace_once(s,before,after,'general unique source parent citation')

REFERENCE_HELPER='''            # Correct the source display when a previously checked adopted
            # printed equation is strictly stronger than its conservative
            # internal up-to-sign claim. This is a reference transcription,
            # never a new theorem or Narrative rule.
            from toda_rules import TodaDeltaImageUpToSignStatement
            if type(statement) is TodaDeltaImageUpToSignStatement:
                from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import (
                    checked_prior_statements,
                )
                from unified_statement_registry import AssertionOrigin
                cited = registry.reference(assertion.reference_id)
                if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                        and cited.locator == "(5.10)"
                        and statement == checked_prior_statements()[1]):
                    from toda_proof_narrative_renderer import render_toda_expression_latex
                    lhs = render_toda_expression_latex(statement.element)
                    rhs = render_toda_expression_latex(statement.positive_value)
                    sentence = rf"$\\Delta({lhs})={rhs}$."
'''

def patch_reference(s):
    return replace_once(s,'            sentence = _verified_source_sentence(statement)\n',
        '            sentence = _verified_source_sentence(statement)\n'+REFERENCE_HELPER,
        'printed (5.10) precise equality')

PATCHES={R56_RULE:patch_rule,R56_TEST:patch_test,
         'phase168_r3_27_typed_statement_projection.py':patch_typed,
         'phase168_r3_5_model_renderer.py':patch_renderer,
         'phase168_r3_37c_reference_projection.py':patch_reference}

def review(dry_run=False):
    if git('branch','--show-current') != 'develop':
        raise RuntimeError('develop branch required')
    if Path(git('rev-parse','--show-toplevel')).resolve()!=ROOT.resolve():
        raise RuntimeError('extract R57 directly into the repository root')
    # The reviewed base commit may be followed by R56's own release commit.
    # A descendant is allowed ONLY when every reviewed target blob and each
    # local R56 rule/test source still matches its independently pinned hash.
    lineage = subprocess.run(
        ('git', 'merge-base', '--is-ancestor', HEAD, 'HEAD'),
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if lineage.returncode != 0:
        raise RuntimeError('unreviewed HEAD lineage (R57 reviewed base not an ancestor): '
                           + lineage.stderr.decode('utf-8', 'replace'))
    if git('diff','--cached','--name-only'):
        raise RuntimeError('staged files require separate review')
    states={}
    for name,func in PATCHES.items():
        path=ROOT/name
        if not path.is_file():
            raise RuntimeError('required R56 or baseline file missing: '+name)
        data=path.read_bytes()
        content,bom,eol=normalize(data)
        if name in PINS:
            if git('rev-parse','HEAD:'+name)!=PINS[name]:
                raise RuntimeError('unreviewed committed blob: '+name)
            raw=git('show','HEAD:'+name,binary=True)
            baseline=normalize(raw)[0]
            intended=func(baseline)
            if content not in (baseline,intended):
                raise RuntimeError('unreviewed local edits: '+name)
            revised=intended
        else:
            current_hash=sha256(content.encode('utf-8'))
            if current_hash==LOCAL_SHA256[name]:
                revised=func(content)
            elif current_hash==AFTER_SHA256[name]:
                revised=content
            else:
                raise RuntimeError('R56 local rule/test differs from reviewed input: '+name)
        ast.parse(revised,filename=name)
        future=bom+revised.replace('\n',eol).encode('utf-8')
        states[name]=(data,future,revised)
    return states

def run(dry_run=False):
    states=review(dry_run)
    print('PHASE174_R57_SOURCE_GUARD=PASS')
    print('PHASE174_R57_NEW_GIVEN=0')
    print('PHASE174_R57_NEW_MATH_RULES=0')
    if dry_run:
        print('PHASE174_R57_GATE=PASS_PREFLIGHT_ONLY')
        return
    for name,(original,after,_) in states.items():
        (ROOT/name).write_bytes(after)
    output=PACKAGE/'output'
    output.mkdir(exist_ok=True)
    functions={
      R56_RULE:['delta_surjectivity_generator_inputs','delta_surjectivity_from_generator_rule'],
      R56_TEST:['test_generator_relation_alone_proves_delta_surjectivity','test_prior_relation_needs_no_prop27_reproof','test_missing_or_wrong_group_generator_blocks_surjectivity'],
      'phase168_r3_27_typed_statement_projection.py':['typed_sentence'],
      'phase168_r3_5_model_renderer.py':['render_model_backed_narrative_markdown'],
      'phase168_r3_37c_reference_projection.py':['project_reference_bodies'],
    }
    full=['# R57 変更後の関数全文','']
    for name,(_,_,source) in states.items():
        (output/(name.replace('/','__')+'.FULL.py')).write_text(source,encoding='utf-8')
        for function in functions[name]:
            tree=ast.parse(source)
            node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==function)
            body=''.join(source.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
            full += [f'## {name} — {function}','', '```python',body.rstrip(),'```','']
    (output/'CHANGED_FUNCTIONS_FULL_JA.md').write_text('\n'.join(full),encoding='utf-8')
    print('PHASE174_R57_CHANGED_FILES='+str(len(states)))
    print('PHASE174_R57_GATE=PASS_R57_REVIEWED_PATCH_APPLIED')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    opts=parser.parse_args()
    run(opts.dry_run)
    print('(END)')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
```

## R57R3 新規インストーラー全文

```python
"""R57R3: repair one outdated proof-matcher test and R57's reproducibility pin.

R57 switched Delta surjectivity to one required group-structure premise.
Unrelated available proof facts must not become a required premise or block
that inference. This package changes no mathematical rule or renderer.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TEST_NAME = 'phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py'
INSTALL_NAME = 'phase174_r3_r7_r57_narrative_source_cleanup/install.py'
TARGET_TEST = ROOT / TEST_NAME
TARGET_INSTALL = ROOT / INSTALL_NAME
REVIEWED_BASE = '0a5be29a4458cdffaa8a7ad4ad31c2e91f6941f9'

BEFORE_TEST_SHA = '8dbc5a52f3c4c57ca2b3f5cc8750112fb86cc4ca4fa9a521fbbb74aa29e48fab'
AFTER_TEST_SHA = 'b13d03c5877d9b24d40a6c2e11d65120465f699b89f9719cde68586522c7b719'
BEFORE_INSTALL_SHA = '5cea9f784ba727d177fcbfdf07c5a10329825d2a33cbac8eb37a7d1c726af11b'
AFTER_INSTALL_SHA = '637e073aea7afb2232c219e200df83561651ae59720139c6ebb8d5833d2de00b'
TEST_FUNCTION = 'test_missing_or_wrong_group_generator_blocks_surjectivity'

TEST_REPLACEMENT = '''def test_missing_or_wrong_group_generator_blocks_surjectivity() -> None:
    theorem = typed_specialization(6)
    goal = MapSurjective(theorem.delta)
    relation, = delta_surjectivity_generator_inputs(goal)
    wrong = Relation(relation.lhs, FreeCyclicGroup(
        replace(relation.rhs.generator, name="Delta of wrong identity")
    ))
    rule = delta_surjectivity_from_generator_rule(goal)
    assert find_inference_matches_for_rule(rule, ()) == ()
    assert find_inference_matches_for_rule(rule, (_test_step(wrong),)) == ()
    assert find_inference_matches_for_rule(rule, (_test_step(theorem),)) == ()
    valid_relation = _test_step(relation)
    unrelated_theorem = _test_step(theorem)
    matches = find_inference_matches_for_rule(
        rule, (valid_relation, unrelated_theorem)
    )
    assert len(matches) == 1
    assert matches[0].premises == (valid_relation,)
    derived = apply_inference_match(matches[0])
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == goal
    assert derived.premises == (valid_relation,)
'''


def sha256_text(source: str) -> str:
    return hashlib.sha256(source.encode('utf-8')).hexdigest()


def _normalize(data: bytes) -> tuple[str, bytes, str]:
    bom = b'\xef\xbb\xbf' if data.startswith(b'\xef\xbb\xbf') else b''
    payload = data[len(bom):]
    if b'\r' in payload.replace(b'\r\n', b''):
        raise RuntimeError('CR-only line endings are not reviewed')
    if b'\r\n' in payload and b'\n' in payload.replace(b'\r\n', b''):
        raise RuntimeError('mixed EOL is not reviewed')
    return payload.decode('utf-8').replace('\r\n', '\n'), bom, ('\r\n' if b'\r\n' in payload else '\n')


def _read(path: Path) -> tuple[bytes, str, bytes, str]:
    raw = path.read_bytes()
    content, bom, eol = _normalize(raw)
    return raw, content, bom, eol


def _one(source: str, before: str, after: str, label: str) -> str:
    if source.count(before) != 1:
        raise RuntimeError('unreviewed or ambiguous R57R3 anchor ' + label)
    return source.replace(before, after, 1)


def _replace_function(source: str, name: str, replacement: str) -> str:
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1 or matches[0].decorator_list:
        raise RuntimeError('unreviewed test function or decorators: ' + name)
    node = matches[0]
    lines = source.splitlines(keepends=True)
    return ''.join(lines[:node.lineno - 1]) + replacement.rstrip() + '\n\n' + ''.join(lines[node.end_lineno:]).lstrip('\n')


def corrected_test(source: str) -> str:
    after = _replace_function(source, TEST_FUNCTION, TEST_REPLACEMENT)
    if sha256_text(after) != AFTER_TEST_SHA:
        raise RuntimeError('R57R3 corrected test does not match reviewed SHA-256')
    return after


def corrected_installer(source: str) -> str:
    start = "NEW_TEST3='''def " + TEST_FUNCTION
    marker = "'''\n\ndef patch_rule"
    if source.count(start) != 1:
        raise RuntimeError('R57 installer NEW_TEST3 anchor missing or ambiguous')
    first = source.index(start)
    last = source.find(marker, first)
    if last < 0:
        raise RuntimeError('R57 installer test template end missing')
    old_literal = source[first:last + 3]
    new_literal = "NEW_TEST3='''" + TEST_REPLACEMENT.rstrip() + "\n'''"
    after = _one(source, old_literal, new_literal, 'NEW_TEST3')
    old_pin = "    '" + TEST_NAME + "': '" + BEFORE_TEST_SHA + "',"
    new_pin = "    '" + TEST_NAME + "': '" + AFTER_TEST_SHA + "',"
    after = _one(after, old_pin, new_pin, 'AFTER_SHA256 R56 test')
    ast.parse(after, filename=INSTALL_NAME)
    if sha256_text(after) != AFTER_INSTALL_SHA:
        raise RuntimeError('R57R3 corrected installer does not match reviewed SHA-256')
    return after


def _git(*args: str) -> tuple[int, str]:
    result = subprocess.run(('git',) + args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode, result.stdout.decode('utf-8', 'replace').strip()


def _check_repo() -> None:
    code, branch = _git('branch', '--show-current')
    if code or branch != 'develop':
        raise RuntimeError('develop branch required')
    code, top = _git('rev-parse', '--show-toplevel')
    if code or Path(top).resolve() != ROOT.resolve():
        raise RuntimeError('extract R57R3 directly into the repository root')
    code, staged = _git('diff', '--cached', '--name-only')
    if code or staged:
        raise RuntimeError('staged files require independent review')
    code, _ = _git('merge-base', '--is-ancestor', REVIEWED_BASE, 'HEAD')
    if code:
        raise RuntimeError('HEAD is not a descendant of reviewed R56 base')


def _check_r57_review(source: str) -> None:
    """Use the R57 verified blob and local-patch guards, without writing."""
    namespace = {'__name__': '_r57r3_guard_review', '__file__': str(TARGET_INSTALL)}
    exec(compile(source, str(TARGET_INSTALL), 'exec'), namespace)
    states = namespace['review'](True)
    if not states or any(before != after for before, after, _ in states.values()):
        raise RuntimeError('R57 reviewed patches are missing or partially applied')


def _check_regeneration(source: str, expected: str) -> None:
    original = (PACKAGE / 'fixtures' / 'R56_TEST_ORIGINAL.py.txt').read_text(encoding='utf-8')
    namespace = {'__name__': '_r57r3_generation_review', '__file__': str(TARGET_INSTALL)}
    exec(compile(source, str(TARGET_INSTALL), 'exec'), namespace)
    if namespace['patch_test'](original) != expected:
        raise RuntimeError('R57 corrected installer cannot reproduce the reviewed test')
    if namespace['AFTER_SHA256'][namespace['R56_TEST']] != AFTER_TEST_SHA:
        raise RuntimeError('R57 corrected installer has a mismatched test hash')


def review() -> tuple[tuple[Path, bytes, bytes], ...]:
    _check_repo()
    if not TARGET_TEST.is_file() or not TARGET_INSTALL.is_file():
        raise RuntimeError('R56 test and R57 installer are required')
    raw_test, test_source, test_bom, test_eol = _read(TARGET_TEST)
    raw_inst, install_source, install_bom, install_eol = _read(TARGET_INSTALL)
    observed = (sha256_text(test_source), sha256_text(install_source))
    if observed == (BEFORE_TEST_SHA, BEFORE_INSTALL_SHA):
        _check_r57_review(install_source)
        revised_test = corrected_test(test_source)
        revised_installer = corrected_installer(install_source)
    elif observed == (AFTER_TEST_SHA, AFTER_INSTALL_SHA):
        revised_test, revised_installer = test_source, install_source
        _check_r57_review(install_source)
    else:
        raise RuntimeError('unreviewed or partially patched R57R3 source: ' + repr(observed))
    _check_regeneration(revised_installer, revised_test)
    return (
        (TARGET_TEST, raw_test, test_bom + revised_test.replace('\n', test_eol).encode('utf-8')),
        (TARGET_INSTALL, raw_inst, install_bom + revised_installer.replace('\n', install_eol).encode('utf-8')),
    )


def _atomic_write(path: Path, before: bytes, after: bytes) -> None:
    if before == after:
        return
    fd, temp = tempfile.mkstemp(prefix='.r57r3_', suffix='.tmp', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(after)
        if path.read_bytes() != before:
            raise RuntimeError('R57R3 target modified during install: ' + str(path))
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def run(dry_run: bool) -> None:
    changes = review()
    print('PHASE174_R57R3_SOURCE_GUARD=PASS')
    print('PHASE174_R57R3_NEW_GIVEN=0')
    print('PHASE174_R57R3_NEW_MATH_RULES=0')
    print('PHASE174_R57R3_CHANGED_TARGETS=2')
    if dry_run:
        print('PHASE174_R57R3_GATE=PASS_PREFLIGHT_ONLY')
        print('(END)')
        return
    for path, before, after in changes:
        _atomic_write(path, before, after)
    if any(path.read_bytes() != after for path, _, after in changes):
        raise RuntimeError('R57R3 final target bytes do not match the review')
    review()
    print('PHASE174_R57R3_GATE=PASS_R57R3_TEST_CONTRACT_AND_INSTALLER_PIN')
    print('(END)')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    opts = parser.parse_args()
    run(opts.dry_run)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

## run.ps1 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r57r3_surjectivity_test_contract_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R57R3 strict preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R57R3_DRYRUN=PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r57r3_surjectivity_test_contract_fix.install
    if ($LASTEXITCODE -ne 0) { throw 'R57R3 guarded test and installer patch failed' }
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase174_r3_r7_r57r3_surjectivity_test_contract_fix/tests/test_patch.py
    if ($LASTEXITCODE -ne 0) { throw 'R57R3 focused patch tests failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r57_narrative_source_cleanup\run.ps1' -DryRun
    if ($LASTEXITCODE -ne 0) { throw 'R57 guarded DryRun failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r57_narrative_source_cleanup\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R57 focused tests or public proof audit failed' }
    Write-Output 'PHASE174_R57R3_FULL_PYTEST=False'
    Write-Output 'PHASE174_R57R3_GATE=PASS_R57R3_FOCUSED_AND_R57_PUBLIC'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```

## 限定テスト全文

```python
"""R57R3: strict regression of one-premise matcher test and installer pin."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r57r3_surjectivity_test_contract_fix import install


@pytest.fixture
def sources() -> tuple[str, str, str, str, str]:
    root = Path(install.__file__).resolve().parent / 'fixtures'
    return tuple((root / filename).read_text(encoding='utf-8') for filename in (
        'R56_TEST_FULL_BEFORE.py.txt',
        'R56_TEST_FULL_AFTER.py.txt',
        'R57_INSTALL_FULL_BEFORE.py.txt',
        'R57_INSTALL_FULL_AFTER.py.txt',
        'R56_TEST_ORIGINAL.py.txt',
    ))


def test_reviewed_inputs_match_independent_pins(sources) -> None:
    old_test, new_test, old_inst, new_inst, original = sources
    assert install.sha256_text(old_test) == install.BEFORE_TEST_SHA
    assert install.sha256_text(new_test) == install.AFTER_TEST_SHA
    assert install.sha256_text(old_inst) == install.BEFORE_INSTALL_SHA
    assert install.sha256_text(new_inst) == install.AFTER_INSTALL_SHA
    assert ast.parse(original)


def test_test_function_replacement_is_only_functional_change(sources) -> None:
    old_test, new_test, _, _, _ = sources
    assert install.corrected_test(old_test) == new_test
    old_tree, new_tree = ast.parse(old_test), ast.parse(new_test)
    old_names = [node.name for node in old_tree.body if isinstance(node, ast.FunctionDef)]
    new_names = [node.name for node in new_tree.body if isinstance(node, ast.FunctionDef)]
    assert old_names == new_names
    assert new_test.count('assert matches[0].premises == (valid_relation,)') == 1
    assert new_test.count('assert derived.premises == (valid_relation,)') == 1
    assert 'rule, (_test_step(relation), _test_step(theorem))' not in new_test


def test_new_expected_behavior_requires_valid_group_not_unrelated_fact(sources) -> None:
    _, new_test, _, _, _ = sources
    fn = next(node for node in ast.parse(new_test).body
              if isinstance(node, ast.FunctionDef)
              and node.name == install.TEST_FUNCTION)
    body = ast.get_source_segment(new_test, fn)
    assert 'find_inference_matches_for_rule(rule, ()) == ()' in body
    assert 'find_inference_matches_for_rule(rule, (_test_step(wrong),)) == ()' in body
    assert 'find_inference_matches_for_rule(rule, (_test_step(theorem),)) == ()' in body
    assert 'assert len(matches) == 1' in body
    assert 'assert derived.conclusion == goal' in body


def test_installer_template_and_sha_are_consistent(sources) -> None:
    _, new_test, old_inst, new_inst, original = sources
    assert install.corrected_installer(old_inst) == new_inst
    scope = {'__name__': '_r57r3_test_installer', '__file__': str(install.TARGET_INSTALL)}
    exec(compile(new_inst, str(install.TARGET_INSTALL), 'exec'), scope)
    assert scope['patch_test'](original) == new_test
    assert scope['AFTER_SHA256'][scope['R56_TEST']] == install.AFTER_TEST_SHA


def test_guard_rejects_unreviewed_or_ambiguous_source() -> None:
    with pytest.raises((RuntimeError, SyntaxError, AssertionError)):
        install.corrected_test('def unrelated():\n    return True\n')
    with pytest.raises(RuntimeError):
        install.corrected_installer('NEW_TEST3 = "missing reviewed anchors"\n')


def test_mocked_dryrun_install_and_idempotency(tmp_path, monkeypatch, sources) -> None:
    old_test, new_test, old_inst, new_inst, _ = sources
    test = tmp_path / install.TEST_NAME
    installer = tmp_path / install.INSTALL_NAME
    test.parent.mkdir(parents=True)
    installer.parent.mkdir(parents=True)
    test.write_text(old_test, encoding='utf-8')
    installer.write_text(old_inst, encoding='utf-8')
    monkeypatch.setattr(install, 'ROOT', tmp_path)
    monkeypatch.setattr(install, 'TARGET_TEST', test)
    monkeypatch.setattr(install, 'TARGET_INSTALL', installer)
    monkeypatch.setattr(install, '_check_repo', lambda: None)
    monkeypatch.setattr(install, '_check_r57_review', lambda source: None)
    install.run(True)
    assert test.read_text(encoding='utf-8') == old_test
    assert installer.read_text(encoding='utf-8') == old_inst
    install.run(False)
    assert test.read_text(encoding='utf-8') == new_test
    assert installer.read_text(encoding='utf-8') == new_inst
    install.run(False)
    assert all(before == after for _, before, after in install.review())


def test_no_mathematical_or_renderer_files_appear_as_patch_targets(sources, monkeypatch, tmp_path) -> None:
    old_test, _, old_inst, _, _ = sources
    test = tmp_path / install.TEST_NAME
    installer = tmp_path / install.INSTALL_NAME
    test.parent.mkdir(parents=True)
    installer.parent.mkdir(parents=True)
    test.write_text(old_test, encoding='utf-8')
    installer.write_text(old_inst, encoding='utf-8')
    monkeypatch.setattr(install, 'ROOT', tmp_path)
    monkeypatch.setattr(install, 'TARGET_TEST', test)
    monkeypatch.setattr(install, 'TARGET_INSTALL', installer)
    monkeypatch.setattr(install, '_check_repo', lambda: None)
    monkeypatch.setattr(install, '_check_r57_review', lambda source: None)
    targets = {path.relative_to(tmp_path).as_posix() for path, _, _ in install.review()}
    assert targets == {install.TEST_NAME, install.INSTALL_NAME}


def test_actual_installed_state_matches_pins_if_repo_available() -> None:
    if not (install.ROOT / '.git').exists():
        pytest.skip('runtime project repository is required')
    test, source, _, _ = install._read(install.TARGET_TEST)
    installer, source_installer, _, _ = install._read(install.TARGET_INSTALL)
    assert test and installer
    assert install.sha256_text(source) == install.AFTER_TEST_SHA
    assert install.sha256_text(source_installer) == install.AFTER_INSTALL_SHA
    assert all(before == after for _, before, after in install.review())
```

## 変更一覧・完了条件・次段階との境界

- 変更：R56 テスト1関数の誤った否定アサーションを訂正、R57 の再現テンプレートと SHA-256 を同時更新。
- 実行する pytest：R57R3 `tests/test_patch.py`、R57 `tests/test_static.py`、R56 `tests/test_rule.py`・`tests/test_public.py`、R37 `tests/test_rule.py`。R57 公開監査は `audit` モジュールで実行。
- 完了：R57R3 ガード PASS、各限定 pytest PASS、R57 公開証明・出典・表示監査 PASS。
- 境界：新しい数学的規則・出典登録・表示規則は追加しない。全体 pytest は Phase 終了時のみ。

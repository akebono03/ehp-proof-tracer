# R57R2 変更コード全文

この修正で既存の import 節は変更しません。既存クラスも変更しません。新しいモジュールは `phase174_r3_r7_r57r2_duplicate_pytest_guard_fix/` 以下に追加します。

## 変更対象と位置

1. `phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py`：既存 `test_generator_relation_alone_proves_delta_surjectivity()` の直前、重複したデコレーター1件を削除。以下は関数全体とデコレーター。
2. `phase174_r3_r7_r57_narrative_source_cleanup/install.py`：モジュール定数 `NEW_TEST1` と `AFTER_SHA256` の検査値の訂正。コード全体を下記に掲載。
3. `phase174_r3_r7_r57r2_duplicate_pytest_guard_fix/install.py`：新規ファイル、ソース全文。
4. `phase174_r3_r7_r57r2_duplicate_pytest_guard_fix/tests/test_patch.py`：新規テストファイル、ソース全文。

## 変更後テスト関数全文

```python
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
```

## R57 install.py 変更後の全文

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
    'phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py': '8dbc5a52f3c4c57ca2b3f5cc8750112fb86cc4ca4fa9a521fbbb74aa29e48fab',
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
    assert find_inference_matches_for_rule(
        rule, (_test_step(relation), _test_step(theorem))
    ) == ()
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

## R57R2 install.py 新規全文

```python
"""Fix R57's accidentally duplicated pytest parametrization, preserving its guards.

Only the R56 test and R57's reviewed test-patch text + SHA are changed.
The established R57 proof rules and shared narrative implementation remain untouched.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
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

BEFORE_TEST_SHA = '05133a242e6dfdf28c3c6a813634299a8b77b01ab1ae9f1bf702e90a553c44d1'
AFTER_TEST_SHA = '8dbc5a52f3c4c57ca2b3f5cc8750112fb86cc4ca4fa9a521fbbb74aa29e48fab'
BEFORE_INSTALL_SHA = '6a4df3c77edd7a0abd902d28782d12a63ebb6bd69f8c7d03e8efff601cd1e32e'
AFTER_INSTALL_SHA = '5cea9f784ba727d177fcbfdf07c5a10329825d2a33cbac8eb37a7d1c726af11b'

DOUBLE_PARAM = """@pytest.mark.parametrize("n", (4, 6, 8, 10))
@pytest.mark.parametrize("n", (4, 6, 8, 10))
def test_generator_relation_alone_proves_delta_surjectivity"""
SINGLE_PARAM = """@pytest.mark.parametrize("n", (4, 6, 8, 10))
def test_generator_relation_alone_proves_delta_surjectivity"""

OLD_INSTALL_SHA_ROW = "    'phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py': '" + BEFORE_TEST_SHA + "',"
NEW_INSTALL_SHA_ROW = "    'phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py': '" + AFTER_TEST_SHA + "',"
OLD_INSTALL_TEST_TEXT = """NEW_TEST1=\'\'\'@pytest.mark.parametrize("n", (4, 6, 8, 10))
def test_generator_relation_alone_proves_delta_surjectivity"""
NEW_INSTALL_TEST_TEXT = """NEW_TEST1=\'\'\'def test_generator_relation_alone_proves_delta_surjectivity"""


def sha256_text(content: str) -> str:
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def normalize(data: bytes) -> tuple[str, bytes, str]:
    """Preserve UTF-8 BOM and CRLF/LF while rejecting mixed or CR-only EOL."""
    bom = b'\xef\xbb\xbf' if data.startswith(b'\xef\xbb\xbf') else b''
    payload = data[len(bom):]
    if b'\r' in payload.replace(b'\r\n', b''):
        raise RuntimeError('unexpected CR-only line ending')
    if b'\r\n' in payload and b'\n' in payload.replace(b'\r\n', b''):
        raise RuntimeError('mixed LF/CRLF line endings')
    return payload.decode('utf-8').replace('\r\n', '\n'), bom, ('\r\n' if b'\r\n' in payload else '\n')


def replace_exactly_once(source: str, old: str, new: str, label: str) -> str:
    count = source.count(old)
    if count != 1:
        raise RuntimeError('unreviewed or ambiguous R57R2 anchor: ' + label + ' count=' + str(count))
    return source.replace(old, new, 1)


def corrected_test(source: str) -> str:
    """Remove the redundant marker without changing the complete test function."""
    revised = replace_exactly_once(source, DOUBLE_PARAM, SINGLE_PARAM, 'duplicate n parametrization')
    tree = ast.parse(revised, filename=TEST_NAME)
    named = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name == 'test_generator_relation_alone_proves_delta_surjectivity']
    if len(named) != 1 or len(named[0].decorator_list) != 1:
        raise RuntimeError('surjectivity test must have exactly one parametrization')
    if sha256_text(revised) != AFTER_TEST_SHA:
        raise RuntimeError('revised test SHA-256 differs from reviewed result')
    return revised


def corrected_installer(source: str) -> str:
    """Update both the patch template and its expected output hash."""
    after = replace_exactly_once(source, OLD_INSTALL_SHA_ROW, NEW_INSTALL_SHA_ROW,
                                 'R57 test hash pin')
    after = replace_exactly_once(after, OLD_INSTALL_TEST_TEXT, NEW_INSTALL_TEST_TEXT,
                                 'R57 test replacement template')
    ast.parse(after, filename=INSTALL_NAME)
    if sha256_text(after) != AFTER_INSTALL_SHA:
        raise RuntimeError('revised installer SHA-256 differs from reviewed result')
    return after


def _read_target(path: Path) -> tuple[bytes, str, bytes, str]:
    raw = path.read_bytes()
    content, bom, eol = normalize(raw)
    return raw, content, bom, eol


def _git(*args: str) -> tuple[int, str]:
    result = subprocess.run(('git',) + args, cwd=ROOT, capture_output=True)
    return result.returncode, result.stdout.decode('utf-8', errors='replace').strip()


def _check_repo() -> None:
    status, branch = _git('branch', '--show-current')
    if status != 0 or branch != 'develop':
        raise RuntimeError('develop branch required')
    status, git_root = _git('rev-parse', '--show-toplevel')
    if status or Path(git_root).resolve() != ROOT.resolve():
        raise RuntimeError('extract directly into the repository root')
    status, staged = _git('diff', '--cached', '--name-only')
    if status or staged:
        raise RuntimeError('staged changes need separate review')
    status, _ = _git('merge-base', '--is-ancestor', REVIEWED_BASE, 'HEAD')
    if status != 0:
        raise RuntimeError('HEAD is not a descendant of the reviewed R56 base')


def _check_r57_review(installer_source: str) -> None:
    """Execute R57's existing strict review without running its installer.

    This still checks its three committed Git blob pins, local R56 rule/test,
    branch and staged files. No mathematical source gate is bypassed.
    """
    namespace = {'__name__': '_r57r2_readonly_review', '__file__': str(TARGET_INSTALL)}
    exec(compile(installer_source, str(TARGET_INSTALL), 'exec'), namespace)
    states = namespace['review'](True)
    if not states or any(before != after for before, after, _ in states.values()):
        raise RuntimeError('R57 did not finish installing its reviewed patch')


def review() -> tuple[tuple[Path, bytes, bytes], ...]:
    _check_repo()
    if not TARGET_TEST.is_file() or not TARGET_INSTALL.is_file():
        raise RuntimeError('R56 test and R57 installer are required')
    raw_test, test_source, test_bom, test_eol = _read_target(TARGET_TEST)
    raw_inst, installer_source, inst_bom, inst_eol = _read_target(TARGET_INSTALL)
    test_sha, inst_sha = sha256_text(test_source), sha256_text(installer_source)
    if (test_sha, inst_sha) == (BEFORE_TEST_SHA, BEFORE_INSTALL_SHA):
        # Validate the already installed R57 before making any additional edits.
        _check_r57_review(installer_source)
        revised_test = corrected_test(test_source)
        revised_inst = corrected_installer(installer_source)
        # The corrected R57 installer must now generate the identical revised
        # test from the reviewed original R56 test, with one marker only.
        original_test = (PACKAGE / 'fixtures' / 'R56_TEST_ORIGINAL.py.txt').read_text(encoding='utf-8')
        checked = {'__name__': '_r57r2_corrected_review', '__file__': str(TARGET_INSTALL)}
        exec(compile(revised_inst, str(TARGET_INSTALL), 'exec'), checked)
        if checked['patch_test'](original_test) != revised_test:
            raise RuntimeError('corrected R57 installer is not reproducible')
    elif (test_sha, inst_sha) == (AFTER_TEST_SHA, AFTER_INSTALL_SHA):
        revised_test, revised_inst = test_source, installer_source
        _check_r57_review(installer_source)
    else:
        raise RuntimeError('unreviewed or partially patched R57R2 sources: test=' + test_sha + ' installer=' + inst_sha)
    return (
        (TARGET_TEST, raw_test, test_bom + revised_test.replace('\n', test_eol).encode('utf-8')),
        (TARGET_INSTALL, raw_inst, inst_bom + revised_inst.replace('\n', inst_eol).encode('utf-8')),
    )


def _atomic_replace(path: Path, before: bytes, after: bytes) -> None:
    if before == after:
        return
    fd, temp = tempfile.mkstemp(prefix='.r57r2_', suffix='.tmp', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'wb') as file:
            file.write(after)
        if path.read_bytes() != before:
            raise RuntimeError('file modified during R57R2 install: ' + str(path))
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def run(dry_run: bool) -> None:
    changes = review()
    print('PHASE174_R57R2_SOURCE_GUARD=PASS')
    print('PHASE174_R57R2_DUPLICATE_PARAMETRIZATION_IDENTIFIED=True')
    print('PHASE174_R57R2_NEW_GIVEN=0')
    print('PHASE174_R57R2_NEW_MATH_RULES=0')
    print('PHASE174_R57R2_CHANGED_TARGETS=2')
    if dry_run:
        print('PHASE174_R57R2_GATE=PASS_PREFLIGHT_ONLY')
        print('(END)')
        return
    for path, before, after in changes:
        _atomic_replace(path, before, after)
    for path, _, after in changes:
        if path.read_bytes() != after:
            raise RuntimeError('failed to apply reviewed correction: ' + str(path))
    review()
    print('PHASE174_R57R2_GATE=PASS_R57R2_TEST_DECORATOR_AND_HASH_CORRECTED')
    print('(END)')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    run(args.dry_run)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

```

## R57R2 tests/test_patch.py 新規全文

```python
"""R57R2 narrow guard tests: duplicate pytest decorator and R57 pin consistency."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r57r2_duplicate_pytest_guard_fix import install


@pytest.fixture
def reviewed_sources() -> tuple[str, str]:
    path = Path(install.__file__).resolve().parent / 'fixtures'
    return (
        (path / 'R56_TEST_ORIGINAL.py.txt').read_text(encoding='utf-8'),
        (path / 'R57_INSTALL_FULL_BEFORE.py.txt').read_text(encoding='utf-8'),
    )


def test_original_patch_duplicates_parametrization(reviewed_sources) -> None:
    original_test, old_installer = reviewed_sources
    namespace = {'__name__': '_r57r2_old_inst', '__file__': str(install.TARGET_INSTALL)}
    exec(compile(old_installer, str(install.TARGET_INSTALL), 'exec'), namespace)
    defective = namespace['patch_test'](original_test)
    assert install.sha256_text(defective) == install.BEFORE_TEST_SHA
    assert defective.count(install.DOUBLE_PARAM) == 1


def test_corrected_test_has_exactly_one_n_parameterization(reviewed_sources) -> None:
    original_test, old_installer = reviewed_sources
    scope = {'__name__': '_r57r2_old_inst', '__file__': str(install.TARGET_INSTALL)}
    exec(compile(old_installer, str(install.TARGET_INSTALL), 'exec'), scope)
    patched = install.corrected_test(scope['patch_test'](original_test))
    tree = ast.parse(patched)
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == 'test_generator_relation_alone_proves_delta_surjectivity')
    assert len(function.decorator_list) == 1
    assert install.sha256_text(patched) == install.AFTER_TEST_SHA


def test_corrected_installer_regenerates_single_marker(reviewed_sources) -> None:
    original_test, old_installer = reviewed_sources
    fixed = install.corrected_installer(old_installer)
    scope = {'__name__': '_r57r2_fixed_inst', '__file__': str(install.TARGET_INSTALL)}
    exec(compile(fixed, str(install.TARGET_INSTALL), 'exec'), scope)
    assert install.sha256_text(fixed) == install.AFTER_INSTALL_SHA
    assert scope['AFTER_SHA256'][scope['R56_TEST']] == install.AFTER_TEST_SHA
    assert scope['patch_test'](original_test).count(install.DOUBLE_PARAM) == 0
    generated = scope['patch_test'](original_test)
    assert install.sha256_text(generated) == install.AFTER_TEST_SHA


def test_source_guard_refuses_modified_or_ambiguous_tests() -> None:
    with pytest.raises(RuntimeError):
        install.corrected_test('def test_something_else(): pass\n')
    with pytest.raises(RuntimeError):
        install.corrected_test(install.DOUBLE_PARAM + '\n' + install.DOUBLE_PARAM)
    with pytest.raises(RuntimeError):
        install.corrected_installer('AFTER_SHA256 = {}')


def test_current_test_and_installer_match_reviewed_final_state() -> None:
    raw_test, test_source, _, _ = install._read_target(install.TARGET_TEST)
    raw_inst, installer_source, _, _ = install._read_target(install.TARGET_INSTALL)
    assert raw_test and raw_inst
    assert install.sha256_text(test_source) == install.AFTER_TEST_SHA
    assert install.sha256_text(installer_source) == install.AFTER_INSTALL_SHA
    assert len(tuple(ast.walk(ast.parse(test_source)))) > 0


def test_no_math_or_renderer_file_is_edited_by_r57r2() -> None:
    changes = install.review()
    assert {target.relative_to(install.ROOT).as_posix() for target, _, _ in changes} == {
        install.TEST_NAME, install.INSTALL_NAME,
    }
    assert all(before == after for _, before, after in changes)


def test_local_dryrun_install_and_idempotency(tmp_path, monkeypatch, reviewed_sources) -> None:
    original_test, old_installer = reviewed_sources
    namespace = {'__name__': '_r57r2_test_setup', '__file__': str(install.TARGET_INSTALL)}
    exec(compile(old_installer, str(install.TARGET_INSTALL), 'exec'), namespace)
    original_installed_test = namespace['patch_test'](original_test)
    test_path = tmp_path / install.TEST_NAME
    installer_path = tmp_path / install.INSTALL_NAME
    test_path.parent.mkdir(parents=True)
    installer_path.parent.mkdir(parents=True)
    test_path.write_text(original_installed_test, encoding='utf-8')
    installer_path.write_text(old_installer, encoding='utf-8')
    monkeypatch.setattr(install, 'ROOT', tmp_path)
    monkeypatch.setattr(install, 'TARGET_TEST', test_path)
    monkeypatch.setattr(install, 'TARGET_INSTALL', installer_path)
    monkeypatch.setattr(install, '_check_repo', lambda: None)
    monkeypatch.setattr(install, '_check_r57_review', lambda _: None)
    install.run(True)
    assert install.sha256_text(test_path.read_text(encoding='utf-8')) == install.BEFORE_TEST_SHA
    install.run(False)
    assert install.sha256_text(test_path.read_text(encoding='utf-8')) == install.AFTER_TEST_SHA
    assert install.sha256_text(installer_path.read_text(encoding='utf-8')) == install.AFTER_INSTALL_SHA
    install.run(False)
    assert all(before == after for _, before, after in install.review())

```

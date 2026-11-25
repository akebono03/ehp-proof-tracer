# Phase 177 R3 — 追加コード全文

既存ファイルは変更しない。以下は新規ファイルの全文。

## __init__.py

```python
"""Isolated unsigned Delta composition rule; no public registration."""
```

## rule.py

```python
"""Cited Toda Proposition 2.5 for unsigned, explicitly typed Delta images."""
from __future__ import annotations

from expression import Composition, IteratedSuspension, MapApplication
from map_facts import EHP_DELTA_MAP
from phase165_r3_recursive_search import GoalExpansion
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase175_r4r10_cited_58_prop25_public.source import CitedTodaProp25
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, Relation, RelationType

RULE_NAME = "cited Toda Proposition 2.5 conditional unsigned Delta composition equality"


def unsigned_prop25_inputs(
    goal: object, base: object, composition_identity: object = None,
) -> tuple[object, ...] | None:
    """Validate exact syntax, map dimensions and the arithmetic equality branch.

    Without a separate identity the argument must literally be alpha o E^2 beta.
    Otherwise that identity is a mandatory, independently inferred premise.
    No alias conversion, sign normalization or 2-primary flag is assumed.
    """
    for relation in (goal, base):
        if (type(relation) is not Relation
                or relation.relation_type is not RelationType.EQUALITY
                or type(relation.lhs) is not MapApplication
                or relation.lhs.map != EHP_DELTA_MAP):
            return None
    if type(goal.rhs) is not Composition or goal == base:
        return None
    alpha, x = base.lhs.expression, base.rhs
    beta = goal.rhs.right
    if goal.rhs.left != x:
        return None
    explicit = Composition(alpha, IteratedSuspension(beta, 2))
    gamma = goal.lhs.expression
    a = typed_endpoints(alpha)
    b = typed_endpoints(beta)
    if a is None or b is None or (a[1] - 1) % 2:
        return None
    m, i, j = (a[1] - 1) // 2, a[0] - 1, b[0] + 1
    if (m < 2 or i < 2*m or j < i or b != (j-1, i-1)
            or not (m % 2 == 1 or j < 3*m-1)
            or typed_endpoints(x) != (i-1, m)
            or typed_endpoints(explicit) != (j+1, 2*m+1)
            or typed_endpoints(gamma) != (j+1, 2*m+1)
            or typed_endpoints(goal.rhs) != (j-1, m)):
        return None
    if composition_identity is None:
        if gamma != explicit:
            return None
        return (CitedTodaProp25(), base)
    if (type(composition_identity) is not Relation
            or composition_identity.relation_type is not RelationType.EQUALITY
            or composition_identity.lhs != explicit
            or composition_identity.rhs != gamma
            or composition_identity in (goal, base)):
        return None
    return (CitedTodaProp25(), base, composition_identity)


def unsigned_prop25_rule(
    goal: Relation, base: Relation, composition_identity: Relation | None = None,
) -> InferenceRule:
    """Require an actual cited GIVEN and the exact independently inferred inputs."""
    required = unsigned_prop25_inputs(goal, base, composition_identity)
    if required is None:
        raise ValueError("not a typed conditional unsigned Proposition 2.5 goal")

    def guard(premises, bindings):
        return (len(premises) == len(required)
                and tuple(step.conclusion for step in premises) == required
                and type(premises[0].conclusion) is CitedTodaProp25
                and premises[0].rule is ProofRule.GIVEN
                and not premises[0].premises
                and all(step.rule is ProofRule.INFERENCE for step in premises[1:])
                and unsigned_prop25_inputs(goal, base, composition_identity) == required)

    return InferenceRule(
        name=RULE_NAME,
        description=("Toda Proposition 2.5: when m is odd or j < 3m-1, "
                     "Delta(alpha o E^2 beta) = Delta(alpha) o beta. "
                     "Require a proved unsigned base equality and, if the argument "
                     "is not literal, a separately proved composition equality."),
        literature_reference=LiteratureReference(
            label="Toda Proposition 2.5", locator="Proposition 2.5"),
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN, statement_type=CitedTodaProp25,
            statement_pattern=required[0]),) + tuple(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=statement)
            for statement in required[1:]),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_unsigned_prop25(
    goal: object, base: object, composition_identity: object = None,
) -> tuple[GoalExpansion, ...]:
    """Return only an ordinary backward proposal; create no proof or GIVEN."""
    required = unsigned_prop25_inputs(goal, base, composition_identity)
    if required is None:
        return ()
    return (GoalExpansion(unsigned_prop25_rule(goal, base, composition_identity), required),)
```

## audit.py

```python
"""Verify reviewed repository dependencies and source integrity without modifying them."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
HEAD = '2d09ecbe10b60a38179022da561931a8e4bb39ba'
PINS = {
    'phase165_r52_r9_shared_math.py': '87e0fe1202fa265c7530d0dd7e2b0adda2f5ebc2',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'web_group_proof.py': '2c66da9c8e80a13812a63b6adda34c9414d8413c',
    'phase175_r4r12r10r1_cited_511_public/source.py': '92670af82d86c0a22b77ddde3b6d6ceb3ac17e5a',
    'phase175_r4r12r10r1_cited_511_public/provider.py': '6a57c443d8c69192ba58e213821cb62aac37553f',
    'phase175_r4r10_cited_58_prop25_public/source.py': 'b5162bdaac25e4578973816290207379734229f6',
    'phase175_r4r10_cited_58_prop25_public/provider.py': 'be1d726fe98c0258685674ea41099aab1103f318',
    'phase175_r4r7_prop25_typed_composition/rule.py': 'e957752baf93f75352d106e53205730af9a02b4d',
    'phase175_r4r12_public_two_summand_quotient/provider.py': '1b34fe0d2707a51af7acc52eaa7d38209e90dfa2',
    'phase175_r4r12r9_delta_generator_image_bridge/rule.py': 'cfff81f4662825b78f30f8b7b4886cb27333b6c2',
    'phase175_r4r12r13r2_delta_injective_e_surjective/rule.py': '763b98521f8d78bbca1f07944194384c55a9ed57',
    'phase168_r2_8_3_generator_identity/identity.py': '9052b3d75809a4a45e026d93da80f6d4aaad8b62',
    'sources/toda/Toda_02_2.tex': 'ed3667788805a429140dedf5d183736e43e0f2c3',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
    'expression.py': '7f7cd97468cd753643369f54774ee9892968c345',
    'map_facts.py': '86fbf404783e15d344595bf54df5a9a8bafc35fc',
    'phase175_r4r7_prop25_typed_composition/tests/test_rule.py': 'aefd725eb326ea9bcca54f93019b479f58a93ad5',
}

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, encoding='utf-8').strip()


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def matches_blob(raw, pin):
    lf = raw.replace(b'\r\n', b'\n')
    return pin in (blob(raw), blob(lf), blob(lf.replace(b'\n', b'\r\n')))


def snapshot():
    return (git('rev-parse', 'HEAD'), git('diff', '--binary', 'HEAD'),
            git('diff', '--cached', '--binary'), git('status', '--porcelain', '--untracked-files=all'))


def preflight():
    if Path(git('rev-parse', '--show-toplevel')).resolve() != ROOT:
        raise RuntimeError('WRONG_REPOSITORY_ROOT')
    if git('branch', '--show-current') != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    local_head = git('rev-parse', 'HEAD')
    remote_head = git('rev-parse', 'origin/develop')
    if local_head != HEAD or remote_head != HEAD:
        raise RuntimeError(
            f'REVIEWED_HEAD_REQUIRED:expected={HEAD};local={local_head};origin/develop={remote_head}'
        )
    if git('status', '--porcelain', '--untracked-files=no'):
        raise RuntimeError('TRACKED_WORKTREE_NOT_CLEAN')
    for name, pin in PINS.items():
        if git('rev-parse', 'HEAD:' + name) != pin or not matches_blob((ROOT/name).read_bytes(), pin):
            raise RuntimeError('SOURCE_PIN_CHANGED:' + name)
    from phase175_r4r12r10r1_cited_511_public.source import verify_cited_511
    from phase175_r4r10_cited_58_prop25_public.source import source_positions
    positions = source_positions(ROOT)
    positions['toda:(5.11)'] = verify_cited_511(ROOT)
    if not positions['toda:Proposition 2.5'] < positions['toda:(5.11)']:
        raise RuntimeError('SOURCE_ORDER_INVALID')
    return {'head': HEAD, 'source_positions': positions, 'pins': PINS}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        before = snapshot()
        result = preflight()
        if snapshot() != before:
            raise RuntimeError('REPOSITORY_CHANGED_DURING_PREFLIGHT')
        print('PHASE177_R3_HEAD=' + result['head'])
        print('PHASE177_R3_SOURCE_POSITIONS=' + repr(result['source_positions']))
        print('PHASE177_R3_PUBLIC_CONNECTION=NOT_ADDED')
        print('PHASE177_R3_FULL_PYTEST=NOT_RUN')
        print('PHASE177_R3_GATE=' + ('PASS_R3_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R3_DEPENDENCIES_VERIFIED'))
        return 0
    except Exception as exc:
        print('PHASE177_R3_ERROR=' + repr(exc))
        print('PHASE177_R3_GATE=FAIL_R3')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
```

## tests/test_rule.py

```python
"""Focused isolated rule contracts, including reuse of actual cited sources."""
from __future__ import annotations

from dataclasses import replace
import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension, MapApplication
from map_facts import EHP_DELTA_MAP, EHP_H_MAP
from phase175_r4r10_cited_58_prop25_public.source import CitedTodaProp25, build_cited_58_prop25_sources
from phase175_r4r12r10r1_cited_511_public.source import CitedToda511, canonical_511, build_cited_511_source
from phase175_r4r12r10r1_cited_511_public.provider import expand_cited_511
from phase177_r3_unsigned_delta_composition_isolated.rule import (
    RULE_NAME, unsigned_prop25_inputs, unsigned_prop25_rule, expand_unsigned_prop25,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)


def element(name, source, target):
    return HomotopyElement(name, target, source=source, target=target)


def fixture(m=4, i=9, j=10):
    alpha = element('a', i+1, 2*m+1)
    beta = element('b', j-1, i-1)
    x = element('x', i-1, m)
    gamma = element('g', j+1, 2*m+1)
    explicit = Composition(alpha, IteratedSuspension(beta, 2))
    base = Relation(MapApplication(EHP_DELTA_MAP, alpha), x)
    identity = Relation(explicit, gamma)
    goal = Relation(MapApplication(EHP_DELTA_MAP, gamma), Composition(x, beta))
    return goal, base, identity


def synthetic(statement, trust=ProofRule.INFERENCE):
    return ProofStep(statement, (), trust, inference_rule=InferenceRule('synthetic test parent'))


def test_literal_formula_needs_no_reflexive_premise():
    goal, base, identity = fixture()
    literal = replace(goal, lhs=MapApplication(EHP_DELTA_MAP, identity.lhs))
    expansion, = expand_unsigned_prop25(literal, base)
    assert expansion.subgoals == (CitedTodaProp25(), base)
    assert expansion.rule.name == RULE_NAME
    assert not expand_unsigned_prop25(goal, base)


def test_substitution_requires_independent_composition_identity():
    goal, base, identity = fixture()
    expansion, = expand_unsigned_prop25(goal, base, identity)
    assert expansion.subgoals == (CitedTodaProp25(), base, identity)
    parents = (synthetic(CitedTodaProp25(), ProofRule.GIVEN), synthetic(base), synthetic(identity))
    matches = find_inference_matches_for_rule(expansion.rule, parents)
    assert len(matches) == 1
    result = apply_inference_match(matches[0])
    assert result.conclusion == goal and result.rule is ProofRule.INFERENCE
    assert result.premises == parents


@pytest.mark.parametrize('m,i,j', [(3,6,10),(4,9,10),(5,11,15)])
def test_valid_general_dimensions(m,i,j):
    assert unsigned_prop25_inputs(*fixture(m,i,j)) is not None


@pytest.mark.parametrize('m,i,j', [(4,9,11),(4,9,12),(6,12,17),(1,2,3),(4,7,9),(4,9,8)])
def test_outside_verified_range(m,i,j):
    assert not expand_unsigned_prop25(*fixture(m,i,j))


@pytest.mark.parametrize('change', ['map','base_map','wrong_x','wrong_beta','wrong_gamma','exponent','reverse','not_equality'])
def test_rejects_mismatched_typed_input(change):
    goal, base, identity = fixture()
    if change == 'map':
        goal = replace(goal, lhs=MapApplication(EHP_H_MAP, goal.lhs.expression))
    elif change == 'base_map':
        base = replace(base, lhs=MapApplication(EHP_H_MAP, base.lhs.expression))
    elif change == 'wrong_x':
        goal = replace(goal, rhs=Composition(element('different',8,4),goal.rhs.right))
    elif change == 'wrong_beta':
        goal = replace(goal, rhs=Composition(base.rhs,element('different',9,8)))
    elif change == 'wrong_gamma':
        identity = replace(identity, rhs=element('different',11,9))
    elif change == 'exponent':
        identity = replace(identity, lhs=Composition(identity.lhs.left,IteratedSuspension(goal.rhs.right,1)))
    elif change == 'reverse':
        identity = replace(identity, lhs=identity.rhs, rhs=identity.lhs)
    else:
        base = replace(base, relation_type=RelationType.ORDER)
    assert not expand_unsigned_prop25(goal, base, identity)


@pytest.mark.parametrize('missing', [0,1,2])
def test_missing_parent_rejected(missing):
    goal, base, identity = fixture()
    rule = unsigned_prop25_rule(goal, base, identity)
    parents = (synthetic(CitedTodaProp25(),ProofRule.GIVEN),synthetic(base),synthetic(identity))
    assert not find_inference_matches_for_rule(rule, parents[:missing]+parents[missing+1:])


@pytest.mark.parametrize('changed', [0,1,2])
def test_wrong_trust_rejected(changed):
    goal, base, identity = fixture()
    rule = unsigned_prop25_rule(goal, base, identity)
    parents = [synthetic(CitedTodaProp25(),ProofRule.GIVEN),synthetic(base),synthetic(identity)]
    parents[changed] = synthetic(parents[changed].conclusion,
                                 ProofRule.INFERENCE if changed == 0 else ProofRule.GIVEN)
    assert not find_inference_matches_for_rule(rule, tuple(parents))


def test_wrong_citation_and_circular_goal_rejected():
    goal, base, identity = fixture()
    rule = unsigned_prop25_rule(goal, base, identity)
    parents = (synthetic(CitedTodaProp25('other'),ProofRule.GIVEN),synthetic(base),synthetic(identity))
    assert not find_inference_matches_for_rule(rule, parents)
    assert not expand_unsigned_prop25(base, base)


def test_actual_511_and_prop25_sources_derive_literal_formula():
    base = canonical_511()
    citation = CitedToda511(base)
    source511 = build_cited_511_source()
    source25 = build_cited_58_prop25_sources()
    step511, = [link.step for link in source511.proof_links if link.step.conclusion == citation]
    step25, = [link.step for link in source25.proof_links if link.step.conclusion == CitedTodaProp25()]
    expansion, = expand_cited_511(base, (citation,))
    match, = find_inference_matches_for_rule(expansion.rule, (step511,))
    base_step = apply_inference_match(match)
    beta = HomotopyElement('η₈',8,9,8,GeneratorSymbol('η',index=8))
    goal = Relation(MapApplication(EHP_DELTA_MAP, Composition(base.lhs.expression,IteratedSuspension(beta,2))),
                    Composition(base.rhs,beta))
    option, = expand_unsigned_prop25(goal, base)
    match, = find_inference_matches_for_rule(option.rule,(step25,base_step))
    result = apply_inference_match(match)
    assert result.conclusion == goal and result.rule is ProofRule.INFERENCE
    assert result.premises == (step25,base_step)
    assert base_step.premises == (step511,)
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
$previousBytecode = $env:PYTHONDONTWRITEBYTECODE
$previousUtf8 = $env:PYTHONUTF8
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONUTF8 = '1'
    $before = @(git status --porcelain --untracked-files=all) -join "`n"
    if ($LASTEXITCODE -ne 0) { throw 'git status failed' }
    if ($DryRun) {
        python -B -m phase177_r3_unsigned_delta_composition_isolated.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R3 DryRun failed' }
    } else {
        python -B -m phase177_r3_unsigned_delta_composition_isolated.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R3 preflight failed' }
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase177_r3_unsigned_delta_composition_isolated/tests phase175_r4r7_prop25_typed_composition/tests/test_rule.py
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R3 focused tests failed' }
        python -B -m phase177_r3_unsigned_delta_composition_isolated.audit
        if ($LASTEXITCODE -ne 0) { throw 'Phase177 R3 postflight failed' }
        $after = @(git status --porcelain --untracked-files=all) -join "`n"
        if ($LASTEXITCODE -ne 0 -or $before -cne $after) { throw 'Phase177 R3 repository status changed' }
        Write-Output 'PHASE177_R3_GATE=PASS_R3_UNSIGNED_DELTA_COMPOSITION_ISOLATED'
    }
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $previousBytecode
    $env:PYTHONUTF8 = $previousUtf8
    Pop-Location
}
```

## README.md

```markdown
# Phase 177 R3 — Isolated unsigned Delta composition

This package adds an isolated, source-backed inference rule for Toda Proposition 2.5. It uses the existing cited Proposition 2.5 GIVEN and a proved unsigned Delta equality. The literal composition needs no reflexive premise; a substituted argument requires a separate inferred equality. The existing signed rule is not changed.

The reviewed HEAD is `2d09ecbe10b60a38179022da561931a8e4bb39ba`. DryRun verifies pinned dependencies and source order. The normal run executes only the new rule tests and the existing signed-rule tests. No public provider registration, new GIVEN, database change, or group-completion claim is made. The eta double-suspension identity, notation transport, and Delta injectivity remain separate future tasks.

The source transcriptions already adopted by the repository are used; original-edition verification is not newly performed. The package was syntax-checked but repository-integrated pytest and Windows execution must be performed locally.
```

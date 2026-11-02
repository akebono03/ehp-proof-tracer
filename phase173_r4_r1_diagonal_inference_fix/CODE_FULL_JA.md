# Phase 173 R4-R1 — 置換可能なコード・テスト全文

既存 `phase173_r4_r1_source_bound_56/rule.py` は以下の全文に置き換える。変更後の import 部分を含み、省略なし。既存の関数・クラスは原則維持し、変更対象は `expand_source_bound_toda56()` のみ。

## 変更後の既存モジュール全文（`phase173_r4_r1_source_bound_56/rule.py`）

```python
"""Source-bound pi_7^4 decomposition: only a backward proposal, never a GIVEN.

The general Toda Proposition 4.4 source is a mandatory screened leaf.
The pi_6^3 prior must pass the published-prior source ordering rule.
The diagonal pi_7^7 relation and H(nu_4)=iota_7 must be independently
proved INFERENCE steps. A DB goal or candidate generator is not evidence.
"""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, MapApplication
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion, SourceBoundGoal
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r57_r20_general_specialization import expand_cited_general_specialization
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3m_prior_result_catalog.prior_results import resolve_prior_group_result
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import EHP_H_MAP


def _target_generators(goal: object) -> tuple[HomotopyElement, HomotopyElement] | None:
    """Match the exact current typed target; do not repair symbolic mismatches."""
    if not (
        isinstance(goal, Relation)
        and goal.relation_type is RelationType.EQUALITY
        and goal.lhs == TodaPrimaryGroup(7, 4)
        and isinstance(goal.rhs, DirectSumGroup)
        and len(goal.rhs.summands) == 2
    ):
        return None
    free, torsion = goal.rhs.summands
    if not (
        isinstance(free, FreeCyclicGroup)
        and isinstance(torsion, FiniteCyclicGroup)
        and type(torsion.order) is int and torsion.order == 4
        and isinstance(free.generator, HomotopyElement)
        and isinstance(torsion.generator, IteratedSuspension)
        and type(torsion.generator.exponent) is int
        and torsion.generator.exponent == 1
        and isinstance(torsion.generator.expression, HomotopyElement)
    ):
        return None
    nu4 = free.generator
    prime = torsion.generator.expression
    if not (
        nu4.dimension == 4 and nu4.source == 7 and nu4.target == 4
        and isinstance(nu4.generator, GeneratorSymbol)
        and nu4.generator.family == "ν" and nu4.generator.index == 4
        and prime.dimension == 3 and prime.source == 6 and prime.target == 3
        and isinstance(prime.generator, GeneratorSymbol)
        and prime.generator.family in ("\\nu'", "ν")
        and (prime.generator.family == "\\nu'" or prime.generator.decoration == "′")
    ):
        return None
    return nu4, prime


def _diagonal_goal(bridge: object) -> Relation | None:
    """Require the independently registered pi_7^7 goal with its identity."""
    candidates = registered_group_goal_candidates(bridge, n=7, k=0)
    if len(candidates) != 1:
        return None
    relation = candidates[0]
    if not (
        isinstance(relation, Relation)
        and relation.relation_type is RelationType.EQUALITY
        and relation.lhs == TodaPrimaryGroup(7, 7)
        and isinstance(relation.rhs, FreeCyclicGroup)
        and isinstance(relation.rhs.generator, HomotopyElement)
    ):
        return None
    iota = relation.rhs.generator
    if not (
        isinstance(iota.generator, GeneratorSymbol)
        and iota.generator.family == "ι" and iota.generator.index == 7
        and iota.dimension == 7
    ):
        return None
    return relation


def source_bound_toda56_rule(
    goal: Relation, prior_relation: Relation, diagonal: Relation, hopf: Relation,
) -> InferenceRule:
    """Derive the exact presentation only after four proved typed premises."""
    generators = _target_generators(goal)
    if generators is None or not isinstance(prior_relation, Relation):
        raise ValueError("Exact pi_7^4 target and typed prior relation required")
    nu4, prime = generators
    expected_prior = Relation(
        TodaPrimaryGroup(6, 3), FiniteCyclicGroup(4, prime), RelationType.EQUALITY,
    )
    if prior_relation != expected_prior:
        raise ValueError("The pi_6^3 generator is not the target's suspended generator")
    if not (
        isinstance(diagonal, Relation)
        and diagonal.relation_type is RelationType.EQUALITY
        and diagonal.lhs == TodaPrimaryGroup(7, 7)
        and isinstance(diagonal.rhs, FreeCyclicGroup)
        and isinstance(diagonal.rhs.generator, HomotopyElement)
        and diagonal.rhs.generator.generator is not None
        and diagonal.rhs.generator.generator.family == "ι"
        and diagonal.rhs.generator.generator.index == 7
    ):
        raise ValueError("An independently typed diagonal generator is required")
    exact_hopf = Relation(
        MapApplication(map=EHP_H_MAP, expression=nu4),
        diagonal.rhs.generator,
        RelationType.EQUALITY,
    )
    if hopf != exact_hopf:
        raise ValueError("The independent n=4 Hopf-invariant premise differs")
    universal = TodaProp44UniversalStatement()
    expected = (universal, expected_prior, diagonal, exact_hopf)

    def guard(premises, bindings):
        return (
            len(premises) == 4
            and tuple(step.conclusion for step in premises) == expected
            and premises[0].rule is ProofRule.GIVEN
            and premises[2].rule is ProofRule.INFERENCE
            and premises[3].rule is ProofRule.INFERENCE
        )

    return InferenceRule(
        name="Toda (5.6) pi_7^4 source-bound direct-sum presentation",
        description=(
            "Specialize cited Toda Proposition 4.4 at n=4, i=7 using the "
            "independently proved Hopf invariant H(nu_4)=iota_7. Its map "
            "(alpha,beta) -> E(alpha)+nu_4 composed with beta sends "
            "nu-prime to E nu-prime and identity iota_7 to nu_4. "
            "Transport the independently proved pi_6^3 and pi_7^7 "
            "presentations along this isomorphism; no DB result is an axiom."
        ),
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.GIVEN,
                           statement_type=TodaProp44UniversalStatement,
                           statement_pattern=universal),
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=expected_prior),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=diagonal),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=exact_hopf),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Proposition 4.4", locator="Proposition 4.4",
        ),
    )


def expand_source_bound_toda56(
    goal: object, available: tuple[object, ...], bridge: object, *, proof_target: object,
) -> tuple[GoalExpansion, ...]:
    """Offer one sound root; proof search must discharge all four subgoals."""
    if not isinstance(available, tuple):
        raise TypeError("screened available claims must be a tuple")
    generators = _target_generators(goal)
    if generators is None or goal != proof_target:
        return ()
    if sum(type(x) is TodaProp44UniversalStatement and x == TodaProp44UniversalStatement()
           for x in available) != 1:
        return ()
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        return ()
    prior = resolve_prior_group_result(
        bridge, source_n=3, source_k=3, citing_assertion_id=citing_id,
    )
    if not prior.eligible or prior.relation is None:
        return ()
    diagonal = _diagonal_goal(bridge)
    if diagonal is None:
        return ()
    # A direct DB/adopted GIVEN for pi_7^7 does not satisfy this root's
    # independent INFERENCE premise. Bind the diagonal to the screened
    # universal Toda (5.1) scalar specialization instead.
    diagonal_routes = expand_cited_general_specialization(diagonal, available)
    if len(diagonal_routes) != 1 or len(diagonal_routes[0].subgoals) != 1:
        return ()
    diagonal_source = diagonal_routes[0].subgoals[0]
    source_links = tuple(
        link for link in bridge.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == diagonal_source
        and bridge.registry.reference(
            bridge.registry.assertion(link.assertion_id).reference_id
        ).locator == "(5.1)"
    )
    if len(source_links) != 1 or diagonal_source == diagonal:
        return ()
    nu4, _ = generators
    hopf = Relation(
        MapApplication(map=EHP_H_MAP, expression=nu4),
        diagonal.rhs.generator,
        RelationType.EQUALITY,
    )
    try:
        rule = source_bound_toda56_rule(goal, prior.relation, diagonal, hopf)
    except ValueError:
        return ()
    return (GoalExpansion(
        rule, (TodaProp44UniversalStatement(), prior.relation,
               SourceBoundGoal(diagonal, diagonal_source), hopf),
    ),)
```

## 新規 `install.py` 全文

```python
"""Install one reviewed, minimal rule-function replacement with exact-source guards."""
from __future__ import annotations

import argparse
from hashlib import sha1, sha256
from pathlib import Path
import shutil
import subprocess
import os

TARGET = Path('phase173_r4_r1_source_bound_56/rule.py')
EXPECTED_BLOB = 'e05ada41cbcf53e8b755428afd245ba2da619fa8'
EXPECTED_PATCH_SHA256 = '1d63582af0e1632ac733e9dcb764a2afd6a1c3583f00acb88b56ce8b0d8964ce'
REVIEWED_SOURCES = {
    'phase165_r3_recursive_search.py': '06009bfcf57f99cac58c229d99c53f16324692d0',
    'phase165_r57_r20_general_specialization.py': 'e09603bee51d776cd4326a95930fc9c41f272a1b',
    'phase165_r52_r9_shared_math.py': '2718c55789af7f442ac2c086d016d3d6f7ca3133',
    'phase173_r4_r1_lemma54_source_bridge/source.py': 'a37bf7447194d72526522366944778c386c8966c',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
}


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ('git', *args), cwd=root, capture_output=True,
        text=True, encoding='utf-8', check=True,
    ).stdout.strip()


def blob_hash(data: bytes) -> str:
    """Compute the Git blob identity for exactly the supplied raw content."""
    prefix = b'blob ' + str(len(data)).encode('ascii') + b'\x00'
    return sha1(prefix + data).hexdigest()


def normalize_line_endings(data: bytes) -> bytes:
    return data.replace(b'\r\n', b'\n')


def proposed_bytes(root: Path) -> bytes:
    source = root / 'phase173_r4_r1_diagonal_inference_fix' / 'replacement_rule.py'
    if not source.is_file():
        raise RuntimeError('Replacement rule payload is missing')
    content = normalize_line_endings(source.read_bytes())
    if 'SourceBoundGoal(diagonal, diagonal_source)' not in content.decode('utf8'):
        raise RuntimeError('Replacement lacks the reviewed scoped diagonal')
    if sha256(content).hexdigest() != EXPECTED_PATCH_SHA256:
        raise RuntimeError('Replacement file differs from the reviewed patch')
    return content


def preflight(root: Path) -> str:
    if git(root, 'branch', '--show-current') != 'develop':
        raise RuntimeError('Only the reviewed develop branch is supported')
    if git(root, 'rev-parse', 'HEAD:' + TARGET.as_posix()) != EXPECTED_BLOB:
        raise RuntimeError('The committed target rule has changed; no patch applied')
    if git(root, 'rev-parse', 'HEAD') != git(root, 'rev-parse', 'origin/develop'):
        raise RuntimeError('Local HEAD differs from origin/develop')
    for name, expected in REVIEWED_SOURCES.items():
        if git(root, 'rev-parse', 'HEAD:' + name) != expected:
            raise RuntimeError('Reviewed dependency blob changed: ' + name)
    target = root / TARGET
    if not target.is_file():
        raise RuntimeError('Reviewed target file is missing')
    original = normalize_line_endings(target.read_bytes())
    replacement = proposed_bytes(root)
    state = 'NEW' if blob_hash(original) == EXPECTED_BLOB else 'ALREADY_INSTALLED' if original == replacement else 'UNREVIEWED'
    if state == 'UNREVIEWED':
        raise RuntimeError('Unreviewed target worktree content; refusing overwrite')
    if git(root, 'diff', '--cached', '--name-only', '--', TARGET.as_posix()):
        raise RuntimeError('Staged changes to the target must not be overwritten')
    # Avoid making any change when an unreviewed patch is staged or present.
    return state


def install(root: Path) -> str:
    state = preflight(root)
    if state == 'ALREADY_INSTALLED':
        return state
    destination = root / TARGET
    before = destination.read_bytes()
    backup = Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / (
        'EHPProofTracerRecovery/phase173_r4_r1_diagonal_inference_fix/original_rule.py'
    )
    backup.parent.mkdir(parents=True, exist_ok=True)
    if backup.exists() and normalize_line_endings(backup.read_bytes()) != normalize_line_endings(before):
        raise RuntimeError('An unrelated backup exists; refusing overwrite')
    if not backup.exists():
        shutil.copy2(destination, backup)
    destination.write_bytes(proposed_bytes(root))
    return 'INSTALLED'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    state = preflight(root)
    print('PHASE173_R4_R1_DIAGONAL_SOURCE_GUARD=PASS')
    print('PHASE173_R4_R1_DIAGONAL_PATCH_STATE=' + state)
    if args.dry_run:
        print('PHASE173_R4_R1_DIAGONAL_DRY_RUN=PASS')
        return 0
    outcome = install(root)
    print('PHASE173_R4_R1_DIAGONAL_INSTALL=' + outcome)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

## 新規 `verify.py` 全文

```python
"""Read-only post-install proof search for the exact Toda (5.6) root."""
from __future__ import annotations

from pathlib import Path

from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge, search_shared_group_goal, shared_expansion_provider,
)
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase173_r4_r1_lemma54_source_bridge.source import (
    add_verified_lemma54_source, expand_cited_lemma54_hopf,
)
from phase173_r4_r1_source_bound_56.rule import expand_source_bound_toda56
from proof import ProofRule
from unified_statement_registry import AssertionOrigin


def run_verification(root: Path) -> dict[str, object]:
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=4, k=3)
    if len(goals) != 1:
        raise RuntimeError('Expected exactly one registered pi_7^4 goal')
    goal = goals[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        raise RuntimeError('Missing published pi_7^4 citation target')
    chapter = (root / 'sources/toda/Toda_05_2.tex').read_text(encoding='utf-8-sig')
    augmented = add_verified_lemma54_source(
        bridge, citing_assertion_id=citing_id, chapter=chapter,
    )
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        augmented, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    ))
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )

    def extra(statement: object):
        hopf = expand_cited_lemma54_hopf(statement, available)
        if hopf:
            return hopf
        return expand_source_bound_toda56(
            statement, available, screened, proof_target=goal,
        )

    root_candidates = expand_source_bound_toda56(
        goal, available, screened, proof_target=goal,
    )
    if len(root_candidates) != 1:
        raise RuntimeError('Expected one strictly source-bound root')
    from phase165_r3_recursive_search import SourceBoundGoal
    if not isinstance(root_candidates[0].subgoals[2], SourceBoundGoal):
        raise RuntimeError('Diagonal is not required to be inferred from Toda (5.1)')
    provider = shared_expansion_provider(
        screened, extra_providers=(extra,), proof_target=goal,
    )
    result = search_shared_group_goal(
        n=4, k=3, group_structure=goal.rhs,
        bridge=augmented, citing_assertion_id=citing_id,
        expansion_provider=provider,
    )
    completed = result.status.value == 'complete' and result.conclusion == goal
    roots = tuple(
        step for step in result.proven_steps
        if step.conclusion == goal and step.rule is ProofRule.INFERENCE
        and step.inference_rule is not None
        and step.inference_rule.name == root_candidates[0].rule.name
    )
    certified = bool(completed and len(roots) == 1
                     and len(roots[0].premises) == 4
                     and roots[0].premises[2].rule is ProofRule.INFERENCE
                     and roots[0].premises[3].rule is ProofRule.INFERENCE
                     and roots[0].premises[2].premises
                     and roots[0].premises[2].premises[0].conclusion
                     == root_candidates[0].subgoals[2].source)
    return {
        'status': result.status.value,
        'complete': completed,
        'source_bound_root_count': len(roots),
        'diagonal_inference_certified': certified,
        'open_goal_count': len(result.open_goals),
        'diagnostics': tuple(str(x) for x in result.diagnostics),
    }


def main() -> int:
    from phase173_r4_r1_diagonal_inference_fix.install import preflight
    root = Path.cwd().resolve()
    if preflight(root) != 'ALREADY_INSTALLED':
        raise RuntimeError('Install the reviewed diagonal route before verifying')
    row = run_verification(root)
    print('PHASE173_R4_R1_DIAGONAL_VERIFICATION=PASS')
    print('PHASE173_R4_R1_PROOF_STATUS=' + str(row['status']))
    print('PHASE173_R4_R1_COMPLETE=' + str(row['complete']))
    print('PHASE173_R4_R1_DIAGONAL_INFERENCE_CERTIFIED=' + str(row['diagonal_inference_certified']))
    print('PHASE173_R4_R1_SOURCE_BOUND_ROOTS=' + str(row['source_bound_root_count']))
    print('PHASE173_R4_R1_OPEN_GOALS=' + str(row['open_goal_count']))
    print('PHASE173_R4_R1_DIAGNOSTICS=' + repr(row['diagnostics']))
    if not row['diagonal_inference_certified']:
        raise RuntimeError('A checked Toda (5.6) root proof is not yet complete')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

## 新規 `tests/test_install.py` 全文

```python
"""Offline tests: patch preflight remains fail-closed without repository imports."""
from __future__ import annotations

from hashlib import sha1
from pathlib import Path
import ast

import pytest

from phase173_r4_r1_diagonal_inference_fix.install import (
    EXPECTED_BLOB, EXPECTED_PATCH_SHA256,
    blob_hash,
    normalize_line_endings,
    proposed_bytes,
)


def test_blob_hash_uses_git_encoding() -> None:
    raw = b'abc'
    assert blob_hash(raw) == sha1(b'blob 3\x00abc').hexdigest()


def test_original_reviewed_blob_is_pinned() -> None:
    assert EXPECTED_BLOB == 'e05ada41cbcf53e8b755428afd245ba2da619fa8'


def test_newline_normalization() -> None:
    assert normalize_line_endings(b'a\r\nb\r\n') == b'a\nb\n'


def test_patch_file_is_complete_and_scoped() -> None:
    root = Path(__file__).resolve().parents[2]
    content = proposed_bytes(root)
    tree = ast.parse(content.decode('utf8'))
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert 'expand_source_bound_toda56' in functions
    assert 'source_bound_toda56_rule' in functions
    assert content.count(b'SourceBoundGoal(diagonal, diagonal_source)') == 1
    from hashlib import sha256
    assert sha256(content).hexdigest() == EXPECTED_PATCH_SHA256


def test_missing_payload_fails_closed(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match='missing'):
        proposed_bytes(tmp_path)


def test_non_scoped_payload_fails_closed(tmp_path: Path) -> None:
    file = tmp_path / 'phase173_r4_r1_diagonal_inference_fix' / 'replacement_rule.py'
    file.parent.mkdir()
    file.write_text('def missing(): return 1\n', encoding='utf8')
    with pytest.raises(RuntimeError, match='scoped diagonal'):
        proposed_bytes(tmp_path)


def test_altered_but_similarly_named_payload_is_rejected(tmp_path: Path) -> None:
    file = tmp_path / 'phase173_r4_r1_diagonal_inference_fix' / 'replacement_rule.py'
    file.parent.mkdir()
    file.write_text('SourceBoundGoal(diagonal, diagonal_source)\n', encoding='utf8')
    with pytest.raises(RuntimeError, match='differs from the reviewed patch'):
        proposed_bytes(tmp_path)
```

## 新規 `tests/test_scoped_diagonal.py` 全文

```python
"""Focused real-project tests for the certified Toda (5.1) diagonal route."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r3_recursive_search import (
    SourceBoundGoal, reconstruct_registered_goal,
)
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge, search_shared_group_goal, shared_expansion_provider,
)
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r57_r20_general_specialization import expand_cited_general_specialization
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource, add_verified_lemma54_source,
    expand_cited_lemma54_hopf,
)
from phase173_r4_r1_source_bound_56.rule import expand_source_bound_toda56
from proof import ProofRule
from unified_statement_registry import AssertionOrigin


@pytest.fixture(scope='module')
def screened_context():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=4, k=3)
    assert len(goals) == 1
    goal = goals[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    assert citing_id is not None
    chapter = (Path(__file__).resolve().parents[2] / 'sources/toda/Toda_05_2.tex').read_text(encoding='utf-8-sig')
    augmented = add_verified_lemma54_source(
        bridge, citing_assertion_id=citing_id, chapter=chapter,
    )
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        augmented, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    ))
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )
    assert sum(isinstance(x, TodaLemma54TypedSource) for x in available) == 1
    return augmented, screened, goal, citing_id, available


def test_diagonal_uses_only_cited_toda51_scalar_inference(screened_context) -> None:
    augmented, screened, goal, citing_id, available = screened_context
    roots = expand_source_bound_toda56(goal, available, screened, proof_target=goal)
    assert len(roots) == 1
    diagonal = roots[0].subgoals[2]
    assert isinstance(diagonal, SourceBoundGoal)
    assert diagonal.conclusion == registered_group_goal_candidates(augmented, n=7, k=0)[0]
    assert len(expand_cited_general_specialization(diagonal.conclusion, available)) == 1
    routes = expand_cited_general_specialization(diagonal.conclusion, available)
    assert routes[0].subgoals == (diagonal.source,)


def test_diagonal_subgoal_is_inference_not_database_given(screened_context) -> None:
    augmented, screened, goal, citing_id, available = screened_context
    diagonal = expand_source_bound_toda56(goal, available, screened, proof_target=goal)[0].subgoals[2]
    provider = shared_expansion_provider(screened, proof_target=goal)
    inferred = reconstruct_registered_goal(
        diagonal, screened, citing_id, provider,
        lookup_mode='typed_reference_publication',
    )
    assert inferred.rule is ProofRule.INFERENCE
    assert inferred.conclusion == diagonal.conclusion
    assert len(inferred.premises) == 1
    assert inferred.premises[0].conclusion == diagonal.source
    assert inferred.premises[0].rule is ProofRule.GIVEN


def test_complete_source_bound_pi74_root(screened_context) -> None:
    augmented, screened, goal, citing_id, available = screened_context

    def extra(statement: object):
        hopf = expand_cited_lemma54_hopf(statement, available)
        if hopf:
            return hopf
        return expand_source_bound_toda56(
            statement, available, screened, proof_target=goal,
        )

    provider = shared_expansion_provider(
        screened, extra_providers=(extra,), proof_target=goal,
    )
    result = search_shared_group_goal(
        n=4, k=3, group_structure=goal.rhs,
        bridge=augmented, citing_assertion_id=citing_id,
        expansion_provider=provider,
    )
    assert result.status.value == 'complete', (
        result.status.value, result.diagnostics, result.open_goals,
    )
    assert result.conclusion == goal
    assert any(step.rule is ProofRule.INFERENCE and step.conclusion == goal
               for step in result.proven_steps)
```

## 新規 `run.ps1` 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
Write-Output 'PHASE173_R4_R1_DIAGONAL_OFFLINE_PYTEST_START'
python -m pytest -q -p no:cacheprovider phase173_r4_r1_diagonal_inference_fix/tests/test_install.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 diagonal install tests failed' }
if ($DryRun) {
    python -m phase173_r4_r1_diagonal_inference_fix.install --root $Root --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 diagonal preflight failed' }
    exit 0
}
python -m phase173_r4_r1_diagonal_inference_fix.install --root $Root
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 diagonal installer failed' }
Write-Output 'PHASE173_R4_R1_DIAGONAL_FOCUSED_PYTEST_START'
python -m pytest -q -p no:cacheprovider `
  phase173_r4_r1_diagonal_inference_fix/tests/test_scoped_diagonal.py `
  phase173_r4_r1_source_bound_56/tests/test_rule.py `
  phase173_r4_r1_lemma54_source_bridge/tests/test_source.py
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 focused verification failed' }
python -m phase173_r4_r1_diagonal_inference_fix.verify
if ($LASTEXITCODE -ne 0) { throw 'R4-R1 checked proof is incomplete' }
Write-Output 'PHASE173_R4_R1_DIAGONAL_INSTALL_AND_PROOF=PASS'
```

## 新規 `README.md` 全文

```markdown
# Phase 173 R4-R1 — Source-bound Diagonal Inference Fix

This package makes one narrowly scoped change to the existing Toda (5.6) backward proposal for the registered group `pi_7^4`.

The preceding audit proved that the original root had four accepted premises but refused the third because `pi_7^7` was accepted as `GIVEN` while the root rule requires `INFERENCE`. The patch **does not relax this rule**. It wraps the diagonal premise in the existing `SourceBoundGoal`, requiring the existing cited Toda (5.1) scalar-specialization rule to infer it from the screened universal source.

## Installation and check

Extract the ZIP in the repository root on a current, synchronized `develop` branch. Invoke `phase173_r4_r1_diagonal_inference_fix/run.ps1 -DryRun`, then `phase173_r4_r1_diagonal_inference_fix/run.ps1`. The installer checks reviewed Git blobs, rejects unknown local target modifications, and backs up the original rule file outside the repository. It then replaces only `phase173_r4_r1_source_bound_56/rule.py`.

The focused tests check the scoped diagonal proof and an isolated, publication-screened proof search using the existing verified Toda Lemma 5.4 source module. The verification script reports `PHASE173_R4_R1_COMPLETE` and `PHASE173_R4_R1_DIAGONAL_INFERENCE_CERTIFIED`. Their value is not assumed in advance.

## Scope

Modified tracked file: `phase173_r4_r1_source_bound_56/rule.py` (imports and `expand_source_bound_toda56` only).

New package: this folder, including a complete replacement payload, guarded installer, focused tests, verification script, and full code listing.

No changes to production registries, proof constructors, source statements, DB goals, or web renderer. No full test suite. Do not treat this package alone as completion of Phase 173 or of the public Web proof.
```

## 新規 `AUDIT_PLAN_JA.md` 全文

```markdown
# Phase 173 R4-R1 — 対角群の出典付き推論修正

## 監査結果

最新 Root Match 監査では `ROOT_DIAGNOSIS=WRONG_PROOF_RULE`。4前提のうち第3前提 $\pi_7^7=\mathbb{Z}\{\iota_7\}$ のみ、既存規則の `INFERENCE` 要件に対し、直接採用された `GIVEN` だった。$H(\nu_4)=\iota_7$ は `INFERENCE` として成立している。

## 変更対象・追加位置

1. **既存ファイル** `phase173_r4_r1_source_bound_56/rule.py`：変更後の import 部分全文を含めて、既存 `expand_source_bound_toda56` 関数全体を置換。`source_bound_toda56_rule` など他の関数は変更しない。
2. **新規パッケージ** `phase173_r4_r1_diagonal_inference_fix/`：`replacement_rule.py`（既存ファイルの完全な置換内容）、`install.py`（`git`、`blob_hash`、`normalize_line_endings`、`proposed_bytes`、`preflight`、`install`、`main`）、`verify.py`（`run_verification`、`main`）、`run.ps1`、`tests/test_install.py`、`tests/test_scoped_diagonal.py`、文書を追加。

## 修正の論理

既存の `expand_cited_general_specialization(diagonal, available)` が提供する Toda (5.1) の一般形とその子目標を、出典 `locator=(5.1)` のスクリーン済み固定文献 `GIVEN` で照合する。その引用命題を `SourceBoundGoal(diagonal, diagonal_source)` に渡す。このラッパーは `reconstruct_registered_goal` にある既存仕様であり、DB 由来の直接 `GIVEN` や別の証明経路を採用せず、指定の一般形からの推論のみを受理する。

Root の `premise_patterns` と `match_guard` は変更しない。先行結果 $\pi_6^3$、Proposition 4.4、Lemma 5.4 の推論は変更しない。一般形が一意でない場合、出典照合が失敗した場合は候補を生成しない。

## 実行テスト

DryRun: `python -m pytest -q -p no:cacheprovider phase173_r4_r1_diagonal_inference_fix/tests/test_install.py`

本実行: `python -m pytest -q -p no:cacheprovider phase173_r4_r1_diagonal_inference_fix/tests/test_scoped_diagonal.py phase173_r4_r1_source_bound_56/tests/test_rule.py phase173_r4_r1_lemma54_source_bridge/tests/test_source.py`

インストール後に `python -m phase173_r4_r1_diagonal_inference_fix.verify` で一時的な公開相当の引用条件における Proof Search を実行する。全体テストは Phase 173 終了時だけ。

## 完了条件

- ソースおよび Git blob のガード PASS。
- 対角群を `INFERENCE` で導出し、その前提が Toda (5.1) の引用済み一般形である。
- Toda (5.6) の最終 Root が `INFERENCE` になり、`COMPLETE=True`・`DIAGONAL_INFERENCE_CERTIFIED=True` になる。
- まだ Web 表示経路には常設接続していない。これを R4-R1 の次段階とする。
- $\pi_8^5$ の群構造と位数8は R4-R2 の範囲。
```


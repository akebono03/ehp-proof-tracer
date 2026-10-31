# Phase 172 R4 — 追加コードおよび変更コード全文

## 既存の Renderer の変更

既存ファイル `phase168_r3_5_model_renderer.py` の変更対象は `render_model_backed_narrative_markdown()` のみです。既存トップレベル import は変更しません。関数内で `projection.py` を import します。

変更後の関数全文と変更後のソースファイル全文は、DryRun により `%LOCALAPPDATA%\EHPProofTracerRecovery\phase172_r4_*\render_model_backed_narrative_markdown_FULL.py` および `phase168_r3_5_model_renderer_FULL.py` として作成します。Git の R2 blob と適用済み R3 の全文を検証したうえで生成し、行の省略は行いません。

## 新規ファイルの全文

### `projection.py`

```python
"""Suppress a repeated Hopf surjectivity sentence backed by the same proof.

Only the display index is returned; every original ProofStep remains in the
verified proof model, including the second derived surjectivity statement.
"""
from __future__ import annotations

from homotopy_groups import TodaHopfInvariantMap
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from proof import ProofRule
from toda_rules import (
    TodaDeltaZeroStatement,
    TodaHopfInvariantSurjectiveStatement,
    TodaProp42ExactnessStatement,
)


def redundant_hopf_surjectivity_indices(
    model: object,
    display_order: tuple[int, ...],
    already_hidden: set[int] | frozenset[int] = frozenset(),
) -> frozenset[int]:
    """Hide only a later, uncited repetition of an earlier visible H-surjection.

    The later MapSurjective must be inferred from a Delta-zero step and an
    exactness step. The Delta-zero step must itself depend on the same exactness
    and a visible, cited-ancestor TodaHopfInvariantSurjectiveStatement for the
    identical typed Hopf map. This proves the repeated wording is redundant
    without relying on a TeX match or imposing a special pi_6^3 exception.
    """
    if (getattr(model, "status", None) is not ProofSearchStatus.COMPLETE
            or getattr(model, "open_goals", ())):
        return frozenset()
    steps = getattr(model, "steps", None)
    numbers = getattr(model, "step_citation_numbers", None)
    root = getattr(model, "root_index", None)
    if (not isinstance(steps, tuple) or not isinstance(numbers, tuple)
            or len(steps) != len(numbers) or type(root) is not int):
        return frozenset()
    try:
        ancestry = root_ancestor_step_indices(steps, root)
    except ValueError:
        return frozenset()
    order = tuple(display_order)
    if (any(type(i) is not int or i not in ancestry for i in order)
            or len(set(order)) != len(order)):
        return frozenset()
    visible = set(order).difference(already_hidden)
    identities = {id(step): i for i, step in enumerate(steps)}
    if len(identities) != len(steps):
        return frozenset()

    def index(step: object) -> int | None:
        by_identity = identities.get(id(step))
        if by_identity is not None:
            return by_identity
        by_value = [i for i, recorded in enumerate(steps) if recorded == step]
        return by_value[0] if len(by_value) == 1 else None

    def premises(step: object, count: int) -> tuple[int, ...] | None:
        parents = getattr(step, "premises", ())
        if len(parents) != count:
            return None
        found = tuple(index(parent) for parent in parents)
        if (any(i is None or i not in ancestry for i in found)
                or len(set(found)) != len(found)):
            return None
        return found

    def has_cited_given(index_: int) -> bool:
        try:
            ancestors = root_ancestor_step_indices(steps, index_)
        except ValueError:
            return False
        return any(
            steps[i].rule is ProofRule.GIVEN and bool(numbers[i])
            for i in ancestors
        )

    hidden: set[int] = set()
    for later_index in order:
        if later_index not in visible or later_index == root:
            continue
        later = steps[later_index]
        later_statement = later.conclusion
        if (later.rule is not ProofRule.INFERENCE
                or numbers[later_index]
                or not isinstance(later_statement, MapSurjective)
                or not isinstance(later_statement.map, TodaHopfInvariantMap)
                or typed_sentence(later_statement, later) is None):
            continue
        pair = premises(later, 2)
        if pair is None:
            continue
        delta_candidates = [i for i in pair if isinstance(steps[i].conclusion, TodaDeltaZeroStatement)]
        exact_candidates = [i for i in pair if isinstance(steps[i].conclusion, TodaProp42ExactnessStatement)]
        if len(delta_candidates) != 1 or len(exact_candidates) != 1:
            continue
        delta_index = delta_candidates[0]
        exact_index = exact_candidates[0]
        delta = steps[delta_index]
        exact = steps[exact_index]
        if (delta.rule is not ProofRule.INFERENCE
                or exact.rule is not ProofRule.INFERENCE
                or not has_cited_given(exact_index)):
            continue
        delta_parents = premises(delta, 2)
        if delta_parents is None or exact_index not in delta_parents:
            continue
        earlier_index = next(i for i in delta_parents if i != exact_index)
        earlier = steps[earlier_index]
        earlier_statement = earlier.conclusion
        if (earlier_index not in visible
                or order.index(earlier_index) >= order.index(later_index)
                or earlier.rule is not ProofRule.INFERENCE
                or not isinstance(earlier_statement, TodaHopfInvariantSurjectiveStatement)
                or not isinstance(earlier_statement.map, TodaHopfInvariantMap)
                or earlier_statement.map != later_statement.map
                or typed_sentence(earlier_statement, earlier) is None
                or not has_cited_given(earlier_index)):
            continue
        hidden.add(later_index)
    return frozenset(hidden)
```

### `tests/test_projection.py`

```python
"""Phase 172 R4: canonical proof, retained citations and safe suppression."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_26_exactness_projection import project_exactness_chains
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase172_r2_suspension_relation_display.projection import redundant_suspension_relation_indices
from phase172_r3_hopf_chain_display.projection import project_verified_hopf_chain
from phase172_r4_hopf_surjectivity_display.projection import redundant_hopf_surjectivity_indices
from proof import ProofRule
from toda_rules import TodaHopfInvariantSurjectiveStatement


@pytest.fixture(scope="module")
def verified_pi63():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    chains = project_exactness_chains(model)
    suppressed = {index for chain in chains for index in chain.step_indices}
    order = tuple(
        item.step_index
        for item in project_narrative_order(model, suppressed)
        if item.step_index in scope
    )
    suppressed.update(redundant_suspension_relation_indices(model, order, suppressed))
    hopf = project_verified_hopf_chain(model, order, suppressed)
    assert hopf is not None
    suppressed.update(hopf.hidden_indices)
    return result, model, order, suppressed


def _repetition(model, hidden):
    assert len(hidden) == 1
    later_index = next(iter(hidden))
    later = model.steps[later_index]
    assert isinstance(later.conclusion, MapSurjective)
    delta = next(step for step in later.premises if type(step.conclusion).__name__ == "TodaDeltaZeroStatement")
    earlier = next(step for step in delta.premises if isinstance(step.conclusion, TodaHopfInvariantSurjectiveStatement))
    earlier_index = next(i for i, step in enumerate(model.steps) if step is earlier)
    return earlier_index, later_index


def test_real_completed_proof_hides_only_later_h_surjectivity(verified_pi63):
    result, model, order, suppressed = verified_pi63
    hidden = redundant_hopf_surjectivity_indices(model, order, suppressed)
    earlier_index, later_index = _repetition(model, hidden)
    assert earlier_index not in hidden
    assert earlier_index in order and later_index in order
    assert model.steps[earlier_index].conclusion.map == model.steps[later_index].conclusion.map
    assert model.steps[earlier_index].rule is ProofRule.INFERENCE
    assert model.steps[later_index].rule is ProofRule.INFERENCE
    assert not model.step_citation_numbers[later_index]
    assert result.proven_steps == model.steps
    assert len(model.citations) == 8


def test_real_web_prose_retains_first_h_and_short_exact_sequence(verified_pi63):
    result, model, order, suppressed = verified_pi63
    markdown = render_model_backed_narrative_markdown(result, model)
    references, body = markdown.split("\n証明\n", 1)
    assert "[R6] Proposition 4.2 (4.4)." in references
    assert r"$H: \pi_{6}^{3}\to \pi_{6}^{5}$ は全射." in body
    assert r"完全性より, $H: \pi_{6}^{3}\to \pi_{6}^{5}$ は全射." not in body
    assert r"$H$ の全射性と完全性より" in body
    assert r"0\longrightarrow \pi_{5}^{2}" in body
    assert r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}" in body
    assert r"H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}" in body
    assert len(model.citations) == 8


def test_direct_citation_on_later_statement_preserves_later_line(verified_pi63):
    _, model, order, suppressed = verified_pi63
    hidden = redundant_hopf_surjectivity_indices(model, order, suppressed)
    _, later = _repetition(model, hidden)
    updated = list(model.step_citation_numbers)
    updated[later] = (6,)
    changed = replace(model, step_citation_numbers=tuple(updated))
    assert redundant_hopf_surjectivity_indices(changed, order, suppressed) == frozenset()


def test_hidden_earlier_source_prevents_suppression(verified_pi63):
    _, model, order, suppressed = verified_pi63
    hidden = redundant_hopf_surjectivity_indices(model, order, suppressed)
    earlier, later = _repetition(model, hidden)
    assert redundant_hopf_surjectivity_indices(
        model, order, set(suppressed).union({earlier}),
    ) == frozenset()
    assert redundant_hopf_surjectivity_indices(
        model, tuple(i for i in order if i != earlier), suppressed,
    ) == frozenset()
    assert later not in suppressed


def test_incomplete_or_invalid_root_never_suppresses(verified_pi63):
    _, model, order, suppressed = verified_pi63
    for changed in (
        replace(model, status=ProofSearchStatus.PARTIAL),
        replace(model, open_goals=("unresolved",)),
        replace(model, root_index=None),
    ):
        assert redundant_hopf_surjectivity_indices(changed, order, suppressed) == frozenset()
    assert redundant_hopf_surjectivity_indices(model, order + (order[0],), suppressed) == frozenset()


def test_missing_source_citation_or_different_map_preserves_both(verified_pi63):
    _, model, order, suppressed = verified_pi63
    hidden = redundant_hopf_surjectivity_indices(model, order, suppressed)
    earlier, later = _repetition(model, hidden)
    cited = list(model.step_citation_numbers)
    for i in root_ancestor_step_indices(model.steps, earlier):
        if model.steps[i].rule is ProofRule.GIVEN:
            cited[i] = ()
    changed = replace(model, step_citation_numbers=tuple(cited))
    assert redundant_hopf_surjectivity_indices(changed, order, suppressed) == frozenset()
    alternate = replace(model.steps[later].conclusion, map=object())
    modified_steps = list(model.steps)
    modified_steps[later] = replace(model.steps[later], conclusion=alternate)
    modified_model = replace(model, steps=tuple(modified_steps))
    assert redundant_hopf_surjectivity_indices(modified_model, order, suppressed) == frozenset()
```

### `install.py`

```python
"""Guarded Phase 172 R4 presentation-only patch with focused tests/rollback."""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from phase172_r3_hopf_chain_display import install as r3_installer

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = Path('phase168_r3_5_model_renderer.py')
PROJECTION = Path('phase172_r4_hopf_surjectivity_display/projection.py')
TESTS = Path('phase172_r4_hopf_surjectivity_display/tests/test_projection.py')
BASE_R2_BLOB = 'bb267bc669bdcaa5b9dcc24bdf7dc8b2ac4e7c95'
R3_PROJECTION_SHA256 = 'fae04a1f9e5c0a2408e8cc29180bfe64c14b8376186ba78b168db270e2e55413'
R3_TEST_SHA256 = '843f889791b3a447051edfd1c22d58208cbe78e481d048c0e998443f12e8e9b6'
R3_INSTALL_SHA256 = 'ee16868581a8496acbb76873d8c3ff39587b5b3297e7fa23040effd594ea6c8a'
OLD = (
    '        if hopf_display is not None:\n'
    '            suppressed_body_indices.update(hopf_display.hidden_indices)\n'
    '    for index in order:\n'
)
NEW = (
    '        if hopf_display is not None:\n'
    '            suppressed_body_indices.update(hopf_display.hidden_indices)\n'
    '    if not incomplete:\n'
    '        from phase172_r4_hopf_surjectivity_display.projection import (\n'
    '            redundant_hopf_surjectivity_indices,\n'
    '        )\n'
    '        suppressed_body_indices.update(\n'
    '            redundant_hopf_surjectivity_indices(\n'
    '                model, order, suppressed_body_indices,\n'
    '            )\n'
    '        )\n'
    '    for index in order:\n'
)
TEST_GROUPS = (
    ('phase172_r4_hopf_surjectivity_display/tests/test_projection.py',),
    ('phase172_r3_hopf_chain_display/tests/test_projection.py',),
    ('phase172_r2_suspension_relation_display/tests/test_projection.py',),
    ('phase171_r20r13_eta_sentence_layout/tests/test_projection.py',),
    ('phase171_r20r12_verified_cyclic_narrative/tests/test_projection.py',),
    ('phase169_r4d_pi64_narrative_audit/tests/test_r4d_narrative_audit.py',),
)


def run_command(args: list[str], *, timeout: int = 45) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=ROOT, capture_output=True, text=True,
        encoding='utf-8', errors='replace', check=False, timeout=timeout,
    )


def checked(*args: str) -> str:
    process = run_command(list(args))
    if process.returncode:
        raise RuntimeError('command failed: ' + repr(args) + ' ' + process.stderr[-1000:])
    return process.stdout.strip()


def normalized(raw: bytes) -> str:
    result = raw.decode('utf-8-sig')
    if '\r' in result.replace('\r\n', ''):
        raise RuntimeError('mixed newline convention in guarded source')
    return result.replace('\r\n', '\n')


def updated_renderer(raw: bytes) -> bytes:
    old = normalized(raw)
    if old.count(OLD) != 1 or NEW in old:
        raise RuntimeError('R3 Renderer insertion anchor changed')
    new = old.replace(OLD, NEW, 1)
    tree = ast.parse(new)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef)
               and node.name == 'render_model_backed_narrative_markdown']
    if len(matches) != 1:
        raise RuntimeError('Renderer function identity changed')
    newline = '\r\n' if b'\r\n' in raw else '\n'
    return new.replace('\n', newline).encode('utf-8')


def full_renderer_function(raw: bytes) -> str:
    source = normalized(raw)
    tree = ast.parse(source)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef)
               and node.name == 'render_model_backed_narrative_markdown']
    if len(matches) != 1:
        raise RuntimeError('Renderer function not uniquely present')
    node = matches[0]
    return '\n'.join(source.splitlines()[node.lineno - 1:node.end_lineno]) + '\n'


def preflight() -> dict[str, str | None]:
    branch = checked('git', 'branch', '--show-current')
    head = checked('git', 'rev-parse', 'HEAD')
    if branch != 'develop':
        raise RuntimeError('R4 requires develop')
    original = subprocess.run(
        ['git', 'cat-file', 'blob', BASE_R2_BLOB], cwd=ROOT,
        capture_output=True, check=True,
    ).stdout
    if r3_installer.REVIEWED_GIT_BLOB != BASE_R2_BLOB:
        raise RuntimeError('R3 reviewed baseline changed')
    expected_r3 = r3_installer.transformed(original)
    current = (ROOT / TARGET).read_bytes()
    if normalized(current) != normalized(expected_r3):
        raise RuntimeError('R3 applied Renderer differs from the reviewed R2->R3 transformation')
    committed = subprocess.run(
        ['git', 'show', 'HEAD:' + TARGET.as_posix()], cwd=ROOT,
        capture_output=True, check=True,
    ).stdout
    if normalized(committed) == normalized(expected_r3):
        renderer_state = 'R3_COMMITTED'
    elif normalized(committed) == normalized(original):
        renderer_state = 'R3_UNCOMMITTED'
    else:
        raise RuntimeError('committed Renderer is neither reviewed R2 nor R3')
    for path, expected in (
        (Path('phase172_r3_hopf_chain_display/projection.py'), R3_PROJECTION_SHA256),
        (Path('phase172_r3_hopf_chain_display/tests/test_projection.py'), R3_TEST_SHA256),
        (Path('phase172_r3_hopf_chain_display/install.py'), R3_INSTALL_SHA256),
    ):
        if not (ROOT / path).is_file():
            raise RuntimeError('missing R3 prerequisite: ' + str(path))
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise RuntimeError('R3 prerequisite payload differs: ' + str(path))
    r2_test = ROOT / 'phase172_r2_suspension_relation_display/tests/test_projection.py'
    if not r2_test.is_file():
        raise RuntimeError('missing R2 regression test')
    updated_r2_test = normalized(r2_test.read_bytes())
    if (r'''    assert r"$\nu'\eta_{6} = \nu'E\eta_{5}$." in body''' in updated_r2_test
            or 'assert "[R4] Proposition 2.2." in references' not in updated_r2_test
            or 'assert "[R5] (5.3)." in references' not in updated_r2_test):
        raise RuntimeError('R3R2 corrected R2 test contract is absent')
    for path in (PROJECTION, TESTS):
        if not (ROOT / path).is_file():
            raise RuntimeError('R4 payload is missing: ' + str(path))
    updated_renderer(current)
    remote = run_command(['git', 'ls-remote', 'origin', 'refs/heads/develop'], timeout=25)
    remote_head = remote.stdout.split()[0] if remote.returncode == 0 and remote.stdout.strip() else None
    if remote_head is not None and remote_head != head:
        raise RuntimeError('local HEAD differs from origin/develop')
    return {'branch': branch, 'head': head, 'remote_head': remote_head,
            'renderer_state': renderer_state,
            'before_sha256': hashlib.sha256(current).hexdigest()}


def report_directory() -> Path:
    base = Path(os.environ.get('LOCALAPPDATA') or Path.home()) / 'EHPProofTracerRecovery'
    result = base / ('phase172_r4_' + datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%fZ'))
    result.mkdir(parents=True, exist_ok=False)
    return result


def focused_tests(destination: Path) -> list[dict[str, object]]:
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONPATH'] = str(ROOT) + os.pathsep + env.get('PYTHONPATH', '')
    reports = []
    for number, paths in enumerate(TEST_GROUPS, 1):
        process = subprocess.run(
            [sys.executable, '-B', '-m', 'pytest', '-q', '--tb=short',
             '-p', 'no:cacheprovider', *paths],
            cwd=ROOT, capture_output=True, text=True,
            encoding='utf-8', errors='replace', env=env, timeout=240,
        )
        content = process.stdout + '\n' + process.stderr
        (destination / f'focused_{number}.log').write_text(content, encoding='utf-8')
        reports.append({'group': number, 'paths': list(paths),
                        'exit_code': process.returncode})
        print(f'PHASE172_R4_FOCUSED_{number}=' +
              ('PASS' if process.returncode == 0 else 'FAIL'), flush=True)
        if process.returncode != 0:
            raise RuntimeError(f'focused pytest group {number} failed:\n' + content[-2500:])
    return reports


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--run-focused-tests', action='store_true')
    options = parser.parse_args()
    if not options.dry_run and not options.run_focused_tests:
        raise RuntimeError('R4 application requires --run-focused-tests')
    state = preflight()
    print('PHASE172_R4_BRANCH=' + state['branch'], flush=True)
    print('PHASE172_R4_HEAD=' + state['head'], flush=True)
    print('PHASE172_R4_R3_RENDERER_STATE=' + state['renderer_state'], flush=True)
    print('PHASE172_R4_REVIEWED_CONTENT=PASS', flush=True)
    before = (ROOT / TARGET).read_bytes()
    after = updated_renderer(before)
    output = report_directory()
    (output / 'render_model_backed_narrative_markdown_FULL.py').write_text(
        full_renderer_function(after), encoding='utf-8',
    )
    (output / 'phase168_r3_5_model_renderer_FULL.py').write_bytes(after)
    if options.dry_run:
        print('PHASE172_R4_DRY_RUN=PASS', flush=True)
        print('PHASE172_R4_FULL_FUNCTION=' + str(output), flush=True)
        print('PHASE172_R4_SOURCE_CHANGES=0', flush=True)
        return 0
    (output / 'renderer_before.py').write_bytes(before)
    report = {'phase': '172-R4', 'mode': 'PRESENTATION_ONLY',
              'state': state, 'full_pytest_executed': False,
              'proof_tree_modified': False, 'mathematical_rules_modified': False,
              'focused_tests': []}
    try:
        (ROOT / TARGET).write_bytes(after)
        report['focused_tests'] = focused_tests(output)
        report['result'] = 'PASS_R4_SURJECTIVITY_DISPLAY_ONLY'
    except BaseException as exc:
        (ROOT / TARGET).write_bytes(before)
        report['result'] = 'FAIL_RESTORED_SOURCE'
        report['exception'] = repr(exc)
        (output / 'result.json').write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
        )
        print('PHASE172_R4_RESTORED=PASS', flush=True)
        print('PHASE172_R4_REPORT=' + str(output), flush=True)
        raise
    (output / 'result.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
    )
    print('PHASE172_R4_REPORT=' + str(output), flush=True)
    print('PHASE172_R4_SOURCE_CHANGES=1', flush=True)
    print('PHASE172_R4_RESULT=PASS_R4_SURJECTIVITY_DISPLAY_ONLY', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

### `run.ps1`

```powershell
param(
    [switch]$DryRun,
    [switch]$RunFocusedTests
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $env:PYTHONUTF8 = '1'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $arguments = @('-B', '-m', 'phase172_r4_hopf_surjectivity_display.install')
    if ($DryRun) { $arguments += '--dry-run' }
    if ($RunFocusedTests) { $arguments += '--run-focused-tests' }
    & python @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R4 failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}
```

### `__init__.py`

```python
"""Phase 172 R4: verified Hopf surjectivity presentation projection."""
```

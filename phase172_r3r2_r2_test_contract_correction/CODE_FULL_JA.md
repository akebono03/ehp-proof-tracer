# Phase 172 R3R2：変更コードとテスト全文

## 既存ファイル：R2 テスト

変更対象：`phase172_r2_suspension_relation_display/tests/test_projection.py` の `test_real_complete_narrative_retains_cited_source_and_hopf_conclusion()`。このテスト関数だけ置換する。import と他の関数は変更しない。ZIP の `payload/test_projection.py` に改訂後ファイル全文を収録する。

### 改訂テスト関数の全文

```python
def test_real_complete_narrative_retains_cited_source_and_hopf_conclusion(
    verified_pi63,
):
    result, model = verified_pi63
    markdown = render_model_backed_narrative_markdown(result, model)
    references, body = markdown.split("\n証明\n", 1)
    assert "[R3] Chapter V, i)." in references
    assert r"[R3]より, $E(\eta_{5})=\eta_{6}$." in body
    assert r"$E\eta_{5} = \eta_{6}$." not in body
    assert r"$\eta_{6} = E\eta_{5}$." not in body
    assert "[R4] Proposition 2.2." in references
    assert "[R5] (5.3)." in references
    assert r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$." in body
    assert r"\operatorname{ord}(\nu')=4" in body
    assert len(model.citations) == 8
```

### 変更後のテストファイル全文（import を含む）

```python
"""Phase 172 R2: exact proof-ancestry-only suspension prose suppression."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Suspension
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase172_r2_suspension_relation_display.projection import (
    redundant_suspension_relation_indices,
    same_typed_generator,
)
from proof import ProofRule, Relation, RelationType


@pytest.fixture(scope="module")
def verified_pi63():
    original = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=original, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(original, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
    )
    return result, build_linked_proof_narrative_model(result, contexts[0])


def _verified_direct_and_symmetric_relation_indices(model):
    direct = [
        index for index, step in enumerate(model.steps)
        if isinstance(step.conclusion, Relation)
        and step.conclusion.relation_type is RelationType.EQUALITY
        and len(step.premises) == 1
        and isinstance(step.premises[0].conclusion, GeneratorSuspension)
        and isinstance(step.conclusion.lhs, Suspension)
        and same_typed_generator(
            step.conclusion.lhs.expression,
            step.premises[0].conclusion.source_generator,
        )
        and same_typed_generator(
            step.conclusion.rhs,
            step.premises[0].conclusion.target_generator,
        )
    ]
    assert len(direct) == 1
    source_index = direct[0]
    symmetric = [
        index for index, step in enumerate(model.steps)
        if isinstance(step.conclusion, Relation)
        and step.conclusion.relation_type is RelationType.EQUALITY
        and len(step.premises) == 1
        and (step.premises[0] is model.steps[source_index]
             or step.premises[0] == model.steps[source_index])
        and step.conclusion.lhs == model.steps[source_index].conclusion.rhs
        and step.conclusion.rhs == model.steps[source_index].conclusion.lhs
    ]
    assert len(symmetric) == 1
    return source_index, symmetric[0]


def test_real_public_tree_hides_only_derived_suspension_equation_and_symmetry(
    verified_pi63,
):
    result, model = verified_pi63
    assert model.root_index is not None
    from phase168_r3_29_order_projection import project_narrative_order
    from phase168_r3_26_exactness_projection import project_exactness_chains
    chains = project_exactness_chains(model)
    omitted = {index for chain in chains for index in chain.step_indices}
    order = tuple(row.step_index for row in project_narrative_order(model, omitted))
    indices = redundant_suspension_relation_indices(model, order)
    direct, symmetric = _verified_direct_and_symmetric_relation_indices(model)
    assert indices == frozenset({direct, symmetric})
    assert all(model.steps[i].rule is ProofRule.INFERENCE for i in indices)
    assert all(not model.step_citation_numbers[i] for i in indices)
    assert any(
        child is not model.steps[symmetric]
        and any(parent is model.steps[direct] or parent == model.steps[direct]
                for parent in child.premises)
        for child in model.steps
    )
    assert any(
        any(parent is model.steps[symmetric] or parent == model.steps[symmetric]
            for parent in child.premises)
        for child in model.steps
    )
    assert result.proven_steps == model.steps


def test_real_complete_narrative_retains_cited_source_and_hopf_conclusion(
    verified_pi63,
):
    result, model = verified_pi63
    markdown = render_model_backed_narrative_markdown(result, model)
    references, body = markdown.split("\n証明\n", 1)
    assert "[R3] Chapter V, i)." in references
    assert r"[R3]より, $E(\eta_{5})=\eta_{6}$." in body
    assert r"$E\eta_{5} = \eta_{6}$." not in body
    assert r"$\eta_{6} = E\eta_{5}$." not in body
    assert "[R4] Proposition 2.2." in references
    assert "[R5] (5.3)." in references
    assert r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$." in body
    assert r"\operatorname{ord}(\nu')=4" in body
    assert len(model.citations) == 8


def test_citation_on_relation_prevents_suppression(verified_pi63):
    _, model = verified_pi63
    edited = list(model.step_citation_numbers)
    direct, symmetric = _verified_direct_and_symmetric_relation_indices(model)
    edited[direct] = (3,)
    changed = replace(model, step_citation_numbers=tuple(edited))
    order = tuple(range(len(model.steps)))
    hidden = redundant_suspension_relation_indices(changed, order)
    assert direct not in hidden and symmetric not in hidden


def test_missing_source_citation_preserves_both_lines(verified_pi63):
    _, model = verified_pi63
    edited = list(model.step_citation_numbers)
    direct, symmetric = _verified_direct_and_symmetric_relation_indices(model)
    cited_family_source = next(
        index for index, step in enumerate(model.steps)
        if type(step.conclusion).__name__ == "TodaEtaFamilyGeneralDefinition"
        and model.step_citation_numbers[index]
    )
    edited[cited_family_source] = ()
    changed = replace(model, step_citation_numbers=tuple(edited))
    order = tuple(range(len(model.steps)))
    hidden = redundant_suspension_relation_indices(changed, order)
    assert direct not in hidden and symmetric not in hidden


def test_hidden_source_or_missing_root_does_not_suppress(verified_pi63):
    _, model = verified_pi63
    order = tuple(range(len(model.steps)))
    direct, symmetric = _verified_direct_and_symmetric_relation_indices(model)
    source = model.steps[direct].premises[0]
    source_index = next(index for index, step in enumerate(model.steps)
                        if step is source or step == source)
    hidden = redundant_suspension_relation_indices(model, order, {source_index})
    assert direct not in hidden and symmetric not in hidden
    partial_like = replace(model, root_index=None)
    assert redundant_suspension_relation_indices(partial_like, order) == frozenset()


def test_typed_identity_recognizes_a_display_alias_without_matching_others(
    verified_pi63,
):
    _, model = verified_pi63
    direct, symmetric = _verified_direct_and_symmetric_relation_indices(model)
    suspension = model.steps[direct].premises[0].conclusion
    equality = model.steps[direct].conclusion
    assert isinstance(suspension, GeneratorSuspension)
    assert isinstance(equality.lhs, Suspension)
    # Two recorded names differ, but their registered structural types agree.
    assert suspension.source_generator.name != equality.lhs.expression.name
    assert same_typed_generator(
        suspension.source_generator, equality.lhs.expression,
    )
    assert not same_typed_generator(
        suspension.source_generator, suspension.target_generator,
    )
    assert not same_typed_generator(equality.lhs, suspension.source_generator)
    assert not same_typed_generator(object(), suspension.source_generator)
    assert symmetric != direct
```

## 新規 Installer（import・全関数）

追加位置：リポジトリ直下 `phase172_r3r2_r2_test_contract_correction/install.py`。

```python
"""Guarded R3 test-contract correction followed by the existing R3 runner.

This Phase 172 repair changes only one existing R2 test function. The canonical
R3 runner owns the production renderer installation and its rollback.
"""
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

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TEST_FILE = Path('phase172_r2_suspension_relation_display/tests/test_projection.py')
RENDERER = Path('phase168_r3_5_model_renderer.py')
R3_INSTALL = Path('phase172_r3_hopf_chain_display/install.py')
R3_PROJECTION = Path('phase172_r3_hopf_chain_display/projection.py')
R3_TEST = Path('phase172_r3_hopf_chain_display/tests/test_projection.py')
REVIEWED_RENDERER_BLOB = 'bb267bc669bdcaa5b9dcc24bdf7dc8b2ac4e7c95'
REVIEWED_R2_TEST_BLOB = '0656bbd9c1b02c757927ab36b8df52cee8c1f45b'
REVIEWED_R3_INSTALL_SHA256 = 'ee16868581a8496acbb76873d8c3ff39587b5b3297e7fa23040effd594ea6c8a'
REVIEWED_R3_PROJECTION_SHA256 = 'fae04a1f9e5c0a2408e8cc29180bfe64c14b8376186ba78b168db270e2e55413'
REVIEWED_R3_TEST_SHA256 = '843f889791b3a447051edfd1c22d58208cbe78e481d048c0e998443f12e8e9b6'
OLD_ASSERTION = r'''    assert r"$\nu'\eta_{6} = \nu'E\eta_{5}$." in body'''
NEW_ASSERTIONS = (
    '    assert "[R4] Proposition 2.2." in references\n'
    '    assert "[R5] (5.3)." in references'
)
TARGET_TEST_NAME = 'test_real_complete_narrative_retains_cited_source_and_hopf_conclusion'


def run_command(*args: str, timeout: int = 45) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8',
        errors='replace', check=False, timeout=timeout,
    )


def checked(*args: str) -> str:
    proc = run_command(*args)
    if proc.returncode:
        raise RuntimeError('command failed: ' + repr(args) + ': ' + proc.stderr[-900:])
    return proc.stdout.strip()


def normalize(data: bytes) -> str:
    content = data.decode('utf-8-sig')
    if '\r' in content.replace('\r\n', ''):
        raise RuntimeError('mixed newlines in checked source')
    return content.replace('\r\n', '\n')


def unique_function(source: str, name: str) -> ast.FunctionDef:
    tree = ast.parse(source)
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(functions) != 1:
        raise RuntimeError('target test function not found uniquely')
    return functions[0]


def transform_test(data: bytes) -> bytes:
    source = normalize(data)
    if source.count(OLD_ASSERTION) != 1 or NEW_ASSERTIONS in source:
        raise RuntimeError('reviewed R2 test assertion is not present exactly once')
    node = unique_function(source, TARGET_TEST_NAME)
    original_lines = source.splitlines()
    if OLD_ASSERTION not in '\n'.join(original_lines[node.lineno - 1:node.end_lineno]):
        raise RuntimeError('target assertion is outside the reviewed R2 test function')
    result = source.replace(OLD_ASSERTION, NEW_ASSERTIONS, 1)
    unique_function(result, TARGET_TEST_NAME)
    ending = '\r\n' if b'\r\n' in data else '\n'
    return result.replace('\n', ending).encode('utf-8')


def function_text(data: bytes) -> str:
    source = normalize(data)
    node = unique_function(source, TARGET_TEST_NAME)
    return '\n'.join(source.splitlines()[node.lineno-1:node.end_lineno]) + '\n'


def preflight() -> dict[str, str | None]:
    if checked('git', 'branch', '--show-current') != 'develop':
        raise RuntimeError('develop branch is required')
    head = checked('git', 'rev-parse', 'HEAD')
    if checked('git', 'rev-parse', 'HEAD:' + TEST_FILE.as_posix()) != REVIEWED_R2_TEST_BLOB:
        raise RuntimeError('committed R2 test differs from reviewed version')
    if checked('git', 'rev-parse', 'HEAD:' + RENDERER.as_posix()) != REVIEWED_RENDERER_BLOB:
        raise RuntimeError('committed Renderer differs from reviewed R2 version')
    for path in (TEST_FILE, RENDERER):
        if checked('git', 'status', '--porcelain=v1', '--', path.as_posix()):
            raise RuntimeError('tracked path has local changes: ' + str(path))
        committed = subprocess.run(
            ['git', 'show', 'HEAD:' + path.as_posix()], cwd=ROOT,
            check=True, capture_output=True,
        ).stdout
        if normalize(committed) != normalize((ROOT / path).read_bytes()):
            raise RuntimeError('worktree bytes differ from committed source: ' + str(path))
    for path, sha in (
        (R3_INSTALL, REVIEWED_R3_INSTALL_SHA256),
        (R3_PROJECTION, REVIEWED_R3_PROJECTION_SHA256),
        (R3_TEST, REVIEWED_R3_TEST_SHA256),
    ):
        if not (ROOT / path).is_file():
            raise RuntimeError('R3 prerequisite missing: ' + str(path))
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != sha:
            raise RuntimeError('R3 prerequisite changed: ' + str(path))
    existing = (ROOT / TEST_FILE).read_bytes()
    corrected = transform_test(existing)
    expected = PACKAGE / 'payload/test_projection.py'
    if normalize(corrected) != normalize(expected.read_bytes()):
        raise RuntimeError('corrected full test differs from reviewed payload')
    remote = run_command('git', 'ls-remote', 'origin', 'refs/heads/develop', timeout=25)
    remote_head = remote.stdout.split()[0] if remote.returncode == 0 and remote.stdout.strip() else None
    if remote_head is not None and remote_head != head:
        raise RuntimeError('origin/develop changed; re-review HEAD before patch')
    return {'branch': 'develop', 'head': head, 'remote': remote_head,
            'test_blob': REVIEWED_R2_TEST_BLOB,
            'renderer_blob': REVIEWED_RENDERER_BLOB,
            'corrected_test_sha256': hashlib.sha256(corrected).hexdigest()}


def output_directory() -> Path:
    base = Path(os.environ.get('LOCALAPPDATA') or Path.home()) / 'EHPProofTracerRecovery'
    directory = base / ('phase172_r3r2_' + datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%fZ'))
    directory.mkdir(parents=True, exist_ok=False)
    return directory


def local_tests(output: Path) -> None:
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONPATH'] = str(ROOT) + os.pathsep + env.get('PYTHONPATH', '')
    run = subprocess.run(
        [sys.executable, '-B', '-m', 'pytest', '-q', '--tb=short', '-p', 'no:cacheprovider',
         'phase172_r3r2_r2_test_contract_correction/tests/test_install.py'],
        cwd=ROOT, env=env, text=True, capture_output=True, encoding='utf-8',
        errors='replace', check=False, timeout=120,
    )
    log = run.stdout + '\n' + run.stderr
    (output / 'correction_tests.log').write_text(log, encoding='utf-8')
    print('PHASE172_R3R2_GUARD_TESTS=' + ('PASS' if run.returncode == 0 else 'FAIL'), flush=True)
    if run.returncode:
        raise RuntimeError('correction tests failed: ' + log[-2500:])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--run-focused-tests', action='store_true')
    args = parser.parse_args()
    state = preflight()
    output = output_directory()
    old_test = (ROOT / TEST_FILE).read_bytes()
    new_test = transform_test(old_test)
    old_renderer = (ROOT / RENDERER).read_bytes()
    (output / 'test_real_complete_narrative_FULL.py').write_text(
        function_text(new_test), encoding='utf-8',
    )
    (output / 'test_projection_FULL.py').write_bytes(new_test)
    print('PHASE172_R3R2_HEAD=' + state['head'], flush=True)
    print('PHASE172_R3R2_SOURCE_GUARD=PASS', flush=True)
    print('PHASE172_R3R2_REPORT=' + str(output), flush=True)
    if args.dry_run:
        print('PHASE172_R3R2_DRY_RUN=PASS', flush=True)
        print('PHASE172_R3R2_SOURCE_CHANGES=0', flush=True)
        return 0
    if not args.run_focused_tests:
        raise RuntimeError('apply requires --run-focused-tests')
    report = {'phase': '172-R3R2', 'state': state,
              'proof_tree_modified': False, 'math_rules_modified': False,
              'full_pytest_executed': False}
    try:
        (ROOT / TEST_FILE).write_bytes(new_test)
        local_tests(output)
        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        env['PYTHONPATH'] = str(ROOT) + os.pathsep + env.get('PYTHONPATH', '')
        proc = subprocess.run(
            [sys.executable, '-B', '-m', 'phase172_r3_hopf_chain_display.install',
             '--run-focused-tests'],
            cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8',
            errors='replace', check=False, timeout=1100,
        )
        (output / 'r3_run.log').write_text(proc.stdout + '\n' + proc.stderr, encoding='utf-8')
        if proc.stdout:
            print(proc.stdout.rstrip(), flush=True)
        if proc.returncode:
            raise RuntimeError('R3 runner failed: ' + proc.stderr[-3000:])
        if 'PHASE172_R3_RESULT=PASS_R3_HOPF_DISPLAY_ONLY' not in proc.stdout:
            raise RuntimeError('R3 runner returned no completion marker')
        report['result'] = 'PASS_R3R2_AND_R3'
        report['r3_result'] = 'PASS_R3_HOPF_DISPLAY_ONLY'
    except BaseException as error:
        (ROOT / TEST_FILE).write_bytes(old_test)
        (ROOT / RENDERER).write_bytes(old_renderer)
        report['result'] = 'FAILED_RESTORED'
        report['diagnostic'] = repr(error)
        (output / 'result.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print('PHASE172_R3R2_RESTORED=PASS', flush=True)
        raise
    (output / 'result.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PHASE172_R3R2_SOURCE_CHANGES=2', flush=True)
    print('PHASE172_R3R2_RESULT=PASS_R3R2_AND_R3', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

## 新規 PowerShell Runner

追加位置：リポジトリ直下 `phase172_r3r2_r2_test_contract_correction/run.ps1`。

```powershell
param(
    [switch]$DryRun,
    [switch]$RunFocusedTests
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldLocation = (Get-Location).Path
$OldPath = $env:PYTHONPATH
$OldUtf8 = $env:PYTHONUTF8
$OldEncoding = $env:PYTHONIOENCODING
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    Set-Location $Root
    $env:PYTHONPATH = "$Root;$OldPath"
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $Arguments = @('-B', '-m', 'phase172_r3r2_r2_test_contract_correction.install')
    if ($DryRun) {
        $Arguments += '--dry-run'
    }
    if ($RunFocusedTests) {
        $Arguments += '--run-focused-tests'
    }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R3R2 failed with exit code $LASTEXITCODE"
    }
}
finally {
    Set-Location $OldLocation
    $env:PYTHONPATH = $OldPath
    $env:PYTHONUTF8 = $OldUtf8
    $env:PYTHONIOENCODING = $OldEncoding
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
}
```

## 新規限定テスト（import・全関数）

追加位置：リポジトリ直下 `phase172_r3r2_r2_test_contract_correction/tests/test_install.py`。

```python
"""Isolated guard tests: do not need to import the production repository."""
from __future__ import annotations

import pytest

from phase172_r3r2_r2_test_contract_correction.install import (
    NEW_ASSERTIONS, OLD_ASSERTION, TARGET_TEST_NAME, function_text, normalize,
    transform_test, unique_function,
)


def source() -> bytes:
    return (
        'from __future__ import annotations\n'
        '\n'
        f'def {TARGET_TEST_NAME}(verified_pi63):\n'
        '    references = "[R4] Proposition 2.2. [R5] (5.3)."\n'
        '    body = "proof"\n'
        + OLD_ASSERTION + '\n'
    ).encode('utf-8')


def test_replaces_only_legacy_visibility_assertion():
    result = transform_test(source())
    output = normalize(result)
    assert NEW_ASSERTIONS in output
    assert OLD_ASSERTION not in output
    assert '    body = "proof"' in output
    assert TARGET_TEST_NAME in function_text(result)


def test_works_with_windows_newlines():
    baseline = source().replace(b'\n', b'\r\n')
    result = transform_test(baseline)
    assert b'\r\n' in result
    assert b'\n' not in result.replace(b'\r\n', b'')


def test_rejects_duplicate_and_missing_assertions():
    with pytest.raises(RuntimeError):
        transform_test(source() + OLD_ASSERTION.encode('utf-8') + b'\n')
    with pytest.raises(RuntimeError):
        transform_test(source().replace(OLD_ASSERTION.encode('utf-8'), b'    assert True'))


def test_rejects_reapplying_patch():
    updated = transform_test(source())
    with pytest.raises(RuntimeError):
        transform_test(updated)


def test_rejects_assertion_outside_target_function():
    bad = (
        'def ' + TARGET_TEST_NAME + '(verified_pi63):\n'
        '    assert True\n'
        '\n'
        'def unrelated():\n' + OLD_ASSERTION + '\n'
    ).encode('utf-8')
    with pytest.raises(RuntimeError):
        transform_test(bad)


def test_unique_function_rejects_ambiguous_target():
    body = normalize(source())
    with pytest.raises(RuntimeError):
        unique_function(body + '\n' + body, TARGET_TEST_NAME)
```

## 変更しないコード

Proof Tree・推論規則・検索器・Reference・DB・R3 Projection・元の R3 Installer は変更しない。既存 Renderer の変更は元の R3 ZIP の完全な関数出力に従い、今回のパッケージで新たな編集ロジックを増やさない。DryRun で関数全文が外部監査ディレクトリへ出力される。

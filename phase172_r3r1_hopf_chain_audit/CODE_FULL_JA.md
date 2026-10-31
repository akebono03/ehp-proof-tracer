# Phase 172 R3R1：追加コード全文

既存コードの変更対象はありません。追加位置はリポジトリ直下の `phase172_r3r1_hopf_chain_audit/` です。次の各ファイルを新規追加します。新規 import・関数・テストは省略せず全文を掲載します。

## `phase172_r3r1_hopf_chain_audit/audit.py`

```python
"""Phase 172 R3R1: read-only, live Hopf proof-chain display audit.

This module does not modify mathematical conclusions, ProofSteps, citations,
renderers or tracked repository files. It does not import a historical proof.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from expression import MapApplication
from map_facts import EHP_H_MAP
from proof import ProofRule, Relation, RelationType
from web_group_proof_common import _group_proof_statement_latex

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
RENDERER = Path('phase168_r3_5_model_renderer.py')
R2_PROJECTION = Path('phase172_r2_suspension_relation_display/projection.py')
R2_TEST = Path('phase172_r2_suspension_relation_display/tests/test_projection.py')
EXPECTED_HEAD_RENDERER_BLOB = '94996b403f1c01f81319824565db422463714f02'
EXPECTED_R2_PROJECTION_SHA256 = 'a7d7072d2adfcdbc17e27200241b5240b0ab17148c60811388e2543df9c09818'
EXPECTED_R2_TEST_SHA256 = 'c021fae71c00e64589685e12061dbb6022ca22189c9ae7599f0a19a7a0ed4036'
FOCUSED = (
    ('phase172_r2_suspension_relation_display/tests/test_projection.py',),
    ('phase171_r20r13_eta_sentence_layout/tests/test_projection.py',),
    ('phase172_r3r1_hopf_chain_audit/tests/test_audit.py',),
)


def command(args: list[str], *, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, encoding='utf-8', errors='replace',
                          check=False, timeout=timeout)


def git(*args: str) -> str:
    allowed = {'branch', 'rev-parse', 'status', 'ls-remote', 'show'}
    if not args or args[0] not in allowed:
        raise ValueError('only read-only Git observations are supported')
    process = command(['git', *args])
    if process.returncode:
        raise RuntimeError('Git observation failed: ' + repr(args) + ' ' + process.stderr[-800:])
    return process.stdout.strip()


def normalize(source: bytes) -> bytes:
    data = source.decode('utf-8-sig')
    if '\r' in data.replace('\r\n', ''):
        raise RuntimeError('mixed/unknown source newlines')
    return data.replace('\r\n', '\n').encode('utf-8')


def sha256(source: bytes) -> str:
    return hashlib.sha256(normalize(source)).hexdigest()


def preflight() -> dict[str, Any]:
    branch = git('branch', '--show-current')
    head = git('rev-parse', 'HEAD')
    if branch != 'develop':
        raise RuntimeError('Phase 172 R3R1 requires develop; nothing changed')
    blob = git('rev-parse', 'HEAD:' + RENDERER.as_posix())
    if blob != EXPECTED_HEAD_RENDERER_BLOB:
        raise RuntimeError('committed Renderer differs from the reviewed Phase 172 R2 baseline')
    # The current R2 is an expected uncommitted 9-line Renderer patch. Compare
    # against its reviewed pure transformation rather than a loose text marker.
    from phase172_r2_suspension_relation_display.install import transformed
    original = subprocess.run(['git', 'show', 'HEAD:' + RENDERER.as_posix()],
                              cwd=ROOT, capture_output=True, check=True).stdout
    expected = transformed(original)
    actual = (ROOT / RENDERER).read_bytes()
    if normalize(actual) != normalize(expected):
        raise RuntimeError('R2 Renderer is absent or differs from its reviewed patch')
    for path, expected_sha in (
        (R2_PROJECTION, EXPECTED_R2_PROJECTION_SHA256),
        (R2_TEST, EXPECTED_R2_TEST_SHA256),
    ):
        if not (ROOT / path).is_file() or sha256((ROOT / path).read_bytes()) != expected_sha:
            raise RuntimeError('R2R1 corrected source/test mismatch: ' + str(path))
    before = git('status', '--porcelain=v1', '--untracked-files=no')
    # Never fetch or pull automatically. Record whether the remote can be seen.
    remote = command(['git', 'ls-remote', 'origin', 'refs/heads/develop'], timeout=25)
    remote_head = (remote.stdout.split()[0] if remote.returncode == 0 and remote.stdout.strip()
                   else None)
    if remote_head is not None and remote_head != head:
        raise RuntimeError('origin/develop advanced; inspect current code before R3')
    return {
        'branch': branch, 'local_head': head, 'remote_develop_head': remote_head,
        'remote_reachable': remote_head is not None,
        'head_renderer_blob': blob, 'r2_renderer_installed': True,
        'r2_projection_sha256': EXPECTED_R2_PROJECTION_SHA256,
        'r2_test_sha256': EXPECTED_R2_TEST_SHA256,
        'tracked_status_before': before,
    }


def index_for(node: object, steps: tuple[object, ...]) -> int:
    identity = [i for i, item in enumerate(steps) if item is node]
    if len(identity) == 1:
        return identity[0]
    if identity:
        raise ValueError('ambiguous identity-indexed ProofStep')
    equal = [i for i, item in enumerate(steps) if item == node]
    if len(equal) != 1:
        raise ValueError('missing/ambiguous ProofStep premise')
    return equal[0]


def is_hopf_relation(statement: object) -> bool:
    return (
        isinstance(statement, Relation)
        and statement.relation_type is RelationType.EQUALITY
        and isinstance(statement.lhs, MapApplication)
        and statement.lhs.map == EHP_H_MAP
    )


def hopf_chain_roots(model: object) -> tuple[int, int]:
    """Use an inferred surjectivity with a proved H-image as its direct premise."""
    steps = model.steps
    if model.root_index is None:
        raise ValueError('completed root missing')
    ancestry = root_ancestor_step_indices(steps, model.root_index)
    candidates: list[tuple[int, int]] = []
    for i in sorted(ancestry):
        step = steps[i]
        if (step.rule is not ProofRule.INFERENCE
                or not isinstance(step.conclusion, MapSurjective)):
            continue
        for parent in step.premises:
            if (parent.rule is ProofRule.INFERENCE
                    and is_hopf_relation(parent.conclusion)):
                parent_index = index_for(parent, steps)
                if parent_index in ancestry:
                    candidates.append((i, parent_index))
    if len(candidates) != 1:
        raise ValueError('expected one proved Hopf-image surjectivity chain; got '
                         + str(len(candidates)))
    return candidates[0]


def descendants_of_proof_premises(steps: tuple[object, ...], root: int) -> tuple[int, ...]:
    """List only the actual verified premise closure of the selected proof step."""
    used: set[int] = set()
    pending = [root]
    while pending:
        i = pending.pop()
        if i in used:
            continue
        used.add(i)
        pending.extend(index_for(p, steps) for p in steps[i].premises)
    return tuple(sorted(used))


def exact_math_line_candidates(body_lines: list[str], latex: str | None) -> list[dict[str, object]]:
    """Report textual candidates, not a claim of mathematical equivalence."""
    if not latex:
        return []
    needle = '$' + latex + '$'
    return [
        {'line_number': i + 1, 'text': text}
        for i, text in enumerate(body_lines)
        if needle in text
    ]


def output_directory() -> Path:
    base = Path(os.environ.get('LOCALAPPDATA') or Path.home())
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%fZ')
    path = base / 'EHPProofTracerRecovery' / ('phase172_r3r1_' + stamp)
    path.mkdir(parents=True, exist_ok=False)
    return path


def save_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def capture_canonical_hopf_chain() -> dict[str, Any]:
    bridge = build_shared_typed_bridge()
    contexts: list[object] = []
    result = search_group_from_registered_goal(n=3, k=3, bridge=bridge,
                                               context_sink=contexts.append)
    if (result.status is not ProofSearchStatus.COMPLETE or result.open_goals
            or len(contexts) != 1):
        raise RuntimeError('canonical π6^3 proof is not verified complete')
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing is None:
        raise RuntimeError('citing source for π6^3 missing')
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    web = build_partial_web_group_proof_view(result, max_depth=2, mode='narrative',
                                             narrative_model=model)
    if web.key != 'generic-complete-proof' or web.partial_result or not web.rendered_lines:
        raise RuntimeError('verified public narrative display is not complete')
    markdown = render_model_backed_narrative_markdown(result, model)
    if '\n証明\n' not in markdown:
        raise RuntimeError('completed proof body absent')
    reference_text, body = markdown.split('\n証明\n', 1)
    if len(model.citations) != 8 or model.root_index is None:
        raise RuntimeError('Phase 171 citation/root baseline changed; audit blocked')
    surj_index, image_index = hopf_chain_roots(model)
    closure = descendants_of_proof_premises(model.steps, image_index)
    body_lines = body.splitlines()
    step_records: list[dict[str, Any]] = []
    for index in closure:
        step = model.steps[index]
        latex, fallback = _group_proof_statement_latex(step.conclusion)
        step_records.append({
            'index': index, 'role': step.rule.value, 'statement_type': type(step.conclusion).__name__,
            'statement_repr': repr(step.conclusion)[:2600],
            'inference_name_diagnostic_only': (step.inference_rule.name
                                                if step.inference_rule is not None else None),
            'premise_indices': [index_for(p, model.steps) for p in step.premises],
            'direct_citations': list(model.step_citation_numbers[index]),
            'renderable_latex': latex, 'fallback_type': fallback,
            'typed_sentence': typed_sentence(step.conclusion, step),
            'body_math_candidates': exact_math_line_candidates(body_lines, latex),
        })
    source_citation_numbers = sorted({
        number for index in closure for number in model.step_citation_numbers[index]
    })
    references = [{
        'number': item.number, 'locator': item.reference.locator or item.reference.label,
        'statement_bodies': list(item.statement_bodies),
        'all_step_indices': list(item.step_indices),
        'supports_chain': item.number in source_citation_numbers,
    } for item in model.citations]
    target_latex, target_fallback = _group_proof_statement_latex(model.steps[image_index].conclusion)
    if target_latex is None or target_fallback is not None:
        raise RuntimeError('Hopf image has no supported public math representation')
    if not exact_math_line_candidates(body_lines, target_latex):
        raise RuntimeError('proved Hopf image disappeared from public narrative')
    return {
        'status': result.status.value, 'web_key': web.key, 'open_goals': len(result.open_goals),
        'step_count': len(model.steps), 'reference_count': len(model.citations),
        'root_step_index': model.root_index, 'surjective_step_index': surj_index,
        'hopf_image_step_index': image_index, 'hopf_target_latex': target_latex,
        'chain_premise_indices': list(closure),
        'chain_cited_reference_numbers': source_citation_numbers,
        'step_records': step_records, 'references': references,
        'reference_text': reference_text, 'body_lines': body_lines,
        'web_rendered_lines_count': len(web.rendered_lines), 'markdown': markdown,
    }


def findings(snapshot: dict[str, Any], state: dict[str, Any]) -> str:
    refs = ', '.join(f'[R{n}]' for n in snapshot['chain_cited_reference_numbers'])
    selected = [r for r in snapshot['step_records'] if r['body_math_candidates']]
    lines = [
        '# Phase 172 R3R1：Hopf 導出表示の監査結果', '',
        '## 確認した実行状態', '',
        f"- local HEAD: `{state['local_head']}`",
        f"- Proof Search: `{snapshot['status']}`、Web: `{snapshot['web_key']}`",
        f"- ProofStep: {snapshot['step_count']} 件、Reference: {snapshot['reference_count']} 件、未解決 Goal: {snapshot['open_goals']} 件",
        f"- 監査した Hopf 像 Step: {snapshot['hopf_image_step_index']}（全射性 Step: {snapshot['surjective_step_index']}）",
        f"- Hopf 像の前提閉包: {len(snapshot['chain_premise_indices'])} 件",
        f'- 前提閉包内の直接 Citation: {refs}', '',
        '## 表示対応の候補', '',
        '以下は数式の完全一致による表示行の対応候補。等式の数学的同値性の判定ではない。', '',
    ]
    for row in selected:
        line_numbers = ', '.join(str(v['line_number']) for v in row['body_math_candidates'])
        lines.append(f"- Step {row['index']}（{row['statement_type']}、行 {line_numbers}）: `${row['renderable_latex']}$")
    lines += [
        '', '## R3 の変更判断に必要な条件', '',
        '- 出典 [R3]・[R4]・[R5] が ProofStep の前提閉包を通じて保持されること。',
        '- 最終 Hopf 等式と、その利用による全射性の根拠が本文に残ること。',
        '- 中間式の削除候補は依存関係を完全に確認し、各既存 Citation の意味を曖昧にしないこと。',
        '- 表示だけを変更し、Proof Tree・Reference・既知の群構造・Backward Search に手を加えないこと。',
        '- この R3R1 は AUDIT_ONLY。R3 の表示変更は別工程で審査する。', '',
    ]
    return '\n'.join(lines)


def run_focused(output: Path) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONPATH'] = str(ROOT) + os.pathsep + env.get('PYTHONPATH', '')
    for number, paths in enumerate(FOCUSED, 1):
        result = subprocess.run(
            [sys.executable, '-B', '-m', 'pytest', '-q', '--tb=short',
             '-p', 'no:cacheprovider', *paths],
            cwd=ROOT, env=env, text=True, encoding='utf-8', errors='replace',
            capture_output=True, check=False,
        )
        log = result.stdout + '\n' + result.stderr
        (output / f'focused_{number}.log').write_text(log, encoding='utf-8')
        print(f'PHASE172_R3R1_FOCUSED_{number}=' + ('PASS' if result.returncode == 0 else 'FAIL'), flush=True)
        results.append({'group': number, 'paths': list(paths), 'exit': result.returncode,
                        'tail': log.splitlines()[-12:]})
        if result.returncode:
            raise RuntimeError('focused pytest failed: ' + str(number) + '\n' + log[-1800:])
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--run-focused-tests', action='store_true')
    args = parser.parse_args()
    state = preflight()
    print('PHASE172_R3R1_BRANCH=' + state['branch'], flush=True)
    print('PHASE172_R3R1_HEAD=' + state['local_head'], flush=True)
    print('PHASE172_R3R1_REMOTE=' + str(state['remote_develop_head']), flush=True)
    print('PHASE172_R3R1_R2_BASELINE=PASS', flush=True)
    print('PHASE172_R3R1_SOURCE_CHANGES=0', flush=True)
    if args.dry_run:
        print('PHASE172_R3R1_DRY_RUN=PASS', flush=True)
        return 0
    out = output_directory()
    report: dict[str, Any] = {'phase': '172-R3R1', 'mode': 'AUDIT_ONLY', 'git': state,
                              'full_pytest_executed': False, 'production_source_changes': 0}
    try:
        snapshot = capture_canonical_hopf_chain()
        report['public'] = {k: v for k, v in snapshot.items() if k in (
            'status', 'web_key', 'open_goals', 'step_count', 'reference_count',
            'root_step_index', 'surjective_step_index', 'hopf_image_step_index',
            'hopf_target_latex', 'chain_premise_indices',
            'chain_cited_reference_numbers', 'web_rendered_lines_count')}
        save_json(out / 'hopf_steps.json', snapshot['step_records'])
        save_json(out / 'reference_provenance.json', snapshot['references'])
        save_json(out / 'hopf_display_alignment.json', [
            {'step_index': item['index'], 'body_line_candidates': item['body_math_candidates']}
            for item in snapshot['step_records']
        ])
        (out / 'web_narrative.md').write_text(snapshot['markdown'], encoding='utf-8')
        (out / 'AUDIT_FINDINGS_JA.md').write_text(findings(snapshot, state), encoding='utf-8')
        print('PHASE172_R3R1_PUBLIC_STATUS=' + snapshot['status'], flush=True)
        print('PHASE172_R3R1_WEB_KEY=' + snapshot['web_key'], flush=True)
        print('PHASE172_R3R1_OPEN_GOALS=' + str(snapshot['open_goals']), flush=True)
        print('PHASE172_R3R1_PROOF_STEPS=' + str(snapshot['step_count']), flush=True)
        print('PHASE172_R3R1_REFERENCES=' + str(snapshot['reference_count']), flush=True)
        print('PHASE172_R3R1_HOPF_IMAGE_STEP=' + str(snapshot['hopf_image_step_index']), flush=True)
        if args.run_focused_tests:
            report['focused'] = run_focused(out)
        if git('status', '--porcelain=v1', '--untracked-files=no') != state['tracked_status_before']:
            raise RuntimeError('tracked worktree changed during audit')
        report['result'] = 'PASS_R3R1_AUDIT_ONLY'
        result_code = 0
    except Exception as error:
        report['result'] = 'FAIL_R3R1_AUDIT'
        report['diagnostic'] = repr(error)
        result_code = 1
        print('PHASE172_R3R1_ERROR=' + repr(error), flush=True)
    save_json(out / 'audit.json', report)
    print('PHASE172_R3R1_REPORT=' + str(out), flush=True)
    print('PHASE172_R3R1_RESULT=' + str(report['result']), flush=True)
    return result_code


if __name__ == '__main__':
    sys.exit(main())
```

## `phase172_r3r1_hopf_chain_audit/tests/test_audit.py`

```python
"""Small, source-independent tests for R3R1 diagnostic helpers."""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from expression import HomotopyElement, MapApplication
from map_facts import EHP_H_MAP
from phase172_r3r1_hopf_chain_audit.audit import (
    descendants_of_proof_premises,
    exact_math_line_candidates,
    index_for,
    is_hopf_relation,
)
from proof import Relation, RelationType


@dataclass(frozen=True)
class Node:
    name: str
    premises: tuple[object, ...] = ()


def test_index_for_unique_identity_and_equal_value():
    steps = (Node('premise'), Node('conclusion'))
    assert index_for(steps[0], steps) == 0
    assert index_for(Node('premise'), steps) == 0


def test_index_for_fails_closed_when_missing_or_ambiguous():
    with pytest.raises(ValueError):
        index_for(Node('absent'), (Node('premise'),))
    with pytest.raises(ValueError):
        index_for(Node('same'), (Node('same'), Node('same')))


def test_descendants_traverse_actual_premise_closure():
    a = Node('a')
    b = Node('b', (a,))
    c = Node('c', (b, a))
    assert descendants_of_proof_premises((a, b, c), 2) == (0, 1, 2)
    assert descendants_of_proof_premises((a, b, c), 0) == (0,)


def test_line_correspondence_requires_an_exact_math_block():
    body = ['$H(x)=y$.', '$H(x)=yz$.', '$H(x)=y$ は結論.', '文字列 H(x)=y']
    candidates = exact_math_line_candidates(body, 'H(x)=y')
    assert [x['line_number'] for x in candidates] == [1, 3]
    assert exact_math_line_candidates(body, None) == []


def test_hopf_relation_requires_typed_map_and_equality():
    x = HomotopyElement('x', 3)
    y = HomotopyElement('y', 3)
    target = Relation(MapApplication(EHP_H_MAP, x), y, RelationType.EQUALITY)
    assert is_hopf_relation(target)
    assert not is_hopf_relation(Relation(x, y, RelationType.EQUALITY))
    assert not is_hopf_relation('H(x)=y')
```

## `phase172_r3r1_hopf_chain_audit/run.ps1`

```powershell
param(
    [switch]$DryRun,
    [switch]$RunFocusedTests
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldLocation = (Get-Location).Path
$OldPythonPath = $env:PYTHONPATH
$OldPythonUTF8 = $env:PYTHONUTF8
$OldPythonEncoding = $env:PYTHONIOENCODING
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE
try {
    Set-Location $Root
    $env:PYTHONPATH = "$Root;$OldPythonPath"
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $Arguments = @('-B', '-m', 'phase172_r3r1_hopf_chain_audit.audit')
    if ($DryRun) {
        $Arguments += '--dry-run'
    }
    if ($RunFocusedTests) {
        $Arguments += '--run-focused-tests'
    }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R3R1 audit failed with exit code $LASTEXITCODE"
    }
}
finally {
    Set-Location $OldLocation
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONUTF8 = $OldPythonUTF8
    $env:PYTHONIOENCODING = $OldPythonEncoding
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
}
```

## `phase172_r3r1_hopf_chain_audit/__init__.py`

```python
"""Read-only Phase 172 R3R1 Hopf-chain audit."""
```


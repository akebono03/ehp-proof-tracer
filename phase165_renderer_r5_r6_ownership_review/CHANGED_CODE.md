# R5-R6: 新規実装全文

以下は ZIP に収録した新規ファイルの全文。既存 import・クラス・関数の変更はありません。

## audit.py

```python
"""Phase 165 R5-R6: read-only ownership assessment of 26 Renderer candidates."""
from __future__ import annotations
import ast
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
PRIOR = PROJECT / 'phase165_renderer_r5_r5_callgraph_audit' / 'audit.py'
OUT = ROOT / 'audit_output'

# Deliberately explicit: no function is declared safe on the basis of its name alone.
HISTORICAL = {
 'toda_group_proof_generic_narrative_renderer.phase165_r42_backup.py',
 'toda_group_proof_generic_narrative_renderer.phase165_r48_backup.py',
 'toda_group_proof_generic_narrative_renderer.phase165_r48_sidecar_backup.py',
 'toda_group_proof_narrative_renderer.phase165_r43_backup.py',
 'toda_group_proof_narrative_renderer.phase165_r44_pre_cleanup.py',
 'toda_group_proof_narrative_renderer.phase165_r48_backup.py',
}
OWNED_PARTIAL = {'phase165_r57_r2_partial_narrative.py','phase165_r57_r10_step_narrative.py'}
# These functions are known to be mathematical-format / section subroutines; still require route audit.
HELPER_COMPONENTS = {
 'toda_group_proof_aggregate_statement_renderer.py',
 'toda_group_proof_narrative_argument_body_renderer.py',
 'toda_group_proof_narrative_argument_discourse.py',
 'toda_group_proof_narrative_argument_multi_renderer.py',
 'toda_group_proof_narrative_argument_renderer.py',
 'toda_group_proof_narrative_argument_single_renderer.py',
 'toda_group_proof_narrative_contribution_renderer.py',
 'toda_group_proof_narrative_exactness_method_renderer.py',
 'toda_group_proof_narrative_reason_renderer.py',
 'toda_group_proof_narrative_references.py',
 'toda_group_proof_narrative_transition_renderer.py',
}
SEPARATE_PRESENTATION_SURFACES = {
 'toda_full_proof_report_renderer.py',
 'toda_group_proof_outline_renderer.py',
 'toda_group_result_proof_replay_renderer.py',
 'toda_proof_narrative_renderer.py',
}
LEGACY_CHAINS = {
 'phase162_r3_narrative_connection.py',
 'toda_group_proof_narrative_concrete_transport.py',
 'toda_group_proof_narrative_proof_chain_renderer.py',
}
FOCUS = {
 'web_group_proof.py', 'phase165_r52_r3_web_adapter.py',
 'phase165_r52_partial_proof.py','toda_group_proof_narrative_renderer.py',
 'phase165_r56_presentation_adapter.py','phase165_r57_r2_partial_narrative.py',
 'phase162_web_narrative_integration.py','phase162_validated_proof_presentation.py',
 'cli.py','main.py',
}


def load_prior():
    if not PRIOR.is_file():
        raise FileNotFoundError('Required R5-R5 package not found: ' + str(PRIOR))
    spec = importlib.util.spec_from_file_location('r5_r5_read_only',PRIOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def category(path: str) -> str:
    if path in HISTORICAL: return 'HISTORICAL_BACKUP'
    if path in OWNED_PARTIAL: return 'CANONICAL_OWNED_SUBROUTINE_REVIEW'
    if path in HELPER_COMPONENTS: return 'SECTION_OR_MATH_COMPONENT_REVIEW'
    if path in SEPARATE_PRESENTATION_SURFACES: return 'OTHER_PRESENTATION_SURFACE_REVIEW'
    if path in LEGACY_CHAINS: return 'LEGACY_OR_SPECIALIZED_CHAIN_REVIEW'
    raise ValueError('Unclassified candidate: ' + path)


def extract_references(source: str, module_names: set[str]) -> list[dict]:
    tree = ast.parse(source)
    items = []
    for node in ast.walk(tree):
        if isinstance(node,ast.ImportFrom) and node.module in module_names:
            for alias in node.names:
                items.append({'kind':'from','module':node.module,'name':alias.name,'line':node.lineno})
        elif isinstance(node,ast.Import):
            for alias in node.names:
                if alias.name in module_names:
                    items.append({'kind':'import','module':alias.name,'name':'*','line':node.lineno})
    return sorted(items,key=lambda x:(x['line'],x['module'],x['name']))


def main():
    prior = load_prior().analyze(PROJECT)
    rows = []
    for c in prior['classifications']:
        path = c['path']
        rows.append({'file':path,'category':category(path),'functions':c['functions'],
                     'direct_callers':c['callers'],
                     'canonical_direct_caller': 'toda_group_proof_narrative_renderer.py' in c['callers'],
                     'production_direct_callers':[x for x in c['callers'] if not x.startswith(('tests/','audit_')) and x not in HISTORICAL],
                     'prior_role':c['role']})
    expected = HISTORICAL|OWNED_PARTIAL|HELPER_COMPONENTS|SEPARATE_PRESENTATION_SURFACES|LEGACY_CHAINS
    actual = {row['file'] for row in rows}
    missing, extra = sorted(expected-actual), sorted(actual-expected)
    focus = {}
    modules = {Path(x).stem for x in actual}|{'toda_group_proof_narrative_renderer', 'phase165_r52_partial_proof','phase165_r56_presentation_adapter'}
    for name in sorted(FOCUS):
        file = PROJECT/name
        if not file.exists():
            focus[name]={'present':False,'imports':[]}
            continue
        source=file.read_text(encoding='utf-8-sig')
        focus[name]={'present':True,'imports':extract_references(source,modules)}
    status = 'REVIEW_REQUIRED' if not (missing or extra) else 'CLASSIFICATION_MISMATCH'
    data = {'phase':'165 R5-R6','status':status,'timestamp_utc':datetime.now(timezone.utc).isoformat(),
            'counts':{'candidates':len(rows),'historical_backups':sum(x['category']=='HISTORICAL_BACKUP' for x in rows),
                      'owned_subroutine_review':sum(x['category']=='CANONICAL_OWNED_SUBROUTINE_REVIEW' for x in rows),
                      'component_review':sum(x['category']=='SECTION_OR_MATH_COMPONENT_REVIEW' for x in rows),
                      'other_presentation_review':sum(x['category']=='OTHER_PRESENTATION_SURFACE_REVIEW' for x in rows),
                      'legacy_chain_review':sum(x['category']=='LEGACY_OR_SPECIALIZED_CHAIN_REVIEW' for x in rows)},
            'missing_categories':missing,'extra_candidates':extra,'candidates':rows,'focus_imports':focus,
            'limitations':['Static imports do not certify runtime control flow or absence of dynamic imports.',
                           'The Phase162 fixture regression remains unresolved.',
                           'No source code is changed; full pytest is not run.',
                           'Categories are investigative ownership buckets, not integration certification.']}
    OUT.mkdir(exist_ok=True)
    (OUT/'audit.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Phase 165 R5-R6 所有経路の分類監査','',f"判定: **{status}**",'',
           '## 件数','']
    lines += [f'- {k}: {v}' for k,v in data['counts'].items()]
    lines += ['', '## 26候補の分類（未認定）','']
    for row in rows:
        lines += [f"### `{row['file']}`", f"- 分類: `{row['category']}`",
                  '- 関数: '+', '.join('`'+x+'`' for x in row['functions']),
                  '- 本番呼出元: '+(', '.join('`'+x+'`' for x in row['production_direct_callers']) or '静的検出なし'),
                  '- 正規 Renderer から直接呼び出し: '+str(row['canonical_direct_caller']), '']
    lines += ['## 主要な公開経路の import 証拠','']
    for name,entry in focus.items():
        lines += [f'### `{name}`']
        if not entry['present']: lines += ['- ファイル未検出（要確認）']
        else:
            lines += [f"- `{r['line']}`: `{r['module']}.{r['name']}`" for r in entry['imports']] or ['- 対象 import なし']
        lines += ['']
    lines += ['## 次に手動で判断する境界','',
              '- Group Proof の Web 公開入口と、旧 Phase162 Web 入口が並行して有効か',
              '- 完成証明の Provenance を維持したまま単一 Dispatcher が所有できるか',
              '- CLI / Generator / Outline / Replay の表示を Group Proof Narrative と混同していないか',
              '- 候補以外の独立 Narrative 関数が未検出のまま残っていないか',
              '- 旧 Phase162 fixture 失敗6件は今回未解決','', '## 限界','']
    lines += ['- '+x for x in data['limitations']]
    (OUT/'review.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'status':status,'counts':data['counts'],
                      'missing_categories':missing,'extra_candidates':extra,
                      'report':str(OUT/'review.md'),'full_pytest_run':False},ensure_ascii=False,indent=2))
    if missing or extra: raise SystemExit(1)

if __name__ == '__main__': main()

```

## test_audit.py

```python
"""Narrow tests for the read-only ownership audit."""
import pytest
from audit import category, extract_references, HISTORICAL, OWNED_PARTIAL, HELPER_COMPONENTS, SEPARATE_PRESENTATION_SURFACES, LEGACY_CHAINS


def test_category_sets_are_disjoint():
    groups=[HISTORICAL,OWNED_PARTIAL,HELPER_COMPONENTS,SEPARATE_PRESENTATION_SURFACES,LEGACY_CHAINS]
    assert sum(map(len,groups))==len(set().union(*groups))==26


def test_historical_never_classified_as_active():
    assert all(category(x)=='HISTORICAL_BACKUP' for x in HISTORICAL)


def test_partial_is_not_declared_independent_or_certified():
    assert category('phase165_r57_r2_partial_narrative.py')=='CANONICAL_OWNED_SUBROUTINE_REVIEW'


def test_phase162_chain_requires_review():
    assert category('phase162_r3_narrative_connection.py')=='LEGACY_OR_SPECIALIZED_CHAIN_REVIEW'


def test_unknown_candidate_causes_failure():
    with pytest.raises(ValueError,match='Unclassified'):
        category('new_unexpected_narrative_renderer.py')


def test_import_evidence_tracks_from_and_import():
    source='from phase162_r3_narrative_connection import render_phase162_r3_narrative\nimport toda_group_proof_narrative_renderer\n'
    result=extract_references(source,{'phase162_r3_narrative_connection','toda_group_proof_narrative_renderer'})
    assert [(x['kind'],x['line']) for x in result]==[('from',1),('import',2)]

```

## run.ps1

```powershell
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$env:PYTHONPATH = "$project$([IO.Path]::PathSeparator)$package$([IO.Path]::PathSeparator)$env:PYTHONPATH"
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
& $python -m pytest -q (Join-Path $package 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R5-R6 audit unit tests failed' }
& $python (Join-Path $package 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R5-R6 classification mismatch; report saved' }
Write-Output 'R5-R6 ownership classification complete; review required. No application source changes or full pytest.'

```

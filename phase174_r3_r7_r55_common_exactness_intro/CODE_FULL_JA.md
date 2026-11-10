# R55 コード全文（追加ファイル）

既存 Renderer の変更前・変更後の**関数全文**は、ハッシュ検証付きインストール時に実ソースから `FULL_CHANGED_FUNCTIONS.md` に自動生成される。`CODE_FULL_JA.md` は新規コード全文（省略なし）を収録する。

既存ファイルの変更は `render_model_backed_narrative_markdown()` の完全列導入部だけ。既存 import の変更はない。

## `source_guard.py` 全文

```python
"""R55: pin the GitHub-reviewed mathematical and common-Renderer sources."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TARGET = 'phase168_r3_5_model_renderer.py'
REVIEWED_HEAD = '40db3a00ca8be58e589e0949e6a70dcedd3b9cf5'
BLOBS = {
    TARGET: '64e0570e8462ee0361ed07afab836c66ce8e7895',
    'phase168_r3_26_exactness_projection.py': 'a62fef3bce2150510e1c487ac6c381227b9a0860',
    'web_group_proof.py': '2c66da9c8e80a13812a63b6adda34c9414d8413c',
    'web_app.py': '6f95663df5cbf028bb16d1f05dca62db2e3fc00e',
    'templates/index.html': '7af2afa40b92b8c1ec3916cf9759516c158b989f',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
    'phase165_r52_r3_web_adapter.py': 'dda215780c0468cf421592aff86c79b1f5482eed',
    'phase174_r3_r7_r54_public_http_narrative_audit/audit.py': '505192a0e166672908322a8e6a2de4f59f23a6ab',
    'phase174_r3_r7_r54_public_http_narrative_audit/tests/test_http.py': 'f7c72f95d055a9d9fd7f7f13529b740a6c431334',
}


def git(*args: str) -> bytes:
    proc = subprocess.run(('git',) + args,cwd=ROOT,capture_output=True,check=True)
    return proc.stdout


def sha_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode('ascii')+b'\0'+data).hexdigest()


def verify_checkout() -> dict[str, object]:
    """Verify HEAD, index, all reviewed blobs, and the exact renderer patch."""
    from phase174_r3_r7_r55_common_exactness_intro.patch import replace_lines_preserving_eol
    if Path(git('rev-parse','--show-toplevel').decode().strip()).resolve()!=ROOT.resolve():
        raise RuntimeError('R55 directory must be unpacked under repo root')
    if git('branch','--show-current').decode().strip()!='develop':
        raise RuntimeError('R55 expects develop')
    head=git('rev-parse','HEAD').decode().strip()
    remote=git('ls-remote','origin','refs/heads/develop').decode().strip().split()
    if head!=REVIEWED_HEAD or not remote or remote[0]!=REVIEWED_HEAD:
        raise RuntimeError('R55 requires the reviewed live GitHub develop HEAD')
    if git('diff','--cached','--name-only').strip():
        raise RuntimeError('Staged files require separate review')
    changed=tuple(git('diff','--name-only').decode().splitlines())
    if changed not in ((),(TARGET,)):
        raise RuntimeError('R55 found unrelated tracked edits: '+repr(changed))
    for file,blob in BLOBS.items():
        baseline=git('show','HEAD:'+file)
        if sha_blob(baseline)!=blob:
            raise RuntimeError('Reviewed GitHub mathematical or renderer source changed: '+file)
        actual=(ROOT/file).read_bytes()
        if file != TARGET and actual.replace(b'\r\n',b'\n')!=baseline.replace(b'\r\n',b'\n'):
            raise RuntimeError('Tracked source differs from GitHub HEAD: '+file)
    previous=git('show','HEAD:'+TARGET)
    actual=(ROOT/TARGET).read_bytes()
    def norm(blob:bytes)->str:
        return blob.decode('utf-8-sig').replace('\r\n','\n')
    desired=replace_lines_preserving_eol(norm(previous))
    installed=(norm(actual)==norm(desired))
    if changed==() and norm(actual)!=norm(previous):
        raise RuntimeError('Renderer changed without Git status evidence')
    if changed==(TARGET,) and not installed:
        raise RuntimeError('Unreviewed renderer edit or mixed patch')
    return {
        'source_guard':'PASS', 'local_head':head,'remote_head':remote[0],
        'reviewed_blobs':len(BLOBS),'tracked_changes':changed,
        'r55_renderer_installed':installed,
        'new_given':0,'new_mathematical_rules':0,'full_pytest':False,
    }
```

## `patch.py` 全文

```python
"""SHA-pinned, newline-preserving repair of only exactness-chain prose.

No ProofStep, inference, citation number, chain, or mathematical rule is changed.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

from phase174_r3_r7_r55_common_exactness_intro.source_guard import ROOT, TARGET, verify_checkout

BASELINE_BLOB = "64e0570e8462ee0361ed07afab836c66ce8e7895"
BEFORE_CHAIN = '    for chain in chains:'
AFTER_CHAIN = '    for chain_index, chain in enumerate(chains):'
BEFORE_INTRO = (
    '        if exactness_numbers:',
    '            tags = ", ".join(f"[R{number}]" for number in exactness_numbers)',
    '            lines.append(f"${group_tex(model.target)}$の群構造を決定するために, {tags}を用いて次の完全列を考える.")',
    '        else:',
    '            lines.append(f"${group_tex(model.target)}$の群構造を決定するために, 次の完全列を考える.")',
)
AFTER_INTRO = (
    '        prefix = (',
    '            f"${group_tex(model.target)}$の群構造を決定するために, "',
    '            if chain_index == 0 else "さらに, "',
    '        )',
    '        if exactness_numbers:',
    '            tags = ", ".join(f"[R{number}]" for number in exactness_numbers)',
    '            lines.append(f"{prefix}{tags}を用いて次の完全列を考える.")',
    '        else:',
    '            lines.append(f"{prefix}次の完全列を考える.")',
)


def normalized(value: bytes) -> bytes:
    return value.replace(b"\r\n", b"\n")


def lines_without_terminator(value: str) -> list[str]:
    return [line.rstrip('\r\n') for line in value.splitlines(keepends=True)]


def replace_lines_preserving_eol(source: str) -> str:
    """Replace only two reviewed syntactic units, retaining every original EOL."""
    lines = source.splitlines(keepends=True)
    text = lines_without_terminator(source)
    if text.count(AFTER_CHAIN) == 1 and text.count(BEFORE_CHAIN) == 0:
        if any(text[index:index + len(AFTER_INTRO)] == list(AFTER_INTRO)
               for index in range(len(text))):
            return source
        raise RuntimeError('Partial R55 patch installation detected')
    if text.count(BEFORE_CHAIN) != 1 or text.count(AFTER_CHAIN) != 0:
        raise RuntimeError('R55 exactness-chain iteration contract changed')
    origins = [i for i in range(len(text))
               if text[i:i+len(BEFORE_INTRO)] == list(BEFORE_INTRO)]
    if len(origins) != 1:
        raise RuntimeError('R55 exactness-chain introductory prose contract changed')
    chain_index = text.index(BEFORE_CHAIN)
    intro_index = origins[0]
    if chain_index >= intro_index:
        raise RuntimeError('Reviewed chain iteration order differs')
    def eol(line: str) -> str:
        return '\r\n' if line.endswith('\r\n') else ('\n' if line.endswith('\n') else '')
    first_eol = eol(lines[chain_index])
    lines[chain_index] = AFTER_CHAIN + first_eol
    intro_eol = eol(lines[intro_index])
    if not intro_eol:
        raise RuntimeError('R55 source has no terminating EOL for introduction')
    lines[intro_index:intro_index+len(BEFORE_INTRO)] = [
        line + intro_eol for line in AFTER_INTRO
    ]
    result = ''.join(lines)
    ast.parse(result)
    return result


def extract_full_function(source: str) -> str:
    """Return the entire, unabridged modified function using Python's own AST."""
    module = ast.parse(source)
    matches = [node for node in module.body if isinstance(node, ast.FunctionDef)
               and node.name == 'render_model_backed_narrative_markdown']
    if len(matches) != 1:
        raise RuntimeError('Expected one shared model-backed renderer function')
    code_lines = source.splitlines(keepends=True)
    return ''.join(code_lines[matches[0].lineno-1:matches[0].end_lineno])


def write_full_changed_unit(before: str, after: str) -> None:
    """Write full old/new function bodies, not a few-line diff or elided code."""
    path = ROOT / 'phase174_r3_r7_r55_common_exactness_intro' / 'FULL_CHANGED_FUNCTIONS.md'
    path.write_text(
        '# R55 変更関数全文（実行対象のソースから生成）\n\n'
        '## 変更前: `render_model_backed_narrative_markdown()`\n\n```python\n'
        + extract_full_function(before).rstrip() + '\n```\n\n'
        '## 変更後: `render_model_backed_narrative_markdown()`\n\n```python\n'
        + extract_full_function(after).rstrip() + '\n```\n',
        encoding='utf-8',
    )


def install(*, dry_run: bool = False) -> dict[str, object]:
    """Apply only the exact reviewed renderer edit, or validate it in DryRun."""
    guard = verify_checkout()
    path = ROOT / TARGET
    before = path.read_bytes().decode('utf-8-sig')
    after = replace_lines_preserving_eol(before)
    already = after == before
    if not dry_run and not already:
        path.write_bytes(after.encode('utf-8'))
    if not dry_run:
        write_full_changed_unit(before, after)
        post = verify_checkout()
        if not post['r55_renderer_installed']:
            raise RuntimeError('R55 installed renderer did not pass source guard')
    return {
        'local_head': guard['local_head'],
        'remote_head': guard['remote_head'],
        'dry_run': dry_run,
        'installed': (not dry_run),
        'already_installed': already,
        'changed_production_files': 0 if dry_run or already else 1,
        'new_given': 0,
        'new_mathematical_rules': 0,
        'full_pytest': False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    opts=parser.parse_args()
    state=install(dry_run=opts.dry_run)
    for k,v in state.items():
        print('PHASE174_R3R7R55_'+k.upper()+'='+str(v))
    print('PHASE174_R3R7R55_GATE='+('PASS_R55_DRYRUN' if opts.dry_run else 'PASS_R55_COMMON_RENDERER_INSTALLED'))
    print('(END)')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
```

## `audit.py` 全文

```python
"""R55: certify two actual Flask HTML routes with only one common intro."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r54_public_http_narrative_audit.audit import inspect_public_http_proof
from phase174_r3_r7_r55_common_exactness_intro.source_guard import verify_checkout


def inspect_common_intro() -> dict[str, object]:
    """Use the R54 real HTTP observer; do not stub any proof search or HTML."""
    from web_group_proof import build_standard_web_group_proof_view
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_partial_proof import ProofSearchStatus

    check = inspect_public_http_proof()
    if not check['both_http_200'] or not check['both_complete_proof']:
        raise RuntimeError('R55 lost the R54 verified public proof')
    cases=check['cases']
    if len(cases)!=2 or any(x['repeated_intro_count']!=1 for x in cases):
        raise RuntimeError('Common renderer must introduce a result only once: '+repr(cases))
    view=build_standard_web_group_proof_view(7,5,max_depth=2,mode='narrative')
    if view.key!='generic-complete-proof' or view.partial_result:
        raise RuntimeError('R55 narrative Model route must still be complete')
    prose=' '.join(str(line.prefix)+' '+str(line.suffix) for line in view.rendered_lines)
    if prose.count('の群構造を決定するために')!=1 or 'さらに' not in prose:
        # The R54 HTTP HTML check is canonical. This additionally checks
        # the common WebGroupProofView, not a second narrative implementation.
        raise RuntimeError('R55 common Web view did not preserve a natural continuation')
    proof=search_group_from_registered_goal(n=7,k=5)
    if proof.status is not ProofSearchStatus.COMPLETE or len(proof.open_goals)!=0 or len(proof.proven_steps)!=28:
        raise RuntimeError('R55 changed the public proof search or verified steps')
    return {
        'root':'pi_12^7 = 0',
        'both_http_200':True,
        'both_complete_proof':True,
        'public_verified_steps':len(proof.proven_steps),
        'public_open_goals':len(proof.open_goals),
        'http_cases':cases,
        'repeated_intro_counts':[x['repeated_intro_count'] for x in cases],
        'common_intro_once':True,
        'later_chain_continuation':True,
        'renderer_is_shared':True,
        'proof_tree_mutated':False,
        'new_given':0,
        'new_mathematical_rules':0,
        'browser_katex_checked':False,
        'full_pytest':False,
    }


def report_path(dry_run:bool)->Path:
    base=Path(os.environ.get('LOCALAPPDATA',tempfile.gettempdir()))
    return base/'EHPProofTracerAudit'/'phase174_r3_r7_r55'/('preflight.json' if dry_run else 'common_exactness_intro.json')


def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dry-run',action='store_true')
    opts=p.parse_args()
    state=verify_checkout()
    if not opts.dry_run and not state['r55_renderer_installed']:
        raise RuntimeError('R55 common renderer patch not yet installed')
    results=None if opts.dry_run else inspect_common_intro()
    gate=('PASS_R55_SOURCE_PREFLIGHT' if opts.dry_run else 'PASS_R55_COMMON_EXACTNESS_INTRO_HTTP_VERIFIED')
    result={'phase':'174-R3-R7-R55','state':state,'observations':results,'gate':gate}
    dest=report_path(opts.dry_run)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    prefix='PHASE174_R3R7R55_'
    for k,v in state.items():
        print(prefix+k.upper()+'='+str(v))
    if results is not None:
        for k,v in results.items():
            print(prefix+k.upper()+'='+str(v))
    print(prefix+'REPORT='+str(dest))
    print(prefix+'GATE='+gate)
    print('(END)')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
```

## `tests/test_patch.py` 全文

```python
"""Static checks before the user's real renderer/Flask regression tests."""
from __future__ import annotations

import ast

import pytest

from phase174_r3_r7_r55_common_exactness_intro.patch import (
    BEFORE_CHAIN, BEFORE_INTRO, AFTER_CHAIN, AFTER_INTRO,
    replace_lines_preserving_eol, extract_full_function,
)


def minimal_source(eol:str='\n')->str:
    original='\n'.join((
        'def render_model_backed_narrative_markdown(result, model):',
        BEFORE_CHAIN,
        '        exactness_numbers = (3,)',
        *BEFORE_INTRO,
        '        lines.append("")',
        '    return lines',
        '',
    ))
    return original.replace('\n',eol)


def test_one_intro_with_multiple_chains_without_changing_proof_obligations()->None:
    patched=replace_lines_preserving_eol(minimal_source())
    assert AFTER_CHAIN in patched
    assert 'if chain_index == 0 else "さらに, "' in patched
    assert patched.count('の群構造を決定するために')==1
    assert 'exactness_numbers' in patched
    assert 'for number in exactness_numbers' in patched
    assert 'lines.append("")' in patched
    ast.parse(patched)


def test_idempotence_and_full_function_is_extractable()->None:
    patched=replace_lines_preserving_eol(minimal_source())
    assert replace_lines_preserving_eol(patched)==patched
    assert 'def render_model_backed_narrative_markdown' in extract_full_function(patched)
    assert 'return lines' in extract_full_function(patched)


def test_original_eol_preserved_and_unrelated_code_unchanged()->None:
    baseline=minimal_source('\r\n')
    patched=replace_lines_preserving_eol(baseline)
    assert '\n' not in patched.replace('\r\n','')
    assert patched.endswith('    return lines\r\n')


def test_reject_drift_and_partial_installation()->None:
    with pytest.raises(RuntimeError):
        replace_lines_preserving_eol(minimal_source().replace(BEFORE_CHAIN,'    for other in chains:'))
    with pytest.raises(RuntimeError):
        replace_lines_preserving_eol(minimal_source().replace(BEFORE_INTRO[2],'            lines.append("unexpected")'))
    with pytest.raises(RuntimeError):
        replace_lines_preserving_eol(minimal_source().replace(BEFORE_CHAIN,AFTER_CHAIN))
```

## `tests/test_http.py` 全文

```python
"""Real Group query POST; strict zero-root, citation and duplicate regression."""
from __future__ import annotations

from phase174_r3_r7_r55_common_exactness_intro.audit import inspect_common_intro


def test_r55_both_public_http_routes_keep_one_intro_and_cited_root()->None:
    report=inspect_common_intro()
    assert report['both_http_200'] is True
    assert report['both_complete_proof'] is True
    assert report['public_verified_steps']==28
    assert report['public_open_goals']==0
    assert report['repeated_intro_counts']==[1,1]
    assert report['common_intro_once'] is True
    assert report['later_chain_continuation'] is True
    assert report['proof_tree_mutated'] is False
    assert report['new_given']==0
    assert report['new_mathematical_rules']==0
    assert report['browser_katex_checked'] is False
```

## `tests/test_static.py` 全文

```python
"""Check the reviewed rendering change, not another mathematical rule."""
from __future__ import annotations

import ast
from pathlib import Path

from phase174_r3_r7_r55_common_exactness_intro.source_guard import ROOT, TARGET
from phase174_r3_r7_r55_common_exactness_intro.patch import AFTER_CHAIN, AFTER_INTRO


def test_shared_renderer_has_single_first_chain_intro_contract()->None:
    source=(ROOT/TARGET).read_text(encoding='utf-8-sig')
    ast.parse(source)
    assert source.count(AFTER_CHAIN)==1
    assert source.count('if chain_index == 0 else "さらに, "')==1
    assert source.count('lines.append(f"{prefix}{tags}を用いて次の完全列を考える.")')==1
    assert 'def render_model_backed_narrative_markdown(' in source


def test_r55_has_no_new_specific_group_match_or_premise_installer()->None:
    folder=Path(__file__).resolve().parents[1]
    source=(folder/'patch.py').read_text(encoding='utf-8')
    assert 'TodaPrimaryGroupZeroStatement(' not in source
    assert 'ProofStep(' not in source
    assert 'ProofRule.GIVEN' not in source
    assert 'n == 7' not in source and 'k == 5' not in source
```

## `run.ps1` 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r55_common_exactness_intro.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R55 source review failed' }
    python -B -m phase174_r3_r7_r55_common_exactness_intro.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R55 guarded patch DryRun failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R55_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r55_common_exactness_intro.patch
    if ($LASTEXITCODE -ne 0) { throw 'R55 guarded renderer install failed' }
    python -B -m phase174_r3_r7_r55_common_exactness_intro.audit
    if ($LASTEXITCODE -ne 0) { throw 'R55 in-process HTTP audit failed' }
    $Groups = @(
        @{Name='R55_PATCH'; Path='phase174_r3_r7_r55_common_exactness_intro/tests/test_patch.py'},
        @{Name='R55_STATIC'; Path='phase174_r3_r7_r55_common_exactness_intro/tests/test_static.py'},
        @{Name='R55_HTTP'; Path='phase174_r3_r7_r55_common_exactness_intro/tests/test_http.py'},
        @{Name='R54_HTTP_REGRESSION'; Path='phase174_r3_r7_r54_public_http_narrative_audit/tests/test_http.py'},
        @{Name='R54_HTML_PARSER_REGRESSION'; Path='phase174_r3_r7_r54_public_http_narrative_audit/tests/test_html_parser.py'},
        @{Name='R53_PROOF_REGRESSION'; Path='phase174_r3_r7_r53_public_source_bound_kernel/tests/test_public.py'},
        @{Name='R52_PROBE_REGRESSION'; Path='phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_probe.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R55_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R55 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R55_RUN=PASS'
    Write-Output 'PHASE174_R3R7R55_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```

# Phase 175 R13R8R4 — 実装コード

変更対象：`phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown`。この関数は長大な既存共通関数なので、ZIP 付属の `installer.py` が Git blob SHA を検証した上で関数全体を再構成し、変更後の完全な関数を `output/render_model_backed_narrative_markdown_FULL.py` に出力します。`...` によるコード省略は行いません。関数外の import とクラスは変更しません。

新規 `installer.py`、`tests/test_citation_prefix.py`、`run.ps1` は ZIP に全文収録されています。インストーラの変更は完全な置換テキストであり、テキスト部分の欠落がないか AST 検証します。

変更するのは既存関数内の2か所に限定されます。最初は `direct_given_premise_citation_numbers` の内側で typed wrapper の厳密な同一性検査を追加します。2番目は BodyLine の引用ラベル生成時に直接 GIVEN と同じ引用番号であることを検査します。

完了条件：Reference R3・R7 の式と、本文 `[R3]より`・`[R7]より` が同じ実証 Proof Tree に基づいて表示され、`generic-complete-proof` が維持されること。実環境 pytest は実行ログで確定します。

## installer.py 全文

```python
"""Guarded, EOL-preserving common narrative citation-prefix correction."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess

PACKAGE = 'phase175_r4r12r13r8r4_body_citation'
TARGET = 'phase168_r3_5_model_renderer.py'
EXPECTED_BLOB = 'cb6989871ea4ad3964f714bfc5ada2a5099424a0'
FUNCTION = 'render_model_backed_narrative_markdown'

OLD_EMBEDDED = '''        if not (is_direct_relation or is_typed_zero):
            return ()
'''
NEW_EMBEDDED = '''        # A verified GIVEN may wrap precisely the typed statement read by
        # the next inference.  Cite only the actual direct premise, never a
        # source discovered from locator text or matching display strings.
        embedded = getattr(source, "statement", None)
        is_cited_typed_statement = (
            embedded is not None
            and type(embedded) is type(target)
            and embedded == target
        )
        if not (is_direct_relation or is_typed_zero or is_cited_typed_statement):
            return ()
'''
OLD_PREFIX = '''                if tags:
                    prefix = f"{tags}を用いて, "
                else:
                    sources = direct_given_premise_citation_numbers(step)
'''
NEW_PREFIX = '''                if tags:
                    # Treat a cited inference as a direct reading only when
                    # its actual GIVEN premise owns the very same citation.
                    matching_direct_given = (
                        step.rule is ProofRule.INFERENCE
                        and len(step.premises) == 1
                        and step.premises[0].rule is ProofRule.GIVEN
                        and any(
                            (candidate is step.premises[0] or candidate == step.premises[0])
                            and tuple(model.step_citation_numbers[source_index])
                                == tuple(body_line.citation_numbers)
                            for source_index, candidate in enumerate(model.steps)
                        )
                    )
                    if matching_direct_given:
                        prefix = f"{tags}より, "
                    else:
                        prefix = f"{tags}を用いて, "
                else:
                    sources = direct_given_premise_citation_numbers(step)
'''

def git(root: Path, *args: str) -> str:
    result = subprocess.run(['git', *args], cwd=root, capture_output=True, text=True,
                            encoding='utf-8', errors='replace', check=False)
    if result.returncode != 0:
        raise RuntimeError('GIT_FAILED: ' + result.stderr)
    return result.stdout.strip()


def function_source(full: str) -> str:
    tree = ast.parse(full)
    matched = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == FUNCTION]
    if len(matched) != 1:
        raise RuntimeError('RENDERER_FUNCTION_NOT_UNIQUE')
    node = matched[0]
    return ''.join(full.splitlines(keepends=True)[node.lineno-1:node.end_lineno])


def updated_bytes(original: bytes) -> tuple[bytes, str]:
    full = original.replace(b'\r\n', b'\n').decode('utf-8')
    body = function_source(full)
    if body.count(OLD_EMBEDDED) != 1 or body.count(OLD_PREFIX) != 1:
        raise RuntimeError('RENDERER_ANCHOR_NOT_UNIQUE')
    updated_body = body.replace(OLD_EMBEDDED, NEW_EMBEDDED).replace(OLD_PREFIX, NEW_PREFIX)
    updated = full.replace(body, updated_body, 1)
    ast.parse(updated)
    if original.count(b'\r\n') and original.count(b'\n') == original.count(b'\r\n'):
        updated = updated.replace('\n', '\r\n')
    return updated.encode('utf-8'), updated_body


def run(root: Path, dry_run: bool) -> None:
    if git(root, 'branch', '--show-current') != 'develop':
        raise RuntimeError('BRANCH_MISMATCH')
    if git(root, 'hash-object', TARGET) != EXPECTED_BLOB:
        raise RuntimeError('RENDERER_BLOB_MISMATCH_NO_WRITE')
    if git(root, 'diff', '--name-only', '--', TARGET):
        raise RuntimeError('RENDERER_TRACKED_DIRTY_NO_WRITE')
    source = (root / TARGET).read_bytes()
    updated, full_function = updated_bytes(source)
    if dry_run:
        print('PHASE175_R13R8R4_PATCH_STATUS=DRYRUN_VERIFIED')
        return
    (root / TARGET).write_bytes(updated)
    output = root / PACKAGE / 'output'
    output.mkdir(parents=True, exist_ok=True)
    (output / 'render_model_backed_narrative_markdown_FULL.py').write_text(full_function, encoding='utf-8')
    print('PHASE175_R13R8R4_PATCH_STATUS=INSTALLED')
    print('PHASE175_R13R8R4_FULL_FUNCTION=' + str(output / 'render_model_backed_narrative_markdown_FULL.py'))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    run(args.root.resolve(), args.dry_run)


if __name__ == '__main__':
    main()

```

## tests/test_citation_prefix.py 全文

```python
"""Focused common citation guard and actual completed pi95 web regression."""
from __future__ import annotations

import ast
from pathlib import Path

from phase175_r4r12r13r8r4_body_citation.installer import (
    OLD_EMBEDDED, OLD_PREFIX, NEW_EMBEDDED, NEW_PREFIX, updated_bytes,
)


def test_patch_changes_only_two_guarded_prefix_regions() -> None:
    source = Path('phase168_r3_5_model_renderer.py').read_bytes()
    normalized = source.replace(b'\r\n', b'\n').decode('utf-8')
    if OLD_EMBEDDED in normalized and OLD_PREFIX in normalized:
        updated, full_function = updated_bytes(source)
        after = updated.replace(b'\r\n', b'\n').decode('utf-8')
        assert NEW_EMBEDDED in full_function
        assert NEW_PREFIX in full_function
        assert after.replace(NEW_EMBEDDED, OLD_EMBEDDED).replace(NEW_PREFIX, OLD_PREFIX) == normalized
        ast.parse(after)
    else:
        assert NEW_EMBEDDED in normalized and NEW_PREFIX in normalized


def test_real_model_has_exact_direct_citation_ownership() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase165_r52_partial_proof import ProofSearchStatus
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(n=5, k=4, bridge=bridge, context_sink=contexts.append)
    assert result.status is ProofSearchStatus.COMPLETE
    model = build_linked_proof_narrative_model(result, contexts[-1])
    for locator in ('(5.11)', '(5.8)'):
        refs = [c for c in model.citations if (c.reference.locator or c.reference.label) == locator]
        assert len(refs) == 1
        citation = refs[0]
        assert citation.statement_bodies
        given = [model.steps[i] for i in citation.step_indices if model.steps[i].rule is ProofRule.GIVEN]
        assert len(given) == 1
        downstream = [i for i, step in enumerate(model.steps)
                      if step.rule is ProofRule.INFERENCE and len(step.premises) == 1
                      and step.premises[0] == given[0]]
        assert downstream


def test_real_web_contains_cited_equations_and_no_unsupported_extra_math() -> None:
    from web_group_proof import build_standard_web_group_proof_view
    view = build_standard_web_group_proof_view(5, 4, mode='narrative')
    assert view.key == 'generic-complete-proof'
    lines = getattr(view, 'rendered_lines', ())
    text = '\n'.join(
        getattr(line, 'prefix', '') + ' ' + str(getattr(line, 'statement_latex', '') or '')
        for line in lines
    )
    assert '[R3]より' in text
    assert '[R7]より' in text

```

## run.ps1 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$package = Join-Path $repo 'phase175_r4r12r13r8r4_body_citation'
$installer = Join-Path $package 'installer.py'
if (-not (Test-Path $installer)) { throw 'Run from repository root' }
if ($DryRun) {
    & python -B $installer --root $repo --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R13R8R4 DryRun failed' }
    Write-Output 'PHASE175_R13R8R4_GATE=DRYRUN_PASS'
    exit 0
}
& python -B $installer --root $repo
if ($LASTEXITCODE -ne 0) { throw 'R13R8R4 installer failed' }
& python -B -m pytest -q -p no:cacheprovider (Join-Path (Join-Path $package 'tests') 'test_citation_prefix.py') (Join-Path (Join-Path 'phase175_r4r12r13r8r3_verified_reference_body' 'tests') 'test_verified_reference.py')
if ($LASTEXITCODE -ne 0) { throw 'R13R8R4 focused pytest failed' }
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'R13R8R4 git diff check failed' }
Write-Output 'PHASE175_R13R8R4_GATE=BODY_CITATION_FOCUSED_TESTED'

```

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

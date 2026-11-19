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

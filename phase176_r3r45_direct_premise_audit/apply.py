"""Byte-preserving, pinned common formatter repair."""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'web_group_proof_common.py'
BASE = 'cb52a4dc2b4c24594f2acf2d76dc6c68ec0947ab'
ANCHOR = '  # A display projection of the typed map property, never a proof claim.\n'
INSERT = '''  from map_property_rules import ImageZeroStatement

  if isinstance(statement, ImageZeroStatement):
    mapping = statement.map
    if isinstance(mapping, (TodaDeltaMap, TodaSuspensionMap, TodaHopfInvariantMap)):
      source = group_tex(mapping.source_group)
      target = group_tex(mapping.target_group)
      symbol = map_symbol_tex(mapping)
      if source is not None and target is not None and symbol is not None:
        return (rf'{symbol}: {source} \\xrightarrow{{0}} {target}', None)

'''

def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def formatter(source):
    functions = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)
                 and node.name == '_group_proof_statement_latex']
    if len(functions) != 1:
        raise ValueError('FORMATTER_NOT_UNIQUE')
    node = functions[0]
    return ''.join(source.splitlines(keepends=True)[node.lineno-1:node.end_lineno])


def updated_source(raw):
    normalized = raw.replace(b'\r\n', b'\n')
    if b'\r' in normalized or (b'\r\n' in raw and raw != normalized.replace(b'\n', b'\r\n')):
        raise ValueError('MIXED_LINE_ENDINGS')
    source = normalized.decode('utf-8')
    baseline = source.replace(INSERT, '', 1)
    canonical = baseline.encode('utf-8')
    if BASE not in (blob(canonical), blob(canonical.replace(b'\n', b'\r\n'))):
        raise ValueError('UNREVIEWED_FORMATTER_BASELINE')
    if baseline.count(ANCHOR) != 1 or formatter(baseline).count(ANCHOR) != 1:
        raise ValueError('FORMATTER_ANCHOR_NOT_UNIQUE')
    changed = baseline.replace(ANCHOR, INSERT+ANCHOR, 1)
    if source not in (baseline, changed):
        raise ValueError('PARTIAL_OR_MOVED_PATCH')
    ast.parse(changed)
    result = changed.encode('utf-8')
    return result.replace(b'\n', b'\r\n') if b'\r\n' in raw else result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    branch = subprocess.check_output(['git','branch','--show-current'], cwd=ROOT, text=True).strip()
    if branch != 'develop':
        raise RuntimeError('DEVELOP_BRANCH_REQUIRED')
    original = TARGET.read_bytes()
    changed = updated_source(original)
    if not args.dry_run:
        if changed != original:
            TARGET.write_bytes(changed)
        full = formatter(changed.decode('utf-8').replace('\r\n','\n'))
        (Path(__file__).parent/'SHARED_FUNCTION_FULL_JA.md').write_text(
            '# 変更後の共通表示関数全文\n\n```python\n'+full+'\n```\n', encoding='utf-8')
    print('PHASE176_R3R45_PATCH='+('DRYRUN_PASS' if args.dry_run else 'APPLIED_OR_ALREADY_PRESENT'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

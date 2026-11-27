"""Install the two reviewed R17R3 files; preserve all proof and source code."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
BASE = '720a7e8658a3f7e94f92a20ab530f763f1b421e1'
PREFIX = 'PHASE178_R17R4_'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def git_text(*args):
    return git(*args).decode('utf-8').strip()


def normalized(raw):
    return raw.decode('utf-8-sig').replace('\r\n', '\n')


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def encode_like(text, raw):
    rest = raw.replace(b'\r\n', b'')
    require(b'\r' not in rest and not (b'\r\n' in raw and b'\n' in rest), 'MIXED_EOL')
    eol = '\r\n' if b'\r\n' in raw else '\n'
    encoding = 'utf-8-sig' if raw.startswith(b'\xef\xbb\xbf') else 'utf-8'
    return text.replace('\n', eol).encode(encoding)


def preflight():
    require(Path(git_text('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(git_text('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    head = git_text('rev-parse', 'HEAD')
    require(head == git_text('rev-parse', 'origin/develop'), 'LOCAL_REMOTE_HEAD_MISMATCH')
    git('merge-base', '--is-ancestor', BASE, head)
    require(not git_text('diff', '--cached', '--name-only'), 'STAGED_CHANGES_PRESENT')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    manifest = json.loads((PACKAGE / 'manifest.json').read_text(encoding='utf-8'))
    changes = {}
    # Review every file in the previously distributed R17R3 package before
    # importing its installer. Accept only the known old or new contents.
    for path, entry in manifest.items():
        raw = (ROOT / path).read_bytes()
        current = digest(normalized(raw))
        require(current in (entry['before'], entry.get('after')), 'UNREVIEWED_R17R3_FILE:' + path)
        if 'replacement' not in entry:
            continue
        text = (PACKAGE / 'replacements' / entry['replacement']).read_text(encoding='utf-8')
        require(digest(text) == entry['after'], 'REPLACEMENT_HASH_MISMATCH:' + path)
        ast.parse(text)
        changes[path] = (raw, encode_like(text, raw), text)

    from phase178_r17r3_common_renderer import installer as previous
    require(previous.HEAD == BASE, 'R17R3_BASE_MISMATCH')
    allowed = set(manifest) | set(previous.PATCHES)
    committed = set(git_text('diff', '--name-only', BASE, head).splitlines())
    worktree = set(git_text('diff', '--name-only', 'HEAD').splitlines())
    require(not (committed | worktree) - allowed, 'UNRELATED_TRACKED_CHANGES')
    # The R17R3 hooks must already be installed. Check their exact content
    # against the pinned original blobs, including when R17R3 was committed.
    for path, pin in previous.PINS.items():
        require(git_text('rev-parse', BASE + ':' + path) == pin, 'BASE_BLOB_CHANGED:' + path)
        original = git('show', BASE + ':' + path)
        require(previous.matches_blob(original, pin), 'BASE_CONTENT_CHANGED:' + path)
        raw = (ROOT / path).read_bytes()
        if path in previous.PATCHES:
            expected = previous.proposed(normalized(original), *previous.PATCHES[path])
            require(normalized(raw) == expected, 'R17R3_HOOK_NOT_INSTALLED_OR_CHANGED:' + path)
        else:
            require(previous.matches_blob(raw, pin), 'DEPENDENCY_CHANGED:' + path)
    return head, changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    head, changes = preflight()
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE.name
    folder.mkdir(parents=True, exist_ok=True)
    for path, (raw, updated, text) in changes.items():
        name = path.replace('/', '__')
        (folder / (name + '.full.txt')).write_text(text, encoding='utf-8')
        if not args.dry_run and raw != updated:
            (folder / (name + '.before')).write_bytes(raw)
    if not args.dry_run:
        for path, (raw, updated, text) in changes.items():
            require((ROOT / path).read_bytes() == raw, 'WORKTREE_CHANGED:' + path)
        for path, (raw, updated, text) in changes.items():
            if raw != updated:
                (ROOT / path).write_bytes(updated)
            require((ROOT / path).read_bytes() == updated, 'INSTALL_BYTE_MISMATCH:' + path)
    print(PREFIX + 'HEAD=' + head)
    print(PREFIX + 'FULL_CODE=' + str(folder))
    print(PREFIX + 'INSTALL=' + ('PASS_DRYRUN' if args.dry_run else 'PASS'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

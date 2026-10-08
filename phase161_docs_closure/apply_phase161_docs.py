"""Phase 161 documentation closure. No tests or implementation code are modified."""
from pathlib import Path
import argparse
import shutil

DOCS = {
    'README.md': Path('README.md'),
    'design.md': Path('docs/design.md'),
    'development_log.md': Path('docs/development_log.md'),
    'roadmap.md': Path('docs/roadmap.md'),
    'proof_records.md': Path('docs/proof_records.md'),
}
MARKERS = {
    'README.md': '## Phase 161 — Concrete Backward-Driven Proof Reconstruction',
    'design.md': '## Phase 161 — Concrete Backward Goal Schema と provenance 境界',
    'development_log.md': '## Phase 161 — Concrete Backward Chaining と証明再構築',
    'roadmap.md': '## Phase 161 — Concrete Backward-Driven Reconstruction（完了：focused 検証のみ）',
    'proof_records.md': '## Phase 161 — $E:',
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', type=Path, default=Path.cwd())
    args = parser.parse_args()
    repository = args.repository.resolve()
    package = Path(__file__).resolve().parent
    sources = {}
    for name, relative in DOCS.items():
        original = repository / relative
        section = package / 'sections' / name
        if not original.is_file():
            raise SystemExit(f'MISSING original document: {original}')
        if not section.is_file():
            raise SystemExit(f'MISSING package section: {section}')
        data = original.read_bytes()
        if len(data) < 1000:
            raise SystemExit(f'Unexpected short original document: {original}')
        sources[name] = data
    backup = package / 'backup_before_phase161'
    output = package / 'output_full_documents'
    print(f'Repository root: {repository}')
    for name, relative in DOCS.items():
        original = repository / relative
        section = (package / 'sections' / name).read_text(encoding='utf-8')
        old_data = sources[name]
        try:
            old_text = old_data.decode('utf-8-sig')
        except UnicodeError as error:
            raise SystemExit(f'Cannot decode {original}: {error}')
        marker = MARKERS[name]
        if marker in old_text:
            print(f'SKIP already applied: {relative}')
            target_text = old_text
        else:
            old_text = old_text.rstrip('\r\n')
            target_text = old_text + '\n\n' + section.strip() + '\n'
        # Full before/after files are preserved, rather than replacing prior history with a section-only file.
        before = backup / relative
        after = output / relative
        before.parent.mkdir(parents=True, exist_ok=True)
        after.parent.mkdir(parents=True, exist_ok=True)
        if not before.exists():
            before.write_bytes(old_data)
        after.write_text(target_text, encoding='utf-8', newline='\n')
        if marker not in target_text:
            raise SystemExit(f'Marker not found in output: {relative}')
        if target_text != old_text and not target_text.startswith(old_text):
            raise SystemExit(f'Existing content not preserved: {relative}')
        original.write_bytes(after.read_bytes())
        print(f'UPDATED full document: {relative} ({after.stat().st_size} bytes)')
    print('Phase 161 documentation closure completed. NO pytest was run.')
    print(f'Full documents: {output}')
    print(f'Original backups: {backup}')

if __name__ == '__main__':
    main()

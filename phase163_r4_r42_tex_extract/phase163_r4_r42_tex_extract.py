"""R4-R42: source-preserving TeX extraction and read-only existing-ID matching.

No Registry mutation.  Only labelled environments receive a locator candidate.
Unlabelled environments are retained, but must be reviewed before registration.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

CHAPTER_FILES = {
    1: 'Toda_01_corrected.tex',
    2: 'Toda_02_2(2).tex',
    3: 'Toda_03_2(2).tex',
    4: 'Toda_04_2(2).tex',
    5: 'Toda_05_2(6).tex',
}
KINDS = ('theorem', 'proposition', 'lemma', 'corollary', 'definition', 'remark', 'equation')
BEGIN_RE = re.compile(r'\\begin\{(' + '|'.join(KINDS) + r')\}')
LABEL_RE = re.compile(r'\\label\{([^}]+)\}')
TAG_RE = re.compile(r'\\tag\{([^}]+)\}')
NUMBER_RE = re.compile(r'(?<!\d)([1-5])[.-](\d+)(?!\d)')


def uncomment(line: str) -> str:
    """Strip an unescaped TeX comment while retaining escaped percent signs."""
    for index, char in enumerate(line):
        if char == '%':
            count = 0
            j = index - 1
            while j >= 0 and line[j] == "\\":
                count += 1
                j -= 1
            if count % 2 == 0:
                return line[:index]
    return line.rstrip("\n")


def clean_source(source: str) -> str:
    return ''.join(uncomment(line) + ('\n' if line.endswith('\n') else '')
                   for line in source.splitlines(keepends=True))


def locate(kind: str, labels: list[str], tags: list[str], chapter: int) -> str | None:
    for label in labels:
        # Restrict to chapter-qualified keys. No speculative numbering.
        found = NUMBER_RE.search(label)
        if found and int(found.group(1)) == chapter:
            number = f'{found.group(1)}.{found.group(2)}'
            return f'({number})' if kind == 'equation' else f'{kind.capitalize()} {number}'
    if kind == 'equation':
        for tag in tags:
            if re.fullmatch(rf'{chapter}\.\d+', tag.strip()):
                return f'({tag.strip()})'
    return None


def extract_chapter(path: Path, chapter: int) -> dict:
    raw = path.read_bytes()
    source = raw.decode('utf-8-sig')
    clean = clean_source(source)
    items = []
    for order, match in enumerate(BEGIN_RE.finditer(clean), start=1):
        kind = match.group(1)
        end_match = re.search(r'\\end\{' + re.escape(kind) + r'\}', clean[match.end():])
        if end_match is None:
            end = len(clean)
            unclosed = True
        else:
            end = match.end() + end_match.end()
            unclosed = False
        # Non-nested theorem environments expected. All content retained verbatim.
        body = clean[match.start():end]
        labels = LABEL_RE.findall(body)
        tags = TAG_RE.findall(body)
        locator = locate(kind, labels, tags, chapter)
        items.append({
            'chapter': chapter, 'order': order, 'kind': kind,
            'line': clean.count('\n', 0, match.start()) + 1,
            'labels': labels, 'tags': tags, 'locator_candidate': locator,
            'tex': body, 'unclosed': unclosed,
        })
    return {'chapter': chapter, 'source_file': path.name,
            'sha256': hashlib.sha256(raw).hexdigest(),
            'items': items}


def existing_reference_ids() -> list[str]:
    """Optional read-only lookup through the existing production bridge."""
    from phase163_r4_registry_bridge import build_registry_bridge
    result = build_registry_bridge()
    return sorted({entry.reference_id for entry in result.registry._references.values()})


def make_report(inputs: Path, *, existing_ids: list[str] | None = None) -> dict:
    chapters = []
    missing = []
    for chapter, filename in CHAPTER_FILES.items():
        path = inputs / filename
        if path.exists():
            chapters.append(extract_chapter(path, chapter))
        else:
            missing.append(filename)
    all_items = [item for group in chapters for item in group['items']]
    seen = {}
    for item in all_items:
        locator = item['locator_candidate']
        if locator is not None:
            seen.setdefault(locator, []).append([item['chapter'], item['line']])
        item['existing_reference_id_candidate'] = (
            'toda:' + locator if locator and existing_ids is not None
            and 'toda:' + locator in existing_ids else None
        )
        item['registration_status'] = 'NOT_REGISTERED'
        item['structured'] = False
        item['source_verified'] = False
    return {
        'phase': '163 R4-R42', 'mode': 'READ_ONLY_EXTRACTION',
        'chapters': chapters, 'missing_sources': missing,
        'item_count': len(all_items),
        'kind_counts': {k: sum(x['kind'] == k for x in all_items) for k in KINDS},
        'unresolved_locator_count': sum(x['locator_candidate'] is None for x in all_items),
        'duplicate_locator_candidates': {k: v for k, v in seen.items() if len(v) > 1},
        'existing_registry_lookup': 'AVAILABLE' if existing_ids is not None else 'UNAVAILABLE',
        'matched_existing_reference_count': sum(bool(x['existing_reference_id_candidate']) for x in all_items),
        'registration_applied': False,
        'proof_search_connected': False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--no-registry', action='store_true')
    args = parser.parse_args()
    ids = None
    if not args.no_registry:
        try:
            ids = existing_reference_ids()
        except (ImportError, ModuleNotFoundError):
            pass
    report = make_report(args.inputs, existing_ids=ids)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'extraction.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: val for key, val in report.items() if key != 'chapters'}, ensure_ascii=False, indent=2))
    if report['missing_sources']:
        raise SystemExit('Missing sources: ' + ', '.join(report['missing_sources']))


if __name__ == '__main__':
    main()

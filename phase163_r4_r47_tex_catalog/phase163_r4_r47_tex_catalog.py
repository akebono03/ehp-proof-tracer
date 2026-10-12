"""Phase 163 R4-R47: standalone, append-safe TeX source catalog.

This does not mutate UnifiedStatementRegistry or turn TeX into proof steps.
Every extracted TeX environment is registered as an independent *source unit*.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

PHASE = '163 R4-R47'


def require(value: bool, reason: str) -> None:
    if not value:
        raise ValueError(reason)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def build_catalog(extraction: dict[str, Any], mapping: dict[str, Any],
                  crosswalk: dict[str, Any], existing_reference_ids: set[str],
                  existing_assertion_ids: set[str]) -> dict[str, Any]:
    """Validate the preceding audits and construct a complete TeX catalog.

    Stable local keys are preserved by compatibility checking on repeated runs.
    Reordering or changing source requires an explicit migration, never silent ID reuse.
    """
    require(extraction.get('phase') == '163 R4-R42', 'wrong extraction phase')
    require(mapping.get('phase') == '163 R4-R43', 'wrong mapping phase')
    require(crosswalk.get('phase') == '163 R4-R44', 'wrong crosswalk phase')
    require(extraction.get('registration_applied') is False, 'input must be read-only')
    require(mapping.get('registration_applied') is False and mapping.get('id_allocated') is False,
            'input must be read-only')
    require(not extraction['missing_sources'], 'missing TeX chapters')
    require(not mapping['duplicate_locator_candidates'], 'duplicated literature locators')
    chapters = extraction['chapters']
    require({x['chapter'] for x in chapters} == {1, 2, 3, 4, 5}, 'need chapters 1-5')
    fingerprints = {str(ch['chapter']): ch['sha256'] for ch in chapters}
    require(fingerprints == mapping['source_sha256'], 'input source fingerprints disagree')
    originals = {(ch['chapter'], x['order']): x for ch in chapters for x in ch['items']}
    require(len(originals) == extraction['item_count'], 'duplicate extraction position')
    rows = mapping['rows']
    require(len(rows) == len(originals) == mapping['item_count'], 'mapping coverage failure')

    # Crosswalk structure comes from R4-R44. It is read-only evidence, not semantic verification.
    units = crosswalk.get('reference_units')
    assertions = crosswalk.get('assertion_crosswalk')
    require(isinstance(units, list) and isinstance(assertions, list),
            'R4-R44 reference_units/assertion_crosswalk required')
    require(len(units) == len(rows), 'crosswalk source coverage failure')
    require({r['assertion_id'] for r in assertions} == existing_assertion_ids,
            'existing Assertion IDs changed since crosswalk')
    require(len(assertions) == len(existing_assertion_ids), 'duplicated assertion in crosswalk')
    cross_positions = {(x['chapter'], x['source_order']): x for x in units}
    require(len(cross_positions) == len(units), 'duplicated crosswalk source position')

    catalog = []
    matched_refs = set()
    seen_positions = set()
    seen_ref_ids = set()
    for row in rows:
        chapter, order = row['chapter'], row['source_order']
        position = (chapter, order)
        require(position not in seen_positions and position in originals,
                f'duplicate or unknown source position {position}')
        seen_positions.add(position)
        original = originals[position]
        cross = cross_positions.get(position)
        require(cross is not None, f'missing crosswalk position {position}')
        tex = original['tex']
        body_sha = digest(tex)
        require(not original['unclosed'], f'unclosed environment {position}')
        require(row['sha256_tex_body'] == body_sha == cross['sha256_tex_body'],
                f'body fingerprint mismatch at {position}')
        require(row['kind'] == original['kind'] == cross['kind'] and
                row['source_line'] == original['line'] == cross['source_line'] and
                row['locator_candidate'] == original['locator_candidate'],
                f'metadata mismatch at {position}')
        require(row['labels'] == original['labels'] and row['tags'] == original['tags'],
                f'label mismatch at {position}')
        status = row['status']
        require(status in {'EXISTING_REFERENCE', 'NEW_REFERENCE_CANDIDATE',
                           'UNNUMBERED_ENVIRONMENT', 'UNRESOLVED_SYMBOLIC_LABEL'},
                f'unknown mapping status {status}')
        reference_id = row['existing_reference_id']
        proposed = row['proposed_reference_id']
        if status == 'EXISTING_REFERENCE':
            require(reference_id in existing_reference_ids and proposed is None,
                    f'invalid existing reference: {position}')
            require(reference_id not in matched_refs, 'existing reference mapped twice')
            matched_refs.add(reference_id)
        elif status == 'NEW_REFERENCE_CANDIDATE':
            require(reference_id is None and isinstance(proposed, str) and
                    proposed not in existing_reference_ids and proposed not in seen_ref_ids,
                    f'proposed reference collision: {position}')
            seen_ref_ids.add(proposed)
        else:
            require(reference_id is None and proposed is None,
                    f'unresolved item given literature identifier: {position}')
        require(cross['mapping_status'] == status and
                cross['existing_reference_id'] == reference_id and
                cross['tex_body'] == tex, f'crosswalk disagreement at {position}')
        # Local source-unit IDs are not Assertion IDs and are never treated as a literature number.
        local_id = f'tex-unit:toda:ch{chapter:02d}:{order:04d}'
        require(local_id not in existing_assertion_ids, 'source unit collides with Assertion ID')
        catalog.append({
            'source_unit_id': local_id,
            'chapter': chapter,
            'publication_position': sum(len(ch['items']) for ch in chapters if ch['chapter'] < chapter) + order,
            'chapter_position': order,
            'kind': row['kind'],
            'source_file': next(ch['source_file'] for ch in chapters if ch['chapter'] == chapter),
            'source_line': row['source_line'],
            'labels': row['labels'], 'tags': row['tags'],
            'locator': row['locator_candidate'],
            'reference_id': reference_id,
            'reference_id_candidate': proposed,
            'mapping_status': status,
            'tex_body': tex,
            'sha256_tex_body': body_sha,
            'TEX_REGISTERED': True,
            'STRUCTURED': False,
            'SOURCE_VERIFIED': False,
            'assertion_link_level': 'REFERENCE_ONLY' if reference_id else 'NONE',
        })
    require(seen_positions == set(originals), 'extraction items omitted')
    require(matched_refs == existing_reference_ids, 'existing Reference IDs omitted')
    catalog.sort(key=lambda x: x['publication_position'])
    require([x['publication_position'] for x in catalog] == list(range(1, len(catalog) + 1)),
            'nonconsecutive publication order')
    require(len({x['source_unit_id'] for x in catalog}) == len(catalog), 'duplicate local IDs')
    counts = Counter(x['mapping_status'] for x in catalog)
    return {
        'phase': PHASE, 'mode': 'STANDALONE_TEX_SOURCE_REGISTRATION',
        'source_sha256': fingerprints,
        'item_count': len(catalog),
        'status_counts': dict(sorted(counts.items())),
        'existing_reference_ids': sorted(existing_reference_ids),
        'existing_assertion_ids': sorted(existing_assertion_ids),
        'tex_registered_count': len(catalog),
        'structured_count': 0, 'source_verified_count': 0,
        'registration_applied': True,
        'production_registry_modified': False,
        'production_ids_allocated': False,
        'proof_search_connected': False,
        'coverage_scope': 'TeX theorem-like and equation environments extracted in R4-R42 only',
        'items': catalog,
    }


def enforce_compatible(previous: dict[str, Any], current: dict[str, Any]) -> None:
    """Reject silent source-unit ID reassignment and changed registry snapshots."""
    require(previous.get('phase') == PHASE, 'incompatible existing catalog format')
    require(previous['source_sha256'] == current['source_sha256'],
            'source files changed: explicit catalog migration required')
    require(previous['existing_reference_ids'] == current['existing_reference_ids'] and
            previous['existing_assertion_ids'] == current['existing_assertion_ids'],
            'Registry changed: explicit reconciliation required')
    require(previous['items'] == current['items'],
            'source unit identity or data changed: explicit migration required')


def write_catalog(catalog: dict[str, Any], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    target = output / 'catalog.json'
    if target.exists():
        enforce_compatible(json.loads(target.read_text(encoding='utf-8')), catalog)
    target.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (output / 'catalog.csv').open('w', encoding='utf-8-sig', newline='') as f:
        cols = ['source_unit_id', 'chapter', 'publication_position', 'chapter_position',
                'kind', 'locator', 'reference_id', 'reference_id_candidate',
                'mapping_status', 'source_file', 'source_line', 'sha256_tex_body',
                'TEX_REGISTERED', 'STRUCTURED', 'SOURCE_VERIFIED']
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in catalog['items']:
            writer.writerow({key: row[key] for key in cols})
    report = [
        '# Phase 163 R4-R47：TeX 本文登録結果', '',
        '第1〜5章の抽出済み TeX 環境を独立カタログへ保存した。',
        '命題本文は `catalog.json` の `tex_body` に保持し、文献掲載順は `publication_position` に保存する。',
        '原稿との外部照合、構造化、証明探索への接続は実施していない。', '',
        f"- 登録環境数：{catalog['item_count']}",
        f"- 既存 Reference：{len(catalog['existing_reference_ids'])}",
        f"- 既存 Assertion：{len(catalog['existing_assertion_ids'])}",
        '- 文献番号未解決の環境にも内部 source_unit_id のみを付与。',
        '- `reference_id_candidate` は提案値であり、既存 Registry に登録・確定していない。',
        '- 既存 Assertion と TeX 環境の対応は Reference 単位に限定。',
        '- TeX 上の環境外の Definition 等は今回の対象外。',
    ]
    (output / 'report.md').write_text('\n'.join(report) + '\n', encoding='utf-8')


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--extraction', type=Path, required=True)
    p.add_argument('--mapping', type=Path, required=True)
    p.add_argument('--crosswalk', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--inputs', type=Path, required=True)
    args = p.parse_args()
    extraction = json.loads(args.extraction.read_text(encoding='utf-8'))
    mapping = json.loads(args.mapping.read_text(encoding='utf-8'))
    crosswalk = json.loads(args.crosswalk.read_text(encoding='utf-8'))
    for chapter in extraction['chapters']:
        source_file = args.inputs / chapter['source_file']
        if not source_file.is_file() or hashlib.sha256(source_file.read_bytes()).hexdigest() != chapter['sha256']:
            raise ValueError(f'missing or modified TeX source: {source_file}')
    from phase163_r4_registry_bridge import build_registry_bridge
    registry = build_registry_bridge().registry
    catalog = build_catalog(extraction, mapping, crosswalk,
                            set(registry._references), set(registry._assertions))
    write_catalog(catalog, args.output)
    print(json.dumps({key: value for key, value in catalog.items()
                      if key not in {'items', 'existing_reference_ids', 'existing_assertion_ids'}},
                     indent=2, ensure_ascii=False))
    print('TeX source catalog written; production Registry and full pytest untouched.')


if __name__ == '__main__':
    main()

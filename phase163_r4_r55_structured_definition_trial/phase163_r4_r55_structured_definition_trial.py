"""R4-R55: isolated source-grounded definition trial; never mutates production registry."""
import argparse
import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from unified_statement_registry import (AssertionEntry, AssertionKind, AssertionOrigin,
                                        LiteratureEntry, ReferenceKind, UnifiedStatementRegistry)


SAMPLES = {
    '(2.9)': ('delta_homomorphism', r'\Delta', 152),
    '(2.10)': ('inverse_delta', r'\Delta^{-1}', 153),
    '(4.3)': ('pi_i_n_subgroup', r'\pi_i^n', 260),
}


@dataclass(frozen=True)
class SourceGroundedDefinition:
    """Typed record of a TeX definition; NOT a parsed mathematical AST."""
    defined_symbol: str
    tex_body: str
    source_unit_id: str
    scope_text: str
    source_verification: str = 'TEX_ONLY_ORIGINAL_UNVERIFIED'


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_trial(catalog, overlap, *, catalog_digest=None, overlap_digest=None):
    if catalog.get('phase') != '163 R4-R47' or overlap.get('phase') != '163 R4-R53':
        raise ValueError('unexpected input phase')
    if len(overlap.get('candidates', [])) != 19 or catalog.get('item_count') != 108:
        raise ValueError('input counts changed')
    if any(overlap.get(k) for k in ('registration_applied', 'registry_modified', 'ids_allocated')):
        raise ValueError('unexpected mutation in input')
    by_locator = {x['locator']: x for x in catalog['items'] if x.get('locator')}
    candidate_by_key = {x['editorial_key']: x for x in overlap['candidates']}
    registry = UnifiedStatementRegistry()
    rows = []
    for locator, (editorial_key, symbol, expected_index) in SAMPLES.items():
        item = by_locator[locator]
        candidate = candidate_by_key[editorial_key]
        if (candidate['r48_index'] != expected_index or
                candidate['matched_source_unit_id'] != item['source_unit_id'] or
                candidate['matched_locator'] != locator or
                candidate['tex_catalog_containment_status'] != 'CATALOG_UNIT_WITHOUT_EXISTING_REFERENCE'):
            raise ValueError('candidate/source unit mismatch: ' + locator)
        if (item['reference_id'] is not None or item['mapping_status'] != 'NEW_REFERENCE_CANDIDATE'
                or not item['TEX_REGISTERED'] or item['STRUCTURED'] or item['SOURCE_VERIFIED']):
            raise ValueError('not a pending TeX source unit: ' + locator)
        body = item['tex_body']
        if hashlib.sha256(body.encode('utf-8')).hexdigest() != item['sha256_tex_body']:
            raise ValueError('TeX body checksum mismatch: ' + locator)
        if symbol not in body or ':=' not in body or f'\\label{{{locator[1:-1]}}}' not in body:
            raise ValueError('formula shape mismatch: ' + locator)
        if item['chapter'] != candidate['chapter']:
            raise ValueError('chapter mismatch')
        # Trial-only IDs are independent of all existing production identifiers.
        ref_id = 'trial:r55:' + item['source_unit_id']
        assertion_id = ref_id + ':definition'
        registry.add_reference(LiteratureEntry(ref_id, ReferenceKind.EQUATION, locator,
                                               source_id='Toda:TeX:unverified',
                                               publication_position=item['publication_position']))
        # The surrounding prose is preserved as context, not promoted to a parsed condition.
        content = SourceGroundedDefinition(symbol, body, item['source_unit_id'],
                                           candidate['context'])
        registry.add_assertion(AssertionEntry(assertion_id, ref_id,
                             AssertionKind.DEFINITION, content,
                             origin=AssertionOrigin.FIXED_STATEMENT,
                             component_position=1, defined_symbol=symbol))
        actual = registry.assertion(assertion_id)
        if actual.content != content or actual.kind is not AssertionKind.DEFINITION:
            raise AssertionError('trial assertion integrity')
        rows.append({'locator': locator, 'r48_index': expected_index,
                     'source_unit_id': item['source_unit_id'],
                     'publication_position': item['publication_position'],
                     'trial_reference_id': ref_id, 'trial_assertion_id': assertion_id,
                     'defined_symbol': symbol, 'content_type': type(content).__name__,
                     'tex_sha256': item['sha256_tex_body'], 'scope_status': 'RAW_CONTEXT_UNPARSED',
                     'mathematical_ast_parsed': False, 'original_edition_verified': False,
                     'production_registration_applied': False})
    existing = set(catalog['existing_reference_ids']) | set(catalog['existing_assertion_ids'])
    if any(row['trial_reference_id'] in existing or row['trial_assertion_id'] in existing for row in rows):
        raise ValueError('ID collision')
    report = {'phase': '163 R4-R55', 'mode': 'ISOLATED_SOURCE_GROUNDED_DEFINITION_TRIAL',
              'catalog_input_sha256': catalog_digest, 'r53_input_sha256': overlap_digest,
              'trial_reference_count': len(rows), 'trial_definition_count': len(rows),
              'candidate_total': len(overlap['candidates']),
              'untouched_candidate_count': len(overlap['candidates']) - len(rows),
              'pending_other_candidates_count': overlap['pending_other_candidates_count'],
              'contents_are_source_grounded_tex': True, 'formal_mathematical_ast_count': 0,
              'mathematical_equivalence_verified_count': 0, 'new_statement_confirmed_count': 0,
              'ids_are_trial_only': True, 'production_registry_modified': False,
              'production_ids_allocated': False, 'proof_search_connected': False,
              'original_edition_verified': False, 'trial_items': rows}
    return report, registry


def write_report(report, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'trial.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (output / 'trial.csv').open('w', newline='', encoding='utf-8-sig') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(report['trial_items'][0]))
        writer.writeheader()
        writer.writerows(report['trial_items'])
    lines = ['# Phase 163 R4-R55 仮 Registry での定義内容登録検証', '',
             '- 検証対象：' + ', '.join(row['locator'] for row in report['trial_items']),
             f"- 仮 Reference：{report['trial_reference_count']}件、仮 Definition：{report['trial_definition_count']}件",
             '- 出典：TeX 原稿、原本未照合',
             '- 内容：型付きの出典根拠付き TeX 記録。数学的 AST と同値性は未検証',
             '- 適用範囲：周辺文脈として保持。構造化した範囲条件ではない',
             '- 仮 ID は本番 ID ではない。本番 Registry と証明探索を変更しない',
             '- 未処理定義候補16件とその他保留237件はそのまま維持',
             '- 全体 pytest は実施しない', '']
    (output / 'report.md').write_text('\n'.join(lines), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--catalog', required=True)
    parser.add_argument('--overlap', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    catalog = json.loads(Path(args.catalog).read_text(encoding='utf-8'))
    overlap = json.loads(Path(args.overlap).read_text(encoding='utf-8'))
    report, _ = build_trial(catalog, overlap, catalog_digest=sha256(args.catalog),
                            overlap_digest=sha256(args.overlap))
    write_report(report, args.output)
    print(json.dumps({k: v for k, v in report.items() if k != 'trial_items'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

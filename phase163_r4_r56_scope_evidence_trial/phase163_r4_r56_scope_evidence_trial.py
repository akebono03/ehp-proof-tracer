"""R4-R56: source-grounded scope evidence for three isolated R55 definitions."""
import argparse
import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ScopeEvidence:
    variable_symbols: tuple[str, ...]
    domain_tex: str | None
    codomain_tex: str | None
    cases: tuple[tuple[str, str], ...]
    qualification: str
    evidence_locator: str
    source_unit_id: str
    status: str = 'SOURCE_TEX_EXPLICIT_NOT_FORMAL_AST'


# Only literal formula fragments visible in catalog TeX are admitted.
SCOPE_RULES = {
    '(2.9)': {
        'symbols': ('m', 'i'),
        'domain': r'\pi_{i+1}(S^{2m+1})',
        'codomain': r'\pi_{i-1}(S^m)\big/\partial\Ker(h_{m*})',
        'cases': (),
        'qualification': 'NONE_EXPLICIT_IN_DEFINITION_EQUATION',
        'context_note': 'The adjacent statement about odd m or i<3m-1 describes the quotient denominator, not a verified global map condition.',
    },
    '(2.10)': {
        'symbols': ('m', 'i'),
        'domain': r'\pi_{i-1}(S^m)',
        'codomain': r'\pi_{i+1}(S^{2m+1})\big/ H\pi_{i+1}(S^{m+1})',
        'cases': (),
        'qualification': 'NONE_EXPLICIT_IN_DEFINITION_EQUATION',
        'context_note': 'No additional range or invertibility assumption is inferred from the superscript -1 notation.',
    },
    '(4.3)': {
        'symbols': ('i', 'n'),
        'domain': None,
        'codomain': None,
        'cases': (
            (r'i=n', r'\pis{n}{S^n}'),
            (r'i=2n-1', r'\Ex^{-1}\bigl(\pis{2n}{S^{n+1};2}\bigr)'),
            (r'i\ne n,\,2n-1', r'\pis{i}{S^n;2}'),
        ),
        'qualification': 'THREE_CASES_EXPLICIT',
        'context_note': 'This is a piecewise subgroup definition, not a map with a domain and codomain.',
    },
}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _compact(tex):
    return ''.join(tex.split())


def _evidence(body, piece, locator):
    if _compact(piece) not in _compact(body):
        raise ValueError(f'missing source evidence for {locator}: {piece}')


def build_scope_report(catalog, trial, *, catalog_digest=None, trial_digest=None):
    if catalog.get('phase') != '163 R4-R47' or trial.get('phase') != '163 R4-R55':
        raise ValueError('unexpected phase')
    if catalog.get('item_count') != 108 or trial.get('trial_definition_count') != 3:
        raise ValueError('unexpected input counts')
    if trial.get('production_registry_modified') or trial.get('production_ids_allocated'):
        raise ValueError('production mutation in input')
    if trial.get('formal_mathematical_ast_count') != 0:
        raise ValueError('trial is no longer a source-only record')
    by_locator = {r['locator']: r for r in catalog['items'] if r.get('locator')}
    by_trial = {r['locator']: r for r in trial['trial_items']}
    if set(by_trial) != set(SCOPE_RULES):
        raise ValueError('unexpected trial locators')
    entries = []
    for locator, rule in SCOPE_RULES.items():
        src = by_locator[locator]
        previous = by_trial[locator]
        body = src['tex_body']
        digest = hashlib.sha256(body.encode('utf-8')).hexdigest()
        if digest != src['sha256_tex_body'] or digest != previous['tex_sha256']:
            raise ValueError('TeX checksum mismatch: ' + locator)
        if (src['source_unit_id'] != previous['source_unit_id'] or
                src['publication_position'] != previous['publication_position'] or
                src['reference_id'] is not None or src['SOURCE_VERIFIED'] or
                previous['production_registration_applied']):
            raise ValueError('source unit or registration boundary mismatch: ' + locator)
        for expr in (rule['domain'], rule['codomain']):
            if expr is not None:
                _evidence(body, expr, locator)
        for condition, value in rule['cases']:
            _evidence(body, condition, locator)
            _evidence(body, value, locator)
        # This stores exact cited TeX segments, not inferred mathematical types.
        scope = ScopeEvidence(rule['symbols'], rule['domain'], rule['codomain'],
                              tuple(rule['cases']), rule['qualification'], locator,
                              src['source_unit_id'])
        entries.append({
            'locator': locator, 'r48_index': previous['r48_index'],
            'publication_position': src['publication_position'],
            'source_unit_id': src['source_unit_id'], 'source_file': src['source_file'],
            'equation_source_line': src['source_line'],
            'trial_assertion_id': previous['trial_assertion_id'],
            'defined_symbol': previous['defined_symbol'],
            'variables': list(scope.variable_symbols),
            'domain_tex': scope.domain_tex, 'codomain_tex': scope.codomain_tex,
            'cases': [{'condition_tex': k, 'value_tex': v} for k, v in scope.cases],
            'condition_status': scope.qualification,
            'context_boundary_note': rule['context_note'],
            'scope_status': scope.status,
            'source_tex_sha256': digest,
            'formal_mathematical_ast_parsed': False,
            'original_edition_verified': False,
            'production_registration_applied': False,
        })
    return {
        'phase': '163 R4-R56', 'mode': 'ISOLATED_EXPLICIT_SCOPE_EVIDENCE_TRIAL',
        'catalog_input_sha256': catalog_digest, 'r55_input_sha256': trial_digest,
        'scope_record_count': len(entries),
        'domain_codomain_record_count': sum(x['domain_tex'] is not None for x in entries),
        'piecewise_record_count': sum(bool(x['cases']) for x in entries),
        'case_count': sum(len(x['cases']) for x in entries),
        'conditions_inferred_count': 0, 'formal_mathematical_ast_count': 0,
        'candidate_total': trial['candidate_total'],
        'untouched_candidate_count': trial['untouched_candidate_count'],
        'pending_other_candidates_count': trial['pending_other_candidates_count'],
        'production_registry_modified': False, 'production_ids_allocated': False,
        'proof_search_connected': False, 'original_edition_verified': False,
        'scope_items': entries,
    }


def write_report(report, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output/'scope.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    with (output/'scope.csv').open('w', newline='', encoding='utf-8-sig') as stream:
        columns = ('locator','r48_index','publication_position','source_file','equation_source_line',
                   'defined_symbol','variables','domain_tex','codomain_tex','cases','condition_status',
                   'context_boundary_note','scope_status')
        writer=csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for entry in report['scope_items']:
            writer.writerow({key: json.dumps(entry[key],ensure_ascii=False) if isinstance(entry[key],list) else entry[key] for key in columns})
    lines = [
        '# Phase 163 R4-R56 適用範囲の出典付き試行', '',
        '- 対象：(2.9) Δ、(2.10) Δ^{-1}、(4.3) π_i^n',
        '- (2.9), (2.10)：TeX に明記された定義域・値域を保持',
        '- (4.3)：TeX に明記された 3 場合分けを保持',
        '- m, i, n は式の変数として記録するが、量化・変数型は推定しない',
        '- (2.9) の周辺にある m の奇偶等は商の分母の説明であり、Δ の一般適用条件として昇格しない',
        '- 記録は TeX の明示的断片に限る。形式的 AST、数学的同値性、原本照合は未完了',
        '- 仮 ID 以外の ID は発行しない。本番 Registry、TeX、証明探索は変更しない',
        '- その他 16 定義候補、237 未判定候補は維持。全体 pytest は実行しない', ''
    ]
    (output/'report.md').write_text('\n'.join(lines),encoding='utf-8')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--catalog',required=True)
    parser.add_argument('--trial',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    catalog=json.loads(Path(args.catalog).read_text(encoding='utf-8'))
    trial=json.loads(Path(args.trial).read_text(encoding='utf-8'))
    report=build_scope_report(catalog,trial,catalog_digest=sha256(args.catalog),trial_digest=sha256(args.trial))
    write_report(report,args.output)
    print(json.dumps({key:value for key,value in report.items() if key != 'scope_items'},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()

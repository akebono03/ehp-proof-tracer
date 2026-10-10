"""Phase 163 R4-R17: conservative registration of Chapter I named statements."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

EXPECTED = (
    ('lem:double-coset', 'Lemma 1.1', 'double_coset', 'Toda bracket is a double coset; under commutativity it is a coset.', 'Composites defining the secondary composition vanish.'),
    ('prop:1-2', 'Proposition 1.2', 'composition_properties', 'Five separate zero and composition inclusion properties of secondary compositions.', 'Specified zero-composite conditions for each clause.'),
    ('prop:1-3', 'Proposition 1.3', 'loop_and_suspension', 'Looping identity and suspension inclusion for secondary compositions.', 'n >= 0.'),
    ('prop:1-4', 'Proposition 1.4', 'composition_relation', 'Relation between right composition of a bracket and left composition of another bracket, with sign.', 'Three consecutive zero-composite conditions.'),
    ('prop:1-5', 'Proposition 1.5', 'higher_coherence', 'Under specified vanishing conditions, a sum of three secondary compositions contains zero.', 'Four consecutive zero composites and two bracket-composite zero-memberships.'),
    ('prop:1-6', 'Proposition 1.6', 'additivity', 'Three conditional additivity relations for secondary compositions.', 'Dimension or suspension-space restrictions specific to each relation.'),
    ('prop:1-7', 'Proposition 1.7', 'extension_coextension', 'Extension–coextension composite represents a signed secondary composition.', 'Two zero composites and extension/coextension choices.'),
    ('prop:1-8', 'Proposition 1.8', 'coextension_relation', 'A coextension composition equals the negative induced image of a secondary composition.', 'Hypotheses of Proposition 1.7 and a coextension.'),
    ('prop:1-9', 'Proposition 1.9', 'extension_coset', 'Existence and coset description of extensions corresponding to bracket elements.', 'Hypotheses of Proposition 1.7 and an extension.'),
)
PATTERN = re.compile(r'\\begin\{(lemma|proposition)\}(?:\[[^\]]*\])?\s*\\label\{([^}]+)\}(.*?)\\end\{\1\}', re.S)
CLAUSE = re.compile(r'\\item\[([^\]]+)\]')


def register(source: Path) -> dict:
    data = source.read_bytes()
    text = data.decode('utf-8-sig')
    # Normalize newlines for stable line numbers across platforms.
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    found = list(PATTERN.finditer(text))
    labels = [match.group(2) for match in found]
    if labels != [row[0] for row in EXPECTED]:
        raise ValueError('Chapter I labels/order differ from reviewed source; manual re-review required')
    result = []
    for i, (match, spec) in enumerate(zip(found, EXPECTED), 1):
        label, locator, semantic_type, interpretation, hypotheses = spec
        body = match.group(3).strip()
        line = text.count('\n', 0, match.start()) + 1
        clause_markers = CLAUSE.findall(body)
        entries = {
            'statement_id': f'TODA-S{i:06d}',
            'chapter': 1,
            'section': 'Chapter I',
            'order_key': str(i),
            'kind': 'Lemma' if label.startswith('lem:') else 'Proposition',
            'locator': locator,
            'tex_label': label,
            'source_line': line,
            'source_statement_tex': body,
            'statement_type': semantic_type,
            'summary_en': interpretation,
            'hypotheses_en': hypotheses,
            'internal_clause_markers': clause_markers,
            'source_status': 'unchecked',
            'transcription_review': 'reviewed_against_supplied_tex',
            'search_status': 'unconnected',
            'existing_component_keys': [],
            'legacy_identity_status': 'unverified',
            'source_statement_sha256': hashlib.sha256(body.encode('utf-8')).hexdigest(),
        }
        result.append(entries)
    return {
        'schema_version': 'r4-r17-chapter1-named-1',
        'source_file': source.name,
        'source_sha256': hashlib.sha256(data).hexdigest(),
        'entries': result,
        'scope': 'Nine named statement environments only; prose definitions and other equations remain to review',
    }


def run(source: Path, output: Path) -> dict:
    payload = register(source)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'named_statements.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    summary = {
        'phase': '163 R4-R17',
        'named_statements_registered': len(payload['entries']),
        'statement_ids_reserved': len(payload['entries']),
        'transcription_reviewed_against_supplied_tex': len(payload['entries']),
        'original_publication_verified': 0,
        'legacy_equivalence_verified': 0,
        'search_connected': 0,
        'unreviewed_scope': ['prose definitions', 'inline mathematical claims', 'standalone equations', 'components within named statements'],
    }
    (output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Phase 163 R4-R17 — 第1章の名前付き命題登録', '',
             '提供された TeX の命題本文を9件、掲載順に保存した。Statement ID は恒久的に再使用しない。',
             '出典状態 unchecked は印刷原典との照合が未完了であることを表す。',
             '既存台帳への数学的同一性の接続、および証明探索への接続は未実施。', '', '## 登録項目', '']
    for entry in payload['entries']:
        lines.append(f"- {entry['statement_id']}: {entry['locator']}（TeX {entry['source_line']}行、内部列挙 {len(entry['internal_clause_markers'])}箇所）— {entry['summary_en']}")
    lines += ['', '## 未完了', '', '本文定義・独立数式の内容確認、命題内の数学的成分分割、既存67成分との同一性照合。', '全体 pytest は Phase 163 の終了時にだけ行う。', '']
    (output / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

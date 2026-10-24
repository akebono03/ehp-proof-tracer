"""R3-41P11: audit the search-screened GIVEN -> Narrative Model boundary.

No application files are changed. This audit does NOT certify a proof: it only
checks that the exact used GIVEN is explicitly linked to a fixed assertion
in the same screened bridge that the public Web path supplied to the Model.
Proof-order/publication admissibility requires separate independent evidence.
"""
from __future__ import annotations

import json
import re
import traceback
from pathlib import Path
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / 'output'
CASES = (('pi3_2', 2, 1), ('pi4_3', 3, 1), ('pi5_4', 4, 1))


def same_content(a: str, b: str) -> bool:
    return a.replace('\r\n', '\n').replace('\r', '\n') == b.replace('\r\n', '\n').replace('\r', '\n')


def matching_step_links(bridge, step):
    """Use exactly the step-identity/value policy of build_linked_proof_narrative_model."""
    return tuple(
        link for link in bridge.proof_links
        if link.step is not None and (link.step is step or link.step == step)
    )


def audit_given_provenance(model, bridge):
    """Observe fixed-source links, without equating source identity with proof validity."""
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    entries = []
    for index, step in enumerate(model.steps):
        if step.rule is not ProofRule.GIVEN:
            continue
        linked = []
        for link in matching_step_links(bridge, step):
            assertion = bridge.registry.assertion(link.assertion_id)
            ref = bridge.registry.reference(assertion.reference_id)
            matched_content = (
                assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and type(assertion.content) is type(step.conclusion)
                and assertion.content == step.conclusion
                and link.step.rule is ProofRule.GIVEN
            )
            matching_reference_citations = tuple(
                cite.number for cite in model.citations
                if assertion.reference_id in cite.reference_ids
                and index in cite.step_indices
            )
            cited_numbers = model.step_citation_numbers[index]
            linked.append({
                'assertion_id': assertion.assertion_id,
                'reference_id': assertion.reference_id,
                'locator': ref.locator,
                'origin': assertion.origin.value,
                'publication_position': ref.publication_position,
                'component_position': assertion.component_position,
                'fixed_content_matches': matched_content,
                'model_citation_numbers': list(cited_numbers),
                'linked_citation_numbers': list(matching_reference_citations),
                'citation_corresponds': bool(set(matching_reference_citations).intersection(cited_numbers)),
            })
        entries.append({
            'index': index,
            'statement_type': type(step.conclusion).__name__,
            'screened_link_count': len(linked),
            'linked': linked,
            'source_link_present': bool(linked),
            'fixed_source_and_citation': bool(linked) and any(
                item['fixed_content_matches'] and item['citation_corresponds']
                for item in linked
            ),
        })
    return {
        'given_count': len(entries),
        'linked_count': sum(item['source_link_present'] for item in entries),
        'fixed_cited_count': sum(item['fixed_source_and_citation'] for item in entries),
        'missing_link_indices': [item['index'] for item in entries if not item['source_link_present']],
        'not_fixed_and_cited_indices': [item['index'] for item in entries if not item['fixed_source_and_citation']],
        'entries': entries,
        'publication_order_reverified': False,
        'why_not_certified': 'Screened membership and citations alone do not independently prove publication order or rule correctness.',
    }


def capture_public_search_context(n: int, k: int):
    """Capture the screened bridge used by the SAME public Web rendering call."""
    import phase168_r3_4_link_bridge as link_bridge
    import phase168_r3_5_model_renderer as renderer
    from web_group_proof import build_standard_web_group_proof_view

    samples = {'bridges': [], 'renderings': []}
    original_link = link_bridge.build_linked_proof_narrative_model
    original_render = renderer.render_model_backed_narrative_markdown

    def capture_link(result, bridge):
        model = original_link(result, bridge)
        samples['bridges'].append((result, bridge, model))
        return model

    def capture_render(result, model):
        text = original_render(result, model)
        samples['renderings'].append((result, model, text))
        return text

    with patch.object(link_bridge, 'build_linked_proof_narrative_model', side_effect=capture_link), \
         patch.object(renderer, 'render_model_backed_narrative_markdown', side_effect=capture_render):
        build_standard_web_group_proof_view(n=n, k=k)

    if len(samples['bridges']) != 1 or len(samples['renderings']) != 1:
        raise AssertionError('Expected one common Web Link Bridge and one common Model Renderer')
    search_result, bridge, model = samples['bridges'][0]
    rendered_result, rendered_model, markdown = samples['renderings'][0]
    if search_result is not rendered_result or model is not rendered_model:
        raise AssertionError('Public Web did not render the same searched result and screened bridge model')
    return markdown, search_result, model, bridge


def counterfeit_given(bridge):
    """A made-up GIVEN can inhabit a result/model but is not in screened sources."""
    from phase165_r52_partial_proof import make_partial_proof_result, ProofSearchStatus
    from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
    from proof import ProofStep, ProofRule
    marker = 'R3-41P11 artificial unregistered given'
    fake_step = ProofStep(conclusion=marker, premises=(), rule=ProofRule.GIVEN)
    result = make_partial_proof_result(
        n=2, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(fake_step,), conclusion=marker,
    )
    fake_model = build_proof_narrative_model(result)
    sources = audit_given_provenance(fake_model, bridge)
    return {
        'model_accepts_fake_given': len(fake_model.steps) == 1,
        'screened_source_gate_rejects': sources['given_count'] == 1 and sources['linked_count'] == 0,
        'given_provenance': sources,
    }


def markdown_report(report):
    lines = [
        '# Phase 168 R3-41P11 — GIVEN provenance / screened bridge audit',
        '',
        '本監査は、公開Web経路で使用されたGIVENと、同一検索で選別された命題台帳との対応を確認する。',
        '証明の新規検証や証明書の発行はしない。GIVENの存在だけで文献順と数学的正当性を保証しない。',
        '',
        '| 対象 | GIVEN | Screened Linkあり | FIXEDかつCitation対応 | 全文一致 |',
        '|---|---:|---:|---:|---|',
    ]
    for name, item in report.get('cases', {}).items():
        a = item.get('given_audit', {})
        lines.append(f'| {name} | {a.get("given_count", "?")} | {a.get("linked_count", "?")} | '
                     f'{a.get("fixed_cited_count", "?")} | {item.get("fulltext_equal", False)} |')
    lines += [
        '', '## 未解決の信頼境界',
        '- `PartialProofResult` と `ProofNarrativeModel` は依然として、偽のGIVEN/INFERENCEを直接受け入れ得る。',
        '- FIXEDな出典へのリンクは必要条件だが、文献順（publication_position/component_position）の独立証明ではない。',
        '- 公開経路のソース選別を通過したという経路上の事実と、Model自身の保証を区別する。',
        '- 本監査はアプリ本体・既存テストを変更しない。全体pytestは実行しない。',
        '', '## 人工GIVEN',
        f'- Modelへの格納: {report.get("counterfeit", {}).get("model_accepts_fake_given")}',
        f'- Screened源に存在しないと検出: {report.get("counterfeit", {}).get("screened_source_gate_rejects")}',
        '', f'**AUDIT_STATUS**: {report.get("status")}',
        '**FULL_PYTEST_NOT_RUN**', '',
    ]
    if report.get('error'):
        lines.extend(['```text', report['error'], '```', ''])
    return '\n'.join(lines)


def main():
    OUTPUT.mkdir(exist_ok=True)
    report = {'phase': 'R3-41P11', 'audit_only': True, 'cases': {}, 'status': 'ERROR'}
    try:
        from phase168_r3_38_frozen_fulltext_audit.audit import sections
        from phase168_r3_39f_frozen_comparison.audit import assess
        from proof import ProofRule
        first_bridge = None
        for name, n, k in CASES:
            markdown, result, model, bridge = capture_public_search_context(n, k)
            if first_bridge is None:
                first_bridge = bridge
            baseline = (PACKAGE / 'baselines' / (name + '_current.md')).read_text(encoding='utf-8-sig')
            reference, proof = sections(markdown)
            citations_used = {int(x) for x in re.findall(r'\[R(\d+)\]', proof)}
            citation_numbers = {x.number for x in model.citations}
            given_audit = audit_given_provenance(model, bridge)
            inference_count = sum(step.rule is ProofRule.INFERENCE for step in model.steps)
            item = {
                'steps': len(model.steps),
                'inference_count': inference_count,
                'fulltext_equal': same_content(markdown, baseline),
                'citations_ok': citations_used == citation_numbers,
                'benchmark_ok': all(x['present'] for x in assess(name, proof)),
                'given_audit': given_audit,
                'screened_bridge_link_count': len(bridge.proof_links),
            }
            (OUTPUT / (name + '_current.md')).write_text(markdown, encoding='utf-8')
            report['cases'][name] = item
            print(f'{name} GIVEN={given_audit["given_count"]} LINKED={given_audit["linked_count"]} '
                  f'FIXED_CITED={given_audit["fixed_cited_count"]} '
                  f'FULLTEXT={item["fulltext_equal"]} CITATIONS={item["citations_ok"]}', flush=True)
        report['counterfeit'] = counterfeit_given(first_bridge)
        print(f'FAKE_GIVEN MODEL_ACCEPTS={report["counterfeit"]["model_accepts_fake_given"]} '
              f'SCREENED_REJECTS={report["counterfeit"]["screened_source_gate_rejects"]}', flush=True)
        base_ok = len(report['cases']) == 3 and all(
            item['fulltext_equal'] and item['citations_ok'] and item['benchmark_ok']
            and item['inference_count'] == {'pi3_2': 13, 'pi4_3': 19, 'pi5_4': 7}[name]
            for name, item in report['cases'].items()
        )
        forged = report['counterfeit']['model_accepts_fake_given'] and report['counterfeit']['screened_source_gate_rejects']
        report['status'] = 'PASS' if base_ok and forged else 'FAIL'
        report['source_coverage_complete'] = all(
            item['given_audit']['fixed_cited_count'] == item['given_audit']['given_count']
            for item in report['cases'].values()
        )
        report['publication_order_reverified'] = False
    except Exception:
        report['error'] = traceback.format_exc()
        report['status'] = 'ERROR'
    (OUTPUT / 'audit.json').write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding='utf-8')
    (OUTPUT / 'audit.md').write_text(markdown_report(report), encoding='utf-8')
    print('AUDIT_STATUS', report['status'])
    print('REPORT', OUTPUT / 'audit.md')
    print('APPLICATION_SOURCE_UNCHANGED')
    print('FULL_PYTEST_NOT_RUN')
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())

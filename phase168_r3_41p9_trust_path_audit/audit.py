"""R3-41P9: audit the trust handoff; never mutate project application files."""
from __future__ import annotations

import hashlib
import json
import traceback
from collections import Counter
from pathlib import Path
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / 'output'
BASELINES = PACKAGE / 'baselines'
CASES = (("pi3_2", 2, 1), ("pi4_3", 3, 1), ("pi5_4", 4, 1))
SOURCE_FILES = (
    'phase165_r3_recursive_search.py',
    'phase164_r8_proofstep_factory.py',
    'phase165_r55_nk_only_goal.py',
    'phase165_r52_partial_proof.py',
    'phase168_r3_3_proof_narrative_model.py',
    'phase168_r3_4_link_bridge.py',
    'phase168_r3_5_model_renderer.py',
    'phase168_r3_27_typed_statement_projection.py',
    'web_group_proof.py',
    'proof.py',
)


def source_fingerprints(root=ROOT):
    return {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest()
        if (root / name).is_file() else None
        for name in SOURCE_FILES
    }


def inferential_steps(steps):
    from proof import ProofRule
    return tuple(step for step in steps if step.rule is ProofRule.INFERENCE)


def capture_path(name, n, k):
    """Observe matching/derivation along the genuine public entry without replaying guards."""
    import phase165_r3_recursive_search as search
    import phase164_r8_proofstep_factory as factory
    from phase168_r3_38_frozen_fulltext_audit.audit import capture, sections
    from phase168_r3_39f_frozen_comparison.audit import assess

    counters = Counter()
    matched_rules = []
    derived_ids = set()
    derived_rules = []
    original_match = search.find_inference_matches_for_rule
    original_derive = search.derive_inference_proof_step
    original_apply = factory.apply_inference_match

    def observe_match(rule, premises):
        counters['matcher_calls'] += 1
        matches = original_match(rule, premises)
        counters['accepted_matches'] += len(matches)
        for match in matches:
            matched_rules.append(str(getattr(match.inference_rule, 'name', type(match.inference_rule).__name__)))
        return matches

    def observe_apply(match):
        counters['factory_apply_calls'] += 1
        return original_apply(match)

    def observe_derive(match):
        counters['derive_calls'] += 1
        step = original_derive(match)
        derived_ids.add(id(step))
        derived_rules.append(str(getattr(match.inference_rule, 'name', type(match.inference_rule).__name__)))
        return step

    with patch.object(search, 'find_inference_matches_for_rule', side_effect=observe_match), \
         patch.object(search, 'derive_inference_proof_step', side_effect=observe_derive), \
         patch.object(factory, 'apply_inference_match', side_effect=observe_apply):
        fulltext, model, _ = capture(n, k)

    actual_baseline = (BASELINES / (name + '.md')).read_text(encoding='utf-8')
    fulltext_ok = actual_baseline == fulltext
    (OUTPUT / (name + '_current.md')).write_text(fulltext, encoding='utf-8')
    if not fulltext_ok:
        import difflib
        diff = ''.join(difflib.unified_diff(
            actual_baseline.splitlines(keepends=True),
            fulltext.splitlines(keepends=True),
            fromfile='R3-41P8', tofile='R3-41P9',
        ))
        (OUTPUT / (name + '_difference.diff')).write_text(diff, encoding='utf-8')

    references, proof = sections(fulltext)
    import re
    used = {int(value) for value in re.findall(r'\[R(\d+)\]', proof)}
    documented = {citation.number for citation in model.citations}
    inference = inferential_steps(model.steps)
    observed = [step for step in inference if id(step) in derived_ids]
    other = [step for step in inference if id(step) not in derived_ids]
    benchmark = all(item['present'] for item in assess(name, proof))
    return {
        'steps': len(model.steps),
        'inference_step_count': len(inference),
        'observed_factory_step_count': len(observed),
        'other_inference_step_count': len(other),
        'other_inference_types': Counter(type(x.conclusion).__name__ for x in other),
        'other_inference_rule_names': sorted({str(getattr(x.inference_rule, 'name', '')) for x in other}),
        'references': len(model.citations),
        'citations_ok': used == documented and bool(references),
        'fulltext_equal': fulltext_ok,
        'benchmark_ok': benchmark,
        'source_match': counters['matcher_calls'],
        'accepted_matches': counters['accepted_matches'],
        'factory_apply_calls': counters['factory_apply_calls'],
        'derive_calls': counters['derive_calls'],
        'derived_rule_names': sorted(set(derived_rules)),
        'note': 'Only calls observed during this capture are counted; unobserved steps are not necessarily invalid.',
    }


def forged_result_model_acceptance():
    """Probe the data-object boundary, not a forged literature premise."""
    from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
    from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
    from proof import InferenceRule, ProofRule, ProofStep, find_inference_matches_for_rule
    fake_rule = InferenceRule(
        name='AUDIT COUNTERFEIT - guard always rejects',
        premise_patterns=(),
        conclusion_pattern='unproved-claim',
        match_guard=lambda premises, bindings: False,
    )
    fake_step = ProofStep('unproved-claim', (), ProofRule.INFERENCE, inference_rule=fake_rule)
    accepted_by_matcher = bool(find_inference_matches_for_rule(fake_rule, ()))
    result = make_partial_proof_result(
        n=2, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(fake_step,), conclusion='unproved-claim',
    )
    model = build_proof_narrative_model(result)
    return {
        'matcher_accepts': accepted_by_matcher,
        'partial_result_accepts': result.conclusion == fake_step.conclusion,
        'narrative_model_accepts': model.steps == (fake_step,),
        'contains_explicit_verified_derivation_certificate': hasattr(model, 'verified_inference_matches'),
        'meaning': 'A complete result and citation model do not attest that the inference matcher produced each ProofStep.',
    }


def write_report(data):
    lines = [
        '# Phase 168 R3-41P9 — trust handoff audit',
        '',
        '監査のみ。既存の Renderer、Backward Search、Model、テストは変更しない。',
        '',
        '## 公開 Web 経路の限定トレース',
        '',
        '| 群 | Step | 推論 Step | この監査で導出生成を観測 | その他の推論 Step | Reference | 前回全文一致 | Citation | 固定基準 |',
        '|---|---:|---:|---:|---:|---:|---|---|---|',
    ]
    for name, _, _ in CASES:
        if name not in data['cases']:
            continue
        c = data['cases'][name]
        lines.append(
            f"| {name} | {c['steps']} | {c['inference_step_count']} | "
            f"{c['observed_factory_step_count']} | {c['other_inference_step_count']} | "
            f"{c['references']} | {c['fulltext_equal']} | {c['citations_ok']} | {c['benchmark_ok']} |"
        )
    lines += [
        '',
        '※「その他」はこの一回の計測区間に導出関数を通るところを直接観測していない Step であり、誤りと同義ではない。',
        '',
        '## 人工入力に対する信頼境界',
        '',
    ]
    for k, v in data.get('forgery', {}).items():
        lines.append(f'- `{k}`: `{v}`')
    lines += [
        '',
        '## コード経路に関する注意',
        '',
        '- 共通探索内の `find_inference_matches_for_rule()` は guard を評価する。',
        '- `derive_inference_proof_step()` は既存の `apply_inference_match()` を通す。',
        '- `PartialProofResult` の COMPLETE 判定は、結論の存在と既存 Step との一致を確認するが、全推論の guard 成功履歴を認証しない。',
        '- `build_proof_narrative_model()` は Citation を射影する。証明規則の検証履歴を証明書として持たない。',
        '- したがって Renderer の残る数学的チェックは、信頼境界を保証する設計・回帰テストができるまでは維持すべきである。',
        '',
        '監査結果の数値だけで既存 Backward Search の健全性全般を宣言しない。',
        '',
        f"**AUDIT_STATUS**: {data['status']}",
        '**FULL_PYTEST_NOT_RUN**',
    ]
    (OUTPUT / 'audit.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    data = {'phase':'R3-41P9','audit_only':True,'sources':source_fingerprints(),'cases':{}}
    try:
        for name,n,k in CASES:
            c = capture_path(name,n,k)
            data['cases'][name] = c
            print(f"{name} steps={c['steps']} refs={c['references']} "
                  f"FULLTEXT={c['fulltext_equal']} CITATIONS={c['citations_ok']} "
                  f"FACTORY_STEPS_OBSERVED={c['observed_factory_step_count']} "
                  f"OTHER_INFERENCE={c['other_inference_step_count']}",flush=True)
        data['forgery'] = forged_result_model_acceptance()
        print('COUNTERFEIT matcher_accepts=',data['forgery']['matcher_accepts'],
              'model_accepts=',data['forgery']['narrative_model_accepts'],flush=True)
        checks = [
            all(c['fulltext_equal'] and c['citations_ok'] and c['benchmark_ok']
                for c in data['cases'].values()),
            data['forgery']['matcher_accepts'] is False,
            data['forgery']['partial_result_accepts'] is True,
            data['forgery']['narrative_model_accepts'] is True,
        ]
        data['status'] = 'PASS' if all(checks) else 'FAIL'
        data['checks'] = checks
    except Exception:
        data['status'] = 'ERROR'
        data['traceback'] = traceback.format_exc()
        print('AUDIT_ERROR:',data['traceback'],flush=True)
    (OUTPUT / 'audit.json').write_text(json.dumps(data,ensure_ascii=False,indent=2,default=list)+'\n',encoding='utf-8')
    write_report(data)
    print('AUDIT_STATUS',data['status'],flush=True)
    print('REPORT',OUTPUT / 'audit.md',flush=True)
    print('APPLICATION_SOURCE_UNCHANGED',flush=True)
    print('FULL_PYTEST_NOT_RUN',flush=True)
    return 0 if data['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())

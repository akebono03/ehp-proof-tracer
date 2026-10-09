"""Compare ordinary and newly derived proof roots using the existing common renderer.

Read-only audit. Does not call the public stable-specific renderer.
"""

import json
from pathlib import Path

from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_stable_eta_proof_replay import build_toda_stable_eta_proof_replay
from toda_group_proof_narrative_renderer import (
    _phase158_baseline_render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_references import (
    build_toda_group_proof_narrative_reference_entries,
)


def _source_result(n):
    presentation, _, _, _ = _method_evidence_data(n, 1)
    return presentation.source_replay.group_result, presentation


def _render_or_error(presentation):
    try:
        return _phase158_baseline_render_toda_group_proof_narrative_markdown(presentation), None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def _entries(presentation):
    return [
        {
            "locator": entry.reference.locator,
            "step_count": len(entry.proof_steps),
            "contains_root": any(step is presentation.root_step for step in entry.proof_steps),
            "root_equivalent": any(
                step.conclusion == presentation.root_step.conclusion
                for step in entry.proof_steps
            ),
            "step_types": [type(step.conclusion).__name__ for step in entry.proof_steps],
        }
        for entry in build_toda_group_proof_narrative_reference_entries(presentation)
    ]


def _flags(markdown):
    if markdown is None:
        return None
    reference_section = markdown.split('## 使用する結果', 1)[-1].split('## 証明', 1)[0] if '## 使用する結果' in markdown else ''
    return {
        "has_symbolic_n": any(x in markdown for x in (r'\eta_{n}', r'\pi_{n + 1}^{n}', r'E^{n - 3}')),
        "reference_toda45": '(4.5)' in reference_section,
        "has_transport_appendage": '証明木に記録された群構造の移送について' in markdown,
        "transition_double": any(x in markdown for x in ('これより, これより', 'これより, 以上より')),
    }


def audit_one(n):
    result, original = _source_result(n)
    base, _ = _source_result(3)
    integrated = build_toda_stable_eta_proof_replay(result, base, max_depth=3)
    old_text, old_error = _render_or_error(original)
    new_text, new_error = _render_or_error(integrated.presentation)
    return {
        "n": n,
        "target": f"pi_{n+1}^{n}",
        "old_root_is_derived_root": original.root_step is integrated.presentation.root_step,
        "derived_root_rule": getattr(integrated.presentation.root_step.inference_rule, 'name', None),
        "derived_root_premises": len(integrated.presentation.root_step.premises),
        "old_references_before_filtering": _entries(original),
        "derived_references_before_filtering": _entries(integrated.presentation),
        "old_flags": _flags(old_text),
        "derived_flags": _flags(new_text),
        "old_render_error": old_error,
        "derived_render_error": new_error,
        "old_markdown": old_text,
        "derived_markdown": new_text,
    }


def write_audit(output_directory):
    path = Path(output_directory)
    path.mkdir(parents=True, exist_ok=True)
    records = [audit_one(n) for n in (4, 5)]
    (path / 'audit.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    report = ['# Phase 162 R4-B3 共通Renderer出力監査', '', '既存の公開stable専用Rendererは呼び出していない。', '既存rootと新しい導出rootを比較した観測結果。', '']
    for r in records:
        report += [f"## {r['target']}", '', '### 旧rootからの共通Renderer', '', f"エラー: {r['old_render_error']}", '', f"flags: `{r['old_flags']}`", '', '```text', r['old_markdown'] or '(render failed)', '```', '', '### 新しい導出rootからの共通Renderer', '', f"エラー: {r['derived_render_error']}", '', f"flags: `{r['derived_flags']}`", '', '```text', r['derived_markdown'] or '(render failed)', '```', '']
    (path / 'comparison.md').write_text('\n'.join(report), encoding='utf-8')
    return records


if __name__ == '__main__':
    records = write_audit(Path(__file__).resolve().parent / 'phase162_r4_b3_common_renderer_audit' / 'audit_output')
    for record in records:
        print(record['target'], 'old:', record['old_flags'], 'derived:', record['derived_flags'], 'error:', record['derived_render_error'])

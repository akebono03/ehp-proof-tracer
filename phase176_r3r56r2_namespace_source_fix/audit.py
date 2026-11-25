"""Check the public current proof and repeat the isolated R56 observation."""
from __future__ import annotations

import ast
import json
from unittest.mock import patch

from phase165_r52_partial_proof import ProofSearchStatus
from phase176_r3r56_cited_source_display_isolated import audit as r56
from phase176_r3r56r2_namespace_source_fix.apply import (
    TARGET, artifact_folder, baseline_source, function_node, preflight, updated_source,
)


def main():
    from phase176_r3r46r1_prior_group_availability.pytest_runner import canonical_hopf_modules
    canonical_hopf_modules()
    import phase168_r3_5_model_renderer as renderer
    import phase175_r3r11_cited_hopf_narrative.projection as source
    raw = preflight()
    if updated_source(raw) != raw:
        raise RuntimeError('NAMESPACE_FIX_NOT_APPLIED')
    base, _ = baseline_source(raw)
    node = function_node(base)
    namespace = dict(vars(source))
    exec(compile(ast.Module(body=[node], type_ignores=[]), '<reviewed legacy lookup>', 'exec'), namespace)
    old_lookup = namespace[node.name]
    current = renderer.render_model_backed_narrative_markdown
    captures = []

    def observe_render(result, model):
        before = r56.baseline.snapshot(model)
        new = current(result, model)
        with patch.object(source, '_source_citation', old_lookup):
            old = current(result, model)
        if before != r56.baseline.snapshot(model):
            raise RuntimeError('MODEL_CHANGED_DURING_NAMESPACE_COMPARISON')
        captures.append((result.status, old, new))
        return new

    git = r56.baseline.prior.git
    before = (git('diff', '--binary', 'HEAD'), git('status', '--porcelain'))
    # The R56 audit preflight has already been verified with the inverse pin.
    # Call its actual public observation; its prior exact source/body guards stay intact.
    with patch.object(renderer, 'render_model_backed_narrative_markdown', observe_render):
        report, _ = r56.observe()
    complete = [row for row in captures if row[0] is ProofSearchStatus.COMPLETE]
    partial = [row for row in captures if row[0] is not ProofSearchStatus.COMPLETE]
    if len(complete) != 1 or len(partial) != 1 or partial[0][1] != partial[0][2]:
        raise RuntimeError('PARTIAL_DISPLAY_CHANGED_OR_RENDER_COUNT')
    if before != (git('diff', '--binary', 'HEAD'), git('status', '--porcelain')):
        raise RuntimeError('REPOSITORY_CHANGED_DURING_AUDIT')
    folder = artifact_folder()
    (folder / 'legacy_lookup.md').write_text(complete[0][1], encoding='utf-8')
    (folder / 'actual_narrative.md').write_text(complete[0][2], encoding='utf-8')
    (folder / 'partial.md').write_text(partial[0][2], encoding='utf-8')
    report = dict(report, gate='PASS_R3R56R2_NAMESPACE_SOURCE_FIX_AND_R56_RECHECK',
                  namespace_fix='APPLIED', historical_test_changes=0,
                  model_unchanged=True, partial_render_unchanged=True,
                  repository_unchanged_during_audit=True)
    (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for key, value in report.items():
        if key != 'gate':
            print('PHASE176_R3R56R2_' + key.upper() + '=' + json.dumps(value, ensure_ascii=False))
    print('REPORT=' + str(folder / 'report.json'))
    print('PHASE176_R3R56R2_GATE=' + report['gate'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

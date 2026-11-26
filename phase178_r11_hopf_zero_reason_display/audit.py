"""Install the display-only hook and inspect the unchanged canonical proof."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
from unittest.mock import patch

from phase178_r11_hopf_zero_reason_display.installer import (
    ROOT, TARGET, SHARED, full_review_source, gt, preflight, require,
)

PREFIX = 'PHASE178_R11_'
TESTS = (
    'phase178_r11_hopf_zero_reason_display/tests/test_projection.py',
    'phase178_r11_hopf_zero_reason_display/tests/test_installer.py',
    'phase178_r11_hopf_zero_reason_display/tests/test_sentence_layout_audit.py',
    'phase175_r4r12r13r2_delta_injective_e_surjective/tests/test_rule.py',
    'phase178_r10_equal_cardinality_reason_display/tests/test_projection.py',
)


def emit(key, value):
    print(PREFIX+key+'='+str(value), flush=True)


def hopf_reason_displayed(markdown, sentence):
    """Require the two exact consecutive proof paragraphs after sentence layout."""
    if not isinstance(markdown, str) or not isinstance(sentence, str):
        return False
    separator = '. よって, '
    if sentence.count(separator) != 1:
        return False
    first, second = sentence.split(separator, 1)
    expected = (first + '.', 'よって, ' + second)
    lines = markdown.splitlines()
    if lines.count('証明') != 1:
        return False
    body = [line for line in lines[lines.index('証明')+1:] if line.strip()]
    if any(body.count(line) != 1 for line in expected):
        return False
    start = body.index(expected[0])
    return tuple(body[start:start+2]) == expected


def inspect_actual(folder):
    import phase168_r3_5_model_renderer as renderer
    from phase178_r1_k6_source_first_audit.audit import observe
    from phase178_r11_hopf_zero_reason_display.projection import project_hopf_zero_reason
    from phase175_r4r12r13r2_delta_injective_e_surjective.rule import E_RULE_NAME
    from phase178_r10_equal_cardinality_reason_display.projection import project_equal_cardinality_reason
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import MapSurjective
    from toda_rules import TodaHopfInvariantZeroStatement
    real = renderer.render_model_backed_narrative_markdown
    calls = []

    def observed(result, model):
        markdown = real(result, model)
        calls.append((result, model, markdown))
        return markdown

    with patch.object(renderer, 'render_model_backed_narrative_markdown', observed):
        summary = observe(3,6,folder)
    require(len(calls)==1,'RENDER_CAPTURE_MISSING_OR_AMBIGUOUS')
    result,model,markdown = calls[0]
    (folder/'narrative.md').write_text(markdown,encoding='utf-8')
    emit('NARRATIVE',folder/'narrative.md')
    require(summary['status']=='complete' and summary['open_goal_count']==0
            and summary['proven_step_count']==20 and summary['trust_status']=='VERIFIED'
            and summary['web_key']=='generic-complete-proof' and summary['target_given_count']==0
            and summary['complete_invariants_hold'] and summary['web_error'] is None,
            'R10_PROOF_INVARIANTS_CHANGED')
    require(len(model.citations)==5,'R10_CITATION_COUNT_CHANGED')
    goal = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(8,2),TodaPrimaryGroup(9,3)))
    accepted = [s for s in model.steps if s.conclusion == goal]
    require(len(accepted)==1 and accepted[0].inference_rule is not None,'E_SURJECTIVITY_STEP_MISSING')
    emit('E_SURJECTIVITY_RULE',accepted[0].inference_rule.name)
    emit('H_ZERO_STEP_COUNT',sum(isinstance(s.conclusion,TodaHopfInvariantZeroStatement) for s in model.steps))
    require(accepted[0].inference_rule.name==E_RULE_NAME,'ACTUAL_E_RULE_DIFFERS_REVIEW_REQUIRED')
    sentence = project_hopf_zero_reason(goal,accepted[0])
    emit('EXPECTED_REASON',sentence)
    require(sentence is not None,'HOPF_ZERO_PROJECTION_FAILED')
    require(hopf_reason_displayed(markdown,sentence),'HOPF_ZERO_REASON_NOT_DISPLAYED_AFTER_LAYOUT')
    emit('HOPF_ZERO_REASON_LAYOUT','TWO_CONSECUTIVE_PROOF_PARAGRAPHS')
    r10 = [text for s in model.steps if (text := project_equal_cardinality_reason(s.conclusion,s)) is not None]
    require(len(r10)==1 and markdown.count(r10[0])==1,'R10_DISPLAY_CHANGED')
    emit('ROOT_STATUS',summary['status'])
    emit('ROOT_STEPS',summary['proven_step_count'])
    emit('ROOT_OPEN_GOALS',summary['open_goal_count'])
    emit('REFERENCES',len(model.citations))
    emit('TRUST_STATUS',summary['trust_status'])
    emit('REASON',sentence)
    return dict(summary,reference_count=len(model.citations),corrected_sentence=sentence)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/Path(__file__).parent.name
    base.mkdir(parents=True,exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_',dir=base))
    report = {'gate':'FAIL_R11','dry_run':args.dry_run,'new_math_rules':0,'new_given':0,'full_pytest':'NOT_RUN'}
    try:
        head,current,updated,revised,shared_before = preflight()
        report['head']=head
        emit('HEAD',head)
        review = folder/'FUNCTION_AND_IMPORTS_FULL.py.txt'
        review.write_text(full_review_source(revised),encoding='utf-8')
        (folder/'FILE_FULL.py.txt').write_text(revised,encoding='utf-8')
        emit('FULL_CODE',review)
        if args.dry_run:
            report['gate']='PASS_R11_READ_ONLY_DRYRUN'
        else:
            if current!=updated:
                (folder/'typed_projection.before').write_bytes(current)
                (ROOT/TARGET).write_bytes(updated)
            report['audit']=inspect_actual(folder)
            command=[sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider','--import-mode=importlib',*TESTS]
            report['focused_command']=command
            subprocess.run(command,cwd=ROOT,check=True)
            check_head,check_current,check_updated,_,shared_after=preflight()
            require(check_head==head and check_current==check_updated==updated and shared_before==shared_after, 'POST_INSTALL_INTEGRITY_FAILED')
            report['gate']='PASS_R11_HOPF_ZERO_REASON_DISPLAY'
    except Exception as exc:
        report.update(error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    emit('REPORT',folder/'report.json')
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__=='__main__':
    raise SystemExit(main())

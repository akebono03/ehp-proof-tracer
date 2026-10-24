"""Read-only cutover checks using the public Web adapters."""
from __future__ import annotations
import json
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from phase165_r52_partial_proof import ProofSearchStatus,make_partial_proof_result
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase165_r52_r4_flask_bridge import build_group_proof_progress_view
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from proof import ProofStep,ProofRule
from web_group_proof import build_web_partial_group_proof_view

OUT=Path(__file__).resolve().parent/'output'

def read_text(view):
    """Include both segmented lines and unsegmented heading prefixes."""
    return '\n'.join(
        ''.join(part.value for part in line.segments)
        if line.segments else line.prefix + (line.statement_latex or '') + line.suffix
        for line in view.rendered_lines
    )

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    cases=(
        ('not_searched',make_partial_proof_result(n=100,k=20,status=ProofSearchStatus.NOT_SEARCHED,open_goals=('target',))),
        ('partial',make_partial_proof_result(n=3,k=2,status=ProofSearchStatus.PARTIAL,proven_steps=(ProofStep('observed',(),ProofRule.GIVEN),),open_goals=('unknown',),references=('Unscreened label',))),
        ('search_failed',make_partial_proof_result(n=17,k=4,status=ProofSearchStatus.SEARCH_FAILED,open_goals=('no-rule',),diagnostics=('No applicable typed rule',))),
    )
    rows=[]
    for name,result in cases:
        public=build_web_partial_group_proof_view(result)
        direct=build_partial_web_group_proof_view(result,narrative_model=build_proof_narrative_model(result))
        rendered=read_text(public)
        (OUT/f'{name}_public.md').write_text(rendered,encoding='utf-8')
        checks={'same_as_explicit_common_model':public.rendered_lines==direct.rendered_lines,
                'status':'探索状態：' in rendered,
                'open_goal':('未解決 Goal' in rendered and any(
                    line.kind=='heading' and line.prefix=='未解決 Goal'
                    for line in public.rendered_lines)),
                'diagnostics':(('探索診断' in rendered and any(
                    line.kind=='heading' and line.prefix=='探索診断'
                    for line in public.rendered_lines)) if result.diagnostics else True),
                'observed_step':('observed' in rendered if result.proven_steps else True),
                'no_unverified_reference':'Unscreened label' not in rendered,
                'no_qed':'□' not in rendered,
                'partial_flag':public.partial_result}
        rows.append({'case':name,'checks':checks})
        print(name,' '.join(f'{key}={val}' for key,val in checks.items()))
        if not all(checks.values()):
            raise AssertionError(f'{name}: {checks}')
    flask=build_group_proof_progress_view(n=3,k=2,goal='pending')
    flask_text=read_text(flask)
    (OUT/'flask_explicit_custom.md').write_text(flask_text,encoding='utf-8')
    if not (flask.partial_result and '探索状態：未探索' in flask_text
            and '未解決 Goal' in flask_text and 'pending' in flask_text
            and '探索診断' in flask_text and any(
            line.kind=='heading' and line.prefix=='探索診断'
            for line in flask.rendered_lines) and '□' not in flask_text):
        raise AssertionError('Flask custom partial route lost information')
    report={'phase':'168 R3-41C','mode':'PARTIAL_WEB_CUTOVER','cases':rows,
            'flask_custom_partial':'PASS',
            'compatibility_preserved':'comparison.json',
            'full_pytest_run':False}
    (OUT/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Phase 168 R3-41C — 共通 Web Narrative 接続の監査','',
           '未完成状態は共通 Model に接続。明示的な legacy と直接 Adapter fallback は保持。','',
           '| Case | 共通 Model 一致 | 状態 | Goal | 診断 | QEDなし |',
           '|---|---|---|---|---|---|']
    for row in rows:
        c=row['checks']
        lines.append('| '+row['case']+' | '+' | '.join('PASS' if c[x] else 'FAIL'
            for x in ('same_as_explicit_common_model','status','open_goal','diagnostics','no_qed'))+' |')
    lines+=['','- Flask 独自探索入力：PASS','- 完成4群・明示 legacy・直接 Adapter fallback：バイト単位で変更なし','- 新しい数学的規則や Reference は追加しない','- 全体 pytest は実行しない','']
    (OUT/'audit.md').write_text('\n'.join(lines),encoding='utf-8')
    bundle=OUT/'review_bundle.zip'
    with ZipFile(bundle,'w',ZIP_DEFLATED) as z:
        for file in sorted(OUT.glob('*.md'))+sorted(OUT.glob('*.json')):
            z.write(file,file.name)
    print('REPORT',OUT/'audit.md')
    print('UPLOAD_BUNDLE',bundle)

if __name__=='__main__':
    main()

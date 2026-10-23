"""Full-text historical baseline audit: no source-code modifications."""
from __future__ import annotations
import difflib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CASES={'pi_3^2':('pi3_2_original.txt','pi_3^2_current.txt'), 'pi_4^3':('pi4_3_original.txt','pi_4^3_current.txt'), 'pi_5^4':('pi5_4_original.txt','pi_5^4_current.txt')}
FINDINGS={
'pi_3^2':[
('REFERENCE_BODY_MISSING','(5.1) の二つの一般公式が使用する結果にない'),
('REFERENCE_BODY_MISSING','Proposition 5.1 の H(η₂)=ι₃ が使用する結果にない'),
('REFERENCE_NUMBERING_CHANGED','Proposition 5.1 は基準 [R2]、現行 [R4]。番号変更だけは誤りとみなさない'),
('REFERENCE_EXTRA','Proposition 4.2 (4.4) と suspension identity が現行欄に追加された。証明上必要かを別途点検'),
('PROOF_EXPLANATION_MISSING','Δ の零写像性について ImΔ=ker E=0 の計算が省略'),
('PROOF_EXPLANATION_MISSING','H の同型性に至る「単射性と全射性より」という説明が省略'),
('PROOF_SOURCE_LINK_MISSING','完全列、H の単射・全射・同型の根拠を本文の対応位置で明示する記述が基準より弱い'),
],
'pi_4^3':[
('REFERENCE_BODY_MISSING','(5.1) の零群公式・対角群の一般公式が使用する結果にない'),
('REFERENCE_BODY_MISSING','Proposition 5.1 の π₃² の群構造と Δ(ι₅)=±2η₂ が使用する結果にない'),
('REFERENCE_EXTRA','eta-family notation / Proposition 4.2 の見出しが追加された。必要性と対応を点検'),
('PROOF_EXPLANATION_DIFF','ImΔ=ker E を別段落で表示しており基準と表現が異なる（欠落ではない）'),
('PROOF_SOURCE_LINK_MISSING','E の全射性など、完全性からの推論が簡略化されている'),
],
'pi_5^4':[
('REFERENCE_BODY_MISSING','Toda (4.5) の一般的同型輸送公式が使用する結果にない'),
('REFERENCE_BODY_MISSING','Proposition 5.1 の π₄³ の群構造が使用する結果にない'),
('REFERENCE_EXTRA','eta-family notation の見出しが現行欄に追加された'),
('PROOF_MISSING','(n,m,k)=(3,4,1) への Toda (4.5) の特殊化が表示されない'),
('PROOF_MISSING','E:π₄³→π₅⁴ が同型であることが表示されない'),
('PROOF_SOURCE_LINK_MISSING','(4.5) が一覧にはあるが証明本文に [R3] が現れない'),
('PROOF_ORDER_DIFF','生成元の像 E(η₃)=η₄ が出典・同型の説明より前に表示される'),
('PROOF_EXTRA','π₅⁴=Z/2{Eη₃} の中間式が現行に追加された（それ自体は誤りとは判定しない）'),
]}

def sections(text):
    text=re.sub(r'(?m)^\d{3} ', '', text)
    i=text.find('使用する結果'); j=text.find('証明',i+len('使用する結果'))
    assert i>=0 and j>i, 'Reference / proof section markers absent'
    return text[i+len('使用する結果'):j], text[j+len('証明'):]

def normalize(text):
    text=re.sub(r'(?m)^\d{3} ', '', text)
    text=re.sub(r'\*\*', '', text)
    text=text.replace('$','').replace('\\left','').replace('\\right','')
    text=re.sub(r'\s+', ' ', text)
    return text.strip()

def generate():
    out=ROOT/'output';out.mkdir(exist_ok=True)
    results={}
    for name,(basefile,currentfile) in CASES.items():
        baseline=(ROOT/'baselines'/basefile).read_text(encoding='utf-8')
        current=(ROOT/'current'/currentfile).read_text(encoding='utf-8')
        b_ref,b_proof=sections(baseline);c_ref,c_proof=sections(current)
        diffs={}
        for label, a, b in [('reference',b_ref,c_ref),('proof',b_proof,c_proof)]:
            diff='\n'.join(difflib.unified_diff(a.splitlines(),b.splitlines(),fromfile=f'BASELINE/{name}/{label}',tofile=f'CURRENT/{name}/{label}',lineterm=''))+'\n'
            (out/f'{name}_{label}.diff').write_text(diff,encoding='utf-8')
            diffs[label]={'identical_normalized':normalize(a)==normalize(b),'diff_file':f'{name}_{label}.diff'}
        results[name]={'comparison':diffs,'findings':[{'category':cat,'description':desc} for cat,desc in FINDINGS[name]],'baseline':basefile,'current':currentfile}
    report={'status':'DIFFERENCES_FOUND','mode':'AUDIT_ONLY','scope':'frozen full text and captured current output, not live execution','results':results,'limitations':['Findings are qualitative comparisons of supplied source snapshots, not a proof of literature correctness.','Current output is the supplied R3-33 capture. Re-run capture separately if repository source has changed.','Reference numbering is not required to equal the frozen baseline.','This audit does not run full pytest or patch source files.']}
    (out/'fulltext_reaudit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Phase 168 R3-34 — 固定基準全文の再監査','', '**判定：差異あり。R3-33 の「一致」を全文一致と解釈するのは誤り。**','','比較対象は同梱した固定基準と R3-33 の実出力。', '']
    for name,r in results.items():
        lines.extend([f'## {name}', ''])
        for f in r['findings']:
            lines.append(f'- **{f["category"]}**: {f["description"]}')
        lines.extend(['',f'- Reference 全文差分: `{r["comparison"]["reference"]["diff_file"]}`',f'- 証明全文差分: `{r["comparison"]["proof"]["diff_file"]}`',''])
    lines.extend(['## 判定上の注意','',*['- '+x for x in report['limitations']]])
    (out/'fulltext_reaudit.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('\n'.join(lines))
    print('REPORT:',out/'fulltext_reaudit.json')
    return report

if __name__=='__main__': generate()

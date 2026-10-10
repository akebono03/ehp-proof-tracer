"""Phase 163 R4-R22: narrow, verified corrections to the R4-R21 TeX."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

BASE_NAME = 'Toda_01_corrected.tex'
OLD_DX = r'd_X = \phi_{X,S^n}\circ (1_X\times \psi_1).'
NEW_DX = r'd_X = \phi_{X,S^1}\circ (1_X\times \psi_1).'
OLD_17 = r'''\begin{equation}
% (1.7)
  f:Y\to Z,\ g:W\to X \text{ に対して, 次は準同型である.}
\end{equation}
\[
f_*:[EX, Y] \to [EX,Z],\quad Eg^*:[EX,Y]\to[EW,Y].
\]'''
NEW_17 = r'''写像 $f:Y\to Z$ と $g:W\to X$ に対して, 次は準同型である.
\begin{equation}
\label{eq:toda-1-7}
f_*:[EX,Y]\longrightarrow[EX,Z],\qquad
(Eg)^*:[EX,Y]\longrightarrow[EW,Y].
\end{equation}'''


def align(text: str) -> str:
    """Replace only exact, unique source spans confirmed from original page 7."""
    changes = ((OLD_DX, NEW_DX), (OLD_17, NEW_17))
    for old, new in changes:
        if text.count(old) != 1:
            raise ValueError('Expected unique correction span missing; no output written')
        text = text.replace(old, new, 1)
    return text


def build_report(source: Path, output: Path) -> dict:
    """Keep source intact and emit corrected copy plus review ledger."""
    original = source.read_text(encoding='utf-8-sig')
    if 'S^{m+n}' not in original or r'\shrink_{m,n}:S^m\times S^n\longrightarrow S^{m+n}' not in original:
        raise ValueError('R4-R21 correction not detected; use its output first')
    revised = align(original)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'Toda_01_corrected.tex').write_text(revised, encoding='utf-8')
    (output / 'Toda_01_before_r22.tex').write_text(original, encoding='utf-8')
    rows = [
        ('CONFIRMED_CORRECTION','7','3','suspension d_X','S^n -> S^1 in phi_{X,S^1}; formula contains psi_1'),
        ('CONFIRMED_CORRECTION','7','3','(1.7)','Numbered expression now displays f_* and (Eg)^* maps; not prose-only'),
        ('RETAINED_FROM_R21','6','2','(1.3)','Preserve prior sphere dimension and shrinking map correction'),
        ('REVIEWED_NO_EDIT','7','3','(1.5), (1.6), (1.8)','Compared visually; no further correction asserted'),
        ('UNVERIFIED','5-6','1-2','(1.1), (1.2), (1.4)','Full symbol-by-symbol verification remains pending'),
        ('UNVERIFIED','8-15','4-11','(1.9)-(1.18), Lemma, Propositions','Full page-level verification remains pending'),
    ]
    with (output / 'alignment_review.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.writer(stream)
        writer.writerow(['status','printed_page','pdf_page','item','finding'])
        writer.writerows(rows)
    result={
        'phase':'163 R4-R22',
        'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'confirmed_corrections':2,
        'carried_forward_r21_corrections':1,
        'chapter_fully_verified':False,
        'statement_ids_changed':0,
        'production_code_changed':False,
        'full_suite_run':False,
    }
    (output/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (output/'report.md').write_text('''# Phase 163 R4-R22 原典照合記録

## 根拠

Toda 原本 PDF の印刷7頁（PDF 3頁目）を画像で確認した。対象は R4-R21 出力の修正版 TeX である。既存原稿は上書きしない。

## 確認した修正

- Suspension（懸垂）を表す $d_X$ の定義で、TeX の $\\phi_{X,S^n}$ を原本に従い $\\phi_{X,S^1}$ に修正した。
- (1.7) の番号付き箇所が説明文だけになっていたため、原本で示される $f_*$ と $(Eg)^*$ の二つの準同型写像を番号付き式に移した。
- R4-R21 の (1.3) の修正は維持した。

## 限界

これは第1章全11ページの完全な逐字照合ではない。(1.5)、(1.6)、(1.8) はページ内で比較したが全記号の一致を保証しない。その他の式・命題・定義は未照合として記録した。Statement ID、Registry、証明探索には手を加えていない。全体 pytest は未実行である。
''',encoding='utf-8')
    return result


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(build_report(args.source,args.output),ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()

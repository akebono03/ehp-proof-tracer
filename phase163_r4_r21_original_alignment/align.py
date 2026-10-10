"""Phase 163 R4-R21: conservative source-alignment patch and review manifest."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

SOURCE_SHA256 = '1c2c263803510d959c64188632bffa098e38b11fd8db80189fc67210a97e1f5c'
OLD_BLOCK = r'''二つの球面 $S^m$ と $S^n$ の reduced join は,
\begin{equation}
S^m\ \wedge\ S^n\ \cong\ S^{m+n+1}.
% \tag{1.3}
\end{equation}
対応は, 
$(x,y)\in I^m\times I^n$ に対して,
次で与えられる.
\[
\shrink_{m,n}\bigl(\psi_m(x),\,\psi_n(y)\bigr)=\psi_{m+n+1}(x,y).
\]'''
NEW_BLOCK = r'''二つの球面 $S^m$ と $S^n$ の reduced join は,
$S^m\wedge S^n\cong S^{m+n}$ と同一視する.
この同一視を与える写像を
\begin{equation}
\shrink_{m,n}:S^m\times S^n\longrightarrow S^{m+n}
% Toda 原本の (1.3): 縮約写像を表示する番号付き式
\end{equation}
と書く. $(x,y)\in I^m\times I^n=I^{m+n}$ に対して,
\[
\shrink_{m,n}\bigl(\psi_m(x),\,\psi_n(y)\bigr)=\psi_{m+n}(x,y)
\]
で定める.'''


def align(text: str) -> str:
    if text.count(OLD_BLOCK) != 1:
        raise ValueError('対象箇所が一意に見つからないため変更しません')
    return text.replace(OLD_BLOCK, NEW_BLOCK, 1)


def verify_source(path: Path) -> str:
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != SOURCE_SHA256:
        raise ValueError(f'原稿 SHA-256 不一致: {digest}')
    return data.decode('utf-8-sig').replace('\r\n', '\n')


def run(source: Path, output: Path) -> dict:
    text = verify_source(source)
    revised = align(text)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'Toda_01_corrected.tex').write_text(revised, encoding='utf-8')
    (output / 'Toda_01_before.tex').write_text(text, encoding='utf-8')
    rows = [
        ('CONFIRMED_CORRECTION', '印刷6頁 / PDF 2頁', '(1.3)', 'TeX 210-220行', 'S^m\\wedge S^n の次元、写像の定義、psi の添字を原本に合わせて修正'),
        ('NOT_YET_VERIFIED', '印刷5頁 / PDF 1頁', '(1.1)-(1.2)', 'TeX 冒頭', '式と定義の逐字照合が必要'),
        ('NOT_YET_VERIFIED', '印刷6-7頁 / PDF 2-3頁', '(1.4)-(1.8)', 'TeX 本文', '関係式、記号、次数条件の照合が必要'),
        ('NOT_YET_VERIFIED', '印刷8-9頁 / PDF 4-5頁', '(1.9)-(1.14), Lemma 1.1', 'TeX 本文', '式番号、lemma の式と証明の照合が必要'),
        ('NOT_YET_VERIFIED', '印刷10-15頁 / PDF 6-11頁', 'Proposition 1.2-1.9, (1.15)-(1.18)', 'TeX 本文', '命題・仮定・証明中の式の照合が必要'),
    ]
    with (output/'alignment_review.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['status','pdf_location','locator','tex_location','description']);w.writerows(rows)
    summary={'phase':'163 R4-R21','original_sha256':SOURCE_SHA256,'confirmed_correction_count':1,'unverified_review_groups':4,'chapter_fully_verified':False,'statement_ids_changed':0,'registry_changed':False,'search_connected':False,'full_suite_run':False}
    (output/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    report='''# Phase 163 R4-R21 原典照合記録

## 照合の根拠

- 参考資料: 添付された Toda_01.pdf（印刷5〜15頁、全11頁）。
- 対象: 既存 Toda_01.tex（SHA-256 固定）。
- 印刷6頁、PDF 2頁の (1.3) を画像で確認した。

## 確認・修正済み

(1.3) は $S^m\times S^n\to S^{m+n}$ の縮約写像である。元の TeX にあった $m+n+1$ を $m+n$ とし、番号付き式は同型式でなく写像の定義へ変更した。reduced join の記号は既存 TeX の $\\wedge$ を維持する（原典は # 記号）。

## 未完了

本作業では原本全11頁の数式・本文・命題の逐字照合は完了していない。未確認部分を一致と判定してはならない。原典では用語・記号・文章が相違する可能性があり、続く監査で1件ずつ確認する。原稿に対する追記候補は alignment_review.csv に列記した。

既存24予約 ID、67成分の台帳、証明探索、描画には変更なし。全体 pytest は行わない。
'''
    (output/'report.md').write_text(report,encoding='utf-8')
    return summary


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(run(args.source,args.output),ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()

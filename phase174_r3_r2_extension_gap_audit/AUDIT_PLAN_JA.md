# Phase 174 R3-R2：有限巡回拡大に必要な推論の境界監査

## 対象

既存ファイル・クラス・関数の変更はない。リポジトリ直下に監査専用ディレクトリ
`phase174_r3_r2_extension_gap_audit/` を新設し、`audit.py`、`run.ps1`、
`tests/test_audit.py` を追加する。新しい Python 関数は `audit.py` のみで定義する。
`README.md` は英語、`AUDIT_PLAN_JA.md` は日本語とする。

## 現在の停止点

既存の有限巡回群構造から群の等式を導出する規則は
`CyclicStructureStatement(G,x,m)` を前提とする。
R3-R1 の実測ではこれに関する2つの Subgoal に逆向き推論候補がない。

既存の `infinite_cyclic_quotient_structure_inference_rule` は
無限巡回群からの商を仮定するので、そのまま $\pi_6^3\cong\mathbb Z/4$ の
有限部分群を扱うことはできない。

## 数学的な証明義務

Toda (4.8) は $\Delta(\iota_7)=0$ を満たす場合に限り、

$$
E^2:\pi_6^3\hookrightarrow\pi_8^5,
\qquad \pi_8^5/E^2\pi_6^3\cong\mathbb Z/2
$$

を与える。Toda (5.5) は

$$
2\nu_5=E^2\nu'
$$

を述べる。ここに既証明 $\pi_6^3\cong\mathbb Z/4\{\nu'\}$ と
上記の型付き証明がすべて接続されれば、指数2の部分群の元 $E^2\nu'$
は位数4であり、$\nu_5$ は位数8の生成元となる。

ただしこの監査は上述の数学的事実を ProofStep として生成しない。
出典の表記そのものを証明に格上げしない。

## 完了条件

R3-R1 原記録の HEAD・３候補・引用27件・有限巡回構造2件の未解決を再確認。
既存の一般規則の前提を型付きで監査し、元の `GIVEN` と証明結果を維持。
限定 pytest のみ実行し、Git 作業ツリーと Index を維持する。

## 次の実装との境界

R3-R3 に移る前に、$\Delta(\iota_7)=0$ 及び (4.8) の条件付き導出が
実際の型付き ProofStep で証明できるかを確認する。
有限群の拡大について、前提不足のまま結論を直接返す規則は禁止する。
`n,k`・生成元名別 Narrative 分岐を新設しない。

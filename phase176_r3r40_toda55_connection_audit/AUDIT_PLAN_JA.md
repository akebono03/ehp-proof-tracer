# Phase 176 R3R40 — 4倍関係への接続監査

## 対象と境界

既存ファイル・クラス・関数の変更なし。ルート直下の新規ディレクトリに
`source.py` の `quadruple_hopf_backward_plan()` と
`build_audit_connection_provider()`（内部 `expand()`）、`audit.py` の
`source_guard()`、`probe()`（内部 `visit()`）、`main()`、限定テストと
PowerShell を追加する。新規数学規則、新規 GIVEN は0件。

## 数学的構成

現行 `canonical_quadruple_goal()` の右辺は右結合であり、R3R39 と型付き
オブジェクトが一致することを確認する。合成結合律は不要。

$$4\nu_5=\eta_5\circ(\eta_6\circ\eta_7),\qquad
H(\nu'\circ(\eta_6\circ\eta_7))=\eta_5\circ(\eta_6\circ\eta_7).$$

既存の対称律と推移律から次を導く。

$$H(\nu'\circ(\eta_6\circ\eta_7))=4\nu_5.$$

2つの独立した Goal を共有探索に委ね、監査時だけ extra_providers で
2段階の既存規則を供給する。Source-first の選別済み GIVEN 以外は採用せず、
R3R39 の6段と Toda (5.5) の3前提が最終証明木に残ることを確認する。
登録済み群の生成元と監査式の構文が一致するかは別項目で報告する。

## 完了条件

DryRun・共有 DFS による監査式の証明・限定 pytest が PASS。既存コードは
変更しない。公開既定 Provider への接続、登録済み生成元の表記差の解消、
根の群構造の証明は次工程以降。全体 pytest は Phase 終了時のみ。

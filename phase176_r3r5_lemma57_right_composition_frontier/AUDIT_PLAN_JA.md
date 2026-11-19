# Phase 176 R3R5 — Lemma 5.7 右合成と懸垂零像の型付き監査

## 前段の確定事実

R3R4 実行では、$(n,k)=(3,5)$ は未完成、Open Goals 3件、独立した零像推論候補1件、共有零像候補0件。`LEMMA57_DIRECT_MATCH=false` だった。ただし R3R4 で直接比較したのは $E(\eta_2\nu'\eta_6)=0$ を要求する生成元と、Lemma 5.7 に明記された $E(\eta_2\nu')=0$ である。右因子の有無が異なるため、直接一致しないことだけでは本文との矛盾を意味しない。

## 出典と既存実装

- `sources/toda/Toda_05_2.tex`: Lemma 5.7 の明示零関係。
- `phase175_r3r9_lemma57_explicit_public/rule.py`: 引用された明示零関係を `GeneratorImage` へ取り出す既存規則。
- `relation_rules.py`: 右合成の等式保存、懸垂と合成の両立、零合成の等式に関する既存の汎用規則。
- `phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py`: 有限巡回群の生成元が零に写ると全像が零になる一般規則。
- `phase174_r3_r7_r5_zero_image_hopf_injective/rule.py`: EHP 完全性と零像から Hopf 単射性を導く一般規則。
- `phase165_r52_r9_shared_math.py`: 公開共有 Provider の登録状況。

## 監査目標

1. 登録済みの先行 $\pi_7^2$ の生成元を型付き合成因子に分解する（先行 DB 値は証明でなく候補）。
2. Lemma 5.7 の対象 $\eta_2\nu'$ と、右合成後 $\eta_2\nu'\eta_6$ を分けて確認する。
3. 既存の出典付き Lemma 5.7 導出規則が基礎零関係に適用できるか調べる。
4. 共有 Bridge 内の引用済み Lemma 5.7 明示ソースと、基礎零関係・合成零像・写像全体零像の各推論候補を記録する。
5. 現在の Proof Search の Open Goals と比較する。規則候補を証明済み ProofStep として扱わない。

## 完了条件

DryRun PASS、限定 pytest PASS、実環境の型付き結果を JSON に記録する。結果が `PASS` でも群の証明が完成したことを意味しない。既存本体コード・GIVEN・推論規則・5文書は変更せず、全体 pytest は実施しない。Phase 174 の Source Guard 既知4件も触らない。

## 次段階との境界

R3R5 の観測後、必要なら R3R6 で既存の出典付き零関係、一般右合成、既存有限巡回零像規則の共有検索への接続だけを最小限追加する。未知の出典の追加や目標の直接 GIVEN は行わない。

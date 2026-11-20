# Phase 176 R3R7 — Lemma 5.7 の独立出典選別と基礎零像 ProofStep 監査

## R3R6 からの引き継ぎ

標準 Bridge の Lemma 5.7 出典数は0件だった。Phase 175 で検証した出典を独立 Bridge に統合すると1件となり、基礎推論候補が1件得られた。先行 DB Prior は承認・再検証できた。対象の引用 ID は取得できなかった。

## 数学的な対象

Toda Lemma 5.7 の明示項 $E(\eta_2\circ\nu')=0$ を、出典付き `GIVEN` から既存 `expand_cited_lemma57_explicit_zero` により型付き `GeneratorImage` として導出する。新しい `GIVEN` や数学規則は作らない。

今後必要な $E(\eta_2\circ\nu'\circ\eta_6)=0$、懸垂写像全体の零像、$H$ の単射、$\ker\Delta$ の構造、$\pi_8^3$ の生成元はこの監査では証明しない。

## 実行内容

1. 現行 develop と R3R6 の実行 HEAD からの祖先関係、追跡ファイルの清浄性を確認する。
2. Toda 原文、既存の出典・推論のコードアンカーを照合する。
3. 既存公開 Proof Search を無変更で実行し、Open Goals を記録する。
4. 既存の検証済み Lemma 5.7 出典を**メモリ上のみ**に統合する。
5. `screen_independent_sources_for_derived_goal` により、目標の引用 ID を捏造せず、独立した文献位置付き出典をちょうど1件選別する。
6. 既存の正規の推論 matcher と factory で `GIVEN` を前提に持つ `INFERENCE` の ProofStep を孤立環境で導出し、出典と前提を検証する。
7. 先行群の DB Prior を再検証し、通常共有 Provider で基礎零関係が候補として出るか記録する。

## 変更対象・境界

追加するのは `phase176_r3r7_lemma57_derived_source_proof/` のみ。共有 Provider、出典台帳、既存 API、Web Renderer は修正しない。新規 GIVEN 0件、新規数学規則0件。全体 pytest は Phase 終了時だけ実施する。Source Guard 既知4失敗は未解決。

本監査が PASS しても、対象の群の完成証明ではない。次工程では出典選別の方法を踏襲し、共有検索への一般的な接続と合成零関係の推論を検討する。

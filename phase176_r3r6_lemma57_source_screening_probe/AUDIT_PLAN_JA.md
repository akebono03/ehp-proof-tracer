# Phase 176 R3R6 — Lemma 5.7 Source Screening Frontier

## 現状

R3R5 のユーザー実行では DryRun と監査が PASS、限定 pytest 6 passed。`(n,k)=(3,5)` の探索は `search_failed`、Open Goals 3件、先行群の生成元は3因子。Lemma 5.7 に対応する最初の2因子の照合は成功した。一方、標準共有 Bridge には明示 Lemma 5.7 型付き source がなく、基礎・合成・全体零像の各共有候補が0件だった。

## 数学的な目標

$$E(\eta_2\nu')=0$$

が Lemma 5.7 に明記されている。先行結果 $\pi_7^2=\mathbb Z/2\{\eta_2\nu'\eta_6\}$ と懸垂の合成保存から

$$E(\eta_2\nu'\eta_6)=0$$

を導き、$E:\pi_7^2\to\pi_8^3$ の零像と EHP 完全性から $H$ 単射を目指す。証明対象の群構造を直接 GIVEN としない。

## 読み取り専用実験

1. 現行 Git `develop`、R3R5 の祖先 HEAD、既存コードと出典アンカーを確認する。
2. `build_shared_typed_bridge` のデフォルトで Lemma 5.7 の source leaf が何件存在するか観測する。
3. Phase 175 既存 `build_explicit_lemma57_source` を**一時的なメモリ上の registry** に追加し、以前の `merge_isolated_cited_source` を利用する。既存ファイルやプロダクション registry は変更しない。
4. 登録済み `(n,k)=(3,5)` 目標の引用 ID を取得できる場合は、`screen_shared_proof_context` により Lemma 5.7 の使用可否を照合する。
5. 先行 DB 結果 `(n,k)=(2,5)` は `admitted_db_step` と `verified_db_step` で検証する。独立文献であるとは主張しない。
6. 明示 Lemma 5.7 の導出候補が一時的な Bridge 上で出現するかを報告する。候補は証明ではない。

## 非対象

数学規則・GIVEN の追加、root の直接証明登録、既存 Provider の変更、Phase 174 の Source Guard 既知4失敗の修正、全体 pytest。

## 完了条件と境界

DryRun PASS、限定 pytest PASS、実ユーザー checkout での R3R6 監査 PASS。出典の時間順判定や既存 Provider の接続が不足する場合は、次 R3R7 で対象を絞る。全体 pytest は Phase 176 完了時のみ。

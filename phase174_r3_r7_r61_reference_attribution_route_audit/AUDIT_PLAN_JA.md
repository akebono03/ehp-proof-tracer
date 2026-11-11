# Phase 174 R61 — Reference 出典選択経路の個別監査

## 監査前の確認

GitHub `akebono03/ehp-proof-tracer` の `develop` について、R60/R60R1 実行ログと現行 Git Blob を確認した。R60 は Reference の相互所有関係を両群で PASS としたが、共通 Renderer に3つの出典選択経路が残る。

## 変更対象

既存ファイル・既存 import・クラス・関数は一切変更しない。

新規ディレクトリ `phase174_r3_r7_r61_reference_attribution_route_audit/` のみ。

- `audit.py`：6ファイル Source Guard、AST による3経路・利用箇所の確認、Verified Proof Tree からの GIVEN 祖先引用の候補監査、2群の公開証明の不変条件チェック。
- `tests/test_audit.py`：8つの限定テスト関数。
- `run.ps1`：DryRun、実監査、限定 pytest。pytest cacheprovider 無効。
- `README.md`、本計画、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md`。

## 監査対象の共通 Renderer 内の処理

1. `cited_general_ancestor_numbers`：命題型を指定して一般文献 GIVEN 祖先を探索する。
2. `direct_given_premise_citation_numbers`：単一 GIVEN 前提を持つ指定型の推論に引用を与える。
3. `single_source_ancestor_numbers`：検証済み GIVEN 祖先から参照番号が1種類に定まる場合のみ使う。

この3処理は既存の `ProofNarrativeModel.step_citation_numbers` を参照している。各呼び出しの所在と、祖先候補の多重性を監査しても、それだけで文章ごとの引用の十分性が証明されたとはみなさない。

## Source Guard の境界

6ファイルの Git Blob SHA を固定し、コード内容の変化は拒否する。一方、HEAD は監査記録として出力するだけとし、R59/R60 のような無関係ファイル追加によるコミット更新では停止しない。

## 完了条件

Source Guard・DryRun・公開済み2群の Reference 7件/3件・R60 相互参照整合性・限定 pytest がすべて PASS。全体 pytest は実行しない。

## 次 Phase との境界

R61 は出典選択の設計監査に限る。出典選択処理の共通関数への移動、本文の変更、推論規則の変更は次の Phase で必要性を改めて検証する。

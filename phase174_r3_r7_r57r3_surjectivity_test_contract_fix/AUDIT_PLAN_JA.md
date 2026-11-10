# Phase 174 R57R3：全射性テスト契約修正の監査計画

## 発生した問題

R57R2 の実行では `phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py::test_missing_or_wrong_group_generator_blocks_surjectivity` の最終 assertion が失敗した。

R57 は全射性の規則を `A=Z{Delta(iota)}` の1前提に変更した。`find_inference_matches_for_rule()` は与えられた ProofStep の集合から推論規則に適合する部分集合を選択するため、利用可能な他の命題が混在していても、必要な1前提がある場合には成功する。旧テストはこの正常な動作を誤って拒否していた。

## 変更する対象と境界

1. `phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py` の `test_missing_or_wrong_group_generator_blocks_surjectivity()` 全体：不正な生成元と前提欠落の拒否を維持し、無関係な命題が追加された場合も1前提だけで導出することを検証する。
2. `phase174_r3_r7_r57_narrative_source_cleanup/install.py` の `NEW_TEST3` 定義と `AFTER_SHA256` にあるテストの SHA-256：修正したテストと、元の R56 テストからの再生成結果を完全一致させる。

新しい数学的規則・GIVEN・Source・Renderer・一般探索処理は追加も変更もしない。既存の上位5文書は変更しないため全文再出力対象にはならない。

## 監査と完了条件

- develop ブランチ・監査済み祖先・staged 変更なし・R57 自体の Source Guard を確認。
- 修正前の2ファイル SHA-256 が一致する場合だけ置換し、修正後も冪等に実行する。
- 修正後 R57 インストーラーの `patch_test()` が、監査済み R56 原本から同じテスト全文を再生する。
- R57R3 限定 pytest PASS。
- R57 の限定 pytest、`pi_11^6` と `pi_12^7` の実証明・出典・Narrative の公開監査 PASS。
- 全体 pytest は Phase 終了時まで実施しない。

## 次の作業との境界

(5.10) の符号付き内部命題の型の再設計、引用表示系の完全統一、証明木のさらなる最適化は R57R3 の対象外とする。

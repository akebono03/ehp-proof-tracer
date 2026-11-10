# R57R2 監査計画

## 事前確認

- GitHub `develop` の R56 実装と関連するテスト `test_rule.py` を照合する。
- R57 の旧 `install.py` の `NEW_TEST1` と `AFTER_SHA256` を照合する。
- HEAD は R56 のレビュー済み基点の子孫、ブランチは `develop`、ステージ済み変更がないことを確認する。
- R57 の既存 Source Guard をそのまま呼び出し、3つの既存表示ファイルと R56 規則コードの照合を保持する。

## 変更対象

1. `phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py` の `test_generator_relation_alone_proves_delta_surjectivity()`：重複した `@pytest.mark.parametrize` のみを削除する。関数本体は不変。
2. `phase174_r3_r7_r57_narrative_source_cleanup/install.py`：`NEW_TEST1` の二重デコレーター生成を解消し、`AFTER_SHA256` の検査値を訂正する。

## 検証

- R57R2 固有限定 pytest 7件。
- R57 の既存限定 pytest 群と、$\pi_{11}^{6}$ / $\pi_{12}^{7}$ 公開証明監査を再実行。
- R57 の完了 Gate と R57R2 の完了 Gate が両方出るまで未完了とする。
- 全体 pytest は Phase 最終段階まで実行しない。

## 次 Phase との境界

この段階では (5.10) の内部命題型や引用統一のさらなる変更は行わない。一般数学規則は追加・変更しない。

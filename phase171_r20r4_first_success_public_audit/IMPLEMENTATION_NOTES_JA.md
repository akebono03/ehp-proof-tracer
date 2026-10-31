# Phase 171 R20R4R2 — HEAD 更新後の監査実行ガード

## 原因

R20R4R1 の `preflight()` は HEAD を `9fca3a6e` / `8eca4f20` に限定していたため、現在の `788261264e63d202b9e9bfe819212f12e0d0134e` を拒否した。これは証明の失敗ではない。

GitHub の指定コミット `78826126` の内容確認により、`phase165_r3_recursive_search.py` に R20R2 の First Successful Proof Search が含まれることを確認した。

## 変更

- 既存本番コード：変更なし
- `phase171_r20r4_first_success_public_audit/audit.py`：定数 `EXPECTED_HEADS` を削除、`REVIEWED_SOURCE_BLOBS` を追加し、`preflight()` 全体を置換
- `run.ps1`：R20R4R1 版をそのまま同梱（`python -m` 実行）
- 旧監査の `proof_ancestry()`・`audit_obligation()`・`audit_public_goal()`・`run_audit()`・`main()` は変更なし

## 安全性

- `git hash-object --path` で GitHub 上で確認した探索器と共通 provider の blob SHA を照合する。HEAD 番号による判定には依存しない。
- `--path` は checkout の改行コード等に対して Git の clean filter を適用するために使う。
- ファイルがレビュー済みの内容と異なれば作業ツリーを変更せず停止する。
- `GIVEN` の追加・既存証明木の注入・引用資格の緩和は行わない。
- 探索の `complete` は Web の表示確認と区別する。

## 期待する出力

`PHASE171_R20R4_RESULT=PASS_DRY_RUN` を確認後、`-RightOnly`、通常監査を実行する。監査が成功しても数学的な結果が `PROVED` とは限らない。`audit.json` の各 stage を評価する。

## pytest

`run.ps1` は既存の次の2件だけを実行する。全体 pytest は Phase 終了時のみ。

- `phase171_r2j_r4_r9_r7_public_cyclic_root/tests/test_audit.py::test_generic_source_anchored_root_is_a_premise_proposal_only`
- `phase171_r2j_r4_r9_r8_public_cardinality/tests/test_audit.py::test_end_groups_yield_only_one_typed_backward_obligation`

## 次工程との境界

本ステップは監査の起動を復旧することに限定する。π₆⁵、π₆³ の証明完成・Web 表示変更は扱わない。

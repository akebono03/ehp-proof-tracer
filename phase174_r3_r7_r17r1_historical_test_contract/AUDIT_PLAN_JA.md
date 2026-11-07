# Phase 174 R3-R7-R17R1 監査計画

## 事実確認

- GitHub `develop` HEAD：`388f63797a6aba61418bb93e734b8ce5999dc7f6`。R16 の表示前実装は取り込み済み。
- R17 のユーザー実行は **DryRun 中**に停止しており、本番の `web_group_proof_common.py` 修正はまだ適用されていない。
- 失敗した既存テスト `phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py` は、`(n,k)=(5,3)` を未完成・未解決 Goal 3 件と仮定している。
- Phase 174 により `$\pi_8^5=\mathbb Z/8\{\nu_5\}$` は完成証明に変化した。よって過去の期待値を修正する必要がある。

## 変更対象

1. **既存テストファイル** `phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py`
   - `test_real_typed_pending_goals_are_grouped_only_in_public_display`: 完成済みの `(5,3,3)` を未完成のパラメータ集合から除外する。`(4,8,3)` と `(4,9,2)` の厳格な検証は保持。
   - **新規** `test_pi8_5_completed_case_is_not_reported_as_an_open_goal`: 上記既存関数の直後に追加。完成、未解決 Goal なし、共通 Narrative、公開 Web の complete を検査する。
   - import ブロックは変更しない。
2. **R17 の既存・未実行修正** `web_group_proof_common.py`
   - R17 の既存 `patch.py` を**無変更で再利用**。同じ `_group_proof_statement_latex` 関数を Source Guard 後に置換。R17R1 では新たな数式表示機能を追加しない。
3. **新規パッケージ** `phase174_r3_r7_r17r1_historical_test_contract/`: `patch.py`、`audit.py`、`rollback.py`、`run.ps1`、テスト、ドキュメント。

## 実行順序と根拠

1. Git HEAD・Git blob・R17 配布物の SHA256・git diff を検査する。
2. 変更を行わず R17 の Source Guard / Patch DryRun と限定テストを実行。
3. 通常実行時のみ、先に R17 の元の `web_group_proof_common.py` パッチを適用し、公開統合テストと厳格な R17 監査を完了。
4. その後、Phase 173 の古いテストを更新し、**修正後のテストファイル全体**を実行。
5. 最終監査では、2つの変更対象ファイル以外が変更されていないことと、R17 の未完成証明契約を確認する。
6. 途中失敗した場合は、今回適用した正確な内容に限ってバックアップから復元する。

## 完了条件と次の段階

- R17 の公開数式表示 Gate と R17R1 の既存テスト訂正 Gate が両方 PASS。
- 新規 GIVEN は0件、新しい数学的推論規則は0件、全体 pytest 未実施。
- `$\Delta:\pi_{13}^{13}\to\pi_{11}^{6}$` の全射性は依然未解決。
- 次の R18 以降で初めて、`$E\pi_{10}^{5}=0$` などの独立した数学的証明連鎖を監査する。

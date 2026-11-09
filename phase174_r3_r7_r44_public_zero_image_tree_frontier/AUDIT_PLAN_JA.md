# Phase 174 R3-R7-R44 監査計画

## 目的

R43 の公開接続後、同じ `n=7, k=5` Web 画面に現れる `Eπ_{10}^{5}=0` と `π_{10}^{5}=0` を混同せずに扱い、R41 → R38 → R7 → R9 → Phase169 → Toda (5.9) の限定 Proof Search 経路を監査する。

## 変更範囲

変更する本番モジュール、クラス、メソッド、関数：**なし**。

追加位置：リポジトリ直下の `phase174_r3_r7_r44_public_zero_image_tree_frontier/`。
新規関数：`source_guard.git`, `normalize`, `git_blob`, `matches_blob`, `verify_checkout`; `audit.inspected_frontier`, `audit.main`。新規テスト関数は `tests/` を参照。

## 契約

- GitHub `develop` の R43 統合履歴と参照対象の SHA を Source Guard で照合する。
- `GIVEN` の信頼境界は既存 `admitted_db_step` と `verified_db_step` に委ねる。
- `π_{10}^{5}=0` は R41 の直接の証明前提でないことを型付き Goal で確かめる。
- 実際の限定再帰探索から採用済み ProofStep・未解決 Goal を記録し、手作業の隔離証明を通常探索の証明に置き換えない。
- `Source-first`、`First Successful Proof Search` を維持し、唯一性検査・専用 Narrative・新規 GIVEN は追加しない。
- `pytest` は R44 の限定群および直接関連の R41/R43 テストだけ実行する。

## 完了条件

Source Guard、型の混同防止、限定探索の監査と限定 pytest が PASS。最終証明の完成や HTTP の動作確認は完了条件に含めない。

## 次工程との境界

R45 以降で、R44 が検出した未接続の一般推論経路のみを接続する。原因不明のまま `π_{10}^{5}=0` を GIVEN に登録しない。

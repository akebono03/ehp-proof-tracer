# Phase 175 R3R12R3 — テスト実施状況

## ユーザー実行済みの R3R12R2

- DryRun：`PASS_R3R12R2_READ_ONLY_DRYRUN`。
- 本実行：**47 passed, 2 failed**。
- 失敗テストは公開 $\pi_7^3$ の重複表示と、内部表記の違いを許容する回帰テスト。
- `ROLLBACK=RESTORED`：対象既存関数の復元済み。

## R3R12R3 の作成環境

- GitHub `develop` のコード（R3R11R4・共通 typed Renderer・関連テスト）を確認。
- `typed_sentence()` の出力が `H: ` の空白を含むことを確認。
- インストーラー限定 pytest：**6 passed**。模擬 Proof Tree（実際の単射性の文面を再現）：**PASS**。構文：PASS。ZIP 整合性：PASS。
- 公開検索を用いる統合テストは作成環境では未実施。合格は Windows 本実行でのみ判定。

## 完了条件

- 限定 pytest：R3R12・R3R11R4・R3R10・R3R9・Phase 172・171・R70 機能。
- $\pi_7^3$：Trust `True`、Reference 7件、Lemma 5.4 非依存、Hopf の全射・同型表示、結論1件。
- $\pi_6^3$：Phase 172 の既存表示を維持。
- 期待 Gate：`PASS_R3R12R3_VERIFIED_HOPF_ISOMORPHISM_SINGLE_CONCLUSION`。

**全体 pytest は Phase 175 最終段階まで実行しない。**

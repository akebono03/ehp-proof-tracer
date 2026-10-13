# Phase 165 統合仕上げ (R38)

## 変更対象
- `phase165_r3_recursive_search.py` 全文置換: `RegisteredGoalUnresolved`, `GoalExpansion`, `_typed_reference_steps`, `reconstruct_registered_goal`。既存 API を維持し、`lookup_mode="typed_reference"` を追加。
- `phase165_r14_r38_direct_registry.py` 新規: `build_adopted_typed_reference_registry`, `reconstruct_registered_pi32`, `audit_completion`。
- `test_phase165_r14_r38_direct_registry.py` 新規: 6 件の対象テスト。
- `run.ps1`, `audit.py`, `toda_51_complete.tex`。

## 設計
別途承認 ID を必要としない方式に変更。採用 TeX の命題は厳密に型付きの `AssertionEntry` として登録し、出典付き `ProofStepLink` を保持する。`SOURCE_ARCHIVE` の文字列をそのまま型付き命題へ昇格せず、R36 で構築済みの型付き Reference を使う。引用の原本照合状況は provenance に残す。本文の生成と導出は既存の共通探索器が担当する。

Proposition 5.1 の archive の完全 ID は未解決なので、正確な ID を偽造せず Locator と既存の `ETA_2_HOPF_INVARIANT_FACT` を使う。原本照合済みであるとは主張しない。

## 対象テストと完了条件
R38 の6件、既存のR3およびR2の対象テストを先に実施。成功し、監査で最終命題が型付き Registry から再構築された場合にのみ全体 pytest を実施する。全体テスト成功を Phase 完了条件とする。

## 次の Phase との境界
π₃²以外の群への汎化や、原本照合の完了を先取りしない。過去の gate 機構は互換性確保のため legacy 経路として残すが、新しい証明処理では用いない。

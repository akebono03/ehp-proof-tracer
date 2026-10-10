# Phase 163 R4-R2 — 全登録経路の網羅性監査（途中結果）

## 対象と測定単位
- 直接配置された Python ファイル: 268 件
- 静的候補箇所: 315 件（命題数ではない）
- 監査範囲: リポジトリ直下の稼働コード。テスト・archive・過去 phase フォルダは除外。

## 静的候補の分類
- entry_constructor_site: 93
- registry_or_factory_call_site: 40
- repository_factory_candidate: 25
- statement_or_definition_class: 157

## R4 Bridge

- metadata_only: 67
- unresolved_source: 1

## 未解決の出典

- theorem_fact/0: LiteratureReference.locator is missing; no attribution invented

## 調査上の未達成項目

- A constructor site is not a runtime record and not a unique mathematical statement.
- Statement class definitions are types, not registered theorem instances.
- Dynamically constructed registrations and indirect factories may not be captured.
- Rule catalog statements are not automatically literature-fixed statements.
- Equivalent, duplicate, specialized and generic mathematical assertions remain unclassified.
- Definition provenance, proof completion order and citation permission are not inferred.
- R4 integration is incomplete; no backward search or renderer integration.

## 判定

**全登録命題の網羅性は未確認。今回の件数から数学的な全命題数を算出しない。**
Phase 163 R4-R2 は読み取り専用の監査段階である。全体 pytest は行わない。

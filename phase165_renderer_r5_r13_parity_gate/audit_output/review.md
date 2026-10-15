# Phase 165 R5-R13 旧 Narrative 置換適合性監査

判定: **REVIEW_REQUIRED**

## 前提条件
- web_uses_phase165_adapter: PASS
- cli_uses_partial_renderer: PASS
- main_calls_partial_renderer: PASS
- shared_leaves_exist: PASS
- replay_uses_shared_leaves: PASS
- legacy_reexports_leaves: PASS
- legacy_web_entry_exists: PASS
- legacy_web_calls_old_renderer: PASS
- legacy_r3_entry_exists: PASS
- legacy_path_not_in_public_entry_imports: PASS

## 実行時の表示結果

### legacy: ERROR
- 原因: ValueError: Expected one independently derived source premise of each kind

### canonical: RENDERED
- 文字数: 215
- 見出し: ## 証明対象, ## 使用する結果, ## 証明, ## 未解決 Goal, ## 探索診断

- 比較結果: BLOCKED_RUNTIME_INPUTS_NO_AUTOMATIC_REPLACEMENT

## 境界
- 結果の文字列や見出しの一致は数学的意味の一致を証明しない。
- 旧 Phase 162 の fixture が空の場合は失敗を記録し、旧経路を自動置換しない。
- 既存ソース、テスト、Reference、ProofStep は変更しない。
- 旧 Phase 162 の6件の既知テスト失敗は未解決。
- 全体 pytest は Phase 165 最終段階でのみ実施。

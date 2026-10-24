# Phase 168 R3-41A — 未完成証明の共通 Narrative 移行ギャップ監査

読み取り専用。数学的推論・Web 経路・Renderer・Reference 台帳は変更しない。

## 現行の経路

- 標準 Web の既定 citation_source: `model`
- 標準 Web が共通 Model を構築する: `True`
- Flask の通常問い合わせが標準 Web を使う: `True`
- Flask の独自探索入力が Model 未指定 Adapter を使う: `True`
- Adapter の旧 fallback 呼出: `[74]`
- Adapter の共通 Renderer 呼出: `[77]`
- 共通 Renderer が open_goals を直接参照する: `False`
- 共通 Renderer が diagnostics を直接参照する: `False`

## 既存表示と共通 Model の状態別比較

| 状態 | 旧状態表示 | 共通状態表示 | 旧未解決 Goal | 共通未解決 Goal | 旧診断 | 共通診断 |
|---|---|---|---|---|---|---|
| not_searched | あり | なし | あり | なし | なし | なし |
| partial | あり | なし | あり | なし | なし | なし |
| search_failed | あり | なし | あり | なし | あり | なし |

## 判定

- 既定の完成証明 Narrative は既に共通 Model 経由である。
- 未完成の結果では、旧 fallback が探索状態・未解決 Goal・探索診断を担っている。
- 共通 Renderer へ単純に差し替えると、それらの情報を失う可能性がある。
- 証明探索や出典を補完するのではなく、実際の PartialProofResult を共通の表示モデルへ拡張することが次の実装課題。
- 既存の明示 legacy API と NarrativeOrderEntry.after_indices は今回変更しない。
- 以上は人工の不完全状態3ケースの比較であり、全群の正常性を保証するものではない。
- 全体 pytest は Phase 168 の最後に実行する。

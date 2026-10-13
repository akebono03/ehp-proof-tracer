# Phase 165 R14-R37 — 厳密な完了判定

## 変更対象（新規追加位置：プロジェクト直下）
- `phase165_r14_r37_closure.py`：`registry_leaf_audit`, `strict_search_attempt`, `audit_r37`（各関数全文を同梱）
- `test_phase165_r14_r37_closure.py`：対象テスト6件（各関数全文を同梱）
- `audit.py`, `run.ps1`, `toda_51_complete.tex`：監査実行用
- 既存のクラス、関数、import、Registry、証明規則は変更しません。

## 確認した実装上の境界
- R36 により採用 TeX の 9 前提と目標からの再帰的導出が成功済み。
- `phase165_r5_manifest_bridge.py` は文献を SOURCE_ARCHIVE として保持し、証明資格を付与しません。
- `reconstruct_registered_goal` は Registry の eligible ProofStep のみ葉として採用します。
- Proposition 5.1 の厳密な Source ID は前工程で未確定です。
- 出典認証・意味照合を省略して `verified_assertion_ids` を増やす行為は禁止します。

## 完了条件と次工程との境界
対象テスト6件と実際の strict 探索を実行します。`phase165_closed=true` は厳密な探索成功時のみです。`false` なら Phase165 は継続し、原本・適用範囲・命題出典・型・登録時点の確証を得た後に適格な登録を行う必要があります。完了時のみ全体 pytest を実行します。

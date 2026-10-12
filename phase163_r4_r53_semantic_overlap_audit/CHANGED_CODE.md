# Phase 163 R4-R53 変更一覧

## 新規ファイルと追加位置

- `phase163_r4_r53_semantic_overlap_audit.py`（プロジェクト直下）: `catalog_digest`, `_unit_span`, `_same_text_unit`, `audit`, `write_results`, `main` を新設。import 節・全関数を省略せず収録。
- `tests/test_phase163_r4_r53_semantic_overlap_audit.py`（tests ディレクトリ）: import 節と9件のテスト関数全文を収録。
- `run.ps1`: 入力の存在確認、限定 pytest、結果生成。
- `README.md`: 英語版の実行案内。
- `CHANGED_CODE.md`: この変更記録。

既存クラス・関数・import の変更はない。既存 API とテストには影響しない。

## 完了条件

- 19候補すべてを追跡し、TeX 5ファイルと既存カタログのハッシュを検証する。
- 同一 TeX 掲載単位と数学的に同値な Assertion を混同しない。
- Reference ID および Assertion ID の推定・発行をしない。
- 限定 pytest 9件が成功し、JSON/CSV/Markdown を生成する。

## 次 Phase との境界

R4-R54 で既存 Assertion の型付き数学的内容を明示的に取得・比較するまでは、数学的な意味での包含・同値は未判定とする。原本の実証的照合も行わない。全体 pytest は Phase 163 終了時のみ。

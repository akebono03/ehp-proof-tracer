# Phase 165 R14-R22

## 変更対象（全文同梱）
- 新規 `phase165_r14_r22_same_reference.py`：`Toda51Integration`、`integrate_toda51_into_existing_reference`、`audit_r22`
- 新規 `test_phase165_r14_r22_same_reference.py`：テスト6関数
- `audit.py`、`run.ps1`、`toda_51_complete.tex`

## 内容
既存 Phase163 Registry の (5.1) の `reference_id` を再利用し、同じ参照下で六つの component assertion を追加する。新規 Reference を増やさず、旧117件の出典アーカイブ主張を保存する。第4項に R21 由来の型付き特殊化2件を保持する。ただし6件は全て SOURCE_ARCHIVE であり、証明用引用を解禁しない。Registry コピーへの統合のため既存呼び出しを破壊しない。

## テスト・完了条件
局所pytest 6件。既存参照の再使用、無条件引用の禁止、元データ不変、重複拒否、6項目整合性。

## 次工程との境界
R23以降に原典確認および認証済み型付き Assertion への段階的変換、共通 Backward Search への接続。全体pytestはPhase165末尾のみ。

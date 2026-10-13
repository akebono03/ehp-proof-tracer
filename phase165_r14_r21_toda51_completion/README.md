# Phase 165 R14-R21

## 変更対象（全文を同梱）
- 新規 `phase165_r14_r21_toda51_completion.py`: `Toda51Clause`, `Toda51CompletedSource`, `normalize_tex`, `complete_toda51_source`, `diagonal_specializations`, `audit_r21`
- 新規 `toda_51_complete.tex`: (5.1) の番号付き数式と直後の表示数式を同じ文献項目として収録
- 新規 `test_phase165_r14_r21_toda51_completion.py`: 7 テスト
- 新規 `audit.py`, `run.ps1`

## 方針
既存の参照番号 (5.1) は維持する。これまで欠落していた後半3項目を含む、全6項目の一つの文献項目として TeX ソースの整合性を検証。対角群の二つの特殊化は R15 の型付きスキーマを再利用する。

この段階では、入力の採用 TeX と掲載されたテキストを照合するだけで、原典版との独立照合や数学的認証の承認とは区別する。既存の Phase163 アーカイブは変更せず、同一 locator の補完ソースを別ファイルで用意する。source-only から ProofStep への無断昇格は行わない。

## 完了条件・次の境界
7 テスト合格、6項目整合性と2つの型付き特殊化を確認できること。次はこの6項目を既存台帳の単一 Reference へ安全に統合する。全体 pytest は Phase165 終了時のみ。

# Phase 166 R2 — Toda (5.3) 数学的同一性の予備監査

## 変更対象

- 新規 `phase166_r2_equation53_audit/audit.py`：`load_rows`、`classify_53_row`、`inspect`、`main` を追加。
- 新規 `phase166_r2_equation53_audit/test_audit.py`：限定テスト4関数を追加。
- 新規 `phase166_r2_equation53_audit/run.ps1`：監査と限定テストを実行。
- 新規 `README.md`、本 `AUDIT.md`。既存本番コードは変更しない。

## 現在の GitHub 実装について

`phase163_r4_registry_bridge.build_registry_bridge()` は文献構成要素を `MigrationStatus.METADATA_ONLY` として台帳に登録する。`TodaFixedStatementComponent` は文献項目・主張の役割・順序・範囲を保持するメタデータで、関係式の左右辺を型付きで保持しない。`phase165_r2_registry_lookup.py` の証明資格判定は本監査では呼び出さない。

## 予備観測

(5.3) 出典行は CSV 3、4、5、8 行。3 と8 は表示上同じ関係式 `\\eta3^3` と `2\\nu'` を持つ。一方で4 は `\\eta3^3(2\\iota6)` と零、5 は左辺空欄と `2E\\nu'` であり、同一の式として扱わない。

## 完了条件と境界

- 出典行数・登録構成要素数の整合、表示式の形、表示上の重複を確認する。
- `mathematical_identity_confirmed=0`、`proof_permission_granted=0` を維持。
- 型付き生成元の検査・文献本文と数学的な等価性の確認・他の群データとの対応は R2 の後続作業。
- 引用資格の判定は R3。共通逆向き探索への接続は R4。全体 pytest は R10。

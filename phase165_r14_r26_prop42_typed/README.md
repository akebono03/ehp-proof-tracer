# Phase 165 R14-R26

## 変更対象
- 新規 `phase165_r14_r26_prop42_typed.py`: `Prop42TypedBinding`, `_clean`, `validate_prop42_source`, `typed_delta_e_window`, `bind_proposition42`, `adopted_tex_proofstep`, `audit_r26`（全文を同梱）
- 新規 `test_phase165_r14_r26_prop42_typed.py`: 7つの対象テスト（全文）
- 新規 `run.ps1`, `audit.py`、本書
- 既存の Registry / rules / tests に変更なし。

## 実装内容
資料を直接照合した結果、`ch4:0002` は式(4.2)・有限群の主張であり対象外。Proposition 4.2 は `ch4:0005`、完全列は式(4.4)。その五つの群項の順序と \(E,H,\Delta\) 記号を照合し、既存 `TodaProp42ExactnessStatement` に \(n=1,i=2\) を特殊化する。

出典本文には適用範囲が書かれていないため、実際の `n=1` への適用には `index_scope_confirmed=True` という明示的承認が必要。テストの条件付き ProofStep はこの分岐のみで生成され、実運用での認証済み証明と混同しない。出典データと元の Registry を変更しない。

## 完了条件と次工程
対象7件の pytest 合格、型付き完全性の対象群が \(\pi_3^3\to\pi_1^1\to\pi_2^2\) に一致すること、未承認では ProofStep を作らないこと。次は適用範囲の根拠を確定した後、既存 R24 の \(\Delta=0\) 推論に接続する。全体 pytest は Phase 終了時のみ。

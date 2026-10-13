# Phase 165 R14-R4 — Toda (5.1) Remaining Typed Schemas

## 変更対象
- 新規 `phase165_r14_r4_remaining_schemas.py`: `StableStem`, `StableIdentity`, `Toda51TypedClaim`, `instantiate_remaining_toda51_clause()`, `audit_remaining_toda51()`
- 新規 `test_phase165_r14_r4_remaining_schemas.py`: 各テスト関数全文
- 新規 `audit.py`, `run.ps1`, `README.md`
- 既存モジュール、Registry、Web、ProofStep は変更しない。

## 方針
残り4主張を型付きスキーマへ変換する。`G_0` は具体的な既存 stable-group object の正確な表現を確認できていないため、記号的な型付き tuple のまま保持する。`E^∞` も計算済みの写像ではない。

## 完了条件
4主張の型付き表現、範囲の拒否、6件の既存 SourceClause の保持、証明資格0件、ProofStep 0件。pytest は追加したテストのみを実行する。

## 次工程
出典の原本照合、`G_0` と `E^∞` の正式な既存数学型への接続、EHP 共通展開規則の認証。R14-R4 の結果のみでは π₃² は証明されない。

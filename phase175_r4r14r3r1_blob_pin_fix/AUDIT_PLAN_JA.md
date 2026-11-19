# R4R14R3R1 — Git blob 固定値修正

## 原因

R4R14R3 の監査コードで `phase174_r3_r7_r7_composite_zero_audit/rule.py` に対応する SHA を42桁として記述したため、DryRun の source guard が失敗した。

## 変更対象

- 新規監査パッケージ `phase175_r4r14r3r1_blob_pin_fix/run.ps1`（追加）
- 同 `audit.py`（既存 R4R14R3 監査ファイル全体の正しいコピー）
- 既存 `phase175_r4r14r3_binary_composition_audit/audit.py`（インストール時、固定 SHA の2文字削除のみ）

本番コード、既存数学規則、GIVEN、共通 Renderer、既存テストは変更しない。

## 検証

DryRun は source guard のみ、本実行は監査本体と限定 pytest。全体 pytest は実行しない。

## 完了条件

R4R14R3 の元の Gate と限定 pytest が PASS し、新規修正 Gate が PASS すること。次段階の二因子一般規則の実装は行わない。

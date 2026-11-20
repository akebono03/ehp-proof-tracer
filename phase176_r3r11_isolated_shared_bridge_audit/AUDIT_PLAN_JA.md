# Phase 176 R3R11 — 独立証明・共有探索の接続監査

## 監査対象

- 前工程 R3R10 の `report.json`（実際の階層キーと検証結果）
- `phase165_r52_r9_shared_math.py` の `shared_expansion_provider`
- `phase175_r4r14r4_general_zero_transport/rule.py` の `composite_value_zero_inputs` と `expand_proved_composite_zero_image`
- `phase175_r4r14r5_public_zero_transport/provider.py` の `build_public_composite_zero_transport_provider`
- `phase175_r4r14r5_public_zero_transport/tests/test_provider.py` の既存テスト

## 変更対象

既存ファイル、クラス、関数、メソッドの変更なし。ルート直下に `phase176_r3r11_isolated_shared_bridge_audit/` を新規作成し、`audit.py` の `git_output`、`scalar_evidence`、`interesting_evidence`、`audit`、`main` と新規テスト4件、実行用 `run.ps1` を追加する。

## 判定境界

既存 Provider の入口条件・静的な接続を確認する。R3R10 の実際の ProofStep と shared Goal の一致、候補0件の原因は、出典・型・証明木が確認されるまで未確定とする。新規 GIVEN 0、数学規則 0、既存 production 変更 0。

## テスト

`python -m pytest -q phase176_r3r11_isolated_shared_bridge_audit/tests/test_audit.py phase175_r4r14r5_public_zero_transport/tests/test_provider.py`

全体 pytest は Phase 最終 Gate のみ。

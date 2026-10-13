# Phase 165 R14-R12 — 未認証前提の接続

## 変更対象
- 新規 `phase165_r14_r12_registry_obligations.py`（`UncertifiedPremiseBinding`, `bind_delta_zero_obligations`, `audit_r12`）
- 新規 `test_phase165_r14_r12_registry_obligations.py`：テスト5件
- 新規 `audit.py`, `run.ps1`, `README.md`

## 変更内容
- R14-R11 の `Delta=0` から逆向きに、`E:π₁¹→π₂²` 同型性と `Δ→E` 完全性を抽出。
- Proposition 4.2 の文献識別子を既存 Registry 内で探索し、見つかれば source archive に関連付ける。
- **同型性は文献固定命題とはみなさず、導出が必要な Goal として扱う。**
- 出典照合だけでは ProofStep の認証・ProofStepLink の作成を行わない。

## 確認・次工程
`run.ps1` は対象テスト5件と監査レポート生成だけを実行。既存 API と既存テストには変更を加えない。全体 pytest は Phase 終了時のみ。

完了条件は2つの型付き前提の接続が確認でき、追加認証0件・ProofStep0件であること。次は Proposition 4.2 の一般条件と、低次元での E 同型性の出典・適用範囲を確認し、個別の登録承認と探索全体の再実行を行う。本文・テスト・スクリプトは ZIP 内に全文収録。

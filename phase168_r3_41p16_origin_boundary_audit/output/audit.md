# Phase 168 R3-41P16 — 推論規則・Bridge 由来の監査

アプリ本体、既存テスト、既存の固定基準は変更しない。

## 実際の3群での経路照合

| 群 | INFERENCE | factory 同一オブジェクト | GIVEN | 選別済み Bridge | 入口確認 | 本文一致 |
|---|---:|---:|---:|---:|---|---|
| pi3_2 | 13 | 13 | 5 | 5 | True | True |
| pi4_3 | 19 | 19 | 6 | 6 | True | True |
| pi5_4 | 7 | 7 | 3 | 3 | True | True |

## 信頼境界の限界

- 任意に与えた規則が既存 matcher を通過可能: `True`
- 任意に与えた Bridge が GIVEN を承認可能: `True`
- 任意 Model に未登録 GIVEN を格納可能: `True`
- Renderer 側の2つの形状チェックは維持: `True`

## 次工程に対する設計判断

- 正規経路の監査で確認したオブジェクト同一性は、公開 API 全体の信頼性証明ではない。
- Backward Search の導出結果と screened Bridge の由来を結び付ける情報は、現在の PartialProofResult に存在しない。
- 信頼境界の一般化には、探索時に確定した根拠の受け渡し・改変防止と、未認証 Model の区別が必要。
- ゼロ前提の自作規則が既存 matcher で通過するため、単なる再照合は規則自体の正当性を保証しない。
- 数学的検証エンジンや別の規則台帳を追加して解決しない。
- 今回は観測のみで、Renderer の2チェックは除去しない。
- partial・既存 API は変更せず、全体 pytest は Phase 終了まで実行しない。

**AUDIT_STATUS**: `ORIGIN_TRACED_LIMITS_CONFIRMED`

**FULL_PYTEST_NOT_RUN**

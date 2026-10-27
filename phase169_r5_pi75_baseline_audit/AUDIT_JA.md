# Phase 169 R5 — π₇⁵ 現状監査

## 目的

Phase 169 R4G の π₆⁴ 完成証明と Reference 表示を維持し、π₇⁵ の Backward Search（逆向き証明探索）と文献順の接続状況を読み取り専用で調べる。

## 検証対象

- `phase165_r55_nk_only_goal.py`: n=5,k=2 の型付き群構造 Goal。
- `phase169_r3o_stable_composite_rule.py`: Toda (4.5) による η² の輸送。
- `phase165_r52_r9_shared_math.py`: 共通 expansion provider。
- `web_group_proof.py`: 公開 Web Narrative。
- `phase168_r3_41p13_trust_boundary`: 完成証明の信頼境界。

## 範囲と完了条件

本監査では変更対象の本番ファイル・クラス・関数・既存テストはない。新規の `audit.py` と `tests/test_r5_pi75_baseline.py` および `run.ps1` を追加するのみ。

限定 pytest 17件、Git tracked status 不変、Goal・既存証明ステップ・未解決 Goal・文献順・Renderer の監査記録が作成されれば完了。探索状態が partial の場合も partial として報告し、完成扱いにしない。

次 Phase は監査から特定した接続不足のみに修正を限定する。全体 pytest は Phase 169 の終了時のみ実施する。

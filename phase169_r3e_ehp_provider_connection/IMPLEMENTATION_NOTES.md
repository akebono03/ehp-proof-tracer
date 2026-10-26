# Phase 169 R3E — 実装記録

## 今回の変更対象

- 本番ファイル：`phase165_r52_r9_shared_math.py` のみ
- 変更関数：`shared_expansion_provider()` 全体
- 関数内 import：`expand_registered_ehp_goal` を追加。既存の top-level import に変更なし
- 追加位置：既存の `extra_providers` 構築直後、`available = []` の直前
- 新規テスト：`tests/test_phase169_r3e_ehp_provider_connection.py`

## 目的と制約

既存の `phase165_r14_r5_ehp_connection.expand_registered_ehp_goal()` が返す `GoalExpansion` を共通 Provider に登録する。新しい数学的公理、GIVEN、ProofStep、完了済み証明、専用 Renderer は追加しない。既存の型付き n=3 EHP 展開を再利用する接続に限り、一般の n についての同型性を主張しない。

この接続だけでは、`TodaHopfInvariantSurjectiveStatement` と `TodaDeltaInjectiveStatement` の終端導出は完成しない。Proposition 4.2 の既存特殊化が4件とも候補として存在することを維持する。

R3D で観察された `PI4_CLAIM_SCREENED_AS_GIVEN=False` は、参照命題成分と完成内部証明との一致性を別途調べる必要がある。この Phase では変更しない。

## 検証

`run.ps1` は新規テストと関連する既存テストを限定実行し、実際の引用文献順の探索を確認する。エラー時は、変更済みファイルが導入直後の内容と完全一致する場合にのみバックアップから復元する。全体 pytest は Phase 169 の最終工程まで実施しない。

## 次の Phase との境界

R3F 以降で残った終端命題について、使用できる先行文献と必要な `INFERENCE` の証明祖先を確認する。R3E の段階では `π_5^3` の完了を主張しない。

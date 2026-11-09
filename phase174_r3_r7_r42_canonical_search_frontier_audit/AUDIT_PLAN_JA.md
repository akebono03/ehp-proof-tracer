# R42 監査方針

- 対象：`phase174_r3_r7_r42_canonical_search_frontier_audit/` の新規コードのみ。
- 既存コード／ルール／共通 Renderer／データベース／ドキュメントは変更しない。
- GitHub `akebono03/ehp-proof-tracer` の `develop` を監査し、R41 の統合済み HEAD `f604062833ff4dc2756daa96235814983f98fbf2` と、統合直前 HEAD `92edf5d5c5025243e70e06e57baa9220668cc7b6` の厳格な引き継ぎを確認する。
- 追跡対象9ファイルについて Git blob SHA を検証し、R41 以外の編集を拒否する。
- 既存の `shared_expansion_provider()` から R41 零像推論候補・R3 最終 EHP 候補・R37 上側 Δ 候補・R5 Hopf 単射性候補を照合する。
- R37 が隔離されている事実を、R41 公開登録の成功と区別する。
- 実際の `search_registered_partial_proof()` を限定した公開候補で呼び、最終目標の未解決上側 Δ と、直接零像 Goal での DB prior 適用境界を確認する。
- **限定探索は Web 全探索ではない。** 全探索の結果や Web HTTP 実測を偽装しない。
- 既存 R41、R40、R37、R5 の限定回帰 pytest のみを実行する。全体 pytest は Phase 終了時のみ。

期待 Gate：`PASS_R42_CANONICAL_SCOPED_SEARCH_UPPER_DELTA_PROVIDER_AND_DB_SCOPE_PENDING`。

次の R43 への境界：R37・R5 の一般推論候補を公開探索へつなぐ工程。実証明がない状態では最終根を完成扱いにしない。

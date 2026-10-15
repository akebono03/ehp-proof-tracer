# R57-R15 監査

- GitHub の `phase165_r52_r9_shared_math.py`, `web_group_proof.py`, `phase165_r52_r3_web_adapter.py`, `phase165_r52_r17_internal_dependency.py` と現行 R57-R14 の配布済み関数を確認した。
- 通常の目標検索の共通関数は R57-R13 時点では完成済み ProofStep を持つ台帳を要求していた。
- R57-R14 はオンデマンド再帰検索を実装したが、別引数で明示する必要があった。
- R57-R15 は、完成証明を持たない `ProofOrderCatalog` を通常の `proof_order_catalog` 引数で受けると再帰検索へ切り替える。
- 既存の型付き Reference、推論規則、ProofStep の意味は変えない。
- 順序データの正式な供給元は未実装である。Web が `n,k` だけで先行証明まで完結するとは主張しない。
- 全体 pytest は Phase 終了時にのみ実施。

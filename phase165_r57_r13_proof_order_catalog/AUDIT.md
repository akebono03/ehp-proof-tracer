# R57-R13 監査

- 現行 GitHub の `phase165_r52_r9_shared_math.py`, `phase165_r52_r17_internal_dependency.py`, `phase165_r52_r18_proof_order.py`, `unified_statement_registry.py` と R57-R12 配布済みの関数全文・テストを確認した。
- `UnifiedStatementRegistry` の `publication_position` は文献掲載順で、群の証明順そのものではない。`available_after_position` も完成 ProofStep の正式順位として自動流用しない。
- R57-R13 は新規 `ProofOrderCatalog` への明示登録を必須とする。各検索では対象の順位と先行完成証明を自動取得する。未登録対象は fail closed。
- 既存の `CompletedInternalProof` の型・循環依存検査と R57-R12 の strict earlier 検査を維持する。
- 本番の catalog 自動構築、旧 Repository からの完成証明取込、Toda (4.5) の具体同型 GIVEN は未実装。
- 全体 pytest は Phase 165 末尾のみ。

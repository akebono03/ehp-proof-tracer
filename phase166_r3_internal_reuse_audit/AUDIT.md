# Phase 166 R3 — 内部証明の再利用資格監査

## 対象と変更

既存コードは変更しない。新規追加するのは、このディレクトリの `audit.py`（`function_tree`, `called_names`, `inspect`, `main`）、`test_audit.py`（`make_completed` および5テスト）、`run.ps1`、`README.md`、`AUDIT.md` のみ。

## 現行コードから確認した境界

- `CompletedInternalProof` は推論規則による根を要求し、祖先の自己依存と構造循環を拒否する。ただし数学的正当性を独立に認定する型ではない。
- `find_reusable_internal_proof` は対象一致、自己引用、祖先経由の依存、曖昧な候補を検査するが、証明順序の検査は引数だけでは行えない。
- `ProofOrderCatalog.select_prior` は明示登録した証明順序に従い、厳密に前の証明のみ選択する。
- GitHub で確認した `reconstruct_registered_goal` の公開入口は `completed_internal_proofs` を直接受け取り、内部で `find_reusable_internal_proof` を呼ぶ。`select_prior` を直接呼ばない。外部呼び出し側で順序を制約しているかは、今回の直接入口だけでは断定できない。

## 判定

R3 未完了。実行結果を見て、順序ゲートの接続経路と、本当に必要な最小修正を判断する。R4 の関係式接続、R6〜R8 の証明生成は先取りしない。全体 pytest は R10 のみ。

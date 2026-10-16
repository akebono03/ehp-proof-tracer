# Phase 165 R6-2 R2: 検証付き逆向き候補生成

追加するファイルは `phase165_r6_2_r2_verified_inverse.py`、新規関数は `reverse_rules_from_witnesses()` です。リポジトリ直下に追加します。既存の `InferenceRule` と `ProofStep` に基づき、結論パターンのない規則でも、既存の型付き前提が揃えば Forward Inference によって検証済みの逆向き GoalExpansion を候補として返します。

未登録の前提を生成せず、探索予算超過時は停止します。これは共通探索に統合する前の独立モジュールです。`expand_existing_pi43_rules()` はまだ削除せず、$\pi_4^3$ の完全な証明生成も今回の完了条件とはしません。

PowerShell の `install.ps1` はファイルの衝突を確認し、配置して限定 pytest 4件を実行します。全体 pytest は Phase 165 終了時のみです。

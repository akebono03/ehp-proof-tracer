# Phase 165 R6-2 R3: 接続

変更ファイルは `phase165_r52_r9_shared_math.py`、変更関数は `shared_expansion_provider()` のみ。既存 import は変更しない（必要な import は変更した関数内にすべて記載）。新規クラス・関数は本番コードに追加しない。

既存の `reverse_rules_from_witnesses()` を共通候補生成に接続する。Witness（候補前提）は出典登録済みの `AssertionOrigin.FIXED_STATEMENT` で、`ProofRule.GIVEN` のステップに限定する。提案された GoalExpansion は証明ステップではない。既存の再帰検証は維持する。

2048 の組み合わせ制限を超えた場合はこの経路から候補を返さず、旧候補生成を維持する。`expand_existing_pi43_rules()` はまだ撤去しない。

`run.ps1` を解凍先リポジトリ直下から実行する。対象限定 pytest は3件。全体 pytest は Phase 終了時のみ。R6-2 R4 は汎用逆向きの再帰的な未登録前提生成と Adapter 置換を扱う。

# R17-R1 変更一覧

- `install.py`: R16 の関数宣言を AST で識別し、`completed_internal_proofs` を追加。既に適用済みなら重複適用しない。全変更の構文を検証後にファイルを更新する。
- `phase165_r52_r9_shared_math.py`: `search_shared_group_goal()` のシグネチャと `search_registered_partial_proof()` への引数伝播のみ修正。変更前バックアップを作成する。
- `phase165_r3_recursive_search.py`: 部分適用済みの変更を保持。
- `phase165_r52_r2_search_adapter.py`: 部分適用済みの変更を保持。
- `phase165_r52_r17_internal_dependency.py`: R17 の新規クラス・関数全文を収録し、リポジトリ直下へ配置。
- `test_phase165_r52_r17_internal_dependency.py`: テスト6件と import 全文を収録。
- `run.ps1`: 既存のR17対象 pytest を実行する。全体 pytest は行わない。

次段階: Registry への証明済み結果の自動登録は本修正の対象外。

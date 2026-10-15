# R57-R17 監査の対象と境界

- GitHub `akebono03/ehp-proof-tracer` の `web_group_proof.py`、`phase165_r52_r9_shared_math.py`、`phase165_r52_r18_proof_order.py`、`phase165_r52_r19_prop51_binding.py` を確認した。
- R57-R14、R57-R15、R57-R16 の配布コードと R57-R16 の関連テストを確認した。GitHub のデフォルトブランチには `phase165_r55_nk_only_goal.py` が存在せず、利用者側のインストール済みコードを直接確認する必要がある。
- 通常入口 `search_group_from_registered_goal` が順序台帳を解決し、`search_shared_group_goal` が R57-R14 の再帰処理を起動する構成である。
- 今回は読み取り専用。既存の関数・クラス・推論規則・Renderer・ドキュメントを変更しない。
- 新規ファイル: `audit.py`、`test_audit.py`、`run.ps1`、`README.md`、`AUDIT.md`、`CHANGED_CODE.md`。
- `audit.py` はプロセス内だけで `search_registered_partial_proof` を計測し、元の関数をそのまま実行する。
- `root_expansion_count` は初期目標に対する展開候補数であり、探索全体の候補数ではない。
- `proven_step_count` は結果の表示可能なステップ数であり、数学的正当性の認証ではない。
- 実行時の出力を読まなければ $π_5^4$ の失敗原因を断定できない。判定は次段階に回す。
- 全体 pytest は実行しない。診断用テスト4件だけを実行する。

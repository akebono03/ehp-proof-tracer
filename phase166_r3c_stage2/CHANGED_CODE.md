# Phase 166 R3-C 第2段階

変更対象：

- `phase165_r52_r16_web_citation_gate.py`: `screen_shared_proof_context` 関数全体（修正後全文を実行時 `.installed_full.txt` に保存）
- `phase165_r3_recursive_search.py`: `reconstruct_registered_goal` 関数全体（同上）
- `phase165_r52_r9_shared_math.py`: `search_shared_group_goal` 関数全体（同上）
- 新規 `phase166_r3c_publication_order.py`: `precedes_citing_assertion`（ZIP に全文）
- 新規 `phase166_r3c_stage2/test_stage2.py`: 全テスト関数と import を全文同梱

既存 import は変更しない。既存クラスは変更しない。`run.ps1` は変更前ファイルをバックアップしてから対象限定 pytest のみ実行する。

完了条件：既存の直接引用／順序テストおよび新規テストが PASS、Web の $\pi_3^2$ 完全証明が維持されること。

R3-D の正式な完全証明回帰、R3-E の $\pi_4^3$ と $\pi_5^3$ は次工程。全体 pytest は Phase 166 の終了時だけ実施。

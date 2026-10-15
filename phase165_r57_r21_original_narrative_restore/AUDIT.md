# Phase 165 R57-R21 表示経路復旧監査

GitHub `akebono03/ehp-proof-tracer` の `phase165_r57_r21_narrative_unification/install.py`、`CHANGED_CODE.md`、現行 `phase165_r56_presentation_adapter.py`、現行 `phase165_r52_partial_proof.py`、旧バックアップ `phase165_r56_presentation_adapter.py.phase165_r57_r21_backup`、Web 公開経路を照合した。

R57-R21 で完成証明の Adapter が従来の `build_complete_toda_group_result_proof_replay` → `build_toda_group_proof_presentation` → `render_toda_group_proof_narrative_markdown` から簡略版 `render_toda_partial_proof_narrative_markdown` に明示的に切り替えられたことを確認した。画面の `generic-partial-proof` は共通 Web Adapter の識別子であり、今回の変更では変更しない。

今回は完成証明の Renderer 経路をバックアップから復旧し、`render_partial_proof_markdown` が COMPLETE のときのみ旧完成 Adapter へ分岐する。部分証明は現在の Renderer を維持。数学的推論と `ProofStep`、探索器は変更しない。

**留意点**: これは以前の表示経路への復旧であって、すべての型付き Goal に対する旧 Narrative の対応を新規に証明するものではない。旧 Adapter は `DirectSumGroup` について明示的に拒否する既存制限があるため、既存の挙動を維持している。旧コードの転記は GitHub に存在する R57-R21 バックアップと照合すること。

実リポジトリの限定 pytest 5件で実動作を検証する。全体 pytest は Phase 165 終了時まで実行しない。

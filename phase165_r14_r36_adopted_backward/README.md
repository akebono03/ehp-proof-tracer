# Phase 165 R14-R36

## 変更対象
新規ファイル `phase165_r14_r36_adopted_backward.py` に `adopted_leaf_steps`、`reconstruct_adopted_tex_goal`、`audit_r36` を追加する。関連テストは `test_phase165_r14_r36_adopted_backward.py` の7関数。`run.ps1`、`audit.py`、採用 TeX を同梱し、既存コード・Registry・数学的推論規則は変更しない。

## スコープ
R34 の最終目標と展開規則を利用し、R35 の既知6件、R23 の Toda (5.1) 対角群2件、R17 の出典付き基本事実1件を型で一致させる。証明木は最終目標から再帰的に生成し、R33 の完成済み証明を Replay しない。

これは採用 TeX に基づく探索の実証であり、厳密な Registry の検証済み引用資格を付与しない。原本照合や source provenance の確認が欠ける状態で `strict_registry_proof_created=true` にしない。

## 完了条件
対象7テスト。9件の葉を一意に取得し、Backwards Search によって最終ゴールの推論 ProofStep を得る。不足・重複葉は拒否する。全体 pytest は Phase 165 終了時だけ。

## 次工程との境界
採用 TeX の探索と strict production Registry を一致させるには、各出典の検証、明示的な資格付与、および strict `reconstruct_registered_goal` を通す必要がある。本工程は資格付与を行わない。

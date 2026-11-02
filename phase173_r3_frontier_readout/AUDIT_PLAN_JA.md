# Phase 173 R3 保存レポートの停止点表示（監査のみ）

- 既存の `phase173_r3_manual/audit.json` から $\pi_7^4$ と $\pi_8^5$ の Root Candidate と直下 Subgoal を表示する。
- `child_proposal_count` と `exact_screened_given` は前回観測された値をそのまま扱い、0件から数学的な「規則が存在しない」とは結論しない。
- 重複 Subgoal で診断が省略された値は `NOT_PROBED_DUPLICATE` と表示する。
- 先行結果の `eligible` は文献順の資格であって、ProofStep 完成を示さない。
- 新規コード: `phase173_r3_frontier_readout/readout.py`、`run.ps1`、`tests/test_readout.py`。既存コード・既存テストは変更しない。
- 既存主要文書5件は変更しない。全体 pytest は Phase 173 の最後のみ実施する。
- 本監査は R4 の実装に進む前の分析補助であり、R4 用新規推論規則は導入しない。

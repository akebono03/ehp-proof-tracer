# Phase 166 R3-AI: Zero Group Web Goal

変更対象: `phase165_r55_nk_only_goal.py` の `search_group_from_registered_goal`、
`toda_group_proof_narrative_renderer.py` の `render_toda_partial_proof_narrative_markdown`、
`phase165_r52_r3_web_adapter.py` の `build_partial_web_group_proof_view`。

WebでDB由来の零群Goalを証明対象・未解決Goalとして表示する。
`ProofSearchStatus.NOT_SEARCHED` を維持し、証明を作らない。
文献順序と既存の証明規則は変更しない。

新規テストは `tests/test_zero_web_display.py` の4件。
実行 `run.ps1` は追加で直前の零群5件を検証する。
全体pytestは実行しない。

完了条件: `pi_9^2 = 0` がWebのProof targetと証明対象・未解決Goalに現れ、
COMPLETEと誤認されないこと。
次段階: 零群の証明探索そのものへの接続。

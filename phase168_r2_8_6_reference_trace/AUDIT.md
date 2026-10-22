# Phase 168 R2-8⑥：Reference 経路監査

## 変更対象

- 新規 `audit.py`：`describe_step()`、`describe_entries()`、`inspect()`、`main()`。
- 新規 `tests/test_r2_8_6_reference_trace.py`：3件の限定テスト。
- 新規 `run.ps1`、`README.md`、`AUDIT.md`。

本番ファイル、既存クラス、既存メソッドは変更しない。

## 対象

GitHub `develop` の `phase165_r56_presentation_adapter.py`、`toda_group_result_proof_replay.py`、`toda_group_proof_presentation.py`、`toda_group_proof_narrative_references.py`、`toda_group_proof_narrative_renderer.py` を確認した。

## 完了条件

`pi_4^2` の探索・ProofStep・Replay・Presentation・Reference entries・本文を同一実行で観測し、欠落位置を判定する。`COMPLETE` だけで表示の数学的正当性を認定しない。次段階で原因に応じた最小修正を行う。全体 pytest は実行しない。

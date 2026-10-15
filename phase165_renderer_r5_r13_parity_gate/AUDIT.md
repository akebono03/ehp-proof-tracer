# Phase 165 R5-R13 監査設計

## 対象

- `phase162_web_narrative_integration.py` の旧 Web Narrative 入口
- `phase162_r3_narrative_connection.py` の旧 Narrative 入口
- `phase162_ehp_leaf_inputs.py` と `phase162_pi5_3_web_replay.py` の R5-R11 接続
- `web_group_proof.py`、`cli.py`、`main.py` の正規経路
- `phase165_r55_nk_only_goal.py` → `phase165_r52_partial_proof.py` の新方式による $\pi_5^3$ の表示

## 方針

新方式に旧 `ExistingProofConnectionResult` を無理に渡したり、証明済みでない Goal を完成証明へ昇格させたりしない。実行時に旧入口と新入口を別々に検査し、出力が得られない場合は理由を記録する。双方が文字列を生成しても、数学的同等性を認定しない。

`PRECONDITION_FAILED` は接続前提の欠落。`REVIEW_REQUIRED` は証拠収集完了であり、旧経路の撤去承認ではない。

## 既知の問題

Phase 162 の旧 fixture の6件は `prop51_steps[0]` が空で失敗していた。今回の監査はこれらを実行も修正もしない。旧出力の生成が同じ原因で失敗した場合は `ERROR` として残す。

## 今回の変更

新規監査用ファイルのみ。既存コード・テスト・5つの主要文書は変更しない。全体 pytest は Phase 165 の最後に限る。

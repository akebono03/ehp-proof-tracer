# Phase 165 R14-R41 — 証明木の受け渡し監査・修正

変更対象：`phase164_r5_r2_common_replay.py` 内の `build_phase164_r5_r2_common_replay`（R40 の分岐のみ更新）、新規 `phase165_r14_r41_proof_transfer.py`（`_registered_reference_leaves`、`build_phase165_r41_pi32_common_replay`、`audit_r41`）。新規 `install.py`、`audit.py`、`run.ps1`、対象テスト5件。既存 Web と共通 Renderer は変更しない。

目的：R38 登録証明木の root と9件の末端 Reference を保持し、Narrative モードでは深度2による切り詰めを避けて完全な祖先を共通 Presentation/Renderer に渡す。Trace モードの指定深度は維持する。

完了条件：新規対象 pytest 5件、9件の末端前提を確認し、共通 Renderer が完全な Replay を受け取ること。Reference の文章化・`GeneratorImage` 等の型対応は今回**未修正**であり、表示品質全体の完成は宣言しない。

次工程：Reference が空欄になる原因を共通 Reference 抽出で修正し、新しい型の文章化に対応する。全体 pytest は実行しない。

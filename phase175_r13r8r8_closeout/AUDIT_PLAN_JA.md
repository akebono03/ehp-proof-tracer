# Phase 175 R13R8R8 — 終了判定の監査計画

対象は完成済み3群 `(5,4)`, `(6,5)`, `(7,5)` とする。既存の Source-first / First Successful Proof Search を変更しない。

1. `develop` の Git HEAD と本番2ファイルの Git blob を一致確認する。
2. `R13R8R6` の既存監査を再利用し、ProofStep と Reference の相互対応、出典本文欠落を検査する。
3. `build_standard_web_group_proof_view()` を3群について実行し、完成証明の provenance を検査する。
4. `(5,4)` について R3 / R7 の出典番号と本文引用表示を検査する。
5. 関連する既存の限定 pytest（4+3+6件）のみ実行する。
6. 不備がなければ R13R8 の Closeout を PASS とする。全体 pytest は Phase 175 の最後だけ実行する。

この監査は読み取り専用であり、専用 Narrative、GIVEN、数学規則を追加しない。終了判定は3群に関するもので、将来のすべての命題型への一般保証ではない。

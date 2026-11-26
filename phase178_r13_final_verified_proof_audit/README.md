# Phase 178 R13 — Final verified proof audit

読み取り専用で $(n,k)=(3,6)$ の完成証明を監査する。既存コードを変更せず、R12R2 の実装が正確に適用された状態を前提とする。R12R2 の未コミット状態と、その同じ変更だけを含む後続コミットの両方を許容する。

R12R2 の実際の Web 証明監査を再利用し、根の型、前提の順序、既存推論の再検証、出典、表示を確認する。Lemma 5.7 の採用転記は既存の検証関数で再確認する（原著の独立照合ではない）。

`run.ps1 -DryRun` は作業ツリー・パッケージの事前検査のみ。通常実行は実際の証明と限定 pytest を実行する。全体 pytest は実行しない。

合格条件：`PASS_R13_N3_FINAL_VERIFIED_PROOF_AUDIT`。出力は LOCALAPPDATA/EHPProofTracerAudit 以下の attempt ディレクトリに保存する。

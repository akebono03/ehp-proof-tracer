Phase157-R4-R1 representative Literature Statement Boundary audit

目的:
- Phase157-R3 の pi_6^3 以外の代表群へ展開する前に、
  現在の Reference entry と R2 boundary catalog の対応状況を機械的に確認する。
- production code は変更しない。
- 未登録文献を rule name / literature_reference だけで FIXED_STATEMENT と決めない。

対象:
- pi_8^5
- pi_10^4
- pi_12^5
- pi_15^8
- pi_16^9
- depth 2 / 3

出力:
- phase157_r4_r1_audit_output/phase157_r4_r1_representative_boundary_audit.md
- phase157_r4_r1_audit_output/phase157_r4_r1_representative_boundary_audit.json

確認する分類:
- fixed_statement
- proof_internal
- UNTRACKED

R4-R2:
- R4-R1 で UNTRACKED と判明した文献のうち、
  fixed statement の境界を確認できたものだけ catalog に追加する。
- その後 representative groups の Reference selection に boundary を接続する。

Repository-wide pytest は Phase157 closure まで実行しない。

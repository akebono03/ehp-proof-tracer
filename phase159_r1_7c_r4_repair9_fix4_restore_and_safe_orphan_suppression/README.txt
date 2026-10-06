Phase 159 R1-7c R4 repair9 fix4

目的
====
fix3 で発生した SyntaxError を安全に復旧し、
repair9 の R9-A / R9-C を構造的に最小修正する。

復旧
====
fix3 は適用前に
`phase159_r1_7c_r4_repair9_fix3_literal_reflexive_and_orphan_reference/backup_before_apply/`
へ production file を保存している。

fix4 は最初にこの backup を読み、
fix3 の SyntaxError 状態を完全に捨てる。

その backup は fix2 適用後の状態なので、
fix2 が追加した:
- final graph-based reflexive suppression
- post-selection Reference relink
も明示的に除去する。

R9-A
====
新規 helper:
`suppress_toda_group_proof_narrative_literal_reflexive_equalities()`

最終 public Markdown が literal に `$A = A$` の場合だけ除去する。

保持:
- `2nu' = eta_3^3`
- `eta_3 eta_4 eta_5 = eta_3^3`

除去:
- `eta_5 = eta_5`
- `eta_3^3 = eta_3^3`

R9-C
====
`else:` は追加しない。

final `reference_section = (` の直前で:

  if "[R" not in rendered:
      reference_entries = ()
      statement_lines_by_reference_number = {}

を実行する。

これにより body marker の無い public Reference は表示しない。

Phase boundary
==============
- Equation (5.7) / Proposition 2.2 dependency は変更しない
- generator canonicalization は変更しない
- pi_4^3 はまだ見ない
- stale Phase157 pi15 dedicated-renderer test は今回変更しない
- repository-wide pytest は実行しない

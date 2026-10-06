Phase 159 R1-7c R4 repair9 fix9

目的
====
fix7 実行後も Equation (5.7) の boundary locator が
`Equation 5.7` のまま残る原因を修正する。

原因
====
ローカル現行コードには fixed-rule mapping として:

  Toda Equation 5.7 nu-prime eta_6 Hopf value
    -> Equation 5.7

が残っていた。

`classify_toda_literature_statement_step()` は
fixed-rule mapping を internal fallback より先に参照するため、
fix7 で追加した `(5.7)` internal locator より
この古い fixed-rule locator が優先されていた。

修正
====
`toda_literature_statement_boundary.py` の
fixed-rule locator 1件だけを:

  Equation 5.7 -> (5.7)

へ変更する。

classification:
- FIXED_STATEMENT のまま

component key:
- nu_prime_eta6_hopf_relation のまま

rule name:
- 変更しない

renderer:
- 変更しない

完了条件
========
- classification=fixed_statement
- boundary_locator=(5.7)
- component_key=nu_prime_eta6_hopf_relation
- inferred_locator=(5.7)
- pi_6^3 Reference: **[R5] (5.7).**
- `Equation 5.7` が public Reference header に出ない

全体 pytest
===========
実行しない。

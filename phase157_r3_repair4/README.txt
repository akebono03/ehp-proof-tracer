Phase157-R3 repair4

目的:
- repair3 の recursive proof-step recovery 自体は成功している。
- 既存 generic renderer は TodaSuspensionIsomorphismStatement を
  `$E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型写像である.`
  と表示する。
- R3 tests が誤って `\xrightarrow{\cong}` を期待していたので、
  現行 renderer contract に合わせる。

Production code changes:
- none

Test changes:
- tests/test_phase157_r3_pi6_3_reference_boundary.py
- tests/test_phase157_r3_repair3_recursive_internal_recovery.py

確認事項:
- suspension isomorphism が Reference に出ないこと
- suspension isomorphism が depth 3 proof body に出ること
- Prop.5.6 earlier fixed group result が Reference に残ること
- R2 boundary tests と Phase156 boundary-collapse regression が維持されること

Repository-wide pytest は Phase157 closure まで実行しない。

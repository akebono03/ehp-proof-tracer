Phase 159 - generic zero/exactness map-property unification repair3

原因
====
Phase 150 regression test にも

  "$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."

という通常文字列が残っていた。

Python では \t が tab escape として解釈されるため、
\to が tab + "o" に変わっていた。

変更対象
========
tests/test_phase150_rc4_5c_2_exactness_to_map_property.py

変更する関数
============
test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion()

変更内容
========
期待文字列を raw string に変更する。

実装変更
========
なし。

完了条件
========
- 4-case generic tests PASS
- pi_4^3 surjectivity focused tests PASS
- pi_4^3 kernel exactness tests PASS
- connector normalization tests PASS
- Phase 150 exactness regression PASS
- Phase 50 bridge regression PASS

repository-wide tests は Phase 159 終了時まで実行しない。

Phase 159 - generic zero/exactness map-property unification repair2

原因
====
tests/test_phase159_pi4_3_exactness_surjectivity_unification.py の期待文字列が

  "$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."

という通常文字列になっていた。

Python では \t が tab escape として解釈されるため、
\to が tab + "o" に変換され、renderer の正しい "\to" と一致しなかった。

変更対象
========
tests/test_phase159_pi4_3_exactness_surjectivity_unification.py

変更する関数
============
test_phase159_pi4_3_surjectivity_reason_is_visible_without_double_connector()

変更内容
========
期待文字列を raw string に変更する。

変更前:
  "$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."

変更後:
  r"$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."

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

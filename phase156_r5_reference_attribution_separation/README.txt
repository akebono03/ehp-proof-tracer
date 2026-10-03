Phase156-R5 repair — (5.3) / Lemma 5.2 attribution separation

変更対象
--------
1. toda_rules.py
   function:
     toda_53_nu_prime_bracket_specialization_inference_rule()

2. tests/test_phase156_r5_reference_attribution_separation.py
   新規テストファイル

Production change
-----------------
nu-prime Toda bracket membership を導入する specialization rule の
LiteratureReference を

  label   = "Toda (5.3) / Lemma 5.2"
  locator = "(5.3) / Lemma 5.2"

から

  label   = "Toda (5.3)"
  locator = "(5.3)"

へ変更する。

変更しないもの
--------------
- Toda bracket membership statement 自体
- Lemma 5.2 specialization rules
- Lemma 5.2 から得る H(nu'), 2nu', membership
- semantic sidecar の Lemma 5.2 application
- その他237件の Reference attribution
- Phase 157 の本文改善

理由
----
112群・238 selected Reference statements の監査で、
composite attribution は pi_6^3 の1件だけだった。

nu' in {eta_3, 2 iota_4, eta_4}_1

は Lemma 5.2 の結論ではなく、Toda (5.3) に由来する input premise。
Lemma 5.2 の適用関係は proof body / semantic application として別に保持する。

実行する focused pytest
-----------------------
tests/test_phase156_r5_reference_attribution_separation.py
tests/test_phase58_nu_prime_specialization.py
tests/test_phase58_lemma52_specialization.py
tests/test_phase153_r11_generic_reference_attribution_filtering.py

完了条件
--------
- focused Phase156-R5 tests PASS
- related existing tests PASS
- 112 groups
- exceptions = 0
- suspicious composite Reference statements = 0
- pi_6^3 の (5.3) Reference が存在
- "(5.3) / Lemma 5.2" composite が存在しない
- proof body には Lemma 5.2 application が残る

次 Phase との境界
-----------------
この repair は Reference attribution の分離だけを行う。
Reference wording や証明本文全般の改善は先取りしない。
repository-wide pytest は Phase 156 closure の最後にのみ行う。

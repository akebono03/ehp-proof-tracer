Phase 159 exactness-reason stale expectation repair6a

変更対象
========

test-only:

- tests/test_phase150_rc4_5c_2_exactness_to_map_property.py
  - 旧:
    test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion()
  - 新:
    test_phase150_rc4_5c_2_exactness_reason_is_visible_without_verbose_duplicate()

production code:
- 変更なし

import:
- 変更なし

理由
====

repair6 後、reason sentence 自体は現在の契約

  完全性より,
  $E: pi_5^2 -> pi_6^3$ は単射.

として正しく1回出力されている。

失敗したのは、旧 verbose conclusion

  $E: pi_5^2 -> pi_6^3$ は単射である.

も別途存在することを期待していた assertion。

現在の public prose 契約では concise reason が conclusion を担い、
verbose duplicate は抑制される。

したがってテストを

- concise reason が1回
- verbose duplicate は0回

へ更新する。

境界
====

- production renderer は変更しない。
- reason builder は変更しない。
- pi4_3 repair5 は変更しない。
- heavy Phase 144 cross-group fixture は実行しない。
- full test suite は Phase 159 終了時まで実行しない。

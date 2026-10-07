Phase 159 - pi_4^3 exactness prose alignment repair2

原因
====
repair1 により EXACTNESS_TO_KERNEL reason が

  完全性より, ker E = Im Δ = ...

を本文に直接表すようになり、その reason が包含する standalone の

  ker E = ...

は semantic duplication として抑制される。

しかし既存の focused test
test_phase159_pi4_3_exactness_reason_is_visible_before_kernel_conclusion()
は、古い契約として kernel standalone statement が本文に残ることを要求していた。

これは新しい表示規則と矛盾する stale expectation である。

変更対象
========
tests/test_phase159_pi4_3_exactness_reason_unification.py

変更する関数
============
test_phase159_pi4_3_exactness_reason_is_visible_before_kernel_conclusion()

import 変更
===========
なし。

変更内容
========
変更前:
  assert kernel_conclusion
  assert kernel_conclusion in rendered
  assert rendered.index(sentence) < rendered.index(kernel_conclusion)

変更後:
  assert kernel_conclusion
  assert kernel_conclusion not in rendered

実装変更
========
なし。

完了条件
========
- Phase 159 pi_4^3 exactness focused tests が PASS。
- Phase 150 exactness-to-map-property regression が PASS。
- Phase 50 pi_4^3 exactness bridge regression が PASS。

Phase 境界
==========
- EXACTNESS_TO_KERNEL 実装は変更しない。
- EXACTNESS_TO_MAP_PROPERTY 実装は変更しない。
- Reference は変更しない。
- equation numbering は変更しない。
- repository-wide tests は Phase 159 終了時まで実行しない。

Phase 159 zero-map stale expectation repair6b

変更対象
========

test-only:

- tests/test_phase157_r11_r17_residual_narrative_defects.py
  - test_phase157_r11_r17_pi6_3_zero_map_statement_precedes_its_use()

production code:
- 変更なし

import:
- 変更なし

監査結果
========

outer-stage audit:

00 with contributions:
  zero_map=True

01 public wrapper:
  zero_map=True

02 finalizer:
  zero_map=True

03 public contract normalization:
  verbose zero-map match=False

しかし actual public output には

  $\Delta: \pi_7^5 \to \pi_5^2$ は零写像.

が存在する。

つまり mathematical statement は消えておらず、
public prose normalization により

  は零写像である.

から

  は零写像.

へ簡潔化されているだけ。

修正
====

旧:

  $\Delta: \pi_7^5 \to \pi_5^2$ は零写像である.

新:

  $\Delta: \pi_7^5 \to \pi_5^2$ は零写像.

順序契約は維持:

  zero-map statement
  <
  完全性より, E は単射.

境界
====

- production renderer は変更しない。
- Phase 159 pi4_3 repair5 は変更しない。
- reason builder は変更しない。
- heavy Phase 144 cross-group fixture は実行しない。
- full test suite は Phase 159 終了時まで実行しない。

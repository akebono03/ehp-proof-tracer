Phase 159 kernel-reason stale expectation repair6c

変更対象
========

test-only:

- tests/test_phase157_r20_repair43_dangling_connector_cleanup.py
  - test_phase157_r20_repair43_required_reason_sentences_remain()

production code:
- 変更なし

import:
- 変更なし

監査結果
========

repair7 後の実際の出力:

CONTRIBUTION:
  完全性より, $\ker \Delta=\operatorname{Im}H=\pi_{7}^{5}$ である.
  $\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像である.
  完全性より, $E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射.

PUBLIC:
  完全性より, $\ker \Delta=\operatorname{Im}H=\pi_{7}^{5}$ である.
  $\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像.
  完全性より, $E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射.

したがって repair7 の順序修正は成立している。

failure の原因は、
Phase 157 dangling-connector test の kernel reason 期待値だけが
repair6 で誤って

  ... \pi_7^5$.

へ変更されていたこと。

実際の production contract は

  ... \pi_7^5$ である.

のままなので、この1箇所だけ期待値を戻す。

完了条件
========

- Phase 159 pi6_3 zero-map reason-order tests PASS
- Phase 150 exactness reason tests PASS
- Phase 157 dangling connector tests PASS
- Phase 157 zero-map/use order test PASS
- Phase 159 pi4_3 focused tests PASS

境界
====

- repair7 production code は変更しない。
- pi4_3 repair5 は変更しない。
- reason renderer は変更しない。
- public contract normalization は変更しない。
- heavy Phase 144 cross-group fixture は実行しない。
- full test suite は Phase 159 終了時まで実行しない。

Phase157-R5-R4 repair1 — test row selection correction

変更対象:
- tests/test_phase157_r5_r4_generic_reference_selection.py

production code:
- 変更なし

import:
- 変更なし

class:
- 変更なし

function / method:
- production function の変更なし
- test function 本体は既存のまま、テスト用 fixed step の rule / locator のみ訂正

原因:
R5-R4 test generator は R5-R3 classification plan から、
r5_r3_component_key が空でない最初の FIXED_STATEMENT 行を選んだ。

しかし R5-R3 repair1 後も classification plan CSV 自体には、
旧 classification plan の
  Proposition 5.3 finite-dimensional aggregate
  -> finite_dimensional_aggregate
が残っている。

production boundary classifier では repair1 により正しく:
  FIXED_STATEMENT
  component_key=None
となるため、generic filter がこの aggregate を除外した。

修正:
テスト用 fixed component を、aggregate ではない concrete fixed statement に変更する。

  locator:
    Proposition 5.8

  rule:
    Toda Proposition 5.8 pi_9^5 group relation

この repair では production filter / restore は変更しない。

focused pytest:
- R5-R4 generic selection
- R5-R3 boundary catalog
- R4 filter / restore compatibility
- R4-R2 catalog
- R2 boundary
- Phase153 selector

完了条件:
- focused tests all pass

次:
- Phase157-R5-R5 112-group cross-audit

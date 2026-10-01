Phase153-R3-10 Fixed2
Route-Neutral Public Reference Verification

原因
====
Fixed1 の残り1件は (n=3, k=3) = pi_6^3。

pi_6^3 の standard generic contribution route は、
canonical Reference section を public output の先頭に持つが、
歴史的に "## 証明" heading を持たない。

そのため、
"structured Reference entry があるなら必ず ## 証明 がある"
というテスト条件が誤っていた。

Fixed2
======
production changes:
- なし

tests:
- tests/test_phase153_r3_10_public_reference_connection_repair.py 全文更新

検証規則
========
1. "## 証明" heading がある route
   -> その heading より前を public Reference section とする。

2. "## 証明" heading がない route
   -> canonical structured Reference section が public output の先頭に
      完全に存在する場合、その canonical section を public Reference section とする。

これにより表示形式ではなく、
selected statement / [Rn] marker が public Reference section に
実際に接続されているかだけを検証する。

今回しないこと
==============
- production code の追加変更
- pi_6^3 の heading 形式変更
- body ownership
- duplicate suppression
- full pytest

完了条件
========
- selected statement public missing = 0
- structured Reference marker missing = 0
- targeted regression tests PASS

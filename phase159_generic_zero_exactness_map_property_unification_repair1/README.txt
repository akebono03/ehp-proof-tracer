Phase 159 - generic zero/exactness map-property unification repair1

原因
====
TodaEHPExactnessWindow.first_map / second_map は MapSymbol で name 属性を持つ。
一方、TodaSuspensionMap / TodaHopfInvariantMap / TodaDeltaMap は
source_group / target_group を持つ concrete map で、name 属性を持たない。

初回実装では concrete map の name を直接比較したため、4ケースすべて不一致になった。

変更対象
========
toda_group_proof_narrative_reasons.py
- import: TodaDeltaMap / TodaHopfInvariantMap / TodaSuspensionMap
- _exactness_to_map_property_reason() 全体

tests/test_phase159_generic_zero_exactness_map_property.py
- 4ケース維持
- TeX テスト文字列を raw string に修正

一般規則
========
TodaSuspensionMap -> E
TodaHopfInvariantMap -> H
TodaDeltaMap -> Δ
MapSymbol -> .name

この正規化を使って exactness window の first/second slot と比較する。

完了条件
========
4 generic tests、pi_4^3 surjectivity、pi_4^3 kernel exactness、
connector normalization、Phase150 exactness、Phase50 bridge がすべて PASS。

全体テストは Phase 159 終了時まで実行しない。

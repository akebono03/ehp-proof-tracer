Phase 158-R5-5 — Derivation completeness audit
================================================

目的
----
Phase 158-R5-3 で public Narrative を generic multi-argument route に一本化し、
R5-4 で equation numbering を共通規則へ修正した後の proof body を監査する。

今回の変更
----------
Production code: 変更なし
Test code: 変更なし
pytest: 実行しない

監査対象
--------
- pi_6^3
- pi_8^5
- pi_15^8
- pi_7^4
- pi_10^4
- pi_11^4
- pi_12^5
- pi_16^9
- pi_4^3

R5-6 との境界
-------------
R5-5 は derivation completeness の defect classification に限定する。
repository-wide public contract の全群監査は R5-6 で行う。

分類
----
VISIBLE_DERIVATION
  「〜を用いる」と表示された proof step に direct consumer があり、
  その consumer の数学的 fact も proof body に表示されている。

RENDERER_VISIBILITY_GAP
  proof graph には direct consumer が存在するが、
  consumer fact が proof body に表示されていない。
  原則として renderer / visibility 側の問題候補。

NO_CONSUMER_IN_PROOF_GRAPH
  「〜を用いる」と表示された step に direct consumer がない。
  proof data / semantic structure / ownership の問題候補。

UNMAPPED_RENDERED_USE
  「〜を用いる」という表示を proof step に対応付けられない。
  prose composition / reference composition 側の問題候補。

STANDALONE_CONNECTOR
  「これらより」「以上より」等の connector の後に
  数学的 conclusion が存在しない。

重要
----
findings は即修正しない。
R5-5 では owner を分類してから repair 方針を決める。

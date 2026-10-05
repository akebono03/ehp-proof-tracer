Phase 158-R5-3 — Public Narrative single generic route
=========================================================

目的
----
public Narrative の full presentation (max_depth >= 2) を、群名に依存せず、
現在 pi_6^3 が利用している generic multi-argument route に一本化する。

監査済み GitHub baseline
------------------------
Repository:
  akebono03/ehp-proof-tracer

HEAD:
  65365234ff0bc52e5ca716dbb92cacd75d4a9c7b

変更対象
--------
Production:
  toda_group_proof_narrative_renderer.py
  - _phase158_baseline_render_toda_group_proof_narrative_markdown

Test:
  tests/test_phase158_r5_3_public_narrative_single_route.py
  - 新規追加

実装内容
--------
max_depth >= 2 の public Narrative は全て次の経路を通す。

TodaGroupProofPresentation
-> semantic closure
-> semantic sidecar
-> narrative blocks
-> narrative arguments
-> multi-argument with contributions renderer
-> public wrapper
-> finalizer
-> Phase 158 public shell normalization

今回行わないこと
----------------
- dedicated helper の削除
- numbering の修正
- dedicated route と generic route の文章差修正
- proof data / semantic data の補完
- repository-wide audit
- full pytest

これらは R5-4 以降の監査・修正対象とする。

互換性
------
max_depth < 2 の direct API fallback は既存動作を維持する。

focused pytest
--------------
tests/test_phase158_r5_3_public_narrative_single_route.py
tests/test_phase143_19_method_evidence.py
tests/test_phase143_46_multi_argument_narrative_assembler.py

full pytest
-----------
実行しない。
Phase 158 closure でのみ実行する。

完了条件
--------
- pi_8^5 が dedicated route を通らない
- pi_15^8 が dedicated route を通らない
- legacy route 代表 pi_7^4 が recursive public route を通らない
- 3群すべて generic multi-argument with contributions renderer を通る
- route selection に群名 hardcoding がない
- depth < 2 direct API fallback は維持される

次 Phase との境界
-----------------
R5-4 で統一後の public Narrative を監査し、
proof item numbering / equation numbering と旧 dedicated 表示との差を扱う。

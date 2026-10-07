Phase 159 - pi_6^3 post-contribution duplicate audit

目的
====
semantic closure contribution renderer の最終出力では

  E:pi_5^2->pi_6^3 は単射.

は1回だけである。

しかし final public Narrative では2回になる。

したがって contribution renderer 後の public pipeline を
4段階に分けて発生点を特定する。

監査段階
========
1. render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()
2. _wrap_phase150_rc4_generic_public_narrative()
3. _finalize_toda_group_proof_narrative_markdown()
4. _phase158_normalize_public_narrative_contract()

各段階で対象文の occurrence count と前後 paragraph を表示する。

production code
===============
変更なし。

tests
=====
変更なし。

repository-wide tests
=====================
実行しない。

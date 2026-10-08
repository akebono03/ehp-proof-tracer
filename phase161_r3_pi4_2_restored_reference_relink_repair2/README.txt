Phase 161-R3 repair2

原因
====
repair1 は GitHub 現行コードの周辺文字列を完全一致 anchor としていた。

ローカル repository では Phase 159-160 の適用履歴による
整形差・配置差があり、意味的には同じ production function でも
その exact block が存在しなかったため、

  Expected exactly one Phase 161-R3 insertion anchor, found 0.

で停止した。

repair2
=======
文字列 block の完全一致を廃止。

対象関数

  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

を AST で特定し、その関数内の

  restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage(...)

を含む statement を探す。

その statement の直後に既存 helper

  link_toda_group_proof_narrative_unmarked_reference_consumers(...)

を再適用する。

これによりローカルの空白・改行・周辺配置の差に依存しない。

変更対象
========
production:
- toda_group_proof_narrative_contribution_renderer.py
  - render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

test:
- tests/test_phase161_pi4_2_restored_reference_relink.py

import の変更なし。

変更しないもの
==============
- Reference fixed-statement catalog
- Toda (5.2) statement
- pi_4^2 proof graph
- final body-usage filter
- pi_5^3
- stable transport
- documentation

全体 pytest は Phase 161 最後にのみ実行する。

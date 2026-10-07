Phase 159 pi4_3 trailing premise placement audit fix1

修正内容
========

前回 audit-only script の import 先が誤っていた。

誤:
- toda_group_proof_narrative_arguments
  - extract_toda_group_proof_narrative_argument_local_body_blocks

正:
- toda_group_proof_narrative_argument_local_body
  - extract_toda_group_proof_narrative_argument_local_body_blocks

production code
===============

変更なし。

test code
=========

変更なし。

pytest
======

実行しない。

確認内容
========

pi4_3 の

  pi3^2 = Z{eta2}

contribution について:

- placement
- provider_anchor
- distance_to_conclusion
- provider_keys
- provider_anchor_index
- insertion_index

を確認する。

全体テスト
==========

実行しない。

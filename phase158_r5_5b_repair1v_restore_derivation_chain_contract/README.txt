Phase 158-R5-5b repair1v — restore derivation-chain contract

目的
====
repair1u までの診断で確認した2つのローカル退行を一般則として修復する。

1. Multi-Argument local body
   - TARGET conclusion だけ dependency order を維持
   - ORDER 等は global blocks order に戻していた
   - これにより calculation chain が order statement / conclusion より後ろへ移動

2. Equation numbering
   - runtime は visible source だけ番号付け
   - derivation target は番号付けしない
   - これにより eq3 が plain のまま

さらに Phase 158 public equation-number normalization は
connector が参照する source tag だけを残していたため、
target tag を追加しても削除される。

修正
====
A. toda_group_proof_narrative_argument_multi_renderer.py

全 Argument について:
- extract_toda_group_proof_narrative_argument_local_body_blocks()
  が返す dependency order を維持
- method evidence にだけ存在する missing block は conclusion の直前へ挿入

TARGET / ORDER による特別分岐を削除。

B. toda_group_proof_narrative_equation_numbering.py

visible transition chain について:
- source steps を番号付け
- target step も番号付け
- display line order で連番化
- connector は source numbers を参照

C. toda_group_proof_narrative_renderer.py

_phase158_normalize_public_equation_numbers():
- connector が参照する source numbers を保持
- connector 直後の tagged derivation target number も保持
- その他の unreferenced / duplicate tag は従来どおり削除
- retained numbers を public body 上で連番化

群固有条件
==========
なし。

import changes
==============
なし。

Tests
=====
既存 canonical tests のみ使用。
新規・変更テストなし。

Focused pytest:
- Phase 143 generic dependency order
- Phase 144 equation numbering
- Phase 149 local-body ordering
- Phase 156 canonical relation/order
- Phase 157 reflexive/dangling cleanup
- Phase 158-R5-5b public ordering

repository-wide pytest:
実行しない。

完了条件
========
pi6^3:
eq1 -> eq2 -> connector -> eq3 -> ord(eta3^3)=2 -> ord(nu')=4

かつ:
- eq1 tag(1)
- eq2 tag(2)
- eq3 tag(3)

pi7^4 / pi15^8:
premise-before-target ordering を維持。

次 Phase 境界
============
repair1v は R5-5b の derivation-chain/order restoration のみ。
current registered groups の cross-audit は次の R5-5c。

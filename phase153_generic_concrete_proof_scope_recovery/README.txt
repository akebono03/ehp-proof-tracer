Phase 153 Generic Concrete Proof-Scope Recovery

目的
====
stable specialization を選ぶ前に、
repository proof scope 内に既存 concrete group proof がある場合は
その concrete proof を優先する。

今回の監査で確認済みの7群:
- pi_6^5
- pi_10^6
- pi_10^7
- pi_12^7
- pi_12^9
- pi_13^11
- pi_14^13

変更対象
========
toda_calculation.py

追加テスト
==========
tests/test_phase153_generic_concrete_proof_scope_recovery.py

一般規則
========
既存の選択順:
foundational
-> direct repository
-> low-dimensional
-> Proposition 5.9 dedicated concrete
-> stable specialization

変更後:
foundational
-> direct repository
-> low-dimensional
-> Proposition 5.9 dedicated concrete
-> existing generic concrete proof-scope result
-> stable specialization

候補選択
========
- query target と conclusion が一致
- source metadata を解決できる
- target conclusion が ancestry に再出現しない
- shortest_depth 最小
- 同 depth は root key / inference rule name で deterministic tie-break

source metadata
===============
containing root_entry ではなく、
selected ProofStep 自身の inference rule / literature source に基づく。

今回必要な canonical mapping:
- Toda Lemma 5.4 -> Phase 60
- Toda Proposition 5.8 -> Phase 68
- Toda Proposition 5.9 -> Phase 70
- Toda Proposition 5.11 -> Phase 73

Phase境界
=========
今回行わないもの:
- Reference selection の6つの n=2 群修正
- stable specialization 実装自体の変更
- sigma specialization の変更
- future Phase の一般化
- documentation closure
- full pytest

full pytest は Phase 153 の最後にのみ実行する。

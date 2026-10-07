Phase 159 pi4_3 repair5 lightweight verification

目的
====

repair5a で Phase 159 focused tests は 7 passed。

その後の regression command は、
Phase 144 の6群横断 fixture 構築中に KeyboardInterrupt となった。
これは assertion failure ではない。

ユーザー方針:
- 重いテストは作らない・不要に回さない。
- 全体テストは Phase 最後のみ。

したがって今回は重い Phase 144 横断 fixture を再実行せず、
直接関係する軽量確認だけを行う。

実行内容
========

1. Phase 157 dangling connector regression
   tests/test_phase157_r20_repair43_dangling_connector_cleanup.py

2. Phase 50 pi4_3 inference regression
   tests/test_phase50_pi4_3_finite_cyclic.py
   tests/test_phase50_pi4_3_exactness_bridge.py

3. current pi4_3 public Narrative を表示し、
   proof body で
   - final conclusion が1回
   - 「以上より, final conclusion」が存在
   を確認する。

production code
===============

変更なし。

test code
=========

変更なし。

この package は verification-only。

完了条件
========

- Phase 157 dangling connector tests PASS
- Phase 50 pi4_3 tests PASS
- proof_body_conclusion_count=1
- connected_final_conclusion=True

全体テスト
==========

実行しない。

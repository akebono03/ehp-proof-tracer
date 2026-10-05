Phase 158-R5-5b repair1k — pi6 tag-vs-plain diagnosis

背景
----
repair1j 後、Phase 156 canonical chain test は仍然 1件失敗。

失敗行:
rendered.index(equation_one)

したがって missing 対象は equation (1):

2 nu' = eta_3 eta_4 eta_5 tag(1)

目的
----
equation (1) が

A. 本文から消えた
B. plain では存在するが tag(1) だけ失われた

のどちらかを確定する。

同時に calculation block の各 step について、
repair1j の reflexive-equality helper 判定を表示する。

確認項目
--------
Public forms:
- eq1 tagged / plain
- eq2 tagged / plain
- connector (1),(2)
- connector (1)
- eq3 tagged / plain

Calculation step:
- rendered step
- reflexive=True/False

変更対象
--------
新規 audit bundle のみ。

Production code changes:
なし。

Existing tests changes:
なし。

repository-wide pytest:
実行しない。

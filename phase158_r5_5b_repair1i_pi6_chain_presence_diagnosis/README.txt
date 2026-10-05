Phase 158-R5-5b repair1i — pi6 calculation-chain presence diagnosis

背景
----
repair1h 後:

Phase 156 independent relation-side normalization:
- 3 passed
- 1 failed

失敗:
test_phase156_r6_repair2_public_chain_and_order_are_canonical

ValueError: substring not found

左右の distinct canonical sides 自体の focused test は PASS しているため、
relation-side normalization の方向は正しい。

目的
----
canonical public chain のどの要素が欠けているか確定する。

確認対象
--------
1. equation_one
   2 nu' = eta_3 eta_4 eta_5 tag(1)

2. equation_two
   eta_3 eta_4 eta_5 = eta_3^3 tag(2)

3. connector
   (1) と (2) より,

4. equation_three
   2 nu' = eta_3^3 tag(3)

5. order_statement
   ord(eta_3^3) = 2

各要素について:
- present
- index
- previous element より後か

を出す。

対象 surface
------------
A. multi-Argument renderer output
B. actual Web depth=2 proof body

変更対象
--------
新規 audit bundle のみ。

Production code changes:
なし。

Existing tests changes:
なし。

repository-wide pytest:
実行しない。

完了条件
--------
1. missing substring を一意に特定できる。
2. multi-Argument と actual Web の差を確認できる。
3. production code を変更しない。

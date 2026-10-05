Phase 158-R5-5b repair1m — relocation identity diagnosis

背景
----
repair1l の runner は最初に Phase 148 test file 全体を実行し、
5 failures で停止した。

分類:
- semantic-closure direct tests 3件:
  repair1l が変更していない領域。
  Phase 157 の map-property closure 追加後の stale / mixed-scope の可能性が高い。
- public numbered-chain tests 2件:
  repair1l の目的に直接関係する。
  tag(1) がまだ復元していないため、repair1l 仮説は不十分。

目的
----
ESTABLISH_ORDER Argument について、
direct premise / support step / transition source / relocatable identity を
実体で確認する。

確認内容
--------
A. order conclusion
B. direct premises
C. support steps
D. calculation transitions
E. order Argument local blocks
F. relocatable result

各 step について:
- object id
- statement type
- rendered line
- transition source か
- incoming transition source
- relocatable か

変更対象
--------
新規 audit bundle のみ。

Production code changes:
なし。

Existing tests changes:
なし。

repository-wide pytest:
実行しない。

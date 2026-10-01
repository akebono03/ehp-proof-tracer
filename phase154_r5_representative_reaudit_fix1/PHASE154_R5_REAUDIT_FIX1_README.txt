Phase 154-R5 Representative Re-audit Fix1

原因
----
初回 re-audit の `incomplete_reference_marker_lines: 15` は false positive。

検出された15行はすべて:

  **[R1] Proposition ...**

のような Reference section の見出しであり、proof body の不完全 marker ではない。

さらに pi6_3 / pi10_4 / pi12_5 / pi16_9 で reference_count=0 だったことから、
初回の section parser が route differences を正しく扱えていなかった。

Fix1
----
- `## 使用する結果` と `## 証明` を exact line heading で分割する。
- proof body 内であっても `**[R...` の Reference heading は incomplete marker から除外する。
- production code は変更しない。
- R5 linkage logic は変更しない。

R5 完了条件
-----------
- residual_linkage_candidates = 0
- incomplete_reference_marker_lines = 0

focused tests
-------------
37件相当の R5 current-contract focused set を再確認。

全体テスト
----------
実行しない。Phase 154 の最後にのみ実行する。

次の境界
--------
両指標が0なら Phase 154-R5 完了。
次は Phase 154-R6 punctuation normalization。

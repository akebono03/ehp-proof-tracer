Phase 154-R6 — Punctuation Audit

目的
----
Narrative prose の句読点混在を一般規則で修正する前に、
5代表群で現在の punctuation を分類する。

対象
----
- pi6_3
- pi10_4
- pi11_4
- pi12_5
- pi16_9
- Narrative
- depth 2

監査対象
--------
日本語 prose のみ。

分類:
- ASCII period 文末 `.`
- Japanese period 文末 `。`
- ASCII comma `,`
- Japanese comma `、`

除外:
- TeX / 数式内部
- display math only line
- Markdown heading
- Reference title:
  `**[R1] Proposition 5.8.**`

R6 の目標規則
-------------
- 日本語 Narrative prose の文末は `。`
- 日本語 Narrative prose の読点は `、`
- 数式内部の記号は変更しない
- 文献ラベルの英語 punctuation は変更しない
- 最終修正は post-render の blind replace ではなく renderer source で行う

production changes
------------------
なし。

focused tests
-------------
R5 current-contract と R2/R4/R8 の限定テストのみ。

全体テスト
----------
実行しない。Phase 154 の最後にのみ実行する。

次
--
audit 結果から punctuation の発生源をまとめ、
必要最小限の shared renderer-level change を R6 implementation として行う。

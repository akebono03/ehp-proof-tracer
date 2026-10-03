Phase157 R11-R8 — Reference filter trace audit

目的
====

R11-R7 repair1 の focused tests で以下を確認した。

- (5.3) の H(nu') = eta_5 が final public Reference に残っていない。
- Reference numbering が変わっている。
- body の nu' membership に [R#] が付いていない。
- historical R5/R9 test が brittle な R3 Proposition 5.6 marker に依存している。

R11-R8 は production/test code を変更せず、Reference pipeline の各段階を trace する。

監査対象
========

- filter_phase157_r3_pi6_3_reference_entries
- reference statement line construction
- exclude root reference
- filter by body usage
- restore fixed references after body usage
- earlier Proposition 5.6 restore

各段階で:
- R番号
- locator
- component_key
- rule name
- statement lines

を表示する。

最後に public Reference header と、
H(nu'), nu' membership, pi_6^5, H-surjectivity の行を表示する。

pytest は実行しない。
full repository pytest は Phase157 closure のみ。

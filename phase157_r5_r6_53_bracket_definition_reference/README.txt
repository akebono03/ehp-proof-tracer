Phase157-R5-R6 — Toda (5.3) bracket definition Reference

変更対象:
- toda_literature_statement_boundary.py
- tests/test_phase157_r5_r6_53_bracket_definition_reference.py

変更:
- (5.3) fixed component catalog に
  nu_prime_bracket_definition を追加。
- exact rule
  Toda 5.3 nu-prime Lemma 5.2 bracket specialization
  をその component に mapping。
- locator は (5.3)。

production import:
- 変更なし

class:
- 変更なし

production function/method:
- 変更なし
- catalog data の追加のみ

renderer:
- 変更なし

proof data:
- 変更なし

完了条件:
- (5.3) catalog が bracket definition を含む。
- specialization step が FIXED_STATEMENT と分類される。
- pi_6^3 の [R1] (5.3) に
  ν' ∈ {η_3, 2ι_4, η_4}_1
  が表示される。
- Lemma 5.2 application は本文に残る。

112群再監査と全体 pytest はこの step では行わない。

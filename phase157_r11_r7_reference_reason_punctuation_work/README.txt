Phase157 R11-R7 — Reference reasons and punctuation

変更対象
========

- toda_group_proof_narrative_references.py
  - filter_phase157_r3_pi6_3_reference_entries
- toda_group_proof_narrative_contribution_renderer.py
  - suppress_toda_group_proof_narrative_reference_body_duplicates
  - normalize_toda_group_proof_narrative_connectors
  - render_toda_group_proof_narrative_multi_argument_with_contributions_markdown
  - 新規 helper 3個
- toda_group_proof_narrative_reason_renderer.py
  - render_toda_group_proof_narrative_reason_sentence
- tests/test_phase157_r5_r9_fixed_definition_body_suppression.py
- tests/test_phase157_r11_reference_reason_punctuation.py

目的
====

- (5.3) の既存 fixed component `nu_prime_hopf_relation` を R1 に含める。
- Reference statement の本文再利用を `[R#]より, ...` と明示する。
- 証明本文先頭の `次に,` を `まず,` に正規化する。
- target group と Reference-backed Hopf value を H 全射性より前へ置く。
- 抽象的な FINAL_RESULT_DERIVATION filler を除く。
- 独立した数式・完全列の末尾を ASCII period `.` に統一する。
- `\square` には period を付けない。

全体 pytest は Phase157 closure まで実行しない。

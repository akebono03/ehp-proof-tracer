Phase 158-R5-5b repair1p — public wrapper tag-loss diagnosis

背景
----
repair1o:
- Phase 157 final reflexive suppression: 2 passed
- Phase 156 relation-side normalization:
  3 passed / 1 failed
- failing line remains equation_one tagged form

現行 public generic route:
1. render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()
2. _wrap_phase150_rc4_generic_public_narrative()
3. _finalize_toda_group_proof_narrative_markdown()
4. _phase158_normalize_public_narrative_contract()

wrapper 内では:
suppress_toda_group_proof_narrative_reference_body_restatements()

を再実行する。

目的
----
eq1/eq2/connector/eq3 の tagged/plain state を
各 public stage で比較し、
tag loss の最初の stage を特定する。

特に reference-body restatement suppression の
before/after を全文記録する。

変更対象
--------
新規 audit bundle のみ。

Production code changes:
なし。

Existing tests changes:
なし。

repository-wide pytest:
実行しない。

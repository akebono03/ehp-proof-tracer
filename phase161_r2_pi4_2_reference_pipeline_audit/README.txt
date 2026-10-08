Phase 161-R2
pi_4^2 Reference pipeline audit

目的
====
Phase 161-R1 で確認された次の不整合を追跡する。

- proof body には
    eta_2 o - : pi_i^3 -> pi_i^2
  が実際に使われている。
- literature boundary ではこの step は
    FIXED_STATEMENT / (5.2) / eta2_composition_isomorphism
  である。
- しかし final public Reference には Proposition 4.4 だけが残り、
  (5.2) が表示されない。

今回の監査
==========
production code を変更せず、current contribution renderer 内の
Reference pipeline helper を runtime wrapper で追跡する。

対象 helper
===========
- build_toda_group_proof_narrative_reference_entries
- filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary
- exclude_toda_group_proof_narrative_root_reference
- restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage
- filter_toda_group_proof_narrative_reference_entries_by_body_usage
- filter_toda_group_proof_narrative_reference_entries_by_step_usage
- render_toda_group_proof_narrative_reference_entries_markdown

期待する監査結果
================
(5.2) がどの helper の前後で消えるかを特定する。

注意
====
- audit-only
- production source changes: none
- full pytest は実行しない
- Phase 161-R3 の修正は R2 の消失点を確認してから行う

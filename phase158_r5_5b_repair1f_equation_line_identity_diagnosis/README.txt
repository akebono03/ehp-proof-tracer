Phase 158-R5-5b repair1f — equation line identity diagnosis

背景
----
repair1e で確認:

- B8 の3 calculation steps は A1 で全て VISIBLE
- B13 の3 calculation steps は A0 で全て VISIBLE
- seen_non_exact_step_ids による suppression が主原因ではない
- B8:
  2 nu' = eta_3^3
  2 nu' = eta_3^3
  eta_3^3 = eta_3^3
- B13:
  H(nu') = eta_5
  H(nu') = eta_5
  eta_5 = eta_5

目的
----
number_toda_group_proof_narrative_equations() が
step identity と rendered line をどのように対応付けているか直接確認する。

診断内容
--------
1. multi renderer 内から capture した raw Markdown に対して
   number_toda_group_proof_narrative_equations() を直接実行。
2. direct output と final output が同一か確認。
3. 各 numbering ProofStep について:
   - ProofStep id
   - plain line
   - numbered line
   - raw Markdown 上の occurrence indices
   - tag insertion が実際に line を変えるか
4. 複数 ProofStep が同じ rendered line を共有する場合を一覧化。
5. direct numbering 後の tag inventory を表示。

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
1. duplicate rendered lines と numbering step の対応が分かる。
2. direct numbering が本当に tag を付けていないか確認できる。
3. production code を変更しない。

Phase153-R3-5
Reference / Body Duplicate Suppression

目的
====
Phase153-R3-4 で Reference section に表示された representative statement と
本文側に再掲される同一 statement の重複だけを一般規則で抑制する。

変更対象
========
production:
- toda_group_proof_narrative_contribution_renderer.py
- toda_group_proof_narrative_renderer.py

tests:
- tests/test_phase153_r2_public_reference_semantic_fact.py
- tests/test_phase153_r3_5_reference_body_duplicate_suppression.py

一般規則
========
Reference section に実際に表示された statement_lines_by_reference_number を
唯一の suppress 対象とする。

1. 本文の独立行が representative statement と完全一致
   -> その行だけ除去する。

2. 本文行が同じ [Rn] marker と representative statement の両方を含む
   -> statement 部分を再掲せず、"[Rn]を用いる。" に縮約する。
   文頭の "まず、" "また、" などの prefix は保持する。

3. 類似していても完全一致しない statement
   -> suppress しない。

4. Reference section 自体
   -> suppress 対象外。

今回しないこと
==============
- semantic equivalence による重複判定
- unresolved 12 statement types の renderer 追加
- theorem-specific / group-specific branch
- full pytest

完了条件
========
- exact standalone duplicate が本文から消える
- [Rn] + exact statement の本文文が [Rn]を用いる。へ縮約される
- 非同一 statement は残る
- Reference section の statement は残る
- pi_10^6 public Narrative で R2 statement は Reference に1回表示され、
  本文は [R2]を用いる。になる
- 関連 regression tests が全て通る

次 Phase との境界
================
R3-5 は exact rendered duplicate suppression まで。
unresolved renderer の補完や semantic-equivalent duplicate suppression は
別 subphase として扱う。

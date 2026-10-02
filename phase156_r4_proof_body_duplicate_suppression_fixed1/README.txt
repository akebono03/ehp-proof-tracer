Phase156-R4 — proof-body duplicate suppression

変更対象
========
1. toda_group_proof_narrative_contribution_renderer.py
   新規関数:
   suppress_toda_group_proof_narrative_reference_body_restatements()

   追加位置:
   suppress_toda_group_proof_narrative_reference_body_duplicates()
   の直前。

2. toda_group_proof_narrative_renderer.py
   import:
   suppress_toda_group_proof_narrative_reference_body_restatements
   を追加。

   変更関数:
   _phase153_r3_10_connect_public_reference_section()
   _wrap_phase150_rc4_generic_public_narrative()

3. 新規 focused test:
   phase156_r4_proof_body_duplicate_suppression/
   test_phase156_r4_body_restatement_suppression.py

4. 新規 audit:
   phase156_r4_proof_body_duplicate_suppression/audit_phase156_r4.py

目的
====
通常 route では既存 duplicate suppression が動作しているが、
public Reference connection route と generic public wrapper route では
同じ抑制が適用されていなかった。

R4 では全 public Reference route に対して、
Reference に既に表示されている statement の単純再掲だけを抑制する。

残すもの
========
次のような derivation / calculation context を持つ本文は残す。

- これらから
- このことから
- したがって
- よって
- 計算
- 導く
- 得る
- 従う
- 示す
- 確認

したがって Reference 側を短くするために、
数学的な導出本文を削除する変更ではない。

R4 で変更しないもの
===================
- Phase156-R3 Reference statement selector
- 既存 suppress_toda_group_proof_narrative_reference_body_duplicates()
- Reference theorem / lemma selection
- proof graph / proof data
- stable range
- repository-wide pytest

実行テスト
==========
Focused:
- Phase156-R4 new helper tests
- Phase154-R2 marker completion
- Phase153-R8 Reference-use prose normalization

Audit-only:
- Phase153-R3-10 all-group Reference population invariant

112-group audit:
- suppressible exact Reference/body restatements = 0
- derivation context 内の exact occurrence は許可し、件数を記録する
- exceptions = 0

Phase 完了条件
==============
- focused tests PASS
- audit-only regression PASS
- 112 groups
- exceptions = 0
- suppressible exact restatements = 0

次 Phase との境界
=================
Phase156-R5 で112群を横断して Reference minimal display 全体を監査する。
R4 では proof-body duplicate suppression のみを扱う。


Fixed1
======
初版の production change と focused tests は変更しない。

初版 112-group audit は public Reference section 内のすべての非空行を
Reference statement と誤認していた。
特殊 route では `\[`、`\]`、説明文なども Reference section に含まれるため、
これらが proof body に現れるだけで exact restatement と誤検出された。

Fixed1 では:
1. semantic closure presentation から canonical selected statements を取得する。
2. public Reference section に実際に表示されている行のうち、
   canonical selected statement と一致するものだけを監査対象にする。
3. `\[`、`\]`、section prose、hand-written display scaffolding は対象外とする。
4. proof body との exact duplicate 判定規則自体は変更しない。

変更:
- audit_phase156_r4.py
- runner の package path

変更しないもの:
- R4 production patch
- focused tests
- existing tests
- Phase156-R3 selector

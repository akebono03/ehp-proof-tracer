Phase156-R5 repair3 — generic final Reference suppression

変更対象
========
Production:
- toda_group_proof_narrative_contribution_renderer.py

変更関数:
- render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

import 変更:
- なし

変更内容
========
Reference filtering 完了後、
Reference section を付与する直前に

suppress_toda_group_proof_narrative_reference_body_restatements()

を最終適用する。

これにより generic route で filtering / linkage の後に残る
canonical Reference statement の本文再掲を一般規則で抑制する。

対象となることが確認された群:
- pi_6^3
- pi_10^4
- pi_12^5
- pi_16^9

R5 audit contract
=================
必須:
- Reference entry header は連番
- body `[R#]` marker には対応 header がある
- R3 minimal selection invariant
- suppressible exact Reference/body restatement = 0

必須にしない:
- すべての Reference header が本文で `[R#]` marker を持つこと

理由:
generic renderer は marker ではなく proof graph usage によって
Reference を保持する経路を正式に持つため。

header-without-marker は informational として件数のみ記録する。

変更しないもの
==============
- Phase156-R3 selector
- Reference theorem / lemma selection
- proof data
- stable range
- existing tests
- documents

テスト
======
Focused:
- 4 generic route groups の exact selected-statement/body duplicate = 0
- existing Phase154-R2
- existing Phase153-R8

Audit-only:
- Phase153-R3-10 public Reference population invariant

112-group audit:
- exceptions = 0
- all required violations = 0

repository-wide pytest は実行しない。

次 Phase
========
PASS 後:
Phase156-R6 — focused/sharded regression

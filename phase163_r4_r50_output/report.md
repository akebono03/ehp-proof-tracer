# Phase 163 R4-R50 数学的役割の限定監査

TeX 第1〜5章の既存108登録環境と ID は変更していない。

## 判定状況

- AUXILIARY_CONTEXT: 6件
- CLAIM_IN_PROSE: 1件
- DEFINITION_CANDIDATE: 13件
- DEFINITION_COMPONENT: 4件
- EXISTING_STATEMENT_CONTEXT: 1件
- LEXICALLY_EXCLUDED: 34件
- PENDING_MATHEMATICAL_REVIEW: 253件
- PROOF_LOCAL_CONSTRUCTION: 4件

- 前後文脈を確認した候補: 29件
- 数学的判定を保留した候補: 253件
- 独立した新規命題として確定した件数: 0件

## 判定の境界

DEFINITION_CANDIDATE は定義として登録するための候補であり、本番登録や原本照合の完了を意味しない。
DEFINITION_COMPONENT は同一の定義に付随する表示式で、別登録を意味しない。
CLAIM_IN_PROSE は文中の主張であり、独立した文献命題として登録するかは未決定。
PROOF_LOCAL_CONSTRUCTION と AUXILIARY_CONTEXT は限定された文脈に基づく役割の判断である。
残りの数学的判断を行っていない数式は PENDING_MATHEMATICAL_REVIEW のまま保持する。
第3章の安定群 G_k、第5章の他の生成元定義は20件の文章検出には必ずしも含まれず、表示式候補の監査で補完が必要。

Registry・TeX・既存 catalog・Statement ID・証明探索は変更しない。全体 pytest は未実施。

Phase156-R5 repair4 — Reference/body ownership diagnostic

Production changes
==================
なし。

repair3 の失敗
==============
repair3 は R4 の
suppress_toda_group_proof_narrative_reference_body_restatements()
を generic renderer の最終段階に適用した。

しかしこの helper は
「したがって」「このことから」などを含む statement を
derivation context として意図的に保持する。

実際:
- pi_6^3: ord(nu') = 4 が「したがって」の後に残る
- pi_10^4: pi_9^3 = 0 が証明本文に残る

したがって本文を一律に削除する修正は不適切。

今回の診断
==========
4群の selected Reference statement ごとに以下を取得する。

- fact_role
- block_role
- argument conclusion か
- narrative block に含まれるか
- same-entry consumer 数
- entry-external consumer 数
- different-reference consumer 数
- 本文 occurrence と前後文脈

対象
====
- pi_6^3
- pi_10^4
- pi_12^5
- pi_16^9

次の判断
========
A. proof-body-owned
   本文で実際に導出される statement。
   Reference 側の表示候補から外す方向を検討する。

B. Reference-owned
   外部結果として使う statement。
   Reference に残し、本文を marker 利用にする方向を検討する。

C. aggregate / mixed
   複合 statement の一部だけが本文で使われる。
   aggregate component selection の既存一般規則を使う。

この分類前には production code を変更しない。

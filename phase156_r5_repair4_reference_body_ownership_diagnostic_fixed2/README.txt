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


Fixed1
======
初版診断には2点の問題があった。

1. pi_6^3 raw generic route では `## 証明` が無いため、
   Reference prefix 内の selected statements を body occurrence と誤認した。
2. pi_10^4 / pi_12^5 / pi_16^9 の例外内容を画面に表示していなかった。

Fixed1:
- `## 証明` がある場合はその直後を proof body start とする。
- `## 証明` が無く `# Group proof narrative` がある場合は、
  その直後を proof body start とする。
- Reference prefix は body occurrence から除外する。
- 例外が発生した場合、group / exception type / message を画面に表示する。
- production changes はなし。


Fixed2
======
Fixed1 で残った3例外:
- pi_10^4
- pi_12^5
- pi_16^9

原因:
diagnostic が古い
classify_toda_group_proof_narrative_step()
を使っていた。
この classifier は pi_6^3 と pi_8^5 だけを対象とする。

Fixed2:
- 全群対応の recognize_toda_group_proof_narrative_step_role()
  を semantic_sidecar 付きで使用する。
- fact_role / legacy block_role は診断対象から外し、
  mathematical_block_role を記録する。
- raw generic route は canonical Reference section が先頭 prefix と一致する場合、
  その直後からを proof body とする。
- `## 証明` がある route はその直後からを proof body とする。
- production changes はなし。

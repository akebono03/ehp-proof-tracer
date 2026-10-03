Phase156-R7 repair1 — multiple H-surjective ownership audit

Production changes: none.

前回 R7 audit の停止原因
========================

pi_6^3 presentation 内に

$$
H:\pi_6^3\to\pi_6^5
$$

の surjective step が 2 件存在した。

前回 audit は `_find_unique()` で exactly one を要求していたため、

`expected exactly one step, found 2`

で停止した。

これは production failure ではない。
むしろ R7 が調べたい ownership / duplicated derivation candidate を
示す監査対象そのものである。

repair1
=======

H-surjective step についてのみ unique 前提を外し、
一致する全候補を列挙する。

各候補について:

- depth
- rendered statement
- statement type
- inference rule
- literature reference
- direct premises
- direct consumers

を表示する。

その他の監査対象は前回 R7 と同じ。

- pi_5^2
- pi_5^3
- pi_6^5
- E: pi_4^2 -> pi_5^3 isomorphism
- root Reference exclusion 前後
- Proposition 5.1 aggregate higher eta result

目的
====

次の実装前に、以下を確定する。

1. pi_5^2 が Proposition 5.6 sibling result として
   root-reference exclusion で落ちているか。

2. pi_6^5 が現在 Lemma 5.4 に誤帰属しているか。

3. H-surjective の 2 candidate が
   同一 conclusion の別 derivation なのか、
   Reference-backed step と derived step の重複なのか。

4. E: pi_4^2 -> pi_5^3 isomorphism が
   Proposition 5.3 proof-internal derived fact として
   どの premises から生成されているか。

Repository-wide pytest は Phase156 closure でのみ実行する。

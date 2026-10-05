Phase157 R11-R13 — dependency and Reference usage audit

前提:
- R11-R11 repair7 focused pytest: 59 passed.
- Hopf chain ordering / Reference punctuation は focused test 上は安定。

残っている公開 Narrative の問題候補:
1. ord(eta_3^3)=2 が E injective より前に表示されている。
2. short exact sequence を述べる時点で H surjective の証明が後ろにある。
3. [R3] Proposition 5.3 が本文で実際に使われているか不明。

この audit は production/test code を変更しない。

出力:
- ord(eta_3^3)=2 / E injective / H surjective / pi_6^5 group の direct premises
- Reference entry ごとの outgoing consumers
- public body の paragraph order
- body 内 [R1]/[R2]/[R3]/[R4] 出現回数

pytest は実行しない。
full repository pytest は Phase157 closure まで実行しない。

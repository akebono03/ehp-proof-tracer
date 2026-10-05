Phase157 R11-R10 — Hopf chain semantic-closure audit

R11-R9 で確認:
- H: pi_6^3 -> pi_6^5 surjective の直接前提は
  1. equality transitivity による H(nu') = eta_5
  2. Proposition 5.1 aggregate
- raw presentation には equality-transitivity step が入っていない。
- (5.3) fixed component は H(nu') = E^2 eta_3。
- H(nu') = eta_5 は derived equality。

今回の監査:
- raw presentation と semantic closure 後を比較。
- surjectivity step の direct premise を表示。
- equality-transitivity step の direct premises も表示。
- 各 step が raw / closure のどちらに含まれるか表示。
- closure が追加した node を全表示。

目的:
renderer special-case ではなく、
semantic closure の generic rule で修正可能か判断する。

production/test code は変更しない。
pytest は実行しない。

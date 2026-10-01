Concrete Proof-Scope Candidate Structure Audit

目的
====
pi_10^6 = 0 と pi_12^7 = 0 について、
production repository proof scope 内にある同一 conclusion の複数 node から、
canonical base-case proof と同じ構造を持つ node を特定する。

production changes
==================
なし。

tests changes
=============
なし。

structural_base_match
=====================
以下を両方満たすもの:

1. inference rule name が canonical base-case と同じ
2. ordered premise conclusions が canonical base-case と同じ

object identity は要求しない。

理由
====
test builder と production repository builder は別々に ProofStep を生成するため、
数学的・構造的に同じ proof でも object identity は一致しない。

期待結果
========
pi_10^6:
  target-matching nodes = 6
  structural base match = 1

pi_12^7:
  target-matching nodes = 2
  structural base match = 1

これが確認できれば、
stable specialization より前に existing concrete proof-scope result を
優先する一般規則を検討できる。

出力
====
output/
- candidate_structure_summary.txt
- candidate_structure_summary.csv
- candidate_inventory.csv
- exception_inventory.csv

full pytest は実行しない。

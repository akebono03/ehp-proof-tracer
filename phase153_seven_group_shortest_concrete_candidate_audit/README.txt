7-Group Shortest Concrete Candidate Audit

目的
====
112-group concrete-before-specialization audit で見つかった7群について、
現在選択される stable specialization と、
specialization 前 proof scope に存在する最短 concrete proof を比較する。

対象
====
- pi_6^5
- pi_10^6
- pi_10^7
- pi_12^7
- pi_12^9
- pi_13^11
- pi_14^13

production changes
==================
なし。

tests changes
=============
なし。

確認項目
========
各群について:

current selected stable specialization
- source key
- rule
- literature reference
- premise count
- 同じ target conclusion が ancestry に再出現するか
- specialization shape か

shortest concrete candidate
- root entry
- depth
- theorem / phase
- inference rule
- literature reference
- premise count
- direct premise の rule / reference
- 同じ target conclusion が ancestry に再出現するか

さらに全 concrete candidate も inventory する。

判断基準
========
shortest concrete candidate が一般選択候補として安全なのは、
少なくとも次を満たすこと:

1. target conclusion が一致
2. theorem / lemma 固有の inference rule を持つ
3. 実際の premise を持つ
4. target conclusion 自身を ancestry に含まない
5. stable specialization の薄い wrapper ではない

出力
====
output/
- seven_group_shortest_candidate_report.txt
- seven_group_summary.csv
- shortest_candidate_premises.csv
- all_concrete_candidates.csv
- exception_inventory.csv

full pytest は実行しない。

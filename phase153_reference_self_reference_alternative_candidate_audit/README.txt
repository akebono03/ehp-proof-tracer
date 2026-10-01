Reference Self-Reference Alternative Candidate Audit

目的
====
前回の112-group auditで確認した8件の自己参照 Reference について、
自己参照候補を除外した後に何が残るかを監査する。

production changes
==================
なし。

tests changes
=============
なし。

監査内容
========
各 defect Reference entry について:

1. 現在の selected candidate を確認。
2. root step 自身を除外。
3. root conclusion と同一の conclusion を持つ candidate を除外。
4. 残った candidate に現行 selection rule を適用。
5. alternative selected candidate が存在するか確認。
6. affected target の direct root premises も別CSVに出力。

出力
====
output/
- alternative_candidate_summary.txt
- affected_groups.csv
- defect_reference_entries.csv
- candidate_inventory.csv
- direct_root_premises.csv
- exception_inventory.csv

重要
====
この監査は alternative candidate の「存在」を調べるだけ。
その candidate が数学的に適切かはまだ決めない。

特に same-source-theorem candidate は、
同一 Proposition 内の先行事実か、
単なる別形式の完成結果かを次段階で確認する必要がある。

full pytest
===========
実行しない。

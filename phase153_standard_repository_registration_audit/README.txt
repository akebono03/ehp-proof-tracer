Standard Repository Registration Audit

目的
====
pi_10^6 = 0 と pi_12^7 = 0 について、
canonical concrete base-case proof が存在するにもかかわらず、
Standard group query が symbolic stable zero specialization を
proof root として選んでいる原因を確認する。

production changes
==================
なし。

tests changes
=============
なし。

監査対象
========
- standard_production_repository
- repository proof scope
- find_normalized_toda_group_results
- _find_specialized_stable_toda_group_results
- build_standard_toda_report

確認事項
========
1. canonical base-case step は proof scope 内に存在するか。
2. その step は direct repository group result として登録されているか。
3. symbolic general zero step は proof scope 内に存在するか。
4. stable specialization が query target と一致する concrete step を追加するか。
5. build_standard_toda_report が最終的にどの source key / proof step を選ぶか。

想定される原因
==============
canonical concrete base-case:
  repository proof scope 内には存在
  しかし direct repository entry ではない

そのため:
  find_normalized_toda_group_results -> 0
  stable specialization -> concrete zero を追加
  group query -> specialization step を選択

この場合、proof の数学的内容ではなく
group-result source registration / selection policy の問題。

出力
====
output/
- registration_summary.txt
- registration_comparison.csv
- matching_scope_nodes.csv
- specialization_nodes.csv
- exception_inventory.csv

full pytest
===========
実行しない。

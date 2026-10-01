Eight-Group Direct Root Premise Audit

目的
====
自己参照 Reference が確認された8群について、
root conclusion が実際に何を直接前提として導かれているかを確認する。

対象
====
- pi_4^2
- pi_5^2
- pi_6^2
- pi_7^2
- pi_8^2
- pi_9^2
- pi_10^6
- pi_12^7

depth=2
semantic closure

production changes
==================
なし。

tests changes
=============
なし。

確認項目
========
各 root について:

- root statement
- root inference rule
- root literature reference
- direct premise の statement
- direct premise の statement type
- direct premise の inference rule
- direct premise の literature reference
- direct premise の depth
- direct premise がさらに何を premise に持つか

premise_class
=============
literature_backed
  direct premise 自身に literature reference がある。

derived_without_literature_reference
  inference rule で導出されているが literature reference はない。

given_or_unreferenced
  GIVEN 等で、literature reference がない。

self_reference / self_reference_equal_conclusion
  root 自身または root conclusion と同一。
  本来 direct premise として出れば構造上の問題。

出力
====
output/
- direct_root_premise_report.txt
- roots.csv
- direct_root_premises_detailed.csv
- second_level_premises.csv
- exception_inventory.csv

次
==
この結果から、
Reference を theorem entry 単位ではなく
actual proof ancestry（実際の証明祖先）から構成すべきかを判断する。

full pytest は実行しない。

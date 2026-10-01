Base-Case / Repository Root Direction Audit

目的
====
pi_10^6 = 0 と pi_12^7 = 0 について、
現行 Standard Repository の group proof root と、
Phase68 / Phase70 の canonical base-case derivation を比較する。

production changes
==================
なし。

tests changes
=============
なし。

確認対象
========
pi_10^6
- canonical base:
  test_phase68_pi_n_plus_4_n_zero.build_phase68_10_data()["pi10_6_zero_step"]
- canonical general:
  build_phase68_10_data()["final_step"]

pi_12^7
- canonical base:
  test_phase70_pi_n_plus_5_n_zero.build_phase70_9_data()["pi12_7_zero_step"]
- canonical general:
  build_phase70_9_data()["higher_zero_step"]

確認事項
========
正しい方向は、

base case
  ↓
Toda (4.5) + range condition
  ↓
general stable zero

である。

したがって canonical base ancestry には、
Toda (4.5) と n>=6 / n>=7 は入らないはずである。

一方 canonical general transport は、
base case + Toda (4.5) + range condition
を前提とするはずである。

Standard Repository root が、
base-case conclusion を持ちながら
general transport を経由して base case に戻っている場合、
repository proof root の wiring が逆向きである。

出力
====
output/
- base_case_direction_report.txt
- comparison.csv
- ancestry_inventory.csv
- exception_inventory.csv

full pytest
===========
実行しない。

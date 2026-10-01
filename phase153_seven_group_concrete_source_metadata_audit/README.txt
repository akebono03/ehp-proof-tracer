7-Group Concrete Source-Metadata Audit

目的
====
shortest concrete candidate を generic concrete recovery で採用するとき、
ProofRepositoryEntry の source metadata をどこから取得すべきか確認する。

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

監査内容
========
各 shortest concrete candidate について:

- containing root_entry.key
- containing root_entry.phase
- containing root_entry.theorem
- proof step inference rule
- proof step literature reference
- literature reference から解決される canonical phase / theorem
- root metadata と canonical metadata が一致するか

canonical metadata
==================
この監査では既存 project history に基づく以下を使用する。

- Toda Lemma 5.4 -> Phase 60
- Toda Proposition 5.8 -> Phase 68
- Toda Proposition 5.9 -> Phase 70
- Toda Proposition 5.11 -> Phase 73

重要な区別
==========
root_entry metadata:
  その proof step を現在包含している repository tree

step literature reference:
  その proof step 自身の数学的出典

例えば Proposition 5.9 の step が
standard.toda.prop511 tree 内に存在しても、
その step 自体の source theorem は Proposition 5.9 である。

generic concrete recovery では、
step literature reference に canonical metadata が存在する場合、
phase/theorem はその metadata から復元するのが候補。

key は containing root_entry を流用せず、
recovered concrete query result を表す独立 key とする候補を監査する。

出力
====
output/
- source_metadata_report.txt
- source_metadata_audit.csv
- exception_inventory.csv

full pytest は実行しない。

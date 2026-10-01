112-Group Concrete-Before-Specialization Audit

目的
====
n=2..15, k=0..7 の112群について、

現在の Group query が
standard.toda.stable::*_specialization
を選んでいるにもかかわらず、

specialization 前の repository proof scope に
同じ concrete target conclusion を証明する ProofStep が
既に存在するケースを全件監査する。

production changes
==================
なし。

tests changes
=============
なし。

confirmed case
==============
以下を両方満たす群:

1. build_standard_toda_report() の selected source key が
   standard.toda.stable::*_specialization
2. specialization 前の build_repository_proof_scope() に
   query.target と一致する concrete group-result conclusion が存在

これは pi_10^6 / pi_12^7 で確認した
「既存 concrete proof より stable specialization が優先された」
パターンを112群へ一般監査するもの。

各 confirmed case について出力
===============================
- selected stable specialization source
- pre-specialization concrete candidate 数
- 最短 concrete depth
- 最短 candidate の root entry
- 最短 candidate の inference rule
- 全 concrete candidate inventory

出力
====
output/
- concrete_before_specialization_summary.txt
- defect_groups.csv
- concrete_candidate_inventory.csv
- all_112_group_inventory.csv
- exception_inventory.csv

注意
====
この監査ではまだ selection rule の実装修正は行わない。
shortest-depth candidate を採用すべきか、
source theorem / literature provenance をどう復元するかは
監査結果を確認してから決める。

full pytest は実行しない。

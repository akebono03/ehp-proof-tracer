Reference Self-Reference Audit
112 Groups

目的
====
Reference candidate selection が、
証明対象そのものを Reference として選んでいないかを
112 groups 全体で監査する。

対象
====
n=2..15
k=0..7
合計112 groups
depth=2
semantic closure

production changes
==================
なし。

tests changes
=============
なし。

分類
====
1. selected_root_step_identity
   selected Reference step が root step 自身。
   confirmed self-reference defect。

2. selected_root_conclusion_equal
   step identity は異なるが、
   selected conclusion == root conclusion。
   confirmed self-reference defect。

3. selected_aggregate_contains_root_conclusion
   selected aggregate dataclass の内部に
   root conclusion がそのまま含まれる。
   confirmed self-reference defect。

4. same_source_theorem_only
   source theorem と同じ theorem の Reference だが、
   上記3条件には該当しない。
   suspicious だが、この監査では confirmed defect に数えない。

5. not_self_reference
   上記に該当しない。

出力
====
output/
- self_reference_summary.txt
- self_reference_defects.csv
- selected_reference_steps.csv
- group_inventory.csv
- exception_inventory.csv

注意
====
この監査は「数学的に不適切な Reference selection」の件数把握だけを行う。
修正は行わない。

same_source_theorem_only は、
同一 Proposition 内の別の先行事実を正当に使っている可能性があるため、
自動的には defect と判定しない。

次
==
監査結果を見て、
- root/self conclusion の除外規則
- aggregate target containment の除外規則
- same-theorem Reference の追加監査
を分けて検討する。

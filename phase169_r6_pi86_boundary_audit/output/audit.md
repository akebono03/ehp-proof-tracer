# Phase 169 R6 — π₈⁶ 輸送経路の原因切り分け

- pi86_target_citation: `shared:0:boundary:Proposition 5.3:higher_eta_squared_group_relation`
- screened_toda45: `True`
- screened_pi64_given: `False`
- screened_pi75_given: `False`
- existing_r3o_options: `0`
- existing_r5b_options: `0`
- existing_r57_options: `0`
- goal_only_one_step_options: `1`
- goal_only_two_step_options: `0`
- two_step_iso_specializable: `True`
- two_step_db_generator_equals_iterated_expression: `False`
- pi86_status: `partial`
- pi86_steps: `2`
- pi86_open_goals: `7`
- web_key: `generic-partial-proof`
- web_partial: `True`

## prior_pi64
- eligible: `True`
- reason: `prior_fixed_source`
- source_assertion_id: `shared:0:boundary:Proposition 5.3:pi6_4_group_relation`
- relation_available_as_db_goal: `True`

## prior_pi75
- eligible: `False`
- reason: `source_not_prior`
- source_assertion_id: `shared:0:boundary:Proposition 5.3:higher_eta_squared_group_relation`
- relation_available_as_db_goal: `True`

## 境界

Goal-only は探索候補の診断に限る。ProofStep は生成せず、既存 Provider も変更しない。
DB の群構造を GIVEN に昇格させず、Toda (4.5) の適用範囲も変更しない。
この監査では全体 pytest を実行しない。

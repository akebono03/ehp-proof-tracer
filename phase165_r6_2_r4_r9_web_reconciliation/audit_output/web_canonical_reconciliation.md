# R4-R9 正規探索・Web 結果照合

状態: `WEB_CANONICAL_RECONCILIATION_AUDITED`

目標候補: 1、型付き主張: 201、リンク: 17

## partial_web_adapter

- 呼出成功: True
- 概要: `{'partial_result': True, 'step_count': 0, 'rendered_line_count': 14}`

## narrative_model

- 呼出成功: True
- 概要: `{'status': 'ProofSearchStatus.SEARCH_FAILED', 'step_count': 0, 'root_step_present': False, 'source_kind': 'search_result'}`

## web_search_entry

- 呼出成功: True
- 完成: False
- 状態: ProofSearchStatus.SEARCH_FAILED
- ProofStep: 0
- 診断: ["expected one registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_3', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None), found 0"]
- 未解決: 2

## shared_direct_no_order

- 呼出成功: True
- 完成: False
- 状態: ProofSearchStatus.SEARCH_FAILED
- ProofStep: 0
- 診断: ["expected one registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_3', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None), found 0"]
- 未解決: 2

## public_web_entry

- 呼出成功: True
- 概要: `{'partial_result': True, 'step_count': 0, 'rendered_line_count': 14, 'key': 'generic-partial-proof'}`

## proof_order

- 呼出成功: True
- 利用順序診断: None

## 判定の限界

この監査は既存の実行経路の出力を照合するのみで、証明済みの結論や Reference を新規生成しません。
各呼出の検証条件や表示内容が一致したことをもって数学的証明の成立を追加認定しません。
全体 pytest は実行していません。

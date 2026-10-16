# R4-R10 候補から ProofStep までの追跡

候補数・前提の解決・推論照合・採用の各段階を調査します。

```json
{
  "status": "CANDIDATE_TRACE_AUDITED",
  "goal_count": 1,
  "traces": {
    "full_bridge": {
      "root_candidate_count": 1,
      "all_status": "CANONICAL_UNRESOLVED",
      "root_statuses": [
        "CANONICAL_UNRESOLVED"
      ],
      "match_calls": 0
    },
    "screened_bridge": {
      "root_candidate_count": 1,
      "all_status": "CANONICAL_UNRESOLVED",
      "root_statuses": [
        "CANONICAL_UNRESOLVED"
      ],
      "match_calls": 0
    }
  },
  "shared_direct": {
    "status": "ProofSearchStatus.SEARCH_FAILED",
    "complete": false,
    "proven_steps": 0,
    "diagnostics": [
      "expected one registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_3', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None), found 0"
    ]
  },
  "web_search": {
    "status": "ProofSearchStatus.SEARCH_FAILED",
    "complete": false,
    "proven_steps": 0,
    "diagnostics": [
      "expected one registered derivation for Relation(lhs=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3), rhs=FiniteCyclicGroup(order=2, generator=HomotopyElement(name='η_3', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None), found 0"
    ]
  },
  "production_modified": false,
  "full_pytest_run": false
}
```

詳細は candidate_trace.json を参照してください。

監査は既存 API を呼び、ファイルを書き換えません。実行中の関数置換は finally 節で復元します。
ルートを1候補に絞る診断は本番の選択方針を変更するものではありません。
全体 pytest は実行していません。

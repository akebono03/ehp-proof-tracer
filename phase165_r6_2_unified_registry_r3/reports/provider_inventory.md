# Phase 165 R6-2 統一規則台帳 R3：非R8経路の棚卸し

- 状態: `INVENTORY_ONLY`
- 本番コード変更: なし
- 推論・証明の実行検証: なし

## 共通 Provider の静的接続箇所

| symbol | connection | 行 |
|---|---|---:|
| `expand_registered_toda45_finite_cyclic_goal` | DIRECT_OPTIONS_EXTEND | 163 |
| `expand_registered_eta_specialization` | DIRECT_OPTIONS_EXTEND | 164 |
| `expand_registered_delta_image_goal` | DIRECT_OPTIONS_EXTEND | 165 |
| `expand_cited_general_specialization` | DIRECT_OPTIONS_EXTEND | 166 |
| `expand_delta_zero_from_suspension_iso` | PROVIDER_LOOP_MEMBER | 167 |
| `expand_diagonal_suspension` | PROVIDER_LOOP_MEMBER | 167 |
| `expand_generic_ehp_hopf_goal` | PROVIDER_LOOP_MEMBER | 167 |
| `expand_generic_iso_goal` | PROVIDER_LOOP_MEMBER | 167 |
| `extra_providers` | PROVIDER_LOOP_DYNAMIC | 167 |
| `provider(goal)` | PROVIDER_LOOP | 174 |
| `witness_options` | MERGE_PATH | 188 |
| `generic_provider` | MERGE_PATH | 189 |
| `seeded_options` | MERGE_PATH | 200 |

## R8以外の expand_ 系関数候補

検出数: 22

これらは関数名による候補であり、一般規則や到達可能な Provider と認定したものではない。

## 次段階

各接続箇所に対して Rule/Provider の分類、実行条件、入力証人、逆向き生成能力を検証してから統一台帳に登録する。

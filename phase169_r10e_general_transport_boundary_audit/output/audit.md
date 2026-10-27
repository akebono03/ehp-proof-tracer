# Phase 169 R10E0: 型付き輸送の共通境界監査

AUDIT_ONLY：本番コード・既存テストを変更しない。
DB の目標候補は引用可能な数学的証明とは区別する。

| 群 | Goal 型 | R7 直接適用 | 先行安定範囲 | 引用に適格な先行 DB 結果 |
|---|---|---|---|---|
| `pi_12^8` | zero_group | no | yes | 0 |
| `pi_14^8` | finite_cyclic | yes | no | 0 |
| `pi_22^15` | finite_cyclic | yes | yes | 0 |
| `pi_23^15` | direct_sum | no | yes | 0 |
| `pi_24^15` | direct_sum | no | yes | 0 |

## 監査の解釈

- `finite_cyclic` 以外では、現行 R7 は根 Goal を直接展開しない。
- 最初の安定次元 `n=k+2` には、それより低次元の安定な輸送元がない。
- 先行 DB 結果は、掲載順が適格であっても自動的な証明済み GIVEN ではない。
- `visible_general_family_ids` は引用審査で残った系列定義の ID。
- 詳細は同じフォルダの audit.json を参照。

全体 pytest は実行していない。

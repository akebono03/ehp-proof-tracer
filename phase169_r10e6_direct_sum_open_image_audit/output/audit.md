# Phase 169 R10E6 — 直和群の未解決生成元像監査

AUDIT_ONLY：既存コード・既存テスト・証明台帳は変更しない。

- Git HEAD: `c61bfaa72b75121c256518fbe37c7e8e27e5f815`
- 監査は探索結果の観測であり、新規証明または Trust Boundary の代用ではない。
- 生成元の DB 名称や型一致は懸垂像の証明ではない。

## pi_23^15

- 探索状態: `partial`
- 安定基点: `pi_18^10`（DB 行: True、先行前提: True）
- 未解決目標: GeneratorImage, Relation, Relation
- 審査済み系列定義 ID: [4, 9]

期待される懸垂像: 10 件

| 成分 | 基点生成元 | 輸送先生成元 | INFERENCE として観測 | 期待数 |
|---|---|---|---:|---:|
| 1 | `ν̅₁₀` | `ν̅₁₅` | 0 | 5 |
| 2 | `ε₁₀` | `ε₁₅` | 0 | 5 |

### 未導出の画像条件

- 成分1・第1回: `ν̅₁₀` → `ν̅₁₁` (exact open=True; family_id=11; cited proposals=0; composition proposals=0)
- 成分1・第2回: `ν̅₁₁` → `ν̅₁₂` (exact open=False; family_id=11; cited proposals=0; composition proposals=0)
- 成分1・第3回: `ν̅₁₂` → `ν̅₁₃` (exact open=False; family_id=11; cited proposals=0; composition proposals=0)
- 成分1・第4回: `ν̅₁₃` → `ν̅₁₄` (exact open=False; family_id=11; cited proposals=0; composition proposals=0)
- 成分1・第5回: `ν̅₁₄` → `ν̅₁₅` (exact open=False; family_id=11; cited proposals=0; composition proposals=0)
- 成分2・第1回: `ε₁₀` → `ε₁₁` (exact open=False; family_id=10; cited proposals=0; composition proposals=0)
- 成分2・第2回: `ε₁₁` → `ε₁₂` (exact open=False; family_id=10; cited proposals=0; composition proposals=0)
- 成分2・第3回: `ε₁₂` → `ε₁₃` (exact open=False; family_id=10; cited proposals=0; composition proposals=0)
- 成分2・第4回: `ε₁₃` → `ε₁₄` (exact open=False; family_id=10; cited proposals=0; composition proposals=0)
- 成分2・第5回: `ε₁₄` → `ε₁₅` (exact open=False; family_id=10; cited proposals=0; composition proposals=0)

探索が直接報告した GeneratorImage: `ν̅₁₀` → `ν̅₁₁`

## pi_24^15

- 探索状態: `partial`
- 安定基点: `pi_20^11`（DB 行: True、先行前提: True）
- 未解決目標: GeneratorImage, Relation, Relation
- 審査済み系列定義 ID: [4, 9]

期待される懸垂像: 12 件

| 成分 | 基点生成元 | 輸送先生成元 | INFERENCE として観測 | 期待数 |
|---|---|---|---:|---:|
| 1 | `(ν₁₁ ∘ (ν₁₄ ∘ ν₁₇))` | `(ν₁₅ ∘ (ν₁₈ ∘ ν₂₁))` | 4 | 4 |
| 2 | `μ₁₁` | `μ₁₅` | 0 | 4 |
| 3 | `(η₁₁ ∘ ε₁₂)` | `(η₁₅ ∘ ε₁₆)` | 0 | 4 |

### 未導出の画像条件

- 成分2・第1回: `μ₁₁` → `μ₁₂` (exact open=True; family_id=12; cited proposals=0; composition proposals=0)
- 成分2・第2回: `μ₁₂` → `μ₁₃` (exact open=False; family_id=12; cited proposals=0; composition proposals=0)
- 成分2・第3回: `μ₁₃` → `μ₁₄` (exact open=False; family_id=12; cited proposals=0; composition proposals=0)
- 成分2・第4回: `μ₁₄` → `μ₁₅` (exact open=False; family_id=12; cited proposals=0; composition proposals=0)
- 成分3・第1回: `(η₁₁ ∘ ε₁₂)` → `(η₁₂ ∘ ε₁₃)` (exact open=False; family_id=None; cited proposals=0; composition proposals=1)
- 成分3・第2回: `(η₁₂ ∘ ε₁₃)` → `(η₁₃ ∘ ε₁₄)` (exact open=False; family_id=None; cited proposals=0; composition proposals=1)
- 成分3・第3回: `(η₁₃ ∘ ε₁₄)` → `(η₁₄ ∘ ε₁₅)` (exact open=False; family_id=None; cited proposals=0; composition proposals=1)
- 成分3・第4回: `(η₁₄ ∘ ε₁₅)` → `(η₁₅ ∘ ε₁₆)` (exact open=False; family_id=None; cited proposals=0; composition proposals=1)

探索が直接報告した GeneratorImage: `μ₁₁` → `μ₁₂`

## 判断基準

- 未解決の GeneratorImage または Relation が残る場合、complete に変更しない。
- 系列定義の追加は原典の記述・掲載位置・型・Trust Boundary を別途監査した後。
- 合成規則が存在しても、その因子の像が両方証明されない限り complete としない。
- 次の実装段階は、この監査による成分別未解決位置の確定後に限定する。
- 全体 pytest は Phase 169 終了時のみ実施。

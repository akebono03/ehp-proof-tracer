# Phase 168 R3-41P4 — 残存する表示時判定の監査

## 方針

- 監査専用。プロジェクト本体のコードとテストは変更しない。
- 確認対象：安定 η 表記、EHP 完全性、推論規則名への依存。
- 検証関数を呼び出す際は元の実装に委譲し、呼び出しの有無と由来のみ記録する。
- 証明本文・Reference は R3-41P3 の保存全文と比較する。

## Git 情報

- branch: `develop`
- HEAD: `9a2834bb381da4073360959206858ff1a68acc0c`

## 静的監査で見つかった箇所

| ファイル | 行 | 呼び出し・条件 | 分類 |
|---|---:|---|---|
| `phase168_r3_5_model_renderer.py` | 227 | `inference_rule.name` | string_name_dependency |
| `phase168_r3_27_typed_statement_projection.py` | 154 | `_stable_eta_renaming_shape` | math_rule_recheck |
| `phase168_r3_27_typed_statement_projection.py` | 220 | `inference_rule.name` | string_name_dependency |
| `phase168_r3_27_typed_statement_projection.py` | 244 | `prop42_exactness_indices` | math_rule_recheck |
| `phase166_r3ac_stable_notation.py` | 67 | `_stable_eta_renaming_shape` | math_rule_recheck |
| `phase166_r3ac_stable_notation.py` | 105 | `_stable_eta_renaming_shape` | math_rule_recheck |
| `phase165_r12_r11_prop42_unified.py` | 102 | `prop42_exactness_indices` | math_rule_recheck |
| `phase165_r12_r11_prop42_unified.py` | 109 | `prop42_exactness_indices` | math_rule_recheck |
| `phase165_r12_r11_prop42_unified.py` | 131 | `prop42_exactness_indices` | math_rule_recheck |
| `phase165_r12_r11_prop42_unified.py` | 175 | `prop42_exactness_indices` | math_rule_recheck |

## 公開 Web の3群

| 群 | ProofStep | Ref. | P3全文一致 | Citation | 数学的関数の表示時呼び出し |
|---|---:|---:|---|---|---:|
| pi3_2 | 18 | 4 | True | True | 0 |
| pi4_3 | 25 | 4 | True | True | 0 |
| pi5_4 | 10 | 3 | True | True | 0 |

## 判定の内訳

### pi3_2
- η 表記の候補数：0
- 単射・全射の説明候補数：2
- 規則名依存の表示省略候補数：0
- 対象の数学的判定関数呼び出し：なし（未使用箇所の安全性は未証明）

### pi4_3
- η 表記の候補数：0
- 単射・全射の説明候補数：1
- 規則名依存の表示省略候補数：0
- 対象の数学的判定関数呼び出し：なし（未使用箇所の安全性は未証明）

### pi5_4
- η 表記の候補数：1
- 単射・全射の説明候補数：0
- 規則名依存の表示省略候補数：1
- 対象の数学的判定関数呼び出し：なし（未使用箇所の安全性は未証明）

## 解釈上の注意

- 表示時の数学的再判定と、表示の整合性確認は区別する。
- 動的呼び出し0回は検証関数が不要と証明されたことを意味しない。
- 規則名を削除する際は、同一結果の別推論規則を誤って表示省略しない保証が必要。
- 本監査は新しい推論や証明を実施しない。
- 全体 pytest は Phase 168 終了時のみ実行する。

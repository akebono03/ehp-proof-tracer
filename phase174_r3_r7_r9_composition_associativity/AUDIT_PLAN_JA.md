# Phase 174 R3-R7-R9 — 合成の結合律と型付き証明義務

## 監査済み現行状態

2026-11-06、GitHub `akebono03/ehp-proof-tracer` の `develop` HEAD `15785b921c15a19810b2b067715832ee20c61280` を確認。R8R1 は限定 pytest 175 PASS、Source Guard PASS、本監査 PASS。既存の合成懸垂推論は0候補、左因子零関係の公開候補は `equality symmetry` のみ。

## 変更対象と実装位置

新規ディレクトリ `phase174_r3_r7_r9_composition_associativity/` のみ。既存の Python ファイル・テスト・共通5文書は変更しない。

- `rule.py`：`typed_composition_factors()`、`right_associated_composition()`、`generator_image_associativity_inputs()`、`generator_image_associativity_rule()`、`expand_generator_image_associativity()` をこの順で追加。
- `audit.py`：GitHub HEAD / SHA 検査、Toda 転写確認、R8 JSON 検証、Source-first 公開候補の監査を新規追加。
- `tests/test_rule.py`、`tests/test_audit.py`：全テスト関数を新規追加。
- `run.ps1`：別プロセス pytest で同名テストの収集衝突を回避する。
- `README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`：新規追加。README は英語。

## 数学的推論と未証明部分

結合律により `(a∘b)∘c = a∘(b∘c)`。この恒等式は合成の括弧付けだけを変え、因子・順序・次元は保持する。`GeneratorImage(E, g, a∘(b∘c))` を独立して証明できた場合に限り、`GeneratorImage(E, g, (a∘b)∘c)` を推論する。

Toda Proposition 5.9 の採用転写には一般関係式 `(5.9)` と生成元の懸垂像が含まれるが、転写確認は引用の証明木を完成させない。`ν₆∘η₉=0` は、等式の対称性を1回適用しただけでは証明されない。

## Gate と次段階

- GitHub の検査済みコミット以外を拒否。全文 SHA-1 の桁不足を拒否し、LF / CRLF のみ正規化する。
- R8 完了 JSON を厳密に照合し、Source-first の既存公開 provider を変更しない。
- 結合律候補の数、括弧整合化後の既存合成規則候補、未解決の因子画像 Goal を記録する。
- 新規 GIVEN 0、production ルール追加 0、全体 pytest 不実施。

次段階 R10 は、R9 の実測値から独立した `GeneratorImage` 子 Goal と Toda (5.9) の引用付き零関係を監査する。`π₁₂⁷=0` の complete は宣言しない。

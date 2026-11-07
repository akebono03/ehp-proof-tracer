# Phase 174 R3-R7-R16 監査計画

## 数学的目的

既存の一般 EHP 零群推論から、目標 `π₁₂⁷=0` に対する Backward Search（逆向き証明探索）の**根の候補**を生成する。

- `Δ: π₁₃¹³→π₁₁⁶` の全射性
- `π₁₃¹³→π₁₁⁶→π₁₂⁷` の完全性
- `π₁₁⁶→π₁₂⁷→π₁₂¹³` の完全性
- `π₁₂¹³=0`

上記の4件は独立に証明が必要な Goal であり、候補の生成は ProofStep（検証済み証明ステップ）ではない。

## 実装範囲

変更する既存コードは `phase165_r52_r9_shared_math.py` の `shared_expansion_provider` のみ。内部関数 `expand` に、既存 `phase174_r3_r7_r3_ehp_zero_rule.rule.expand_ehp_zero_from_delta_surjectivity` の出力を追加する。

変更しないもの：数学的規則自体、文献 GIVEN、共有 Narrative Renderer、Web 専用分岐、Proof Search の first-success 規則、唯一性検査、既存 API。

## 監査・テスト

1. GitHub `develop` の HEAD を `e7bcd34a526b3f885a8e3be81c4aac362d8834c7` と照合する。
2. Git の R15-only 変更と、現在の R14 production source Git blob を検証する。
3. 前回の R15 JSON における根の候補0件・新規 ProofStep 0件を検証する。
4. DryRun で置換後の既存関数全文を `MODIFIED_FUNCTION_FULL_JA.md` に出力する。
5. 限定 pytest で既存 R3 一般規則、R14 出典付き関係、EHP 完全性、および R16 監査を検査する。
6. 本実行では既存コード1ファイルを guarded patch（事前検査付き変更）し、公開 Provider から根の候補1件・部分目標4件を確認する。
7. 通常 Group Query の未完成状態と Open Goals を実測し、最終証明の完成は宣言しない。

## 完了条件

- `Source Guard=PASS`。
- 限定 pytest がすべて PASS。
- Public root proposals = 1。
- 4件の部分目標を確認。
- 目標群の直接 GIVEN 0件。
- 既存数学的推論規則の改変0件。
- 検証済みの最終証明を捏造していない。
- Gate: `PASS_PUBLIC_GENERIC_EHP_ROOT_PREMISES_OPEN`。

## 次の Phase との境界

R16 は根の展開だけを接続する。`Δ` の全射性、`Eπ₁₀⁵=0`、`π₁₁⁶` の構造、各 Subgoal の証明、および Web 表示の共通改善は次の監査対象とする。全体 pytest は Phase 174 の最後にのみ実施する。

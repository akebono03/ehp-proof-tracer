# Phase 174 R3-R7-R22：型付き Hopf–Δ 証明境界監査

## 変更対象

新規ディレクトリ `phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/` のみ。既存クラス・関数・テスト・README.md・docs 文書は変更しない。

- `audit.py`：Git 履歴と Source Guard、Toda Prop.5.9 の7記述、型付き Δ の始域・終域・前提構造、公開未完成状態を監査。
- `tests/test_audit.py`：出典順序と HEAD の不一致、改行差異、読み取り専用契約を検査。
- `tests/test_public.py`：既存の型付き前提と Proof Search における未完成状態の回帰テスト。
- `run.ps1`：DryRun／本監査と限定 pytest。全体 pytest を呼び出さない。

## 数学的境界

Toda の採用 TeX における $H(\Delta(\iota_{13}))=\pm2\iota_{11}$、$\ker\Delta=\langle2\iota_{11}angle$、$\pi_{11}^{6}=\mathbb Z\{\Delta(\iota_{13})\}$ は、出典の依存関係として確認するが、直接 GIVEN に追加しない。

既存の `HomotopyElement` に表示された `Δ(ι13)` は `MapApplication` 型の検証済み証拠ではない。`TodaDeltaImageUpToSignStatement` の証拠と、`TodaDeltaImageFreeCyclicStatement` を導く一般推論、生成元表示の独立した証明が必要となる。

## 完了条件

1. R21 統合後の Git 履歴に限定し、Source Guard PASS。
2. 出典7記述と既存型付き前提構造を確認。
3. 限定 pytest PASS。公開 signed Δ witness 0、Verified ProofStep 0、root 未完成を検証。
4. 新規 GIVEN 0、数学規則 0、本番コード変更 0、全体 pytest 未実施。

## R23 との境界

R22 は型付き前提のギャップを特定するだけで、出典から新しい一般推論規則を構築せず、公開 Provider に接続しない。次段階では、Prop 2.7 を一般的な Hopf–Delta element image statement として正しく型付けできるかと、その根拠を検討する。

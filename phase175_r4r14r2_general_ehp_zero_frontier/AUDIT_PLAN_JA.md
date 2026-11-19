# Phase 175 R4R14R2 — 二因子合成と EHP 零群証明の監査

## 目的

Todo (5.9) の型付き一般関係 $\nu_n\eta_{n+3}=0\ (n\ge 6)$ について、$n=6$ の特殊化が、$\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\}$ の生成元の懸垂を経て $\pi_{10}^6=0$ の証明に使用できるか調査する。

## 監査対象

- `phase165_r52_r9_shared_math.py`: 共有 Proof Search Provider
- `phase174_r3_r7_r38_source_bound_zero_image_public_wiring/provider.py`: 出典付きの像ゼロ経路
- `phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/provider.py`: 先行 DB 結果の採用境界
- `phase174_r3_r7_r3_ehp_zero_rule/rule.py`: EHP の零群推論
- `phase174_r3_r7_r12_toda59_annihilator_source/source.py`: Toda (5.9)

## 確認事項

1. 既存の出典登録、添字6の関係、先行 DB 群の型を確認する。
2. 2因子の生成元の懸垂について `left_associated` の制限を監査する。
3. `ImageZeroStatement` と `GeneratorImage` に対する既存 Provider の候補を比較する。
4. EHP 零群規則の既存前提と実際の未解決 Goal を確認する。
5. 本番コードは変更せず、限定 pytest のみ実行する。

## 完了条件

Git blob 照合・実際の Provider の観測・限定 pytest が PASS し、出典なしの GIVEN や直接的な群消滅主張を導入していないこと。

## 次段階との境界

この監査では零群の完成を宣言しない。必要なら次段階で既存の一般規則を再利用し、不足する最小単位だけを実装する。

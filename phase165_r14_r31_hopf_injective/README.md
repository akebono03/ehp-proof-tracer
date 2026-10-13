# Phase 165 R14-R31

## 変更対象
新規 `phase165_r14_r31_hopf_injective.py` に以下の関数全文を追加:
`pi32_hopf_injective_goal`, `toda51_pi21_zero_step`,
`prop42_e_h_exactness_step`, `derive_hopf_injectivity_from_steps`,
`derive_adopted_tex_hopf_injectivity`, `audit_r31`。
新規テスト `test_phase165_r14_r31_hopf_injective.py`（7関数全文）。
実行 `run.ps1`, `audit.py` および採用 TeX の (5.1) 抜粋。
既存の API・推論規則・登録台帳は変更しない。

## 意味
Toda (5.1) の $\\pi_2^1=0$ を採用 TeX から特殊化し、
Proposition 4.2 (4.4) の
$\\pi_2^1\\to\\pi_3^2\\to\\pi_3^3$ における完全性と組み合わせる。
R9 の `hopf_injective_from_exactness_rule()` を利用し
$H:\\pi_3^2\\to\\pi_3^3$ の単射性を導出する。
$n=1$ はこれまでの採用 TeX 解釈に従うが、章全体の独立照合や
Registry の厳密な引用資格は未完了。

## 完了条件
対象7件の pytest 合格、同じ群・写像の完全性を照合した上で
単射性の ProofStep 1件を生成し、誤った前提を拒否する。

## 次との境界
R30 全射性と統合し、既存の単射＋全射→同型の一般規則に渡す。
全体 pytest は Phase 165 終了時のみ実施。

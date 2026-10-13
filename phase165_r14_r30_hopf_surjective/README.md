# Phase 165 R14-R30

## 変更対象
- 新規 `phase165_r14_r30_hopf_surjective.py`：`pi32_hopf_surjectivity_goal`, `prop42_h_delta_exactness_step`, `derive_hopf_surjectivity_from_steps`, `derive_adopted_tex_hopf_surjectivity`, `audit_r30` の全文。
- 新規 `test_phase165_r14_r30_hopf_surjective.py`：対象7テストの全文。
- 新規 `run.ps1`, `audit.py`, `toda_51_complete.tex`。
- 既存コード・文献台帳・推論規則は変更しない。

## 数学的内容
Proposition 4.2 (4.4) の同じ $n=1,i=2$ の連続部分
$$
\pi_3^2\xrightarrow{H}\pi_3^3\xrightarrow{\Delta}\pi_1^1
$$
の exactness（完全性）を型付きで構成する。R29 の $\Delta=0$ と既存 R9 `hopf_surjective_from_exactness_rule` を組み合わせ、$H$ の surjectivity（全射性）を `INFERENCE` ProofStep として導出する。旧証明の再生は行わない。

## 完了条件と未達
対象7テスト成功、適用制限があれば fail-closed、不正な完全性窓は拒否。採用 TeX に基づく $H$ 全射 ProofStep は生成するが、原典照合と厳密な Registry 引用資格は未承認。$\pi_3^2$ の全体証明はまだ完了しない。

## 次工程
Toda (5.1) の $\pi_2^1=0$、Proposition 4.2 の $E\to H$ 完全性から $H$ 単射を導き、単射・全射から同型を組み立てる。全体 pytest は Phase 終了時のみ。

# Phase 174 R3-R7-R37 — 上側 Δ 全射性の一般推論（隔離実装）

## 変更対象

追加場所はリポジトリ直下 `phase174_r3_r7_r37_upper_delta_surjectivity_isolated/` のみ。既存クラス・既存関数・import・pytest・既存ドキュメントは変更しない。

- 新規 `rule.py`：`upper_delta_surjectivity_inputs()`、`upper_delta_surjectivity_rule()`、`expand_upper_delta_surjectivity()`。
- 新規 `audit.py`：`verify_checkout()`、`inspect_isolated_upper_delta()`、`report()`、`main()` と Source Guard の補助関数。
- 新規 `tests/test_rule.py`、`tests/test_audit.py`、`tests/test_static.py`：テスト関数全体。
- 新規 `run.ps1`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`IMPORTS_FULL.txt`、`TEST_RESULTS_JA.md`、`__init__.py`。

## 数学的規則

偶数 $n\ge4$ の Toda Proposition 2.7 の型付き事例について、

$$
\Delta_u:\pi_{2n+1}^{2n+1}\to\pi_{2n-1}^{n},\quad
H:\pi_{2n-1}^{n}\to\pi_{2n-1}^{2n-1},\quad
\Delta_l:\pi_{2n-1}^{2n-1}\to\pi_{2n-3}^{n-1}
$$

を考える。以下の4つが、それぞれ検証済み `INFERENCE` として成立するときだけ、$\Delta_u$ 全射を導く。

1. $H$ の単射性。
2. EHP 完全列から $\operatorname{im}H=\ker\Delta_l$。
3. $\ker\Delta_l=\langle2\iota_{2n-1}\rangle$。
4. Toda Proposition 2.7 から $H\Delta_u(\iota_{2n+1})=\pm2\iota_{2n-1}$。

任意の $y\in\pi_{2n-1}^{n}$ について $H(y)$ は $H\Delta_u(\iota)$ の整数倍であり、$H$ は単射だから $y$ は $\Delta_u$ の像に属する。

## 境界

今回の規則は **隔離実装**。Web Provider には登録しない。R36 で核の監査推論は成立しているが、$E\pi_{10}^5=0$ に由来する Hopf 単射性の公開検証は未完成。`π_12^7=0` と上側 Δ の全射性は未証明のままとする。`Source-first` と `First Successful Proof Search`、共通 Narrative Renderer を変更しない。

## 完了条件

Source Guard、DryRun、型・添字・偽 GIVEN 拒否テスト、R36/R35/R5 の限定回帰テストが PASS。全体 pytest は Phase 最終時のみ。

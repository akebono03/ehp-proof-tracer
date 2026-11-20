# Phase 176 R3R22 監査仕様

## 対象と目的

既証明の Hopf η-chain を出発点とする右合成像の導出可能性について、Toda Proposition 2.2 の既存特殊化器が「合成式を左因子に持つ型付き Goal」を受理するか確認する。式を新たな GIVEN として登録しない。

## 対象ファイル

既存の `hopf_rules.py`、`expression.py`、`phase171_r2h_prop22_cited_hopf/source.py`、`phase171_r2i_eta_hopf_bridge/source.py`、`phase175_r3_pi73_hopf_lift/rule.py`、`phase176_r3r20_cyclic_candidate_boundary/audit.py`、`tests/test_hopf_rules.py` を読み取る。

新規追加はこのディレクトリの `audit.py`、`__init__.py`、`run.ps1`、`tests/test_audit.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md` のみ。

## 数学的な区別

既存の公式は $H(\alpha\circ E\gamma)=H(\alpha)\circ E\gamma$。今回の $\alpha=\nu'\eta_6$ は合成式である。公式の数学的適用可能性は、現在の構文的な特殊化が成功することを意味しない。また、$\pi_8^5\cong\mathbb{Z}/8$ から $\pi_8^3\cong\mathbb{Z}/2$ は直接導けない。

## 実行結果の判定

`PASS_R3R22_COMPOSITE_LEFT_BOUNDARY_RECORDED` は監査の成功のみを表す。公開群構造の証明完成は主張しない。全体 pytest は Phase 終了時だけ実行する。

## 次段階との境界

R3R23 以降では、出典付き右合成公式を型安全に一般化する最小実装と関連する検証を検討する。R3R22 では変更しない。

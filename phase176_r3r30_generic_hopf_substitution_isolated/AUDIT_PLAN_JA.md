# Phase 176 R3R30 監査・実装仕様

## 対象

Toda Proposition 2.2 の一般公式と、独立に検証された Hopf 値からの右合成代入を、合成左因子を含む一般的な場合へ拡張する。

$$
H(\alpha\circ E\beta)=H(\alpha)\circ E\beta,\qquad
H(\alpha)=\delta
\quad\Longrightarrow\quad
H(\alpha\circ E\beta)=\delta\circ E\beta.
$$

`\delta` は単一の生成元に限らず、型の合う合成式も認める。

## 変更一覧

**既存ファイル変更なし。** 新規 `phase176_r3r30_generic_hopf_substitution_isolated/` のみ。

- `source.py`: 新規 `generic_hopf_substitution_inputs`, `generic_hopf_substitution_rule`, `expand_generic_hopf_substitution`
- `audit.py`: 新規 `inspect`, `main`
- `tests/test_source.py`: 新規 `elements`, `goal_and_inputs` と5テスト
- `run.ps1`: DryRun・本監査・限定 pytest
- `README.md`: 英語
- `AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`: 日本語、変更コード全文

各 import 節および各関数全文は `CODE_FULL_JA.md` に収録する。

## 完了条件

公式の特殊化と Hopf 値を独立した2つの前提として候補生成し、`ProofRule.INFERENCE` のみで一般代入の結論を得られることを限定テストで確認する。誤った型、必要な前提の欠落、出典の重複は拒否する。

## 次の段階との境界

R3R31 で、今回の一般推論を共有 Proof Search に接続し、実際のソース審査済み前提から未解決 Goal に到達できるか検証する。今回の Phase では本番 provider に接続せず、根の群構造証明を完成扱いにしない。全体 pytest は Phase 終了時のみ。

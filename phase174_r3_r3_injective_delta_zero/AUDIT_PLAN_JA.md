# Phase 174 R3-R3 — 単射な懸垂からの Delta 零写像（独立規則）

## 今回の変更対象

新規ファイルのみ。既存のクラス・関数・import は変更しない。

- `phase174_r3_r3_injective_delta_zero/rule.py`：新規関数 `delta_e_injectivity_inputs()`、`delta_zero_from_injection_rule()`、`expand_delta_zero_from_injection()`。いずれもファイル冒頭に全文を新規追加する。
- `phase174_r3_r3_injective_delta_zero/audit.py`：独立監査、新規 `validate_prior_r3r2()`、`validate_source_passage()`、`proof_has_cited_leaf()`、`inspect_verified_delta_inputs()`、`make_report()`、`main()` など。新規ファイルのため全文を収録。
- `phase174_r3_r3_injective_delta_zero/tests/test_rule.py`：7件の新規限定テストを全文収録。
- `phase174_r3_r3_injective_delta_zero/run.ps1`：DryRun と通常実行。
- `README.md`（英語）、`AUDIT_PLAN_JA.md`（日本語）。

`README.md`、`docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md` の既存本体は変更しない。

## 数学的内容

EHP 完全列（Toda Proposition 4.2、式 (4.4)）により、適正な添字の列

$$
\pi_{q+2}^{2n+1}\xrightarrow{\Delta}\pi_q^n\xrightarrow{E}\pi_{q+1}^{n+1}
$$

では $\operatorname{im}(\Delta)=\ker(E)$ が成立する。$E$ の単射性が独立に検証されれば $\ker(E)=0$ なので $\Delta=0$ となる。この一般的な推論だけを新規規則として実装する。

今回の具体的な適用候補は

$$
\pi_7^7\xrightarrow{\Delta}\pi_5^3\xrightarrow{E}\pi_6^4
$$

である。単射性は既存の Proposition 4.4 の推論器、完全性は既存の Proposition 4.2 の型付き特殊化器で再生を試みる。これら2つの前提が実際に成功した場合だけ、監査中のメモリに $\Delta=0$ の `INFERENCE` ProofStep を構築する。

この導出は Toda (4.8) の条件 $\Delta(\iota_7)=0$ を満たすための候補だが、**(4.8) の商群同型、$\nu_5$ の生成元、位数8、公開 Group proof は今回実装しない。**

## 安全性とテスト

- 2前提の ProofStep はともに `INFERENCE` を要求。
- Prop 4.2 の EHP ウィンドウの添字と写像の順序を検証。
- 誤った懸垂写像・EHP の順序・無関係な次元・裸の `GIVEN` を拒否。
- 現行コードと関連する Prop 4.4／既存 Delta-zero テスト、R3-R2 テストのみを実行。
- Git 作業ツリー、index、公開探索を維持。全体 pytest は Phase 174 末尾のみ。

## 完了条件と次工程

`PHASE174_R3R3_GATE=PASS` と限定 pytest の全 PASS を必要とする。さらに監査ログの `PHASE174_R3R3_DELTA_ZERO_DERIVED_IN_MEMORY` により、前提の実際の証明再生状況を確認する。Gate PASS は公開探索の complete を意味しない。

次の R3-R4 で初めて、実証された一般規則の公開 Provider 接続と Toda (4.8) の「条件付き商群構造」の推論を検討する。新しい専用 Narrative は作らない。

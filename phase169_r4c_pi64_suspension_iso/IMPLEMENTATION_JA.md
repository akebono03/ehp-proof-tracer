# Phase 169 R4C — 実装内容・完了条件

## 事前確認

GitHub `akebono03/ehp-proof-tracer`、`develop` HEAD `7f4db3c50b817e2501238ec5c1ab966378ea5409` を確認。R4B 導入前 Git blob `8a9d534f...` と、R4B コミット済み Git blob `c94dc82f...` の双方について、既知の挿入内容を含む同一の R4B 状態であることを検証する。関連する既存コードは `phase165_r14_r6_generic_iso.py`、`phase165_r12_r12_ehp_consequences.py`、`phase165_r12_r24_web_search_connection.py`、`phase165_r12_r15_toda51.py`、`phase169_r4b_prop44_injectivity/rule.py`。関連既存テストは R4B 6件、R3O 7件。

## 変更対象

- 既存 `phase165_r52_r9_shared_math.py`：`shared_expansion_provider` の1箇所だけ。既存の import 節は変更しない。関数内に `phase169_r4c_pi64_suspension_iso.rule.expand_pi64_suspension_isomorphism` の import を追加し、既存 R4B 展開直後に1行の呼び出しを追加する。
- 新規 `phase169_r4c_pi64_suspension_iso/rule.py`：`pi64_suspension_isomorphism_rule`、`expand_pi64_suspension_isomorphism`、定数 `_PI64_E` を追加（全体を同ファイルに記載）。
- 新規 `phase169_r4c_pi64_suspension_iso/tests/test_r4c_pi64_suspension_iso.py`：テスト関数6件、必要な import を含む全文を同ファイルに記載。
- 新規実行ファイル：`run.ps1`、`patch.py`、`audit.py`。

既存の `README.md`、`design.md`、`development_log.md`、`roadmap.md`、`proof_records.md` は変更しない。

## 数学的根拠

対象は次の具体的な写像のみ。

$$
E:\pi_5^3 \longrightarrow \pi_6^4.
$$

Toda Proposition 4.4 に基づく単射性（R4B）と、Proposition 4.2 (4.4) の EHP exactness と (5.1) による $\pi_6^7=0$ からの全射性を、双方とも `INFERENCE` の ProofStep として要求する。次の2前提からのみ同型を導出する。

$$
\mathrm{Injective}(E) \quad\land\quad \mathrm{Surjective}(E)
\quad\Longrightarrow\quad E:\pi_5^3\xrightarrow{\cong}\pi_6^4.
$$

Toda (4.5) の安定範囲は変更しない。$\pi_6^4$ の既知群構造を与件として挿入しない。群構造輸送および Renderer は既存のまま。

## 検証と完了条件

限定 pytest：R4C の6件 + R4C1 安全確認6件 + 既存 R4B 6件 + 既存 R3O 7件 = **25件**（既存他のテストが同一ファイルに追加されている場合は件数が変わる）。全体テストは Phase 最終段階のみ。

**R4C 成功条件**：新規規則が証明義務を生成し、引用審査済みの Prop 4.4、Prop 4.2 (4.4)、(5.1) の GIVEN 祖先がある証明を再構成できること。`run.ps1` は限定 pytest または監査失敗時に R4B 状態へロールバックする。

**次の Phase との境界**：$\pi_6^4$ の公開探索結果を監査し、未解決 Goal がある場合のみ追加する。完成していないものは completed と宣言しない。Web Renderer の形式修正は別件。

## R4C1 の修正範囲

旧コミットの Git blob にのみ依存していた `patch.py` の安全確認を拡張。`rule.py`、`audit.py`、R4C 数学テストの内容は不変。監査・テストに成功しなければ R4C 前の状態に戻す。

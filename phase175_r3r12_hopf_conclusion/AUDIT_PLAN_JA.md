# Phase 175 R3R12R5 — Hopf 写像の始域・終域表示統一

## 変更対象（実装前の列挙）

- `phase175_r3r12_hopf_conclusion/projection.py`：`project_verified_hopf_lift_conclusion()` 全体。既存 import に変更なし。
- `phase175_r3r12_hopf_conclusion/tests/test_projection.py`：`test_pi73_single_final_conclusion_and_hopf_isomorphism()`、`test_internal_cyclic_latex_is_not_a_second_proof_requirement()`、`test_concise_consequences_follow_typed_hopf_map()`、`test_injectivity_line_matches_the_real_typed_renderer()`、`test_pi63_old_narrative_remains_unchanged()` の期待文字列等を変更。import と各関数全文は `CODE_FULL_JA.md` を参照。
- `phase175_r3r12_hopf_conclusion/audit.py`：`GATE` 定数、`_public_gate()`、`run()`、`main()` の Gate 識別子・出力期待値を更新。
- `phase175_r3r12_hopf_conclusion/run.ps1`：Gate 識別子を更新。
- `README.md`（英語）、`AUDIT_PLAN_JA.md`、`TEST_RESULTS_JA.md`、`CODE_FULL_JA.md`（日本語）：全文更新。

新規クラス・関数なし。`install.py`、既存 R3R11・Phase 172・Proof Search・DB・数学的規則・GIVEN は変更しない。

## 現行コードと関連テストの事前確認

GitHub `akebono03/ehp-proof-tracer` の `develop` から、R3R12、R3R11、Phase 168 の型付き表示、R3 の Hopf lift 一般規則と verified prior DB 版の関連コードおよびテストを確認した。出発点は直近の R3R12R4 配布 ZIP（ユーザーが `develop` で正常実行した版）。R3R12R4 は DryRun PASS・限定 pytest **52 passed**・公開 Group query complete・Trust True・Reference 7件・結論1件・最終 Gate PASS。

## 実装の境界

既存の証明木で使われた `MapInjective` の写像から `map_symbol_tex()` で $H$ を得て、証明済みの始域・終域に `group_tex()` を適用する。$n=3$、$k=4$ 等の特定の数字を文章テンプレートへ直接埋め込まない。

結果は例として以下の2文にする。

- `よって, $H: \pi_{7}^{3}\to \pi_{7}^{5}$ は全射.`
- `よって, $H: \pi_{7}^{3}\to \pi_{7}^{5}$ は同型.`

前提に関する fail-closed（不明なら無変更）検証、出典、Hopf 等式、最終結論の重複防止をすべて維持する。`MapSurjective` または `MapIsomorphism` の証明ステップを新規に生成しない。

## テスト・完了条件

- DryRun：既存版が導入済みなら `PATCH_STATUS=ALREADY_APPLIED` を期待。
- 本実行：R3R12・R3R11・Phase 172 等の既定の限定 pytest のみ実施。
- 公開証明：両方の写像文・合成式・最終結論1件、Reference 7件・Trust True、Lemma 5.4 非依存を確認。
- $n=3,k=3$：既存 Phase 172 の証明表示を維持。
- 全体 pytest：Phase 175 の最後にのみ実施。

期待 Gate：`PASS_R3R12R5_VERIFIED_HOPF_MAP_DOMAIN_CODOMAIN`。

次の Phase で扱う新しい群構造の推論や専用証明は先取りしない。

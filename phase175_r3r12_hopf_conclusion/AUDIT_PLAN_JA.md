# Phase 175 R3R12R4 — 共通 Hopf lift の短文表示

## 変更するファイル・関数

- `phase175_r3r12_hopf_conclusion/projection.py`：`project_verified_hopf_lift_conclusion()` 全体。`map_symbol_tex` を import に追加。
- `phase175_r3r12_hopf_conclusion/tests/test_projection.py`：短文表示を確認する既存テスト関数全文の期待値を更新、新規テスト関数を `test_partial_or_missing_source_citations_are_unchanged()` の直前に追加。
- `audit.py`：`GATE`、`_public_gate()`、`run()`、`main()`。
- `run.ps1` および4文書：監査 ID と記録を更新。

既存の R3R11R4 接続関数・その他の数学的コードには手を加えない。

## 監査済みの現行コード

GitHub `akebono03/ehp-proof-tracer` の `develop` を確認した。R3R11R4 の `projection.py` の blob は `258d22589f92fbebdb9c4516dbe72c1f94a98afd`。関連して Phase 175 R3 Hopf lift の一般規則と verified prior DB variant、共通型付き Renderer、Phase 172 と R3R11 の表示回帰テストを確認した。さらに配布済み R3R12R3 の実行コードと、ユーザーの Windows 実行結果（限定 pytest 51 passed、Gate PASS、結論1件）を確認した。

## 数学的・表示上の境界

検証済みの Hopf lift 前提 `H` の単射性、余域の有限巡回構造、生成元像は既存の Proof Tree からのみ取得する。これらをもとにした共通の帰結を「よって, $H$ は全射.」「よって, $H$ は同型.」と短く表示する。写像名は検証済み `MapInjective` の map object から描画するため、$\nu\prime$、$\eta_5$、`n=3`、`k=4`、参照番号を文章テンプレートに埋め込まない。

新たな `MapSurjective`、`MapIsomorphism` の証明ステップを追加したと宣言しない。既存の一般規則の論理的帰結を文章化するだけである。元の出典つき群構造・Hopf 合成式・単射性の表示が欠ける場合は無変更とする。

## テスト・合格条件

- DryRun：既存のソース固定検査と作業ツリー検査が PASS。`PATCH_STATUS=ALREADY_APPLIED` を期待。
- 本実行：R3R12・R3R11R4・R3R10・R3R9・Phase 171・172・R70 の限定 pytest のみ。
- $\pi_7^3$：公開検索 complete / Trust True / Reference 7件、Hopf 合成式1件、結論1件、短文2件を確認。
- $\pi_6^3$：Phase 172 の従来表示を維持。
- 数学的規則追加0、GIVEN 追加0、全体 pytest 未実施。

Gate: `PASS_R3R12R4_CONCISE_VERIFIED_HOPF_CONSEQUENCES`。

R4 の新しい群探索機能や、将来の一般的な全射・同型 `ProofStep` 生成は導入しない。

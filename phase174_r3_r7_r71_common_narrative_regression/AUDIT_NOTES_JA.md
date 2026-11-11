# Phase 174 R71 — 共通 Narrative 限定回帰監査

## 目的と境界

R70R1 までの共通表示を基準とし、既存の別の完成証明で回帰が生じていないかを確認する。実装コードの変更は行わない。既存の数学規則・GIVEN・専用 Narrative を追加しない。全体 pytest は Phase の最後に限る。

## GitHub 事前監査

2026-11-11 の `akebono03/ehp-proof-tracer` `develop` は `01c5246a011b43e10ed85699a6048f117562a748`。引き継ぎ HEAD `fa98a4301026820714cd51da80ffacfd99e47b20` から二つ進んだ状態で、R70 と R70R1 の変更が取り込まれている。

次の関係ファイルを確認した：

- `phase171_r20r13_eta_sentence_layout/projection.py`：共通 Formatter と R70 projection 接続。
- `phase174_r3_r7_r70_verified_narrative_projection/projection.py`：出典・ProofStep 条件付きの表示統合。
- `phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py`：根、出典、曖昧一致等の保護。
- `phase174_r3_r7_r70r1_assoc_chain_display_fix/tests/test_install.py`：associativity の正規の親 ProofStep 経路を検査。
- `phase168_r3_5_model_renderer.py`：共通 Renderer。
- `phase171_r20r13_eta_sentence_layout/tests/test_projection.py`：既存 $\pi_6^3$ の完成表示。
- `phase174_r3_r7_r56_cyclic_generator_bridge/audit.py`：既存の公開探索＋Verifier 経路。
- `phase174_r3_r7_r68_ehp_premise_semantics_audit/audit.py`：推論規則の直接前提。

## 変更対象のファイル・関数

既存ソース／テスト：変更なし。

新規ファイル：

1. `phase174_r3_r7_r71_common_narrative_regression/__init__.py`（パッケージ宣言）。
2. `phase174_r3_r7_r71_common_narrative_regression/audit.py`。新規関数 `git_blob_sha`、`source_guard`、`local_head`、`reference_body_contract`、`inspect_public`、`main` は同ファイルの定数定義後に追加。
3. `phase174_r3_r7_r71_common_narrative_regression/tests/test_audit.py`。8件の独立テスト関数を追加。
4. `phase174_r3_r7_r71_common_narrative_regression/run.ps1`。
5. `phase174_r3_r7_r71_common_narrative_regression/README.md`（英語、全文同梱）。
6. `phase174_r3_r7_r71_common_narrative_regression/AUDIT_NOTES_JA.md`（日本語、全文同梱）。

## 対象と検査

既存の完成例 $(n,k)=(3,3),(4,3),(4,4),(4,5),(4,7),(5,3),(6,5),(7,5)$ に対し、実際の Group search、Verifier（証明検証）、ProofNarrativeModel（証明文章モデル）、共通 Renderer を通す。すべて complete、Open Goal なし、検証済み根と結論の一致、Reference の連番表示、既存の段落境界、ProofStep／Citation の不変性を確認する。

既知の Reference 件数 $(3,3)=8$、$(6,5)=7$、$(7,5)=3$ を固定する。R70 で統合した合成像と EHP 説明の文字列についても回帰を検査する。未完成モデルには R70 の表示変換が適用されないことを単体テストで検査する。

この監査で全証明文章の数学的意味が網羅的に正しいと保証することはしない。R71 の監査自身も `ProofStep` 生成・推論規則の追加・直接 GIVEN 登録を行わない。

## 実行手順と完了条件

解凍後、プロジェクトルートから `run.ps1 -DryRun` を実行し、その後 `run.ps1` を実行する。DryRun は出典ガードのみ。通常実行は限定 pytest と8例の公開探索を実行し、監査 JSON を `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r71_common_narrative_regression\report.json` に出力する。

Gate が `PASS_R71_FOCUSED_AND_CROSS_GROUP` となった場合のみ R71 の限定回帰を PASS と扱う。実環境でのテスト結果を確認する前に PASS を宣言しない。次は監査結果から Phase 174 Closeout 対象と未確認項目を確定する。

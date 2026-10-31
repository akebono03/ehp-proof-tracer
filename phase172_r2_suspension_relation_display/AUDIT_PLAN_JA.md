# Phase 172 R2 — 懸垂等式の表示重複解消

## 参照した監査結果

- 2026-10-31 Phase 172 R1：`PASS_AUDIT_ONLY`。
- 実行 HEAD `845508ddf8f3bc30fa8a51349c065c7551eb893a`、Web `generic-complete-proof`、ProofStep 50件、Reference 8件、未解決 Goal 0。
- R1 `proof_steps.json` の Step 5 は引用つき `GeneratorSuspension` で `E(η₅)=η₆` を示す。
- Step 6 はその Step 5 に依存する `Eη₅=η₆`、Step 7 は Step 6 に依存する `η₆=Eη₅`。
- Step 8 は Step 7、Step 15 は Step 6 に依存するので、Step 6/7 を Proof Tree から除去してはならない。
- GitHub `develop` の共通 Renderer、Phase 171 の η 表示 Projection・位数4 Projection と関連テストを確認。

## 変更対象

| ファイル | クラス・関数 | 変更 |
|---|---|---|
| `phase168_r3_5_model_renderer.py` | `render_model_backed_narrative_markdown()` | 既存の表示省略集合に、検証済み懸垂等式の投影結果を統合する。関数全体は DryRun 時に外部ディレクトリへ全文出力 |
| `phase172_r2_suspension_relation_display/projection.py` | 新規関数 `redundant_suspension_relation_indices()` | 生成元の懸垂、等式、左右対称の型付き ProofStep と引用祖先の対応を確認し、本文表示を省く番号だけ返す |
| `phase172_r2_suspension_relation_display/tests/test_projection.py` | 新規 pytest テスト5件と fixture | π₆³ 実探索・引用保持・未証明や出典欠損時の fail-closed（不正表示を避ける動作）を確認 |
| `phase172_r2_suspension_relation_display/install.py` | 新規実行補助 | HEAD 内容検査・全文関数出力・復旧つき限定テスト |
| `phase172_r2_suspension_relation_display/run.ps1` | 新規 PowerShell Runner | DryRun と限定テスト |

既存の import 節は変更しない。共通 Renderer の該当関数内に新たなローカル import を追加する。新規 Projection はパッケージ直下に設置する。

## 設計上の制限

- 数式文字列の正規化・文字列一致で同値性を宣言しない。
- 元の GeneratorSuspension が実際の完成根の祖先にあり、型付き文として表示され、引用済み GIVEN 祖先に基づく場合のみ対象とする。
- 派生する等式も対称等式も、前提を正確にたどり、引用のない INFERENCE であることを確認する。
- 元の懸垂の表示が先の表示処理ですでに隠れていれば、一切削らない。
- 個別の η/ν family、添字、特定の群による表示例外を追加しない。
- Proof Tree、Reference、Trust Boundary と検索エンジンには触れない。

## テストと完了条件

実行する限定 pytest は以下の5セット（それぞれ別 pytest プロセス）。

1. 新規 R2 Projection テスト。
2. Phase 171 η 文章整形テスト。
3. Phase 171 位数4文章整形テスト。
4. Phase 169 先行証明の Reference テスト。
5. Phase 169 π₆⁴ の叙述テスト。

完了条件：DryRun 成功、内容検査 PASS、限定 pytest PASS、π₆³ の `[R3] E(η₅)=η₆` は維持、等式と対称等式の重複2行を非表示、Hopf の最終関係と位数4の結論を維持、引用8件・未解決0、変更対象の既存ソースは Renderer の1件のみ。

## R3 との境界

R3 では Hopf 写像の導出を別途監査・整理する。R2 は Step 8 以降、MapSurjective、Reference の内部名、数学的な証明探索を変更しない。全体 pytest は Phase 172 最後の R6 のみで実行。

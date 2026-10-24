# Phase 168 R3-41O — 共通 Renderer の最終表示整理

## 変更範囲

- `phase168_r3_5_model_renderer.py` / `render_model_backed_narrative_markdown()` の全文置換。
- `phase168_r3_41n1_import_scope_fix/tests/test_phase168_r3_41n_composed_proof_display.py` / `test_pi43_exactness_is_consumed_by_concrete_kernel()` の期待値更新（テストファイル全体を収録）。
- `phase168_r3_41o_renderer_closure/tests/test_phase168_r3_41o_renderer_closure.py` を新設（関数全文）。
- module-level import には変更なし。変更後の関数内 import 部分は `function_import_section_full.txt` に省略なしで収録。

## 修正

1. 共通 `model.target` から `π` の対象群を導入文に表示。
2. 完全性に関する型付きの `SuspensionKernelFreeCyclicStatement` が、別途抑制された `EHPImageEqualsKernelStatement` を実際に消費しているときだけ、`ker E = Im Δ = Z{...}` に合成して表示。根拠ステップは削除しない。
3. Renderer 内の `generator_transport_normalization_rule(...).match_guard(...)` の直接実行をやめ、既に証明済みである `ProofStep.inference_rule.name` と型付きの直接前提・対応する群の一致から、**表示の省略だけ**を決める。証明探索や適用条件は変更しない。
4. Reference、固定基準、出典台帳、群固有の証明、ほかの Phase の機能には触れない。

## 検証

- GitHub develop の現行 Renderer、R3-41N1、R3-41M2、R3-41L、R3-41J2、および R3-41I 監査のテストを確認した。
- 限定 pytest（対象10群テストファイル）のみ実行。失敗時は本番2ファイルを SHA256 確認のうえ復元。
- 終了監査では3群の Reference と本文と凍結基準を比較。本文差分数は文字列一致率ではない。
- Phase 168 全体 pytest は **本 Phase の最後だけ**に実行する。

## 次 Phase との境界

今回の修正は証明の文章化のみ。新しい型付き命題・既存 Goal の選択・publication order・Backward Search・他の群の追加証明は今 Phase の変更範囲外。

## 注意

R3-41O は限定検証が成功しても Phase 終了を即宣言しない。差分の最終レビューと、既に把握した群個別の DB 表記処理・固定 assertion ID 除外の責務監査を先に行う。

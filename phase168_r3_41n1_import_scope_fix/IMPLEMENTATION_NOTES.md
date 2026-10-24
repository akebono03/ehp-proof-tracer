# Phase 168 R3-41N1 — `Relation` import スコープ修正

## 今回のエラー

R3-41N は `Relation` を新しい中間表示の抑制条件で参照しているが、`from proof import Relation` が同じ関数の後方にあった。Python が変数を未初期化の局所変数と扱い、`UnboundLocalError` が発生した。これは数理的な判定エラーではない。

## 変更対象

- `phase168_r3_5_model_renderer.py`：`render_model_backed_narrative_markdown` **関数全体**。関数先頭の `from proof import ProofRule` を `from proof import ProofRule, Relation` とし、後方の `from proof import Relation` を削除。R3-41N のその他の実装は一切変更しない。
- `phase168_r3_41l_reasoned_prose/tests/test_phase168_r3_41l_reasoned_prose.py`：R3-41N で変更予定だった既存テスト全体（中間ステップは証明木にあるが本文で重複させない条件）。import 変更なし。
- 新規 `phase168_r3_41n1_import_scope_fix/tests/test_phase168_r3_41n1_import_scope.py`：関数内 import の実行順序を限定検査。追加位置は R3-41N1 フォルダの `tests/`。
- R3-41N の限定テストはそのまま同梱。

## ファイルとテスト

- `renderer_function_full.py`：変更後の関数全文。
- `renderer_full_file.py`：変更後の Renderer ファイル全文。
- `r341l_test_full.py`：変更後の既存テスト全文。
- `renderer_function_before_fix.py`：今回修正前の R3-41N の関数全文（差分確認用）。
- `install.py`：SHA256 による R3-41M2 preimage ガード。バックアップ付き。
- `run.ps1`：新規・既存の限定 pytest、3群の Web 監査を実行。失敗時は2ファイルをバイト単位で復元。

## 完了条件

1. 追加 import の配置検証と限定 pytest が PASS。
2. π₃², π₄³, π₅⁴ の出典、証明順、基準論証に欠落なし。
3. π₄³ と π₅⁴ の不要な中間表示は抑制され、証明木には残る。
4. 未完成表示、群専用固定文章、Reference に影響しない。
5. 全体 pytest は Phase 168 の終了時のみ実行。

## 次 Phase との境界

探索規則、命題台帳、証明生成の対象拡大、文献順処理には手を加えない。

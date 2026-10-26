# Phase 169 R3Q 実装記録

変更対象は `phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown()` と `phase168_r3_27_typed_statement_projection.py` の `typed_sentence()`・`map_symbol_tex()`、同じファイルの `typed_sentence()` 直前に追加する `map_property_sentence()` のみ。

以前の `body_line` の有無で「型付き理由」と「LaTeX 定型文」を分岐させる構造を改める。すべての ProofStep に `typed_sentence()` を最初に適用し、未対応だけ従来の表示へフォールバックする。`MapInjective` / `MapSurjective` と `TodaSuspensionInjectiveStatement` 等を同じ意味別の判定にまとめた。

完全性の理由は単なるキーワードで判断せず、実際の ProofStep 前提に含まれる正しい位置の EHP 完全列・写像の性質から導く。π₅³等の群番号で分岐しない。`R3P` の追加補助経路が適用済みであれば、その表示分岐を取り除く。命題台帳・証明木・Citation・Backward Search は変更しない。

実行後 `output` に両ファイルの差替え可能な全文と変更関数の全文・旧内容のバックアップを保存する。全体 pytest は Phase 169 の最後のみ行う。

ただし Proposition 5.1 の複合命題が Reference 本文へ完全に投影される問題は別課題であり、引用情報や文献根拠をこの段階で作り足さない。

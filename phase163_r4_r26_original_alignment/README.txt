Phase 163 R4-R26 — 原本照合済み転記修正

プロジェクト直下に解凍し、PowerShell で実行：
powershell -ExecutionPolicy Bypass -File .\phase163_r4_r26_original_alignment\run.ps1

前提：phase163_r4_r25_output\Toda_01_corrected.tex が存在すること。
原本：ユーザー提供 Toda_01.pdf 印刷14ページ（PDF 10ページ目）。

修正対象：Proposition 1.9 の証明における上線欠落2箇所。
前提 SHA-256 が一致しないと処理停止。元原稿の上書きなし。
出力：phase163_r4_r26_output 内の全文TeX、修正前全文、CSV、JSON、報告。
既存コード、台帳、Statement ID、証明探索は変更なし。
全体テストは Phase 163 の最終段階まで行わない。

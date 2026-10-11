Phase 163 R4-R33 — Toda 第1章 印刷6ページ（PDF 2ページ）の部分原本照合

プロジェクト直下へ ZIP を解凍し、以下を実行してください。
  powershell -ExecutionPolicy Bypass -File .\phase163_r4_r33_page6_alignment\run.ps1

必要な入力：
  phase163_r4_r32_output\Toda_01_corrected.tex
  phase163_r4_r32_output\page_ledger.json

実行前に focused test のみを実施します。全体 pytest は実行しません。
入力の SHA-256 と台帳状態を確認し、想定外の場合は変更を行いません。
既存の原稿・Registry・ProofStep・Renderer・Backward Search は上書き・変更しません。
出力：phase163_r4_r33_output 以下に修正前後 TeX 全文、台帳、照合記録、summary、report。
原本 PDF の数学的内容の部分照合であり、印刷6ページ全文の逐語・数学的照合完了ではありません。

Phase 163 R4-R27 - page-by-page verification ledger

Extract in the repository root and run:
  powershell -ExecutionPolicy Bypass -File .\phase163_r4_r27_page_ledger\run.ps1

Input: phase163_r4_r26_output\Toda_01_corrected.tex
Output: phase163_r4_r27_output\page_ledger.json, page_ledger.csv, correction_history.csv, summary.json, report.md

The input's normalized UTF-8 SHA-256 must match the R26 output.
This is a read-only audit. The supplied original PDF must be inspected by a reviewer before any page is marked VERIFIED. All pages start UNVERIFIED. This phase does NOT establish full chapter parity.
Focused pytest only. No production code or prior outputs modified.

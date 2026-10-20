# Phase 166 R3-L — Unified Reference Order Binding

This package connects all currently registered literature references to the existing Phase 163 order manifest where a verified, structural reference identity exists. It never matches by displayed citation locator and never invents missing publication positions.

Run `run.ps1` from the repository root. It backs up and patches one function in `phase165_r52_r9_shared_math.py`, installs `phase166_r3l_reference_order.py`, runs focused tests, and writes the complete audit to `phase166_r3l_all_reference_order_results.json`.

No inference rules, renderer, proof replay, or full test suite are changed. Missing identity mappings remain explicitly unresolved and are reported.

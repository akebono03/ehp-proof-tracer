# Phase 162 R3 Web display-math repair

The existing Web parser accepts `\\[` and `\\]` but not a standalone `$$` delimiter. R3 currently emits standalone `$$` lines, making raw TeX appear on screen.

This repair changes **only** the R3 Markdown output delimiters. Mathematical derivations, proof trees, existing references, punctuation and the upper Group proof remain unchanged.

Run `run_phase162_r3_2_web_math_display.ps1` after extracting this folder directly beneath the repository root. The installer is idempotent and backs up the original R3 source. Only focused tests run.

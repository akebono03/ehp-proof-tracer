# Phase 163 R4-R63 source boundary audit — path fix

Run `run.ps1` from the project. The script finds the previously extracted Toda TeX sources under `phase163_r4_r42_tex_extract/inputs` (preferred), falling back to the project root when all three required files are present. The same resolved source root is passed to both focused pytest and the audit CLI.

Requires `phase163_r4_r62_output/remaining_definitions.json` and the three source files `Toda_01_corrected.tex`, `Toda_03_2(2).tex`, `Toda_05_2(6).tex`. The script does not copy or modify source files. No full pytest suite, production registry changes, ID allocation, or proof search integration.

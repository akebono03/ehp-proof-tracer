# Phase 163 R4-R94: Source-only registry finalization

R94 builds an independent, ordered reference/assertion registry from R91/R92 data and recomputed R93 source evidence. It preserves all existing source IDs and assigns publication positions based on the current translated TeX files, not the unverified original edition.

It does not modify production registration, proof search, theorem certification, or the five main project documentation files.

Run `run.ps1` from the extracted package. Output files are written to `phase163_r4_r94_output` under the project root.

Prerequisites: R91 source catalog and R92 audit in their standard output folders; R93 and R92 and R91 package directories; five Toda TeX files in `sources/toda`.

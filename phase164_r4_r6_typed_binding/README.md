# Phase 164 R4-R6 — Limited Typed Binding Registration

This package builds an isolated in-memory registry containing exactly two typed assertions: a four-component subset of Toda Proposition 5.1 and the Hopf equality from equation (5.3). The original-source correspondence was confirmed by the user; this confirmation is recorded as provenance, not an independent machine check. The existing proof steps are retained, including their inference ancestry. Neither original-publication position nor citation-availability position is invented.

Run `run.ps1` from the extracted package folder. Targeted pytest runs before the report is generated. The report is written to `phase164_r4_r6_output/report.json` and `report.md` in the repository root. No full pytest run and no global production registry mutation take place.

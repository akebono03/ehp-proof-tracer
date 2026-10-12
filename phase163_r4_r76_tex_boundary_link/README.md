# Phase 163 R4-R76 — TeX Numbered-Boundary Crosswalk

This package reads the 11 focused R75 editorial proposals and scans the local Toda TeX extraction for theorem environments and adjacent proof markers. It does not alter production files or create registry IDs. Candidate ownership remains provisional; source positions are structural observations, not verification against Toda's original edition.

Run `run.ps1` from the repository root in PowerShell. Prerequisites: `phase163_r4_r75_output/ownership_proposals.json`, `phase163_r4_r42_tex_extract/inputs/`, Python, pytest.

Output: `phase163_r4_r76_output/numbered_boundary_crosswalk.json`, `.csv`, and `report.md`.

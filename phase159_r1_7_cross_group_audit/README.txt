Phase 159-R1-7 — cross-group display audit

Purpose
-------
Audit whether the generic public Narrative display rules established around
pi_3^2 are applied consistently to representative non-pi_3^2 groups.

This package is audit-only.

Production code changes: none.
Existing repository test changes: none.
Repository-wide pytest: do not run in this subphase.

Representative groups
---------------------
- pi_6^3  : n=3, k=3
- pi_8^5  : n=5, k=3
- pi_10^4 : n=4, k=6
- pi_11^4 : n=4, k=7

Audit topics
------------
- excessive exact-sequence display candidates
- exact-sequence display-math placement
- numbered equation display-math placement and numbering
- injective / surjective / isomorphism / zero-map wording
- exactness reason wording
- Reference declaration/use linkage and connector form
- group/generator notation candidates
- display-math terminal punctuation
- unwanted "を示す." in the proof-target section
- accidental pi_3^2 / Phase159 internal-text leakage

Important interpretation rule
-----------------------------
A machine hit is not automatically a mathematical defect.

Classify confirmed findings as:
A. generic display rule defect
B. generic rule exists but is not applied on a route
C. proof data / semantic classification issue
D. group-specific mathematical circumstance

If repair is needed, create R1-7a, R1-7b, ... by root cause.
Do not repair anything inside R1-7 itself.

Run
---
From the repository root:

powershell -ExecutionPolicy Bypass -File ".\phase159_r1_7_cross_group_audit\run_phase159_r1_7.ps1"

Output
------
phase159_r1_7_cross_group_audit\audit_output\phase159_r1_7_summary.md
phase159_r1_7_cross_group_audit\audit_output\phase159_r1_7_audit.json
phase159_r1_7_cross_group_audit\audit_output\pi6_3.md
phase159_r1_7_cross_group_audit\audit_output\pi8_5.md
phase159_r1_7_cross_group_audit\audit_output\pi10_4.md
phase159_r1_7_cross_group_audit\audit_output\pi11_4.md

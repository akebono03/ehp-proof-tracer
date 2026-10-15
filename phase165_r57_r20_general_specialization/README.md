# Phase 165 R57-R20: General Typed Reference Specialization

This package provides a reusable scalar-pattern matching and proof-checked instantiation engine. It registers the symbolic diagonal clause of the already adopted Toda (5.1) TeX as a fixed, cited general statement rather than storing a table of special cases.

The common proof search can instantiate this source for any positive dimension, subject to the existing screened-reference and proof-order policies. The existing direct higher-eta target specialization remains forbidden by the proof-order gate. No completed ProofStep is saved and no uncited mathematical facts are synthesized.

Run `run.ps1` after extracting the ZIP at the project root. The installer fails without modifying the project if R57-R18/R19 are missing or the expected existing function bodies have changed. Only focused pytest files are executed; the full suite is not run.

The general matcher handles typed dataclasses, scalar symbols, addition, multiplication when previously bound, and indexed homotopy-element names. This Phase does not claim to fully support every formula in Toda; each general source must be adopted with a verified locator and its actual domain.

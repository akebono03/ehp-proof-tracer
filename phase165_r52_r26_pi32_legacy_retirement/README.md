# Phase 165 R52-R26 — Retire the legacy pi3^2 inference factory

This package removes the pi3^2-specific inference factory from `toda_rules.py` and its two active invocations in the historic bootstrap and probe. It does not alter the typed Phase 165 common backward search or its generic inference rules.

Run `run.ps1` from the unzipped package located directly under the repository root. The installer rejects unexpected AST shapes, preserves originals as `.phase165_r52_r26_backup` files, and is idempotent when all three removals have already occurred. It does not retire other legacy rule factories or claim that the entire bootstrap is unused.

The old bootstrap/probe might no longer produce their previous pi3^2 generator conclusion. They are legacy exploratory paths, not the supported proof-generation path. R26 runs focused migration tests plus the existing typed shared search test. Full pytest is deferred until Phase completion.

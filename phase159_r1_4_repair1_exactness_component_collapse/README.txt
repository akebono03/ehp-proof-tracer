Phase 159-R1-4 repair1

Purpose:
Collapse overlapping public exact-sequence lines generically.

Rules:
- Normalize `Δ` and `\Delta` for comparison.
- Treat a shorter exact sequence as belonging to a longer component when its
  normalized LaTeX is a contiguous substring.
- Keep one maximal line per component.
- Render the kept line as `... は完全である.`
- Preserve unrelated non-overlapping exactness components.

No imports changed.
No tests changed.
No full pytest.

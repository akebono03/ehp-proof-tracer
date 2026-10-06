Phase 159-R1-7b repair8

Fixes two runtime-confirmed generic defects:
1. typed TodaProp42ExactnessStatement -> LaTeX extraction returned None;
2. visible exactness lines in `$...$.` form were not recognized.

No group-specific or proposition-specific branch is added.
Focused tests only; no repository-wide pytest.

Phase 143-75AH R2

The first implementation run showed:
- 27 existing/related tests passed
- 3 new tests failed only because their expected strings were wrong

R2 changes no production code.

Test corrections:
1. Expect one LaTeX backslash, not two.
2. Preserve the existing generic HomotopyElement rendering of Unicode alpha.
3. Expect the canonical source-group LaTeX with one backslash.

Focused tests only.
No full pytest.

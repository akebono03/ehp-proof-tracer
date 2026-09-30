# Phase 150 / RC4-5F-2-R1

Test/audit-harness-only repair.

The RC4-5F-2 production implementation rendered the intended final
group-structure reason correctly. The single focused-test failure and the
false visible-check result came from Python string literals whose backslashes
were not raw strings.

This package changes only the newly added RC4-5F-2 test:

- the `2\cdot2=4` expectation is a raw string;
- the final `\pi_6^3 = \mathbb{Z}/4\{\nu'\}` expectation is a raw string.

The PowerShell visible check is also rewritten to use raw Python strings and
to report separate reason/conclusion/ordering checks.

No production file is changed. Repository-wide tests remain deferred until
the end of Phase 150.

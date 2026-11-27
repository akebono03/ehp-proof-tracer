# Phase 178 R15R2 — Toda (5.12) public connection

Append the three already tested source claims to the default shared typed registry and append the existing screened provider to the shared provider list. No new mathematical inference, group-structure GIVEN, or change to publication screening is introduced.

Requires the reviewed R15 isolated package (including the R15R1 HEAD fix). The installer accepts the reviewed base or a descendant whose only committed file changes relative to that base are exact copies of the pinned R15 package. Other tracked modifications are refused. A previously applied exact R15R2 module is accepted for reruns. The installer saves the entire proposed module and the two complete modified functions in the external audit directory; `-DryRun` does not alter the repository. A failed first installation restores the original module bytes. Do not run concurrently with repository edits.

Run `run.ps1 -DryRun` and then `run.ps1` from PowerShell. Focused tests exercise the real shared registry, source screening and provider, the existing EHP candidate chain, and regressions. The full test suite is not run. These checks do not certify the three target group proofs or complete (5.13) registration.

# Phase 174 R3-R7-R45: EHP Open Obligation Audit

Read-only inspection of four EHP exactness windows required by the generic
proof of the target group statement `pi_12^7 = 0`.

The audit reuses the existing source-first screened general Toda Proposition
4.2 source, canonical backward-search adapter, R3 EHP zero-group inference,
R5 Hopf injectivity, and R37 upper Delta surjectivity. It does not modify
production modules, install math rules, add `GIVEN` facts, create a dedicated
narrative, or claim the final theorem. It deliberately excludes R44's
zero-image proof branch from its limited search.

Run the `run.ps1` script first with `-DryRun`, then normally. Outputs are
stored under the user's local application-data audit directory. The runner
uses only focused pytest groups and does not run the complete test suite.

Two reviewed local states are accepted: the preceding R44 HEAD (with the
checked R44 package files present) and the subsequent R44 merge HEAD. Both
require the current remote `develop` HEAD to match the reviewed merge.

# Phase 174 R57R3: Surjectivity Test Contract Correction

This narrowly scoped correction fixes the outdated negative expectation in the R57 regression test. The one-premise Delta-surjectivity rule correctly matches its one required cyclic group presentation even if an unrelated typed Proposition 2.7 statement is also present among available facts. Only the cyclic group statement belongs to the resulting proof step's premises.

The package modifies two files: the existing R56 focused test module, and R57's installation script, which stores the reproducible test template and its SHA-256 digest. No mathematical rule, proof search, source registration, narrative renderer, or top-level project document is changed.

Extract `R57R3.zip` into the repository root. Run `phase174_r3_r7_r57r3_surjectivity_test_contract_fix/run.ps1 -DryRun` first, then run it without `-DryRun`. The installer checks the reviewed branch ancestry, original SHA-256 digests, and the R57 source guard; unexpected local modifications fail closed.

Full project pytest is not run during this intermediate phase. The runner executes the R57R3 focused tests and then the existing R57 focused and public proof audits.

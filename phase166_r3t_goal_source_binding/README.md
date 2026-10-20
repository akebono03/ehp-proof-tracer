# Phase 166 R3-T goal source binding

This package connects the existing specialized eta-group goal to its canonical registered source assertion. It does not add proof leaves or alter the reference-screening and Toda (4.5) rules.

Run `run.ps1` from the extracted package. It backs up the original module, applies one guarded function replacement and one import, then runs targeted pytest only. The replaced complete function is written to `modified_function.txt`.

This is a scoped connection patch, not proof of pi_5^4. Full pytest is deferred until the end of Phase 166.

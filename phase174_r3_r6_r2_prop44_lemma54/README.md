# EHP Proof Tracer — Phase 174 R3-R6-R2

## Conditional Proposition 4.4 with independently verified Hopf hypothesis

This package removes the Hopf-fibration existence metadata from the cited typed
Proposition 4.4 and requires an independent typed inference for its Hopf
hypothesis. For the public proof of `pi_8^5`, it reconstructs
`H(nu_4)=iota_7` from the source-verified Lemma 5.4, then applies the
conditional Proposition 4.4 to prove suspension injectivity.

The separately printed Chapter IV paragraph immediately preceding Proposition
4.4 says that `E+h_*` is an isomorphism for `n=2,4,8`. It does *not* print an
equation asserting `H(h)=+/-iota`. This independent earlier statement is cited
as such and may support earlier group computations for which Lemma 5.4 is not
available in publication order.

No group structure is added as a new GIVEN. No group-specific narrative branch
or future Phase feature is introduced. The shared proof renderer no longer
manufactures a Hopf-invariant statement about the Hopf fibration projection.

The runner uses reviewed Git blob guards for every modified existing file.
DryRun makes no production changes. A normal run applies full-function/class
replacements, exports the full resulting files and functions to `output/`,
then runs a source-ancestry audit and focused pytest. The complete suite is
reserved for the Phase closeout.

Extract this ZIP in the repository root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r6_r2_prop44_lemma54\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r6_r2_prop44_lemma54\run.ps1"
```

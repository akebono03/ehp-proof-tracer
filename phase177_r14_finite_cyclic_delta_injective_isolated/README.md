# Phase 177 R14 — Isolated finite cyclic Delta injectivity

This package introduces two **isolated** inference rules, without modifying the shared provider, registry, renderer, source files, or root proof. The reviewed develop baseline is `6482605898a83a3007565988c252cb594cef9a1d`. A synchronized descendant is accepted only if all pinned dependencies are unchanged and tracked files are clean.

## Mathematical rules

1. Given a proved explicit direct sum containing a finite cyclic summand $\mathbb{Z}/m\{b\}$, the actual listed generator $b$ has order $m$. The rule uses the existing `FiniteElementOrder` statement and checks exact typed endpoints, distinct explicit cyclic generators, and a positive nontrivial order.
2. Given a proved $A=\mathbb{Z}/m\{a\}$, a typed Delta homomorphism with proved `GeneratorImage` $\Delta(a)=b$, and a proved `FiniteElementOrder` $\operatorname{ord}(b)=m$, the map is injective. Indeed $\Delta(ra)=rb=0$ implies $m\mid r$ and thus $ra=0$. The implementation deliberately supports only valid typed EHP Delta maps in this phase; the group-theoretic implication is general.

No separate nonzero rule is required by these implications. A group label or an expansion is not proof evidence. The matcher requires the exact premise statements, and the image and order must be INFERENCE steps. The ordinary proof-search admission/trust boundary remains responsible for group premise provenance.

## Tests

The generic unit tests use test-only hypothetical premises for orders 2, 4, 8, and 16, including rejection of mismatched maps, dimensions, orders, generators and missing premises. The actual-premise test obtains the lower Delta generator image through the existing public source-first search and verifies its Toda (5.11) leaf. The codomain is obtained through the existing, verified root-context DB admission gate, **not** claimed as an independently successful public search. The test replays the two new rules in isolation using those premises. No synthetic premise is used in this actual-premise test, and the replay is not an accepted root proof.

Run `run.ps1 -DryRun`, then `run.ps1`. Only the two new test files and four existing focused regression files are run. No full pytest, new GIVEN, or provider installation. A PASS is the isolated test gate, not group completion. Public candidate wiring and the codomain admission issue are deferred to the next phase step.

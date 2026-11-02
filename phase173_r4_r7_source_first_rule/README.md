# Phase 173 R4-R7 — Source-first Toda (5.6) Rule Contract

This package introduces a **bounded, isolated** typed inference proposal for `pi_i^4`, where `i` is 8, 9, or 10. It does not install any production search hook, modify the public Web selector, assert a completed public proof, assign a fabricated target publication position, or alter the underlying group database.

## Existing mathematics and trust model

Toda Proposition 4.4 gives the isomorphism

$$
\pi_{i-1}^{3}\oplus\pi_i^{7}\longrightarrow\pi_i^4,
\qquad (\alpha,\beta)\longmapsto E\alpha+\nu_4\circ\beta,
$$

provided the Hopf identity $H(\nu_4)=\iota_7$ is established. The latter is a separately source-verified inference from Toda Lemma 5.4. The previously audited `sphere.csv` presentations for both source groups must be admissible under the existing strict `(stem, sphere dimension)` ordering. Database priors are identified explicitly as adopted premises; they are not passed off as independently proved literature theorems.

The same registered typed eta-generator alias checker is reused, accepting only the two explicitly recognized `η_7` and `η₇` spellings when all generator indices, source/target dimensions, orders, and summand multiplicities agree. No free-form or global name normalization occurs. All four subgoals—Proposition 4.4, both prior groups, and the Hopf identity—remain obligations to the ordinary backward solver.

## Scope and files

New files only, under `phase173_r4_r7_source_first_rule/`:

- `source.py`: isolated, source-hash-verified adoption of Lemma 5.4 under the pre-existing `source-first` selection policy, without a target citation position.
- `rule.py`: bounded generator correspondence and a four-premise, guarded inference proposal.
- `audit.py`: strict source/Git guards, independently run typed searches, and JSON/Markdown reports outside the repository.
- `run.ps1`: focused tests, DryRun, isolated diagnostic search, and the existing public `pi_7^4` regression.
- `tests/test_rule.py`: real-type tests for source identity, guards, generator matching and rejection of invalid priors.
- `監査計画.md`: full Japanese scope and acceptance criteria.

## Execution

From the repository root, after extracting the ZIP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r7_source_first_rule\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r7_source_first_rule\run.ps1"
```

The reviewed `develop` commit is `85e9311c7c71108a60ee52578cdf279add210ce7`. If the commit or a reviewed source file has changed, the runner stops rather than silently overriding its safety checks.

Look for `PHASE173_R4_R7_OUTPUT`. The `audit.json` file reports source-first eligibility, one or zero proposals, isolated proof-search status and actual certified root status for each group. `OBSERVATION_COMPLETE` means the audit ran; it does **not** mean all three groups have a completed proof. Public Web integration belongs to a subsequent step after these conditions have been checked.

Full pytest is deliberately deferred to the close of Phase 173.

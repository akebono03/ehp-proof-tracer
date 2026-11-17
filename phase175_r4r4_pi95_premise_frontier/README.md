# Phase 175 R4R4 — Source-First Premise Frontier Audit for π₉⁵

This package performs a **read-only audit** of the six independent inputs of the isolated rank-two EHP quotient inference introduced in Phase 175 R4R3. It **does not construct a proof of π₉⁵**, create new mathematical rules or GIVEN steps, modify production code, or register a provider.

## Mathematical scope

The isolated inference consumes a verified presentation of the elementary rank-two group $A$, a verified order-two presentation of $C$, a cited and inferred image of the generator under $\Delta$, a proved EHP exactness window, a proved surjectivity statement for $E$, and a proved image of the surviving generator under $E$:

$$
C=\mathbb Z/2\{z\}\xrightarrow{\Delta}
A=\mathbb Z/2\{a\}\oplus\mathbb Z/2\{b\}
\xrightarrow{E} B.
$$

The intended instantiation is $C=\pi_{10}^9$, $A=\pi_8^4$, and $B=\pi_9^5$. The target generator $\nu_5\eta_8$ must **not** be admitted directly as a literature GIVEN.

In particular, Toda Proposition 2.5 includes an **inclusion**, with explicitly qualified conditions allowing equality. The adopted Chapter V transcription includes the relation $\Delta(\iota_9)=\pm(2\nu_4-E\nu')$ and the subsequent computation of $\Delta(\eta_9)$. The printed computation is source evidence, **not** an executable verified `ProofStep`. The order-two summand must justify removal of sign. The suspicious $\pi_8^9$ dimensional notation in the printed exact sequence is not silently corrected or used as a typed statement.

## Inputs and gates

The audit requires the actual successful Phase 175 R4R3 report, with Gate `PASS_R4R3_ISOLATED_RULE_NOT_PUBLIC` and an explicitly incomplete target. It validates the current Git `develop` source pins from Phase 175 R4R2, seven additional reviewed Git blobs (Toda Chapters II and V plus existing rule implementations), and the **exact bytes** of the shipped R4R3 `rule.py`.

A subsequent commit is accepted only if the earlier R4R3 report HEAD remains an ancestor and intervening tracked changes are limited to the isolated R4R3 package or the already-reviewed pytest cache path. Changed mathematical sources fail the source-pin checks, and any changed R4R3 `rule.py` fails the content hash.

The audit validates a correctly indexed $\Delta\to E$ EHP window using the actual project type checker. A well-typed window is **not** a proof of exactness. The six rows in `report.json` explicitly record that R4R4 did not replay any verified parent `ProofStep`.

The expected gates are:

- DryRun: `PASS_R4R4_PREMISE_FRONTIER_DRYRUN`
- Full read-only audit: `PASS_R4R4_PREMISE_FRONTIER_RECORDED_NOT_PUBLIC`

These indicate an **audit only**, not a completed proof. The whole test suite is deferred until the end of Phase 175.

## Run on Windows PowerShell

Extract the ZIP to the root of the existing `ehp_proof` checkout. From the checkout root, run the script as a file (do not paste the contents of `run.ps1` into the console):

```powershell
$script = ".\phase175_r4r4_pi95_premise_frontier\run.ps1"
$r4r3Report = "C:\Users\oomae\AppData\Local\EHPProofTracerAudit\phase175_r4r3_two_summand_quotient\20261117T051236_126038Z\report.json"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -R4R3Report $r4r3Report -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File $script -R4R3Report $r4r3Report
```

The report is written under `%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r4r4_pi95_premise_frontier\<UTC timestamp>`. The script runs a **focused** pytest collection with `--import-mode=importlib` and `-p no:cacheprovider` to avoid the previously observed name collision and modified pytest cache.

## Files

- `audit.py`: actual report, Git pin, Toda source, and EHP-schema verification; six-premise inventory.
- `tests/test_audit.py`: synthetic, fail-closed contracts for the read-only audit.
- `run.ps1`: the focused tests and audit in DryRun or normal mode.
- `AUDIT_PLAN_JA.md`: Japanese audit plan and boundary.
- `TEST_RESULTS_JA.md`: local test evidence and deferred Windows checks.
- `CODE_FULL_JA.md`: complete code of every new executable and test file.

No root-level README, design, development log, roadmap, or proof record is changed in this step.

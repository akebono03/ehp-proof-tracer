# Phase 171 R2J-R4-R9-R20 — cited eta specialization precedence

This narrowly scoped patch repairs a **duplicate derivation** discovered in R19. The public provider independently proposed both `Toda Proposition 5.1 generic higher-eta specialization` and `generic cited typed scalar specialization` from exactly the same earlier citation. The canonical resolver rejects the two distinct proof trees as ambiguous (correctly).

The patch retains the established eta-specific inference and suppresses the generic scalar proposal **only when** the two backward obligations use the identical screened, verified symbolic eta source. Both independent provider APIs, reference screening, the canonical uniqueness check, and Trust Boundary are unchanged.

The ZIP contains the full new source/test/import code and a guarded installer that extracts both the complete original and replacement `shared_expansion_provider` functions into `output/`. These files have no omitted lines. The original shared module is backed up byte-for-byte. The installer refuses a different committed Git blob or an unrelated working edit, is idempotent, and preserves CRLF and UTF-8 BOM when present. It does not run Git mutation commands.

Run `run.ps1 -DryRun` and then `run.ps1` from the extracted folder. The second command performs focused pytest only, followed by an independent read-only proof audit. The entire test suite is intentionally deferred until the Phase closeout.

**Completion boundary:** this patch aims to make the right end group `pi_6^5` unambiguous and then verify its `pi_6^3` cardinality consumer. It does **not** claim that `pi_6^3` group structure or its Web proof is complete; the order-four generator remains a separate obligation.

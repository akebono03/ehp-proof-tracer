Phase 148 RC2-1 Repair R1

Reason for repair
-----------------
The original RC2-1 audit package contained two incorrect audit assertions.

It assumed that the pi_6^3 ESTABLISH_ORDER Argument contained both a primary
exactness component and a separate non-primary recursive component.

The actual audit result shows:

- pi_6^3 ESTABLISH_GROUP_STRUCTURE:
  3 evidence blocks -> 1 component -> primary component 0
- pi_6^3 ESTABLISH_ORDER:
  2 evidence blocks -> 1 component -> primary component 0

Therefore the two failed assertions were audit-harness assumptions, not
production regressions.

The audit also revealed the more important RC2 boundary: exactness evidence
can remain visible when an Argument has evidence but no owned primary
component. Examples include pi_8^5 group structure, pi_10^4 group structure,
pi_12^5 definition, and pi_16^9 arguments.

Changes in this repair
----------------------
Production code changes: none.
Existing repository test changes: none.

This package:
1. replaces the two incorrect RC2-1 package assertions with observations
   supported by the audit output;
2. adds checks for unowned visible recursive evidence;
3. makes the PowerShell runner fail when pytest or Python exits nonzero.

The original audit script is reused unchanged.

Run
---
From the repository root:

powershell -ExecutionPolicy Bypass `
  -File ".\phase148_rc2_1_repair_r1\run_phase148_rc2_1_repair_r1.ps1"

Phase boundary
--------------
RC2-1 remains audit-only.
RC2-2 designs the general exposure-selection rule.
RC3 owns Narrative ordering and is not changed here.
Repository-wide pytest is reserved for the end of Phase 148.

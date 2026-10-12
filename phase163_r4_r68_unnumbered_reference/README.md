# Phase 163 R4-R68: Unnumbered References

This read-only package records the agreed policy: independent unnumbered literature statements get an unnumbered Reference proposal, and each statement receives a separate ordered Assertion proposal. A single Reference may contain multiple Assertions.

## Inputs

From the project root, the package reads `phase163_r4_r66_output/boundary_decisions.json` and `phase163_r4_r67_output/context_review.json`. Run R4-R66 and R4-R67 first. The input phase and provenance gates reject already-registered or semantically approved data.

## Windows execution

Extract this folder into the project root and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase163_r4_r68_unnumbered_reference\run.ps1
```

The script runs six focused pytest tests and writes `phase163_r4_r68_output/unnumbered_reference_proposals.json` and `.md`.

## Scope and limitations

The original sixteen provisional Definition references and twenty-one Assertions are preserved. One additional unnumbered Reference proposal with two Statement Assertions is added from chapter 1, lines 1118–1121. Totals become seventeen Reference proposals and twenty-three Assertion proposals.

The new Reference is tagged `UNNUMBERED_PROPOSAL`; numbering status for preexisting entries remains `NOT_ASSESSED`. No formal identifiers, publication positions, mathematical approvals, original-book verification, migrations, or proof-search changes are performed. The full test suite is reserved for the end of Phase 163.

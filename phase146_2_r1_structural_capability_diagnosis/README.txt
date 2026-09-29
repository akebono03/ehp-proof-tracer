Phase 146-2 R1 Structural Capability Diagnosis

This revision repairs only the diagnostic harness.

Cause of R0 failure
-------------------
`build_standard_toda_report()` returns a `TodaCalculationReportResult`.
The diagnostic incorrectly expected `report.group_results`.

Existing repository tests obtain the selected group result through:

    report.candidates[0].source_candidate.group_result

R1 now uses that established repository access path.

Production changes
------------------
None.

Existing test changes
---------------------
None.

Phase boundary
--------------
This remains diagnosis only. No Narrative routing behavior is changed.

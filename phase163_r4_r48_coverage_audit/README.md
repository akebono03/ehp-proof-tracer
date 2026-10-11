# Phase 163 R4-R48: TeX Coverage Audit

Read-only review of mathematical displays outside the 108 registered TeX environments, prose definition cues, and nested environments. This is not proof of completeness and does not allocate IDs or alter any existing catalog or Registry.

Run `run.ps1` from the project root after extracting this archive. Requires the Phase R4-R47 `catalog.json`, Phase R4-R42 input files and Python with pytest. Outputs are placed under `phase163_r4_r48_output`.

Candidates are **unreviewed**, not confirmed independent statements. `OUTSIDE_DISPLAY` indicates a display outside registered environments. `PROSE_DEFINITION_CUE` is a conservative line-level lexical cue. Nested equations within parent proposition environments remain covered by the previously registered source units. This audit is limited to detectable syntactic forms, not all mathematical prose.

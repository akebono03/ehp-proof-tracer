# Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R3-R4-R2 Read-PopulationCache Restoration Repair

## Confirmed cause

The user's search recovered the original historical-audit implementation of
`Read-PopulationCache` from the earlier R2-R1 package.

The function was located between `Remove-TemporaryWorktree` and
`Write-PopulationCache`.

R4 replaced the complete range from `Remove-TemporaryWorktree` through the
start of `Write-PopulationCache`. That range unintentionally included and
removed `Read-PopulationCache`.

R4-R1 then proved that the scalar exit-code and complete `Measure-Commit`
repair itself is healthy: all 37 focused tests passed. Historical localization
failed only when the script later called the missing helper.

## Changed function

Only the original `Read-PopulationCache` helper is restored.

Insertion position:

immediately before `function Write-PopulationCache {`.

The recovered implementation is preserved without semantic changes:

- returns an empty array when the cache file does not exist;
- reads through `Invoke-WithRetry`;
- stores the read lines in `$script:cacheReadLines`;
- copies those lines into the returned result array.

## Explicitly unchanged

- `Remove-TemporaryWorktree`;
- `Measure-Commit`;
- production code;
- existing project tests;
- collector;
- population cache contents;
- expected historical population 190.

## Focused tests

The new audit-only test verifies:

- exactly one `Read-PopulationCache`;
- exactly one `Write-PopulationCache`;
- exactly one `Measure-Commit`;
- helper order `Read -> Write -> Measure`;
- the recovered cache-read implementation;
- R4 scalar `$addExitCode` remains present;
- `$Expected = 190` remains present.

The runner then executes only the historical-localization audit directory and
resumes localization.

No full project pytest is run.

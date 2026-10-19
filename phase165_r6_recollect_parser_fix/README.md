# Phase 165 R6 recollection parser correction

This package fixes the error-file accounting in an existing pytest collection report without running collection again. The historical parser expected `ERROR collecting` at the beginning of the line, but pytest usually surrounds the header with underscores.

Run `run.ps1` from the repository root after extracting the archive. The script runs four isolated parser tests, validates the count of extracted headers against the pytest summary, saves a timestamped backup of the original `report.json`, and rewrites only `error_file_count`, `error_files`, and parser-specific metadata.

No production source, active test, pytest collection, or full pytest execution is changed or performed. On an inconsistent or missing log, the script fails without modifying the original report.

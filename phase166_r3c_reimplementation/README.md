# Phase 166 R3-C: Publication-order connection before shared namespacing

Run from the repository root after applying R3-B and the R3-C import fix:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase166_r3c_reimplementation.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase166_r3c_reimplementation\run.ps1"
```

This is an incremental repair, not a completed R3-C search-order cutover. The production shared registry now carries original Phase 163 publication positions before adding the `shared:<index>:` namespace. No locator matching, TeX parsing, SQLite, internal proof-order change, or source qualification rule is added.

The public group query still uses the established complete-proof search. Its implicit `assertions[0]` context ID must not be treated as a verified publication-order target. A separate follow-up is required to attach an actual, typed goal position and enable the ordered citation gate safely.

The runner executes focused tests only. It records the patched source as `INSTALLED_SOURCE.py.txt` and a timestamped backup. Full pytest is reserved for Phase closure.

# Phase 169 R10E4R1 — Historical Test Compatibility Repair

This package corrects one outdated R10E2 test assertion that requires the current R10E4 transport module to be byte-for-byte equal to its older R10E2 output. That assumption is invalid once R10E4 intentionally extends the same function.

No production code or mathematical rules are changed by this overlay. The wrapped runner first updates the single historical test, then invokes the **original R10E4 run.ps1**, which patches three production files and runs its focused pytest and audit. A failure restores the test; the original runner restores production files.

## Run

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10e4r1_historical_test_compatibility.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r10e4r1_historical_test_compatibility\run.ps1"
```

The original R10E4 package must already be extracted. Only focused pytest is run. Full-suite pytest is deferred until Phase 169 closeout.

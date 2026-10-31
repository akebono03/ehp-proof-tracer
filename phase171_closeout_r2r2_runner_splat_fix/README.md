# Phase 171 Closeout R2R2 — PowerShell Runner Correction

This package corrects a **single PowerShell argument-splat typo** in the already-extracted Phase 171 R2R1 runner. The previous runner built `$PythonArguments` but launched `python` with the unrelated automatic variable `@Args`, opening an interactive Python shell instead of executing the guarded document updater.

The corrected runner executes `& python @PythonArguments`. The repair checks the original and corrected script hashes and the existing R2 and R2R1 package contents before changing one file. It preserves an exact backup and saves an audit report outside the Git working tree.

No application code, mathematical Proof Tree, or document content is modified by this repair itself. The corrected R2R1 runner then invokes the already-reviewed five-document writer and its focused regression tests. **No full test suite is run.**

## Execute in Windows PowerShell

Unpack `EHP_Phase171_Closeout_R2R2_Runner_Splat_Fix.zip` at the repository root; run `phase171_closeout_r2r2_runner_splat_fix/run.ps1 -DryRun`, followed by the same script without `-DryRun`. Do not run the older R2R1 runner before the correction is applied.

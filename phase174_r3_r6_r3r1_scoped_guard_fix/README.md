# EHP Proof Tracer — Phase 174 R3-R6-R3R1 Scoped Worktree Guard Repair

This package repairs the previously over-broad **whole-file Git blob guard** of
R3-R6-R3. It does not modify search rules, register axioms, or add a
sphere-specific narrative. The previous package is retained unmodified.

## Reviewed baseline and local edits

- GitHub `develop` HEAD: `ecbb2fea225c5b88000629d9c025934fcc2d7075`.
- The two source modules' committed bytes are read from `git show HEAD:path`,
  and their SHA-1 Git blob IDs are pinned to the reviewed GitHub objects.
- The target function's parsed AST and all module-level imports must exactly
  match the reviewed HEAD. Changes inside a target function or its imports
  **block application**.
- Differences elsewhere in the local file are preserved byte for byte,
  including unrelated local work and mixed newline styles. Only the reviewed
  lines are inserted inside the two verified target functions.
- The original R3-R6-R3 `patch.py` and `projection.py` are SHA-256 guarded and
  neither is overwritten by this package.

## Files and scope

- New `patch.py`: complete reviewed function-scoped installer.
- New `tests/test_patch.py`: five regression tests for preservation and failure.
- New `run.ps1`: pinned HEAD guard, DryRun, Apply and focused pytest.
- `output/CODE_FULL_JA.md` is generated during DryRun and contains the two
  complete changed functions. `patch.py` itself contains all new functions.
- No existing import section, class, mathematical rule or citation identity
  is changed.

## Execution

Extract the ZIP at the repository root. Run `run.ps1 -DryRun` first. Only on a
PASS should you run `run.ps1` without parameters. The runner does not invoke
`git reset`, `git clean`, `git pull`, `git checkout` or the full test suite.

If the target function or import differs semantically from HEAD, stop and
inspect `git diff HEAD -- phase168_r3_27_typed_statement_projection.py` (or the
other guarded file). Do not force the patch over an unreviewed edit.

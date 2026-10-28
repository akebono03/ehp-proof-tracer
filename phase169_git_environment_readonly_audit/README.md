# Git Environment Read-Only Audit

This diagnostic examines the Git for Windows working environment of EHP Proof Tracer after a VS Code Git log reported Dropbox conflicted refs and long filenames. It is **not** a Phase 169 production patch.

The `run.ps1` script only reads repository files and invokes non-mutating Git commands with optional locks disabled. It saves results under Windows `%TEMP%`, outside the repository. It does not stage, commit, fetch, restore, delete, configure, or rename any repository data.

Unzip the package under the repository root and run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase169_git_environment_readonly_audit\run.ps1` from the repository root. Read the generated `audit.md` and `audit.json` before attempting any repair.

If needed later, Git for Windows supports `git config --local core.longpaths true`. This audit deliberately does **not** enable it. The official Git for Windows documentation notes that long paths support is limited to some Git commands and does not necessarily fix Windows Explorer or IDE tooling.

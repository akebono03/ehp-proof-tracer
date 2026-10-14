# Phase 165 R27-R18 — Disable hidden legacy generator routes

This package removes direct execution of four hidden legacy generator workflows from the Flask public entry point. It does not delete mathematical statements, generalized inference rules, or historical modules. Group and Operation request paths remain untouched. Template variable names remain available with `None` values.

Run `powershell -ExecutionPolicy Bypass -File .\phase165_r27_r18\run.ps1` from the repository root. The installer saves a backup before changing `web_app.py`. Targeted tests only. Full suite runs at the end of Phase 165.

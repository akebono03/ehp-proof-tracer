# Phase 165 R27-R33-R1 — Group Proof Import Repair

This patch restores the imports required by the already installed R27-R33 typed Web Group Proof entry. It does not replace the proof function, its renderer, or any proof-generating logic.

Run `run.ps1` from the unpacked directory. It performs a safe, idempotent update and runs the five installer tests plus four targeted functional tests. No full pytest run is performed.

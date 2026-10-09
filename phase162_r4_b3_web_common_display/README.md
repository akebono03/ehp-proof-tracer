# Phase 162 R4-B3 Web Common Narrative Display

Connect the R4-B2 derived eta proof replay to the existing Group Proof web display for `pi_5^4` and `pi_6^5` in narrative mode. The baseline common renderer supplies unmodified Markdown, which is converted by the existing web markdown-line parser and displayed by the existing template. This retains known issues (symbolic powers, duplicate transitions, appended prose) rather than inventing replacement proof text.

Changes: a guarded delegation at the start of `build_standard_web_group_proof_view`, new `phase162_r4_b3_web_common_display.py`, and focused tests. The original `web_group_proof.py` is backed up. Other groups and trace/outline mode are unaffected. Full suite is not run.

Run the PowerShell launcher from the project root, then start `python -B web_app.py` or the project's usual Flask launch command and select Group Proof, `n=4` or `n=5`, `k=1`, mode Narrative.

Phase 167 R1 dynamic audit of pi_4^3.
Run from the project root with PowerShell: .\phase167_r1_dynamic_audit\run.ps1
Outputs dynamic_report.json and web_lines.txt in this folder.
No production source edits, no pytest. The Web builder is executed and temporarily instrumented in-process.
If no Reference renderer call occurs, the event log will show only the path actually encountered.

# Phase 166 R3 — Read-only Order Inventory

This package inspects the live production registry and selected assertions related to the low-dimensional EHP proof. It does **not** patch production code, grant citation rights, or generate proofs.

From the project root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase166_r3_order_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase166_r3_order_audit\run.ps1"
```

Output: `phase166_r3_order_audit/results/order_inventory.json`. The tool inspects production discovery data, which might differ from the actual Web route. The inventory therefore does not by itself prove which path the Web uses.

Only three focused tests run. No full pytest is performed.

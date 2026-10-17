"""Run read-only inspection of existing eta-family definition registry links."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r12_r19_eta_definition_audit import inspect_eta_runtime


def main() -> None:
    result = inspect_eta_runtime()
    destination = Path(__file__).resolve().parent / "audit_result.json"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("Audit saved:", destination)


if __name__ == "__main__":
    main()

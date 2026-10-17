"""Run R12-R25 read-only audit from an arbitrary working directory."""
from __future__ import annotations
import json
from pathlib import Path

from phase165_r12_r25_web_order_diagnostic.phase165_r12_r25_web_order_diagnostic import audit_web_order


def main() -> None:
    result = audit_web_order()
    output = Path(__file__).resolve().parent / "audit_result.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k not in ("candidates", "backward", "order")}, ensure_ascii=False, indent=2))
    print("order:", json.dumps(result["order"], ensure_ascii=False, indent=2))
    print("backward:", json.dumps(result["backward"], ensure_ascii=False, indent=2))
    print("Audit saved:", output)


if __name__ == "__main__":
    main()

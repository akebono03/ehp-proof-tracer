"""Read-only Phase 165 R12-R8 command-line report."""
from __future__ import annotations

import json
from phase165_r12_r8_typed_source_connection import audit_real_pi43_quotient_connection


def main() -> None:
    print(json.dumps(audit_real_pi43_quotient_connection(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

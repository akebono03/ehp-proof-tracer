from pathlib import Path

TARGET = Path(
    "phase157_r4_r1_representative_boundary_audit"
) / "audit_phase157_r4_r1.py"

ANCHOR = "from __future__ import annotations\n\n"
INSERT = """from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path.cwd()
if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

"""


def main():
    if not TARGET.exists():
        raise SystemExit(
            "R4-R1 audit script not found. "
            "Apply the original R4-R1 package first."
        )

    text = TARGET.read_text(
        encoding="utf-8"
    )

    if "REPOSITORY_ROOT = Path.cwd()" in text:
        print(
            "R4-R1 import-path repair already applied."
        )
        return

    if not text.startswith(
        ANCHOR
    ):
        raise SystemExit(
            "unexpected R4-R1 audit script header"
        )

    text = (
        INSERT
        + text[
            len(
                ANCHOR
            ):
        ]
    )

    TARGET.write_text(
        text,
        encoding="utf-8",
        newline="\n",
    )

    print(
        "Phase157-R4-R1 repair1 applied."
    )
    print(
        f"updated: {TARGET.resolve()}"
    )
    print(
        "Production code changes: none"
    )


if __name__ == "__main__":
    main()

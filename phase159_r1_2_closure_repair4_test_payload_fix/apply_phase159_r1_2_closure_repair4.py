from __future__ import annotations

import base64
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
TEST = ROOT / "tests" / "test_phase159_r1_2_pi3_2_closure.py"

TEST_PAYLOAD_BASE64 = "ZnJvbSBob21vdG9weV9ncm91cHMgaW1wb3J0ICgKICBUb2RhU3VzcGVuc2lvbklzb21vcnBoaXNtU3RhdGVtZW50LAopCmZyb20gdG9kYV9jYWxjdWxhdGlvbl9mYWNhZGUgaW1wb3J0ICgKICBidWlsZF9zdGFuZGFyZF90b2RhX3JlcG9ydCwKKQpmcm9tIHRvZGFfZ3JvdXBfcHJvb2ZfbmFycmF0aXZlX3JlbmRlcmVyIGltcG9ydCAoCiAgcmVuZGVyX3RvZGFfZ3JvdXBfcHJvb2ZfbmFycmF0aXZlX21hcmtkb3duLAopCmZyb20gdG9kYV9ncm91cF9wcm9vZl9wcmVzZW50YXRpb24gaW1wb3J0ICgKICBidWlsZF90b2RhX2dyb3VwX3Byb29mX3ByZXNlbnRhdGlvbiwKKQpmcm9tIHRvZGFfZ3JvdXBfcmVzdWx0X3Byb29mX3JlcGxheSBpbXBvcnQgKAogIGJ1aWxkX3RvZGFfZ3JvdXBfcmVzdWx0X3Byb29mX3JlcGxheSwKKQpmcm9tIHRvZGFfcnVsZXMgaW1wb3J0ICgKICBUb2RhU3VzcGVuc2lvbkluamVjdGl2ZVN0YXRlbWVudCwKKQoKCmRlZiBfYnVpbGRfcGhhc2UxNTlfcjFfMl9waTNfMl9wcmVzZW50YXRpb24oKToKICByZXBvcnQgPSBidWlsZF9zdGFuZGFyZF90b2RhX3JlcG9ydCgKICAgIG49MiwKICAgIGs9MSwKICApCiAgZ3JvdXBfcmVzdWx0ID0gKAogICAgcmVwb3J0CiAgICAuY2FuZGlkYXRlc1swXQogICAgLnNvdXJjZV9jYW5kaWRhdGUKICAgIC5ncm91cF9yZXN1bHQKICApCiAgcmVwbGF5ID0gYnVpbGRfdG9kYV9ncm91cF9yZXN1bHRfcHJvb2ZfcmVwbGF5KAogICAgZ3JvdXBfcmVzdWx0LAogICAgbWF4X2RlcHRoPTIsCiAgKQoKICByZXR1cm4gYnVpbGRfdG9kYV9ncm91cF9wcm9vZl9wcmVzZW50YXRpb24oCiAgICByZXBsYXkKICApCgoKZGVmIF9yZW5kZXJfcGhhc2UxNTlfcjFfMl9waTNfMigpIC0+IHN0cjoKICBwcmVzZW50YXRpb24gPSAoCiAgICBfYnVpbGRfcGhhc2UxNTlfcjFfMl9waTNfMl9wcmVzZW50YXRpb24oKQogICkKCiAgcmV0dXJuIHJlbmRlcl90b2RhX2dyb3VwX3Byb29mX25hcnJhdGl2ZV9tYXJrZG93bigKICAgIHByZXNlbnRhdGlvbgogICkKCgpkZWYgX3JlY3Vyc2l2ZV9hbmNlc3RyeSgKICBwcm9vZl9zdGVwLAopOgogIG9yZGVyZWQgPSBbXQogIHZpc2l0ZWQgPSBzZXQoKQoKICBkZWYgdmlzaXQoCiAgICBzdGVwLAogICk6CiAgICBzdGVwX2lkID0gaWQoCiAgICAgIHN0ZXAKICAgICkKCiAgICBpZiBzdGVwX2lkIGluIHZpc2l0ZWQ6CiAgICAgIHJldHVybgoKICAgIHZpc2l0ZWQuYWRkKAogICAgICBzdGVwX2lkCiAgICApCiAgICBvcmRlcmVkLmFwcGVuZCgKICAgICAgc3RlcAogICAgKQoKICAgIGZvciBwcmVtaXNlIGluIHN0ZXAucHJlbWlzZXM6CiAgICAgIHZpc2l0KAogICAgICAgIHByZW1pc2UKICAgICAgKQoKICB2aXNpdCgKICAgIHByb29mX3N0ZXAKICApCgogIHJldHVybiB0dXBsZSgKICAgIG9yZGVyZWQKICApCgoKZGVmIHRlc3RfcGhhc2UxNTlfcjFfMl9waTNfMl9vbWl0c19lbXB0eV9yZWZlcmVuY2Vfc2VjdGlvbigpOgogIHJlbmRlcmVkID0gKAogICAgX3JlbmRlcl9waGFzZTE1OV9yMV8yX3BpM18yKCkKICApCgogIGFzc2VydCAiIyMg5L2/55So44GZ44KL57WQ5p6cIiBub3QgaW4gcmVuZGVyZWQKICBhc3NlcnQgIiMjIOiovOaYjiIgaW4gcmVuZGVyZWQKCgpkZWYgdGVzdF9waGFzZTE1OV9yMV8yX3BpM18yX2RlcGVuZGVuY3lfZXhpc3RzX2luX3JlY3Vyc2l2ZV9hbmNlc3RyeSgpOgogIHByZXNlbnRhdGlvbiA9ICgKICAgIF9idWlsZF9waGFzZTE1OV9yMV8yX3BpM18yX3ByZXNlbnRhdGlvbigpCiAgKQogIGFuY2VzdHJ5ID0gKAogICAgX3JlY3Vyc2l2ZV9hbmNlc3RyeSgKICAgICAgcHJlc2VudGF0aW9uLnJvb3Rfc3RlcAogICAgKQogICkKCiAgaW5qZWN0aXZlX3N0ZXAgPSBuZXh0KAogICAgc3RlcAogICAgZm9yIHN0ZXAgaW4gYW5jZXN0cnkKICAgIGlmIGlzaW5zdGFuY2UoCiAgICAgIHN0ZXAuY29uY2x1c2lvbiwKICAgICAgVG9kYVN1c3BlbnNpb25JbmplY3RpdmVTdGF0ZW1lbnQsCiAgICApCiAgKQoKICBhc3NlcnQgYW55KAogICAgKAogICAgICBpc2luc3RhbmNlKAogICAgICAgIHByZW1pc2UuY29uY2x1c2lvbiwKICAgICAgICBUb2RhU3VzcGVuc2lvbklzb21vcnBoaXNtU3RhdGVtZW50LAogICAgICApCiAgICAgIGFuZCBwcmVtaXNlLmNvbmNsdXNpb24ubWFwCiAgICAgID09IGluamVjdGl2ZV9zdGVwLmNvbmNsdXNpb24ubWFwCiAgICApCiAgICBmb3IgcHJlbWlzZSBpbiBpbmplY3RpdmVfc3RlcC5wcmVtaXNlcwogICkKCgpkZWYgdGVzdF9waGFzZTE1OV9yMV8yX3BpM18yX3Nob3dzX2lzb21vcnBoaXNtX2JlZm9yZV9pbmplY3Rpdml0eSgpOgogIHJlbmRlcmVkID0gKAogICAgX3JlbmRlcl9waGFzZTE1OV9yMV8yX3BpM18yKCkKICApCgogIGlzb21vcnBoaXNtID0gKAogICAgIiRFOiBcXHBpX3sxfV57MX0gXFx0byAiCiAgICAiXFxwaV97Mn1eezJ9JCDjga/lkIzlnovlhpnlg4/jgafjgYLjgosuIgogICkKICBpbmplY3Rpdml0eSA9ICgKICAgICIkRTogXFxwaV97MX1eezF9IFxcdG8gIgogICAgIlxccGlfezJ9XnsyfSQg44Gv5Y2Y5bCE44Gn44GC44KLLiIKICApCgogIGFzc2VydCBpc29tb3JwaGlzbSBpbiByZW5kZXJlZAogIGFzc2VydCBpbmplY3Rpdml0eSBpbiByZW5kZXJlZAogIGFzc2VydCAoCiAgICByZW5kZXJlZC5pbmRleCgKICAgICAgaXNvbW9ycGhpc20KICAgICkKICAgIDwgcmVuZGVyZWQuaW5kZXgoCiAgICAgIGluamVjdGl2aXR5CiAgICApCiAgKQogIGFzc2VydCAoCiAgICAi44GX44Gf44GM44Gj44GmLCAiCiAgICArIGluamVjdGl2aXR5CiAgKSBpbiByZW5kZXJlZAo="


def main() -> int:
    if not TEST.is_file():
        raise RuntimeError(
            f"missing test file: {TEST}"
        )

    test_content = base64.b64decode(
        TEST_PAYLOAD_BASE64
    ).decode(
        "utf-8"
    )

    compile(
        test_content,
        str(TEST),
        "exec",
    )

    backup = ROOT / (
        "phase159_r1_2_closure_repair4_backup_"
        + datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
    )
    backup.mkdir(
        parents=True,
        exist_ok=False,
    )
    shutil.copy2(
        TEST,
        backup / TEST.name,
    )

    TEST.write_text(
        test_content,
        encoding="utf-8",
        newline="\n",
    )

    print(
        "Phase 159-R1-2 closure repair4 applied."
    )
    print(
        "Production code changes: none"
    )
    print(
        "Test-only payload/escape correction:"
    )
    print(
        "  tests/test_phase159_r1_2_pi3_2_closure.py"
    )
    print(
        "Backup:",
        backup,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )

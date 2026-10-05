from __future__ import annotations

import ast
import base64
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
FUNCTION_NAME = "_phase158_normalize_public_narrative_contract"
FUNCTION_PAYLOAD_BASE64 = "ZGVmIF9waGFzZTE1OF9ub3JtYWxpemVfcHVibGljX25hcnJhdGl2ZV9jb250cmFjdCgKICBwcmVzZW50YXRpb246IFRvZGFHcm91cFByb29mUHJlc2VudGF0aW9uLAogIHJlbmRlcmVkOiBzdHIsCikgLT4gc3RyOgogIGlmIG5vdCBpc2luc3RhbmNlKAogICAgcHJlc2VudGF0aW9uLAogICAgVG9kYUdyb3VwUHJvb2ZQcmVzZW50YXRpb24sCiAgKToKICAgIHJhaXNlIFR5cGVFcnJvcigKICAgICAgInByZXNlbnRhdGlvbiBtdXN0IGJlIGEgIgogICAgICAiVG9kYUdyb3VwUHJvb2ZQcmVzZW50YXRpb24iCiAgICApCgogIGlmIG5vdCBpc2luc3RhbmNlKAogICAgcmVuZGVyZWQsCiAgICBzdHIsCiAgKToKICAgIHJhaXNlIFR5cGVFcnJvcigKICAgICAgInJlbmRlcmVkIG11c3QgYmUgYSBzdHIiCiAgICApCgogIGlmIHByZXNlbnRhdGlvbi5tYXhfZGVwdGggPCAyOgogICAgcmV0dXJuIHJlbmRlcmVkCgogIHRpdGxlID0gIiMgR3JvdXAgcHJvb2YgbmFycmF0aXZlIgogIHRhcmdldF9oZWFkZXIgPSAiIyMg6Ki85piO5a++6LGhIgogIHJlZmVyZW5jZV9oZWFkZXIgPSAiIyMg5L2/55So44GZ44KL57WQ5p6cIgogIHNlcGFyYXRvciA9ICItLS0iCiAgcHJvb2ZfaGVhZGVyID0gIiMjIOiovOaYjiIKICBxZWQgPSAi4pahIgoKICBzb3VyY2VfbGluZXMgPSAoCiAgICByZW5kZXJlZC5yc3RyaXAoKS5zcGxpdGxpbmVzKCkKICApCgogIGlmICgKICAgIHNvdXJjZV9saW5lcwogICAgYW5kIHNvdXJjZV9saW5lc1swXSA9PSB0aXRsZQogICk6CiAgICBjb250ZW50X2xpbmVzID0gc291cmNlX2xpbmVzWzE6XQogIGVsc2U6CiAgICBjb250ZW50X2xpbmVzID0gc291cmNlX2xpbmVzWzpdCgogIHdoaWxlICgKICAgIGNvbnRlbnRfbGluZXMKICAgIGFuZCBub3QgY29udGVudF9saW5lc1swXS5zdHJpcCgpCiAgKToKICAgIGNvbnRlbnRfbGluZXMucG9wKDApCgogIGRlZiBleGFjdF9pbmRleCgKICAgIG1hcmtlcjogc3RyLAogICkgLT4gaW50IHwgTm9uZToKICAgIHRyeToKICAgICAgcmV0dXJuIGNvbnRlbnRfbGluZXMuaW5kZXgoCiAgICAgICAgbWFya2VyCiAgICAgICkKICAgIGV4Y2VwdCBWYWx1ZUVycm9yOgogICAgICByZXR1cm4gTm9uZQoKICB0YXJnZXRfaW5kZXggPSBleGFjdF9pbmRleCgKICAgIHRhcmdldF9oZWFkZXIKICApCiAgcmVmZXJlbmNlX2luZGV4ID0gZXhhY3RfaW5kZXgoCiAgICByZWZlcmVuY2VfaGVhZGVyCiAgKQogIHByb29mX2luZGV4ID0gZXhhY3RfaW5kZXgoCiAgICBwcm9vZl9oZWFkZXIKICApCgogIGlmIHRhcmdldF9pbmRleCBpcyBub3QgTm9uZToKICAgIHRhcmdldF9lbmRfY2FuZGlkYXRlcyA9IFsKICAgICAgaW5kZXgKICAgICAgZm9yIGluZGV4IGluICgKICAgICAgICByZWZlcmVuY2VfaW5kZXgsCiAgICAgICAgcHJvb2ZfaW5kZXgsCiAgICAgICAgbGVuKAogICAgICAgICAgY29udGVudF9saW5lcwogICAgICAgICksCiAgICAgICkKICAgICAgaWYgKAogICAgICAgIGluZGV4IGlzIG5vdCBOb25lCiAgICAgICAgYW5kIGluZGV4ID4gdGFyZ2V0X2luZGV4CiAgICAgICkKICAgIF0KICAgIHRhcmdldF9lbmQgPSBtaW4oCiAgICAgIHRhcmdldF9lbmRfY2FuZGlkYXRlcwogICAgKQogICAgdGFyZ2V0X2JvZHkgPSBjb250ZW50X2xpbmVzWwogICAgICB0YXJnZXRfaW5kZXggKyAxOgogICAgICB0YXJnZXRfZW5kCiAgICBdCiAgZWxzZToKICAgIHRhcmdldF9ib2R5ID0gKAogICAgICBfcGhhc2UxNThfcHVibGljX25hcnJhdGl2ZV90YXJnZXRfbGluZXMoCiAgICAgICAgcHJlc2VudGF0aW9uCiAgICAgICkKICAgICkKCiAgd2hpbGUgKAogICAgdGFyZ2V0X2JvZHkKICAgIGFuZCBub3QgdGFyZ2V0X2JvZHlbMF0uc3RyaXAoKQogICk6CiAgICB0YXJnZXRfYm9keS5wb3AoMCkKCiAgd2hpbGUgKAogICAgdGFyZ2V0X2JvZHkKICAgIGFuZCBub3QgdGFyZ2V0X2JvZHlbLTFdLnN0cmlwKCkKICApOgogICAgdGFyZ2V0X2JvZHkucG9wKCkKCiAgcmVmZXJlbmNlX2JvZHk6IGxpc3Rbc3RyXSA9IFtdCgogIGlmICgKICAgIHJlZmVyZW5jZV9pbmRleCBpcyBub3QgTm9uZQogICAgYW5kIHByb29mX2luZGV4IGlzIG5vdCBOb25lCiAgICBhbmQgcmVmZXJlbmNlX2luZGV4IDwgcHJvb2ZfaW5kZXgKICApOgogICAgcmVmZXJlbmNlX2JvZHkgPSBjb250ZW50X2xpbmVzWwogICAgICByZWZlcmVuY2VfaW5kZXggKyAxOgogICAgICBwcm9vZl9pbmRleAogICAgXQoKICB3aGlsZSAoCiAgICByZWZlcmVuY2VfYm9keQogICAgYW5kIG5vdCByZWZlcmVuY2VfYm9keVswXS5zdHJpcCgpCiAgKToKICAgIHJlZmVyZW5jZV9ib2R5LnBvcCgwKQoKICB3aGlsZSAoCiAgICByZWZlcmVuY2VfYm9keQogICAgYW5kIG5vdCByZWZlcmVuY2VfYm9keVstMV0uc3RyaXAoKQogICk6CiAgICByZWZlcmVuY2VfYm9keS5wb3AoKQoKICBpZiAoCiAgICByZWZlcmVuY2VfYm9keQogICAgYW5kIHJlZmVyZW5jZV9ib2R5Wy0xXS5zdHJpcCgpCiAgICA9PSBzZXBhcmF0b3IKICApOgogICAgcmVmZXJlbmNlX2JvZHkucG9wKCkKCiAgICB3aGlsZSAoCiAgICAgIHJlZmVyZW5jZV9ib2R5CiAgICAgIGFuZCBub3QgcmVmZXJlbmNlX2JvZHlbLTFdLnN0cmlwKCkKICAgICk6CiAgICAgIHJlZmVyZW5jZV9ib2R5LnBvcCgpCgogIGlmIHByb29mX2luZGV4IGlzIG5vdCBOb25lOgogICAgcHJvb2ZfYm9keSA9IGNvbnRlbnRfbGluZXNbCiAgICAgIHByb29mX2luZGV4ICsgMToKICAgIF0KICBlbGlmICgKICAgIHRhcmdldF9pbmRleCBpcyBOb25lCiAgICBhbmQgcmVmZXJlbmNlX2luZGV4IGlzIE5vbmUKICApOgogICAgcHJvb2ZfYm9keSA9IGNvbnRlbnRfbGluZXNbOl0KICBlbHNlOgogICAgcHJvb2ZfYm9keSA9IFtdCgogIHdoaWxlICgKICAgIHByb29mX2JvZHkKICAgIGFuZCBub3QgcHJvb2ZfYm9keVswXS5zdHJpcCgpCiAgKToKICAgIHByb29mX2JvZHkucG9wKDApCgogIHByb29mX2JvZHkgPSAoCiAgICBfcGhhc2UxNThfc3RyaXBfdGVybWluYWxfcWVkX2xpbmVzKAogICAgICBwcm9vZl9ib2R5CiAgICApCiAgKQogIHByb29mX2JvZHkgPSAoCiAgICBfcGhhc2UxNThfbm9ybWFsaXplX3B1YmxpY19lcXVhdGlvbl9udW1iZXJzKAogICAgICBwcm9vZl9ib2R5CiAgICApCiAgKQogIHByb29mX2JvZHkgPSAoCiAgICBfcGhhc2UxNTlfcmVzdG9yZV9pc29tb3JwaGlzbV90b19pbmplY3RpdmVfZGVwZW5kZW5jeV92aXNpYmlsaXR5KAogICAgICBwcmVzZW50YXRpb24sCiAgICAgIHByb29mX2JvZHksCiAgICApCiAgKQoKICBsaW5lcyA9IFsKICAgIHRpdGxlLAogICAgIiIsCiAgICB0YXJnZXRfaGVhZGVyLAogICAgIiIsCiAgICAqdGFyZ2V0X2JvZHksCiAgICAiIiwKICBdCgogIGlmIHJlZmVyZW5jZV9ib2R5OgogICAgbGluZXMuZXh0ZW5kKAogICAgICAoCiAgICAgICAgcmVmZXJlbmNlX2hlYWRlciwKICAgICAgICAiIiwKICAgICAgICAqcmVmZXJlbmNlX2JvZHksCiAgICAgICAgIiIsCiAgICAgICAgc2VwYXJhdG9yLAogICAgICAgICIiLAogICAgICApCiAgICApCgogIGxpbmVzLmV4dGVuZCgKICAgICgKICAgICAgcHJvb2ZfaGVhZGVyLAogICAgICAiIiwKICAgICAgKnByb29mX2JvZHksCiAgICAgICIiLAogICAgICBxZWQsCiAgICApCiAgKQoKICBub3JtYWxpemVkID0gKAogICAgIlxuIi5qb2luKAogICAgICBsaW5lcwogICAgKS5yc3RyaXAoKQogICAgKyAiXG4iCiAgKQoKICByZXR1cm4gKAogICAgX3BoYXNlMTM2X2NvbXBhY3RfZXRhX3Bvd2VycygKICAgICAgbm9ybWFsaXplZAogICAgKQogICkK"


def _function_range(
    source: str,
    function_name: str,
) -> tuple[int, int]:
    tree = ast.parse(
        source
    )
    lines = source.splitlines(
        keepends=True
    )
    offsets = [0]
    total = 0

    for line in lines:
        total += len(
            line
        )
        offsets.append(
            total
        )

    for node in tree.body:
        if (
            isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
            and node.name == function_name
        ):
            start = offsets[
                node.lineno - 1
            ]
            end = offsets[
                node.end_lineno
            ]

            while (
                end < len(
                    source
                )
                and source[
                    end:end + 1
                ] == "\n"
            ):
                end += 1

            return (
                start,
                end,
            )

    raise RuntimeError(
        f"function not found: {function_name}"
    )


def main() -> int:
    if not RENDERER.is_file():
        raise RuntimeError(
            f"missing production file: {RENDERER}"
        )

    source = RENDERER.read_text(
        encoding="utf-8"
    )
    compile(
        source,
        str(RENDERER),
        "exec",
    )

    replacement = base64.b64decode(
        FUNCTION_PAYLOAD_BASE64
    ).decode(
        "utf-8"
    )
    compile(
        replacement,
        FUNCTION_NAME,
        "exec",
    )

    if (
        "_phase159_restore_isomorphism_to_injective_dependency_visibility"
        not in source
    ):
        raise RuntimeError(
            "repair2 dependency helper is missing"
        )

    start, end = _function_range(
        source,
        FUNCTION_NAME,
    )

    updated = (
        source[:start]
        + replacement.rstrip()
        + "\n\n"
        + source[end:]
    )

    compile(
        updated,
        str(RENDERER),
        "exec",
    )

    backup = ROOT / (
        "phase159_r1_2_closure_repair5_backup_"
        + datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
    )
    backup.mkdir(
        parents=True,
        exist_ok=False,
    )
    shutil.copy2(
        RENDERER,
        backup / RENDERER.name,
    )

    RENDERER.write_text(
        updated,
        encoding="utf-8",
        newline="\n",
    )

    print(
        "Phase 159-R1-2 closure repair5 applied."
    )
    print(
        "Production:"
    )
    print(
        "  toda_group_proof_narrative_renderer.py"
    )
    print(
        "  _phase158_normalize_public_narrative_contract"
    )
    print(
        "Tests changed: none"
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

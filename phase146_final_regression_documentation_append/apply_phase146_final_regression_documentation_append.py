from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent

APPENDS = {
  "docs/development_log.md": """
## Phase 146 final repository-wide regression

Test Performance Repair 1〜9 後の repository-wide final:

```text
10306 passed in 1304.31s (0:21:44)
```

Phase 146 完了。
""",
  "docs/proof_records.md": """
## final verification record

Test Performance Repair 1〜9 後の repository-wide final:

```text
10306 passed in 1304.31s (0:21:44)
```

この結果を Phase 146 の final regression boundary とする。
""",
}

REQUIRED_MARKERS = {
  "docs/development_log.md": "Phase 147 以降は6 root causes を依存順に1件ずつ扱う。",
  "docs/proof_records.md": "historical $\\pi_6^3$ の文字列を直接 special case として\n埋め込まない。",
}

RESULT = "10306 passed in 1304.31s (0:21:44)"


def main():
  for relative_path, append_text in APPENDS.items():
    path = ROOT / relative_path
    data = path.read_bytes()
    text = data.decode(
      "utf-8",
      errors="strict",
    )

    if RESULT in text:
      raise SystemExit(
        f"ABORT: final regression result already exists in {relative_path}"
      )

    marker = REQUIRED_MARKERS[
      relative_path
    ]
    if marker not in text:
      raise SystemExit(
        f"ABORT: Phase 146 closure marker not found in {relative_path}"
      )

    newline = "\r\n" if b"\r\n" in data else "\n"
    normalized_append = append_text.strip("\n").replace(
      "\n",
      newline,
    )

    if not text.endswith(
      (
        "\n",
        "\r\n",
      )
    ):
      normalized_append = newline + normalized_append

    new_text = text.rstrip(
      "\r\n"
    ) + newline + newline + normalized_append + newline
    path.write_bytes(
      new_text.encode(
        "utf-8",
      )
    )

    print(
      "Appended final regression:",
      relative_path,
    )
    print(
      "Preserved newline:",
      "CRLF" if newline == "\r\n" else "LF",
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

from pathlib import Path

TARGET = Path(
  "phase150_rc4_7b_2_intermediate_conclusion_handoff_audit"
  "/audit_phase150_rc4_7b_2.py"
)

OLD = """    for consumer in (
      proof_consumers.get(
        step_id,
        ()
      )
      + semantic_consumers.get(
        step_id,
        ()
      )
    ):
"""

NEW = """    for consumer in (
      tuple(
        proof_consumers.get(
          step_id,
          ()
        )
      )
      + tuple(
        semantic_consumers.get(
          step_id,
          ()
        )
      )
    ):
"""


def main():
  text = TARGET.read_text(
    encoding="utf-8"
  )

  if OLD in text:
    TARGET.write_text(
      text.replace(
        OLD,
        NEW,
        1,
      ),
      encoding="utf-8",
    )
    print(
      "RC4-7B-2 audit harness list/tuple repair applied."
    )
    print(
      "Production files were not changed."
    )
    return

  if NEW in text:
    print(
      "RC4-7B-2 audit harness repair is already applied."
    )
    return

  raise SystemExit(
    "Target audit-harness block was not found; no file was changed."
  )


if __name__ == "__main__":
  main()

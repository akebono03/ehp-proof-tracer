from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_reason_renderer.py"
)
BACKUP = (
  REPO_ROOT
  / "phase154_r4_semantic_duplication_transition_refinement"
  / "backup_before_r4"
  / TARGET.name
)

FUNCTION = 'def insert_toda_group_proof_narrative_reason_prose(\n  markdown: str,\n  reason_sidecar: TodaGroupProofNarrativeReasonSidecar,\n) -> str:\n  if not isinstance(markdown, str):\n    raise TypeError("markdown must be a str")\n  if not isinstance(\n    reason_sidecar,\n    TodaGroupProofNarrativeReasonSidecar,\n  ):\n    raise TypeError(\n      "reason_sidecar must be a "\n      "TodaGroupProofNarrativeReasonSidecar"\n    )\n\n  rendered = markdown\n  emitted_final_result_sentences = set()\n\n  for reason in reason_sidecar.reasons:\n    sentence = render_toda_group_proof_narrative_reason_sentence(\n      reason\n    )\n    if sentence is None:\n      continue\n\n    if (\n      reason.kind\n      is TodaGroupProofNarrativeReasonKind\n      .FINAL_RESULT_DERIVATION\n    ):\n      if sentence in emitted_final_result_sentences:\n        continue\n\n      emitted_final_result_sentences.add(\n        sentence\n      )\n\n    insertion_index = (\n      _toda_group_proof_narrative_reason_insertion_index(\n        rendered,\n        reason,\n        reason_sidecar,\n      )\n    )\n    if insertion_index is None:\n      continue\n\n    prefix = sentence + "\\n\\n"\n    if rendered[\n      max(0, insertion_index - len(prefix)):\n      insertion_index\n    ] == prefix:\n      continue\n\n    rendered = (\n      rendered[:insertion_index]\n      + prefix\n      + rendered[insertion_index:]\n    )\n\n  return rendered\n'


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
  marker = (
    "def "
    + name
    + "("
  )
  start = source.find(
    marker
  )

  if start < 0:
    raise RuntimeError(
      "function not found: "
      + name
    )

  next_def = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_def < 0:
    suffix = ""
  else:
    suffix = source[
      next_def + 1:
    ]

  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n\n"
    + suffix
  )


def main() -> int:
  if not TARGET.exists():
    raise RuntimeError(
      "missing production file: "
      + str(
        TARGET
      )
    )

  BACKUP.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    TARGET,
    BACKUP,
  )

  source = TARGET.read_text(
    encoding="utf-8",
  )
  source = replace_function(
    source,
    "insert_toda_group_proof_narrative_reason_prose",
    FUNCTION,
  )
  TARGET.write_text(
    source,
    encoding="utf-8",
  )

  test_source = (
    Path(__file__).resolve().parent
    / "tests"
    / "test_phase154_r4_semantic_duplication_transition_refinement.py"
  )
  test_target = (
    REPO_ROOT
    / "tests"
    / "test_phase154_r4_semantic_duplication_transition_refinement.py"
  )
  shutil.copy2(
    test_source,
    test_target,
  )

  print(
    "updated:",
    TARGET.name,
  )
  print(
    "added:",
    test_target.relative_to(
      REPO_ROOT
    ),
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

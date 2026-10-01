from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent
BACKUP_ROOT = PACKAGE_ROOT / "backup_before_repair1"


def backup(path: Path) -> None:
  relative = path.relative_to(REPO_ROOT)
  target = BACKUP_ROOT / relative
  target.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    path,
    target,
  )


def replace_required(
  path: Path,
  old: str,
  new: str,
  label: str,
) -> None:
  if not path.exists():
    raise RuntimeError(
      "missing file: " + str(path)
    )

  text = path.read_text(
    encoding="utf-8",
  )

  if old in text:
    backup(path)
    path.write_text(
      text.replace(
        old,
        new,
      ),
      encoding="utf-8",
    )
    print(
      "updated:",
      label,
    )
    return

  if new in text:
    print(
      "already-current:",
      label,
    )
    return

  raise RuntimeError(
    "neither old nor new pattern found for "
    + label
  )


def main() -> int:
  phase149 = (
    REPO_ROOT
    / "tests"
    / "test_phase149_rc3_3_minimal_ordering.py"
  )

  replace_required(
    phase149,
    'assert "(1) と (2) より、" in rendered',
    'assert "(1) と (2) より, " in rendered',
    "Phase 149 numbered derivation punctuation",
  )

  phase150_visible = (
    REPO_ROOT
    / "tests"
    / "test_phase150_rc4_5_visible_reasons.py"
  )

  old_function = '''@pytest.mark.parametrize("_label,n,k", CASES)
def test_phase150_rc4_5_visible_reason_count_matches_typed_reason_count(
  _label,
  n,
  k,
):
  (
    presentation,
    semantic_sidecar,
    reason_sidecar,
    rendered,
  ) = _render_case(n, k)

  expected_sentences = tuple(
    sentence
    for reason in reason_sidecar.reasons
    for sentence in (
      render_toda_group_proof_narrative_reason_sentence(reason),
    )
    if sentence is not None
  )
  expected_sentence_counts = {
    sentence: expected_sentences.count(sentence)
    for sentence in dict.fromkeys(
      expected_sentences
    )
  }

  for sentence, expected_count in expected_sentence_counts.items():
    assert rendered.count(sentence) == expected_count
'''

  new_function = '''@pytest.mark.parametrize("_label,n,k", CASES)
def test_phase150_rc4_5_visible_reason_count_matches_current_deduplication_contract(
  _label,
  n,
  k,
):
  (
    presentation,
    semantic_sidecar,
    reason_sidecar,
    rendered,
  ) = _render_case(n, k)

  sentence_reasons = {}

  for reason in reason_sidecar.reasons:
    sentence = (
      render_toda_group_proof_narrative_reason_sentence(
        reason
      )
    )

    if sentence is None:
      continue

    sentence_reasons.setdefault(
      sentence,
      [],
    ).append(
      reason
    )

  for sentence, reasons in sentence_reasons.items():
    if any(
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .FINAL_RESULT_DERIVATION
      for reason in reasons
    ):
      assert rendered.count(
        sentence
      ) == 1
      continue

    assert rendered.count(
      sentence
    ) == len(
      reasons
    )
'''

  replace_required(
    phase150_visible,
    old_function,
    new_function,
    "Phase 150 visible-reason deduplication expectation",
  )

  phase150_vocab = (
    REPO_ROOT
    / "tests"
    / "test_phase150_rc4_7d_generic_reason_vocabulary.py"
  )

  if not phase150_vocab.exists():
    raise RuntimeError(
      "missing file: "
      + str(
        phase150_vocab
      )
    )

  text = phase150_vocab.read_text(
    encoding="utf-8",
  )
  updated = text.replace(
    "、",
    ", ",
  )

  if updated != text:
    backup(phase150_vocab)
    phase150_vocab.write_text(
      updated,
      encoding="utf-8",
    )
    print(
      "updated: Phase 150 generic reason vocabulary punctuation"
    )
  else:
    print(
      "already-current: Phase 150 generic reason vocabulary punctuation"
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

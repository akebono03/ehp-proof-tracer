from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_repair1"
BACKUP.mkdir(exist_ok=True)

REFERENCES = ROOT / "toda_group_proof_narrative_references.py"
CONTRIBUTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
R11_TEST = ROOT / "tests" / "test_phase157_r11_reference_reason_punctuation.py"


def backup(path: Path) -> None:
  destination = BACKUP / path.name
  if not destination.exists():
    shutil.copy2(
      path,
      destination,
    )


for path in (
  REFERENCES,
  CONTRIBUTION,
  R11_TEST,
):
  backup(path)


def replace_function_slice(
  path: Path,
  start_marker: str,
  end_marker: str,
  transform,
  label: str,
) -> None:
  text = path.read_text(
    encoding="utf-8"
  )
  start = text.find(
    start_marker
  )
  end = text.find(
    end_marker,
    start,
  )

  if start < 0 or end < 0:
    raise RuntimeError(
      f"could not locate function slice for {label}"
    )

  old_slice = text[
    start:end
  ]
  new_slice = transform(
    old_slice
  )

  if new_slice == old_slice:
    print(
      f"Already applied or no change needed: {label}"
    )
    return

  path.write_text(
    text[
      :start
    ]
    + new_slice
    + text[
      end:
    ],
    encoding="utf-8",
  )
  print(
    f"Applied: {label}"
  )


def transform_restore_function(
  function_text: str,
) -> str:
  text = function_text

  old_signature = '''  used_step_ids: frozenset[
    int
  ],
) -> tuple[
'''
  new_signature = '''  used_step_ids: frozenset[
    int
  ],
  presentation: TodaGroupProofPresentation | None = None,
) -> tuple[
'''

  if new_signature not in text:
    if old_signature not in text:
      raise RuntimeError(
        "restore function signature anchor not found"
      )
    text = text.replace(
      old_signature,
      new_signature,
      1,
    )

  old_validation = '''  if not isinstance(
    used_step_ids,
    frozenset,
  ):
    raise TypeError(
      "used_step_ids must be a frozenset"
    )

  retained_reference_keys = {
'''
  new_validation = '''  if not isinstance(
    used_step_ids,
    frozenset,
  ):
    raise TypeError(
      "used_step_ids must be a frozenset"
    )

  if (
    presentation is not None
    and not isinstance(
      presentation,
      TodaGroupProofPresentation,
    )
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation or None"
    )

  retained_reference_keys = {
'''

  if new_validation not in text:
    if old_validation not in text:
      raise RuntimeError(
        "restore function validation anchor not found"
      )
    text = text.replace(
      old_validation,
      new_validation,
      1,
    )

  old_desired = '''  desired_entries = []

  for entry in original_entries:
    has_selected_statement = (
'''
  new_desired = '''  reference_internal_step_ids = {
    id(
      proof_step
    )
    for entry in original_entries
    for proof_step in entry.proof_steps
    if proof_step is not root_step
  }
  consumers_by_step_id = {}

  if presentation is not None:
    for edge in presentation.edges:
      consumers_by_step_id.setdefault(
        id(
          edge.premise_step
        ),
        [],
      ).append(
        edge.parent_step
      )

  desired_entries = []

  for entry in original_entries:
    has_selected_statement = (
'''

  if new_desired not in text:
    if old_desired not in text:
      raise RuntimeError(
        "restore function desired_entries anchor not found"
      )
    text = text.replace(
      old_desired,
      new_desired,
      1,
    )

  old_used = '''    is_used_fixed_reference = (
      has_selected_statement
      and any(
        id(
          proof_step
        )
        in used_step_ids
        for proof_step in entry.proof_steps
      )
    )
'''
  new_used = '''    is_used_fixed_reference = (
      has_selected_statement
      and any(
        id(
          proof_step
        )
        in used_step_ids
        and (
          presentation is None
          or any(
            consumer is root_step
            or id(
              consumer
            )
            not in reference_internal_step_ids
            for consumer in consumers_by_step_id.get(
              id(
                proof_step
              ),
              (),
            )
          )
        )
        for proof_step in entry.proof_steps
      )
    )
'''

  if new_used not in text:
    if old_used not in text:
      raise RuntimeError(
        "restore function is_used_fixed_reference anchor not found"
      )
    text = text.replace(
      old_used,
      new_used,
      1,
    )

  return text


replace_function_slice(
  REFERENCES,
  "def restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage(\n",
  "\ndef render_toda_group_proof_narrative_reference_entries_markdown(\n",
  transform_restore_function,
  "restore fixed Reference entries with ancestry-only pruning",
)


def patch_restore_call() -> None:
  text = CONTRIBUTION.read_text(
    encoding="utf-8"
  )

  old = '''        presentation.root_step,
        generic_used_step_ids,
      )
'''
  new = '''        presentation.root_step,
        generic_used_step_ids,
        presentation=presentation,
      )
'''

  if new in text:
    print(
      "Already applied: pass presentation to fixed-Reference restoration"
    )
    return

  count = text.count(
    old
  )

  if count != 1:
    raise RuntimeError(
      "expected exactly one restore call tail, "
      f"found {count}"
    )

  CONTRIBUTION.write_text(
    text.replace(
      old,
      new,
      1,
    ),
    encoding="utf-8",
  )

  print(
    "Applied: pass presentation to fixed-Reference restoration"
  )


patch_restore_call()


def append_tests() -> None:
  text = R11_TEST.read_text(
    encoding="utf-8"
  )
  additions = []

  if (
    "def test_phase157_r11_r14_eta3_cube_order_follows_injectivity():"
    not in text
  ):
    additions.append(
      r'''


def test_phase157_r11_r14_eta3_cube_order_follows_injectivity():
  _, body = _reference_and_body()

  injectivity = (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である."
  )
  eta_cube_order = (
    r"$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$."
  )

  assert injectivity in body
  assert eta_cube_order in body
  assert body.index(
    injectivity
  ) < body.index(
    eta_cube_order
  )
'''
    )

  if (
    "def test_phase157_r11_r14_surjectivity_precedes_short_exact_derivation():"
    not in text
  ):
    additions.append(
      r'''


def test_phase157_r11_r14_surjectivity_precedes_short_exact_derivation():
  _, body = _reference_and_body()

  surjectivity = (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である."
  )
  short_exact_reason = (
    "この完全性と, 左の写像が単射, "
    "右の写像が全射であることより, "
    "次の短完全列を得る."
  )
  short_exact = (
    r"$0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0$."
  )

  assert surjectivity in body
  assert short_exact_reason in body
  assert short_exact in body
  assert body.index(
    surjectivity
  ) < body.index(
    short_exact_reason
  )
  assert body.index(
    surjectivity
  ) < body.index(
    short_exact
  )
'''
    )

  if (
    "def test_phase157_r11_r14_ancestry_only_reference_is_not_public():"
    not in text
  ):
    additions.append(
      r'''


def test_phase157_r11_r14_ancestry_only_reference_is_not_public():
  reference, body = _reference_and_body()

  assert "**[R3] Proposition 5.3.**" not in reference
  assert "[R3]" not in body
'''
    )

  if additions:
    R11_TEST.write_text(
      text.rstrip()
      + "".join(
        additions
      )
      + "\n",
      encoding="utf-8",
    )
    print(
      "Added: R11-R14 regression tests"
    )
  else:
    print(
      "Already applied: R11-R14 regression tests"
    )


append_tests()

print("")
print("Phase157 R11-R14 repair1 applied successfully.")

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"
BACKUP.mkdir(exist_ok=True)

PRODUCTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST = ROOT / "tests" / "test_phase157_r11_proof_body_relevance.py"


def backup(path: Path) -> None:
    if not path.exists():
        return

    destination = BACKUP / path.name

    if not destination.exists():
        shutil.copy2(
            path,
            destination,
        )


def remove_once(
    path: Path,
    old: str,
    label: str,
) -> None:
    text = path.read_text(
        encoding="utf-8"
    )

    if old not in text:
        print(
            f"Already absent: {label}"
        )
        return

    count = text.count(
        old
    )

    if count != 1:
        raise RuntimeError(
            f"expected exactly one match for {label} "
            f"in {path}, found {count}"
        )

    path.write_text(
        text.replace(
            old,
            "",
            1,
        ),
        encoding="utf-8",
    )

    print(
        f"Removed: {label}"
    )


backup(
    PRODUCTION
)
backup(
    TEST
)

restore_call = '''  rendered = (
    _phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism(
      presentation,
      rendered,
    )
  )

'''

remove_once(
    PRODUCTION,
    restore_call,
    (
        "Phase157-R3 pi6_3-only suspension-isomorphism "
        "body restoration call"
    ),
)

test_content = r'''from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _render_pi6_3(
  max_depth: int = 2,
) -> str:
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=max_depth,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _proof_body(
  rendered: str,
) -> str:
  return rendered.split(
    "\n## 証明\n",
    1,
  )[1]


def test_phase157_r11_pi6_3_body_excludes_unconsumed_suspension_isomorphism():
  body = _proof_body(
    _render_pi6_3()
  )

  assert (
    r"$E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型写像である."
    not in body
  )


def test_phase157_r11_pi6_3_body_keeps_consumed_pi6_5_group():
  body = _proof_body(
    _render_pi6_3()
  )

  assert (
    r"$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$"
    in body
  )


def test_phase157_r11_pi6_5_group_precedes_its_order_consumer():
  body = _proof_body(
    _render_pi6_3()
  )
  pi6_5 = (
    r"$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$"
  )
  consumer = (
    "この短完全列と両端の群の位数より, "
    "中央の群の位数は"
  )

  assert pi6_5 in body
  assert consumer in body
  assert body.index(
    pi6_5
  ) < body.index(
    consumer
  )
'''

TEST.write_text(
    test_content,
    encoding="utf-8",
)

print(
    f"Written: {TEST.relative_to(ROOT)}"
)
print("")
print("Phase157 R11-R6 patch applied successfully.")
print(f"Changed: {PRODUCTION.relative_to(ROOT)}")
print(f"Added/replaced: {TEST.relative_to(ROOT)}")

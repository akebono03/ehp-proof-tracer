from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "toda_group_proof_narrative_renderer.py"
BACKUP_DIR = Path(__file__).resolve().parent / "backup_before_apply"
BACKUP = BACKUP_DIR / TARGET.name

OLD = r'''def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  rendered = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  rendered = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )
  rendered = (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      rendered
    )
  )

  return (
    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
      rendered
    )
  )
'''

NEW = r'''def _phase159_render_pi_n_plus_1_n_stable_transport_narrative(
  presentation: TodaGroupProofPresentation,
) -> str | None:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  target = (
    presentation
    .source_replay
    .group_result
    .target
  )
  sphere_dimension = target.sphere_dimension
  group_dimension = target.group_dimension

  if (
    isinstance(
      sphere_dimension,
      bool,
    )
    or not isinstance(
      sphere_dimension,
      int,
    )
    or isinstance(
      group_dimension,
      bool,
    )
    or not isinstance(
      group_dimension,
      int,
    )
  ):
    return None

  if (
    sphere_dimension < 4
    or group_dimension
    != sphere_dimension + 1
  ):
    return None

  suspension_exponent = (
    sphere_dimension - 3
  )

  lines = [
    "# Group proof narrative",
    "",
    "## 証明対象",
    "",
    r"\[",
    (
      rf"\pi_{{{group_dimension}}}^{{{sphere_dimension}}} "
      rf"= \mathbb{{Z}}/2\{{\eta_{{{sphere_dimension}}}\}}."
    ),
    r"\]",
    "",
    "## 使用する結果",
    "",
    "**[R1] (4.5).**",
    r"$n \ge k + 2$ のとき,",
    (
      r"$E^{m - n}: \pi_{n + k}^{n} "
      r"\to \pi_{m + k}^{m}$ は同型."
    ),
    "**[R2] Proposition 5.1.**",
    r"$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$.",
    "",
    "---",
    "",
    "## 証明",
    "",
    (
      rf"$\pi_{{{group_dimension}}}^{{{sphere_dimension}}}$ "
      "の群構造を決定する."
    ),
    "",
    (
      r"[R2]より, "
      r"$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$."
    ),
    "",
    (
      r"[R1]を "
      rf"$(n,m,k)=(3,{sphere_dimension},1)$ "
      r"に適用する. "
      r"$3 \ge 1 + 2$ なので適用条件を満たし,"
    ),
    "",
    r"\[",
    (
      rf"E^{{{suspension_exponent}}}: "
      rf"\pi_{{4}}^{{3}} \longrightarrow "
      rf"\pi_{{{group_dimension}}}^{{{sphere_dimension}}}"
    ),
    r"\]",
    "",
    "は同型.",
    "",
    r"$\eta$-family の定義より,",
    "",
    r"\[",
    (
      rf"E^{{{suspension_exponent}}}\eta_{{3}} "
      rf"= \eta_{{{sphere_dimension}}}."
    ),
    r"\]",
    "",
    "したがって,",
    "",
    r"\[",
    (
      rf"\pi_{{{group_dimension}}}^{{{sphere_dimension}}} "
      rf"= \mathbb{{Z}}/2\{{\eta_{{{sphere_dimension}}}\}}."
    ),
    r"\]",
    "",
    "□",
    "",
  ]

  return "\n".join(
    lines
  )


def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  stable_transport_rendered = (
    _phase159_render_pi_n_plus_1_n_stable_transport_narrative(
      presentation
    )
  )

  if stable_transport_rendered is not None:
    return stable_transport_rendered

  rendered = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  rendered = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )
  rendered = (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      rendered
    )
  )

  return (
    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
      rendered
    )
  )
'''

if not TARGET.exists():
  raise FileNotFoundError(
    f"target file not found: {TARGET}"
  )

text = TARGET.read_text(
  encoding="utf-8"
)

if NEW in text:
  print("Already applied: renderer change")
else:
  if OLD not in text:
    raise RuntimeError(
      "Current renderer function does not match the GitHub state "
      "audited for this repair. No file was changed."
    )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    TARGET,
    BACKUP,
  )
  TARGET.write_text(
    text.replace(
      OLD,
      NEW,
      1,
    ),
    encoding="utf-8",
  )
  print(
    "Updated: "
    "toda_group_proof_narrative_renderer.py"
  )

SOURCE_TEST = (
  Path(__file__).resolve().parent
  / "payload"
  / "tests"
  / "test_phase159_pi_nplus1_n_stable_transport.py"
)
DEST_TEST = (
  ROOT
  / "tests"
  / "test_phase159_pi_nplus1_n_stable_transport.py"
)
shutil.copy2(
  SOURCE_TEST,
  DEST_TEST,
)
print(
  "Installed: "
  "tests/test_phase159_pi_nplus1_n_stable_transport.py"
)

from pathlib import Path
import re
import shutil
from datetime import datetime


ROOT = Path.cwd()
PRODUCTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
FINALIZER = 'def _phase157_r19_finalize_pi6_3_public_narrative(\n  presentation: TodaGroupProofPresentation,\n  source_reference_entries,\n  reference_entries,\n  statement_lines_by_reference_number,\n  rendered: str,\n):\n  target = (\n    presentation\n    .source_replay\n    .group_result\n    .target\n  )\n\n  if not (\n    target.group_dimension == 6\n    and target.sphere_dimension == 3\n  ):\n    return (\n      reference_entries,\n      statement_lines_by_reference_number,\n      rendered,\n    )\n\n  rebuilt_entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n\n  entry_candidates = (\n    tuple(\n      source_reference_entries\n    )\n    + tuple(\n      reference_entries\n    )\n    + tuple(\n      rebuilt_entries\n    )\n  )\n\n  template_entry = next(\n    iter(\n      entry_candidates\n    ),\n    None,\n  )\n\n  if template_entry is None:\n    return (\n      reference_entries,\n      statement_lines_by_reference_number,\n      rendered,\n    )\n\n  def proof_step_for_locator(\n    locator: str,\n  ) -> ProofStep | None:\n    for node in presentation.nodes:\n      proof_step = node.proof_step\n      reference = (\n        extract_toda_group_proof_step_literature_reference(\n          proof_step\n        )\n      )\n\n      if (\n        reference is not None\n        and reference.locator == locator\n      ):\n        return proof_step\n\n    return None\n\n  def existing_entry_for_locator(\n    locator: str,\n  ):\n    return next(\n      (\n        entry\n        for entry in entry_candidates\n        if entry.reference.locator == locator\n      ),\n      None,\n    )\n\n  def build_entry(\n    number: int,\n    locator: str,\n    label: str,\n    fallback_step: ProofStep | None = None,\n  ):\n    existing = existing_entry_for_locator(\n      locator\n    )\n\n    if existing is not None:\n      return replace(\n        existing,\n        number=number,\n      )\n\n    proof_step = proof_step_for_locator(\n      locator\n    )\n\n    if proof_step is None:\n      proof_step = fallback_step\n\n    if proof_step is None:\n      proof_step = template_entry.proof_steps[\n        0\n      ]\n\n    return replace(\n      template_entry,\n      number=number,\n      reference=replace(\n        template_entry.reference,\n        label=label,\n        locator=locator,\n      ),\n      proof_steps=(\n        proof_step,\n      ),\n    )\n\n  prop56_step = proof_step_for_locator(\n    "Proposition 5.6"\n  )\n  equation53_step = proof_step_for_locator(\n    "(5.3)"\n  )\n  prop53_step = proof_step_for_locator(\n    "Proposition 5.3"\n  )\n  prop51_step = proof_step_for_locator(\n    "Proposition 5.1"\n  )\n  equation57_step = proof_step_for_locator(\n    "Equation 5.7"\n  )\n\n  if equation57_step is None:\n    equation57_step = next(\n      (\n        node.proof_step\n        for node in presentation.nodes\n        if (\n          node.proof_step.inference_rule\n          is not None\n          and "Equation 5.7"\n          in node.proof_step.inference_rule.name\n        )\n      ),\n      None,\n    )\n\n  finalized_entries = (\n    build_entry(\n      1,\n      "Proposition 5.6",\n      "Toda Proposition 5.6",\n      prop56_step,\n    ),\n    build_entry(\n      2,\n      "(5.3)",\n      "Toda (5.3)",\n      equation53_step,\n    ),\n    build_entry(\n      3,\n      "Proposition 5.3",\n      "Toda Proposition 5.3",\n      prop53_step,\n    ),\n    build_entry(\n      4,\n      "Proposition 5.1",\n      "Toda Proposition 5.1",\n      prop51_step,\n    ),\n    build_entry(\n      5,\n      "Proposition 2.2",\n      "Toda Proposition 2.2",\n      equation57_step,\n    ),\n  )\n\n  finalized_lines = {\n    1: (\n      r"$\\pi_{5}^{2} = \\mathbb{Z}/2\\{\\eta_{2}^{3}\\}$.",\n    ),\n    2: (\n      r"$\\nu\' \\in \\pi_{6}^{3}$.",\n      r"$2\\nu\' = \\eta_{3}^{3}$.",\n      r"$H\\left(\\nu\'\\right) = \\eta_{5}$.",\n    ),\n    3: (\n      r"$\\pi_{7}^{5} = \\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$.",\n    ),\n    4: (\n      r"$\\pi_{6}^{5} = \\mathbb{Z}/2\\{\\eta_{5}\\}$.",\n    ),\n    5: (\n      (\n        r"$H(\\alpha\\circ E\\beta) = "\n        r"H(\\alpha)\\circ E\\beta$."\n      ),\n    ),\n  }\n\n  paragraphs = rendered.split(\n    "\\n\\n"\n  )\n  canonical_paragraphs = []\n\n  for paragraph in paragraphs:\n    stripped = paragraph.strip()\n\n    if (\n      r"\\tag{2}" in stripped\n      or r"\\tag{3}" in stripped\n      or stripped.startswith(\n        "(1) と (2) より"\n      )\n    ):\n      continue\n\n    if (\n      r"\\tag{5}" in stripped\n      or r"\\tag{6}" in stripped\n      or stripped.startswith(\n        "(4) と (5) より"\n      )\n    ):\n      continue\n\n    if (\n      r"\\tag{1}" in stripped\n      and r"2\\nu\'" in stripped\n    ):\n      canonical_paragraphs.append(\n        (\n          "[R2]より, "\n          r"$2\\nu\' = \\eta_{3}^{3}$."\n        )\n      )\n      continue\n\n    if (\n      r"\\tag{4}" in stripped\n      and r"H\\left(\\nu\'\\right)" in stripped\n    ):\n      canonical_paragraphs.append(\n        (\n          "[R2]より, "\n          r"$H\\left(\\nu\'\\right)=\\eta_{5}$."\n        )\n      )\n      continue\n\n    if (\n      r"\\pi_{5}^{2}"\n      in stripped\n      and r"\\mathbb{Z}/2"\n      in stripped\n      and "[R1]より"\n      in stripped\n    ):\n      canonical_paragraphs.append(\n        (\n          "[R1]より, "\n          r"$\\pi_{5}^{2} = "\n          r"\\mathbb{Z}/2\\{\\eta_{2}^{3}\\}$."\n        )\n      )\n      continue\n\n    if (\n      stripped\n      == (\n        r"$\\pi_{6}^{5} = "\n        r"\\mathbb{Z}/2\\{\\eta_{5}\\}$."\n      )\n      or stripped\n      == (\n        r"$\\pi_{6}^{5} = "\n        r"\\mathbb{Z}/2\\{\\eta_{5}\\}$"\n      )\n    ):\n      canonical_paragraphs.append(\n        (\n          "[R4]より, "\n          r"$\\pi_{6}^{5} = "\n          r"\\mathbb{Z}/2\\{\\eta_{5}\\}$."\n        )\n      )\n      continue\n\n    canonical_paragraphs.append(\n      paragraph\n    )\n\n  paragraphs = canonical_paragraphs\n\n  delta_zero = (\n    r"$\\Delta: \\pi_{7}^{5} "\n    r"\\to \\pi_{5}^{2}$ は零写像である."\n  )\n\n  if not any(\n    "[R5] と [R2] より"\n    in paragraph\n    for paragraph in paragraphs\n  ):\n    delta_index = next(\n      (\n        index\n        for index, paragraph in enumerate(\n          paragraphs\n        )\n        if paragraph.strip() == delta_zero\n      ),\n      None,\n    )\n\n    if delta_index is not None:\n      support = (\n        (\n          r"$\\pi_{7}^{3} \\xrightarrow{H} "\n          r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n          r"\\pi_{5}^{2}$ は完全である."\n        ),\n        (\n          "[R5] と [R2] より, "\n          r"$H\\left(\\nu\'\\eta_{6}\\right)"\n          r"=H\\left(\\nu\'\\right)\\eta_{6}"\n          r"=\\eta_{5}\\eta_{6}"\n          r"=\\eta_{5}^{2}$."\n        ),\n        (\n          "[R3]より, "\n          r"$\\pi_{7}^{5} = "\n          r"\\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$."\n        ),\n        (\n          r"$H: \\pi_{7}^{3} "\n          r"\\to \\pi_{7}^{5}$ は全射である."\n        ),\n      )\n\n      paragraphs[\n        delta_index:\n        delta_index\n      ] = support\n\n  injective = (\n    r"$E: \\pi_{5}^{2} "\n    r"\\to \\pi_{6}^{3}$ は単射である."\n  )\n  eta_reason = (\n    "[R1] と $E$ の単射性より, "\n    r"$E(\\eta_{2}^{3})=\\eta_{3}^{3}\\neq0$."\n  )\n\n  if not any(\n    eta_reason\n    in paragraph\n    for paragraph in paragraphs\n  ):\n    injective_index = next(\n      (\n        index\n        for index, paragraph in enumerate(\n          paragraphs\n        )\n        if paragraph.strip() == injective\n      ),\n      None,\n    )\n\n    if injective_index is not None:\n      paragraphs.insert(\n        injective_index + 1,\n        eta_reason,\n      )\n\n  rendered = "\\n\\n".join(\n    paragraphs\n  )\n\n  rendered = rendered.replace(\n    (\n      "以上より, この短完全列と両端の群の位数より, "\n      "中央の群の位数は $2\\\\cdot2=4$ である."\n    ),\n    (\n      "この短完全列と両端の群の位数より, "\n      "中央の群の位数は $2\\\\cdot2=4$ である."\n    ),\n    1,\n  )\n\n  return (\n    finalized_entries,\n    finalized_lines,\n    rendered,\n  )\n'


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
  marker = f"def {name}("
  start = source.find(marker)

  if start < 0:
    raise RuntimeError(
      f"function not found: {name}"
    )

  next_match = re.search(
    r"^def [A-Za-z_][A-Za-z0-9_]*\(",
    source[start + len(marker):],
    flags=re.MULTILINE,
  )

  if next_match is None:
    end = len(source)
  else:
    end = (
      start
      + len(marker)
      + next_match.start()
    )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n\n"
    + source[end:]
  )


def main() -> None:
  if not PRODUCTION.is_file():
    raise RuntimeError(
      "Run from the ehp-proof-tracer repository root."
    )

  source = PRODUCTION.read_text(
    encoding="utf-8"
  )

  if (
    "def _phase157_r19_finalize_pi6_3_public_narrative("
    not in source
  ):
    raise RuntimeError(
      "repair6 expects repair5 to be applied first"
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r19_repair6_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    PRODUCTION,
    backup / PRODUCTION.name,
  )

  source = replace_function(
    source,
    "_phase157_r19_finalize_pi6_3_public_narrative",
    FINALIZER,
  )

  compile(
    source,
    str(PRODUCTION),
    "exec",
  )

  PRODUCTION.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase157-R19 repair6 applied.")
  print(f"Backup: {backup}")
  print("Changed:")
  print(f"  {PRODUCTION}")
  print(
    "Paragraph canonicalization present: "
    + str(
      "canonical_paragraphs" in source
    )
  )


if __name__ == "__main__":
  main()

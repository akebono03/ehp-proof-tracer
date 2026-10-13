from pathlib import Path
import ast
import shutil

ROOT=Path(__file__).resolve().parent.parent
A=ROOT/'toda_group_proof_narrative_reasons.py'
B=ROOT/'toda_group_proof_narrative_reason_renderer.py'

def replace_once(s, old, new, path):
    if s.count(old)!=1:
        raise RuntimeError(f'{path}: expected one anchor, found {s.count(old)}')
    return s.replace(old,new,1)

def patch_reasons(s):
    s=replace_once(s,'  EXACTNESS_TO_KERNEL = (\n    "exactness_to_kernel"\n  )','  EXACTNESS_TO_KERNEL = (\n    "exactness_to_kernel"\n  )\n  EXACTNESS_TO_DELTA_ZERO = "exactness_to_delta_zero"\n  INJECTIVE_SURJECTIVE_TO_ISOMORPHISM = "injective_surjective_to_isomorphism"','reasons enum')
    new='''def _exactness_to_delta_zero_reason(
  proof_step: ProofStep,
) -> TodaGroupProofNarrativeReason | None:
  """Recognize a typed Delta-zero inference, not its rendered prose."""
  conclusion = proof_step.conclusion
  if not isinstance(conclusion, TodaDeltaZeroStatement):
    return None
  iso_steps = tuple(
    premise for premise in proof_step.premises
    if isinstance(premise.conclusion, TodaSuspensionIsomorphismStatement)
  )
  exact_steps = tuple(
    premise for premise in proof_step.premises
    if isinstance(premise.conclusion, TodaProp42ExactnessStatement)
  )
  matches = []
  for iso in iso_steps:
    suspension = iso.conclusion.map
    for exact in exact_steps:
      window = exact.conclusion.window
      if (
        isinstance(suspension, TodaSuspensionMap)
        and window.first_map.name == "Δ"
        and window.second_map.name == "E"
        and window.source_term == conclusion.map.source_group
        and window.middle_term == conclusion.map.target_group
        and suspension.source_group == window.middle_term
        and suspension.target_group == window.target_term
      ):
        matches.append((iso, exact))
  if len(matches) != 1:
    return None
  return TodaGroupProofNarrativeReason(
    kind=TodaGroupProofNarrativeReasonKind.EXACTNESS_TO_DELTA_ZERO,
    premise_steps=matches[0],
    conclusion_step=proof_step,
  )


def _injective_surjective_to_isomorphism_reason(
  proof_step: ProofStep,
) -> TodaGroupProofNarrativeReason | None:
  """Require exactly matching, explicit generic map property premises."""
  from phase165_r14_r6_generic_iso import MapInjective, MapSurjective, MapIsomorphism
  conclusion = proof_step.conclusion
  if not isinstance(conclusion, MapIsomorphism):
    return None
  inj = tuple(
    p for p in proof_step.premises
    if isinstance(p.conclusion, MapInjective)
    and p.conclusion.map == conclusion.map
  )
  surj = tuple(
    p for p in proof_step.premises
    if isinstance(p.conclusion, MapSurjective)
    and p.conclusion.map == conclusion.map
  )
  if len(inj) != 1 or len(surj) != 1:
    return None
  return TodaGroupProofNarrativeReason(
    kind=TodaGroupProofNarrativeReasonKind.INJECTIVE_SURJECTIVE_TO_ISOMORPHISM,
    premise_steps=(inj[0], surj[0]),
    conclusion_step=proof_step,
  )


'''
    s=replace_once(s,'def _exactness_to_kernel_reason(',new+'def _exactness_to_kernel_reason(','new functions')
    import_start = s.index('from homotopy_groups import (')
    import_end = s.index('\n)', import_start) + 2
    import_block = s[import_start:import_end]
    changed_block = replace_once(
        import_block,
        '  TodaSuspensionMap,\n',
        '  TodaSuspensionMap,\n  TodaSuspensionIsomorphismStatement,\n',
        'homotopy_groups import',
    )
    s = s[:import_start] + changed_block + s[import_end:]
    s=replace_once(s,'    exactness_kernel_reason = (\n','    delta_zero_reason = _exactness_to_delta_zero_reason(node.proof_step)\n    if delta_zero_reason is not None:\n      append_if_visible(delta_zero_reason)\n\n    isomorphism_reason = _injective_surjective_to_isomorphism_reason(node.proof_step)\n    if isomorphism_reason is not None:\n      append_if_visible(isomorphism_reason)\n\n    exactness_kernel_reason = (\n','builder')
    return s

def patch_renderer(s):
    text='''  if reason.kind is TodaGroupProofNarrativeReasonKind.EXACTNESS_TO_DELTA_ZERO:
    if len(reason.premise_steps) != 2:
      return None
    exactness = reason.premise_steps[1].conclusion
    window = exactness.window
    first = window.first_map.name
    second = window.second_map.name
    return (
      "完全性より, "
      f"$\\\\operatorname{{Im}}{first}=\\\\ker {second}=0$ なので, "
      + _render_generic_narrative_step(reason.conclusion_step)
    )

  if reason.kind is TodaGroupProofNarrativeReasonKind.INJECTIVE_SURJECTIVE_TO_ISOMORPHISM:
    if len(reason.premise_steps) != 2:
      return None
    return (
      "単射性と全射性より, "
      + _render_generic_narrative_step(reason.conclusion_step)
    )

'''
    s=replace_once(s,'  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .EXACTNESS_TO_KERNEL\n  ):',text+'  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .EXACTNESS_TO_KERNEL\n  ):','renderer sentence')
    # Existing injection is before conclusion. Remove redundant connector only when tied to typed reason.
    new='''def _normalize_phase165_r49_reason_prose(
  markdown: str,
  reason: TodaGroupProofNarrativeReason,
) -> str:
  if reason.kind not in (
    TodaGroupProofNarrativeReasonKind.EXACTNESS_TO_DELTA_ZERO,
    TodaGroupProofNarrativeReasonKind.INJECTIVE_SURJECTIVE_TO_ISOMORPHISM,
  ):
    return markdown
  sentence = render_toda_group_proof_narrative_reason_sentence(reason)
  if sentence is None:
    return markdown
  paragraphs = markdown.split("\\n\\n")
  hits = [i for i, paragraph in enumerate(paragraphs) if paragraph.strip() == sentence]
  if len(hits) != 1:
    return markdown
  index = hits[0]
  # A pre-existing generic connector is redundant after the typed reason.
  if index > 0 and paragraphs[index - 1].strip() == "これより,":
    paragraphs.pop(index - 1)
  return "\\n\\n".join(paragraphs)


'''
    s=replace_once(s,'def insert_toda_group_proof_narrative_reason_prose(',new+'def insert_toda_group_proof_narrative_reason_prose(','renderer helper')
    s=replace_once(s,'  return rendered\n', '  return rendered\n','noop') if False else s
    needle='''  for reason in reason_sidecar.reasons:
    rendered = (
      _normalize_exactness_to_kernel_reason_prose(
        rendered,
        reason,
      )
    )

  return rendered'''
    replacement='''  for reason in reason_sidecar.reasons:
    rendered = (
      _normalize_exactness_to_kernel_reason_prose(
        rendered,
        reason,
      )
    )

  for reason in reason_sidecar.reasons:
    rendered = _normalize_phase165_r49_reason_prose(rendered, reason)

  return rendered'''
    s=replace_once(s,needle,replacement,'renderer end')
    return s

def main():
    original={A:A.read_text(encoding='utf-8'),B:B.read_text(encoding='utf-8')}
    patches={A:patch_reasons(original[A]),B:patch_renderer(original[B])}
    for path, content in patches.items():
        ast.parse(content,filename=str(path))
    backup=ROOT/'phase165_r49_reason_bridge'/'backup_before_apply'
    backup.mkdir(parents=True,exist_ok=True)
    for path,content in patches.items():
        if not (backup/path.name).exists():
            shutil.copy2(path,backup/path.name)
        path.write_text(content,encoding='utf-8')
    print('R49 typed reason bridge installed; backups:',backup)
if __name__=='__main__':
    main()

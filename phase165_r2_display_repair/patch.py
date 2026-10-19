from pathlib import Path
import shutil

root = Path.cwd()
path = root / 'toda_group_proof_narrative_renderer.py'
backup = root / 'phase165_r2_renderer_before.py.bak'
src = path.read_text(encoding='utf-8')
start = src.index('def render_toda_group_proof_narrative_markdown(')
end = src.index('\ndef render_toda_partial_proof_narrative_markdown(', start)
old = src[start:end]
if 'Phase 165 R2: retain typed quotient derivations' in old:
    print('R2 patch already applied')
    raise SystemExit(0)
needle = '''  return rendered\n'''
assert old.count(needle) == 1, 'Unexpected current renderer; no changes made'
replacement = '''  # Phase 165 R2: retain typed quotient derivations already proved in the tree.
  # The established renderer remains the only public rendering entry point.
  from phase165_r12_r2_quotient_rules import (
    KernelMultipleStatement,
    QuotientIsomorphismStatement,
  )
  from phase165_r57_r10_step_narrative import ordered_proof_ancestry
  replay = getattr(presentation, "source_replay", None)
  group_result = getattr(replay, "group_result", None)
  proof_root = getattr(group_result, "proof_step", None)
  if proof_root is not None:
    ancestry = ordered_proof_ancestry(proof_root)
    kernel_steps = tuple(
      step for step in ancestry
      if isinstance(step.conclusion, KernelMultipleStatement)
    )
    quotient_steps = tuple(
      step for step in ancestry
      if isinstance(step.conclusion, QuotientIsomorphismStatement)
    )
    if kernel_steps and quotient_steps:
      from phase165_r12_r34_r2_semantic_narrative import (
        _element,
        _group,
      )
      missing = []
      for step in kernel_steps:
        item = step.conclusion
        generator = _element(item.source_generator)
        formula = (
          r"\\ker E=\\mathbb{Z}\\{"
          + str(item.multiple) + generator + r"\\}"
        )
        if r"\\ker E" not in rendered:
          missing.append("完全性より, $" + formula + "$. ")
      for step in quotient_steps:
        item = step.conclusion
        if r"\\cong" not in rendered and "第一同型定理" not in rendered:
          formula = (
            _group(item.codomain) + r"\\cong "
            + _group(item.domain) + r"/\\mathbb{Z}\\{"
            + str(item.multiple) + _element(item.source_generator) + r"\\}"
          )
          missing.append("全射性と核の決定から, 第一同型定理より $" + formula + "$. ")
      if missing:
        conclusion_start = rendered.rfind("以上より,")
        if conclusion_start < 0:
          raise ValueError("R2: cannot locate established final conclusion")
        rendered = (
          rendered[:conclusion_start]
          + "\\n\\n".join(missing)
          + "\\n\\n"
          + rendered[conclusion_start:]
        )
  return rendered
'''
new = old.replace(needle,replacement)
assert new != old
shutil.copy2(path, backup)
path.write_text(src[:start] + new + src[end:], encoding='utf-8')
print('Patched existing public renderer; original saved:',backup)

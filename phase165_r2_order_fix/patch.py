from pathlib import Path
import shutil

root = Path.cwd()
path = root / 'toda_group_proof_narrative_renderer.py'
backup = root / 'phase165_r2_order_fix_before.py.bak'
src = path.read_text(encoding='utf-8')
start = src.index('def render_toda_group_proof_narrative_markdown(')
end = src.index('\ndef render_toda_partial_proof_narrative_markdown(', start)
old = src[start:end]
marker = '  # Phase 165 R2: retain typed quotient derivations already proved in the tree.'
next_marker = '  return rendered\n'
if marker not in old:
    raise RuntimeError('Expected earlier R2 terminal insertion not found; no changes made')
if 'Phase 165 R2 order repair' in old:
    raise RuntimeError('Order repair already installed; no changes made')
a = old.index(marker)
b = old.index(next_marker, a) + len(next_marker)
replacement = r'''  # Phase 165 R2 order repair: consume existing typed ancestry, not new facts.
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
      from phase165_r12_r34_r2_semantic_narrative import _element, _group
      paragraphs = rendered.split("\n\n")

      def unique_index(fragment):
        indices = [
          index for index, paragraph in enumerate(paragraphs)
          if fragment in paragraph
        ]
        if len(indices) != 1:
          raise ValueError(
            "R2: cannot uniquely locate existing narrative anchor: " + fragment
          )
        return indices[0]

      for step in kernel_steps:
        item = step.conclusion
        expression = str(item.multiple) + _element(item.source_generator)
        formula = r"\ker E=\mathbb{Z}\{" + expression + r"\}"
        if formula not in rendered and r"\ker E" not in rendered:
          delta_index = unique_index(r"\operatorname{Im}\Delta")
          paragraphs.insert(
            delta_index + 1,
            "完全性より, $" + formula + "$."
          )
      for step in quotient_steps:
        item = step.conclusion
        formula = (
          _group(item.codomain) + r"\cong "
          + _group(item.domain) + r"/\mathbb{Z}\{"
          + str(item.multiple) + _element(item.source_generator) + r"\}"
        )
        if "第一同型定理" not in "\n\n".join(paragraphs):
          surjective_index = unique_index("は全射")
          prior_group = _group(item.domain) + " = "
          group_indices = [
            i for i, paragraph in enumerate(paragraphs)
            if prior_group in paragraph and i > surjective_index
          ]
          if len(group_indices) != 1:
            raise ValueError("R2: cannot locate earlier group after surjectivity")
          paragraphs.insert(
            group_indices[0] + 1,
            "全射性と核の決定から, 第一同型定理より $" + formula + "$."
          )
      rendered = "\n\n".join(paragraphs)
  return rendered
'''
new = old[:a] + replacement + old[b:]
if new == old or old.count(marker) != 1:
    raise RuntimeError('Ambiguous prior R2 patch; no changes made')
if backup.exists():
    raise RuntimeError('Backup already exists; refusing to overwrite')
shutil.copy2(path, backup)
path.write_text(src[:start] + new + src[end:], encoding='utf-8')
print('Replaced only previous R2 terminal insertion block; backup:', backup)

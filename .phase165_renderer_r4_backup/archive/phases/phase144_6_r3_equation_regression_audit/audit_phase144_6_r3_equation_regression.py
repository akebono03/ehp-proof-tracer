from pathlib import Path
import inspect

import toda_group_proof_narrative_argument_body_renderer as body_renderer
import toda_group_proof_narrative_argument_multi_renderer as multi_renderer
import toda_group_proof_narrative_step_transitions as step_transitions
import toda_group_proof_generic_narrative_renderer as generic_renderer


def show_source(label, obj):
  print("=" * 78)
  print(label)
  print("=" * 78)
  try:
    print(inspect.getsource(obj))
  except Exception as exc:
    print(f"<source unavailable: {exc!r}>")


print("Phase 144-6-R3 equation-reference regression audit")
print()

show_source(
  "multi renderer",
  multi_renderer.render_toda_group_proof_narrative_multi_argument_markdown,
)
show_source(
  "argument body renderer",
  body_renderer.render_toda_group_proof_narrative_argument_body_markdown,
)

print("=" * 78)
print("equation/reference-related symbols")
print("=" * 78)
modules = (
  body_renderer,
  multi_renderer,
  step_transitions,
  generic_renderer,
)
for module in modules:
  print(f"[{module.__name__}]")
  for name in sorted(vars(module)):
    lowered = name.lower()
    if (
      "equation" in lowered
      or "number" in lowered
      or "derivation" in lowered
      or "transition" in lowered
      or "reference" in lowered
    ):
      value = getattr(module, name)
      if callable(value):
        try:
          signature = inspect.signature(value)
        except Exception:
          signature = "<signature unavailable>"
        print(f"  {name}{signature}")
      else:
        print(f"  {name}: {type(value).__name__}")
  print()

root = Path(__file__).resolve().parent.parent
print("=" * 78)
print("local source text hits")
print("=" * 78)
for filename in (
  "toda_group_proof_narrative_argument_body_renderer.py",
  "toda_group_proof_narrative_argument_multi_renderer.py",
  "toda_group_proof_narrative_step_transitions.py",
  "toda_group_proof_generic_narrative_renderer.py",
):
  path = root / filename
  text = path.read_text(encoding="utf-8-sig")
  print(f"[{filename}]")
  for number, line in enumerate(text.splitlines(), start=1):
    lowered = line.lower()
    if (
      "equation" in lowered
      or "number" in lowered
      or "reference" in lowered
      or "derivation" in lowered
      or "transition" in lowered
      or '"これらより、"' in line
      or '"より、"' in line
    ):
      print(f"{number}: {line}")
  print()

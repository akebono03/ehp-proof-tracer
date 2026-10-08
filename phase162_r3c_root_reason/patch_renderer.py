"""Apply the single-function R3-C production connection, preserving other code."""
from pathlib import Path

ROOT = Path.cwd()
TARGET = ROOT / 'toda_group_proof_narrative_renderer.py'
IMPORT_ANCHOR = 'from toda_group_proof_presentation import (\n'
NEW_IMPORT = (
    'from toda_group_structure_transport_reason import (\n'
    '  render_group_structure_transport_reason,\n'
    ')\n'
)
OLD_FUNCTION = '''def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  stable_transport_narrative = (
    _phase160_r7_render_stable_finite_cyclic_transport_narrative(
      presentation
    )
  )

  if stable_transport_narrative is not None:
    return stable_transport_narrative

  return (
    _phase160_r7_previous_public_narrative_renderer(
      presentation
    )
  )
'''
NEW_FUNCTION = '''def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  stable_transport_narrative = (
    _phase160_r7_render_stable_finite_cyclic_transport_narrative(
      presentation
    )
  )

  if stable_transport_narrative is not None:
    return stable_transport_narrative

  rendered = (
    _phase160_r7_previous_public_narrative_renderer(
      presentation
    )
  )
  reason = render_group_structure_transport_reason(
    presentation.root_step
  )
  if reason is None:
    return rendered

  # Connect the verified inference explanation immediately before its
  # existing final conclusion; do not replace proof text or use old Markdown.
  conclusion_marker = '以上より,'
  marker_position = rendered.rfind(conclusion_marker)
  proof_position = rendered.find('## 証明')
  if marker_position < 0 or marker_position < proof_position:
    raise ValueError('Cannot locate final proof conclusion for transport reasoning')
  return (
    rendered[:marker_position]
    + reason
    + '\\n\\n'
    + rendered[marker_position:]
  )
'''


def main() -> None:
    if not TARGET.is_file():
        raise FileNotFoundError(TARGET)
    raw = TARGET.read_bytes()
    newline = '\r\n' if b'\r\n' in raw else '\n'
    source = raw.decode('utf-8').replace('\r\n', '\n')
    if NEW_FUNCTION in source and NEW_IMPORT in source:
        print('R3-C already applied')
        return
    if source.count(OLD_FUNCTION) != 1:
        raise RuntimeError('Unexpected renderer contract: public function does not match current GitHub code')
    if source.count(IMPORT_ANCHOR) != 1:
        raise RuntimeError('Unexpected renderer contract: import anchor missing')
    updated = source.replace(IMPORT_ANCHOR, NEW_IMPORT + IMPORT_ANCHOR, 1)
    updated = updated.replace(OLD_FUNCTION, NEW_FUNCTION, 1)
    TARGET.write_bytes(updated.replace('\n', newline).encode('utf-8'))
    print('Updated:', TARGET)


if __name__ == '__main__':
    main()

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'toda_literature_statement_boundary.py'

REPLACEMENTS = (
    (
        '''    component_key="higher_eta_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=4,
    range_text=None,
    range_is_explicit_in_current_aggregate=False,''',
        '''    component_key="higher_eta_group_relation",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=4,
    range_text="n >= 3",
    range_is_explicit_in_current_aggregate=False,''',
    ),
    (
        '''      component_key="eta2_composition_isomorphism",
      statement_role=TodaLiteratureStatementRole.OTHER,
      order=None,
      range_text=None,
      range_is_explicit_in_current_aggregate=True,''',
        '''      component_key="eta2_composition_isomorphism",
      statement_role=TodaLiteratureStatementRole.OTHER,
      order=None,
      range_text="i >= 3",
      range_is_explicit_in_current_aggregate=True,''',
    ),
)


def main() -> None:
    if not TARGET.is_file():
        raise SystemExit(f'Missing repository file: {TARGET}')
    original = TARGET.read_bytes()
    content = original.decode('utf-8')
    newline = '\r\n' if b'\r\n' in original else '\n'
    normalized = content.replace('\r\n', '\n')
    for before, after in REPLACEMENTS:
        if normalized.count(after) == 1 and normalized.count(before) == 0:
            print('Already applied:', after.splitlines()[0].strip())
            continue
        if normalized.count(before) != 1:
            raise SystemExit('Expected exactly one target block: ' + before.splitlines()[0].strip())
        normalized = normalized.replace(before, after, 1)
    modified = normalized.replace('\n', newline).encode('utf-8')
    if modified != original:
        TARGET.write_bytes(modified)
        print('Updated:', TARGET)
    else:
        print('No changes required')


if __name__ == '__main__':
    main()

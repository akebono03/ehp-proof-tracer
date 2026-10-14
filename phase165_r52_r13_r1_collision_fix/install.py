from pathlib import Path
import shutil

root = Path.cwd()
target = root / 'phase165_r3_recursive_search.py'
if not target.is_file() or not (root / 'phase165_r52_r13_reference_registration.py').is_file():
    raise SystemExit('Run from repository root with R52-R13 installed')
s = target.read_text(encoding='utf-8')
old = '''            expansions = expansion_provider(target)
            if not isinstance(expansions, tuple):'''
new = '''            # A uniquely registered fixed Reference is a complete proof leaf.
            # Do not count a second derivation of the same statement as ambiguity.
            # Multiple direct references remain ambiguous and are rejected below.
            if lookup_mode == "typed_reference" and len(options) == 1:
                step = options[0]
                solved.append((target, step))
                report("proved", target, step)
                return step
            expansions = expansion_provider(target)
            if not isinstance(expansions, tuple):'''
if new in s:
    print('R52-R13-R1 collision fix already installed')
elif s.count(old) == 1:
    backup = target.with_name(target.name + '.r52_r13_r1_backup')
    if not backup.exists():
        shutil.copy2(target, backup)
    target.write_text(s.replace(old,new), encoding='utf-8')
    print('R52-R13-R1 direct Reference priority installed')
else:
    raise SystemExit('Search source signature changed; no modification applied')
shutil.copy2(Path(__file__).with_name('test_phase165_r52_r13_r1_collision_fix.py'), root / 'test_phase165_r52_r13_r1_collision_fix.py')

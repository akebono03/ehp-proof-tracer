from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
src = Path(__file__).resolve().parent
new = root / 'phase165_r12_r33_proof_tree_dedup.py'
shutil.copyfile(src / new.name, new)
target = root / 'phase165_r6_2_r4_r8_dedup.py'
text = target.read_text(encoding='utf-8')
old = '''    if any(same_cited_scalar_specialization(old, candidate) for old in options):
        return
    options.append(candidate)'''
replacement = '''    from phase165_r12_r33_proof_tree_dedup import same_completed_proof_tree
    if any(
        same_cited_scalar_specialization(old, candidate)
        or same_completed_proof_tree(old, candidate)
        for old in options
    ):
        return
    options.append(candidate)'''
if replacement in text:
    print('R12-R33 proof-tree dedup: ALREADY CONNECTED')
elif old in text:
    backup = target.with_suffix('.py.r12_r33_backup')
    if not backup.exists():
        shutil.copyfile(target, backup)
    target.write_text(text.replace(old, replacement, 1), encoding='utf-8')
    print('R12-R33 proof-tree dedup: CONNECTED')
else:
    raise RuntimeError('Existing dedup function does not match reviewed GitHub version; no changes applied')

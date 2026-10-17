"""Install R12-R7 with an exact guarded insertion and an original backup."""
from __future__ import annotations

import shutil
from pathlib import Path


def install() -> None:
    package = Path(__file__).resolve().parent
    root = package.parent
    source = root / "phase165_r52_r9_shared_math.py"
    if not source.is_file():
        raise FileNotFoundError("Project root must contain phase165_r52_r9_shared_math.py")
    destination = root / "phase165_r12_r7_proof_order_guard.py"
    current = source.read_text(encoding="utf-8")
    anchor = '    if proof_use_order == "registered":\n'
    insertion = (
        '    # R12-R7: enforce reviewed dependencies before using cited proof leaves.\n'
        '    from phase165_r12_r7_proof_order_guard import restrict_registered_ordered_claims\n'
        '    proof_context = restrict_registered_ordered_claims(proof_context, goal)\n'
    )
    previous = (
        '    # R12-R7: exclude composite parents and later clauses before any provider\n'
        '    # can use fixed source witnesses. No target is promoted to a GIVEN fact.\n'
        '    from phase165_r12_r7_proof_order_guard import restrict_registered_ordered_claims\n'
        '    proof_context = restrict_registered_ordered_claims(proof_context, goal)\n'
    )
    if insertion not in current:
        if previous in current:
            patched = current.replace(previous, insertion)
        else:
            if current.count(anchor) != 1:
                raise ValueError("Shared search changed: refusing unsafe installation")
            patched = current.replace(anchor, insertion + anchor)
        backup = root / "phase165_r52_r9_shared_math.r12_r7_backup.py"
        if not backup.exists():
            shutil.copyfile(source, backup)
        source.write_text(patched, encoding="utf-8")
    claim_order = root / "phase165_prop51_claim_order.py"
    if not claim_order.is_file():
        raise FileNotFoundError("phase165_prop51_claim_order.py missing")
    old_claims = claim_order.read_text(encoding="utf-8")
    if "def ordered_prop51_items(" not in old_claims or "def pi4_3_goal(" not in old_claims:
        raise ValueError("Unknown claim order version: refusing to overwrite")
    if "def proof_ordered_prop51_items(" not in old_claims:
        backup_claims = root / "phase165_prop51_claim_order.r12_r7_backup.py"
        if not backup_claims.exists():
            shutil.copyfile(claim_order, backup_claims)
        full = (package / "phase165_prop51_claim_order.py").read_text(encoding="utf-8")
        start = full.index("def proof_ordered_prop51_items(")
        end = full.index("\n\ndef prop51_intermediate_goal(", start)
        helper = full[start:end]
        claim_order.write_text(old_claims.rstrip() + "\n\n\n" + helper + "\n", encoding="utf-8")
    shutil.copyfile(package / destination.name, destination)
    print("R12-R7 installed: explicit proof dependencies, no composite bypass")


if __name__ == "__main__":
    install()

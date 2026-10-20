"""Minimal guarded installation of Phase 166 R3-C stage 2."""
from __future__ import annotations
import ast
from datetime import datetime, timezone
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
BACKUP = Path(__file__).resolve().parent / "backups"


def install_one(name: str, operations: tuple[tuple[str, str], ...]) -> None:
    path = ROOT / name
    original = path.read_text(encoding="utf-8-sig")
    updated = original
    for old, new in operations:
        if new in updated:
            continue
        if updated.count(old) != 1:
            raise RuntimeError(f"Unexpected source in {name}: expected one exact anchor")
        updated = updated.replace(old, new, 1)
    ast.parse(updated)
    if updated == original:
        print("UNCHANGED:", name)
        return
    BACKUP.mkdir(exist_ok=True)
    shutil.copy2(path, BACKUP / (name + "." + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + ".bak"))
    path.write_text(updated, encoding="utf-8")
    (Path(__file__).resolve().parent / (name + ".installed_full.txt")).write_text(updated, encoding="utf-8")
    print("PATCHED:", name)


def main() -> None:
    helper = Path(__file__).resolve().parent / "phase166_r3c_publication_order.py"
    shutil.copy2(helper, ROOT / helper.name)
    install_one("phase165_r52_r16_web_citation_gate.py", (
        ('    verified_assertion_ids: tuple[str, ...] = (),\n) -> RegistryBridgeResult:',
         '    verified_assertion_ids: tuple[str, ...] = (),\n    explicit_publication_target: bool = False,\n) -> RegistryBridgeResult:'),
        ('    accepted = []\n    for link in bridge.proof_links:',
         '    accepted = []\n    if explicit_publication_target:\n        from phase166_r3c_publication_order import precedes_citing_assertion\n    for link in bridge.proof_links:'),
        ('        # A source admitted under the explicit adopted-Tex convention keeps its',
         '        if explicit_publication_target:\n            if precedes_citing_assertion(bridge, assertion.assertion_id, citing_assertion_id):\n                accepted.append(link)\n            continue\n        # A source admitted under the explicit adopted-Tex convention keeps its'),
    ))
    install_one("phase165_r3_recursive_search.py", (
        ('("legacy", "typed_reference", "typed_reference_ordered"):',
         '("legacy", "typed_reference", "typed_reference_ordered", "typed_reference_publication"):'),
        ('            if lookup_mode == "typed_reference_ordered":',
         '            if lookup_mode == "typed_reference_publication":\n                from phase166_r3c_publication_order import precedes_citing_assertion\n                options = []\n                for assertion in bridge.registry._assertions.values():\n                    if not precedes_citing_assertion(bridge, assertion.assertion_id, citing_assertion_id):\n                        continue\n                    if type(assertion.content) is not type(target) or assertion.content != target:\n                        continue\n                    links = tuple(link for link in bridge.proof_links if link.assertion_id == assertion.assertion_id)\n                    if len(links) != 1 or links[0].step is None:\n                        continue\n                    step = links[0].step\n                    if (not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN\n                            or type(step.conclusion) is not type(target) or step.conclusion != target):\n                        raise ValueError("ordered reference has inconsistent ProofStep")\n                    options.append(step)\n            elif lookup_mode == "typed_reference_ordered":'),
        ('if lookup_mode in ("typed_reference", "typed_reference_ordered") and len(options) == 1:',
         'if lookup_mode in ("typed_reference", "typed_reference_ordered", "typed_reference_publication") and len(options) == 1:'),
    ))
    install_one("phase165_r52_r9_shared_math.py", (
        ('        verified_assertion_ids=verified_assertion_ids,\n    )\n    # R12-R7:',
         '        verified_assertion_ids=verified_assertion_ids,\n        explicit_publication_target=citing_assertion_id is not None,\n    )\n    # R12-R7:'),
        ('        lookup_mode="typed_reference",\n        structure_status=GroupStructureStatus.UNKNOWN,',
         '        lookup_mode="typed_reference_publication" if citing_assertion_id is not None else "typed_reference",\n        structure_status=GroupStructureStatus.UNKNOWN,'),
    ))
    print("R3-C stage 2 installed; implicit public goals retain previous reference lookup")


if __name__ == "__main__":
    main()

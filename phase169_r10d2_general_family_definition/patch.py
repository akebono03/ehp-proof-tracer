"""Guarded transactional R10D2 patch, saving complete changed functions."""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
REFERENCE_TARGET = ROOT / "phase168_r3_37c_reference_projection.py"
OUT = HERE / "output"
BACKUP = OUT / "phase165_r52_r9_shared_math.py.before"
REFERENCE_BACKUP = OUT / "phase168_r3_37c_reference_projection.py.before"
EXPECTED_BLOBS = {
    TARGET.name: "f4697aec0fd613c94ea8f1ea2f9e2655b80c53fb",
    REFERENCE_TARGET.name: "874d56b04e25d40bc3f43367243cc7b229660586",
}

OLD_SOURCE = "build_adopted_toda53_hopf_reference(production))"
NEW_SOURCE = '''build_adopted_toda53_hopf_reference(production))
        from phase169_r10d2_general_family_definition.family_citation import (
            build_cited_stable_family_definitions,
        )
        sources = sources + (build_cited_stable_family_definitions(),)'''

OLD_FAMILY = "    from phase165_r12_r21_eta_generator_chain import expand_cited_eta_generator"
NEW_FAMILY = '''    from phase165_r12_r21_eta_generator_chain import expand_cited_eta_generator
    from phase169_r10d2_general_family_definition.family_citation import (
        expand_cited_stable_family,
    )'''

OLD_FAMILY_CALL = "        options.extend(expand_cited_eta_generator(goal))"
NEW_FAMILY_CALL = '''        options.extend(expand_cited_eta_generator(goal))
        options.extend(expand_cited_stable_family(goal, tuple(available)))'''

OLD_GATE = '''        # R7 integration boundary: enable on the active 2-stem only.
        # The mathematical inference rule itself has no stem-specific branch.
        # Preserve the already verified R5B/R6A routes without ambiguity.
        from phase169_r7_general_stable_transport.rule import (
            expand_prior_general_stable_transport,
        )
        if (not legacy_one_step_options and not legacy_two_step_options
                and isinstance(goal, Relation)
                and isinstance(goal.lhs, TodaPrimaryGroup)
                and type(goal.lhs.group_dimension) is int
                and type(goal.lhs.sphere_dimension) is int
                and goal.lhs.group_dimension - goal.lhs.sphere_dimension == 2):
            options.extend(expand_prior_general_stable_transport(
                goal, tuple(available), bridge, proof_target=proof_target,
            ))'''

NEW_GATE = '''        # R10D2: stem-neutral R7 transport, with publication order checked
        # by the prior-source resolver and each generator image independently proved.
        # Retain the already verified R5B/R6A expansions when they are available.
        from phase169_r7_general_stable_transport.rule import (
            expand_prior_general_stable_transport,
        )
        if (not legacy_one_step_options and not legacy_two_step_options
                and isinstance(goal, Relation)
                and isinstance(goal.lhs, TodaPrimaryGroup)
                and type(goal.lhs.group_dimension) is int
                and type(goal.lhs.sphere_dimension) is int):
            options.extend(expand_prior_general_stable_transport(
                goal, tuple(available), bridge, proof_target=proof_target,
            ))'''

OLD_REF_IMPORT = '    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition'
NEW_REF_IMPORT = '''    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase169_r10d2_general_family_definition.family_citation import (
        CitedStableFamilyDefinition, cited_family_reference_sentence,
    )'''

OLD_REF_BRANCH = '''            if isinstance(statement, TodaEtaFamilyGeneralDefinition):
                if statement.lower_bound == 2:
                    sentence = r"$n\\ge 2$ に対し, $\\eta_n=E^{n-2}\\eta_2$ と定義する."'''
NEW_REF_BRANCH = '''            if isinstance(statement, TodaEtaFamilyGeneralDefinition):
                if statement.lower_bound == 2:
                    sentence = r"$n\\ge 2$ に対し, $\\eta_n=E^{n-2}\\eta_2$ と定義する."
            elif isinstance(statement, CitedStableFamilyDefinition):
                sentence = cited_family_reference_sentence(statement)'''


def _functions(source: str) -> dict[str, str]:
    parsed = ast.parse(source)
    lines = source.splitlines(keepends=True)
    return {node.name: "".join(lines[node.lineno - 1:node.end_lineno])
            for node in parsed.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}


def replacement_content(original: bytes) -> tuple[bytes, dict[str, str]]:
    windows = b"\r\n" in original
    source = original.decode("utf-8").replace("\r\n", "\n")
    old_functions = _functions(source)
    if "build_shared_typed_bridge" not in old_functions or "shared_expansion_provider" not in old_functions:
        raise RuntimeError("required reviewed functions are missing")
    for old, new, label in (
        (OLD_SOURCE, NEW_SOURCE, "source registration"),
        (OLD_FAMILY, NEW_FAMILY, "family import"),
        (OLD_FAMILY_CALL, NEW_FAMILY_CALL, "provider expansion"),
        (OLD_GATE, NEW_GATE, "stem-neutral transport"),
    ):
        if source.count(old) != 1 or new in source:
            raise RuntimeError("R10D2 unexpected original content: " + label)
        source = source.replace(old, new, 1)
    updated_functions = _functions(source)
    for name in ("build_shared_typed_bridge", "shared_expansion_provider"):
        if old_functions[name] == updated_functions[name]:
            raise RuntimeError("target function unexpectedly unchanged: " + name)
    ast.parse(source)
    content = source.replace("\n", "\r\n") if windows else source
    return content.encode("utf-8"), updated_functions


def reference_replacement(original: bytes) -> tuple[bytes, str]:
    windows = b"\r\n" in original
    source = original.decode("utf-8").replace("\r\n", "\n")
    for old, new in ((OLD_REF_IMPORT, NEW_REF_IMPORT), (OLD_REF_BRANCH, NEW_REF_BRANCH)):
        if source.count(old) != 1 or new in source:
            raise RuntimeError("R10D2 unexpected Reference content")
        source = source.replace(old, new, 1)
    result = _functions(source)
    if "project_reference_bodies" not in result:
        raise RuntimeError("Reference projection function missing")
    ast.parse(source)
    content = source.replace("\n", "\r\n") if windows else source
    return content.encode("utf-8"), result["project_reference_bodies"]


def main() -> None:
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                            capture_output=True, text=True, check=True).stdout.strip()
    if branch != "develop":
        raise RuntimeError("R10D2 requires branch develop")
    for target in (TARGET, REFERENCE_TARGET):
        expected = EXPECTED_BLOBS[target.name]
        digest = subprocess.run(["git", "hash-object", str(target)], cwd=ROOT,
                                capture_output=True, text=True, check=True).stdout.strip()
        if digest != expected:
            raise RuntimeError("R10D2 expected reviewed baseline differs: " + str(target))
    original = TARGET.read_bytes()
    ref_original = REFERENCE_TARGET.read_bytes()
    updated, functions = replacement_content(original)
    updated_ref, ref_function = reference_replacement(ref_original)
    # Prepare all outputs and backups BEFORE mutating production files.
    OUT.mkdir(parents=True, exist_ok=True)
    for backup, source in ((BACKUP, original), (REFERENCE_BACKUP, ref_original)):
        if backup.exists() and backup.read_bytes() != source:
            raise RuntimeError("R10D2 previous backup does not match baseline")
        if not backup.exists():
            backup.write_bytes(source)
    for name in ("build_shared_typed_bridge", "shared_expansion_provider"):
        (OUT / (name + "_FULL.py")).write_text(functions[name], encoding="utf-8")
    (OUT / "phase165_r52_r9_shared_math.py.FULL").write_bytes(updated)
    (OUT / "project_reference_bodies_FULL.py").write_text(ref_function, encoding="utf-8")
    (OUT / "phase168_r3_37c_reference_projection.py.FULL").write_bytes(updated_ref)
    temp = TARGET.with_name(TARGET.name + ".r10d2-temp")
    ref_temp = REFERENCE_TARGET.with_name(REFERENCE_TARGET.name + ".r10d2-temp")
    try:
        temp.write_bytes(updated)
        ref_temp.write_bytes(updated_ref)
        temp.replace(TARGET)
        ref_temp.replace(REFERENCE_TARGET)
    except BaseException:
        TARGET.write_bytes(original)
        REFERENCE_TARGET.write_bytes(ref_original)
        raise
    finally:
        for item in (temp, ref_temp):
            if item.exists():
                item.unlink()
    print("R10D2_PATCHED=" + str(TARGET))
    print("R10D2_PATCHED=" + str(REFERENCE_TARGET))
    print("R10D2_BACKUP=" + str(BACKUP))
    print("R10D2_BACKUP=" + str(REFERENCE_BACKUP))
    for name in ("build_shared_typed_bridge", "shared_expansion_provider"):
        print("R10D2_FULL_FUNCTION=" + str(OUT / (name + "_FULL.py")))
    print("R10D2_FULL_FUNCTION=" + str(OUT / "project_reference_bodies_FULL.py"))
    print("R10D2_FULL_FILE=" + str(OUT / "phase165_r52_r9_shared_math.py.FULL"))
    print("R10D2_FULL_FILE=" + str(OUT / "phase168_r3_37c_reference_projection.py.FULL"))


if __name__ == "__main__":
    main()

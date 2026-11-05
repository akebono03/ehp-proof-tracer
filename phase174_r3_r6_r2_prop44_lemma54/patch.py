"""Exact, fail-closed patch against the reviewed Phase 174 R3-R6 develop baseline."""
from __future__ import annotations

import ast
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
HEAD = "e4a5b73962bb98acb62b5335ffecae4728d98378"
BLOBS = {
    "phase165_r52_r27_r5_literature.py": "c9bfe2788f4cf043db6dada98a437afea6accf75",
    "phase169_r4b_prop44_injectivity/rule.py": "aba4c769f2e6bc9a3359c2f8e4b4fa7d869aac4b",
    "phase165_r52_r9_shared_math.py": "bf5bc76c842a6fcac65fc88846f96a95917d0624",
    "phase168_r3_37c_reference_projection.py": "fac793665068c5ae8ac51c413687123a470cfbd8",
    "phase168_r3_5_model_renderer.py": "eb34d6fd4783ca943e07de6e6d9756d0e85ff9b8",
    "phase169_r4b_prop44_injectivity/tests/test_r4b_prop44_injectivity.py": "9bcec30bb228126e1e7670a221d447a524219d0c",
    "phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py": "bd3244471191a6dda4d1deba7c7cf419e896623b",
    "phase174_r3_r5_preflight/audit.py": "0e00b6514ffd1b7eed79708b48081af8482dac0f",
    "phase174_r3_r4_public_delta_connection/tests/test_connection.py": "59e0905444f73a656b24a4528edaeeddad2ebda6",
}


def run_git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=ROOT, check=True,
                          capture_output=True, text=True, encoding="utf-8").stdout.strip()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n")


def replace_one(text: str, before: str, after: str, *, label: str) -> str:
    if text.count(before) != 1:
        raise ValueError(f"Unreviewed source context: {label}: {text.count(before)}")
    return text.replace(before, after, 1)


def full_unit(text: str, name: str) -> str:
    tree = ast.parse(text)
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))
               and node.name == name]
    if len(matches) != 1:
        raise ValueError("Expected one complete unit: " + name)
    node = matches[0]
    start = min([node.lineno] + [d.lineno for d in node.decorator_list]) - 1
    return "\n".join(text.split("\n")[start:node.end_lineno]) + "\n"


PROP44_CLASS = '''@dataclass(frozen=True)
class TodaProp44UniversalStatement:
    """Toda Proposition 4.4: a conditional isomorphism, not existence of alpha.

    The hypothesis H(alpha)=+/-iota is proved independently before use.
    The preceding Hopf-fibration paragraph is NOT part of the proposition.
    """
    source_condition: str = "alpha in pi_(2n-1)^n; H(alpha)=+/-iota_(2n-1)"
    isomorphism_map: str = "(beta,gamma)->E(beta)+alpha o gamma"
    source_group: str = "pi_(i-1)^(n-1) + pi_i^(2n-1)"
    target_group: str = "pi_i^n"
    quantifiers: tuple[str, ...] = ("n", "i", "alpha")
    includes_suspension_injectivity: bool = True
'''

RULES = '''def prop44_hopf_four_injectivity_rule(goal: MapInjective) -> InferenceRule:
    """Apply conditional Proposition 4.4 to a proved Lemma 5.4 Hopf witness."""
    from phase173_r4_r1_lemma54_source_bridge.source import (
        TodaLemma54TypedSource,
        canonical_hopf_relation,
    )
    from proof import Relation, RelationType

    if not _is_hopf_four_suspension(goal):
        raise ValueError("goal must be an n=4 suspension injectivity")
    hopf = canonical_hopf_relation()
    proposition = TodaProp44UniversalStatement()

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.GIVEN
            and premises[0].conclusion == proposition
            and premises[1].rule is ProofRule.INFERENCE
            and premises[1].conclusion == hopf
            and len(premises[1].premises) == 1
            and premises[1].premises[0].rule is ProofRule.GIVEN
            and type(premises[1].premises[0].conclusion) is TodaLemma54TypedSource
            and premises[1].premises[0].conclusion == TodaLemma54TypedSource()
            and _is_hopf_four_suspension(goal)
        )

    return InferenceRule(
        name="Toda Proposition 4.4 using separately proved Hopf invariant",
        description=(
            "Proposition 4.4 is conditional; independently prove H(nu_4)=iota_7 "
            "from the earlier, screened Lemma 5.4 before specializing it."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=TodaProp44UniversalStatement,
                statement_pattern=proposition,
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=hopf,
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Proposition 4.4", locator="Proposition 4.4",
        ),
    )


def expand_cited_prop44_injectivity(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Propose the conditional theorem only when Lemma 5.4 is source-screened."""
    from phase173_r4_r1_lemma54_source_bridge.source import (
        TodaLemma54TypedSource,
        canonical_hopf_relation,
    )

    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not _is_hopf_four_suspension(goal):
        return ()
    proposition = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    if available.count(proposition) != 1 or available.count(lemma) != 1:
        return ()
    return (GoalExpansion(
        prop44_hopf_four_injectivity_rule(goal),
        (proposition, canonical_hopf_relation()),
    ),)
'''


def patch_literature(text: str) -> str:
    text = replace_one(text, full_unit(text, "TodaProp44UniversalStatement"),
                       PROP44_CLASS.rstrip() + "\n", label="conditional proposition class")
    return replace_one(
        text,
        '    verify_prop44_hopf_fibration_source()\n    registry = UnifiedStatementRegistry()\n',
        '    registry = UnifiedStatementRegistry()\n',
        label="decouple conditional proposition source from prelude",
    )


def patch_injectivity(text: str) -> str:
    start = text.index("def prop44_hopf_four_injectivity_rule(")
    end = len(text)
    # These two functions are the final units in the reviewed R4-B module.
    if text.count("def prop44_hopf_four_injectivity_rule(") != 1 or text.count("def expand_cited_prop44_injectivity(") != 1:
        raise ValueError("Unreviewed R4-B rule structure")
    return text[:start] + RULES


def patch_shared(text: str) -> str:
    before = '        sources = sources + (build_cited_extension_sources(),)\n'
    after = (before +
        '        from phase174_r3_r6_r2_prop44_lemma54.source import (\n'
        '            build_cited_preprop44_splitting,\n'
        '        )\n'
        '        sources = sources + (build_cited_preprop44_splitting(),)\n')
    text = replace_one(text, before, after, label="independent prelude source")
    before = ('        from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity\n'
              '        options.extend(expand_cited_prop44_injectivity(goal, tuple(available)))\n')
    after = (
        '        from phase174_r3_r6_r2_prop44_lemma54.source import (\n'
        '            expand_cited_preprop44_splitting,\n'
        '        )\n'
        '        options.extend(expand_cited_preprop44_splitting(goal, tuple(available)))\n'
        '        from phase173_r4_r1_lemma54_source_bridge.source import (\n'
        '            expand_cited_lemma54_hopf,\n'
        '        )\n'
        '        options.extend(expand_cited_lemma54_hopf(goal, tuple(available)))\n'
        '        from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity\n'
        '        conditional_prop44 = expand_cited_prop44_injectivity(goal, tuple(available))\n'
        '        if conditional_prop44:\n'
        '            return conditional_prop44\n'
    )
    text = replace_one(text, before, after, label="general typed proof providers")
    before = ('        if pi74_connection is not None:\n'
              '            bridge, citing_assertion_id, expansion_provider = pi74_connection\n'
              '    assertions = tuple(bridge.registry._assertions.values())\n')
    after = ('        if pi74_connection is not None:\n'
             '            bridge, citing_assertion_id, expansion_provider = pi74_connection\n'
             '    if citing_assertion_id is not None and expansion_provider is None:\n'
             '        from phase174_r3_r6_r2_prop44_lemma54.source import (\n'
             '            attach_earlier_verified_lemma54,\n'
             '        )\n'
             '        bridge = attach_earlier_verified_lemma54(bridge, citing_assertion_id)\n'
             '    assertions = tuple(bridge.registry._assertions.values())\n')
    return replace_one(text, before, after, label="source-first citation admission")


def patch_projection(text: str) -> str:
    old = ('    from phase165_r52_r27_r5_literature import Toda52UniversalStatement, TodaProp44UniversalStatement\n')
    new = (old +
           '    from phase174_r3_r6_r2_prop44_lemma54.source import (\n'
           '        TodaPreProp44SplittingStatement,\n'
           '    )\n')
    text = replace_one(text, old, new, label="reference-projector import")
    old = ('            elif (type(statement) is TodaProp44UniversalStatement\n'
           '                  and statement == TodaProp44UniversalStatement()\n'
           '                  and statement.preceding_hopf_fibration_dimensions == (2, 4, 8)):\n')
    new = ('            elif (type(statement) is TodaProp44UniversalStatement\n'
           '                  and statement == TodaProp44UniversalStatement()):\n')
    text = replace_one(text, old, new, label="conditional proposition projection")
    anchor = '            elif isinstance(statement, TodaProp42GeneralExactnessStatement):\n'
    inserted = (
        '            elif (type(statement) is TodaPreProp44SplittingStatement\n'
        '                  and statement == TodaPreProp44SplittingStatement()):\n'
        '                sentence = (\n'
        '                    r"$n=2,4,8$ では Hopf fibration $h:S^{2n-1}\\to S^n$ "\n'
        '                    r"が存在し, 任意の $i$ で "\n'
        '                    r"$E+h_*:\\pi_{i-1}^{n-1}\\oplus\\pi_i^{2n-1}"\n'
        '                    r"\\xrightarrow{\\cong}\\pi_i^n$ が成り立つ "\n'
        '                    r"(Steenrod 1951 を引用)."\n'
        '                )\n'
    )
    return replace_one(text, anchor, inserted + anchor, label="independent prelude reference")


def patch_renderer(text: str) -> str:
    start = text.find('                    # R4F: the source paragraph immediately BEFORE Prop. 4.4\n')
    end_anchor = '                        lines.extend((application, ""))\n'
    end = text.find(end_anchor, start)
    if start < 0 or end < start or text.count(end_anchor) != 1:
        raise ValueError("Unreviewed handwritten Hopf fibration narrative")
    return text[:start] + text[end + len(end_anchor):]


PREFLIGHT_FUNCTION = '''def inspect_source_provider(root: Path) -> dict[str, Any]:
    """Compare against the pinned current HEAD or the exact reviewed new provider."""
    file = root / SOURCE_FILE
    source = file.read_bytes()
    parsed = ast.parse(source.decode("utf-8-sig"))
    functions = [
        node for node in parsed.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "shared_expansion_provider"
    ]
    if len(functions) != 1:
        raise ValueError("shared_expansion_provider must have one definition")
    if source.count(DELTA_HOOK.encode("utf-8")) != 1:
        raise ValueError("R3-R4 general Delta-zero hook is absent or duplicated")
    import subprocess
    from phase174_r3_r6_r2_prop44_lemma54.patch import git_blob, normalize, patch_shared

    original = subprocess.run(
        ("git", "show", "HEAD:" + SOURCE_FILE),
        cwd=root, check=True, capture_output=True,
    ).stdout
    if git_blob(original) != "bf5bc76c842a6fcac65fc88846f96a95917d0624":
        raise ValueError("Unexpected committed R3-R6 source")
    original_text = normalize(original.decode("utf-8-sig"))
    expected = patch_shared(original_text)
    normalized_current = normalize(source.decode("utf-8-sig"))
    if normalized_current not in (original_text, expected):
        raise ValueError("Unreviewed production source modifications")
    state = "COMMITTED" if normalized_current == original_text else "WORKTREE_PATCHED"
    return {
        "state": state,
        "delta_provider_hook_present": True,
        "full_function_line_count": functions[0].end_lineno - functions[0].lineno + 1,
        "production_source_changed_by_this_audit": False,
    }
'''


def patch_preflight(text: str) -> str:
    return replace_one(
        text, full_unit(text, "inspect_source_provider"),
        PREFLIGHT_FUNCTION.rstrip() + "\n", label="strict preflight source guard",
    )


def patch_r3r4_test(text: str) -> str:
    before = ("    from phase174_r3_r6_source_extension.patch import connect_shared\n"
              "    old = git('show', 'b5f5208a7e23397834e4a38ad307c660a4f26b59:phase165_r52_r9_shared_math.py')\n")
    after = ("    from phase174_r3_r6_source_extension.patch import connect_shared\n"
             "    from phase174_r3_r6_r2_prop44_lemma54.patch import patch_shared\n"
             "    old = git('show', 'b5f5208a7e23397834e4a38ad307c660a4f26b59:phase165_r52_r9_shared_math.py')\n")
    text = replace_one(text, before, after, label="R3-R4 cumulative test import")
    before = "    assert current in (r3r4, r3r5, connect_shared(r3r5))\n"
    after = ("    r3r6 = connect_shared(r3r5)\n"
             "    new_source = patch_shared(r3r6.decode('utf-8')).encode('utf-8')\n"
             "    assert current in (r3r4, r3r5, r3r6, new_source)\n")
    return replace_one(text, before, after, label="R3-R4 cumulative test guard")


def patch_r4b_tests(text: str) -> str:
    if text.count("def test_r4b_source_bound_dim4_has_one_proposal") != 1:
        raise ValueError("R4-B tests changed")
    return (PACKAGE / "overrides/test_r4b_prop44_injectivity.py").read_text(encoding="utf-8")


def patch_r4g_tests(text: str) -> str:
    if text.count("def test_r4g_typed_prop44_cannot_accept_fake_fibration_metadata") != 1:
        raise ValueError("R4-G tests changed")
    return (PACKAGE / "overrides/test_r4g_hopf_reference.py").read_text(encoding="utf-8")


TRANSFORM = {
    "phase165_r52_r27_r5_literature.py": patch_literature,
    "phase169_r4b_prop44_injectivity/rule.py": patch_injectivity,
    "phase165_r52_r9_shared_math.py": patch_shared,
    "phase168_r3_37c_reference_projection.py": patch_projection,
    "phase168_r3_5_model_renderer.py": patch_renderer,
    "phase169_r4b_prop44_injectivity/tests/test_r4b_prop44_injectivity.py": patch_r4b_tests,
    "phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py": patch_r4g_tests,
    "phase174_r3_r5_preflight/audit.py": patch_preflight,
    "phase174_r3_r4_public_delta_connection/tests/test_connection.py": patch_r3r4_test,
}


def verified_changes() -> dict[str, tuple[bytes, bytes]]:
    if run_git("branch", "--show-current") != "develop":
        raise ValueError("Expected develop branch")
    if run_git("rev-parse", "HEAD") != HEAD:
        raise ValueError("Unreviewed local HEAD")
    remote = run_git("ls-remote", "origin", "refs/heads/develop").split()[0]
    if remote != HEAD:
        raise ValueError("Unreviewed remote HEAD")
    if run_git("diff", "--cached", "--name-only"):
        raise ValueError("Staged changes require review")
    result: dict[str, tuple[bytes, bytes]] = {}
    for path, sha in BLOBS.items():
        original = subprocess.run(("git", "show", "HEAD:" + path), cwd=ROOT,
                                  capture_output=True, check=True).stdout
        if git_blob(original) != sha:
            raise ValueError("Reviewed Git blob changed: " + path)
        text = normalize(original.decode("utf-8-sig"))
        updated = TRANSFORM[path](text)
        ast.parse(updated, filename=path)
        modified = updated.encode("utf-8")
        current = (ROOT / path).read_bytes()
        # Only the literal reviewed original or this exact patch is accepted.
        if normalize(current.decode("utf-8-sig")) not in (text, updated):
            raise ValueError("Unreviewed working source: " + path)
        result[path] = (original, modified)
    return result


def execute(dry_run: bool) -> None:
    edits = verified_changes()
    print("PHASE174_R3R6R2_SOURCE_GUARD=PASS")
    print("PHASE174_R3R6R2_REVIEWED_HEAD=" + HEAD)
    print("PHASE174_R3R6R2_TARGET_FILES=" + str(len(edits)))
    if dry_run:
        print("PHASE174_R3R6R2_DRY_RUN_GATE=PASS")
        return
    snapshots = {path: (ROOT / path).read_bytes() for path in edits}
    try:
        for path, (before, after) in edits.items():
            (ROOT / path).write_bytes(after)
        output = PACKAGE / "output"
        output.mkdir(exist_ok=True)
        for path in edits:
            content = (ROOT / path).read_text(encoding="utf-8")
            (output / (path.replace("/", "__") + ".FULL.py")).write_text(
                content, encoding="utf-8",
            )
            for name in {
                "phase165_r52_r27_r5_literature.py": ("TodaProp44UniversalStatement", "build_typed_literature_bridge"),
                "phase169_r4b_prop44_injectivity/rule.py": (
                    "prop44_hopf_four_injectivity_rule", "expand_cited_prop44_injectivity"),
                "phase165_r52_r9_shared_math.py": (
                    "build_shared_typed_bridge", "shared_expansion_provider", "search_shared_group_goal"),
                "phase168_r3_37c_reference_projection.py": ("project_reference_bodies",),
                "phase168_r3_5_model_renderer.py": ("render_model_backed_narrative_markdown",),
                "phase169_r4b_prop44_injectivity/tests/test_r4b_prop44_injectivity.py": (),
                "phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py": (),
                "phase174_r3_r5_preflight/audit.py": ("inspect_source_provider",),
                "phase174_r3_r4_public_delta_connection/tests/test_connection.py":
                    ("test_r3r4_real_production_file_has_only_reviewed_wiring",),
            }[path]:
                (output / (name + "_FULL.py")).write_text(full_unit(content, name), encoding="utf-8")
        print("PHASE174_R3R6R2_PATCH=PASS")
        print("PHASE174_R3R6R2_FULL_REPLACEMENTS=" + str(output))
    except BaseException:
        for path, content in snapshots.items():
            (ROOT / path).write_bytes(content)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    execute(args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

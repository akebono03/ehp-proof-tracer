# Phase 174 R3-R6-R4 — 変更コード全文

GitHub のレビュー済み `develop` の対象 Git blob `754e63cf4beee3c882c601dbe4b97cb8ecbdc4d2` とソース全文を照合したうえで、既存 `project_reference_bodies()` に2箇所だけ追加した。変更後 import（関数内 import 全部）と関数・モジュール全文は以下に示す。

## 変更後の既存関数 `project_reference_bodies()` — 全文

```python
def project_reference_bodies(registry, assertion_ids):
    """Project only cited, typed source statements, including registered composite fields.

    Composite expansion follows the assertion's registered field scope. It does
    not read text from a literature catalog or create a new proof premise.
    """
    if registry is None:
        return ()
    from dataclasses import fields, is_dataclass
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase169_r10d2_general_family_definition.family_citation import (
        CitedStableFamilyDefinition, cited_family_reference_sentence,
    )
    from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
    from phase165_r12_r15_toda51 import Toda51BelowDiagonalZeroStatement
    from phase165_r52_r27_r5_literature import Toda52UniversalStatement, TodaProp44UniversalStatement
    from phase174_r3_r6_r2_prop44_lemma54.source import (
        TodaPreProp44SplittingStatement,
    )
    from phase165_r57_r8_eta_specialization import _is_generic_eta_group_relation
    from toda_rules import Toda45IsomorphismStatement
    from expression import ScalarSymbol, ScalarSum, ScalarProduct
    from homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroupZeroStatement
    from proof import Relation
    from phase174_r3_r6_r4_common_reference.projection import (
        project_cited_universal_toda_reference_body,
    )

    result = []
    for assertion_id in assertion_ids:
        assertion = registry.assertion(assertion_id)
        content = assertion.content
        scope = getattr(assertion, "scope", ())
        statements = (content,)
        if (isinstance(scope, tuple) and len(scope) >= 2
                and scope[0] == "typed_composite_fields"):
            field_names = scope[1]
            if not isinstance(field_names, tuple) or len(field_names) < 2:
                raise ValueError("registered composite field scope is inconsistent")
            content_fields = (
                tuple(field.name for field in fields(content))
                if is_dataclass(content) and not isinstance(content, type) else ()
            )
            if content_fields == field_names:
                statements = tuple(getattr(content, field_name) for field_name in field_names)
            else:
                # The registered component bridge retains the parent's scope
                # on an atomic child. Validate the exact parent dependency and
                # field content instead of expanding this child a second time.
                dependencies = getattr(assertion, "dependencies", ())
                if not isinstance(dependencies, tuple) or len(dependencies) != 1:
                    raise ValueError("registered composite field scope is inconsistent")
                parent = registry.assertion(dependencies[0])
                parent_content = parent.content
                parent_fields = (
                    tuple(field.name for field in fields(parent_content))
                    if is_dataclass(parent_content) and not isinstance(parent_content, type)
                    else ()
                )
                if (parent.scope != scope
                        or parent_fields != field_names
                        or not any(
                            type(content) is type(getattr(parent_content, field_name))
                            and content == getattr(parent_content, field_name)
                            for field_name in field_names
                        )):
                    raise ValueError("registered composite field scope is inconsistent")

        for statement in statements:
            sentence = _verified_source_sentence(statement)
            if isinstance(statement, TodaEtaFamilyGeneralDefinition):
                if statement.lower_bound == 2:
                    sentence = r"$n\ge 2$ に対し, $\eta_n=E^{n-2}\eta_2$ と定義する."
            elif isinstance(statement, CitedStableFamilyDefinition):
                sentence = cited_family_reference_sentence(statement)
            elif (isinstance(statement, TodaPrimaryGroupZeroStatement)
                  and isinstance(statement.group.group_dimension, ScalarSymbol)
                  and statement.group.sphere_dimension == 1):
                sentence = r"$\pi_i^1=0\quad(i>1)$."
            elif isinstance(statement, Toda51BelowDiagonalZeroStatement):
                sentence = r"$\pi_i^n=0\quad(i<n)$."
            elif (type(statement) is TodaProp44UniversalStatement
                  and statement == TodaProp44UniversalStatement()):
                sentence = (
                    r"$\alpha\in\pi_{2n-1}^{n}$ で "
                    r"$H(\alpha)=\pm\iota_{2n-1}$ とする."
                    "\n"
                    r"このとき, 任意の $i$ に対して次の写像は同型である."
                    "\n"
                    r"$\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}"
                    r"\xrightarrow{\;\cong\;}\pi_i^n,\quad"
                    r"(\beta,\gamma)\longmapsto E\beta+\alpha\circ\gamma$."
                    "\n"
                    r"特に $E:\pi_{i-1}^{n-1}\to\pi_i^{n}$ は単射である."
                )
            elif (type(statement) is TodaPreProp44SplittingStatement
                  and statement == TodaPreProp44SplittingStatement()):
                sentence = (
                    r"$n=2,4,8$ では Hopf fibration $h:S^{2n-1}\to S^n$ "
                    r"が存在し, 任意の $i$ で "
                    r"$E+h_*:\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}"
                    r"\xrightarrow{\cong}\pi_i^n$ が成り立つ "
                    r"(Steenrod 1951 を引用)."
                )
            elif isinstance(statement, TodaProp42GeneralExactnessStatement):
                sentence = (
                    r"$\pi_i^n\xrightarrow{E}\pi_{i+1}^{n+1}"
                    r"\xrightarrow{H}\pi_{i+1}^{2n+1}"
                    r"\xrightarrow{\Delta}\pi_{i-1}^{n}"
                    r"\xrightarrow{E}\pi_i^{n+1}$ は完全."
                )
            elif isinstance(statement, Toda52UniversalStatement):
                if (statement.variable == "i" and statement.minimum_i == 3
                        and statement.map_formula == "alpha -> eta_2 o alpha"
                        and statement.source_group == "pi_i^3"
                        and statement.target_group == "pi_i^2"):
                    sentence = (
                        r"$i\ge 3$ に対し, "
                        r"$\eta_2\circ(-):\pi_i^3\xrightarrow{\cong}\pi_i^2$ は同型."
                    )
            elif isinstance(statement, Toda45IsomorphismStatement):
                mapping = statement.map
                n, m, k = ScalarSymbol("n"), ScalarSymbol("m"), ScalarSymbol("k")
                if (
                    isinstance(mapping, TodaIteratedSuspensionMap)
                    and mapping.exponent == ScalarSum(left=m, right=ScalarProduct(left=-1, right=n))
                    and mapping.source_group.sphere_dimension == n
                    and mapping.target_group.sphere_dimension == m
                    and mapping.source_group.group_dimension == ScalarSum(left=n, right=k)
                    and mapping.target_group.group_dimension == ScalarSum(left=m, right=k)
                ):
                    sentence = (
                        r"$n\ge k+2$, $m\ge n$, $k\ge0$ に対し, "
                        r"$E^{m-n}:\pi_{n+k}^{n}\xrightarrow{\cong}\pi_{m+k}^{m}$ "
                        r"が成り立つ."
                    )
            elif isinstance(statement, Relation) and _is_generic_eta_group_relation(statement):
                # The typed source schema, already guarded by the general
                # eta-group recognizer, has the documented n >= 4 range.
                variable = statement.lhs.sphere_dimension.name
                sentence = (
                    r"$\pi_{" + variable + r"+1}^{" + variable + r"}="
                    r"\mathbb{Z}/2\{\eta_{" + variable + r"}\}"
                    r"\quad(" + variable + r"\ge4)$."
                )
            if sentence is None:
                sentence = project_cited_universal_toda_reference_body(
                    assertion, registry, statement,
                )
            if sentence is None:
                sentence = typed_sentence(statement, None)
            if sentence is None:
                latex, fallback = _group_proof_statement_latex(statement)
                if latex is not None and fallback is None:
                    sentence = "$" + latex + "$."
            if (sentence is not None and r"\pi_{n}^{n}" in sentence
                    and r"\mathbb{Z}" in sentence and r"n\ge" not in sentence
                    and sentence.endswith("$.")):
                sentence = sentence[:-2] + r"\quad(n\ge 1)$."
            if sentence is not None and sentence not in result:
                result.append(sentence)
    return tuple(result)
```

## 変更後の既存モジュール `phase168_r3_37c_reference_projection.py` — 全文

```python
"""Common typed reference sentence projection. No source lookup."""
from phase168_r3_27_typed_statement_projection import typed_sentence
from web_group_proof_common import _group_proof_statement_latex


def _verified_source_sentence(statement: object) -> str | None:
    """Render a fully source-screened typed statement without deducing a fact."""
    from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource

    if type(statement) is TodaLemma54TypedSource and statement == TodaLemma54TypedSource():
        return (
            r"$\nu_4\in\pi_7^4$, "
            r"$H(\nu_4)=\iota_7$ および "
            r"$2E\nu_4=E^2\nu'$."
        )
    return None


def project_cited_proof_step_reference_bodies(
    reference: object, cited_steps: tuple[object, ...],
) -> tuple[str, ...]:
    """Use an already cited GIVEN statement if registry links do not expose its body.

    The citation must already own the exact source step; simply finding a
    literature locator or a mathematically similar statement is insufficient.
    """
    from proof import LiteratureReference, ProofRule, ProofStep

    if not isinstance(reference, LiteratureReference) or not isinstance(cited_steps, tuple):
        return ()
    locator = reference.locator or reference.label
    candidates = tuple(
        (step, _verified_source_sentence(step.conclusion))
        for step in cited_steps
        if isinstance(step, ProofStep) and step.rule is ProofRule.GIVEN
        and not step.premises
    )
    verified = tuple(
        sentence for step, sentence in candidates
        if sentence is not None and locator == "Lemma 5.4"
    )
    return verified if len(verified) == 1 else ()


def project_reference_bodies(registry, assertion_ids):
    """Project only cited, typed source statements, including registered composite fields.

    Composite expansion follows the assertion's registered field scope. It does
    not read text from a literature catalog or create a new proof premise.
    """
    if registry is None:
        return ()
    from dataclasses import fields, is_dataclass
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase169_r10d2_general_family_definition.family_citation import (
        CitedStableFamilyDefinition, cited_family_reference_sentence,
    )
    from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
    from phase165_r12_r15_toda51 import Toda51BelowDiagonalZeroStatement
    from phase165_r52_r27_r5_literature import Toda52UniversalStatement, TodaProp44UniversalStatement
    from phase174_r3_r6_r2_prop44_lemma54.source import (
        TodaPreProp44SplittingStatement,
    )
    from phase165_r57_r8_eta_specialization import _is_generic_eta_group_relation
    from toda_rules import Toda45IsomorphismStatement
    from expression import ScalarSymbol, ScalarSum, ScalarProduct
    from homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroupZeroStatement
    from proof import Relation
    from phase174_r3_r6_r4_common_reference.projection import (
        project_cited_universal_toda_reference_body,
    )

    result = []
    for assertion_id in assertion_ids:
        assertion = registry.assertion(assertion_id)
        content = assertion.content
        scope = getattr(assertion, "scope", ())
        statements = (content,)
        if (isinstance(scope, tuple) and len(scope) >= 2
                and scope[0] == "typed_composite_fields"):
            field_names = scope[1]
            if not isinstance(field_names, tuple) or len(field_names) < 2:
                raise ValueError("registered composite field scope is inconsistent")
            content_fields = (
                tuple(field.name for field in fields(content))
                if is_dataclass(content) and not isinstance(content, type) else ()
            )
            if content_fields == field_names:
                statements = tuple(getattr(content, field_name) for field_name in field_names)
            else:
                # The registered component bridge retains the parent's scope
                # on an atomic child. Validate the exact parent dependency and
                # field content instead of expanding this child a second time.
                dependencies = getattr(assertion, "dependencies", ())
                if not isinstance(dependencies, tuple) or len(dependencies) != 1:
                    raise ValueError("registered composite field scope is inconsistent")
                parent = registry.assertion(dependencies[0])
                parent_content = parent.content
                parent_fields = (
                    tuple(field.name for field in fields(parent_content))
                    if is_dataclass(parent_content) and not isinstance(parent_content, type)
                    else ()
                )
                if (parent.scope != scope
                        or parent_fields != field_names
                        or not any(
                            type(content) is type(getattr(parent_content, field_name))
                            and content == getattr(parent_content, field_name)
                            for field_name in field_names
                        )):
                    raise ValueError("registered composite field scope is inconsistent")

        for statement in statements:
            sentence = _verified_source_sentence(statement)
            if isinstance(statement, TodaEtaFamilyGeneralDefinition):
                if statement.lower_bound == 2:
                    sentence = r"$n\ge 2$ に対し, $\eta_n=E^{n-2}\eta_2$ と定義する."
            elif isinstance(statement, CitedStableFamilyDefinition):
                sentence = cited_family_reference_sentence(statement)
            elif (isinstance(statement, TodaPrimaryGroupZeroStatement)
                  and isinstance(statement.group.group_dimension, ScalarSymbol)
                  and statement.group.sphere_dimension == 1):
                sentence = r"$\pi_i^1=0\quad(i>1)$."
            elif isinstance(statement, Toda51BelowDiagonalZeroStatement):
                sentence = r"$\pi_i^n=0\quad(i<n)$."
            elif (type(statement) is TodaProp44UniversalStatement
                  and statement == TodaProp44UniversalStatement()):
                sentence = (
                    r"$\alpha\in\pi_{2n-1}^{n}$ で "
                    r"$H(\alpha)=\pm\iota_{2n-1}$ とする."
                    "\n"
                    r"このとき, 任意の $i$ に対して次の写像は同型である."
                    "\n"
                    r"$\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}"
                    r"\xrightarrow{\;\cong\;}\pi_i^n,\quad"
                    r"(\beta,\gamma)\longmapsto E\beta+\alpha\circ\gamma$."
                    "\n"
                    r"特に $E:\pi_{i-1}^{n-1}\to\pi_i^{n}$ は単射である."
                )
            elif (type(statement) is TodaPreProp44SplittingStatement
                  and statement == TodaPreProp44SplittingStatement()):
                sentence = (
                    r"$n=2,4,8$ では Hopf fibration $h:S^{2n-1}\to S^n$ "
                    r"が存在し, 任意の $i$ で "
                    r"$E+h_*:\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}"
                    r"\xrightarrow{\cong}\pi_i^n$ が成り立つ "
                    r"(Steenrod 1951 を引用)."
                )
            elif isinstance(statement, TodaProp42GeneralExactnessStatement):
                sentence = (
                    r"$\pi_i^n\xrightarrow{E}\pi_{i+1}^{n+1}"
                    r"\xrightarrow{H}\pi_{i+1}^{2n+1}"
                    r"\xrightarrow{\Delta}\pi_{i-1}^{n}"
                    r"\xrightarrow{E}\pi_i^{n+1}$ は完全."
                )
            elif isinstance(statement, Toda52UniversalStatement):
                if (statement.variable == "i" and statement.minimum_i == 3
                        and statement.map_formula == "alpha -> eta_2 o alpha"
                        and statement.source_group == "pi_i^3"
                        and statement.target_group == "pi_i^2"):
                    sentence = (
                        r"$i\ge 3$ に対し, "
                        r"$\eta_2\circ(-):\pi_i^3\xrightarrow{\cong}\pi_i^2$ は同型."
                    )
            elif isinstance(statement, Toda45IsomorphismStatement):
                mapping = statement.map
                n, m, k = ScalarSymbol("n"), ScalarSymbol("m"), ScalarSymbol("k")
                if (
                    isinstance(mapping, TodaIteratedSuspensionMap)
                    and mapping.exponent == ScalarSum(left=m, right=ScalarProduct(left=-1, right=n))
                    and mapping.source_group.sphere_dimension == n
                    and mapping.target_group.sphere_dimension == m
                    and mapping.source_group.group_dimension == ScalarSum(left=n, right=k)
                    and mapping.target_group.group_dimension == ScalarSum(left=m, right=k)
                ):
                    sentence = (
                        r"$n\ge k+2$, $m\ge n$, $k\ge0$ に対し, "
                        r"$E^{m-n}:\pi_{n+k}^{n}\xrightarrow{\cong}\pi_{m+k}^{m}$ "
                        r"が成り立つ."
                    )
            elif isinstance(statement, Relation) and _is_generic_eta_group_relation(statement):
                # The typed source schema, already guarded by the general
                # eta-group recognizer, has the documented n >= 4 range.
                variable = statement.lhs.sphere_dimension.name
                sentence = (
                    r"$\pi_{" + variable + r"+1}^{" + variable + r"}="
                    r"\mathbb{Z}/2\{\eta_{" + variable + r"}\}"
                    r"\quad(" + variable + r"\ge4)$."
                )
            if sentence is None:
                sentence = project_cited_universal_toda_reference_body(
                    assertion, registry, statement,
                )
            if sentence is None:
                sentence = typed_sentence(statement, None)
            if sentence is None:
                latex, fallback = _group_proof_statement_latex(statement)
                if latex is not None and fallback is None:
                    sentence = "$" + latex + "$."
            if (sentence is not None and r"\pi_{n}^{n}" in sentence
                    and r"\mathbb{Z}" in sentence and r"n\ge" not in sentence
                    and sentence.endswith("$.")):
                sentence = sentence[:-2] + r"\quad(n\ge 1)$."
            if sentence is not None and sentence not in result:
                result.append(sentence)
    return tuple(result)
```

## 新規 projection.py — 全文

```python
"""Read-only Reference prose for previously registered, source-checked Toda laws.

The registered source assertion, not a nearby string, inferred group goal, or
bibliography heading, authorizes each formula.  No inference or new GIVEN is
constructed here.  This projection applies to every valid cited instance.
"""
from __future__ import annotations

from phase174_r3_r5_finite_cyclic_extension.rule import (
    Toda48UniversalConditionalStatement,
)
from phase174_r3_r6_source_extension.source import Toda55UniversalDoubleStatement
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def project_cited_universal_toda_reference_body(
    assertion: object, registry: object, statement: object,
) -> str | None:
    """Display one authenticated general GIVEN, retaining its source conditions.

    A matching locator or a forged dataclass alone is never sufficient.  The
    caller must supply the actual, already cited registry assertion.  Source
    text checking and publication screening happen upstream, not in Renderer.
    """
    if not isinstance(assertion, AssertionEntry) or not isinstance(
        registry, UnifiedStatementRegistry
    ):
        return None

    if type(statement) is Toda48UniversalConditionalStatement:
        locator = "(4.8)"
        source_chapter = "04"
        publication_position = 7500
        canonical = Toda48UniversalConditionalStatement()
        sentence = (
            r"$n$ を偶数とし, $\Delta(\iota_{2n-1})=0$ と仮定する."
            "\n"
            r"このとき $E^2:\pi_{2n-2}^{n-1}\hookrightarrow\pi_{2n}^{n+1}$ は単射で, "
            r"$\pi_{2n}^{n+1}/E^2(\pi_{2n-2}^{n-1})\cong\mathbb{Z}/2$."
        )
    elif type(statement) is Toda55UniversalDoubleStatement:
        locator = "(5.5)"
        source_chapter = "05"
        publication_position = 8600
        canonical = Toda55UniversalDoubleStatement()
        sentence = r"$n\ge5$ に対し, $2\nu_n=E^{n-3}\nu'$."
    else:
        return None

    # The assertion must be the object owned by this exact registry, not
    # a free-standing imitation with a convincing citation label.
    try:
        registered = registry.assertion(assertion.assertion_id)
    except KeyError:
        return None
    if registered is not assertion:
        return None

    if (
        statement != canonical
        or type(assertion.content) is not type(canonical)
        or assertion.content != statement
        or assertion.assertion_id != "toda:174:r3r6:universal:" + locator
        or assertion.reference_id != "toda:" + locator
        or assertion.kind is not AssertionKind.STATEMENT
        or assertion.origin is not AssertionOrigin.FIXED_STATEMENT
        or assertion.scope != (
            "universal formula only", "no direct group conclusion",
        )
        or assertion.dependencies
    ):
        return None

    reference = registry.reference(assertion.reference_id)
    if (
        reference.reference_id != "toda:" + locator
        or reference.kind is not ReferenceKind.EQUATION
        or reference.locator != locator
        or reference.publication_position != publication_position
        or reference.source_id != (
            f"sources/toda/Toda_{source_chapter}_2.tex "
            "(adopted transcription; original edition unverified)"
        )
    ):
        return None
    return sentence
```

## 新規 patch.py — 全文

```python
"""Guarded, scope-limited installation of Phase 174 R3-R6-R4 Reference prose.

Only the existing project_reference_bodies function is extended by two
source-checked presentation lines. All other paths and functions are retained.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("phase168_r3_37c_reference_projection.py")
REVIEWED_REMOTE_HEAD = "f2e148afefb11eb0b0ca31da67c65ec1ffe9e1e9"
REVIEWED_LOCAL_HEADS = (
    "ecbb2fea225c5b88000629d9c025934fcc2d7075",
    REVIEWED_REMOTE_HEAD,
)
REVIEWED_BLOB = "754e63cf4beee3c882c601dbe4b97cb8ecbdc4d2"
MODULE = "phase174_r3_r6_r4_common_reference.projection"

IMPORT_OLD = """    from proof import Relation

    result = []
"""
IMPORT_NEW = """    from proof import Relation
    from phase174_r3_r6_r4_common_reference.projection import (
        project_cited_universal_toda_reference_body,
    )

    result = []
"""
BODY_OLD = """            if sentence is None:
                sentence = typed_sentence(statement, None)
"""
BODY_NEW = """            if sentence is None:
                sentence = project_cited_universal_toda_reference_body(
                    assertion, registry, statement,
                )
            if sentence is None:
                sentence = typed_sentence(statement, None)
"""


def _git(*args: str) -> bytes:
    completed = subprocess.run(
        ("git",) + args,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        message = completed.stderr.decode("utf-8", errors="replace")
        raise ValueError(f"Git preflight rejected {args}: {message.strip()}")
    return completed.stdout


def _git_blob(content: bytes) -> str:
    return sha1(b"blob " + str(len(content)).encode("ascii") + b"\x00" + content).hexdigest()


def _normalized(source: str) -> str:
    return source.replace("\r\n", "\n")


def _replace_one_preserving_ends(source: str, before: str, after: str) -> str:
    """Add one reviewed block, preserving every untouched byte/EOL sequence."""
    candidates = tuple(
        (before.replace("\n", ending), after.replace("\n", ending))
        for ending in ("\r\n", "\n")
    )
    matches = tuple((old, new) for old, new in candidates if source.count(old) == 1)
    if len(matches) != 1:
        raise ValueError("Reviewed insertion anchor is missing or ambiguous")
    old, new = matches[0]
    return source.replace(old, new, 1)


def candidate_source(source: str) -> str:
    """Return an entire replacement module from exactly two reviewed inserts."""
    result = _replace_one_preserving_ends(source, IMPORT_OLD, IMPORT_NEW)
    result = _replace_one_preserving_ends(result, BODY_OLD, BODY_NEW)
    original = ast.parse(source)
    changed = ast.parse(result)
    original_functions = [node.name for node in original.body if isinstance(node, ast.FunctionDef)]
    changed_functions = [node.name for node in changed.body if isinstance(node, ast.FunctionDef)]
    if original_functions != changed_functions:
        raise ValueError("Function API changed during Reference projection patch")
    return result


def _function_source(module: str, name: str) -> str:
    tree = ast.parse(_normalized(module))
    found = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(found) != 1:
        raise ValueError("Expected exactly one existing Reference projection function")
    node = found[0]
    lines = _normalized(module).splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno])


def reviewed_changes() -> tuple[bytes, bool]:
    """Validate the pinned remote and exact target content before any write."""
    branch = _git("branch", "--show-current").decode("ascii").strip()
    local_head = _git("rev-parse", "HEAD").decode("ascii").strip()
    remote_head = _git("rev-parse", "origin/develop").decode("ascii").strip()
    print("PHASE174_R3R6R4_BRANCH=" + branch)
    print("PHASE174_R3R6R4_LOCAL_HEAD=" + local_head)
    print("PHASE174_R3R6R4_REMOTE_HEAD=" + remote_head)
    if branch != "develop" or remote_head != REVIEWED_REMOTE_HEAD:
        raise ValueError("Unreviewed branch or remote HEAD; do not apply")
    if local_head not in REVIEWED_LOCAL_HEADS:
        raise ValueError("Unreviewed local HEAD; do not apply")
    if _git("diff", "--cached", "--name-only", "--", TARGET.as_posix()).strip():
        raise ValueError("Target contains staged changes; do not overwrite")

    baseline = _git("show", f"{REVIEWED_REMOTE_HEAD}:{TARGET.as_posix()}")
    if _git_blob(baseline) != REVIEWED_BLOB:
        raise ValueError("Reviewed reference file blob was replaced")
    target = ROOT / TARGET
    raw = target.read_bytes()
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    local = raw[len(bom):].decode("utf-8")
    canonical = baseline.decode("utf-8")
    expected = candidate_source(canonical)
    if _normalized(local) == _normalized(expected):
        print("PHASE174_R3R6R4_ALREADY_INSTALLED=True")
        return raw, True
    if _normalized(local) != _normalized(canonical):
        raise ValueError("Unreviewed local Reference changes; refusing overwrite")
    revised = candidate_source(local)
    if (len(ast.parse(revised).body) != len(ast.parse(local).body)
            or _normalized(revised) != _normalized(expected)):
        raise ValueError("Unexpected module-level changes after patch")
    return bom + revised.encode("utf-8"), False


def _write_output(candidate: bytes, installed: bool) -> None:
    folder = ROOT / "phase174_r3_r6_r4_common_reference" / "output"
    folder.mkdir(parents=True, exist_ok=True)
    source = candidate.decode("utf-8-sig")
    full = _normalized(source)
    (folder / "phase168_r3_37c_reference_projection.py.FULL.py").write_text(
        full, encoding="utf-8", newline="\n",
    )
    (folder / "project_reference_bodies_FULL.py").write_text(
        _function_source(full, "project_reference_bodies"), encoding="utf-8", newline="\n",
    )
    (folder / "README.txt").write_text(
        "Reviewed HEAD: " + REVIEWED_REMOTE_HEAD + "\n"
        "Production target: " + TARGET.as_posix() + "\n"
        "Entire modified function and entire module are in this directory.\n"
        "Already installed: " + str(installed) + "\n"
        "No other production file is modified.\n",
        encoding="utf-8", newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    candidate, installed = reviewed_changes()
    _write_output(candidate, installed)
    print("PHASE174_R3R6R4_SOURCE_GUARD=PASS")
    print("PHASE174_R3R6R4_PRODUCTION_TARGETS=1")
    print("PHASE174_R3R6R4_NEW_GIVEN=0")
    if args.dry_run:
        print("PHASE174_R3R6R4_DRY_RUN=PASS")
        return 0
    if not installed:
        (ROOT / TARGET).write_bytes(candidate)
    print("PHASE174_R3R6R4_APPLIED=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規 audit.py — 全文

```python
"""Public proof and reference-body audit; does not mutate any proof data."""
from __future__ import annotations

from phase174_r3_r6_r2_prop44_lemma54.audit import inspect


def main() -> int:
    proof = inspect()
    narrative = proof["narrative"]
    if proof["root_status"] != "complete" or proof["root_proven_steps"] != 16:
        raise ValueError("Public completed proof or its 16 steps regressed")
    if proof["new_group_given"] != 0:
        raise ValueError("New direct group GIVEN appeared")
    expected = (
        r"$\Delta(\iota_{2n-1})=0$ と仮定する",
        r"E^2:\pi_{2n-2}^{n-1}\hookrightarrow\pi_{2n}^{n+1}",
        r"\pi_{2n}^{n+1}/E^2(\pi_{2n-2}^{n-1})\cong\mathbb{Z}/2",
        r"$n\ge5$ に対し, $2\nu_n=E^{n-3}\nu'$.",
        r"E^{2}:\pi_{6}^{3}\hookrightarrow \pi_{8}^{5}",
        r"|\pi_{8}^{5}|=2\cdot 4=8",
    )
    if any(formula not in narrative for formula in expected):
        raise ValueError("Missing sourced general statement or prior typed inference")
    if narrative.count("[R4] (4.8).") != 1 or narrative.count("[R7] (5.5).") != 1:
        raise ValueError("Unexpected Reference count")
    roots = tuple(line for line in narrative.splitlines()
                  if r"\pi_{8}^{5}" in line and r"\mathbb{Z}/8" in line and "=" in line)
    if len(roots) != 1:
        raise ValueError("Root group relation is missing or duplicated")
    print("PHASE174_R3R6R4_PI85_COMPLETE=True")
    print("PHASE174_R3R6R4_PROVEN_STEPS=16")
    print("PHASE174_R3R6R4_TODA48_REFERENCE_BODY=True")
    print("PHASE174_R3R6R4_TODA55_REFERENCE_BODY=True")
    print("PHASE174_R3R6R4_R3_NARRATIVE_PRESERVED=True")
    print("PHASE174_R3R6R4_FINAL_CONCLUSION_ONCE=True")
    print("PHASE174_R3R6R4_NEW_GROUP_GIVEN=0")
    print("PHASE174_R3R6R4_AUDIT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規テスト tests/test_r3r4_reference_bodies.py — 全文

```python
"""Focused source-bound Reference projections, not a new proof-search rule."""
from __future__ import annotations

from dataclasses import replace

from phase168_r3_37c_reference_projection import project_reference_bodies
from phase174_r3_r5_finite_cyclic_extension.rule import (
    Toda48UniversalConditionalStatement,
)
from phase174_r3_r6_source_extension.source import (
    Toda55UniversalDoubleStatement,
    build_cited_extension_sources,
)
from phase174_r3_r6_r4_common_reference.projection import (
    project_cited_universal_toda_reference_body,
)
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def test_reviewed_toda48_keeps_condition_and_generic_formula() -> None:
    bridge = build_cited_extension_sources()
    assertion_id = "toda:174:r3r6:universal:(4.8)"
    entry = bridge.registry.assertion(assertion_id)
    body = project_reference_bodies(bridge.registry, (assertion_id,))
    assert len(body) == 1
    assert r"$\Delta(\iota_{2n-1})=0$ と仮定する" in body[0]
    assert r"E^2:\pi_{2n-2}^{n-1}\hookrightarrow\pi_{2n}^{n+1}" in body[0]
    assert r"\pi_{2n}^{n+1}/E^2(\pi_{2n-2}^{n-1})\cong\mathbb{Z}/2" in body[0]
    assert r"\pi_{8}^{5}" not in body[0]
    assert entry.content == Toda48UniversalConditionalStatement()


def test_reviewed_toda55_is_general_and_distinct_from_group_result() -> None:
    bridge = build_cited_extension_sources()
    assertion_id = "toda:174:r3r6:universal:(5.5)"
    body = project_reference_bodies(bridge.registry, (assertion_id,))
    assert body == (r"$n\ge5$ に対し, $2\nu_n=E^{n-3}\nu'$.",)
    assert "\\pi_{8}^{5}" not in body[0]
    assert bridge.registry.assertion(assertion_id).content == Toda55UniversalDoubleStatement()


def test_unowned_mismatched_or_modified_source_is_not_rendered() -> None:
    bridge = build_cited_extension_sources()
    assertion_id = "toda:174:r3r6:universal:(5.5)"
    assertion = bridge.registry.assertion(assertion_id)
    expected = assertion.content
    projector = project_cited_universal_toda_reference_body
    assert projector(replace(assertion), bridge.registry, expected) is None
    assert projector(replace(assertion, reference_id="toda:(4.8)"), bridge.registry, expected) is None
    assert projector(replace(assertion, scope=("other",)), bridge.registry, expected) is None
    assert projector(replace(assertion, origin=AssertionOrigin.PROOF_INTERNAL), bridge.registry, expected) is None
    assert projector(assertion, bridge.registry, replace(expected, coefficient=3)) is None
    assert projector(assertion, bridge.registry, Toda48UniversalConditionalStatement()) is None
    fake = UnifiedStatementRegistry()
    fake.add_reference(LiteratureEntry(
        reference_id="toda:(5.5)", kind=ReferenceKind.EQUATION,
        locator="(5.5)", source_id="unverified", publication_position=8600,
    ))
    fake.add_assertion(assertion)
    assert project_reference_bodies(fake, (assertion_id,)) == ()


def test_unrelated_reference_is_unchanged_and_no_group_given_added() -> None:
    bridge = build_cited_extension_sources()
    ids = ("toda:174:r3r6:universal:(4.8)", "toda:174:r3r6:universal:(5.5)")
    body = project_reference_bodies(bridge.registry, ids)
    assert len(body) == 2
    assert project_reference_bodies(bridge.registry, ()) == ()
    assert project_reference_bodies(None, ids) == ()
    assert len(bridge.proof_links) == 2
    from proof import ProofRule, Relation
    assert all(link.step is not None and link.step.rule is ProofRule.GIVEN
               and not isinstance(link.step.conclusion, Relation)
               for link in bridge.proof_links)


def test_public_pi85_uses_registered_reference_without_duplicate_conclusion() -> None:
    from phase174_r3_r6_r2_prop44_lemma54.audit import inspect

    result = inspect()
    assert result["root_status"] == "complete"
    assert result["root_proven_steps"] == 16
    assert result["new_group_given"] == 0
    narrative = result["narrative"]
    assert "[R4] (4.8)." in narrative
    assert "[R7] (5.5)." in narrative
    assert r"$\Delta(\iota_{2n-1})=0$ と仮定する" in narrative
    assert r"$n\ge5$ に対し, $2\nu_n=E^{n-3}\nu'$." in narrative
    assert r"E^{2}:\pi_{6}^{3}\hookrightarrow \pi_{8}^{5}" in narrative
    assert r"|\pi_{8}^{5}|=2\cdot 4=8" in narrative
    root_lines = tuple(
        line for line in narrative.splitlines()
        if r"\pi_{8}^{5}" in line and r"\mathbb{Z}/8" in line and "=" in line
    )
    assert len(root_lines) == 1, root_lines
```

## 新規テスト tests/test_r3r4_patch.py — 全文

```python
"""Focused insertion behavior without running or changing a real Git tree."""
from __future__ import annotations

import pytest

from phase174_r3_r6_r4_common_reference.patch import (
    candidate_source,
    _normalized,
)


MOCK = '''def project_reference_bodies(registry, assertion_ids):
    from proof import Relation

    result = []
    for statement in assertion_ids:
        if sentence is None:
            sentence = typed_sentence(statement, None)
    return result
'''


def test_two_unique_inserts_only_and_no_function_api_change() -> None:
    original = MOCK.replace("        if sentence is None:", "            if sentence is None:").replace(
        "            sentence = typed_sentence", "                sentence = typed_sentence",
    )
    patched = candidate_source(original)
    assert "project_cited_universal_toda_reference_body(" in patched
    assert patched.count("project_cited_universal_toda_reference_body") == 2
    assert patched.startswith("def project_reference_bodies(")
    assert "return result" in patched


def test_crlf_and_unrelated_text_preserved() -> None:
    original = MOCK.replace("        if sentence is None:", "            if sentence is None:").replace(
        "            sentence = typed_sentence", "                sentence = typed_sentence",
    )
    windows = "# unrelated\r\n" + original.replace("\n", "\r\n")
    patched = candidate_source(windows)
    assert patched.startswith("# unrelated\r\n")
    assert _normalized(patched).count("project_cited_universal_toda_reference_body") == 2
    assert "\r\n" in patched


def test_missing_or_duplicate_import_anchor_rejected() -> None:
    original = MOCK.replace("        if sentence is None:", "            if sentence is None:").replace(
        "            sentence = typed_sentence", "                sentence = typed_sentence",
    )
    with pytest.raises(ValueError, match="anchor"):
        candidate_source(original.replace("from proof import Relation", "from proof import ProofStep"))
    with pytest.raises(ValueError, match="anchor"):
        candidate_source(original.replace("    from proof import Relation\n\n    result = []\n",
                                          "    from proof import Relation\n\n    result = []\n    from proof import Relation\n\n    result = []\n"))
```

## run.ps1 — 全文

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location -LiteralPath $Repo

& git fetch origin develop
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R4 failed to fetch GitHub develop.' }

$Tests = @(
    'phase174_r3_r6_r4_common_reference/tests/test_r3r4_patch.py',
    'phase174_r3_r6_r4_common_reference/tests/test_r3r4_reference_bodies.py',
    'phase174_r3_r6_r3r2_pytest_importmode_fix/tests/test_r3r2_importmode.py',
    'phase174_r3_r6_r3r1_scoped_guard_fix/tests/test_patch.py',
    'phase174_r3_r6_r3_common_narrative/tests/test_projection.py',
    'phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py',
    'phase174_r3_r6_source_extension/tests/test_source.py',
    'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py',
    'phase172_r5_prior_reference_display/tests/test_projection.py'
)

if ($DryRun) {
    & python -m phase174_r3_r6_r4_common_reference.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R4 source guard failed.' }
    Write-Output 'PHASE174_R3R6R4_COLLECTION_START'
    & python -m pytest --import-mode=importlib --collect-only -q @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R4 focused test collection failed.' }
    Write-Output 'PHASE174_R3R6R4_COLLECTION=PASS'
    Write-Output 'PHASE174_R3R6R4_DRYRUN_GATE=PASS'
} else {
    & python -m phase174_r3_r6_r4_common_reference.patch
    if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R4 patch application failed.' }
    Write-Output 'PHASE174_R3R6R4_FOCUSED_PYTEST_START'
    & python -m pytest --import-mode=importlib -q @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R4 focused pytest failed.' }
    Write-Output 'PHASE174_R3R6R4_FOCUSED_PYTEST=PASS'
    & python -m phase174_r3_r6_r4_common_reference.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R4 public Reference audit failed.' }
    Write-Output 'PHASE174_R3R6R4_GATE=PASS'
}
Write-Output '(END)'
```


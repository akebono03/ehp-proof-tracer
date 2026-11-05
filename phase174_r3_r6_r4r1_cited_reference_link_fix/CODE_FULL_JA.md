# Phase 174 R3-R6-R4R1 コード全文

対象: `phase168_r3_37c_reference_projection.py` の既存 `project_cited_proof_step_reference_bodies()` を全文置換し、`phase174_r3_r6_r4_common_reference/projection.py` で既存 `project_cited_universal_toda_reference_body()` を全文置換、新規 `_universal_toda_formula()` を既存関数の直前に、新規 `project_verified_cited_toda_given_reference_body()` を既存関数の後に追加する。既存 import は変更しない。

既存モジュールの全文・新規モジュール・テスト関数の全文は以下に省略せず掲載する。

## 変更後の Reference 投影モジュール全文: `output/phase168_r3_37c_reference_projection.py.FULL.py`

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
    """Render an actual cited GIVEN when an assertion-ID body was not attached.

    Preserve the established Lemma 5.4 fallback. For Toda (4.8) and (5.5),
    require a unique canonical cited GIVEN with explicit source provenance,
    plus reverified adopted source text and chronological position. This is
    display-only: neither source links nor ProofSteps are created here.
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
    if verified:
        return verified if len(verified) == 1 else ()

    from phase174_r3_r6_r4_common_reference.projection import (
        project_verified_cited_toda_given_reference_body,
    )
    return project_verified_cited_toda_given_reference_body(reference, cited_steps)

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

## 変更後の source-backed 投影モジュール全文: `output/phase174_r3_r6_r4_common_reference__projection.py.FULL.py`

```python
"""Read-only Reference prose for previously registered, source-checked Toda laws.

The registered source assertion, not a nearby string, inferred group goal, or
bibliography heading, authorizes each formula. No inference or new GIVEN is
constructed here. A verified cited GIVEN can also supply the same formula when
an older Narrative Model lacks the registry assertion-ID binding.
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


def _universal_toda_formula(statement: object) -> str | None:
    """Format the canonical typed source clause, without making it a proof."""
    if (type(statement) is Toda48UniversalConditionalStatement
            and statement == Toda48UniversalConditionalStatement()):
        return (
            r"$n$ を偶数とし, $\Delta(\iota_{2n-1})=0$ と仮定する."
            "\n"
            r"このとき $E^2:\pi_{2n-2}^{n-1}\hookrightarrow\pi_{2n}^{n+1}$ は単射で, "
            r"$\pi_{2n}^{n+1}/E^2(\pi_{2n-2}^{n-1})\cong\mathbb{Z}/2$."
        )
    if (type(statement) is Toda55UniversalDoubleStatement
            and statement == Toda55UniversalDoubleStatement()):
        return r"$n\ge5$ に対し, $2\nu_n=E^{n-3}\nu'$."
    return None


def project_cited_universal_toda_reference_body(
    assertion: object, registry: object, statement: object,
) -> str | None:
    """Display one authenticated general GIVEN, retaining its source conditions.

    A matching locator or a forged dataclass alone is never sufficient. The
    caller supplies the actual, already cited registry assertion. Source text
    checking and publication screening happen upstream, not in Renderer.
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
    elif type(statement) is Toda55UniversalDoubleStatement:
        locator = "(5.5)"
        source_chapter = "05"
        publication_position = 8600
        canonical = Toda55UniversalDoubleStatement()
    else:
        return None

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
    return _universal_toda_formula(statement)


def project_verified_cited_toda_given_reference_body(
    reference: object, cited_steps: tuple[object, ...],
) -> tuple[str, ...]:
    """Recover a *display body* only from a cited and source-verified GIVEN leaf.

    This does not reconstruct registry links or promote a goal to a GIVEN.
    The cited step must have the exact canonical universal type, an explicit
    authentic source reference, and no premises. Source bytes and publication
    order are reverified; title matching alone never qualifies.
    """
    from proof import LiteratureReference, ProofRule, ProofStep
    from phase174_r3_r6_source_extension.source import verify_extension_texts

    if not isinstance(reference, LiteratureReference) or not isinstance(cited_steps, tuple):
        return ()
    locator = reference.locator or reference.label
    if locator == "(4.8)":
        canonical = Toda48UniversalConditionalStatement()
        expected_position = 7500
    elif locator == "(5.5)":
        canonical = Toda55UniversalDoubleStatement()
        expected_position = 8600
    else:
        return ()

    candidates: list[ProofStep] = []
    for step in cited_steps:
        if not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN:
            continue
        source_rule = step.inference_rule
        source_reference = getattr(source_rule, "literature_reference", None)
        source_locator = getattr(source_reference, "locator", None)
        source_name = getattr(source_rule, "name", None)
        if (
            step.premises
            or type(step.conclusion) is not type(canonical)
            or step.conclusion != canonical
            or source_locator != locator
            or source_name not in (
                "Cited universal Toda " + locator,
                "Registered fixed statement: " + locator,
            )
        ):
            continue
        candidates.append(step)
    if len(candidates) != 1:
        return ()

    # The adopted Toda TeX text and manifest order must still match the
    # previously checked source hashes. Do not trust an isolated citation title.
    try:
        positions = dict(verify_extension_texts())
    except (ValueError, OSError, UnicodeError):
        return ()
    if positions.get(locator) != expected_position:
        return ()
    sentence = _universal_toda_formula(candidates[0].conclusion)
    return (sentence,) if sentence is not None else ()
```

## 既存 Reference 関数の置換全文: `output/project_cited_proof_step_reference_bodies_FULL.py`

```python
def project_cited_proof_step_reference_bodies(
    reference: object, cited_steps: tuple[object, ...],
) -> tuple[str, ...]:
    """Render an actual cited GIVEN when an assertion-ID body was not attached.

    Preserve the established Lemma 5.4 fallback. For Toda (4.8) and (5.5),
    require a unique canonical cited GIVEN with explicit source provenance,
    plus reverified adopted source text and chronological position. This is
    display-only: neither source links nor ProofSteps are created here.
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
    if verified:
        return verified if len(verified) == 1 else ()

    from phase174_r3_r6_r4_common_reference.projection import (
        project_verified_cited_toda_given_reference_body,
    )
    return project_verified_cited_toda_given_reference_body(reference, cited_steps)
```

## 安全な適用処理: `patch.py`

```python
"""Safe installation of a source-cited Reference-body fallback (Phase 174 R3-R6-R4R1).

Two existing full modules are replaced ONLY after comparing their normalized
contents to pinned approved originals, then preserving their newline styles.
Neither backward-search logic nor any registered GIVEN is modified.
"""
from __future__ import annotations

import argparse
from hashlib import sha1, sha256
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path("phase174_r3_r6_r4r1_cited_reference_link_fix")
PUBLIC_REF = Path("phase168_r3_37c_reference_projection.py")
SOURCE_REF = Path("phase174_r3_r6_r4_common_reference/projection.py")
REVIEWED_HEAD = "f2e148afefb11eb0b0ca31da67c65ec1ffe9e1e9"
REVIEWED_REMOTE_BLOB = "754e63cf4beee3c882c601dbe4b97cb8ecbdc4d2"
REVIEWED_R4_SHA256 = "f8268429ba7c0751d20feea533fd5bad5d6a94912ec776f788be3c3e006b81ec"
REVIEWED_SOURCE_SHA256 = "fd848af37cd0debd8bc0f8b26d59c4415670f043bfa416d40d2df8218e10a188"
REVIEWED_OUTPUT_SHA256 = {
    PUBLIC_REF.as_posix(): "a58da77164fbc344b5a5c8fafb4a22081122d003abc62f905b5652e32fb29b9a",
    SOURCE_REF.as_posix(): "bde402ac49186f63645a559558c9e1bbaa465447d65c999e25d3ac29a749aba9",
}


def _git(*args: str) -> bytes:
    result = subprocess.run(("git",) + args, cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        raise ValueError("Git preflight rejected " + str(args) + ": "
                         + result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def _git_blob(raw: bytes) -> str:
    return sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()


def _normalized(raw: bytes) -> bytes:
    data = raw[3:] if raw.startswith(b"\xef\xbb\xbf") else raw
    return data.replace(b"\r\n", b"\n")


def _normalized_sha256(raw: bytes) -> str:
    return sha256(_normalized(raw)).hexdigest()


def _reapply_eol(source: bytes, new_lf_bytes: bytes) -> bytes:
    """Preserve a reviewed file's BOM and uniform line-ending convention."""
    bom = b"\xef\xbb\xbf" if source.startswith(b"\xef\xbb\xbf") else b""
    data = source[len(bom):]
    without_crlf = data.replace(b"\r\n", b"")
    if b"\n" in without_crlf or b"\r" in without_crlf:
        if b"\r\n" in data:
            raise ValueError("Mixed or unsupported EOL; refuse to rewrite")
        if b"\r" in without_crlf:
            raise ValueError("CR-only EOL is unsupported")
        return bom + new_lf_bytes
    if b"\r\n" in data:
        return bom + new_lf_bytes.replace(b"\n", b"\r\n")
    return bom + new_lf_bytes


def _reviewed_source(path: Path, expected_sha: str, generated: Path) -> bytes:
    original = (ROOT / path).read_bytes()
    current_sha = _normalized_sha256(original)
    new_lf = (ROOT / PACKAGE / generated).read_bytes()
    expected_output_sha = sha256(new_lf).hexdigest()
    if expected_output_sha != REVIEWED_OUTPUT_SHA256[path.as_posix()]:
        raise ValueError("Unreviewed generated replacement: " + path.as_posix())
    if current_sha == expected_output_sha:
        return original
    if current_sha != expected_sha:
        raise ValueError("Unreviewed local changes: " + path.as_posix()
                         + "; expected " + expected_sha + " found " + current_sha)
    return _reapply_eol(original, new_lf)


def reviewed_changes() -> tuple[tuple[Path, bytes, bool], ...]:
    """Check GitHub HEAD and both exact reviewed source modules before writing."""
    branch = _git("branch", "--show-current").decode("ascii").strip()
    local_head = _git("rev-parse", "HEAD").decode("ascii").strip()
    remote_head = _git("rev-parse", "origin/develop").decode("ascii").strip()
    print("PHASE174_R3R6R4R1_BRANCH=" + branch)
    print("PHASE174_R3R6R4R1_LOCAL_HEAD=" + local_head)
    print("PHASE174_R3R6R4R1_REMOTE_HEAD=" + remote_head)
    if branch != "develop" or local_head != REVIEWED_HEAD or remote_head != REVIEWED_HEAD:
        raise ValueError("Unreviewed HEAD or branch; no changes applied")
    for path in (PUBLIC_REF, SOURCE_REF):
        if _git("diff", "--cached", "--name-only", "--", path.as_posix()).strip():
            raise ValueError("Staged target changes require review: " + path.as_posix())
    if _git_blob(_git("show", f"{REVIEWED_HEAD}:{PUBLIC_REF.as_posix()}")) != REVIEWED_REMOTE_BLOB:
        raise ValueError("Public Reference baseline differs from reviewed GitHub")

    files = (
        (PUBLIC_REF, REVIEWED_R4_SHA256,
         Path("output/phase168_r3_37c_reference_projection.py.FULL.py")),
        (SOURCE_REF, REVIEWED_SOURCE_SHA256,
         Path("output/phase174_r3_r6_r4_common_reference__projection.py.FULL.py")),
    )
    reviewed = []
    for path, baseline_sha, generated in files:
        original = (ROOT / path).read_bytes()
        candidate = _reviewed_source(path, baseline_sha, generated)
        installed = candidate == original
        print("PHASE174_R3R6R4R1_TARGET_" + path.name.replace(".", "_")
              + "_ALREADY_INSTALLED=" + str(installed))
        reviewed.append((path, candidate, installed))
    return tuple(reviewed)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    changes = reviewed_changes()
    print("PHASE174_R3R6R4R1_SOURCE_GUARD=PASS")
    print("PHASE174_R3R6R4R1_PRODUCTION_TARGETS=2")
    print("PHASE174_R3R6R4R1_NEW_GIVEN=0")
    if args.dry_run:
        print("PHASE174_R3R6R4R1_DRY_RUN=PASS")
        return 0
    # All preflights have succeeded. No other files are touched.
    for path, new_content, installed in changes:
        if not installed:
            (ROOT / path).write_bytes(new_content)
    print("PHASE174_R3R6R4R1_APPLIED=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 実行スクリプト: `run.ps1`

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location -LiteralPath $Repo

& git fetch origin develop
if ($LASTEXITCODE -ne 0) { throw 'R4R1 failed to fetch GitHub develop.' }

$Tests = @(
    'phase174_r3_r6_r4r1_cited_reference_link_fix/tests/test_r4r1_guard.py',
    'phase174_r3_r6_r4r1_cited_reference_link_fix/tests/test_r4r1_live_binding.py',
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
    & python -m phase174_r3_r6_r4r1_cited_reference_link_fix.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R4R1 source guard failed.' }
    Write-Output 'PHASE174_R3R6R4R1_COLLECTION_START'
    & python -m pytest --import-mode=importlib -p no:cacheprovider --collect-only -q @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R1 focused collection failed.' }
    Write-Output 'PHASE174_R3R6R4R1_COLLECTION=PASS'
    Write-Output 'PHASE174_R3R6R4R1_DRYRUN_GATE=PASS'
} else {
    & python -m phase174_r3_r6_r4r1_cited_reference_link_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R4R1 guarded application failed.' }
    Write-Output 'PHASE174_R3R6R4R1_FOCUSED_PYTEST_START'
    & python -m pytest --import-mode=importlib -p no:cacheprovider -q @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R1 focused pytest failed; gate not certified.' }
    Write-Output 'PHASE174_R3R6R4R1_FOCUSED_PYTEST=PASS'
    & python -m phase174_r3_r6_r4_common_reference.audit
    if ($LASTEXITCODE -ne 0) { throw 'R4R1 public Reference audit failed.' }
    Write-Output 'PHASE174_R3R6R4R1_AUDIT=PASS'
    Write-Output 'PHASE174_R3R6R4R1_GATE=PASS'
}
Write-Output '(END)'
```

## 安全ガード試験: `tests/test_r4r1_guard.py`

```python
"""Read-only contract checks for the two scoped Reference display edits."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r6_r4r1_cited_reference_link_fix.patch import (
    PACKAGE,
    ROOT,
    _normalized_sha256,
    _reapply_eol,
    REVIEWED_R4_SHA256,
    REVIEWED_SOURCE_SHA256,
)


def test_both_originals_match_the_reviewed_local_artifacts() -> None:
    original_ref = (ROOT / "phase174_r3_r6_r4_common_reference" / "output"
                    / "phase168_r3_37c_reference_projection.py.FULL.py")
    original_source = (ROOT / PACKAGE / "output"
                       / "phase174_r3_r6_r4_common_reference__projection.py.BASELINE.py")
    assert _normalized_sha256(original_ref.read_bytes()) == REVIEWED_R4_SHA256
    assert _normalized_sha256(original_source.read_bytes()) == REVIEWED_SOURCE_SHA256


def test_only_one_existing_reference_function_is_replaced() -> None:
    old = (ROOT / "phase174_r3_r6_r4_common_reference" / "output"
           / "phase168_r3_37c_reference_projection.py.FULL.py").read_text(encoding="utf-8")
    new = (ROOT / PACKAGE / "output"
           / "phase168_r3_37c_reference_projection.py.FULL.py").read_text(encoding="utf-8")
    def functions(text: str) -> dict[str, str]:
        tree = ast.parse(text)
        lines = text.splitlines(keepends=True)
        return {
            node.name: "".join(lines[node.lineno - 1:node.end_lineno])
            for node in tree.body if isinstance(node, ast.FunctionDef)
        }
    before, after = functions(old), functions(new)
    assert before.keys() == after.keys()
    assert set(name for name in before if before[name] != after[name]) == {
        "project_cited_proof_step_reference_bodies",
    }
    assert "project_verified_cited_toda_given_reference_body" in after[
        "project_cited_proof_step_reference_bodies"
    ]
    assert before["project_reference_bodies"] == after["project_reference_bodies"]


def test_source_formula_is_shared_between_two_reviewed_reference_paths() -> None:
    old = (ROOT / PACKAGE / "output"
           / "phase174_r3_r6_r4_common_reference__projection.py.BASELINE.py").read_text()
    new = (ROOT / PACKAGE / "output"
           / "phase174_r3_r6_r4_common_reference__projection.py.FULL.py").read_text()
    assert old.count(r"$\Delta(\iota_{2n-1})=0$") == 1
    assert new.count(r"$\Delta(\iota_{2n-1})=0$") == 1
    assert new.count(r"$n\ge5$ に対し, $2\nu_n=E^{n-3}\nu'$.") == 1
    assert "verify_extension_texts()" in new
    assert "step.rule is not ProofRule.GIVEN" in new
    assert "source_locator != locator" in new
    ast.parse(new)


def test_preserve_bom_and_crlf_and_reject_mixed_newlines() -> None:
    changed = _reapply_eol(b"\xef\xbb\xbfbefore\r\nafter\r\n", b"before\nchanged\n")
    assert changed == b"\xef\xbb\xbfbefore\r\nchanged\r\n"
    assert _reapply_eol(b"before\nafter\n", b"before\nchanged\n") == b"before\nchanged\n"
    with pytest.raises(ValueError, match="Mixed"):
        _reapply_eol(b"before\r\nafter\n", b"before\nchanged\n")
```

## Reference 投影と公開証明の回帰試験: `tests/test_r4r1_live_binding.py`

```python
"""Source-screened source-body and public Narrative regression checks."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase168_r3_37c_reference_projection import (
    project_cited_proof_step_reference_bodies,
    project_reference_bodies,
)
from phase174_r3_r6_source_extension.source import build_cited_extension_sources
from proof import InferenceRule, LiteratureReference, ProofRule


def test_cited_given_fallback_matches_registered_reference_body_for_both_sources() -> None:
    bridge = build_cited_extension_sources()
    for locator in ("(4.8)", "(5.5)"):
        assertion_id = "toda:174:r3r6:universal:" + locator
        links = tuple(link for link in bridge.proof_links if link.assertion_id == assertion_id)
        assert len(links) == 1 and links[0].step is not None
        reference = LiteratureReference(label="Toda " + locator, locator=locator)
        expected = project_reference_bodies(bridge.registry, (assertion_id,))
        actual = project_cited_proof_step_reference_bodies(reference, (links[0].step,))
        assert actual == expected
        assert len(actual) == 1


def test_cited_given_fallback_rejects_unproved_or_wrongly_cited_statement() -> None:
    bridge = build_cited_extension_sources()
    source = next(link.step for link in bridge.proof_links
                  if link.step is not None and link.assertion_id.endswith("(4.8)"))
    reference = LiteratureReference(label="Toda (4.8)", locator="(4.8)")
    assert project_cited_proof_step_reference_bodies(reference, ()) == ()
    assert project_cited_proof_step_reference_bodies(
        LiteratureReference(label="Toda (5.5)", locator="(5.5)"), (source,),
    ) == ()
    assert project_cited_proof_step_reference_bodies(
        reference, (replace(source, rule=ProofRule.INFERENCE),),
    ) == ()
    assert project_cited_proof_step_reference_bodies(
        reference, (replace(source, inference_rule=None),),
    ) == ()
    assert project_cited_proof_step_reference_bodies(reference, (source, source)) == ()
    assert project_cited_proof_step_reference_bodies(
        reference, (replace(source, inference_rule=InferenceRule(
            name="unrelated", literature_reference=reference,
        )),),
    ) == ()


def test_source_guard_failure_does_not_show_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    import phase174_r3_r6_source_extension.source as source_module
    bridge = build_cited_extension_sources()
    step = next(link.step for link in bridge.proof_links
                if link.step is not None and link.assertion_id.endswith("(5.5)"))
    reference = LiteratureReference(label="Toda (5.5)", locator="(5.5)")

    def unverified() -> None:
        raise ValueError("unverified adopted source")

    monkeypatch.setattr(source_module, "verify_extension_texts", unverified)
    assert project_cited_proof_step_reference_bodies(reference, (step,)) == ()


def test_public_pi85_reference_bodies_and_complete_root_unchanged() -> None:
    from phase174_r3_r6_r2_prop44_lemma54.audit import inspect

    result = inspect()
    narrative = result["narrative"]
    assert result["root_status"] == "complete"
    assert result["root_proven_steps"] == 16
    assert result["new_group_given"] == 0
    assert narrative.count("[R4] (4.8).") == 1
    assert narrative.count("[R7] (5.5).") == 1
    assert r"$\Delta(\iota_{2n-1})=0$ と仮定する" in narrative
    assert r"$n\ge5$ に対し, $2\nu_n=E^{n-3}\nu'$." in narrative
    assert r"E^{2}:\pi_{6}^{3}\hookrightarrow \pi_{8}^{5}" in narrative
    assert r"|\pi_{8}^{5}|=2\cdot 4=8" in narrative
    conclusion_lines = [line for line in narrative.splitlines()
                        if r"\pi_{8}^{5}" in line and r"\mathbb{Z}/8" in line and "=" in line]
    assert len(conclusion_lines) == 1
```

## package init: `__init__.py`

```python
"""Phase 174 R3-R6-R4R1: cited source Reference-body binding recovery."""
```

## tests init: `tests/__init__.py`

```python
"""Focused R4R1 regression tests."""
```

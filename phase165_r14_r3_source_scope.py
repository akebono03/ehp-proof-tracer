"""Toda (5.1) extended citation scope; source-claim catalog, not proof facts.

Keep the archived equation checksum and 117-item source manifest unchanged.
The adjacent display was explicitly supplied by the user and has not been
independently verified against the complete source file or original edition.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib

from phase165_r14_r2_toda51 import TODA_51_SCHEMAS, instantiate_toda51_clause

REFERENCE_LOCATOR = "(5.1)"
ARCHIVE_ID = "phase163:archive:toda:tex:ch5:0001"
ADJACENT_TEX = (
    r"\["
    "\n"
    r"\pi^{n}_{n}=\gen{\iota_n}\cong \mathbb Z,\qquad"
    "\n"
    r"G_0=\gen{\iota}\cong \mathbb Z. \quad "
    "\n"
    r"\iota=E^{\infty}\iota_n."
    "\n"
    r"\]"
)


@dataclass(frozen=True)
class SourceClause:
    key: str
    source_part: str
    tex: str
    typed_schema: str | None
    semantics_certified: bool = False
    proof_eligible: bool = False


CLAUSES = (
    SourceClause("pi_i_1_zero", "numbered_equation",
                 r"\pi^{1}_{i}=0\ (i>1)", "sphere_one_zero"),
    SourceClause("pi_i_n_zero", "numbered_equation",
                 r"\pi^{n}_{i}=0\ (i<n)", None),
    SourceClause("negative_stem_zero", "numbered_equation",
                 r"G_k=(G_k;2)=0\ (k<0)", None),
    SourceClause("pi_n_n_cyclic", "adjacent_display",
                 r"\pi^{n}_{n}=\gen{\iota_n}\cong \mathbb Z",
                 "diagonal_infinite_cyclic"),
    SourceClause("stable_zero_stem_cyclic", "adjacent_display",
                 r"G_0=\gen{\iota}\cong \mathbb Z", None),
    SourceClause("stable_identity", "adjacent_display",
                 r"\iota=E^{\infty}\iota_n", None),
)


def collect_toda51_scope(bridge, adjacent_tex: str = ADJACENT_TEX) -> dict:
    """Build an audit-only composite citation, refusing altered text or origin."""
    if adjacent_tex != ADJACENT_TEX:
        raise ValueError("adjacent source span differs from supplied TeX")
    archive = bridge.registry.assertion(ARCHIVE_ID)
    reference = bridge.registry.reference(archive.reference_id)
    body = archive.content
    numbered_tex = body["source_text"]
    if (reference.locator != REFERENCE_LOCATOR
            or body.get("proof_eligible") is not False
            or hashlib.sha256(numbered_tex.encode("utf-8")).hexdigest()
               != body["source_sha256"]):
        raise ValueError("archived (5.1) identity or checksum invalid")
    for clause in CLAUSES:
        source = numbered_tex if clause.source_part == "numbered_equation" else adjacent_tex
        if clause.tex not in source:
            raise ValueError("source clause absent: " + clause.key)
    schemas = {item.name for item in TODA_51_SCHEMAS}
    if {item.typed_schema for item in CLAUSES if item.typed_schema} != schemas:
        raise ValueError("existing R14-R2 typed schema mismatch")
    return {
        "phase": "165 R14-R3",
        "reference_id": archive.reference_id,
        "source_statement_id": body["source_statement_id"],
        "archive_source_sha256": body["source_sha256"],
        "numbered_source": numbered_tex,
        "adjacent_source": adjacent_tex,
        "adjacent_source_status": "USER_SUPPLIED_NOT_ARCHIVE_VERIFIED",
        "reference_scope": "NUMBERED_EQUATION_PLUS_ADJACENT_DISPLAY",
        "source_clause_count": len(CLAUSES),
        "typed_schema_count": len(schemas),
        "clauses": [vars(item) for item in CLAUSES],
        "typed_examples": [
            repr(instantiate_toda51_clause(TODA_51_SCHEMAS[0], 2)),
            repr(instantiate_toda51_clause(TODA_51_SCHEMAS[1], 3)),
        ],
        "registry_modified": False,
        "new_proof_eligible": 0,
        "proof_steps_created": 0,
        "status": "SOURCE_SCOPE_RECORDED_PROVENANCE_NOT_CERTIFIED",
        "full_pytest_run": False,
    }

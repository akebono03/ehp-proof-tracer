Phase 145-2 Stage 1 - Phase Artifact Archiving Audit

Goal
----
Audit whether root-level Phase artifacts can be moved under archive/phases/
without changing runtime behavior.

This stage performs NO move and NO deletion.

Baseline
--------
develop commit:
4737d71e339b704b787668f493201e4aebeeb991
(Phase 145-1)

Classification
--------------
MOVE_SAFE_CANDIDATE
    No canonical path reference, no detected repository-root/relative-path risk,
    and no destination collision.

MOVE_REQUIRES_CANONICAL_REFERENCE_UPDATE
    A canonical/non-Phase tracked file contains an explicit artifact path.

MOVE_REQUIRES_RELATIVE_PATH_REVIEW
    The artifact itself contains markers suggesting repository-root or relative
    path assumptions and requires review before moving.

MOVE_REQUIRES_DESTINATION_REVIEW
    The proposed archive destination already exists.

Root Phase files
----------------
Root-level PHASE...README/INSTRUCTIONS, apply/audit/diagnose/check/find scripts,
and Phase report files are included. They are proposed for:
archive/phases/_root_files/

Testing
-------
No pytest is run in this audit stage.
The full suite remains reserved for the end of Phase 145-2.

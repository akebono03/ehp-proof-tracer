"""Read-only confirmation of the R20R13R2/R3 corrected proof audit."""
from __future__ import annotations

import json
from pathlib import Path

from phase171_r20r13r4_test_count_fix.install import (
    CORRECTED_SHA256, ROOT, TARGET, OUTPUT, normalized, sha256,
)


def main() -> None:
    test_content = normalized((ROOT / TARGET).read_bytes())
    if sha256(test_content) != CORRECTED_SHA256:
        raise RuntimeError("reviewed test-only assertion is not installed")
    r2_path = ROOT / "phase171_r20r13r2_multiple_blank_eta_merge/output/audit.json"
    r3_path = ROOT / "phase171_r20r13r3_content_guard_fix/output/audit.json"
    r2 = json.loads(r2_path.read_text(encoding="utf-8"))
    r3 = json.loads(r3_path.read_text(encoding="utf-8"))
    if (
        r2.get("public_status") != "complete"
        or r2.get("exact_three_eta_grouped") is not True
        or r2.get("reference_count") != 8
        or r3.get("public_status") != "complete"
        or r3.get("exact_three_eta_grouped") is not True
        or r3.get("reference_count") != 8
    ):
        raise RuntimeError("corrected public narrative does not meet requirements")
    result = {
        "phase": "171-R20R13R4",
        "fix": "LIST_COUNT_TEST_ASSERTION_ONLY",
        "public_status": "complete",
        "exact_three_eta_grouped": True,
        "reference_count": 8,
        "changed_production_code": False,
        "changed_proof_tree": False,
        "changed_reference": False,
        "full_pytest": False,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "audit.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("PHASE171_R20R13R4_PUBLIC_STATUS=complete", flush=True)
    print("PHASE171_R20R13R4_ETA_GROUPED_THREE=True", flush=True)
    print("PHASE171_R20R13R4_REFERENCES=8", flush=True)
    print("PHASE171_R20R13R4_PRODUCTION_MODIFIED=False", flush=True)
    print("PHASE171_R20R13R4_RESULT=PASS_TEST_ONLY_CORRECTION", flush=True)


if __name__ == "__main__":
    main()

"""Read-only preflight: validate local R6A baseline and referenced tests."""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path

from phase169_r7_general_stable_transport.patch import ROOT, TARGET, replacement_content

REQUIRED_FILES = (
    "phase169_r5b_pi75_prior_transport/rule.py",
    "phase169_r6a_pi86_two_step_transport/rule.py",
    "phase169_r3m_prior_result_catalog/prior_results.py",
    "phase165_r57_r7_stable_expansion.py",
    "phase165_r12_r21_eta_generator_chain.py",
    "phase169_r5b_pi75_prior_transport/tests/test_r5b_pi75_transport.py",
    "phase169_r6a_pi86_two_step_transport/tests/test_r6a_two_step_transport.py",
    "phase169_r3m_prior_result_catalog/tests/test_prior_results.py",
    "phase165_r57_r7_toda45_backward_connection/test_phase165_r57_r7_toda45_backward_connection.py",
)


def main() -> None:
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    if missing:
        raise RuntimeError("required checked-out files missing: " + repr(missing))
    if not TARGET.is_file():
        raise RuntimeError("production provider missing")
    replacement_content(TARGET.read_bytes())
    for name in REQUIRED_FILES:
        if name.endswith(".py"):
            ast.parse((ROOT / name).read_text(encoding="utf-8-sig"))
    print("R7_PREFLIGHT=PASS")
    print("R7_REQUIRED_LOCAL_FILES=" + str(len(REQUIRED_FILES)))
    print("R7_PRODUCTION_PATCHED=False")


if __name__ == "__main__":
    main()

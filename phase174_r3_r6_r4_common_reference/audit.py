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

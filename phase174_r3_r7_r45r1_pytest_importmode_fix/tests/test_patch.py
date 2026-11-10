"""The R45R1 patch must not alter mathematical rules or unrelated files."""
from __future__ import annotations

from pathlib import Path

from phase174_r3_r7_r45r1_pytest_importmode_fix.patch import (
    ROOT, TARGETS, normalized_sha256, pending_replacements, target_fragments,
)


def test_import_mode_repair_changes_only_two_reviewed_r45_files():
    assert TARGETS == (
        "phase174_r3_r7_r45_ehp_open_obligation_audit/run.ps1",
        "phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_static.py",
    )
    run_before, run_after = target_fragments(TARGETS[0])
    test_before, test_after = target_fragments(TARGETS[1])
    original = run_before.read_text(encoding="utf-8")
    revised = run_after.read_text(encoding="utf-8")
    assert "--import-mode=importlib" in original
    assert "$ImportMode = 'prepend'" not in original
    assert "$ImportMode = 'prepend'" in revised
    assert "'PROP42_SPECIALIZATION_REGRESSION', 'PROP42_CONSEQUENCE_REGRESSION'" in revised
    original_call = "        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path"
    revised_call = "\n".join((
        "        # The historical Prop42 test directories shadow same-named .py modules",
        "        # under pytest importlib mode; prepend resolves the real module.",
        "        $ImportMode = 'importlib'",
        "        if ($Group.Name -in @('PROP42_SPECIALIZATION_REGRESSION', 'PROP42_CONSEQUENCE_REGRESSION')) {",
        "            $ImportMode = 'prepend'",
        "        }",
        '        python -B -m pytest -q "--import-mode=$ImportMode" -p no:cacheprovider $Group.Path',
    ))
    assert revised.replace(revised_call, original_call) == original
    original_static = test_before.read_text(encoding="utf-8")
    revised_static = test_after.read_text(encoding="utf-8")
    start = revised_static.index("\n\ndef test_prop42_regressions_use_prepend_")
    end = revised_static.index("\n\ndef test_no_derived_theorem_is_installed_or_given", start)
    without_added_guard = revised_static[:start] + revised_static[end:]
    old_assertion = '    assert "--import-mode=importlib" in source'
    new_assertion = '    assert "$ImportMode = \'importlib\'" in source'
    assert without_added_guard.replace(new_assertion, old_assertion) == original_static


def test_repair_current_files_are_pinned_and_idempotent():
    changes = pending_replacements(ROOT)
    assert len(changes) == 2
    assert all(mode == "ALREADY_REPAIRED" for _, _, mode in changes)
    for dest, replacement, _ in changes:
        assert normalized_sha256(dest.read_bytes()) == normalized_sha256(replacement.read_bytes())


def test_repair_runner_has_dry_run_and_no_full_suite():
    script = (Path(__file__).resolve().parents[1] / "run.ps1").read_text(encoding="utf-8")
    assert "[switch]$DryRun" in script
    assert "patch --dry-run" in script
    assert "phase174_r3_r7_r45_ehp_open_obligation_audit\\run.ps1" in script
    assert "--import-mode=importlib" in script
    assert "git reset" not in script
    assert "git clean" not in script
    assert "FULL_PYTEST=False" in script

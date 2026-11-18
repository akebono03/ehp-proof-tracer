"""Pure diagnostic contract checks, without constructing mathematical evidence."""
from __future__ import annotations
from types import SimpleNamespace
from phase175_r4r12r10r1r7_public_visibility_diagnostic import audit


def test_count_named_exact_name() -> None:
    objects = (SimpleNamespace(rule=SimpleNamespace(name="citation")),
               SimpleNamespace(rule=SimpleNamespace(name="other")),
               SimpleNamespace(rule=SimpleNamespace(name="citation")))
    assert audit.count_named(objects, "citation") == 2
    assert audit.count_named(objects, "missing") == 0


def test_diagnostic_never_declares_group_complete() -> None:
    import inspect
    source = inspect.getsource(audit.investigate)
    assert '"group_complete": False' in source
    assert 'installer.install(' not in source


def test_report_gate_is_diagnostic_only() -> None:
    import inspect
    body = inspect.getsource(audit.main)
    assert "PASS_R7_PUBLIC_VISIBILITY_DIAGNOSED_NOT_COMPLETE" in body
    assert 'group proof complete' not in body


def test_no_git_mutations_in_diagnostic() -> None:
    import inspect
    body = inspect.getsource(audit.investigate)
    for command in ('"reset"', '"checkout"', '"commit"', '"add"'):
        assert command not in body

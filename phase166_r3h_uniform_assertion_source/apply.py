"""Safely replace one complete production function using an expected source anchor."""
from pathlib import Path
import ast
import shutil
from datetime import datetime, timezone

ROOT = Path.cwd()
PATH = ROOT / 'phase165_r52_r16_web_citation_gate.py'
if not PATH.is_file():
    raise SystemExit('Repository root not found')
source = PATH.read_text(encoding='utf-8')
tree = ast.parse(source)
funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'screen_shared_proof_context']
if len(funcs) != 1:
    raise SystemExit('Expected exactly one screen_shared_proof_context function')
func = funcs[0]
original = ''.join(source.splitlines(keepends=True)[func.lineno-1:func.end_lineno])
if ('explicit_publication_target' not in original or 'for link in bridge.proof_links:' not in original):
    raise SystemExit('Unexpected current source; no modification')
replacement = '''def screen_shared_proof_context(
    bridge: RegistryBridgeResult,
    *,
    goal: object,
    citing_assertion_id: str,
    verified_assertion_ids: tuple[str, ...] = (),
    explicit_publication_target: bool = False,
) -> RegistryBridgeResult:
    """Filter source statements by existing policies or explicit publication order.

    In explicit publication-order mode the registry is authoritative: a prior
    FIXED_STATEMENT needs no manually maintained ProofStepLink. The link is
    constructed uniformly from the registered typed assertion, independent of
    any pre-existing ProofStepLink. Legacy implicit-target mode is unchanged.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not isinstance(verified_assertion_ids, tuple):
        raise TypeError("verified_assertion_ids must be a tuple")
    bridge.registry.assertion(citing_assertion_id)
    accepted = []
    if explicit_publication_target:
        from dataclasses import is_dataclass
        from phase166_r3c_publication_order import precedes_citing_assertion
        from proof import ProofStep
        from unified_statement_registry import AssertionKind, ProofStepLink

        for assertion in bridge.registry._assertions.values():
            if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
                continue
            if assertion.kind is not AssertionKind.STATEMENT:
                continue
            if not is_dataclass(assertion.content) or isinstance(assertion.content, type):
                continue
            if type(assertion.content) is type(goal) and assertion.content == goal:
                continue
            if not precedes_citing_assertion(
                bridge, assertion.assertion_id, citing_assertion_id
            ):
                continue
            accepted.append(ProofStepLink(
                assertion_id=assertion.assertion_id,
                step=ProofStep(
                    conclusion=assertion.content,
                    premises=(),
                    rule=ProofRule.GIVEN,
                ),
            ))
        return RegistryBridgeResult(bridge.registry, bridge.records, tuple(accepted))

    for link in bridge.proof_links:
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if type(assertion.content) is type(goal) and assertion.content == goal:
            continue
        step = link.step
        if step is None or step.rule is not ProofRule.GIVEN:
            continue
        if type(step.conclusion) is not type(assertion.content) or step.conclusion != assertion.content:
            raise ValueError("fixed reference has inconsistent GIVEN proof link")
        adopted = (
            assertion.assertion_id.startswith("shared:")
            and (
                ":adopted:assertion:" in assertion.assertion_id
                or ":toda:adopted:prop5.1:finite_dimensional" in assertion.assertion_id
                or assertion.assertion_id.endswith(":adopted:assertion:prop42:general")
            )
        )
        if adopted:
            accepted.append(link)
            continue
        decision = assess_phase164_r2_citation(
            bridge, assertion.assertion_id, citing_assertion_id,
            verified_assertion_ids=verified_assertion_ids,
        )
        if decision.usable:
            accepted.append(link)
    return RegistryBridgeResult(bridge.registry, bridge.records, tuple(accepted))
'''
parts = source.splitlines(keepends=True)
updated = ''.join(parts[:func.lineno-1]) + replacement + ''.join(parts[func.end_lineno:])
ast.parse(updated)
backup_dir = ROOT / 'phase166_r3h_uniform_assertion_source_backup' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
backup_dir.mkdir(parents=True, exist_ok=False)
shutil.copy2(PATH, backup_dir / PATH.name)
PATH.write_text(updated, encoding='utf-8')
print('PATCHED:', PATH)
print('BACKUP:', backup_dir)
print('REPLACEMENT FUNCTION: phase165_r52_r16_web_citation_gate.py::screen_shared_proof_context')
print(replacement)

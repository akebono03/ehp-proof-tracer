from pathlib import Path
import ast
import shutil

root = Path(__file__).resolve().parent.parent
bundle = Path(__file__).resolve().parent
path = root / 'phase165_r52_r16_web_citation_gate.py'
old = path.read_text(encoding='utf-8')
anchor = '''            accepted.append(ProofStepLink(
                assertion_id=assertion.assertion_id,
                step=registered_reference_step(assertion, ProofStep(
'''
addition = '''            # A concrete fixed assertion is not an independent GIVEN if the
            # same cited source already contains an eligible typed schema
            # whose established specialization rule derives that assertion.
            # Keep the registry entry for provenance; only the direct leaf is
            # suppressed. This applies uniformly to printed source locators.
            from phase165_r57_r20_general_specialization import specialize_typed_statement
            reference = bridge.registry.reference(assertion.reference_id)
            covered_by_schema = any(
                alternative.assertion_id != assertion.assertion_id
                and alternative.origin is AssertionOrigin.FIXED_STATEMENT
                and alternative.kind in (AssertionKind.STATEMENT, AssertionKind.DEFINITION)
                and bridge.registry.reference(alternative.reference_id).locator == reference.locator
                and precedes_citing_assertion(
                    bridge, alternative.assertion_id, citing_assertion_id
                )
                and specialize_typed_statement(alternative.content, assertion.content) is not None
                for alternative in bridge.registry._assertions.values()
            )
            if covered_by_schema:
                continue
'''
if old.count(anchor) != 1:
    raise SystemExit(f'Expected exactly one insertion point, found {old.count(anchor)}')
if 'covered_by_schema = any(' in old:
    raise SystemExit('Patch already present; no changes applied')
new = old.replace(anchor, addition + anchor, 1)
ast.parse(new)
backup = bundle / 'backup' / path.name
backup.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(path, backup)
path.write_text(new, encoding='utf-8')
full = bundle / 'full_files' / path.name
full.parent.mkdir(parents=True, exist_ok=True)
full.write_text(new, encoding='utf-8')
node = next(n for n in ast.parse(new).body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == 'screen_shared_proof_context')
lines = new.splitlines(keepends=True)
(bundle / 'full_function.py').write_text(''.join(lines[node.lineno - 1:node.end_lineno]), encoding='utf-8')
print('PATCHED', path)
print('FULL_FUNCTION', bundle / 'full_function.py')
print('FULL_FILE', full)

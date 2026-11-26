"""Install only the reviewed display hook; retain the exact R9 search hook."""
from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = 'b6a986e72e70d17046e8ea2f0fd9d3cb42d03352'
TARGET = 'phase168_r3_27_typed_statement_projection.py'
SHARED = 'phase165_r52_r9_shared_math.py'
PINS = {'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
 'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
 'phase165_r52_r2_search_adapter.py': 'c1d08b803a4d9f9e4e1ad5180a1487422f1cd191',
 'phase165_r52_r9_shared_math.py': '4556e76736a3d5624632900ee9c4ab45599ffb0f',
 'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
 'phase168_r3_3_proof_narrative_model.py': '6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52',
 'phase168_r3_41p13_trust_boundary/verification.py': '547464846ce574d227092a4aacb895d2e2dfefca',
 'phase168_r3_5_model_renderer.py': '9afd21ed344beea80699f49cba16ddd68197198b',
 'phase175_r4r12r13r2_delta_injective_e_surjective/rule.py': '763b98521f8d78bbca1f07944194384c55a9ed57',
 'phase175_r4r12r13r2_delta_injective_e_surjective/tests/test_rule.py': 'dae9c098b3070dcca46c033ffc0b5c3cbee70176',
 'phase175_r4r12r13r4_hopf_zero_public/rule.py': '74b7e8dee9032f5b0cbfc0086646bb423e73be74',
 'phase177_r17r1_finite_delta_reason_display/projection.py': '8829b03bc1d5c1033013d76fe878c8af1dbae559',
 'phase177_r17r1_finite_delta_reason_display/tests/test_display.py': '5c145a1a8a04d45384cfe52fbc112aa3c5616941',
 'phase178_r1_k6_source_first_audit/audit.py': '4990d6ab37de46860a375d4d7a17207ed2daeb05',
 'phase178_r4_delta_surjective_zero_suspension_isolated/rule.py': '60b91c4ba674ca4680f0c3b353ceb873ecebc7ee',
 'phase178_r6_finite_group_cardinality_isolated/rule.py': '8c6de74a331d75b38d592603062d99c591a040b9',
 'phase178_r7_finite_group_cardinality_public/provider.py': '51b616d49ffed46d0589406a7e3856fed45c29b4',
 'phase178_r8_finite_group_surjective_injective_isolated/rule.py': '278fd450cfe9eacc20bb29af2b54bf5d72f528b7',
 'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
 'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314'}
R10_HASH = '8189641d53fa89c31d0f857bf9b53fd44752b24040b488ff662e467621dce1f9'
R10_HOOK = '    # Phase 178 R10: explain the direct equal-cardinality premises.\n    from phase178_r8_finite_group_surjective_injective_isolated.rule import RULE_NAME as equal_cardinality_rule\n    if (type(statement) is MapInjective and step.inference_rule is not None\n            and step.inference_rule.name == equal_cardinality_rule):\n        from phase178_r10_equal_cardinality_reason_display.projection import project_equal_cardinality_reason\n        return project_equal_cardinality_reason(statement, step) or result\n\n'
ANCHOR = '    premises = tuple(parent.conclusion for parent in step.premises)\n'
HOOK = '    # Phase 178 R11: explain the actual combined Delta-injective EHP inference.\n    from phase175_r4r12r13r2_delta_injective_e_surjective.rule import E_RULE_NAME as combined_e_rule\n    if (type(statement) is MapSurjective and step.inference_rule is not None\n            and step.inference_rule.name == combined_e_rule):\n        from phase178_r11_hopf_zero_reason_display.projection import project_hopf_zero_reason\n        return project_hopf_zero_reason(statement, step) or result\n\n'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def gt(*args):
    return git(*args).decode('utf-8').strip()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def normalize(raw):
    return raw.decode('utf-8-sig').replace('\r\n', '\n')


def proposed_source(source):
    lines = source.splitlines(keepends=True)
    tree = ast.parse(source)
    function, = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'map_property_sentence']
    original = ''.join(lines[function.lineno-1:function.end_lineno])
    require(original.count(ANCHOR) == 1 and 'project_hopf_zero_reason' not in source, 'DISPLAY_ANCHOR_OR_DUPLICATE')
    revised = ''.join(lines[:function.lineno-1]) + original.replace(ANCHOR, HOOK + ANCHOR, 1) + ''.join(lines[function.end_lineno:])
    ast.parse(revised)
    return revised


def full_review_source(source):
    lines = source.splitlines(keepends=True)
    nodes = [x for x in ast.parse(source).body if isinstance(x, (ast.Import, ast.ImportFrom)) or (isinstance(x, ast.FunctionDef) and x.name == 'map_property_sentence')]
    return '\n'.join(''.join(lines[x.lineno-1:x.end_lineno]) for x in nodes)


def preflight():
    head = gt('rev-parse', 'HEAD')
    require(Path(os.fsdecode(git('rev-parse', '--show-toplevel').strip())).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch', '--show-current') == 'develop' and head == gt('rev-parse', 'origin/develop'), 'HEAD_OR_BRANCH_MISMATCH')
    require(gt('merge-base', BASE, head) == BASE, 'REVIEWED_BASE_REQUIRED')
    require(not gt('diff', '--cached', '--name-only'), 'STAGED_CHANGES_REFUSED')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    changed = set(gt('diff', '--name-only', 'HEAD').splitlines())
    require(not changed - {TARGET}, 'UNRELATED_TRACKED_CHANGES:'+repr(sorted(changed)))
    for path, pin in PINS.items():
        require(gt('rev-parse', 'HEAD:'+path) == pin, 'PIN_CHANGED:'+path)
        require(normalize((ROOT/path).read_bytes()) == normalize(git('show', 'HEAD:'+path)), 'DEPENDENCY_CHANGED:'+path)
    r10 = ROOT/'phase178_r10_equal_cardinality_reason_display/projection.py'
    require(hashlib.sha256(r10.read_bytes().replace(b'\r\n',b'\n')).hexdigest() == R10_HASH, 'R10_PROJECTION_CHANGED')
    require(gt('rev-parse', BASE+':'+TARGET) == 'fc19a65386b92ce096c3f4c55fc10622b19c3d65', 'R10_BASE_BLOB_CHANGED')
    original = normalize(git('show', BASE+':'+TARGET))
    tree = ast.parse(original)
    function, = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'map_property_sentence']
    lines = original.splitlines(keepends=True)
    body = ''.join(lines[function.lineno-1:function.end_lineno])
    require(body.count(ANCHOR)==1 and R10_HOOK not in original, 'R10_BASE_ANCHOR_CHANGED')
    expected = ''.join(lines[:function.lineno-1]) + body.replace(ANCHOR,R10_HOOK+ANCHOR,1) + ''.join(lines[function.end_lineno:])
    require(normalize(git('show','HEAD:'+TARGET)) in (original,expected), 'HEAD_TARGET_UNREVIEWED')
    revised = proposed_source(expected)
    current = (ROOT/TARGET).read_bytes()
    require(normalize(current) in (expected,revised), 'R10_NOT_INSTALLED_OR_UNREVIEWED_TARGET_CHANGE')
    rest = current.replace(b'\r\n', b'')
    require(b'\r' not in rest and not (b'\r\n' in current and b'\n' in rest), 'MIXED_EOL')
    eol = '\r\n' if b'\r\n' in current else '\n'
    encoding = 'utf-8-sig' if current.startswith(b'\xef\xbb\xbf') else 'utf-8'
    updated = revised.replace('\n',eol).encode(encoding)
    git('diff','--check')
    return head,current,updated,revised,(ROOT/SHARED).read_bytes()

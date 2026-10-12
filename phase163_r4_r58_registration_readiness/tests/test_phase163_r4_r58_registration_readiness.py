import json
import os
from pathlib import Path

import pytest

from phase163_r4_r58_registration_readiness import assess, write_report


@pytest.fixture
def inputs():
    root = Path(__file__).resolve().parents[2]
    paths = (
        Path(os.environ.get('R58_TRIAL_PATH', str(root / 'phase163_r4_r55_output' / 'trial.json'))),
        Path(os.environ.get('R58_SCOPE_PATH', str(root / 'phase163_r4_r56_output' / 'scope.json'))),
        Path(os.environ.get('R58_BOUNDARY_PATH', str(root / 'phase163_r4_r57_output' / 'boundary.json'))),
    )
    return tuple(json.loads(path.read_text(encoding='utf-8-sig')) for path in paths)


def test_three_archival_candidates_without_semantic_promotion(inputs):
    result=assess(*inputs)
    assert result['archival_staging_ready_count']==3
    assert result['semantic_registration_ready_count']==0
    assert result['proof_eligible_count']==0


def test_existing_order_and_locators(inputs):
    result=assess(*inputs)
    assert [(r['locator'],r['publication_position']) for r in result['records']]==[('(2.9)',40),('(2.10)',41),('(4.3)',65)]


def test_unresolved_preserved(inputs):
    result=assess(*inputs)
    assert result['unresolved_semantics_count']==9
    assert all(len(r['unresolved_semantics'])==3 for r in result['records'])


def test_trial_ids_never_promoted(inputs):
    result=assess(*inputs)
    assert result['trial_ids_promoted_count']==0
    assert all(r['trial_assertion_id'].startswith('trial:r55:') for r in result['records'])


def test_different_scope_rejected(inputs):
    trial,scope,boundary=inputs
    scope['scope_items'][0]['domain_tex']='fabricated'
    with pytest.raises(ValueError,match='scope mismatch'):
        assess(trial,scope,boundary)


def test_different_source_digest_rejected(inputs):
    trial,scope,boundary=inputs
    trial['trial_items'][0]['tex_sha256']='altered'
    with pytest.raises(ValueError,match='digest mismatch'):
        assess(trial,scope,boundary)


def test_unsafe_registration_rejected(inputs):
    trial,scope,boundary=inputs
    boundary['production_ids_allocated']=True
    with pytest.raises(ValueError,match='unsafe'):
        assess(trial,scope,boundary)


def test_false_semantic_claim_rejected(inputs):
    trial,scope,boundary=inputs
    boundary['items'][0]['mathematical_semantics_verified']=True
    with pytest.raises(ValueError,match='semantic verification'):
        assess(trial,scope,boundary)


def test_files_written(tmp_path,inputs):
    result=assess(*inputs)
    write_report(result,tmp_path)
    assert (tmp_path/'readiness.json').exists()
    assert (tmp_path/'readiness.csv').exists()
    assert '未検証' in (tmp_path/'report.md').read_text(encoding='utf-8')

import json
from pathlib import Path
from audit import analyze

def test_static_chain(tmp_path):
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'probes').mkdir()
    (tmp_path / 'tests' / 'test_sample.py').write_text('from probes.probe_phase58_capabilities import x\n', encoding='utf-8')
    (tmp_path / 'probes' / 'probe_phase58_capabilities.py').write_text('from probes.probe_phase50_capabilities import y\n', encoding='utf-8')
    (tmp_path / 'probes' / 'probe_phase50_capabilities.py').write_text('from toda_rules import toda_pi4_3_delta_image_free_cyclic_inference_rule\n', encoding='utf-8')
    t = tmp_path / 'triage.json'
    t.write_text(json.dumps({'records':[{'test_path':'tests/test_sample.py','detail':"cannot import name 'toda_pi4_3_delta_image_free_cyclic_inference_rule'"}]}), encoding='utf-8')
    result = analyze(tmp_path, t)
    assert result['classification_counts'] == {'PROVEN_STATIC_CHAIN':1}
    assert result['test_dependencies'][0]['path_to_legacy_probe'][-1] == 'probes.probe_phase50_capabilities'

def test_unresolved_remains_unresolved(tmp_path):
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'tests' / 'test_sample.py').write_text('pass\n', encoding='utf-8')
    t = tmp_path / 'triage.json'
    t.write_text(json.dumps({'records':[{'test_path':'tests/test_sample.py','detail':'toda_pi4_3_delta_image_free_cyclic_inference_rule'}]}), encoding='utf-8')
    result = analyze(tmp_path, t)
    assert result['classification_counts'] == {'UNRESOLVED_STATIC_CHAIN':1}

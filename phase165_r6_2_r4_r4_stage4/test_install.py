from pathlib import Path
from types import SimpleNamespace
import ast
import pytest
from install import install, INSERT


def make_project(tmp_path):
    (tmp_path / 'phase165_r52_r9_shared_math.py').write_text(
        'def shared_expansion_provider(bridge, extra_providers=()):\n'
        '    available = []\n    return available\n', encoding='utf-8')
    (tmp_path / 'map_property_rules.py').write_text('\n'.join(
        f'class {n}:\n    pass' for n in
        ('KernelZeroStatement','ImageWholeStatement','ImageZeroStatement','KernelWholeStatement'))
        + '\n' + '\n'.join(f'def {n}():\n    pass' for n in
        ('exactness_and_zero_image_implies_zero_kernel_inference_rule',
         'exactness_and_whole_kernel_implies_whole_image_inference_rule')), encoding='utf-8')
    return tmp_path


def test_installs_and_preserves_other_source(tmp_path):
    root = make_project(tmp_path)
    assert install(root) == 'INSTALLED'
    content = (root / 'phase165_r52_r9_shared_math.py').read_text()
    assert INSERT in content
    ast.parse(content)


def test_idempotent(tmp_path):
    root = make_project(tmp_path)
    assert install(root) == 'INSTALLED'
    assert install(root) == 'ALREADY_INSTALLED'


def test_requires_prior_stages(tmp_path):
    root = make_project(tmp_path)
    (root / 'map_property_rules.py').write_text('')
    with pytest.raises(RuntimeError, match='prerequisite'):
        install(root)


def test_does_not_modify_unknown_shared_code(tmp_path):
    root = make_project(tmp_path)
    shared = root / 'phase165_r52_r9_shared_math.py'
    shared.write_text('def different():\n    return 3\n')
    with pytest.raises(RuntimeError):
        install(root)
    assert shared.read_text() == 'def different():\n    return 3\n'

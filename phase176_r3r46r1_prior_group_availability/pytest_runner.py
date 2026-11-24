"""Run one focused suite in a fresh process with canonical Hopf module identity."""
from __future__ import annotations

import argparse
import importlib
import importlib.util
import inspect
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def canonical_hopf_modules() -> None:
    """Load production modules before tests/conftest.py changes sys.path."""
    for name in ('hopf_rules', 'hopf_facts'):
        expected = (ROOT / (name + '.py')).resolve()
        spec = importlib.util.find_spec(name)
        if spec is None or spec.origin is None or Path(spec.origin).resolve() != expected:
            raise RuntimeError(f'NONCANONICAL_MODULE:{name}:{getattr(spec, "origin", None)}')
        module = importlib.import_module(name)
        if Path(module.__file__).resolve() != expected:
            raise RuntimeError(f'NONCANONICAL_LOADED_MODULE:{name}:{module.__file__}')
        print(f'PHASE176_R3R46R2_IMPORT_{name.upper()}={expected}', flush=True)
    from hopf_rules import HopfInvariantStatement
    from hopf_facts import ETA_2_HOPF_INVARIANT_FACT

    parameters = inspect.signature(HopfInvariantStatement).parameters
    if not {'expression', 'value', 'source', 'note'}.issubset(parameters):
        raise RuntimeError('CANONICAL_HOPF_SIGNATURE_MISMATCH')
    if type(ETA_2_HOPF_INVARIANT_FACT) is not HopfInvariantStatement:
        raise RuntimeError('CANONICAL_HOPF_TYPE_IDENTITY_MISMATCH')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('test_file', nargs='?')
    args = parser.parse_args()
    if Path.cwd().resolve() != ROOT:
        raise RuntimeError('REPOSITORY_ROOT_REQUIRED')
    if args.check_only == bool(args.test_file):
        parser.error('specify exactly one test file or --check-only')
    canonical_hopf_modules()
    if args.check_only:
        return 0
    path = (ROOT / args.test_file).resolve()
    if ROOT not in path.parents or not path.is_file() or path.suffix != '.py':
        raise RuntimeError('INVALID_FOCUSED_TEST_PATH')
    import pytest

    return int(pytest.main(['-q', '-p', 'no:cacheprovider', '--import-mode=importlib', str(path)]))


if __name__ == '__main__':
    raise SystemExit(main())

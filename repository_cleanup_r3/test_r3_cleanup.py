"""Targeted R3 safety tests; avoid the full project test suite."""
import csv
from pathlib import Path
import subprocess
import tempfile
import unittest

from r3_cleanup import FIELDS, is_cache_path, run


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        subprocess.run(['git', '-C', str(self.root), 'init', '-q'], check=True)
        (self.root / 'unified_statement_registry.py').write_text('example = 1\n', encoding='utf-8')
        self.cache = self.root / '__pycache__' / 'example.pyc'
        self.cache.parent.mkdir()
        self.cache.write_bytes(b'cache')
        self.manifest = self.root / 'phase163_r4_r94_output' / 'manifest.json'
        self.manifest.parent.mkdir()
        self.manifest.write_text('{}', encoding='utf-8')
        self.r2 = self.root / 'repository_cleanup_r2_output' / 'r2_cache_candidates.csv'
        self.r2.parent.mkdir()
        self.row = {'Path': '__pycache__/example.pyc', 'R1Category': 'CACHE_CANDIDATE',
                    'R2Decision': 'CACHE_DELETE_CANDIDATE', 'Reason': 'safe', 'Tracked': 'False',
                    'Exists': 'True', 'Bytes': '5', 'SHA256': '', 'IdenticalTo': ''}
        self.write_rows([self.row])
        self.out = self.root / 'repository_cleanup_r3_output'

    def tearDown(self):
        self.temp.cleanup()

    def write_rows(self, rows):
        with self.r2.open('w', encoding='utf-8-sig', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    def test_cache_shape(self):
        self.assertTrue(is_cache_path('x/__pycache__/foo.pyc'))
        self.assertTrue(is_cache_path('.pytest_cache/v/cache/nodeids'))
        self.assertFalse(is_cache_path('phase163_r4_r94_output/manifest.json'))

    def test_dry_run_preserves_everything(self):
        result = run(self.root, self.r2, self.out, apply=False)
        self.assertEqual(result['deleted_files'], 0)
        self.assertTrue(self.cache.is_file())

    def test_apply_only_cache(self):
        result = run(self.root, self.r2, self.out, apply=True)
        self.assertEqual(result['deleted_files'], 1)
        self.assertFalse(self.cache.exists())
        self.assertTrue(self.manifest.exists())
        self.assertTrue(result['tracked_status_unchanged'])

    def test_modified_size_blocks_all(self):
        self.cache.write_bytes(b'changed')
        with self.assertRaisesRegex(RuntimeError, 'Preflight blocked'):
            run(self.root, self.r2, self.out, apply=True)
        self.assertTrue(self.cache.exists())

    def test_tracked_cache_blocks_all(self):
        subprocess.run(['git', '-C', str(self.root), 'add', '__pycache__/example.pyc'], check=True)
        with self.assertRaisesRegex(RuntimeError, 'Preflight blocked'):
            run(self.root, self.r2, self.out, apply=True)
        self.assertTrue(self.cache.exists())

    def test_traversal_blocks_all(self):
        bad = dict(self.row, Path='../outside.pyc')
        self.write_rows([self.row, bad])
        with self.assertRaisesRegex(RuntimeError, 'Preflight blocked'):
            run(self.root, self.r2, self.out, apply=True)
        self.assertTrue(self.cache.exists())

    def test_symlink_blocks_all(self):
        self.cache.unlink()
        self.cache.symlink_to(self.manifest)
        with self.assertRaisesRegex(RuntimeError, 'Preflight blocked'):
            run(self.root, self.r2, self.out, apply=True)
        self.assertTrue(self.manifest.exists())


if __name__ == '__main__':
    unittest.main()

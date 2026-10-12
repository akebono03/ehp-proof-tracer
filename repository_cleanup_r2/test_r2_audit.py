import unittest
from r2_audit import cache_candidate, evaluate


class AuditClassificationTests(unittest.TestCase):
    def test_cache_paths(self):
        self.assertTrue(cache_candidate('tests/__pycache__/test_file.pyc'))
        self.assertTrue(cache_candidate('.pytest_cache/v/cache/nodeids'))
        self.assertFalse(cache_candidate('phase163_source_archive_catalog.json'))

    def test_tracked_cache_is_held(self):
        self.assertEqual(evaluate('__pycache__/x.pyc', True)[0], 'HOLD_TRACKED_CACHE')
        self.assertEqual(evaluate('__pycache__/x.pyc', None)[0], 'HOLD_GIT_UNKNOWN')
        self.assertEqual(evaluate('__pycache__/x.pyc', False)[0], 'CACHE_DELETE_CANDIDATE')

    def test_provenance_preserved(self):
        self.assertEqual(evaluate('phase163_r4_r94_output/manifest.json', False)[0], 'PRESERVE')
        self.assertEqual(evaluate('phase163_source_archive_catalog.json', False)[0], 'PRESERVE')
        self.assertEqual(evaluate('x.phase163_r84_before.py.bak', False)[0], 'REVIEW_BACKUP')


if __name__ == '__main__':
    unittest.main()

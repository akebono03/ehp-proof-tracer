"""Add the failed collection and repaired gate history to complete documents."""
from phase176_closeout.documents import sections as original_sections
from phase176_closeout_r1_test_scope_repair.repair import FAIL_STDOUT, FAIL_STDERR


def sections(report):
    if report['passed'] != 3546 or report['full_pytest_exit'] != 0:
        raise ValueError('REPAIRED_ACTIVE_SUITE_NOT_VERIFIED')
    if report['preflight']['r1']['collection_count'] != 3546:
        raise ValueError('R1_COLLECTION_NOT_VERIFIED')
    result = original_sections(report)
    en = ('The first closeout attempt on `471d79109d3054b088c7f910372b5f4f6cd5efa1` '
          'stopped during collection (exit 2) because a reintroduced historical Phase 77 test '
          'imported an archived module. R1 preserved four misplaced files as `.py.txt` archives, '
          'without changing the active test assertions or exclusion policy. R1 passed five focused '
          'tests and collected exactly 3546 active tests. R2 completed the repaired active suite. '
          f'The original failure stdout SHA-256 is `{FAIL_STDOUT}`, stderr SHA-256 `{FAIL_STDERR}`. '
          'The failed attempt and collection evidence remain separate from the successful final run.\n')
    ja = ('初回 Closeout（HEAD `471d79109d3054b088c7f910372b5f4f6cd5efa1`）は、'
          '混入した旧 Phase 77 テストの import エラーで収集時に停止した（終了コード2）。'
          'R1 は混入4ファイルを `.py.txt` として保存し、現行テストの合格条件や除外方針を変更せず、'
          '限定5件 PASS、3546件の収集成功を確認した。R2 は修正後の現行全体テストを実行した。'
          f'初回 stdout SHA-256 `{FAIL_STDOUT}`、stderr SHA-256 `{FAIL_STDERR}`。'
          '初回失敗記録と R1 収集記録を成功した終了記録とは別に保持する。\n')
    for name, text in result.items():
        if name == 'README.md':
            text = text.replace('The end-of-phase active `tests/` suite was run once successfully.',
                                'The repaired end-of-phase active `tests/` suite was run once successfully at R2.')
            result[name] = text.rstrip() + '\n\n' + en
        else:
            text = text.replace('現行アクティブ `tests/` 全体 pytest を Phase 末尾に1回実施し、成功を確認した。',
                                'R2 で修正後の現行アクティブ `tests/` 全体 pytest を1回実施し、成功を確認した。')
            result[name] = text.rstrip() + '\n\n' + ja
    return result

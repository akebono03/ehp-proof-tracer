from pathlib import Path

ROOT = Path.cwd()
FILES = (
    'phase165_r27_r6/test_phase165_r27_r6_legacy_entry_cut.py',
    'test_phase165_r52_r5_auto_search.py',
    'test_phase165_r52_r4_flask_connection.py',
)
for name in FILES:
    path = ROOT / name
    if not path.is_file():
        raise SystemExit(f'Missing test file: {name}')
    content = path.read_text(encoding='utf-8-sig')
    if "assert b'search_failed' in response.data" not in content and 'assert b"search_failed" in response.data' not in content:
        if 'assert "証明未完成".encode("utf-8") in response.data' in content:
            print(f'Already fixed: {name}')
            continue
        raise SystemExit(f'Expected assertion not found in {name}; no changes made to this file')
    content = content.replace("assert b'search_failed' in response.data", 'assert "証明未完成".encode("utf-8") in response.data')
    content = content.replace('assert b"search_failed" in response.data', 'assert "証明未完成".encode("utf-8") in response.data')
    path.write_text(content, encoding='utf-8', newline='')
    print(f'Updated: {name}')
print('Display contract test assertions aligned; no production files changed')

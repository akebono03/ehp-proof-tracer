from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    output = Path(__file__).resolve().parent
    command = [sys.executable, '-m', 'pytest', 'tests', '-q', '--tb=short', '--disable-warnings']
    log_path = output / 'pytest_full.log'
    status_path = output / 'pytest_status.json'
    started = datetime.now(timezone.utc).isoformat()
    print('ROOT:', root, flush=True)
    print('COMMAND:', ' '.join(command), flush=True)
    print('LOG:', log_path, flush=True)
    result_code = None
    state = 'interrupted'
    try:
        with log_path.open('w', encoding='utf-8', errors='replace') as stream:
            stream.write('COMMAND: ' + ' '.join(command) + '\n')
            stream.flush()
            proc = subprocess.Popen(command, cwd=root, stdout=stream, stderr=subprocess.STDOUT)
            try:
                result_code = proc.wait()
                state = 'completed'
            except KeyboardInterrupt:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                result_code = 130
    finally:
        status = {'command': command, 'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(), 'state': state, 'exit_code': result_code, 'log': str(log_path)}
        status_path.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding='utf-8')
    print('STATE:', state, flush=True)
    print('EXIT_CODE:', result_code, flush=True)
    print('LOG_TAIL:', flush=True)
    for line in log_path.read_text(encoding='utf-8', errors='replace').splitlines()[-35:]:
        print(line, flush=True)
    return result_code if result_code is not None else 130


if __name__ == '__main__':
    raise SystemExit(main())

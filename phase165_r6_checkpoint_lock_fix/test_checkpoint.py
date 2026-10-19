import importlib.util
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("checkpoint", Path(__file__).with_name("resumable_full_pytest.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_retry_permission_error(tmp_path):
    original = module.os.replace
    count = [0]
    def intermittent(src, dst):
        count[0] += 1
        if count[0] <= 2:
            raise PermissionError(5, "Access denied")
        return original(src, dst)
    with patch.object(module.os, "replace", side_effect=intermittent), patch.object(module.time, "sleep"):
        module.atomic_json(tmp_path / "state.json", {"status": "RUNNING"})
    assert count[0] == 3
    assert '"RUNNING"' in (tmp_path / "state.json").read_text()

def test_recover_only_complete_success_log(tmp_path):
    log = tmp_path / "batch_0007.log"
    log.write_text("."*40 + "\n40 passed in 11.75s\n")
    assert module.recover_successful_batch(log, 40)
    assert not module.recover_successful_batch(log, 39)
    log.write_text("39 passed, 1 failed in 11.75s\n")
    assert not module.recover_successful_batch(log, 40)

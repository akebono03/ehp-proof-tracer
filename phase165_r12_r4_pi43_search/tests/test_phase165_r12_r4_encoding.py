"""R12-R4: subprocess encoding must never be mistaken for a proof failure."""
from pathlib import Path
import importlib.util

AUDIT_PATH = Path(__file__).resolve().parents[1] / "audit.py"


def _load():
    spec = importlib.util.spec_from_file_location("phase165_r12_r4_encoding_audit", AUDIT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_decode_utf8_worker_json():
    module = _load()
    assert module.decode_worker_output('{"status":"証明未完了"}'.encode("utf-8")) == '{"status":"証明未完了"}'


def test_decode_cp932_worker_output():
    module = _load()
    assert module.decode_worker_output("探索失敗".encode("cp932")) == "探索失敗"


def test_decode_malformed_worker_output_does_not_crash():
    module = _load()
    output = module.decode_worker_output(b"invalid\x83\xff")
    assert isinstance(output, str)
    assert output

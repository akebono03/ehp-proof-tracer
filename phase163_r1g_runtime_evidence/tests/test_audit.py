from phase163_r1g_runtime_evidence.audit import describe_repository, write_report


class Statement:
    pass


class Step:
    def __init__(self):
        self.conclusion = Statement()
        self.premises = ()


class Entry:
    def __init__(self):
        self.key = "sample"
        self.theorem = "Sample"
        self.phase = "0"
        self.step = Step()


class Repository:
    def entries(self):
        return (Entry(),)


def test_describe_repository_records_runtime_entry():
    result = describe_repository("sample_repository", Repository())
    assert result["entry_count"] == 1
    assert result["entries"][0]["key"] == "sample"
    assert result["entries"][0]["statement_type"] == "Statement"
    assert result["entries"][0]["premise_count"] == 0


def test_write_report_exports_evidence(tmp_path):
    result = {
        "repositories": [describe_repository("sample_repository", Repository())],
        "errors": [],
        "unverified": ["literature order"],
    }
    write_report(tmp_path, result)
    assert (tmp_path / "summary.json").exists()
    assert "sample" in (tmp_path / "runtime_entries.csv").read_text(encoding="utf-8-sig")
    assert "未完了" in (tmp_path / "report.md").read_text(encoding="utf-8")

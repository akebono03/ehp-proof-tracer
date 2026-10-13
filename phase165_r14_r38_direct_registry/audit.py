import json
from pathlib import Path
from phase165_r14_r38_direct_registry import audit_completion

if __name__ == "__main__":
    result = audit_completion(Path(__file__).with_name("toda_51_complete.tex"))
    p = Path("phase165_r14_r38_output")
    p.mkdir(exist_ok=True)
    (p / "report.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf8")
    print(json.dumps(result, indent=2, ensure_ascii=False))

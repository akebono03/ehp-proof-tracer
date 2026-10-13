import json
from pathlib import Path
from phase165_r14_r41_proof_transfer import audit_r41
from toda_calculation_facade import build_standard_toda_report

def main():
    report = build_standard_toda_report(n=2, k=1)
    if len(report.candidates) != 1:
        raise ValueError("expected unique pi3^2 group result")
    output = audit_r41(report.candidates[0].source_candidate.group_result)
    target = Path("phase165_r14_r41_output")
    target.mkdir(exist_ok=True)
    (target / "report.json").write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

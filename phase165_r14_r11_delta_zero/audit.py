import json
from pathlib import Path
from phase165_r14_r11_delta_zero import audit_delta_pi32


def main():
    report = audit_delta_pi32()
    output = Path("phase165_r14_r11_output")
    output.mkdir(exist_ok=True)
    (output/"report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf8")
    (output/"report.md").write_text(
        "# Phase 165 R14-R11 — Δ=0 の導出\n\n" +
        "\n".join(f"- {key}: {val}" for key,val in report.items())+"\n",
        encoding="utf8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

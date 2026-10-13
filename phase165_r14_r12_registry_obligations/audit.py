import json
from pathlib import Path
from phase165_r14_r12_registry_obligations import audit_r12


def main():
    result = audit_r12()
    output = Path("phase165_r14_r12_output")
    output.mkdir(exist_ok=True)
    (output / "report.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf8"
    )
    lines = ["# Phase 165 R14-R12", ""]
    lines += [f"- {x['label']}: {x['origin']}" for x in result['obligations']]
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

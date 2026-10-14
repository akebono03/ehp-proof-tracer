# 追加ファイル

- `diagnose.py`: `diagnose()`（新規。読み取り専用）
- `run.ps1`: 実行スクリプト
- 既存の本番ファイル・関数・クラスは変更しません。

```python
"""Read-only trace of the old Toda (5.2) construction."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import traceback

import toda_upstream_bootstrap as bootstrap


def diagnose() -> dict:
    records = []
    original = bootstrap.run_inference_until_stable_with_history

    def capture(*args, **kwargs):
        result = original(*args, **kwargs)
        candidates = result.steps
        rules = args[0] if args else kwargs.get("rules", ())
        if not isinstance(rules, (tuple, list)):
            rules = (rules,)
        records.append({
            "rule_names": [getattr(rule, "name", repr(rule)) for rule in rules],
            "step_count": len(candidates),
            "conclusion_types": dict(Counter(type(step.conclusion).__name__ for step in candidates)),
            "toda52_conclusions": [
                repr(step.conclusion) for step in candidates
                if "52" in type(step.conclusion).__name__ or "Prop44" in type(step.conclusion).__name__
            ],
            "eta2_statements": [
                {
                    "type": type(step.conclusion).__name__,
                    "conclusion": repr(step.conclusion),
                    "proof_rule": str(step.rule),
                }
                for step in candidates
                if "Eta2" in type(step.conclusion).__name__ or "η₂" in repr(step.conclusion)
            ][:30],
        })
        return result

    bootstrap.run_inference_until_stable_with_history = capture
    error = None
    try:
        bootstrap.build_toda_52_composition_isomorphism_step()
    except Exception as exc:
        error = {"type": type(exc).__name__, "message": str(exc)}
    finally:
        bootstrap.run_inference_until_stable_with_history = original

    result = {
        "phase": "165 R52-R27-R3",
        "mode": "READ_ONLY_TODA52_PROOF_STEP_TRACE",
        "failure": error,
        "runs": records,
        "production_modified": False,
        "full_pytest_run": False,
    }
    out = Path(__file__).resolve().parent / "audit_output"
    out.mkdir(exist_ok=True)
    (out / "toda52_trace.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out / "review.md").write_text(
        "# Toda (5.2) 推論停止点\n\n"
        + f"- status: {error['type'] if error else 'SUCCESS'}\n"
        + f"- 推論エンジン呼び出し数: {len(records)}\n"
        + "\n## 規則と結論型\n\n"
        + "\n".join(
            f"### {i+1}\n\n規則: {r['rule_names']}\n\n結論の型: {r['conclusion_types']}\n"
            for i, r in enumerate(records)
        ) + "\n",
        encoding="utf-8",
    )
    return result


if __name__ == "__main__":
    report = diagnose()
    print(json.dumps({
        "phase": report["phase"],
        "mode": report["mode"],
        "failure": report["failure"],
        "run_count": len(report["runs"]),
        "output": "audit_output/toda52_trace.json",
        "production_modified": False,
        "full_pytest_run": False,
    }, ensure_ascii=False, indent=2))

```

from __future__ import annotations
import json
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
FUNCTIONS = {
    "render_completed_shared_narrative",
    "render_toda_group_proof_narrative_markdown",
    "render_completed_from_proofsteps",
    "build_toda_group_proof_narrative_reference_entries",
    "filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary",
    "_select_toda_group_proof_narrative_reference_entries_and_statement_lines",
    "_toda_group_proof_narrative_reference_statement_lines_by_number",
    "render_toda_group_proof_narrative_reference_entries_markdown",
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
}
MODULE_PREFIXES = ("toda_group_proof_narrative", "phase165_r56_", "phase165_r57_")

def step_summary(step):
    inference = getattr(step, "inference_rule", None)
    lit = getattr(inference, "literature_reference", None)
    return {"type": type(getattr(step, "conclusion", None)).__name__,
            "rule": getattr(inference, "name", None),
            "locator": getattr(lit, "locator", None),
            "statement": repr(getattr(step, "conclusion", None))[:550]}

def entries_summary(entries):
    if not isinstance(entries, (list, tuple)):
        return None
    if not all(hasattr(e, "reference") and hasattr(e, "proof_steps") for e in entries):
        return None
    return [{"number": e.number,
             "locator": getattr(e.reference, "locator", None),
             "steps": [step_summary(s) for s in e.proof_steps]}
            for e in entries]

def lines_summary(value):
    if not isinstance(value, dict):
        return None
    return {str(k): [str(x) for x in v] for k, v in value.items() if isinstance(v, tuple)}

def summarize(value):
    refs = entries_summary(value)
    if refs is not None:
        return {"entries": refs}
    if isinstance(value, tuple) and len(value) == 2:
        refs = entries_summary(value[0])
        if refs is not None:
            return {"entries": refs, "statement_lines": lines_summary(value[1])}
    if isinstance(value, str):
        before = value.split("## 証明", 1)[0]
        return {"text_length": len(value),
                "reference_excerpt": before[-3500:],
                "has_infinite_cyclic_raw": "infinite cyclic quotient structure" in value}
    return {"type": type(value).__name__}

def run():
    import web_group_proof
    events = []
    tracked = {}
    def profiler(frame, event, arg):
        if event not in ("call", "return", "exception"):
            return
        name = frame.f_code.co_name
        module = frame.f_globals.get("__name__", "")
        if name not in FUNCTIONS or not module.startswith(MODULE_PREFIXES):
            return
        if event == "call":
            info = {"function": name, "module": module, "stage": "call"}
            if "entries" in frame.f_locals:
                info["entries_input"] = entries_summary(frame.f_locals["entries"])
            if "reference_entries" in frame.f_locals:
                info["reference_entries_input"] = entries_summary(frame.f_locals["reference_entries"])
            if "statement_lines_by_reference_number" in frame.f_locals:
                info["statement_lines_input"] = lines_summary(frame.f_locals["statement_lines_by_reference_number"])
            events.append(info)
            tracked[id(frame)] = info
        elif event == "return":
            info = {"function": name, "module": module, "stage": "return",
                    "output": summarize(arg)}
            events.append(info)
            tracked.pop(id(frame), None)
        elif event == "exception":
            events.append({"function": name, "stage": "exception", "error": repr(arg[1])})
    report = {"phase": "167 R1", "mode": "READ_ONLY_FUNCTION_TRACE",
              "production_changes": False, "full_pytest_run": False,
              "target": "pi_4^3", "events": events}
    previous = sys.getprofile()
    try:
        sys.setprofile(profiler)
        try:
            view = web_group_proof.build_standard_web_group_proof_view(3, 1, 2, "narrative")
        finally:
            sys.setprofile(previous)
        report["view"] = {"key": view.key, "mode": view.mode,
                          "line_count": len(view.rendered_lines)}
        rows = []
        for line in view.rendered_lines:
            rows.append(str(line) if isinstance(line, str)
                        else str(getattr(line, "prefix", "")) + " " +
                        str(getattr(line, "statement_latex", "") or "") +
                        " " + str(getattr(line, "suffix", "")))
        text = "\n".join(rows)
        (HERE/"web_lines.txt").write_text(text, encoding="utf-8")
        reference_section = text.split("使用する結果",1)[-1].split("証明",1)[0]
        report["final_reference_section"] = reference_section
        report["final_has_general_diagonal"] = r"\pi_{n}^{n}" in reference_section
        report["final_has_general_zero"] = (r"\pi_{i}^{n}" in reference_section or
                                            r"\pi_{i}^{1}" in reference_section)
        report["final_has_raw_english"] = "infinite cyclic quotient structure" in text
    except BaseException:
        sys.setprofile(previous)
        report["error"] = traceback.format_exc()
    output = HERE/"trace_report.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str),encoding="utf-8")
    print(json.dumps({"phase":report["phase"],"mode":report["mode"],
                      "view":report.get("view"),
                      "functions_called":[e["function"] for e in events if e["stage"]=="call"],
                      "final_has_general_diagonal":report.get("final_has_general_diagonal"),
                      "final_has_general_zero":report.get("final_has_general_zero"),
                      "final_has_raw_english":report.get("final_has_raw_english"),
                      "error":report.get("error"),
                      "report":str(output)},ensure_ascii=False,indent=2))
if __name__=="__main__":
    run()

"""Read-only stage audit of existing Phase 159 exactness linker."""
from __future__ import annotations
import json
from pathlib import Path
from toda_calculation_facade import build_standard_toda_report
from phase165_r14_r41_proof_transfer import build_phase165_r41_pi32_common_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
import toda_group_proof_narrative_renderer as renderer
from phase164_r9_narrative_contract import normalize_public_narrative_contract


def report():
    result = build_standard_toda_report(n=2, k=1).candidates[0].source_candidate.group_result
    replay = build_phase165_r41_pi32_common_replay(result, 2, "narrative")
    presentation = build_toda_group_proof_presentation(replay)
    baseline = renderer._phase158_baseline_render_toda_group_proof_narrative_markdown(presentation)
    contract = renderer._phase158_normalize_public_narrative_contract(presentation, baseline)
    wording = renderer._phase159_normalize_public_map_property_wording(presentation, contract)
    reference_wording = renderer._phase159_normalize_public_reference_map_property_wording(wording)
    toda51 = renderer._phase159_r1_6c_canonicalize_toda_51_reference(reference_wording)
    reduced = renderer._phase159_r1_6c_remove_redundant_exactness_sentence(toda51)
    linked = renderer._phase159_r1_6c_link_proof_reasons(presentation, reduced)
    final = renderer.render_toda_group_proof_narrative_markdown(presentation)
    relinked = renderer._phase159_r1_6c_link_proof_reasons(presentation, final)
    normalized_again = normalize_public_narrative_contract(relinked)
    snapshots = {
        "baseline": baseline,
        "contract": contract,
        "wording": wording,
        "reduced": reduced,
        "linked": linked,
        "final": final,
        "final_relinked": relinked,
        "final_relinked_normalized": normalized_again,
    }
    stages = {}
    for key, value in snapshots.items():
        stages[key] = {
            "exactness_connector_count": value.count("完全性より"),
            "changed_from_baseline": value != baseline,
            "has_reference_section": "使用する結果" in value,
            "has_proof_section": "証明" in value,
        }
    steps = []
    for node in presentation.nodes:
        step = node.proof_step
        if any(type(p.conclusion).__name__ == "TodaProp42ExactnessStatement"
               for p in step.premises):
            generic = renderer._render_generic_narrative_step(step)
            compact = renderer._phase159_r1_6c_compact_map_property_line(generic)
            key = renderer._phase159_r1_6c_statement_match_key(compact)
            body = reduced.split("## 証明",1)[-1]
            matches = [line for line in body.splitlines()
                       if renderer._phase159_r1_6c_statement_match_key(line.strip()) == key]
            steps.append({
                "statement_type": type(step.conclusion).__name__,
                "inference_rule": step.inference_rule.name if step.inference_rule else None,
                "generic": generic,
                "expected_match_key": key,
                "matching_lines_before_linker": matches,
            })
    return {"phase":"165 R46 READ_ONLY", "stages":stages,
            "exactness_proofsteps":steps,
            "linker_changes_final_output":final!=relinked,
            "public_normalizer_removes_relinked_connector":
                relinked.count("完全性より")>normalized_again.count("完全性より"),
            "sources_modified":False,"full_pytest_run":False}


if __name__=="__main__":
    data=report()
    path=Path("phase165_r46_stage_audit_output/report.json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf8")
    print(json.dumps(data,ensure_ascii=False,indent=2))

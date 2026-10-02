from __future__ import annotations
import argparse, ast, json
from pathlib import Path

DELETE = {
"tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py::test_phase144_6_r5_43_10_all_sixteen_uniform_chains_receive_compression_connector",
"tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py::test_phase144_6_r5_43_10_preserves_direct_connector",
"tests/test_phase144_6_r5_43_2_placement_aware_contribution_insertion.py::test_phase144_6_r5_43_2_pi6_uses_provider_anchor_indices",
"tests/test_phase144_6_r5_43_2_placement_aware_contribution_insertion.py::test_phase144_6_r5_43_2_pi6_contributions_are_not_dumped_after_final_connector",
"tests/test_phase144_6_r5_43_2_placement_aware_contribution_insertion.py::test_phase144_6_r5_43_2_pi6_contributions_remain_unique_and_topologically_ordered",
"tests/test_phase144_6_r5_43_4_dependency_aware_contribution_connector.py::test_phase144_6_r5_43_4_only_direct_contribution_dependency_gets_direct_connector",
"tests/test_phase144_6_r5_43_4_dependency_aware_contribution_connector.py::test_phase144_6_r5_43_4_c4_to_c5_has_connector",
"tests/test_phase144_6_r5_43_4_dependency_aware_contribution_connector.py::test_phase144_6_r5_43_4_preserves_r5_43_2_placement_and_uniqueness",
"tests/test_phase144_6_r5_43_generic_renderer_contribution_connection.py::test_phase144_6_r5_43_pi6_contributions_enter_generic_narrative_in_order",
}

REPLACE = {
("tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py","test_phase144_6_r5_43_10_renderer_does_not_read_inference_rule_names"):
'def test_phase144_6_r5_43_10_renderer_does_not_hard_code_historical_rule_names():\n  import inspect\n  import toda_group_proof_narrative_contribution_renderer as module\n\n  source = inspect.getsource(module)\n\n  assert "finite-cyclic transport" not in source\n  assert "eta_4 squared stable transport" not in source\n',
("tests/test_phase153_r3_4_reference_statement_rendering_connection.py","test_phase153_r3_4_public_pi10_6_reference_section_excludes_obsolete_45"):
'def test_phase153_r3_4_public_pi10_6_reference_section_excludes_obsolete_45():\n  rendered = render_toda_group_proof_narrative_markdown(\n    _phase153_r3_4_pi10_6_presentation()\n  )\n  reference_section = rendered.split("## 証明", 1)[0]\n\n  assert "[R" in reference_section\n  assert "(4.5)" not in reference_section\n  assert "$\\\\pi_{10}^{6} = 0$" in rendered\n',
("tests/test_phase96_full_proof_report_renderer.py","test_phase96_11_actual_pi9_5_full_report_contains_source_metadata"):
'def test_phase96_11_actual_pi9_5_full_report_contains_source_metadata():\n  actual = build_phase96_11_presentation("pi9_5")\n  rendered = render_toda_full_proof_report_markdown(actual["presentation"])\n  goal_source = actual["candidate"].goal_source\n\n  assert "## Source" in rendered\n\n  if goal_source is None:\n    assert "- Discovery source: direct repository result" in rendered\n    return\n\n  repository_source = goal_source.source_entry\n  assert "- Phase: " + (repository_source.phase or "unknown") in rendered\n  assert "- Theorem: " + (repository_source.theorem or "unknown") in rendered\n  assert "- Branch: `" + goal_source.branch_name + "`" in rendered\n',
("tests/test_phase96_human_readable_renderer.py","test_phase96_9_actual_pi9_5_markdown_contains_result_source_and_ehp"):
'def test_phase96_9_actual_pi9_5_markdown_contains_result_source_and_ehp():\n  actual = build_phase96_9_presentation("pi9_5")\n  rendered = render_toda_end_to_end_markdown(actual["presentation"])\n  goal_source = actual["candidate"].goal_source\n\n  assert "# $\\\\pi_{9}^{5}$" in rendered\n  assert "## Result" in rendered\n  assert r"\\pi_{9}^{5} \\cong \\mathbb{Z}/2\\{\\nu_{5}\\eta_{8}\\}" in rendered\n  assert "## Source" in rendered\n\n  if goal_source is None:\n    assert "- Discovery source: direct repository result" in rendered\n  else:\n    repository_source = goal_source.source_entry\n    assert "- Phase: " + (repository_source.phase or "unknown") in rendered\n    assert "- Theorem: " + (repository_source.theorem or "unknown") in rendered\n    assert "- Branch: `" + goal_source.branch_name + "`" in rendered\n\n  assert "## EHP sequence" in rendered\n  assert r"\\xrightarrow{\\Delta}" in rendered\n  assert r"\\xrightarrow{E}" in rendered\n  assert r"\\xrightarrow{H}" in rendered\n'
}

def funcs(src):
    t=ast.parse(src)
    return {n.name:n for n in t.body if isinstance(n,ast.FunctionDef)}

def replace(src,name,new):
    ls=src.splitlines(keepends=True); fs=funcs(src); n=fs[name]
    a=sum(map(len,ls[:n.lineno-1])); b=sum(map(len,ls[:n.end_lineno]))
    out=src[:a]+new.rstrip()+"\n"+src[b:]; ast.parse(out); return out

def remove(src,names):
    ls=src.splitlines(keepends=True); fs=funcs(src)
    spans=sorted([(fs[n].lineno-1,fs[n].end_lineno) for n in names], reverse=True)
    for a,b in spans: del ls[a:b]
    out="".join(ls); ast.parse(out); return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--repo-root",type=Path,default=Path.cwd()); ap.add_argument("--original-plan",type=Path,required=True)
    a=ap.parse_args(); root=a.repo_root.resolve(); plan=json.loads(a.original_plan.read_text(encoding="utf-8"))
    mapping={k.replace("\\\\","/"):int(v) for k,v in plan["file_to_shard"].items()}
    expected={
      "tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py":4,
      "tests/test_phase144_6_r5_43_2_placement_aware_contribution_insertion.py":4,
      "tests/test_phase144_6_r5_43_4_dependency_aware_contribution_connector.py":4,
      "tests/test_phase144_6_r5_43_generic_renderer_contribution_connection.py":5,
      "tests/test_phase153_r3_4_reference_statement_rendering_connection.py":5,
      "tests/test_phase96_full_proof_report_renderer.py":8,
      "tests/test_phase96_human_readable_renderer.py":8,
    }
    for p,s in expected.items():
      if mapping.get(p)!=s: raise SystemExit(f"unexpected shard for {p}: {mapping.get(p)}")
    for (p,n),new in REPLACE.items():
      path=root/p; src=path.read_text(encoding="utf-8-sig"); path.write_text(replace(src,n,new),encoding="utf-8")
    grouped={}
    for nodeid in DELETE:
      p,n=nodeid.split("::",1); grouped.setdefault(p,set()).add(n)
    for p,names in grouped.items():
      path=root/p; src=path.read_text(encoding="utf-8-sig"); path.write_text(remove(src,names),encoding="utf-8")
    print("stale repairs applied")
    print("deleted:",len(DELETE))
    print("replaced:",len(REPLACE))
    print("production changes: none")

if __name__=="__main__": main()

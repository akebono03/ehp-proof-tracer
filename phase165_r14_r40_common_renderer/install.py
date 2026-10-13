"""Remove the R39 Web special case and select R38 proof in the common replay."""
from pathlib import Path
import ast

root = Path(__file__).resolve().parent.parent
web = root / "web_group_proof.py"
common = root / "phase164_r5_r2_common_replay.py"
web_source = web.read_text(encoding="utf-8")
route = (
    "  if n == 2 and k == 1:\n"
    "    from phase165_r14_r39_web_connection import build_phase165_pi32_web_view\n"
    "    return build_phase165_pi32_web_view(max_depth=max_depth, mode=mode)\n"
)
if route in web_source:
    web_updated = web_source.replace(route, "", 1)
else:
    if "build_phase165_pi32_web_view" in web_source:
        raise RuntimeError("Unexpected R39 Web route; refusing to modify")
    web_updated = web_source
common_source = common.read_text(encoding="utf-8")
needle = '    if mode == "narrative" and n == 3 and k == 2:\n'
new_branch = (
    "    if n == 2 and k == 1:\n"
    "        from phase165_r14_r40_replay import build_phase165_r40_pi32_common_replay\n"
    "        return build_phase165_r40_pi32_common_replay(group_result, max_depth)\n\n"
)
if new_branch not in common_source:
    if common_source.count(needle) != 1:
        raise RuntimeError("Unexpected common replay layout; refusing to modify")
    common_updated = common_source.replace(needle, new_branch + needle, 1)
else:
    common_updated = common_source
compile(web_updated, str(web), "exec")
compile(common_updated, str(common), "exec")
if web_updated != web_source:
    web.with_name("web_group_proof.phase165_r40_backup.py").write_text(web_source, encoding="utf-8")
    web.write_text(web_updated, encoding="utf-8")
if common_updated != common_source:
    common.with_name("phase164_r5_r2_common_replay.phase165_r40_backup.py").write_text(common_source, encoding="utf-8")
    common.write_text(common_updated, encoding="utf-8")
print("R39 special-case removed; R38 proof routed through common replay/presentation/renderer")

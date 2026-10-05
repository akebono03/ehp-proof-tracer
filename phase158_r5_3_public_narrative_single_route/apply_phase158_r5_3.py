from pathlib import Path
import shutil
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
TARGET = REPO_ROOT / "toda_group_proof_narrative_renderer.py"

OLD = r"""  phase134_24_pi15_8 = (
    _phase134_24_render_pi15_8_narrative(
      presentation
    )
  )

  if phase134_24_pi15_8 is not None:
    return (
      _finalize_toda_group_proof_narrative_markdown(
        _phase153_r3_10_connect_public_reference_section(
          presentation,
          phase134_24_pi15_8,
        )
      )
    )

  if (
    _is_phase134_3_pi6_3_presentation(
      presentation
    )
    or _is_phase150_rc4_generic_route_target(
      presentation
    )
  ):
    semantic_sidecar = (
      build_toda_group_proof_narrative_semantic_sidecar(
        presentation
      )
    )
    blocks = (
      build_toda_group_proof_narrative_blocks(
        presentation,
        semantic_sidecar=semantic_sidecar,
      )
    )
    arguments = (
      build_toda_group_proof_narrative_arguments(
        presentation,
        blocks,
        semantic_sidecar=semantic_sidecar,
      )
    )

    rendered = (
      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )

    public_rendered = (
      _wrap_phase150_rc4_generic_public_narrative(
        presentation,
        rendered,
      )
    )

    return (
      _finalize_toda_group_proof_narrative_markdown(
        public_rendered
      )
    )

  if _is_phase134_9_pi8_5_presentation(
    presentation
  ):
    rendered = (
      _render_phase134_9_pi8_5_narrative_markdown(
        presentation
      )
    )

    return (
      _finalize_toda_group_proof_narrative_markdown(
        _phase153_r3_10_connect_public_reference_section(
          presentation,
          rendered,
        )
      )
    )

"""
NEW = r"""  if presentation.max_depth >= 2:
    semantic_sidecar = (
      build_toda_group_proof_narrative_semantic_sidecar(
        presentation
      )
    )
    blocks = (
      build_toda_group_proof_narrative_blocks(
        presentation,
        semantic_sidecar=semantic_sidecar,
      )
    )
    arguments = (
      build_toda_group_proof_narrative_arguments(
        presentation,
        blocks,
        semantic_sidecar=semantic_sidecar,
      )
    )

    rendered = (
      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )

    public_rendered = (
      _wrap_phase150_rc4_generic_public_narrative(
        presentation,
        rendered,
      )
    )

    return (
      _finalize_toda_group_proof_narrative_markdown(
        public_rendered
      )
    )

"""

def main() -> int:
    if not TARGET.exists():
        raise FileNotFoundError(f"target file not found: {TARGET}")

    raw = TARGET.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8")
    normalized = text.replace("\r\n", "\n")

    count = normalized.count(OLD)
    if count != 1:
        raise RuntimeError(
            "expected exactly one current Phase 158 baseline route block; "
            f"found {count}. Repository may not match the audited HEAD."
        )

    updated = normalized.replace(OLD, NEW, 1)

    backup = TARGET.with_suffix(TARGET.suffix + ".phase158_r5_3_backup")
    if not backup.exists():
        shutil.copy2(TARGET, backup)

    if newline == "\r\n":
        updated = updated.replace("\n", "\r\n")

    TARGET.write_bytes(updated.encode("utf-8"))

    print("Phase 158-R5-3 applied.")
    print("Production code:")
    print("  toda_group_proof_narrative_renderer.py")
    print("Changed function:")
    print("  _phase158_baseline_render_toda_group_proof_narrative_markdown")
    print("Public Narrative depth >= 2 now uses one generic multi-argument route.")
    print("Depth < 2 fallback is preserved.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

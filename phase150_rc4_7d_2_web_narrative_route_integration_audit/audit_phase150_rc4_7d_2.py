from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_renderer import (
  _is_phase134_3_pi6_3_presentation,
  _is_phase134_9_pi8_5_presentation,
  _phase134_24_render_pi15_8_narrative,
  render_toda_group_proof_narrative_markdown,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)


CASES = (
  ("pi_6^3", 3, 3),
  ("pi_8^5", 5, 3),
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _web_text(view):
  parts = []
  for line in view.rendered_lines:
    if line.segments:
      parts.append(
        "".join(
          segment.value
          for segment in line.segments
        )
      )
    else:
      parts.append(
        line.prefix
        + (
          ""
          if line.statement_latex is None
          else line.statement_latex
        )
        + line.suffix
      )
  return "\n".join(parts)


def _route_name(presentation):
  if (
    _phase134_24_render_pi15_8_narrative(
      presentation
    )
    is not None
  ):
    return "DEDICATED_PI15_8"

  if _is_phase134_3_pi6_3_presentation(
    presentation
  ):
    return "GENERIC_CONTRIBUTION_PI6_3"

  if _is_phase134_9_pi8_5_presentation(
    presentation
  ):
    return "DEDICATED_PI8_5"

  return "LEGACY_RECURSIVE_FALLBACK"


def main():
  print(
    "Phase 150 RC4-7D-2 "
    "Web Narrative Route Integration Audit"
  )
  print("Production changes: none")
  print()

  mismatch_count = 0
  legacy_target_count = 0

  for label, n, k in CASES:
    (
      presentation,
      blocks,
      sidecar,
      arguments,
    ) = _method_evidence_data(n, k)

    public_markdown = (
      render_toda_group_proof_narrative_markdown(
        presentation
      )
    )
    generic_markdown = (
      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
      )
    )
    web_view = build_standard_web_group_proof_view(
      n,
      k,
      max_depth=2,
      mode="narrative",
    )
    web_text = _web_text(web_view)
    route = _route_name(presentation)

    reason_phrase = (
      "以上で得た群構造、生成元、および写像に関する"
      "結果を合わせると"
    )
    map_reason_phrase = (
      "この完全性、既知の群構造、および写像の像に関する"
      "結果を合わせると"
    )
    order_reason_phrase = (
      "この群構造と写像による移送の結果を合わせると"
    )

    generic_reason_visible = any(
      phrase in generic_markdown
      for phrase in (
        reason_phrase,
        map_reason_phrase,
        order_reason_phrase,
      )
    )
    public_reason_visible = any(
      phrase in public_markdown
      for phrase in (
        reason_phrase,
        map_reason_phrase,
        order_reason_phrase,
      )
    )
    web_reason_visible = any(
      phrase in web_text
      for phrase in (
        reason_phrase,
        map_reason_phrase,
        order_reason_phrase,
      )
    )

    public_web_same_reason_visibility = (
      public_reason_visible
      == web_reason_visible
    )
    generic_public_same_reason_visibility = (
      generic_reason_visible
      == public_reason_visible
    )

    if not generic_public_same_reason_visibility:
      mismatch_count += 1

    if (
      label in (
        "pi_10^4",
        "pi_12^5",
        "pi_16^9",
      )
      and route == "LEGACY_RECURSIVE_FALLBACK"
    ):
      legacy_target_count += 1

    print("=" * 100)
    print(label)
    print("=" * 100)
    print(f"route={route}")
    print(
      "generic_reason_visible="
      f"{generic_reason_visible}"
    )
    print(
      "public_reason_visible="
      f"{public_reason_visible}"
    )
    print(
      "web_reason_visible="
      f"{web_reason_visible}"
    )
    print(
      "public_web_same_reason_visibility="
      f"{public_web_same_reason_visibility}"
    )
    print(
      "generic_public_same_reason_visibility="
      f"{generic_public_same_reason_visibility}"
    )
    print()
    print("PUBLIC_RENDERER_HEAD")
    print("-" * 100)
    print("\n".join(public_markdown.splitlines()[:32]))
    print()
    print("GENERIC_CONTRIBUTION_HEAD")
    print("-" * 100)
    print("\n".join(generic_markdown.splitlines()[:32]))
    print()

  print("=" * 100)
  print("CROSS-GROUP SUMMARY")
  print("=" * 100)
  print(
    "GENERIC_PUBLIC_REASON_VISIBILITY_MISMATCH_COUNT="
    f"{mismatch_count}"
  )
  print(
    "RC4_TARGETS_ON_LEGACY_RECURSIVE_FALLBACK="
    f"{legacy_target_count}/3"
  )

  if legacy_target_count == 3:
    print(
      "AUDIT_DECISION="
      "PUBLIC_RENDERER_DISPATCH_BYPASSES_GENERIC_REASON_ROUTE"
    )
  else:
    print(
      "AUDIT_DECISION="
      "ROUTE_INTEGRATION_REQUIRES_FURTHER_DIAGNOSIS"
    )


if __name__ == "__main__":
  main()

from repository_operation_query_presentation import (
  RepositoryOperationQueryPresentation,
)


def render_repository_operation_query_markdown(
  presentation: RepositoryOperationQueryPresentation,
) -> str:
  if not isinstance(
    presentation,
    RepositoryOperationQueryPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "RepositoryOperationQueryPresentation"
    )

  lines = [
    "# Known repository facts",
    "",
  ]

  for index, item in enumerate(
    presentation.items,
    start=1,
  ):
    if index > 1:
      lines.append(
        ""
      )

    primary_match = (
      item.primary_match
    )

    node = (
      primary_match.scope_node
    )

    lines.append(
      (
        str(
          index
        )
        + ". $"
        + item.statement_latex
        + "$"
      )
    )

    theorem = (
      node.root_entry.theorem
    )

    phase = (
      node.root_entry.phase
    )

    if theorem is not None:
      provenance_text = theorem

      if phase is not None:
        provenance_text += (
          ", Phase "
          + phase
        )

      provenance_text += (
        ", depth "
        + str(
          node.shortest_depth
        )
      )

      lines.append(
        (
          "   - First provenance: "
          + provenance_text
        )
      )
    else:
      lines.append(
        (
          "   - First provenance: "
          + node.root_entry.key
          + ", depth "
          + str(
            node.shortest_depth
          )
        )
      )

    if item.provenance_count > 1:
      lines.append(
        (
          "   - Provenance paths: "
          + str(
            item.provenance_count
          )
        )
      )

  return (
    "\n".join(
      lines
    )
    + "\n"
  )

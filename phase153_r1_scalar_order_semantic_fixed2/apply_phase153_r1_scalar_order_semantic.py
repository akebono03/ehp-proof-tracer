from pathlib import Path

TARGET = Path("toda_group_proof_narrative_classifier.py")


def replace_once(text, old, new):
    if old not in text:
        raise RuntimeError("target text not found")
    return text.replace(old, new, 1)


def main():
    text = TARGET.read_text(encoding="utf-8")

    if "from scalar_rules import (" not in text:
        text = replace_once(
            text,
            "from proof import (\n  ProofStep,\n  Relation,\n  RelationType,\n)\n",
            "from proof import (\n  ProofStep,\n  Relation,\n  RelationType,\n)\nfrom scalar_rules import (\n  ScalarGreaterEqualStatement,\n)\n",
        )

    helper = r"""def _is_order_statement(
  statement,
) -> bool:
  if isinstance(
    statement,
    ScalarGreaterEqualStatement,
  ):
    return True

  return (
    isinstance(
      statement,
      Relation,
    )
    and statement.relation_type
    is RelationType.ORDER
  )


"""

    if "def _is_order_statement(" not in text:
        text = replace_once(
            text,
            "def _is_order_dependency(\n",
            helper + "def _is_order_dependency(\n",
        )

    marker = """  statement = proof_step.conclusion
  root_group = _root_group(
    presentation
  )

"""
    addition = """  statement = proof_step.conclusion
  root_group = _root_group(
    presentation
  )

  if _is_order_statement(
    statement,
  ):
    return (
      TodaGroupProofNarrativeBlockRole.ORDER
    )

"""

    if "if _is_order_statement(" not in text:
        text = replace_once(text, marker, addition)

    TARGET.write_text(text, encoding="utf-8")
    print("Phase153-R1 production patch applied.")


if __name__ == "__main__":
    main()

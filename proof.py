from dataclasses import dataclass


@dataclass
class ProofFact:
  statement: str
  reference: str | None = None


@dataclass
class ProofStep:
  conclusion: str
  rule: str
  premises: list[ProofFact]
  
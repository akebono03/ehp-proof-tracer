# Phase 161 R1 — 7規則の実体監査

実際の Production 規則を読み取った記録。逆向き探索の実行は行っていません。

## toda_53_n3_prop51_delta_injective_inference_rule

- Production name: `Toda Proposition 5.1 n=3 Delta injectivity`
- Premise count: 1
- conclusion_pattern: `None`
- conclusion_builder: `True`
- match_guard: `True`

### premise_patterns

```json
[
  {
    "type": "proof.PremisePattern",
    "fields": {
      "proof_rule": "<ProofRule.INFERENCE: 'inference'>",
      "statement_type": "toda_rules.TodaProp51FiniteDimensionalStatement",
      "statement_pattern": null,
      "relation_type": null,
      "relation_pattern": null
    }
  }
]
```

### factory_source

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30051`

```python
def toda_53_n3_prop51_delta_injective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    statement = (
      premises[
        0
      ].conclusion
    )

    delta_relation = (
      statement
      .delta_iota5_relation
    )

    pi_5_5 = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )

    pi_3_2 = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    if (
      delta_relation.map.source_group
      != pi_5_5
    ):
      return False

    if (
      delta_relation.map.target_group
      != pi_3_2
    ):
      return False

    iota_5 = HomotopyElement(
      name="ι_5",
      dimension=5,
      generator=GeneratorSymbol(
        family="ι",
        index=5,
      ),
    )

    if (
      delta_relation.element
      != iota_5
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    return (
      delta_relation.positive_value
      == Multiple(
        coefficient=2,
        expression=eta_2,
      )
    )

  def build_conclusion(
    premises,
  ):
    statement = (
      premises[
        0
      ].conclusion
    )

    return TodaDeltaInjectiveStatement(
      map=(
        statement
        .delta_iota5_relation
        .map
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.1 "
      "n=3 Delta injectivity"
    ),
    description=(
      "For the concrete Delta map "
      "from pi_5^5 to pi_3^2, "
      "the Proposition 5.1 data "
      "Delta(iota_5)=plus or minus "
      "2 eta_2 gives the injectivity "
      "required in the n=3 proof of "
      "Toda Proposition 5.3."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp51FiniteDimensionalStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )

```

### conclusion_builder

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30123`

```python
  def build_conclusion(
    premises,
  ):
    statement = (
      premises[
        0
      ].conclusion
    )

    return TodaDeltaInjectiveStatement(
      map=(
        statement
        .delta_iota5_relation
        .map
      ),
    )

```

### match_guard

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30052`

```python
  def guard(
    premises,
    bindings,
  ):
    statement = (
      premises[
        0
      ].conclusion
    )

    delta_relation = (
      statement
      .delta_iota5_relation
    )

    pi_5_5 = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )

    pi_3_2 = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    if (
      delta_relation.map.source_group
      != pi_5_5
    ):
      return False

    if (
      delta_relation.map.target_group
      != pi_3_2
    ):
      return False

    iota_5 = HomotopyElement(
      name="ι_5",
      dimension=5,
      generator=GeneratorSymbol(
        family="ι",
        index=5,
      ),
    )

    if (
      delta_relation.element
      != iota_5
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    return (
      delta_relation.positive_value
      == Multiple(
        coefficient=2,
        expression=eta_2,
      )
    )

```

## toda_53_n3_delta_injective_hopf_zero_inference_rule

- Production name: `Toda Proposition 5.3 n=3 Delta injectivity implies Hopf zero`
- Premise count: 2
- conclusion_pattern: `None`
- conclusion_builder: `True`
- match_guard: `True`

### premise_patterns

```json
[
  {
    "type": "proof.PremisePattern",
    "fields": {
      "proof_rule": "<ProofRule.INFERENCE: 'inference'>",
      "statement_type": "toda_rules.TodaDeltaInjectiveStatement",
      "statement_pattern": null,
      "relation_type": null,
      "relation_pattern": null
    }
  },
  {
    "type": "proof.PremisePattern",
    "fields": {
      "proof_rule": null,
      "statement_type": "toda_rules.TodaProp42ExactnessStatement",
      "statement_pattern": null,
      "relation_type": null,
      "relation_pattern": null
    }
  }
]
```

### factory_source

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30167`

```python
def toda_53_n3_delta_injective_hopf_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    injectivity = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    expected_source = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    if (
      window.first_map
      != EHP_H_MAP
    ):
      return False

    if (
      window.second_map
      != EHP_DELTA_MAP
    ):
      return False

    if (
      window.source_term
      != expected_source
    ):
      return False

    if (
      window.middle_term
      != expected_middle
    ):
      return False

    if (
      window.target_term
      != expected_target
    ):
      return False

    return (
      injectivity.map
      == TodaDeltaMap(
        source_group=expected_middle,
        target_group=expected_target,
      )
    )

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    return TodaHopfInvariantZeroStatement(
      map=TodaHopfInvariantMap(
        source_group=window.source_term,
        target_group=window.middle_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=3 Delta injectivity "
      "implies Hopf zero"
    ),
    description=(
      "In the concrete exact sequence "
      "pi_5^3 -> pi_5^5 -> pi_3^2, "
      "injectivity of Delta makes "
      "Ker(Delta) zero. Exactness "
      "therefore makes the image of H "
      "zero."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaInjectiveStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )

```

### conclusion_builder

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30239`

```python
  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    return TodaHopfInvariantZeroStatement(
      map=TodaHopfInvariantMap(
        source_group=window.source_term,
        target_group=window.middle_term,
      ),
    )

```

### match_guard

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30168`

```python
  def guard(
    premises,
    bindings,
  ):
    injectivity = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    expected_source = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    if (
      window.first_map
      != EHP_H_MAP
    ):
      return False

    if (
      window.second_map
      != EHP_DELTA_MAP
    ):
      return False

    if (
      window.source_term
      != expected_source
    ):
      return False

    if (
      window.middle_term
      != expected_middle
    ):
      return False

    if (
      window.target_term
      != expected_target
    ):
      return False

    return (
      injectivity.map
      == TodaDeltaMap(
        source_group=expected_middle,
        target_group=expected_target,
      )
    )

```

## toda_53_n3_hopf_zero_suspension_surjective_inference_rule

- Production name: `Toda Proposition 5.3 n=3 Hopf zero implies suspension surjective`
- Premise count: 2
- conclusion_pattern: `None`
- conclusion_builder: `True`
- match_guard: `True`

### premise_patterns

```json
[
  {
    "type": "proof.PremisePattern",
    "fields": {
      "proof_rule": "<ProofRule.INFERENCE: 'inference'>",
      "statement_type": "toda_rules.TodaHopfInvariantZeroStatement",
      "statement_pattern": null,
      "relation_type": null,
      "relation_pattern": null
    }
  },
  {
    "type": "proof.PremisePattern",
    "fields": {
      "proof_rule": null,
      "statement_type": "toda_rules.TodaProp42ExactnessStatement",
      "statement_pattern": null,
      "relation_type": null,
      "relation_pattern": null
    }
  }
]
```

### factory_source

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30289`

```python
def toda_53_n3_hopf_zero_suspension_surjective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    hopf_zero = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    expected_source = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=2,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )

    if (
      window.first_map
      != EHP_E_MAP
    ):
      return False

    if (
      window.second_map
      != EHP_H_MAP
    ):
      return False

    if (
      window.source_term
      != expected_source
    ):
      return False

    if (
      window.middle_term
      != expected_middle
    ):
      return False

    if (
      window.target_term
      != expected_target
    ):
      return False

    return (
      hopf_zero.map
      == TodaHopfInvariantMap(
        source_group=expected_middle,
        target_group=expected_target,
      )
    )

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    return TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=window.source_term,
        target_group=window.middle_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=3 Hopf zero "
      "implies suspension surjective"
    ),
    description=(
      "In the concrete exact sequence "
      "pi_4^2 -> pi_5^3 -> pi_5^5, "
      "if H is zero then Ker(H) is "
      "all of pi_5^3. Exactness "
      "therefore makes suspension E "
      "surjective."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaHopfInvariantZeroStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )

```

### conclusion_builder

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30361`

```python
  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    return TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=window.source_term,
        target_group=window.middle_term,
      ),
    )

```

### match_guard

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30290`

```python
  def guard(
    premises,
    bindings,
  ):
    hopf_zero = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    expected_source = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=2,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )

    if (
      window.first_map
      != EHP_E_MAP
    ):
      return False

    if (
      window.second_map
      != EHP_H_MAP
    ):
      return False

    if (
      window.source_term
      != expected_source
    ):
      return False

    if (
      window.middle_term
      != expected_middle
    ):
      return False

    if (
      window.target_term
      != expected_target
    ):
      return False

    return (
      hopf_zero.map
      == TodaHopfInvariantMap(
        source_group=expected_middle,
        target_group=expected_target,
      )
    )

```

## toda_53_n3_hopf_eta5_surjective_inference_rule

- Production name: `Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity`
- Premise count: 2
- conclusion_pattern: `None`
- conclusion_builder: `True`
- match_guard: `True`

### premise_patterns

```json
[
  {
    "type": "proof.PremisePattern",
    "fields": {
      "proof_rule": "<ProofRule.INFERENCE: 'inference'>",
      "statement_type": "proof.Relation",
      "statement_pattern": null,
      "relation_type": "<RelationType.EQUALITY: 'equality'>",
      "relation_pattern": null
    }
  },
  {
    "type": "proof.PremisePattern",
    "fields": {
      "proof_rule": "<ProofRule.INFERENCE: 'inference'>",
      "statement_type": "toda_rules.TodaProp51FiniteDimensionalStatement",
      "statement_pattern": null,
      "relation_type": null,
      "relation_pattern": null
    }
  }
]
```

### factory_source

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30411`

```python
def toda_53_n3_hopf_eta5_surjective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    hopf_relation = (
      premises[
        0
      ].conclusion
    )

    prop51_statement = (
      premises[
        1
      ].conclusion
    )

    nu_prime = HomotopyElement(
      name="ν′",
      dimension=3,
      source=6,
      target=3,
      generator=GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )

    eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    if (
      hopf_relation
      != Relation(
        lhs=MapApplication(
          map=EHP_H_MAP,
          expression=nu_prime,
        ),
        rhs=eta_5,
        relation_type=RelationType.EQUALITY,
      )
    ):
      return False

    higher_relation = (
      prop51_statement
      .higher_eta_group_relation
    )

    if not isinstance(
      higher_relation.lhs,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      higher_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    n = (
      higher_relation
      .lhs
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    expected_symbolic_group = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=1,
      ),
      sphere_dimension=n,
    )

    if (
      higher_relation.lhs
      != expected_symbolic_group
    ):
      return False

    if (
      higher_relation.rhs.order
      != 2
    ):
      return False

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=ScalarSum(
        left=n,
        right=1,
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    return (
      higher_relation
      .rhs
      .generator
      == eta_n
    )

  def build_conclusion(
    premises,
  ):
    return TodaHopfInvariantSurjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=TodaPrimaryGroup(
          group_dimension=6,
          sphere_dimension=3,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=6,
          sphere_dimension=5,
        ),
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=3 Hopf eta_5 surjectivity"
    ),
    description=(
      "Phase 58 gives H(nu-prime)=eta_5. "
      "Proposition 5.1 gives the "
      "order-two higher eta family, "
      "whose n=5 instance is "
      "pi_6^5=Z/2{eta_5}. Therefore "
      "H from pi_6^3 to pi_6^5 is "
      "surjective."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp51FiniteDimensionalStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )

```

### conclusion_builder

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30533`

```python
  def build_conclusion(
    premises,
  ):
    return TodaHopfInvariantSurjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=TodaPrimaryGroup(
          group_dimension=6,
          sphere_dimension=3,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=6,
          sphere_dimension=5,
        ),
      ),
    )

```

### match_guard

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30412`

```python
  def guard(
    premises,
    bindings,
  ):
    hopf_relation = (
      premises[
        0
      ].conclusion
    )

    prop51_statement = (
      premises[
        1
      ].conclusion
    )

    nu_prime = HomotopyElement(
      name="ν′",
      dimension=3,
      source=6,
      target=3,
      generator=GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )

    eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    if (
      hopf_relation
      != Relation(
        lhs=MapApplication(
          map=EHP_H_MAP,
          expression=nu_prime,
        ),
        rhs=eta_5,
        relation_type=RelationType.EQUALITY,
      )
    ):
      return False

    higher_relation = (
      prop51_statement
      .higher_eta_group_relation
    )

    if not isinstance(
      higher_relation.lhs,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      higher_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    n = (
      higher_relation
      .lhs
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    expected_symbolic_group = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=1,
      ),
      sphere_dimension=n,
    )

    if (
      higher_relation.lhs
      != expected_symbolic_group
    ):
      return False

    if (
      higher_relation.rhs.order
      != 2
    ):
      return False

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=ScalarSum(
        left=n,
        right=1,
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    return (
      higher_relation
      .rhs
      .generator
      == eta_n
    )

```

## toda_53_n3_hopf_surjective_delta_zero_inference_rule

- Production name: `Toda Proposition 5.3 n=3 Hopf surjective implies Delta zero`
- Premise count: 2
- conclusion_pattern: `None`
- conclusion_builder: `True`
- match_guard: `True`

### premise_patterns

```json
[
  {
    "type": "proof.PremisePattern",
    "fields": {
      "proof_rule": "<ProofRule.INFERENCE: 'inference'>",
      "statement_type": "toda_rules.TodaHopfInvariantSurjectiveStatement",
      "statement_pattern": null,
      "relation_type": null,
      "relation_pattern": null
    }
  },
  {
    "type": "proof.PremisePattern",
    "fields": {
      "proof_rule": null,
      "statement_type": "toda_rules.TodaProp42ExactnessStatement",
      "statement_pattern": null,
      "relation_type": null,
      "relation_pattern": null
    }
  }
]
```

### factory_source

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30583`

```python
def toda_53_n3_hopf_surjective_delta_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    surjectivity = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    expected_source = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=3,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=5,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=2,
    )

    if (
      window.first_map
      != EHP_H_MAP
    ):
      return False

    if (
      window.second_map
      != EHP_DELTA_MAP
    ):
      return False

    if (
      window.source_term
      != expected_source
    ):
      return False

    if (
      window.middle_term
      != expected_middle
    ):
      return False

    if (
      window.target_term
      != expected_target
    ):
      return False

    return (
      surjectivity.map
      == TodaHopfInvariantMap(
        source_group=expected_source,
        target_group=expected_middle,
      )
    )

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    return TodaDeltaZeroStatement(
      map=TodaDeltaMap(
        source_group=window.middle_term,
        target_group=window.target_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=3 Hopf surjective "
      "implies Delta zero"
    ),
    description=(
      "In the concrete exact sequence "
      "pi_6^3 -> pi_6^5 -> pi_4^2, "
      "surjectivity of H makes Im(H) "
      "all of pi_6^5. Exactness gives "
      "Ker(Delta)=pi_6^5, so Delta "
      "is zero."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaHopfInvariantSurjectiveStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )

```

### conclusion_builder

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30655`

```python
  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    return TodaDeltaZeroStatement(
      map=TodaDeltaMap(
        source_group=window.middle_term,
        target_group=window.target_term,
      ),
    )

```

### match_guard

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30584`

```python
  def guard(
    premises,
    bindings,
  ):
    surjectivity = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    expected_source = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=3,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=5,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=2,
    )

    if (
      window.first_map
      != EHP_H_MAP
    ):
      return False

    if (
      window.second_map
      != EHP_DELTA_MAP
    ):
      return False

    if (
      window.source_term
      != expected_source
    ):
      return False

    if (
      window.middle_term
      != expected_middle
    ):
      return False

    if (
      window.target_term
      != expected_target
    ):
      return False

    return (
      surjectivity.map
      == TodaHopfInvariantMap(
        source_group=expected_source,
        target_group=expected_middle,
      )
    )

```

## toda_53_n3_delta_zero_suspension_injective_inference_rule

- Production name: `Toda Proposition 5.3 n=3 Delta zero implies suspension injective`
- Premise count: 2
- conclusion_pattern: `None`
- conclusion_builder: `True`
- match_guard: `True`

### premise_patterns

```json
[
  {
    "type": "proof.PremisePattern",
    "fields": {
      "proof_rule": "<ProofRule.INFERENCE: 'inference'>",
      "statement_type": "toda_rules.TodaDeltaZeroStatement",
      "statement_pattern": null,
      "relation_type": null,
      "relation_pattern": null
    }
  },
  {
    "type": "proof.PremisePattern",
    "fields": {
      "proof_rule": null,
      "statement_type": "toda_rules.TodaProp42ExactnessStatement",
      "statement_pattern": null,
      "relation_type": null,
      "relation_pattern": null
    }
  }
]
```

### factory_source

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30705`

```python
def toda_53_n3_delta_zero_suspension_injective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_zero = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    expected_source = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=5,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=2,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    )

    if (
      window.first_map
      != EHP_DELTA_MAP
    ):
      return False

    if (
      window.second_map
      != EHP_E_MAP
    ):
      return False

    if (
      window.source_term
      != expected_source
    ):
      return False

    if (
      window.middle_term
      != expected_middle
    ):
      return False

    if (
      window.target_term
      != expected_target
    ):
      return False

    return (
      delta_zero.map
      == TodaDeltaMap(
        source_group=expected_source,
        target_group=expected_middle,
      )
    )

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    return TodaSuspensionInjectiveStatement(
      map=TodaSuspensionMap(
        source_group=window.middle_term,
        target_group=window.target_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=3 Delta zero "
      "implies suspension injective"
    ),
    description=(
      "In the concrete exact sequence "
      "pi_6^5 -> pi_4^2 -> pi_5^3, "
      "Delta zero makes Im(Delta) zero. "
      "Exactness therefore makes the "
      "kernel of suspension E zero, so "
      "E is injective."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaZeroStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )

```

### conclusion_builder

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30777`

```python
  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    return TodaSuspensionInjectiveStatement(
      map=TodaSuspensionMap(
        source_group=window.middle_term,
        target_group=window.target_term,
      ),
    )

```

### match_guard

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30706`

```python
  def guard(
    premises,
    bindings,
  ):
    delta_zero = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    expected_source = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=5,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=2,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    )

    if (
      window.first_map
      != EHP_DELTA_MAP
    ):
      return False

    if (
      window.second_map
      != EHP_E_MAP
    ):
      return False

    if (
      window.source_term
      != expected_source
    ):
      return False

    if (
      window.middle_term
      != expected_middle
    ):
      return False

    if (
      window.target_term
      != expected_target
    ):
      return False

    return (
      delta_zero.map
      == TodaDeltaMap(
        source_group=expected_source,
        target_group=expected_middle,
      )
    )

```

## toda_53_n3_suspension_isomorphism_inference_rule

- Production name: `Toda Proposition 5.3 n=3 suspension isomorphism`
- Premise count: 2
- conclusion_pattern: `None`
- conclusion_builder: `True`
- match_guard: `True`

### premise_patterns

```json
[
  {
    "type": "proof.PremisePattern",
    "fields": {
      "proof_rule": "<ProofRule.INFERENCE: 'inference'>",
      "statement_type": "toda_rules.TodaSuspensionInjectiveStatement",
      "statement_pattern": null,
      "relation_type": null,
      "relation_pattern": null
    }
  },
  {
    "type": "proof.PremisePattern",
    "fields": {
      "proof_rule": "<ProofRule.INFERENCE: 'inference'>",
      "statement_type": "toda_rules.TodaSuspensionSurjectiveStatement",
      "statement_pattern": null,
      "relation_type": null,
      "relation_pattern": null
    }
  }
]
```

### factory_source

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30827`

```python
def toda_53_n3_suspension_isomorphism_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    injectivity = (
      premises[
        0
      ].conclusion
    )

    surjectivity = (
      premises[
        1
      ].conclusion
    )

    expected_map = TodaSuspensionMap(
      source_group=TodaPrimaryGroup(
        group_dimension=4,
        sphere_dimension=2,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=5,
        sphere_dimension=3,
      ),
    )

    return (
      injectivity.map
      == expected_map
      and surjectivity.map
      == expected_map
    )

  def build_conclusion(
    premises,
  ):
    injectivity = (
      premises[
        0
      ].conclusion
    )

    return TodaSuspensionIsomorphismStatement(
      map=injectivity.map,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=3 suspension isomorphism"
    ),
    description=(
      "If the concrete suspension map "
      "from pi_4^2 to pi_5^3 is both "
      "injective and surjective, it is "
      "an isomorphism."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaSuspensionInjectiveStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaSuspensionSurjectiveStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )

```

### conclusion_builder

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30862`

```python
  def build_conclusion(
    premises,
  ):
    injectivity = (
      premises[
        0
      ].conclusion
    )

    return TodaSuspensionIsomorphismStatement(
      map=injectivity.map,
    )

```

### match_guard

Source: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof\toda_rules.py:30828`

```python
  def guard(
    premises,
    bindings,
  ):
    injectivity = (
      premises[
        0
      ].conclusion
    )

    surjectivity = (
      premises[
        1
      ].conclusion
    )

    expected_map = TodaSuspensionMap(
      source_group=TodaPrimaryGroup(
        group_dimension=4,
        sphere_dimension=2,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=5,
        sphere_dimension=3,
      ),
    )

    return (
      injectivity.map
      == expected_map
      and surjectivity.map
      == expected_map
    )

```

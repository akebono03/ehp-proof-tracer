# Phase 159-R1-7c R2 repair5 full provenance equality audit

Production code changes: none
Test changes: none
pytest: not run

nodes=178
edges=204

## Interesting equality nodes

### id=2569600666640 depth=2
- rule='equality transitivity'
- rendered="$2\\nu' = \\eta_{3}^{3}$"
- latex="2\\nu' = \\eta_{3}\\eta_{4}\\eta_{5}"
- premises=2
- premise 1: id=2569600624976 rule='Toda 5.3 nu-prime Lemma 5.2 double specialization' latex="2\\nu' = \\eta_{3}E\\eta_{3}\\eta_{5}"
- premise 2: id=2569600594032 rule='equality preserved under left composition' latex='\\eta_{3}E\\eta_{3}\\eta_{5} = \\eta_{3}\\eta_{4}\\eta_{5}'

### id=2569600624976 depth=3
- rule='Toda 5.3 nu-prime Lemma 5.2 double specialization'
- rendered="$2\\nu' = \\eta_{3}\\eta_{4}\\eta_{5}$"
- latex="2\\nu' = \\eta_{3}E\\eta_{3}\\eta_{5}"
- premises=2
- premise 1: id=2569600619312 rule='Toda 5.3 nu-prime Lemma 5.2 bracket specialization' latex="Toda53NuPrimeBracketSpecializationStatement(nu_prime=HomotopyElement(name='ν′', dimension=3, source=6, target=3, generator=GeneratorSymbol(family='ν', index=None, decoration='′')), alpha=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None)), lemma52_index=4, bracket_membership=TodaBracketMembershipStatement(element=HomotopyElement(name='ν′', dimension=3, source=6, target=3, generator=GeneratorSymbol(family='ν', index=None, decoration='′')), bracket=TodaBracket(first=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None)), second=Multiple(coefficient=2, expression=HomotopyElement(name='ι_4', dimension=4, source=None, target=None, generator=GeneratorSymbol(family='ι', index=4, decoration=None))), third=HomotopyElement(name='η₄', dimension=4, source=5, target=4, generator=GeneratorSymbol(family='η', index=4, decoration=None)), index=1), source=None, note=None))"
- premise 2: id=2569600620752 rule='Toda 5.3 eta_3 twice zero' latex="Relation(lhs=Multiple(coefficient=2, expression=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), rhs=Zero(), relation_type=<RelationType.ZERO: 'zero'>, source=None, note=None)"

### id=2569600594032 depth=3
- rule='equality preserved under left composition'
- rendered='$\\eta_{3}\\eta_{4}\\eta_{5} = \\eta_{3}^{3}$'
- latex='\\eta_{3}E\\eta_{3}\\eta_{5} = \\eta_{3}\\eta_{4}\\eta_{5}'
- premises=1
- premise 1: id=2569600616720 rule='equality preserved under right composition' latex='E\\eta_{3}\\eta_{5} = \\eta_{4}\\eta_{5}'

## Edges touching interesting equality nodes

- parent=2569601136624 parent_rule='Toda Proposition 5.6 nu-prime order four' premise_index=1 premise=2569600666640 premise_rule='equality transitivity'
- parent=2569600666640 parent_rule='equality transitivity' premise_index=0 premise=2569600624976 premise_rule='Toda 5.3 nu-prime Lemma 5.2 double specialization'
- parent=2569600666640 parent_rule='equality transitivity' premise_index=1 premise=2569600594032 premise_rule='equality preserved under left composition'
- parent=2569600624976 parent_rule='Toda 5.3 nu-prime Lemma 5.2 double specialization' premise_index=0 premise=2569600619312 premise_rule='Toda 5.3 nu-prime Lemma 5.2 bracket specialization'
- parent=2569600624976 parent_rule='Toda 5.3 nu-prime Lemma 5.2 double specialization' premise_index=1 premise=2569600620752 premise_rule='Toda 5.3 eta_3 twice zero'
- parent=2569600594032 parent_rule='equality preserved under left composition' premise_index=0 premise=2569600616720 premise_rule='equality preserved under right composition'

## Full-depth replay occurrences

- replay_depth=2 id=2569600666640 rule='equality transitivity' latex="2\\nu' = \\eta_{3}\\eta_{4}\\eta_{5}"
- replay_depth=3 id=2569600624976 rule='Toda 5.3 nu-prime Lemma 5.2 double specialization' latex="2\\nu' = \\eta_{3}E\\eta_{3}\\eta_{5}"
- replay_depth=3 id=2569600594032 rule='equality preserved under left composition' latex='\\eta_{3}E\\eta_{3}\\eta_{5} = \\eta_{3}\\eta_{4}\\eta_{5}'

# Phase 165 R14-R4 監査

- phase: 165 R14-R4
- reference_id: phase163:archive:toda:(5.1)
- source_clause_count: 6
- previous_schema_count: 2
- new_schema_count: 4
- total_schema_count: 6
- claims: [{'key': 'pi_i_n_zero', 'conditions': ['0 <= i < n', 'n >= 1'], 'assertion_repr': "Relation(lhs=TodaPrimaryGroup(group_dimension=2, sphere_dimension=3), rhs=0, relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)"}, {'key': 'negative_stem_zero', 'conditions': ['k < 0'], 'assertion_repr': "(Relation(lhs=StableStem(index=-1, prime=None), rhs=0, relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None), Relation(lhs=StableStem(index=-1, prime=2), rhs=0, relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None))"}, {'key': 'stable_zero_stem_cyclic', 'conditions': [], 'assertion_repr': "('G_0', '<iota>', 'isomorphic_Z')"}, {'key': 'stable_identity', 'conditions': ['n >= 1'], 'assertion_repr': "StableIdentity(stable_generator='iota', suspension_source='iota_3', source_dimension=3)"}]
- adjacent_source_status: USER_SUPPLIED_NOT_ARCHIVE_VERIFIED
- mathematically_certified: False
- new_proof_eligible: 0
- proof_steps_created: 0
- global_ehp_expansion_connected: False
- status: FOUR_SCHEMAS_TYPED_PROVENANCE_NOT_CERTIFIED
- full_pytest_run: False

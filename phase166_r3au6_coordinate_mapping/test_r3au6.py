from phase166_r3au6_coordinate_mapping.audit import inspect


def case(i, pos, n='4', k='3'):
    return {'n':n,'k':k,'id':str(i),'Element':'1 2','gen_coe':' '.join('1' if x==pos else '0' for x in range(12)), 'gen_coe_nonzero_positions_zero_based':f'[[{pos}, 1]]', 'reference_generator_optional':''}


def test_sorted_matching_positions_are_observations_not_certificates():
    summary, rows = inspect([case(0,0),case(1,1)])
    assert summary['counts']['rows_MATCHES_SORTED_POSITION'] == 2
    assert summary['mapping_certified'] is False


def test_unexpected_position_is_recorded_without_guessing():
    summary, rows = inspect([case(0,1),case(1,0)])
    assert summary['counts']['rows_OTHER_UNIT_POSITION'] == 2
    assert summary['counts']['groups_with_nonidentity_or_special_rows'] == 1


def test_zero_vector_and_empty_generator_are_allowed():
    row = case(0, 0)
    row['gen_coe'] = ' '.join(['0']*12)
    row['gen_coe_nonzero_positions_zero_based'] = '[]'
    summary, rows = inspect([row])
    assert rows[0]['classification'] == 'ZERO_VECTOR'
    assert summary['generator_reference_is_optional'] is True

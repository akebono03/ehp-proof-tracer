"""Shared historical EHP leaf construction, independent of Narrative rendering.

This module preserves Phase 162 leaf semantics; it does not certify the
underlying historical GIVEN facts or change the Phase 165 search.
"""

from homotopy_groups import TodaEHPExactnessWindow, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase162_reference_boundary import cite_verified_fixed_statement
from phase164_r8_proofstep_factory import create_legacy_given_proof_step
from probes.probe_phase55_capabilities import build_phase55_representative_result
from probes.probe_phase58_capabilities import build_phase58_representative_result
from proof import ProofRule
from toda_rules import TodaProp42ExactnessStatement


def _phase162_ehp_leaves():
    """Reuse the original independent EHP input leaves, not an iso conclusion."""
    prop51 = build_phase55_representative_result()["prop51_steps"][0]
    hopf_eta5 = cite_verified_fixed_statement(
        build_phase58_representative_result()["final_hopf_step"],
        reference_locator="(5.3)",
        component_key="nu_prime_hopf_relation",
        expected_conclusion=build_phase58_representative_result()["expected_final_hopf"],
    )
    pi_3_2 = TodaPrimaryGroup(group_dimension=3, sphere_dimension=2)
    pi_4_2 = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
    pi_5_3 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
    pi_5_5 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=5)
    pi_6_3 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=3)
    pi_6_5 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=5)
    windows = (
        (pi_5_3, pi_5_5, pi_3_2, EHP_H_MAP, EHP_DELTA_MAP),
        (pi_4_2, pi_5_3, pi_5_5, EHP_E_MAP, EHP_H_MAP),
        (pi_6_3, pi_6_5, pi_4_2, EHP_H_MAP, EHP_DELTA_MAP),
        (pi_6_5, pi_4_2, pi_5_3, EHP_DELTA_MAP, EHP_E_MAP),
    )
    exactness = tuple(
        create_legacy_given_proof_step(
            conclusion=TodaProp42ExactnessStatement(
                window=TodaEHPExactnessWindow(
                    source_term=source,
                    middle_term=middle,
                    target_term=target,
                    first_map=first,
                    second_map=second,
                )
            ),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for source, middle, target, first, second in windows
    )
    return prop51, hopf_eta5, exactness

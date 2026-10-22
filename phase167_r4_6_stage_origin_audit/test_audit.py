from phase167_r4_6_stage_origin_audit.audit import relevant_lines


def test_general_and_specialized_rows_are_both_selected():
    sample = (
        r"$\pi_{n}^{n} = \mathbb{Z}\{\iota_n\}$."
        + "\n"
        + r"$\pi_{5}^{5} = \mathbb{Z}\{\iota_5\}$."
    )
    assert len(relevant_lines(sample)) == 2


def test_irrelevant_lines_are_excluded():
    assert relevant_lines(r"$E(\eta_2)=\eta_3$.") == []

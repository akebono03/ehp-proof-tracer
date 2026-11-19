def _verified_source_sentence(statement: object) -> str | None:
    """Render only a uniquely verified, canonical typed source statement."""
    from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource

    if type(statement) is TodaLemma54TypedSource and statement == TodaLemma54TypedSource():
        return (
            r"$\nu_4\in\pi_7^4$, "
            r"$H(\nu_4)=\iota_7$ および "
            r"$2E\nu_4=E^2\nu'$."
        )

    from phase175_r4r12r10r1_cited_511_public.source import (
        CitedToda511, canonical_511, verify_cited_511,
    )
    if type(statement) is CitedToda511:
        if statement != CitedToda511(canonical_511()):
            return None
        verify_cited_511()
        return r"$\Delta(\eta_9)=E\nu'\eta_7$."

    from phase175_r4r10_cited_58_prop25_public.source import (
        CitedToda58SignedDelta, canonical_toda58, source_positions,
    )
    if type(statement) is CitedToda58SignedDelta:
        if statement != CitedToda58SignedDelta(canonical_toda58()):
            return None
        source_positions()
        return r"$\Delta(\iota_9)=\pm(2\nu_4-E\nu')$."
    return None

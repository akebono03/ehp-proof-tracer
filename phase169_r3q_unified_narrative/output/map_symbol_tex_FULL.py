def map_symbol_tex(map_object):
    if isinstance(map_object, TodaSuspensionMap):
        return "E"
    if isinstance(map_object, TodaHopfInvariantMap):
        return "H"
    if isinstance(map_object, TodaDeltaMap):
        return r"\Delta"
    return None


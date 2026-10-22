from collections import Counter

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_16_existing_prose_audit import audit_existing_typed_prose


def main():
    bridge = build_shared_typed_bridge()
    for n, k in ((2, 1), (3, 1), (2, 2), (4, 1)):
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        entries = audit_existing_typed_prose(result)
        counts = Counter(item.source for item in entries if item.prose is not None)
        failures = [item for item in entries if item.prose is None]
        print(f"PI_{n+k}^{n}: status={result.status.value} "
              f"previously_unrenderable={len(entries)} "
              f"reused={len(entries)-len(failures)} "
              f"sources={dict(counts)} failures={len(failures)}")
        for item in entries:
            print(f"  STEP {item.step_index}: {item.type_name} "
                  f"source={item.source} "
                  f"prose={item.prose!r} error={item.error!r}")
    print("R3-16 EXISTING TYPED PROSE AUDIT ONLY")


if __name__ == "__main__":
    main()
